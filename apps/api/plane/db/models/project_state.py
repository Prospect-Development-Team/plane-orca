# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models import Q
from .base import BaseModel


class ProjectStateGroup(models.TextChoices):
    BACKLOG = "backlog", "Backlog"
    UNSTARTED = "unstarted", "Unstarted"
    STARTED = "started", "Started"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


DEFAULT_PROJECT_STATES = [
    {
        "name": "Backlog",
        "color": "#60646C",
        "sequence": 15000,
        "group": ProjectStateGroup.BACKLOG.value,
        "default": True,
    },
    {
        "name": "Todo",
        "color": "#60646C",
        "sequence": 25000,
        "group": ProjectStateGroup.UNSTARTED.value,
        "default": False,
    },
    {
        "name": "In Progress",
        "color": "#F59E0B",
        "sequence": 35000,
        "group": ProjectStateGroup.STARTED.value,
        "default": False,
    },
    {
        "name": "Done",
        "color": "#46A758",
        "sequence": 45000,
        "group": ProjectStateGroup.COMPLETED.value,
        "default": False,
    },
    {
        "name": "Cancelled",
        "color": "#9AA4BC",
        "sequence": 55000,
        "group": ProjectStateGroup.CANCELLED.value,
        "default": False,
    },
]


class ProjectState(BaseModel):
    workspace = models.ForeignKey(
        "db.Workspace",
        on_delete=models.CASCADE,
        related_name="project_states",
    )
    name = models.CharField(max_length=255, verbose_name="Project State Name")
    description = models.TextField(verbose_name="Project State Description", blank=True)
    color = models.CharField(max_length=255, verbose_name="Project State Color")
    slug = models.SlugField(max_length=100, blank=True)
    sequence = models.FloatField(default=65535)
    group = models.CharField(
        choices=ProjectStateGroup.choices,
        default=ProjectStateGroup.BACKLOG,
        max_length=20,
    )
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} <{self.workspace.name}>"

    class Meta:
        unique_together = ["name", "workspace", "deleted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "workspace"],
                condition=Q(deleted_at__isnull=True),
                name="project_state_unique_name_workspace_when_deleted_at_null",
            )
        ]
        verbose_name = "Project State"
        verbose_name_plural = "Project States"
        db_table = "project_states"
        ordering = ("sequence",)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self._state.adding:
            last_id = ProjectState.objects.filter(workspace=self.workspace).aggregate(largest=models.Max("sequence"))["largest"]
            if last_id is not None:
                self.sequence = last_id + 10000
        return super().save(*args, **kwargs)


class WorkspaceProjectStateSettings(BaseModel):
    workspace = models.OneToOneField(
        "db.Workspace",
        on_delete=models.CASCADE,
        related_name="project_state_settings",
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Workspace Project State Settings"
        verbose_name_plural = "Workspace Project State Settings"
        db_table = "workspace_project_state_settings"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.workspace.name} - is_enabled={self.is_enabled}"


class ProjectStateProperty(BaseModel):
    project = models.OneToOneField(
        "db.Project",
        on_delete=models.CASCADE,
        related_name="state_property",
    )
    state = models.ForeignKey(
        "db.ProjectState",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    is_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Project State Property"
        verbose_name_plural = "Project State Properties"
        db_table = "project_state_properties"
        ordering = ("-created_at",)

    def __str__(self):
        state_name = self.state.name if self.state else "None"
        return f"{self.project.name} - state={state_name} - is_enabled={self.is_enabled}"
