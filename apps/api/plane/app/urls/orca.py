# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.urls import path
from plane.app.views import (
    WorkspaceProjectStateSettingsEndpoint,
    ProjectStateViewSet,
    ProjectStatePropertyEndpoint,
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
]
