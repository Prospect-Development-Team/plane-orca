/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observer } from "mobx-react";
// plane imports
import { EUserPermissionsLevel, EUserPermissions } from "@plane/constants";
import { useTranslation } from "@plane/i18n";
import { EmptyStateDetailed } from "@plane/propel/empty-state";
import { ContentWrapper } from "@plane/ui";
// components
import { calculateTotalFilters } from "@plane/utils";
import { ProjectsLoader } from "@/components/ui/loader/projects-loader";
// hooks
import { useCommandPalette } from "@/hooks/store/use-command-palette";
import { useProject } from "@/hooks/store/use-project";
import { useProjectFilter } from "@/hooks/store/use-project-filter";
import { useUserPermissions } from "@/hooks/store/user";
// local imports
import { ProjectCard } from "./card";

import { useLocalStorage } from "@plane/hooks";
import { useCustomProjectLabel } from "@/hooks/store/use-custom-project-label";

type TProjectCardListProps = {
  totalProjectIds?: string[];
  filteredProjectIds?: string[];
};

export const ProjectCardList = observer(function ProjectCardList(props: TProjectCardListProps) {
  const { totalProjectIds: totalProjectIdsProps, filteredProjectIds: filteredProjectIdsProps } = props;
  // plane hooks
  const { t } = useTranslation();
  // store hooks
  const { toggleCreateProjectModal } = useCommandPalette();
  const {
    loader,
    fetchStatus,
    workspaceProjectIds: storeWorkspaceProjectIds,
    filteredProjectIds: storeFilteredProjectIds,
    getProjectById,
  } = useProject();
  const { currentWorkspaceDisplayFilters, currentWorkspaceFilters } = useProjectFilter();
  const { allowPermissions } = useUserPermissions();
  const labelStore = useCustomProjectLabel();

  // local storage group_by
  const { storedValue: groupBy } = useLocalStorage<"none" | "label">("project_list_group_by", "none");

  // derived values
  const workspaceProjectIds = totalProjectIdsProps ?? storeWorkspaceProjectIds;
  const filteredProjectIds = filteredProjectIdsProps ?? storeFilteredProjectIds;

  // permissions
  const canPerformEmptyStateActions = allowPermissions(
    [EUserPermissions.ADMIN, EUserPermissions.MEMBER],
    EUserPermissionsLevel.WORKSPACE
  );

  if (!filteredProjectIds || !workspaceProjectIds || loader === "init-loader" || fetchStatus !== "complete")
    return <ProjectsLoader />;

  if (workspaceProjectIds?.length === 0 && !currentWorkspaceDisplayFilters?.archived_projects)
    return (
      <EmptyStateDetailed
        title={t("workspace_projects.empty_state.general.title")}
        description={t("workspace_projects.empty_state.general.description")}
        assetKey="project"
        assetClassName="size-40"
        actions={[
          {
            label: t("workspace_projects.empty_state.general.primary_button.text"),
            onClick: () => {
              toggleCreateProjectModal(true);
            },
            disabled: !canPerformEmptyStateActions,
            variant: "primary",
          },
        ]}
      />
    );

  if (filteredProjectIds.length === 0)
    return (
      <EmptyStateDetailed
        title={
          currentWorkspaceDisplayFilters?.archived_projects &&
          calculateTotalFilters(currentWorkspaceFilters ?? {}) === 0
            ? t("workspace_empty_state.projects_archived.title")
            : t("common_empty_state.search.title")
        }
        description={
          currentWorkspaceDisplayFilters?.archived_projects &&
          calculateTotalFilters(currentWorkspaceFilters ?? {}) === 0
            ? t("workspace_empty_state.projects_archived.description")
            : t("common_empty_state.search.description")
        }
        assetKey={
          currentWorkspaceDisplayFilters?.archived_projects &&
          calculateTotalFilters(currentWorkspaceFilters ?? {}) === 0
            ? "archived-work-item"
            : "search"
        }
        assetClassName="size-40"
      />
    );

  if (groupBy === "label") {
    // Group projects by label
    const grouped: Record<string, string[]> = { "no-label": [] };
    labelStore.labels?.forEach((lbl) => {
      grouped[lbl.id] = [];
    });

    filteredProjectIds.forEach((pId) => {
      const assignments = labelStore.projectLabelAssignments[pId] || [];
      const labelIds = assignments.map((a: any) => a.label);
      if (labelIds.length === 0) {
        grouped["no-label"].push(pId);
      } else {
        labelIds.forEach((lId: string) => {
          if (grouped[lId]) {
            grouped[lId].push(pId);
          } else {
            // fallback if label wasn't pre-initialized
            grouped[lId] = [pId];
          }
        });
      }
    });

    const labelGroups = [
      ...(labelStore.labels || []).map((lbl) => ({
        id: lbl.id,
        name: lbl.name,
        color: lbl.color,
        projectIds: grouped[lbl.id] || [],
      })),
      {
        id: "no-label",
        name: "No Label",
        color: "#6b7280",
        projectIds: grouped["no-label"] || [],
      },
    ].filter((g) => g.projectIds.length > 0);

    return (
      <ContentWrapper>
        <div className="flex flex-col gap-10">
          {labelGroups.map((group) => (
            <div key={group.id} className="flex flex-col gap-4">
              <div className="flex items-center gap-2 border-b border-subtle pb-2">
                <span className="size-3 rounded-full" style={{ backgroundColor: group.color }} />
                <h4 className="text-md text-custom-text-100 font-semibold">
                  {group.name} ({group.projectIds.length})
                </h4>
              </div>
              <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
                {group.projectIds.map((projectId) => {
                  const projectDetails = getProjectById(projectId);
                  if (!projectDetails) return null;
                  return <ProjectCard key={projectDetails.id} project={projectDetails} />;
                })}
              </div>
            </div>
          ))}
        </div>
      </ContentWrapper>
    );
  }

  return (
    <ContentWrapper>
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
        {filteredProjectIds.map((projectId) => {
          const projectDetails = getProjectById(projectId);
          if (!projectDetails) return;
          return <ProjectCard key={projectDetails.id} project={projectDetails} />;
        })}
      </div>
    </ContentWrapper>
  );
});
