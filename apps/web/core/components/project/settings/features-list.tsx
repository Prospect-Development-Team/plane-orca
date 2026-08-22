/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect } from "react";
import { observer } from "mobx-react";
// plane imports
import { useTranslation } from "@plane/i18n";
import { setPromiseToast } from "@plane/propel/toast";
import { Tooltip } from "@plane/propel/tooltip";
import type { IProject } from "@plane/types";
import { CycleIcon, IntakeIcon, ModuleIcon, PageIcon, ViewsIcon } from "@plane/propel/icons";
import { Layers, Tags } from "lucide-react";
import { ToggleSwitch } from "@plane/ui";
import { useCustomProjectState } from "@/hooks/store/use-custom-project-state";
import { useCustomProjectLabel } from "@/hooks/store/use-custom-project-label";
// components
import { SettingsBoxedControlItem } from "@/components/settings/boxed-control-item";
import { SettingsHeading } from "@/components/settings/heading";
// hooks
import { useProject } from "@/hooks/store/use-project";
// plane web imports
import { UpgradeBadge } from "@/components/workspace/upgrade-badge";
// local imports
import { ProjectFeatureToggle } from "./helper";

type Props = {
  workspaceSlug: string;
  projectId: string;
  isAdmin: boolean;
};

const PROJECT_FEATURES_LIST = {
  cycles: {
    key: "cycles",
    property: "cycle_view",
    title: "Cycles",
    description: "Timebox work as you see fit per project and change frequency from one period to the next.",
    icon: <CycleIcon className="h-5 w-5 flex-shrink-0 rotate-180 text-tertiary" />,
    isPro: false,
    isEnabled: true,
  },
  modules: {
    key: "modules",
    property: "module_view",
    title: "Modules",
    description: "Group work into sub-project-like set-ups with their own leads and assignees.",
    icon: <ModuleIcon width={20} height={20} className="flex-shrink-0 text-tertiary" />,
    isPro: false,
    isEnabled: true,
  },
  views: {
    key: "views",
    property: "issue_views_view",
    title: "Views",
    description: "Save sorts, filters, and display options for later or share them.",
    icon: <ViewsIcon className="h-5 w-5 flex-shrink-0 text-tertiary" />,
    isPro: false,
    isEnabled: true,
  },
  pages: {
    key: "pages",
    property: "page_view",
    title: "Pages",
    description: "Write anything like you write anything.",
    icon: <PageIcon className="h-5 w-5 flex-shrink-0 text-tertiary" />,
    isPro: false,
    isEnabled: true,
  },
  inbox: {
    key: "intake",
    property: "inbox_view",
    title: "Intake",
    description: "Consider and discuss work items before you add them to your project.",
    icon: <IntakeIcon className="h-5 w-5 flex-shrink-0 text-tertiary" />,
    isPro: false,
    isEnabled: true,
  },
};

export const ProjectFeaturesList = observer(function ProjectFeaturesList(props: Props) {
  const { workspaceSlug, projectId, isAdmin } = props;
  // store hooks
  const { t } = useTranslation();
  const { getProjectById, updateProject } = useProject();
  // derived values
  const currentProjectDetails = getProjectById(projectId);

  const customStore = useCustomProjectState();
  const labelStore = useCustomProjectLabel();

  useEffect(() => {
    if (workspaceSlug && projectId) {
      customStore.fetchSettings(workspaceSlug);
      customStore.fetchProjectProperty(workspaceSlug, projectId);
      labelStore.fetchSettings(workspaceSlug);
      labelStore.fetchProjectProperty(workspaceSlug, projectId);
    }
  }, [workspaceSlug, projectId, customStore, labelStore]);

  const projectProperty = customStore.projectProperties[projectId];
  const isProjectStateEnabled = projectProperty ? projectProperty.is_enabled : false;

  const projectLabelProperty = labelStore.projectProperties[projectId];
  const isProjectLabelEnabled = projectLabelProperty ? projectLabelProperty.is_enabled : false;

  const handleSubmit = async (featureKey: string, property: string, value: boolean) => {
    if (!workspaceSlug || !projectId) return;

    const promise = updateProject(workspaceSlug, projectId, {
      [property]: value,
    });

    const featureName = t(`project_settings.features.${featureKey}.title`);

    setPromiseToast(promise, {
      loading: t("project_settings.features.toast.loading", { feature: featureName }),
      success: {
        title: t("project_settings.features.toast.success_title"),
        message: () => t("project_settings.features.toast.success", { feature: featureName }),
      },
      error: {
        title: t("project_settings.features.toast.error_title"),
        message: () => t("project_settings.features.toast.error", { feature: featureName }),
      },
    });
  };

  return (
    <>
      <div className="flex flex-col gap-6">
        <SettingsHeading
          title={t("project_settings.features.title")}
          description={t("project_settings.features.description")}
        />

        <div className="flex flex-col gap-4">
          {Object.values(PROJECT_FEATURES_LIST).map((featureItem) => (
            <div key={featureItem.key}>
              <SettingsBoxedControlItem
                title={
                  <span className="flex items-center gap-2">
                    {featureItem.icon}
                    {featureItem.title}
                    {featureItem.isPro && (
                      <Tooltip tooltipContent="Available on plan paid" theme="dark">
                        <UpgradeBadge className="rounded-sm" />
                      </Tooltip>
                    )}
                  </span>
                }
                description={t(`${featureItem.key}_description`)}
                control={
                  <ProjectFeatureToggle
                    workspaceSlug={workspaceSlug}
                    projectId={projectId}
                    featureItem={featureItem}
                    value={Boolean(currentProjectDetails?.[featureItem.property as keyof IProject])}
                    handleSubmit={handleSubmit}
                    disabled={!isAdmin}
                  />
                }
              />
              {/* {currentProjectDetails?.[featureItem.property as keyof IProject] && (
                <div className="pl-14">{featureItem.renderChildren?.(currentProjectDetails, workspaceSlug)}</div>
              )} */}
            </div>
          ))}
          {customStore.settings?.is_enabled && (
            <div key="project-states">
              <SettingsBoxedControlItem
                title={
                  <span className="flex items-center gap-2">
                    <Layers className="h-5 w-5 flex-shrink-0 text-tertiary" />
                    Project States
                  </span>
                }
                description="Classify and track this project's progress using workspace-level states."
                control={
                  <ToggleSwitch
                    value={isProjectStateEnabled}
                    onChange={async () => {
                      if (!workspaceSlug || !projectId) return;
                      await customStore.updateProjectProperty(workspaceSlug, projectId, {
                        is_enabled: !isProjectStateEnabled,
                      });
                    }}
                    disabled={!isAdmin}
                  />
                }
              />
            </div>
          )}
          {labelStore.settings?.is_enabled && (
            <div key="project-labels">
              <SettingsBoxedControlItem
                title={
                  <span className="flex items-center gap-2">
                    <Tags className="h-5 w-5 flex-shrink-0 text-tertiary" />
                    Project Labels
                  </span>
                }
                description="Categorize and group this project using workspace-level labels."
                control={
                  <ToggleSwitch
                    value={isProjectLabelEnabled}
                    onChange={async () => {
                      if (!workspaceSlug || !projectId) return;
                      await labelStore.updateProjectLabelProperty(workspaceSlug, projectId, {
                        is_enabled: !isProjectLabelEnabled,
                      });
                    }}
                    disabled={!isAdmin}
                  />
                }
              />
            </div>
          )}
        </div>
      </div>
    </>
  );
});
