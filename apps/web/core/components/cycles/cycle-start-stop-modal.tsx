/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

/**
 * Orca Custom: CycleStartStopModal
 * @description A single shared confirmation modal for both "Start Cycle" and "End Cycle" actions.
 * When ending a cycle that still has incomplete work items, an amber warning callout is shown
 * to notify the user that those items will not be auto-completed.
 */

import { useState } from "react";
import { observer } from "mobx-react";
import { AlertTriangle } from "lucide-react";
// plane imports
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
import type { ICycle } from "@plane/types";
import { AlertModalCore } from "@plane/ui";
import { renderFormattedDate } from "@plane/utils";
// hooks
import { useCycle } from "@/hooks/store/use-cycle";
import { useProjectState } from "@/hooks/store/use-project-state";
import { useTimeZoneConverter } from "@/hooks/use-timezone-converter";

type TMode = "start" | "end";

type Props = {
  /** Whether the modal is open */
  isOpen: boolean;
  /** "start" = Start Cycle; "end" = End Cycle */
  mode: TMode;
  /** Full cycle details, used for the name and incomplete items count */
  cycleDetails: ICycle;
  workspaceSlug: string;
  projectId: string;
  /** Callback to close the modal */
  handleClose: () => void;
};

const MODAL_COPY: Record<TMode, { title: string; primaryDefault: string; primaryLoading: string }> = {
  start: {
    title: "Start cycle",
    primaryDefault: "Start cycle",
    primaryLoading: "Starting…",
  },
  end: {
    title: "Complete cycle",
    primaryDefault: "Complete cycle",
    primaryLoading: "Completing…",
  },
};

export const CycleStartStopModal = observer(function CycleStartStopModal(props: Props) {
  const { isOpen, mode, cycleDetails, workspaceSlug, projectId, handleClose } = props;
  // state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [setInProgress, setSetInProgress] = useState<boolean>(true);
  const [markCompleted, setMarkCompleted] = useState<boolean>(true);
  // store
  const { startCycle, endCycle } = useCycle();
  const { getProjectStates } = useProjectState();
  const projectStates = getProjectStates(projectId);
  const hasInProgressState = projectStates?.some((s) => s.group === "started");
  const hasCompletedState = projectStates?.some((s) => s.group === "completed");
  // timezone converter
  const { renderFormattedDateInUserTimezone } = useTimeZoneConverter(projectId);

  const copy = MODAL_COPY[mode];
  const formattedDate =
    renderFormattedDateInUserTimezone(new Date().toISOString()) || renderFormattedDate(new Date()) || "today";

  const description =
    mode === "start" ? (
      <>
        This will set <span className="font-semibold text-primary">{formattedDate}</span> as the start date and move the
        cycle to active.
      </>
    ) : (
      <>
        This will set <span className="font-semibold text-primary">{formattedDate}</span> as the end date and mark the
        cycle as completed.
      </>
    );

  /**
   * Number of work items that are not yet done (not completed or cancelled).
   * Used to show the warning callout when ending a cycle.
   */
  const incompleteCount =
    (cycleDetails.total_issues ?? 0) - ((cycleDetails.completed_issues ?? 0) + (cycleDetails.cancelled_issues ?? 0));

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      if (mode === "start") {
        const willUpdateState = setInProgress && Boolean(hasInProgressState);
        await startCycle(workspaceSlug, projectId, cycleDetails.id, { set_in_progress: willUpdateState });
        setToast({
          type: TOAST_TYPE.SUCCESS,
          title: "Cycle started",
          message: willUpdateState
            ? `"${cycleDetails.name}" is now active and unstarted issues were moved to In Progress.`
            : `"${cycleDetails.name}" is now active.`,
        });
      } else {
        const willMarkCompleted = markCompleted && Boolean(hasCompletedState) && incompleteCount > 0;
        await endCycle(workspaceSlug, projectId, cycleDetails.id, { mark_completed: willMarkCompleted });
        setToast({
          type: TOAST_TYPE.SUCCESS,
          title: "Cycle completed",
          message: willMarkCompleted
            ? `"${cycleDetails.name}" has been marked as completed and incomplete issues were moved to Completed.`
            : `"${cycleDetails.name}" has been marked as completed.`,
        });
      }
      handleClose();
    } catch {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Something went wrong",
        message: "Please try again later.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const modalContent = (
    <div className="flex flex-col gap-3">
      <p>
        Are you sure you want to {mode === "start" ? "start" : "end"}{" "}
        <span className="font-medium break-words text-primary">"{cycleDetails.name}"</span>? {description}
      </p>

      {/* Option to move unstarted items to In Progress when starting a cycle */}
      {mode === "start" && hasInProgressState && (
        <div className="flex items-start gap-2.5 rounded-md border border-subtle bg-surface-2 p-3">
          <input
            type="checkbox"
            id="set_in_progress"
            checked={setInProgress}
            onChange={(e) => setSetInProgress(e.target.checked)}
            className="focus:ring-primary mt-0.5 h-4 w-4 cursor-pointer rounded border-subtle text-primary"
          />
          <label htmlFor="set_in_progress" className="text-xs cursor-pointer select-none">
            <span className="font-medium text-primary">Move unstarted work items to In Progress</span>
            <p className="mt-0.5 text-secondary">
              All backlog and unstarted work items in this cycle will automatically move to the In Progress state.
            </p>
          </label>
        </div>
      )}

      {/* Warning if project has no In Progress state */}
      {mode === "start" && !hasInProgressState && (
        <div className="bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 flex items-start gap-2 rounded-md p-3">
          <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
          <p className="text-13">
            <span className="font-medium">No "In Progress" state found.</span> Work items in this cycle will remain in
            their current state when started.
          </p>
        </div>
      )}

      {/* Option to mark incomplete items as Completed when ending a cycle */}
      {mode === "end" && incompleteCount > 0 && hasCompletedState && (
        <div className="flex items-start gap-2.5 rounded-md border border-subtle bg-surface-2 p-3">
          <input
            type="checkbox"
            id="mark_completed"
            checked={markCompleted}
            onChange={(e) => setMarkCompleted(e.target.checked)}
            className="focus:ring-primary mt-0.5 h-4 w-4 cursor-pointer rounded border-subtle text-primary"
          />
          <label htmlFor="mark_completed" className="text-xs cursor-pointer select-none">
            <span className="font-medium text-primary">Mark all incomplete work items as Completed</span>
            <p className="mt-0.5 text-secondary">
              All {incompleteCount} unfinished work item{incompleteCount !== 1 ? "s" : ""} in this cycle will
              automatically move to the Completed state.
            </p>
          </label>
        </div>
      )}

      {/* Warning if ending cycle with incomplete work items when no Completed state exists */}
      {mode === "end" && incompleteCount > 0 && !hasCompletedState && (
        <div className="bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 flex items-start gap-2 rounded-md p-3">
          <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" aria-hidden="true" />
          <p className="text-13">
            <span className="font-medium">
              {incompleteCount} work item{incompleteCount !== 1 ? "s" : ""} not yet done.
            </span>{" "}
            No "Completed" state found in this project to update them automatically.
          </p>
        </div>
      )}
    </div>
  );

  return (
    <AlertModalCore
      isOpen={isOpen}
      handleClose={handleClose}
      handleSubmit={handleSubmit}
      isSubmitting={isSubmitting}
      title={copy.title}
      content={modalContent}
      variant="primary"
      primaryButtonText={{
        default: copy.primaryDefault,
        loading: copy.primaryLoading,
      }}
      secondaryButtonText="Cancel"
    />
  );
});
