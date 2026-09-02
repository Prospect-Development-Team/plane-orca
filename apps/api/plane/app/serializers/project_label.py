# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from rest_framework import serializers
from plane.db.models import Label, ProjectProjectLabel, WorkspaceProjectLabelSettings, ProjectLabelProperty
from .base import BaseSerializer


class WorkspaceProjectLabelSerializer(BaseSerializer):
    class Meta:
        model = Label
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "workspace", "project", "deleted_at"]


class WorkspaceProjectLabelSettingsSerializer(BaseSerializer):
    class Meta:
        model = WorkspaceProjectLabelSettings
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "workspace", "deleted_at"]


class ProjectLabelPropertySerializer(BaseSerializer):
    class Meta:
        model = ProjectLabelProperty
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "project", "deleted_at"]


class ProjectProjectLabelSerializer(BaseSerializer):
    label_detail = WorkspaceProjectLabelSerializer(source="label", read_only=True)

    class Meta:
        model = ProjectProjectLabel
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "project", "deleted_at"]
