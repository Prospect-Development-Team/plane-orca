/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useState } from "react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
import { Trash2, Archive, Tag, Bell, BellOff } from "lucide-react";
// plane imports
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
import { Button } from "@plane/propel/button";
import { Checkbox } from "@plane/ui";
import type { TBulkOperationsPayload, TIssue, TIssuePriorities } from "@plane/types";
// components
import { DateDropdown } from "@/components/dropdowns/date";
import { LabelDropdown } from "@/components/issues/issue-layouts/properties/label-dropdown";
import { MemberDropdown } from "@/components/dropdowns/member/dropdown";
import { PriorityDropdown } from "@/components/dropdowns/priority";
import { StateDropdown } from "@/components/dropdowns/state/dropdown";
import { CycleDropdown } from "@/components/dropdowns/cycle";
import { ModuleDropdown } from "@/components/dropdowns/module/dropdown";
// hooks
import { useIssuesStore } from "@/hooks/use-issue-layout-store";
import { useMultipleSelectStore } from "@/hooks/store/use-multiple-select-store";
import { useProjectState } from "@/hooks/store/use-project-state";
import { useLabel } from "@/hooks/store/use-label";
import { useMember } from "@/hooks/store/use-member";
// local
import { BulkDeleteConfirmModal } from "./delete-modal";
import { BulkArchiveConfirmModal } from "./archive-modal";
import { cn } from "@plane/utils";

type TPendingProperties = Partial<TBulkOperationsPayload["properties"]>;

type Props = {
  className?: string;
  wrapperClassName?: string;
  onClearSelection: () => void;
};

