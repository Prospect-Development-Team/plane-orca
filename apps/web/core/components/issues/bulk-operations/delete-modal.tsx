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

export const BulkDeleteConfirmModal = observer(function BulkDeleteConfirmModal(props: Props) {
  const { isOpen, issueIds, onClose, onSuccess } = props;
  // router
  const { workspaceSlug, projectId } = useParams();
  // store
  const {
    issues: { removeBulkIssues },
  } = useIssuesStore();
  // state
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!workspaceSlug || !projectId || issueIds.length === 0) return;
    setIsDeleting(true);
    try {
      await removeBulkIssues(workspaceSlug.toString(), projectId.toString(), issueIds);
      setToast({
        type: TOAST_TYPE.SUCCESS,
        title: "Deleted!",
        message: `${issueIds.length} work item${issueIds.length > 1 ? "s" : ""} deleted successfully.`,
      });
      onSuccess();
      onClose();
    } catch {
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error",
        message: "Something went wrong while deleting. Please try again.",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <AlertModalCore
      isOpen={isOpen}
      handleClose={onClose}
      handleSubmit={handleDelete}
      isSubmitting={isDeleting}
      title="Delete work items"
      variant="danger"
      width={EModalWidth.SM}
      primaryButtonText={{
        loading: "Deleting...",
        default: `Delete ${issueIds.length} item${issueIds.length > 1 ? "s" : ""}`,
      }}
      content={
        <>
          Are you sure you want to delete{" "}
          <span className="font-medium break-words text-primary">
            {issueIds.length} work item{issueIds.length > 1 ? "s" : ""}
          </span>
          ? This action cannot be undone.
        </>
      }
    />
  );
});
