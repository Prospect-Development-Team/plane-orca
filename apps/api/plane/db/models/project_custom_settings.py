# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Django imports
from django.db import models

# Module imports
from .project import ProjectBaseModel


class ProjectCustomSettings(ProjectBaseModel):
    """
    Relational sidecar table for storing project-specific custom overrides and configurations.
    Designed in compliance with FORK.md to store customization metadata without modifying 
    the core Project database schema directly.
    
    Attributes:
        project (Project): One-to-one relation to the core Project model.
        parallel_cycles (bool): Flag indicating whether the project allows multiple active cycles concurrently.
    """
    project = models.OneToOneField(
        "db.Project",
        on_delete=models.CASCADE,
        related_name="custom_settings",
    )
    parallel_cycles = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Project Custom Settings"
        verbose_name_plural = "Project Custom Settings"
        db_table = "project_custom_settings"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.project.name} - parallel_cycles={self.parallel_cycles}"