export const BulkOperationsActionBar = observer(function BulkOperationsActionBar(props: Props) {
  const { className, wrapperClassName, onClearSelection } = props;
  const { workspaceSlug, projectId } = useParams();
  const { selectedEntityIds, clearSelection } = useMultipleSelectStore();
  const {
    issues: { bulkUpdateProperties },
    issueMap,
  } = useIssuesStore();
  const { getStateById } = useProjectState();
  const { getLabelById } = useLabel();
  const { getUserDetails: _getUserDetails } = useMember();

  const [pending, setPending] = useState<TPendingProperties>({});
  const [isUpdating, setIsUpdating] = useState(false);

  const renderLabelTrigger = () => {
    const ids = pending.label_ids !== undefined ? pending.label_ids : commonLabels;
    if (ids.length === 0) {
      return (
        <span className="text-xs text-custom-text-100 flex items-center gap-1.5 font-medium">
          <Tag className="h-3 w-3" />
          {isMixedLabels ? "Labels (Mixed)" : "Labels"}
        </span>
      );
    }
    const firstLabel = getLabelById(ids[0]);
    const firstLabelName = firstLabel?.name || "Label";
    const labelColor = firstLabel?.color || "#ccc";

    return (
      <span className="text-xs text-custom-text-100 flex max-w-40 min-w-0 items-center gap-1.5 font-medium">
        <span className="h-2 w-2 flex-shrink-0 rounded-full" style={{ backgroundColor: labelColor }} />
        <span className="truncate">{firstLabelName}</span>
        {ids.length > 1 && <span className="flex-shrink-0">+{ids.length - 1}</span>}
      </span>
    );
  };

  const getCommonValue = <T,>(key: keyof TIssue): T | null => {
    if (selectedEntityIds.length === 0) return null;
    const firstIssue = issueMap[selectedEntityIds[0]];
    if (!firstIssue) return null;
    const firstVal = firstIssue[key];

    const isSame = selectedEntityIds.every((id) => {
      const issue = issueMap[id];
      return issue && issue[key] === firstVal;
    });

    return isSame ? (firstVal as T) : null;
  };

  const getCommonArrayValue = <T,>(key: keyof TIssue): T[] => {
    if (selectedEntityIds.length === 0) return [];
    const firstIssue = issueMap[selectedEntityIds[0]];
    if (!firstIssue) return [];
    const firstVal = (firstIssue[key] as T[]) || [];

    const isSame = selectedEntityIds.every((id) => {
      const issue = issueMap[id];
      if (!issue) return false;
      const val = (issue[key] as T[]) || [];
      if (val.length !== firstVal.length) return false;
      return val.every((v) => firstVal.includes(v));
    });

    return isSame ? firstVal : [];
  };

  const isMixedValue = (key: keyof TIssue): boolean => {
    if (selectedEntityIds.length <= 1) return false;
    const firstIssue = issueMap[selectedEntityIds[0]];
    if (!firstIssue) return false;
    const firstVal = firstIssue[key];

    if (Array.isArray(firstVal)) {
      const firstArray = firstVal as any[];
      return selectedEntityIds.some((id) => {
        const issue = issueMap[id];
        if (!issue) return true;
        const val = (issue[key] as any[]) || [];
        if (val.length !== firstArray.length) return true;
        return !val.every((v) => firstArray.includes(v));
      });
    }

    return selectedEntityIds.some((id) => {
      const issue = issueMap[id];
      return issue && issue[key] !== firstVal;
    });
  };

  const commonStateId = getCommonValue<string>("state_id");
  const commonPriority = getCommonValue<TIssuePriorities>("priority");
  const commonAssignees = getCommonArrayValue<string>("assignee_ids");
  const commonLabels = getCommonArrayValue<string>("label_ids");
  const commonCycle = getCommonValue<string>("cycle_id");
  const commonModules = getCommonArrayValue<string>("module_ids");
  const commonStartDate = getCommonValue<string>("start_date");
  const commonTargetDate = getCommonValue<string>("target_date");

  const isMixedState = isMixedValue("state_id");
  const isMixedPriority = isMixedValue("priority");
  const isMixedAssignees = isMixedValue("assignee_ids");
  const isMixedLabels = isMixedValue("label_ids");
  const isMixedCycle = isMixedValue("cycle_id");
  const isMixedModules = isMixedValue("module_ids");
  const isMixedStartDate = isMixedValue("start_date");
  const isMixedTargetDate = isMixedValue("target_date");

  const commonIsSubscribed = getCommonValue<boolean>("is_subscribed");
  const currentIsSubscribed =
    pending.is_subscribed !== undefined ? pending.is_subscribed : (commonIsSubscribed ?? false);
  const handleToggleSubscription = () => {
    updatePending({ is_subscribed: !currentIsSubscribed });
  };

  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [isArchiveOpen, setIsArchiveOpen] = useState(false);

  const selectedCount = selectedEntityIds.length;
  const projectIdStr = projectId?.toString() ?? undefined;
  const hasPendingChanges = Object.keys(pending).length > 0;

  const canArchive =
    selectedEntityIds.length > 0 &&
    selectedEntityIds.every((id) => {
      const issue = issueMap[id];
      if (!issue) return false;
      const state = getStateById(issue.state_id);
      return state?.group === "completed" || state?.group === "cancelled";
    });

  const updatePending = (patch: TPendingProperties) => setPending((prev) => ({ ...prev, ...patch }));

  const handleClear = () => {
    clearSelection();
    onClearSelection();
  };

  const handleUpdate = async () => {
    if (!workspaceSlug || !projectIdStr || !hasPendingChanges) return;
    setIsUpdating(true);
    try {
      await bulkUpdateProperties(workspaceSlug.toString(), projectIdStr, {
        issue_ids: selectedEntityIds,
        properties: pending,
      });
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Updated!",
        message: `${selectedCount} work item${selectedCount > 1 ? "s" : ""} updated successfully.`,
      });
      setPending({});
      clearSelection();
      onClearSelection();
    } catch {
      setToast({ type: TOAST_TYPE.ERROR, title: "Error", message: "Something went wrong. Please try again." });
    } finally {
      setIsUpdating(false);
    }
  };

  const dropdownCls =
    "!h-7 !rounded border-[0.5px] border-strong !bg-custom-background-90/50 hover:!bg-custom-background-80 !px-2 !py-1 !text-xs !font-medium !text-custom-text-100 transition-colors flex items-center justify-center gap-1.5";

  return (
    <>
      {/* ─── Floating Centered Wide Tray ─────────────────────────────────── */}
      <div
        className={cn(
          "absolute bottom-4 left-1/2 z-[30] w-[calc(100%-4rem)] max-w-full -translate-x-1/2",
          wrapperClassName
        )}
      >
        <div
          className={cn(
            "flex items-center justify-between gap-3 rounded-lg border border-accent-strong bg-surface-1 p-2 shadow-raised-200",
            className
          )}
        >
          {/* ── LEFT: Selection & Quick Actions ─────────────────────────── */}
          <div className="flex shrink-0 items-center gap-2">
            {/* Indeterminate Checkbox Style for Clear Selection with !border-none override */}
            <button onClick={handleClear} className="flex items-center transition-opacity hover:opacity-80">
              <Checkbox
                containerClassName="flex items-center justify-center size-3.5 mr-1.5 shrink-0"
                className="pointer-events-none size-3.5 !border-none !outline-none"
                iconClassName="size-3"
                checked={false}
                indeterminate={true}
              />
              <span className="text-xs text-custom-text-100 font-semibold">{selectedCount} selected</span>
            </button>

            {/* Vertical Divider */}
            <div className="mx-1 h-5 border-r border-strong" />

            {/* Notification Toggle Action */}
            <button
              onClick={handleToggleSubscription}
              title={
                currentIsSubscribed ? "Mute notifications for selected" : "Subscribe to notifications for selected"
              }
              className="text-custom-text-400 hover:bg-custom-background-80 hover:text-custom-text-100 flex h-7 w-7 items-center justify-center rounded transition-colors"
            >
              {currentIsSubscribed ? <BellOff className="h-4 w-4" /> : <Bell className="h-4 w-4" />}
            </button>

            {/* Archive Action */}
            <button
              onClick={() => setIsArchiveOpen(true)}
              disabled={!canArchive}
              title={canArchive ? "Archive selected" : "Only completed or canceled work items can be archived"}
              className="text-custom-text-400 hover:bg-custom-background-80 hover:text-custom-text-100 flex h-7 w-7 items-center justify-center rounded transition-colors disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Archive className="h-4 w-4" />
            </button>

            {/* Delete Action */}
            <button
              onClick={() => setIsDeleteOpen(true)}
              title="Delete selected"
              className="text-custom-text-400 hover:bg-custom-background-80 hover:text-custom-text-100 flex h-7 w-7 items-center justify-center rounded transition-colors"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>

          {/* ── MIDDLE: Property Dropdowns ─────────────────────────────── */}
          <div className="scrollbar-none flex flex-1 items-center gap-2 overflow-x-auto px-1">
            {/* State */}
            {projectIdStr && (
              <StateDropdown
                projectId={projectIdStr}
                value={pending.state_id !== undefined ? pending.state_id : (commonStateId ?? null)}
                onChange={(val) => updatePending({ state_id: val })}
                buttonVariant="border-with-text"
                buttonClassName={dropdownCls}
                placeholder={isMixedState ? "State (Mixed)" : "State"}
                renderByDefault={false}
                placement="top-start"
              />
            )}

            {/* Priority */}
            <PriorityDropdown
              value={pending.priority !== undefined ? pending.priority : (commonPriority ?? null)}
              onChange={(val) => updatePending({ priority: val })}
              buttonVariant="border-with-text"
              buttonClassName={dropdownCls}
              placeholder={isMixedPriority ? "Priority (Mixed)" : "Priority"}
              renderByDefault={false}
              placement="top-start"
            />

            {/* Assignees */}
            {projectIdStr && (
              <MemberDropdown
                projectId={projectIdStr}
                value={pending.assignee_ids !== undefined ? pending.assignee_ids : commonAssignees}
                onChange={(val: string[]) => updatePending({ assignee_ids: val })}
                multiple
                buttonVariant="border-with-text"
                buttonClassName={dropdownCls}
                placeholder={isMixedAssignees ? "Assignees (Mixed)" : "Assignees"}
                renderByDefault={false}
                placement="top-start"
                showUserDetails={true}
              />
            )}

            {/* Labels */}
            {projectIdStr && (
              <LabelDropdown
                projectId={projectIdStr}
                value={pending.label_ids !== undefined ? pending.label_ids : commonLabels}
                onChange={(val) => updatePending({ label_ids: val })}
                label={renderLabelTrigger()}
                hideDropdownArrow={false}
                fullHeight={true}
                className="flex h-7 items-center justify-center"
                buttonClassName={dropdownCls}
                placement="top-start"
              />
            )}

            {/* Cycle */}
            {projectIdStr && (
              <CycleDropdown
                projectId={projectIdStr}
                value={pending.cycle_id !== undefined ? pending.cycle_id : (commonCycle ?? null)}
                onChange={(val) => updatePending({ cycle_id: val ?? undefined })}
                buttonVariant="border-with-text"
                buttonClassName={dropdownCls}
                placeholder={isMixedCycle ? "Cycle (Mixed)" : "Cycle"}
                renderByDefault={false}
                placement="top-start"
              />
            )}

            {/* Module */}
            {projectIdStr && (
              <ModuleDropdown
                projectId={projectIdStr}
                value={pending.module_ids !== undefined ? pending.module_ids : commonModules}
                onChange={(val: string[]) => updatePending({ module_ids: val })}
                multiple={true}
                showCount={true}
                buttonVariant="border-with-text"
                buttonClassName={dropdownCls}
                placeholder={isMixedModules ? "Modules (Mixed)" : "Modules"}
                renderByDefault={false}
                placement="top-start"
              />
            )}

            {/* Start date */}
            <DateDropdown
              value={pending.start_date !== undefined ? pending.start_date : (commonStartDate ?? null)}
              onChange={(val) => updatePending({ start_date: val ? val.toISOString().split("T")[0] : null })}
              buttonVariant="border-with-text"
              buttonClassName={dropdownCls}
              placeholder={isMixedStartDate ? "Start date (Mixed)" : "Start date"}
              renderByDefault={false}
              isClearable
              placement="top-start"
            />

            {/* Due date */}
            <DateDropdown
              value={pending.target_date !== undefined ? pending.target_date : (commonTargetDate ?? null)}
              onChange={(val) => updatePending({ target_date: val ? val.toISOString().split("T")[0] : null })}
              buttonVariant="border-with-text"
              buttonClassName={dropdownCls}
              placeholder={isMixedTargetDate ? "Due date (Mixed)" : "Due date"}
              renderByDefault={false}
              isClearable
              placement="top-start"
            />
          </div>

          {/* ── RIGHT: Update button ───────────────────────────────────── */}
          <div className="flex shrink-0 items-center">
            <Button
              variant="primary"
              size="lg"
              onClick={handleUpdate}
              disabled={!hasPendingChanges || isUpdating}
              loading={isUpdating}
            >
              Update
            </Button>
          </div>
        </div>
      </div>

      <BulkDeleteConfirmModal
        isOpen={isDeleteOpen}
        issueIds={selectedEntityIds}
        onClose={() => setIsDeleteOpen(false)}
        onSuccess={() => {
          clearSelection();
          onClearSelection();
        }}
      />

      <BulkArchiveConfirmModal
        isOpen={isArchiveOpen}
        issueIds={selectedEntityIds}
        onClose={() => setIsArchiveOpen(false)}
        onSuccess={() => {
          clearSelection();
          onClearSelection();
        }}
      />
    </>
  );
});
