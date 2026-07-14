# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import json
from datetime import datetime

# Django imports
from django.utils import timezone

# Third Party imports
from rest_framework.response import Response
from rest_framework import status

# Module imports
from .. import BaseAPIView
from plane.app.permissions import (
    ProjectEntityPermission,
)
from plane.db.models import (
    Project,
    Issue,
    IssueLabel,
    IssueAssignee,
    IssueSubscriber,
    State,
    CycleIssue,
    ModuleIssue,
)
from plane.bgtasks.issue_activities_task import issue_activity


class BulkIssueOperationsEndpoint(BaseAPIView):
    permission_classes = [
        ProjectEntityPermission,
    ]

    def post(self, request, slug, project_id):
        issue_ids = request.data.get("issue_ids", [])
        if not len(issue_ids):
            return Response(
                {"error": "Issue IDs are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get all the issues
        issues = (
            Issue.objects.filter(
                workspace__slug=slug, project_id=project_id, pk__in=issue_ids
            )
            .select_related("state")
            .prefetch_related("labels", "assignees")
        )
        # Current epoch
        epoch = int(timezone.now().timestamp())

        # Project details
        project = Project.objects.get(workspace__slug=slug, pk=project_id)
        workspace_id = project.workspace_id

        # Initialize arrays
        bulk_update_issues = []
        bulk_issue_activities = []
        bulk_update_issue_labels = []
        bulk_update_issue_assignees = []

        properties = request.data.get("properties", {})

        if properties.get("start_date", False) and properties.get(
            "target_date", False
        ):
            if (
                datetime.strptime(
                    properties.get("start_date"), "%Y-%m-%d"
                ).date()
                > datetime.strptime(
                    properties.get("target_date"), "%Y-%m-%d"
                ).date()
            ):
                return Response(
                    {
                        "error_code": 4100,
                        "error_message": "INVALID_ISSUE_DATES",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        for issue in issues:
            # Priority
            if properties.get("priority", False):
                bulk_issue_activities.append(
                    {
                        "type": "issue.activity.updated",
                        "requested_data": json.dumps(
                            {"priority": properties.get("priority")}
                        ),
                        "current_instance": json.dumps(
                            {"priority": (issue.priority)}
                        ),
                        "issue_id": str(issue.id),
                        "actor_id": str(request.user.id),
                        "project_id": str(project_id),
                        "epoch": epoch,
                    }
                )
                issue.priority = properties.get("priority")

            # Subscription
            if "is_subscribed" in properties:
                is_subscribed = properties.get("is_subscribed")
                if is_subscribed:
                    IssueSubscriber.objects.get_or_create(
                        issue=issue,
                        subscriber=request.user,
                        project_id=project_id,
                        workspace_id=workspace_id,
                    )
                else:
                    IssueSubscriber.objects.filter(
                        issue=issue,
                        subscriber=request.user,
                        project_id=project_id,
                    ).delete()

            # State
            if properties.get("state_id", False):
                try:
                    state_obj = State.objects.get(pk=properties.get("state_id"), project_id=project_id)
                    bulk_issue_activities.append(
                        {
                            "type": "issue.activity.updated",
                            "requested_data": json.dumps(
                                {"state": properties.get("state")}
                            ),
                            "current_instance": json.dumps(
                                {"state": str(issue.state_id)}
                            ),
                            "issue_id": str(issue.id),
                            "actor_id": str(request.user.id),
                            "project_id": str(project_id),
                            "epoch": epoch,
                        }
                    )
                    issue.state = state_obj
                except State.DoesNotExist:
                    pass

            # Start date
            if "start_date" in properties:
                start_date_val = properties.get("start_date")
                start_date_val = start_date_val if start_date_val else None
                if start_date_val:
                    if (
                        issue.target_date
                        and not properties.get("target_date", False)
                        and issue.target_date
                        <= datetime.strptime(
                            start_date_val, "%Y-%m-%d"
                        ).date()
                    ):
                        return Response(
                            {
                                "error_code": 4101,
                                "error_message": "INVALID_ISSUE_START_DATE",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                bulk_issue_activities.append(
                    {
                        "type": "issue.activity.updated",
                        "requested_data": json.dumps(
                            {"start_date": start_date_val}
                        ),
                        "current_instance": json.dumps(
                            {"start_date": str(issue.start_date)}
                        ),
                        "issue_id": str(issue.id),
                        "actor_id": str(request.user.id),
                        "project_id": str(project_id),
                        "epoch": epoch,
                    }
                )
                issue.start_date = start_date_val

            # Target date
            if "target_date" in properties:
                target_date_val = properties.get("target_date")
                target_date_val = target_date_val if target_date_val else None
                if target_date_val:
                    if (
                        issue.start_date
                        and not properties.get("start_date", False)
                        and issue.start_date
                        >= datetime.strptime(
                            target_date_val, "%Y-%m-%d"
                        ).date()
                    ):
                        return Response(
                            {
                                "error_code": 4102,
                                "error_message": "INVALID_ISSUE_TARGET_DATE",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                bulk_issue_activities.append(
                    {
                        "type": "issue.activity.updated",
                        "requested_data": json.dumps(
                            {"target_date": target_date_val}
                        ),
                        "current_instance": json.dumps(
                            {"target_date": str(issue.target_date)}
                        ),
                        "issue_id": str(issue.id),
                        "actor_id": str(request.user.id),
                        "project_id": str(project_id),
                        "epoch": epoch,
                    }
                )
                issue.target_date = target_date_val

            # Cycles
            if "cycle_id" in properties:
                cycle_id = properties.get("cycle_id")
                # Delete existing CycleIssue for the issue
                CycleIssue.objects.filter(issue=issue, project_id=project_id).delete()
                if cycle_id:
                    CycleIssue.objects.create(
                        issue=issue,
                        cycle_id=cycle_id,
                        project_id=project_id,
                        workspace_id=workspace_id,
                    )

            # Modules
            if "module_ids" in properties:
                module_ids = properties.get("module_ids", [])
                ModuleIssue.objects.filter(
                    issue=issue,
                    project_id=project_id,
                ).exclude(module_id__in=module_ids).delete()

                # Get existing module IDs for the issue
                existing_module_ids = {
                    str(mi.module_id)
                    for mi in ModuleIssue.objects.filter(issue=issue, project_id=project_id)
                }
                new_module_ids = [
                    m_id for m_id in module_ids
                    if str(m_id) not in existing_module_ids
                ]
                for module_id in new_module_ids:
                    ModuleIssue.objects.create(
                        issue=issue,
                        module_id=module_id,
                        project_id=project_id,
                        workspace_id=workspace_id,
                    )

            bulk_update_issues.append(issue)

            # Labels
            if "label_ids" in properties:
                label_ids = properties.get("label_ids", [])
                IssueLabel.objects.filter(
                    issue=issue,
                    project_id=project_id,
                ).exclude(label_id__in=label_ids).delete()

                existing_label_ids = {
                    str(il.label_id)
                    for il in IssueLabel.objects.filter(issue=issue, project_id=project_id)
                }
                new_label_ids = [
                    l_id for l_id in label_ids
                    if str(l_id) not in existing_label_ids
                ]
                for label_id in new_label_ids:
                    bulk_update_issue_labels.append(
                        IssueLabel(
                            issue=issue,
                            label_id=label_id,
                            created_by=request.user,
                            project_id=project_id,
                            workspace_id=workspace_id,
                        )
                    )
                bulk_issue_activities.append(
                    {
                        "type": "issue.activity.updated",
                        "requested_data": json.dumps(
                            {"label_ids": label_ids}
                        ),
                        "current_instance": json.dumps(
                            {
                                "label_ids": [
                                    str(label.id)
                                    for label in issue.labels.all()
                                ]
                            }
                        ),
                        "issue_id": str(issue.id),
                        "actor_id": str(request.user.id),
                        "project_id": str(project_id),
                        "epoch": epoch,
                    }
                )

            # Assignees
            if "assignee_ids" in properties:
                assignee_ids = properties.get("assignee_ids", [])
                IssueAssignee.objects.filter(
                    issue=issue,
                    project_id=project_id,
                ).exclude(assignee_id__in=assignee_ids).delete()

                existing_assignee_ids = {
                    str(ia.assignee_id)
                    for ia in IssueAssignee.objects.filter(issue=issue, project_id=project_id)
                }
                new_assignee_ids = [
                    a_id for a_id in assignee_ids
                    if str(a_id) not in existing_assignee_ids
                ]
                for assignee_id in new_assignee_ids:
                    bulk_update_issue_assignees.append(
                        IssueAssignee(
                            issue=issue,
                            assignee_id=assignee_id,
                            created_by=request.user,
                            project_id=project_id,
                            workspace_id=workspace_id,
                        )
                    )
                bulk_issue_activities.append(
                    {
                        "type": "issue.activity.updated",
                        "requested_data": json.dumps(
                            {
                                "assignee_ids": assignee_ids
                            }
                        ),
                        "current_instance": json.dumps(
                            {
                                "assignee_ids": [
                                    str(assignee.id)
                                    for assignee in issue.assignees.all()
                                ]
                            }
                        ),
                        "issue_id": str(issue.id),
                        "actor_id": str(request.user.id),
                        "project_id": str(project_id),
                        "epoch": epoch,
                    }
                )

        # Bulk update all the objects
        Issue.objects.bulk_update(
            bulk_update_issues,
            [
                "priority",
                "start_date",
                "target_date",
                "state",
            ],
            batch_size=100,
        )

        # Create new labels
        IssueLabel.objects.bulk_create(
            bulk_update_issue_labels,
            ignore_conflicts=True,
            batch_size=100,
        )

        # Create new assignees
        IssueAssignee.objects.bulk_create(
            bulk_update_issue_assignees,
            ignore_conflicts=True,
            batch_size=100,
        )
        # update the issue activity
        [
            issue_activity.delay(**activity)
            for activity in bulk_issue_activities
        ]

        return Response(status=status.HTTP_204_NO_CONTENT)
