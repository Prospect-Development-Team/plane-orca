# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from plane.db.models import Workspace, Project, ProjectState, WorkspaceProjectStateSettings, ProjectStateProperty, DEFAULT_PROJECT_STATES
from plane.app.permissions import WorkSpaceAdminPermission, WorkspaceEntityPermission, ProjectBasePermission
from plane.app.serializers import (
    ProjectStateSerializer,
    WorkspaceProjectStateSettingsSerializer,
    ProjectStatePropertySerializer,
)
from .base import BaseAPIView, BaseViewSet


class WorkspaceProjectStateSettingsEndpoint(BaseAPIView):
    permission_classes = [WorkSpaceAdminPermission]

    def get(self, request, slug):
        workspace = Workspace.objects.get(slug=slug)
        settings_obj, created = WorkspaceProjectStateSettings.objects.get_or_create(
            workspace=workspace,
            defaults={"is_enabled": False}
        )

        # Seed default project states if it is a new workspace or if there are no states
        if not ProjectState.objects.filter(workspace=workspace).exists():
            for state_data in DEFAULT_PROJECT_STATES:
                ProjectState.objects.create(
                    workspace=workspace,
                    name=state_data["name"],
                    color=state_data["color"],
                    group=state_data["group"],
                    sequence=state_data["sequence"],
                    default=state_data["default"],
                )

        serializer = WorkspaceProjectStateSettingsSerializer(settings_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        workspace = Workspace.objects.get(slug=slug)
        settings_obj, _ = WorkspaceProjectStateSettings.objects.get_or_create(
            workspace=workspace,
            defaults={"is_enabled": False}
        )
        serializer = WorkspaceProjectStateSettingsSerializer(settings_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils.text import slugify

def propagate_workspace_state_change(workspace_state, action="save"):
    from plane.db.models import ProjectStateProperty, State, Issue, ProjectState
    workspace = workspace_state.workspace
    enabled_project_ids = ProjectStateProperty.objects.filter(
        project__workspace=workspace, is_enabled=True
    ).values_list("project_id", flat=True)

    for project_id in enabled_project_ids:
        state_slug = slugify(workspace_state.name)
        if action == "save":
            State.objects.update_or_create(
                project_id=project_id,
                slug=state_slug,
                defaults={
                    "name": workspace_state.name,
                    "color": workspace_state.color,
                    "group": workspace_state.group,
                    "default": workspace_state.default,
                    "sequence": workspace_state.sequence,
                    "description": workspace_state.description or "",
                    "workspace": workspace,
                }
            )
        elif action == "delete":
            ps = State.objects.filter(project_id=project_id, slug=state_slug).first()
            if ps:
                default_ws = ProjectState.objects.filter(workspace=workspace, default=True).first()
                default_slug = slugify(default_ws.name) if default_ws else ""
                default_ps = State.objects.filter(project_id=project_id, slug=default_slug).first()
                if default_ps:
                    Issue.objects.filter(state=ps).update(state=default_ps)
                ps.delete()


def sync_workspace_states_to_project(workspace, project):
    from plane.db.models import ProjectState, State, Issue
    workspace_states = ProjectState.objects.filter(workspace=workspace)
    project_states = State.objects.filter(project=project)

    workspace_states_by_slug = {slugify(ws.name): ws for ws in workspace_states}
    project_states_by_slug = {slugify(ps.name): ps for ps in project_states}

    default_ws = workspace_states.filter(default=True).first() or workspace_states.first()
    default_project_state = None
    if default_ws:
        default_slug = slugify(default_ws.name)
        if default_slug in project_states_by_slug:
            default_project_state = project_states_by_slug[default_slug]
        else:
            default_project_state = State.objects.create(
                name=default_ws.name,
                color=default_ws.color,
                group=default_ws.group,
                default=default_ws.default,
                sequence=default_ws.sequence,
                description=default_ws.description or "",
                project=project,
                workspace=workspace,
            )
            project_states_by_slug[default_slug] = default_project_state

    for ws_slug, ws in workspace_states_by_slug.items():
        if ws_slug in project_states_by_slug:
            ps = project_states_by_slug[ws_slug]
            ps.name = ws.name
            ps.color = ws.color
            ps.group = ws.group
            ps.default = ws.default
            ps.sequence = ws.sequence
            ps.description = ws.description or ""
            ps.save()
        else:
            ps = State.objects.create(
                name=ws.name,
                color=ws.color,
                group=ws.group,
                default=ws.default,
                sequence=ws.sequence,
                description=ws.description or "",
                project=project,
                workspace=workspace,
            )
            project_states_by_slug[ws_slug] = ps

    for ps_slug, ps in list(project_states_by_slug.items()):
        if ps_slug not in workspace_states_by_slug:
            if default_project_state and ps.id != default_project_state.id:
                Issue.objects.filter(state=ps).update(state=default_project_state)
                ps.delete()


class ProjectStateViewSet(BaseViewSet):
    serializer_class = ProjectStateSerializer
    model = ProjectState

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [WorkspaceEntityPermission]
        else:
            self.permission_classes = [WorkSpaceAdminPermission]
        return super().get_permissions()

    def get_queryset(self):
        return ProjectState.objects.filter(
            workspace__slug=self.workspace_slug
        )

    def perform_create(self, serializer):
        workspace = Workspace.objects.get(slug=self.workspace_slug)
        if serializer.validated_data.get("default", False):
            ProjectState.objects.filter(workspace=workspace).update(default=False)
        instance = serializer.save(workspace=workspace)
        propagate_workspace_state_change(instance, "save")

    def perform_update(self, serializer):
        workspace = Workspace.objects.get(slug=self.workspace_slug)
        if serializer.validated_data.get("default", False):
            ProjectState.objects.filter(workspace=workspace).update(default=False)
        instance = serializer.save()
        propagate_workspace_state_change(instance, "save")

    def perform_destroy(self, instance):
        propagate_workspace_state_change(instance, "delete")
        instance.delete()


class ProjectStatePropertyEndpoint(BaseAPIView):
    permission_classes = [ProjectBasePermission]

    def get(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        default_state = ProjectState.objects.filter(workspace__slug=slug, default=True).first()
        prop, _ = ProjectStateProperty.objects.get_or_create(
            project=project,
            defaults={"state": default_state, "is_enabled": False}
        )
        serializer = ProjectStatePropertySerializer(prop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        default_state = ProjectState.objects.filter(workspace__slug=slug, default=True).first()
        prop, _ = ProjectStateProperty.objects.get_or_create(
            project=project,
            defaults={"state": default_state, "is_enabled": False}
        )
        was_enabled = prop.is_enabled
        serializer = ProjectStatePropertySerializer(prop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # If toggled on, synchronize the states
            if not was_enabled and prop.is_enabled:
                sync_workspace_states_to_project(project.workspace, project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
