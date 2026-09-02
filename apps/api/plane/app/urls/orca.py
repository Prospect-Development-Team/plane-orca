# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.urls import path
from plane.app.views import (
    WorkspaceProjectStateSettingsEndpoint,
    ProjectStateViewSet,
    ProjectStatePropertyEndpoint,
    WorkspaceProjectLabelSettingsEndpoint,
    WorkspaceProjectLabelViewSet,
    ProjectLabelPropertyEndpoint,
    ProjectProjectLabelEndpoint,
)

urlpatterns = [
    # Workspace Project State Settings
    path(
        "orca/workspaces/<str:slug>/project-states/settings/",
        WorkspaceProjectStateSettingsEndpoint.as_view(),
        name="workspace-project-state-settings",
    ),
    # Workspace Project States CRUD
    path(
        "orca/workspaces/<str:slug>/project-states/",
        ProjectStateViewSet.as_view({"get": "list", "post": "create"}),
        name="workspace-project-states",
    ),
    path(
        "orca/workspaces/<str:slug>/project-states/<uuid:pk>/",
        ProjectStateViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="workspace-project-state",
    ),
    # Project-level Project State Properties
    path(
        "orca/workspaces/<str:slug>/projects/<uuid:project_id>/project-state/",
        ProjectStatePropertyEndpoint.as_view(),
        name="project-project-state-property",
    ),
    # Workspace Project Label Settings
    path(
        "orca/workspaces/<str:slug>/project-labels/settings/",
        WorkspaceProjectLabelSettingsEndpoint.as_view(),
        name="workspace-project-label-settings",
    ),
    # Workspace Project Labels CRUD
    path(
        "orca/workspaces/<str:slug>/project-labels/",
        WorkspaceProjectLabelViewSet.as_view({"get": "list", "post": "create"}),
        name="workspace-project-labels",
    ),
    path(
        "orca/workspaces/<str:slug>/project-labels/<uuid:pk>/",
        WorkspaceProjectLabelViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="workspace-project-label",
    ),
    # Project-level Project Label Properties
    path(
        "orca/workspaces/<str:slug>/projects/<uuid:project_id>/project-labels/",
        ProjectProjectLabelEndpoint.as_view(),
        name="project-project-labels",
    ),
    path(
        "orca/workspaces/<str:slug>/projects/<uuid:project_id>/project-label/",
        ProjectLabelPropertyEndpoint.as_view(),
        name="project-project-label-property",
    ),
]

