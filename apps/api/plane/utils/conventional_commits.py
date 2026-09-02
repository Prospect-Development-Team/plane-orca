# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import re

# Django imports
from django.db.models import Count, Q


# Standard conventional commit types with semantic UI colors
CONVENTIONAL_COMMIT_PREFIXES = {
    "feat": "#3B82F6",      # Blue
    "fix": "#EF4444",       # Red
    "docs": "#8B5CF6",      # Purple
    "style": "#EC4899",     # Pink
    "refactor": "#F59E0B",  # Amber
    "perf": "#10B981",      # Emerald
    "test": "#6366F1",      # Indigo
    "build": "#F97316",     # Orange
    "ci": "#06B6D4",        # Cyan
    "chore": "#64748B",     # Slate
    "revert": "#6B7280",    # Gray
}

# Regex pattern matching conventional commit format: <type>(<scope>)!?: <description>
CONVENTIONAL_COMMIT_REGEX = re.compile(
    r"^([a-zA-Z]+)(?:\([^\)]+\))?!?:\s+\S+",
    re.IGNORECASE
)


def extract_conventional_commit_type(title: str) -> str | None:
    """
    @description Extracts the conventional commit type from a work item title if it conforms to the standard.
    Strictly matches from the start of the title and requires description content after the prefix.
    @param {str} title - The title of the work item.
    @returns {str | None} The lowercased commit type (e.g. 'feat', 'fix') or None if no match.
    """
    if not title:
        return None
    match = CONVENTIONAL_COMMIT_REGEX.match(title.strip())
    if match:
        commit_type = match.group(1).lower()
        if commit_type in CONVENTIONAL_COMMIT_PREFIXES:
            return commit_type
    return None


def apply_conventional_commit_label(issue, old_title: str | None = None):
    """
    @description Checks if auto-labeling is enabled for the issue's project and assigns the matching
    conventional commit label (creating the project label if it does not yet exist).
    If the issue title previously matched a different conventional commit prefix, removes the old prefix label.
    @param {Issue} issue - The Issue model instance.
    @param {str | None} old_title - The previous title of the work item before this update.
    @returns {Label | None} The assigned Label instance or None if not applicable.
    """
    from plane.db.models import ProjectCustomSettings, Label, IssueLabel

    if not issue or not getattr(issue, "project_id", None):
        return None

    # Check if auto conventional commit labels is enabled for this project
    custom_settings = ProjectCustomSettings.objects.filter(
        project_id=issue.project_id
    ).first()
    if not custom_settings or not custom_settings.auto_conventional_commit_labels:
        return None

    commit_type = extract_conventional_commit_type(issue.name)

    # If the work item was renamed from a previous conventional commit prefix, remove the old label
    if old_title:
        old_commit_type = extract_conventional_commit_type(old_title)
        if old_commit_type and old_commit_type != commit_type:
            IssueLabel.objects.filter(
                issue_id=issue.id,
                label__name__iexact=old_commit_type,
            ).delete()

    if not commit_type:
        return None

    # Get or create the project label with standard color
    color = CONVENTIONAL_COMMIT_PREFIXES.get(commit_type, "#64748B")
    label, _ = Label.objects.get_or_create(
        project_id=issue.project_id,
        name__iexact=commit_type,
        defaults={
            "name": commit_type,
            "color": color,
            "workspace_id": issue.workspace_id,
        }
    )

    # Attach the label to the issue if not already assigned
    existing_issue_label = IssueLabel.objects.filter(
        issue_id=issue.id,
        label_id=label.id,
        deleted_at__isnull=True
    ).exists()

    if not existing_issue_label:
        IssueLabel.objects.create(
            issue=issue,
            label=label,
            project_id=issue.project_id,
            workspace_id=issue.workspace_id,
            created_by_id=issue.created_by_id,
            updated_by_id=issue.updated_by_id,
        )

    return label


def auto_label_conventional_commits_for_project(project):
    """
    @description Scans all existing work items in a project that currently have no labels,
    and assigns conventional commit labels to those matching conventional commit prefixes.
    @param {Project} project - The Project model instance.
    """
    from plane.db.models import Issue, Label, IssueLabel

    if not project or not getattr(project, "id", None):
        return

    # Find all active issues in the project that currently have no active labels
    unlabeled_issues = (
        Issue.issue_objects.filter(project_id=project.id)
        .annotate(
            active_label_count=Count(
                "labels",
                filter=Q(labels__deleted_at__isnull=True, label_issue__deleted_at__isnull=True)
            )
        )
        .filter(active_label_count=0)
    )

    for issue in unlabeled_issues:
        commit_type = extract_conventional_commit_type(issue.name)
        if not commit_type:
            continue

        color = CONVENTIONAL_COMMIT_PREFIXES.get(commit_type, "#64748B")
        label, _ = Label.objects.get_or_create(
            project_id=project.id,
            name__iexact=commit_type,
            defaults={
                "name": commit_type,
                "color": color,
                "workspace_id": project.workspace_id,
            }
        )

        IssueLabel.objects.get_or_create(
            issue=issue,
            label=label,
            defaults={
                "project_id": project.id,
                "workspace_id": project.workspace_id,
                "created_by_id": issue.created_by_id,
                "updated_by_id": issue.updated_by_id,
            }
        )
