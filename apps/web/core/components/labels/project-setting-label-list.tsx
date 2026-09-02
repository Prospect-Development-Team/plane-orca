/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useState, useRef } from "react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
// plane imports
import { EUserPermissions, EUserPermissionsLevel } from "@plane/constants";
import { useTranslation } from "@plane/i18n";
import { Button } from "@plane/propel/button";
import { EmptyStateCompact } from "@plane/propel/empty-state";
import type { IIssueLabel } from "@plane/types";
import { Loader } from "@plane/ui";
import type { TLabelOperationsCallbacks } from "@/components/labels";
import {
  CreateUpdateLabelInline,
  DeleteLabelModal,
  ProjectSettingLabelGroup,
  ProjectSettingLabelItem,
} from "@/components/labels";
// hooks
import { useLabel } from "@/hooks/store/use-label";
import { useUserPermissions } from "@/hooks/store/user";
// local imports
import { SettingsHeading } from "../settings/heading";

type TProjectSettingsLabelListProps = {
  title?: React.ReactNode;
  description?: React.ReactNode;
  labels?: any[];
  labelsTree?: any[];
  labelOperationsCallbacks?: TLabelOperationsCallbacks;
  onDrop?: (
    draggingLabelId: string,
    droppedParentId: string | null,
    droppedLabelId: string | undefined,
    dropAtEndOfList: boolean
  ) => void;
  isEditable?: boolean;
  handleDelete?: (label: IIssueLabel) => Promise<void>;
};

export const ProjectSettingsLabelList = observer(function ProjectSettingsLabelList(
  props: TProjectSettingsLabelListProps
) {
  const {
    title,
    description,
    labels: propLabels,
    labelsTree: propLabelsTree,
    labelOperationsCallbacks: propLabelOperationsCallbacks,
    onDrop: propOnDrop,
    isEditable: propIsEditable,
    handleDelete,
  } = props;

  // router
  const { workspaceSlug, projectId } = useParams();
  // refs
  const scrollToRef = useRef<HTMLDivElement>(null);
  // states
  const [showLabelForm, setLabelForm] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [selectDeleteLabel, setSelectDeleteLabel] = useState<IIssueLabel | null>(null);
  // plane hooks
  const { t } = useTranslation();
  // store hooks
  const {
    projectLabels: storeLabels,
    updateLabelPosition,
    projectLabelsTree: storeLabelsTree,
    createLabel,
    updateLabel,
  } = useLabel();
  const { allowPermissions } = useUserPermissions();

  // derived values
  const isEditable =
    propIsEditable !== undefined
      ? propIsEditable
      : allowPermissions([EUserPermissions.ADMIN], EUserPermissionsLevel.PROJECT);
  const projectLabels = propLabels ?? storeLabels;
  const projectLabelsTree = propLabelsTree ?? storeLabelsTree;

  const defaultLabelOperationsCallbacks: TLabelOperationsCallbacks = {
    createLabel: (data: Partial<IIssueLabel>) => createLabel(workspaceSlug?.toString(), projectId?.toString(), data),
    updateLabel: (labelId: string, data: Partial<IIssueLabel>) =>
      updateLabel(workspaceSlug?.toString(), projectId?.toString(), labelId, data),
  };
  const labelOperationsCallbacks = propLabelOperationsCallbacks ?? defaultLabelOperationsCallbacks;

  const defaultOnDrop = (
    draggingLabelId: string,
    droppedParentId: string | null,
    droppedLabelId: string | undefined,
    dropAtEndOfList: boolean
  ) => {
    if (workspaceSlug && projectId) {
      updateLabelPosition(
        workspaceSlug?.toString(),
        projectId?.toString(),
        draggingLabelId,
        droppedParentId,
        droppedLabelId,
        dropAtEndOfList
      );
      return;
    }
  };
  const onDrop = propOnDrop ?? defaultOnDrop;

  const newLabel = () => {
    setIsUpdating(false);
    setLabelForm(true);
  };

  const finalTitle = title !== undefined ? title : t("project_settings.labels.heading");
  const finalDescription = description !== undefined ? description : t("project_settings.labels.description");

  return (
    <>
      <DeleteLabelModal
        isOpen={!!selectDeleteLabel}
        data={selectDeleteLabel ?? null}
        onClose={() => setSelectDeleteLabel(null)}
        handleDelete={handleDelete}
      />
      {(finalTitle || finalDescription) && (
        <SettingsHeading
          title={finalTitle}
          description={finalDescription}
          control={
            isEditable && (
              <Button variant="primary" size="lg" onClick={newLabel}>
                {t("common.add_label")}
              </Button>
            )
          }
        />
      )}
      {/* If header is hidden but editable, we still need the Add Label button at the top */}
      {!finalTitle && !finalDescription && isEditable && !showLabelForm && (
        <div className="flex w-full justify-end">
          <Button variant="primary" size="lg" onClick={newLabel}>
            {t("common.add_label")}
          </Button>
        </div>
      )}
      <div className="mt-6 w-full">
        {showLabelForm && (
          <div className="my-2 w-full rounded-sm border border-subtle px-3.5 py-2">
            <CreateUpdateLabelInline
              labelForm={showLabelForm}
              setLabelForm={setLabelForm}
              isUpdating={isUpdating}
              labelOperationsCallbacks={labelOperationsCallbacks}
              ref={scrollToRef}
              onClose={() => {
                setLabelForm(false);
                setIsUpdating(false);
              }}
            />
          </div>
        )}
        {projectLabels ? (
          projectLabels.length === 0 && !showLabelForm ? (
            <EmptyStateCompact
              assetKey="label"
              assetClassName="size-20"
              title={t("settings_empty_state.labels.title")}
              description={t("settings_empty_state.labels.description")}
              actions={[
                {
                  label: t("settings_empty_state.labels.cta_primary"),
                  onClick: () => {
                    newLabel();
                  },
                },
              ]}
              align="start"
              rootClassName="py-20"
            />
          ) : (
            projectLabelsTree?.map((label, index) => {
              if (label.children && label.children.length) {
                return (
                  <ProjectSettingLabelGroup
                    key={label.id}
                    label={label}
                    labelChildren={label.children || []}
                    handleLabelDelete={(lbl: IIssueLabel) => setSelectDeleteLabel(lbl)}
                    isUpdating={isUpdating}
                    setIsUpdating={setIsUpdating}
                    isLastChild={index === projectLabelsTree.length - 1}
                    onDrop={onDrop}
                    labelOperationsCallbacks={labelOperationsCallbacks}
                    isEditable={isEditable}
                  />
                );
              }
              return (
                <ProjectSettingLabelItem
                  key={label.id}
                  label={label}
                  handleLabelDelete={(lbl: IIssueLabel) => setSelectDeleteLabel(lbl)}
                  setIsUpdating={setIsUpdating}
                  isChild={false}
                  isLastChild={index === projectLabelsTree.length - 1}
                  onDrop={onDrop}
                  labelOperationsCallbacks={labelOperationsCallbacks}
                  isEditable={isEditable}
                />
              );
            })
          )
        ) : (
          <Loader className="space-y-3">
            <Loader.Item height="30px" />
            <Loader.Item height="30px" />
            <Loader.Item height="30px" />
          </Loader>
        )}
      </div>
    </>
  );
});
