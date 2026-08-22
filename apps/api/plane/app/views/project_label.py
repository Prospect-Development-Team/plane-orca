# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from plane.db.models import Workspace, Project, Label, ProjectProjectLabel, WorkspaceProjectLabelSettings, ProjectLabelProperty
from plane.app.permissions import WorkSpaceAdminPermission, WorkspaceEntityPermission, ProjectBasePermission
from plane.app.serializers import (
    WorkspaceProjectLabelSerializer,
    WorkspaceProjectLabelSettingsSerializer,
    ProjectLabelPropertySerializer,
    ProjectProjectLabelSerializer,
)
from .base import BaseAPIView, BaseViewSet


def propagate_workspace_label_change(workspace_label, action="save"):
    from plane.db.models import ProjectLabelProperty, Label
    workspace = workspace_label.workspace
    enabled_project_ids = ProjectLabelProperty.objects.filter(
        project__workspace=workspace, is_enabled=True
    ).values_list("project_id", flat=True)

    for project_id in enabled_project_ids:
        if action == "save":
            parent_lbl = None
            if workspace_label.parent:
                parent_lbl = Label.objects.filter(project_id=project_id, name=workspace_label.parent.name).first()
            
            Label.objects.update_or_create(
                project_id=project_id,
                name=workspace_label.name,
                defaults={
                    "color": workspace_label.color,
                    "description": workspace_label.description or "",
                    "parent": parent_lbl,
                    "workspace": workspace,
                }
            )
        elif action == "delete":
            Label.objects.filter(project_id=project_id, name=workspace_label.name).delete()


def sync_workspace_labels_to_project(workspace, project):
    from plane.db.models import Label
    workspace_labels = Label.objects.filter(workspace=workspace, project__isnull=True)
    
    # First pass: create or update project-level labels matching workspace labels non-destructively
    created_labels = {}
    for wl in workspace_labels:
        lbl, _ = Label.objects.update_or_create(
            project=project,
            name=wl.name,
            defaults={
                "color": wl.color,
                "description": wl.description or "",
                "workspace": workspace,
            }
        )
        created_labels[wl.name] = lbl
        
    # Second pass: set parents
    for wl in workspace_labels:
        if wl.parent:
            lbl = created_labels.get(wl.name)
            parent_lbl = created_labels.get(wl.parent.name)
            if lbl and parent_lbl:
                lbl.parent = parent_lbl
                lbl.save()


class WorkspaceProjectLabelSettingsEndpoint(BaseAPIView):
    permission_classes = [WorkSpaceAdminPermission]

    def get(self, request, slug):
        workspace = Workspace.objects.get(slug=slug)
        settings_obj, created = WorkspaceProjectLabelSettings.objects.get_or_create(
            workspace=workspace,
            defaults={"is_enabled": False}
        )
        serializer = WorkspaceProjectLabelSettingsSerializer(settings_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug):
        workspace = Workspace.objects.get(slug=slug)
        settings_obj, _ = WorkspaceProjectLabelSettings.objects.get_or_create(
            workspace=workspace,
            defaults={"is_enabled": False}
        )
        serializer = WorkspaceProjectLabelSettingsSerializer(settings_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceProjectLabelViewSet(BaseViewSet):
    serializer_class = WorkspaceProjectLabelSerializer
    model = Label

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [WorkspaceEntityPermission]
        else:
            self.permission_classes = [WorkSpaceAdminPermission]
        return super().get_permissions()

    def get_queryset(self):
        return Label.objects.filter(
            workspace__slug=self.workspace_slug,
            project__isnull=True,
        )

    def perform_create(self, serializer):
        workspace = Workspace.objects.get(slug=self.workspace_slug)
        instance = serializer.save(workspace=workspace, project=None)
        propagate_workspace_label_change(instance, "save")

    def perform_update(self, serializer):
        instance = serializer.save()
        propagate_workspace_label_change(instance, "save")

    def perform_destroy(self, instance):
        propagate_workspace_label_change(instance, "delete")
        instance.delete()


class ProjectLabelPropertyEndpoint(BaseAPIView):
    permission_classes = [ProjectBasePermission]

    def get(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        prop, _ = ProjectLabelProperty.objects.get_or_create(
            project=project,
            defaults={"is_enabled": False}
        )
        serializer = ProjectLabelPropertySerializer(prop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        prop, _ = ProjectLabelProperty.objects.get_or_create(
            project=project,
            defaults={"is_enabled": False}
        )
        was_enabled = prop.is_enabled
        serializer = ProjectLabelPropertySerializer(prop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if not was_enabled and prop.is_enabled:
                sync_workspace_labels_to_project(project.workspace, project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectProjectLabelEndpoint(BaseAPIView):
    permission_classes = [ProjectBasePermission]

    def get(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        mappings = ProjectProjectLabel.objects.filter(project=project)
        serializer = ProjectProjectLabelSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, slug, project_id):
        project = Project.objects.get(id=project_id, workspace__slug=slug)
        label_ids = request.data.get("label_ids", [])
        
        # Validate that the labels belong to this workspace and are workspace-level (project=None)
        workspace_labels = Label.objects.filter(workspace__slug=slug, project__isnull=True, id__in=label_ids)
        valid_label_ids = set(str(l.id) for l in workspace_labels)
        
        # Get existing mappings
        existing_mappings = ProjectProjectLabel.objects.filter(project=project)
        existing_label_ids = set(str(m.label_id) for m in existing_mappings)
        
        # Mappings to delete
        to_delete = existing_mappings.filter(label_id__in=existing_label_ids - valid_label_ids)
        to_delete.delete()
        
        # Mappings to create
        to_create = []
        for l_id in (valid_label_ids - existing_label_ids):
            label_obj = next(l for l in workspace_labels if str(l.id) == l_id)
            to_create.append(ProjectProjectLabel(project=project, label=label_obj))
            
        if to_create:
            ProjectProjectLabel.objects.bulk_create(to_create)
            
        # Return updated list of mappings
        updated_mappings = ProjectProjectLabel.objects.filter(project=project)
        serializer = ProjectProjectLabelSerializer(updated_mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
