/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useCallback } from "react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
import { EIssuesStoreType } from "@plane/types";
// hooks
import { useCycle } from "@/hooks/store/use-cycle";
import { useIssues } from "@/hooks/store/use-issues";
// components
import { CycleIssueQuickActions } from "../../quick-action-dropdowns";
import { BaseCalendarRoot } from "../base-calendar-root";

export const CycleCalendarLayout = observer(function CycleCalendarLayout() {
  const { getCycleById } = useCycle();
  const { workspaceSlug, projectId, cycleId } = useParams();

  const {
    issues: { addIssueToCycle },
  } = useIssues(EIssuesStoreType.CYCLE);

  const cycleDetails = cycleId ? getCycleById(cycleId.toString()) : null;
  const isCompletedCycle = !!cycleDetails?.archived_at;

  const addIssuesToView = useCallback(
    (issueIds: string[]) => {
      if (!workspaceSlug || !projectId || !cycleId) throw new Error();
      return addIssueToCycle(workspaceSlug.toString(), projectId.toString(), cycleId.toString(), issueIds);
    },
    [addIssueToCycle, workspaceSlug, projectId, cycleId]
  );

  if (!cycleId) return null;

  return (
    <BaseCalendarRoot
      QuickActions={CycleIssueQuickActions}
      addIssuesToView={addIssuesToView}
      isCompletedCycle={isCompletedCycle}
      viewId={cycleId?.toString()}
    />
  );
});
