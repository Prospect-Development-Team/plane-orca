/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useState } from "react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
// plane imports
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
import { AlertModalCore, EModalWidth } from "@plane/ui";
// hooks
import { useIssuesStore } from "@/hooks/use-issue-layout-store";

type Props = {
  isOpen: boolean;
  issueIds: string[];
  onClose: () => void;
  onSuccess: () => void;
};

export const BulkArchiveConfirmModal = observer(function BulkArchiveConfirmModal(props: Props) {
  const { isOpen, issueIds, onClose, onSuccess } = props;
  // router
  const { workspaceSlug, projectId } = useParams();
  // store
  const {
    issues: { archiveBulkIssues },
  } = useIssuesStore();
  // state
  const [isArchiving, setIsArchiving] = useState(false);

  const handleArchive = async () => {
    if (!workspaceSlug || !projectId || issueIds.length === 0) return;
    setIsArchiving(true);
    try {
      if (archiveBulkIssues) {
        await archiveBulkIssues(workspaceSlug.toString(), projectId.toString(), issueIds);
      }
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Archived!",
        message: `${issueIds.length} work item${issueIds.length > 1 ? "s" : ""} archived successfully.`,
      });
      onSuccess();
      onClose();
    } catch {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error",
        message: "Something went wrong while archiving. Please try again.",
      });
    } finally {
      setIsArchiving(false);
    }
  };

  return (
    <AlertModalCore
      isOpen={isOpen}
      handleClose={onClose}
      handleSubmit={handleArchive}
      isSubmitting={isArchiving}
      title="Archive work items"
      variant="primary"
      width={EModalWidth.SM}
      primaryButtonText={{
        loading: "Archiving...",
        default: `Archive ${issueIds.length} item${issueIds.length > 1 ? "s" : ""}`,
      }}
      content={
        <>
          Are you sure you want to archive{" "}
          <span className="font-medium break-words text-primary">
            {issueIds.length} work item{issueIds.length > 1 ? "s" : ""}
          </span>
          ? You can view and restore them from the project archives later.
        </>
      }
    />
  );
});
