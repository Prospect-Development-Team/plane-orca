/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect, useState, useMemo } from "react";
import { observer } from "mobx-react";
import { EUserPermissions, EUserPermissionsLevel } from "@plane/constants";
import { useTranslation } from "@plane/i18n";
import { AlertTriangle } from "lucide-react";
// components
import { NotAuthorizedView } from "@/components/auth-screens/not-authorized-view";
import { PageHead } from "@/components/core/page-title";
import { ProjectStateRoot, GroupList } from "@/components/project-states";
import { SettingsContentWrapper } from "@/components/settings/content-wrapper";
import { SettingsHeading } from "@/components/settings/heading";
import { ToggleSwitch, AlertModalCore } from "@plane/ui";
// hook
import { useProject } from "@/hooks/store/use-project";
import { useUserPermissions } from "@/hooks/store/user";
import { useCustomProjectState } from "@/hooks/store/use-custom-project-state";
import { useProjectState } from "@/hooks/store/use-project-state";
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
// local imports
import type { Route } from "./+types/page";
import { StatesProjectSettingsHeader } from "./header";

function StatesSettingsPage({ params }: Route.ComponentProps) {
  const { workspaceSlug, projectId } = params;
  // store
  const { currentProjectDetails } = useProject();
  const { workspaceUserInfo, allowPermissions } = useUserPermissions();
  const { fetchProjectStates } = useProjectState();

  const customStore = useCustomProjectState();
  const [loadingProperty, setLoadingProperty] = useState(true);

  useEffect(() => {
    if (workspaceSlug && projectId) {
      Promise.all([
        customStore.fetchSettings(workspaceSlug),
        customStore.fetchStates(workspaceSlug),
        customStore.fetchProjectProperty(workspaceSlug, projectId),
      ]).finally(() => {
        setLoadingProperty(false);
      });
    }
  }, [workspaceSlug, projectId, customStore]);

  const { t } = useTranslation();

  // derived values
  const pageTitle = currentProjectDetails?.name ? `${currentProjectDetails?.name} - States` : undefined;
  // derived values
  const canPerformProjectMemberActions = allowPermissions(
    [EUserPermissions.ADMIN, EUserPermissions.MEMBER],
    EUserPermissionsLevel.PROJECT
  );

  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleToggle = () => {
    setIsConfirmationModalOpen(true);
  };

  const handleConfirmToggle = async () => {
    if (!workspaceSlug || !projectId) return;
    setIsSubmitting(true);
    try {
      const currentProp = customStore.projectProperties[projectId];
      const nextValue = currentProp ? !currentProp.is_enabled : true;
      await customStore.updateProjectProperty(workspaceSlug, projectId, {
        is_enabled: nextValue,
      });
      // Trigger re-fetch of standard project states to update the cache
      await fetchProjectStates(workspaceSlug, projectId);
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Success",
        message: `Project States feature ${nextValue ? "enabled" : "disabled"} successfully.`,
      });
    } catch (_e) {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error",
        message: "Failed to update project state settings.",
      });
    } finally {
      setIsSubmitting(false);
      setIsConfirmationModalOpen(false);
    }
  };

  const workspaceMappedStates = useMemo(() => {
    return (
      customStore.states?.map((st) => ({
        id: st.id,
        name: st.name,
        description: st.description || "",
        color: st.color,
        group: st.group as any,
        default: st.default,
        sequence: st.sequence,
        project_id: "",
        workspace_id: "",
        order: st.sequence,
      })) || []
    );
  }, [customStore.states]);

  const workspaceGroupedStates = useMemo(() => {
    const groups: Record<string, any[]> = {
      backlog: [],
      unstarted: [],
      started: [],
      completed: [],
      cancelled: [],
    };
    workspaceMappedStates.forEach((state) => {
      if (groups[state.group]) {
        groups[state.group].push(state);
      }
    });
    return groups;
  }, [workspaceMappedStates]);

  const dummyStateOperationsCallbacks = useMemo(
    () => ({
      createState: async () => {
        throw new Error("Not allowed");
      },
      updateState: async () => {
        throw new Error("Not allowed");
      },
      deleteState: async () => {
        throw new Error("Not allowed");
      },
      markStateAsDefault: async () => {
        throw new Error("Not allowed");
      },
      moveStatePosition: async () => {
        throw new Error("Not allowed");
      },
    }),
    []
  );

  if (workspaceUserInfo && !canPerformProjectMemberActions) {
    return <NotAuthorizedView section="settings" isProjectView className="h-auto" />;
  }

  const projectProperty = customStore.projectProperties[projectId];
  const isWorkspaceStatesEnabled = customStore.settings?.is_enabled || false;
  const isProjectUsingWorkspaceStates = projectProperty ? projectProperty.is_enabled : false;

  // If the workspace-level setting is enabled AND this project is using workspace states, local states edit is disabled
  const isLocalEditDisabled = isWorkspaceStatesEnabled && isProjectUsingWorkspaceStates;

  return (
    <SettingsContentWrapper header={<StatesProjectSettingsHeader />}>
      <PageHead title={pageTitle} />
      <div className="flex w-full flex-col gap-6">
        <div className="flex flex-col gap-1">
          <SettingsHeading
            title={t("project_settings.states.heading")}
            description={t("project_settings.states.description")}
          />
        </div>

        {isWorkspaceStatesEnabled && (
          <div className="bg-custom-background-90 flex items-center justify-between rounded-xl border border-subtle p-4">
            <div>
              <h4 className="text-sm text-custom-text-100 font-semibold">Use Workspace Project States</h4>
              <p className="text-xs text-custom-text-300">
                When enabled, project-level state management is locked and controlled globally from the workspace.
              </p>
            </div>
            {!loadingProperty && (
              <ToggleSwitch
                value={isProjectUsingWorkspaceStates}
                onChange={handleToggle}
                disabled={!canPerformProjectMemberActions}
              />
            )}
          </div>
        )}

        <div className={isLocalEditDisabled ? "opacity-60" : ""}>
          {isLocalEditDisabled ? (
            <>
              <div className="bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 text-sm mb-6 flex items-start gap-2.5 rounded-md p-3">
                <AlertTriangle className="mt-0.5 size-4 shrink-0" />
                <div className="flex flex-col gap-0.5">
                  <span className="font-semibold">Workspace Project States Active</span>
                  <span className="text-xs opacity-90">
                    This project is currently using workspace-level project states. Editing is disabled. Turn off the
                    toggle above to customize states locally.
                  </span>
                </div>
              </div>
              <GroupList
                groupedStates={workspaceGroupedStates}
                stateOperationsCallbacks={dummyStateOperationsCallbacks as any}
                isEditable={false}
                shouldTrackEvents={false}
              />
            </>
          ) : (
            <ProjectStateRoot workspaceSlug={workspaceSlug} projectId={projectId} isEditableOverride={true} />
          )}
        </div>
      </div>
      {isConfirmationModalOpen && (
        <AlertModalCore
          isOpen={isConfirmationModalOpen}
          handleClose={() => setIsConfirmationModalOpen(false)}
          handleSubmit={handleConfirmToggle}
          isSubmitting={isSubmitting}
          title="Confirm Toggle Project States"
          content={`Are you sure you want to ${isProjectUsingWorkspaceStates ? "disable" : "enable"} workspace project states for this project? This will change how states are managed. Work items in this project might have their states updated or moved.`}
          variant="primary"
          primaryButtonText={{
            loading: "Updating...",
            default: "Confirm",
          }}
        />
      )}
    </SettingsContentWrapper>
  );
}

export default observer(StatesSettingsPage);
