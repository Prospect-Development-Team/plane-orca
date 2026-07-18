# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from rest_framework import serializers
from plane.db.models import ProjectState, WorkspaceProjectStateSettings, ProjectStateProperty
from .base import BaseSerializer


class ProjectStateSerializer(BaseSerializer):
    class Meta:
        model = ProjectState
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "workspace", "deleted_at"]


class WorkspaceProjectStateSettingsSerializer(BaseSerializer):
    class Meta:
        model = WorkspaceProjectStateSettings
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "workspace", "deleted_at"]


class ProjectStatePropertySerializer(BaseSerializer):
    state_detail = ProjectStateSerializer(source="state", read_only=True)

    class Meta:
        model = ProjectStateProperty
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "project", "deleted_at"]
