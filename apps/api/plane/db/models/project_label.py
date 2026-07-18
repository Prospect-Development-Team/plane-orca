# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.db import models
from django.db.models import Q
from .base import BaseModel


class WorkspaceProjectLabelSettings(BaseModel):
    workspace = models.OneToOneField(
        "db.Workspace",
        on_delete=models.CASCADE,
        related_name="project_label_settings",
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Workspace Project Label Settings"
        verbose_name_plural = "Workspace Project Label Settings"
        db_table = "workspace_project_label_settings"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.workspace.name} - is_enabled={self.is_enabled}"


class ProjectLabelProperty(BaseModel):
    project = models.OneToOneField(
        "db.Project",
        on_delete=models.CASCADE,
        related_name="label_property",
    )
    is_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Project Label Property"
        verbose_name_plural = "Project Label Properties"
        db_table = "project_label_properties"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.project.name} - is_enabled={self.is_enabled}"


class ProjectProjectLabel(BaseModel):
    project = models.ForeignKey(
        "db.Project",
        on_delete=models.CASCADE,
        related_name="project_project_labels",
    )
    label = models.ForeignKey(
        "db.Label",
        on_delete=models.CASCADE,
        related_name="project_label_mappings",
    )

    class Meta:
        unique_together = ["project", "label", "deleted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "label"],
                condition=Q(deleted_at__isnull=True),
                name="project_project_label_unique_project_label_when_deleted_at_null",
            )
        ]
        verbose_name = "Project Project Label"
        verbose_name_plural = "Project Project Labels"
        db_table = "project_project_labels"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.project.name} - {self.label.name}"
