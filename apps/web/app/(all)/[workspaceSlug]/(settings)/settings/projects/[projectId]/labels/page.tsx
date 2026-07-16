/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect, useRef, useState, useMemo } from "react";
import { combine } from "@atlaskit/pragmatic-drag-and-drop/combine";
import { autoScrollForElements } from "@atlaskit/pragmatic-drag-and-drop-auto-scroll/element";
import { observer } from "mobx-react";
import { useParams } from "react-router";
import React from "react";
import { AlertTriangle } from "lucide-react";

// components
import { EUserPermissions, EUserPermissionsLevel } from "@plane/constants";
import { NotAuthorizedView } from "@/components/auth-screens/not-authorized-view";
import { PageHead } from "@/components/core/page-title";
import { ProjectSettingsLabelList } from "@/components/labels";
import { SettingsContentWrapper } from "@/components/settings/content-wrapper";
import { SettingsHeading } from "@/components/settings/heading";
import { ToggleSwitch } from "@plane/ui";
import { TOAST_TYPE, setToast } from "@plane/propel/toast";

// hooks
import { useProject } from "@/hooks/store/use-project";
import { useUserPermissions } from "@/hooks/store/user";
import { useCustomProjectLabel } from "@/hooks/store/use-custom-project-label";
import { useTranslation } from "@plane/i18n";

// local imports
import { LabelsProjectSettingsHeader } from "./header";

function LabelsSettingsPage() {
  const { workspaceSlug, projectId } = useParams();

  // store hooks
  const { currentProjectDetails } = useProject();
  const { workspaceUserInfo, allowPermissions } = useUserPermissions();
  const labelStore = useCustomProjectLabel();
  const { t } = useTranslation();

  const [loadingProperty, setLoadingProperty] = useState(true);

  useEffect(() => {
    if (workspaceSlug && projectId) {
      Promise.all([
        labelStore.fetchSettings(workspaceSlug.toString()),
        labelStore.fetchProjectProperty(workspaceSlug.toString(), projectId.toString()),
        labelStore.fetchLabels(workspaceSlug.toString()),
      ]).finally(() => {
        setLoadingProperty(false);
      });
    }
  }, [workspaceSlug, projectId, labelStore]);

  const pageTitle = currentProjectDetails?.name ? `${currentProjectDetails?.name} - Labels` : undefined;

  const scrollableContainerRef = useRef<HTMLDivElement | null>(null);

  // derived values
  const canPerformProjectMemberActions = allowPermissions(
    [EUserPermissions.ADMIN, EUserPermissions.MEMBER],
    EUserPermissionsLevel.PROJECT
  );

  // Enable Auto Scroll for Labels list
  useEffect(() => {
    const element = scrollableContainerRef.current;

    if (!element) return;

    return combine(
      autoScrollForElements({
        element,
      })
    );
  }, []);

  const dummyLabelOperationsCallbacks = useMemo(
    () => ({
      createLabel: async () => {
        throw new Error("Not allowed");
      },
      updateLabel: async () => {
        throw new Error("Not allowed");
      },
    }),
    []
  );

  if (workspaceUserInfo && !canPerformProjectMemberActions) {
    return <NotAuthorizedView section="settings" isProjectView className="h-auto" />;
  }

  const projectProperty = projectId ? labelStore.projectProperties[projectId] : undefined;
  const isWorkspaceLabelsEnabled = labelStore.settings?.is_enabled || false;
  const isProjectUsingWorkspaceLabels = projectProperty ? projectProperty.is_enabled : true;

  const isLocalEditDisabled = isWorkspaceLabelsEnabled && isProjectUsingWorkspaceLabels;

  const handleToggle = async () => {
    if (!workspaceSlug || !projectId) return;
    try {
      await labelStore.updateProjectLabelProperty(workspaceSlug.toString(), projectId.toString(), {
        is_enabled: !isProjectUsingWorkspaceLabels,
      });
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Success",
        message: `Workspace Project Labels ${!isProjectUsingWorkspaceLabels ? "enabled" : "disabled"} successfully for this project.`,
      });
    } catch (_e) {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error",
        message: "Failed to update project labels setting.",
      });
    }
  };

  return (
    <SettingsContentWrapper header={<LabelsProjectSettingsHeader />}>
      <PageHead title={pageTitle} />
      <div className="flex w-full flex-col gap-6">
        {isLocalEditDisabled && (
          <SettingsHeading
            title={t("project_settings.labels.heading") || "Labels"}
            description={
              t("project_settings.labels.description") || "Define and customize labels to categorize your work items."
            }
          />
        )}

        {isWorkspaceLabelsEnabled && (
          <div className="bg-custom-background-90 flex items-center justify-between rounded-xl border border-subtle p-4">
            <div>
              <h4 className="text-sm text-custom-text-100 font-semibold">Use Workspace Project Labels</h4>
              <p className="text-xs text-custom-text-300">
                When enabled, workspace-level project labels will be assigned and shown on this project card.
              </p>
            </div>
            {!loadingProperty && (
              <ToggleSwitch
                value={isProjectUsingWorkspaceLabels}
                onChange={handleToggle}
                disabled={!canPerformProjectMemberActions}
              />
            )}
          </div>
        )}

        <div className={isLocalEditDisabled ? "opacity-60" : ""}>
          {isLocalEditDisabled && (
            <div className="bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 text-sm mb-6 flex items-start gap-2.5 rounded-md p-3">
              <AlertTriangle className="mt-0.5 size-4 shrink-0" />
              <div className="flex flex-col gap-0.5">
                <span className="font-semibold">Workspace Project Labels Active</span>
                <span className="text-xs opacity-90">
                  This project is currently using workspace-level project labels. Editing is disabled. Turn off the
                  toggle above to customize labels locally.
                </span>
              </div>
            </div>
          )}

          <div ref={scrollableContainerRef} className="size-full">
            <ProjectSettingsLabelList
              title={isLocalEditDisabled ? null : undefined}
              description={isLocalEditDisabled ? null : undefined}
              labels={isLocalEditDisabled ? labelStore.labels || [] : undefined}
              labelsTree={isLocalEditDisabled ? labelStore.labelsTree || [] : undefined}
              labelOperationsCallbacks={isLocalEditDisabled ? dummyLabelOperationsCallbacks : undefined}
              onDrop={isLocalEditDisabled ? () => {} : undefined}
              isEditable={!isLocalEditDisabled}
            />
          </div>
        </div>
      </div>
    </SettingsContentWrapper>
  );
}

export default observer(LabelsSettingsPage);
