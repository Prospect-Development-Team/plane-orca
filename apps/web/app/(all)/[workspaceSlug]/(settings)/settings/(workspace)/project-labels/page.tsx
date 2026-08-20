/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect, useState, useRef } from "react";
import { observer } from "mobx-react";
import { useParams } from "react-router";
import React from "react";
import { combine } from "@atlaskit/pragmatic-drag-and-drop/combine";
import { autoScrollForElements } from "@atlaskit/pragmatic-drag-and-drop-auto-scroll/element";

// plane imports
import { PageHead } from "@/components/core/page-title";
import { SettingsContentWrapper } from "@/components/settings/content-wrapper";
import { ToggleSwitch, AlertModalCore } from "@plane/ui";
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
import { ProjectSettingsLabelList } from "@/components/labels";
import { useTranslation } from "@plane/i18n";

// hooks
import { useCustomProjectLabel } from "@/hooks/store/use-custom-project-label";
import { ProjectLabelsWorkspaceSettingsHeader } from "./header";

const ProjectLabelsPage = observer(function ProjectLabelsPage() {
  const { workspaceSlug } = useParams();
  const store = useCustomProjectLabel();
  const { t } = useTranslation();

  const [isLoading, setIsLoading] = useState(true);

  // Toggle settings states
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  const [isSubmittingToggle, setIsSubmittingToggle] = useState(false);

  const scrollableContainerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!workspaceSlug) return;
    Promise.all([store.fetchSettings(workspaceSlug.toString()), store.fetchLabels(workspaceSlug.toString())]).finally(
      () => {
        setIsLoading(false);
      }
    );
  }, [workspaceSlug, store]);

  // Enable Auto Scroll for Labels list
  useEffect(() => {
    const element = scrollableContainerRef.current;
    if (!element) return;
    return combine(
      autoScrollForElements({
        element,
      })
    );
  }, [isLoading]);

  const handleToggle = () => {
    setIsConfirmationModalOpen(true);
  };

  const handleConfirmToggle = async () => {
    if (!workspaceSlug || !store.settings) return;
    setIsSubmittingToggle(true);
    const nextValue = !store.settings.is_enabled;
    try {
      await store.updateSettings(workspaceSlug.toString(), {
        is_enabled: nextValue,
      });
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Success",
        message: `Project Labels feature ${nextValue ? "enabled" : "disabled"} successfully.`,
      });
    } catch (_e) {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error",
        message: "Failed to update project label settings.",
      });
    } finally {
      setIsSubmittingToggle(false);
      setIsConfirmationModalOpen(false);
    }
  };

  if (isLoading) {
    return (
      <SettingsContentWrapper header={<ProjectLabelsWorkspaceSettingsHeader />}>
        <div className="text-custom-text-300 flex h-full w-full items-center justify-center py-20">
          Loading settings...
        </div>
      </SettingsContentWrapper>
    );
  }

  const labelOperationsCallbacks = {
    createLabel: async (data: any) => {
      const res = await store.createLabel(workspaceSlug!.toString(), data);
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Success",
        message: "Project label created successfully.",
      });
      return res;
    },
    updateLabel: async (id: string, data: any) => {
      const res = await store.updateLabel(workspaceSlug!.toString(), id, data);
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Success",
        message: "Project label updated successfully.",
      });
      return res;
    },
  };

  const handleDelete = async (label: any) => {
    if (!workspaceSlug) return;
    await store.deleteLabel(workspaceSlug.toString(), label.id);
    setToast({
      type: TOAST_TYPE.SUCCESS,
      title: "Success",
      message: "Project label deleted successfully.",
    });
  };

  const onDrop = (
    draggingLabelId: string,
    droppedParentId: string | null,
    droppedLabelId: string | undefined,
    dropAtEndOfList: boolean
  ) => {
    if (workspaceSlug) {
      store.updateLabelPosition(
        workspaceSlug.toString(),
        draggingLabelId,
        droppedParentId,
        droppedLabelId,
        dropAtEndOfList
      );
    }
  };

  return (
    <SettingsContentWrapper header={<ProjectLabelsWorkspaceSettingsHeader />}>
      <PageHead
        title={
          !t("workspace_settings.settings.project_labels.title") ||
          t("workspace_settings.settings.project_labels.title") === "workspace_settings.settings.project_labels.title"
            ? "Workspace Project Labels"
            : t("workspace_settings.settings.project_labels.title")
        }
      />
      <div className="flex max-w-4xl flex-col gap-6 p-6">
        <div className="flex items-center justify-between border-b border-subtle pb-6">
          <div>
            <h3 className="text-xl text-custom-text-100 font-medium">
              {!t("workspace_settings.settings.project_labels.heading") ||
              t("workspace_settings.settings.project_labels.heading") ===
                "workspace_settings.settings.project_labels.heading"
                ? "Project Labels"
                : t("workspace_settings.settings.project_labels.heading")}
            </h3>
            <p className="text-sm text-custom-text-300">
              {!t("workspace_settings.settings.project_labels.description") ||
              t("workspace_settings.settings.project_labels.description") ===
                "workspace_settings.settings.project_labels.description"
                ? "Create and manage workspace-level project labels for categorization and board/list grouping."
                : t("workspace_settings.settings.project_labels.description")}
            </p>
          </div>
          <ToggleSwitch value={store.settings?.is_enabled || false} onChange={handleToggle} size="lg" />
        </div>

        {store.settings?.is_enabled && (
          <div ref={scrollableContainerRef} className="size-full">
            <ProjectSettingsLabelList
              title="Workspace Project Labels"
              description={null}
              labels={store.labels || []}
              labelsTree={store.labelsTree || []}
              labelOperationsCallbacks={labelOperationsCallbacks}
              onDrop={onDrop}
              isEditable={true}
              handleDelete={handleDelete}
            />
          </div>
        )}
      </div>

      {isConfirmationModalOpen && (
        <AlertModalCore
          isOpen={isConfirmationModalOpen}
          handleClose={() => setIsConfirmationModalOpen(false)}
          handleSubmit={handleConfirmToggle}
          isSubmitting={isSubmittingToggle}
          title="Confirm Toggle Project Labels"
          content={`Are you sure you want to ${store.settings?.is_enabled ? "disable" : "enable"} workspace project labels? This will change how labels are managed across all projects.`}
          variant="primary"
          primaryButtonText={{
            loading: "Updating...",
            default: "Confirm",
          }}
        />
      )}
    </SettingsContentWrapper>
  );
});

export default ProjectLabelsPage;
