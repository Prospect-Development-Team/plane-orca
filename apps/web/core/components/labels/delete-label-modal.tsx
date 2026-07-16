/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useState } from "react";
import { observer } from "mobx-react";
import { useParams as useNextParams } from "next/navigation";
import { useParams as useReactParams } from "react-router";
// types
import { TOAST_TYPE, setToast } from "@plane/propel/toast";
import type { IIssueLabel } from "@plane/types";
// ui
import { AlertModalCore } from "@plane/ui";
// hooks
import { useLabel } from "@/hooks/store/use-label";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  data: IIssueLabel | null;
  handleDelete?: (label: IIssueLabel) => Promise<void>;
};

export const DeleteLabelModal = observer(function DeleteLabelModal(props: Props) {
  const { isOpen, onClose, data, handleDelete } = props;
  // router
  const nextParams = useNextParams();
  const reactParams = useReactParams();
  const workspaceSlug = nextParams?.workspaceSlug || reactParams?.workspaceSlug;
  const projectId = nextParams?.projectId || reactParams?.projectId;

  // store hooks
  const { deleteLabel } = useLabel();
  // states
  const [isDeleteLoading, setIsDeleteLoading] = useState(false);

  const handleClose = () => {
    onClose();
    setIsDeleteLoading(false);
  };

  const handleDeletion = async () => {
    if (!workspaceSlug || !data) return;
    if (!projectId && !handleDelete) return;

    setIsDeleteLoading(true);

    try {
      if (handleDelete) {
        await handleDelete(data);
      } else {
        await deleteLabel(workspaceSlug.toString(), projectId.toString(), data.id);
      }
      handleClose();
    } catch (err: any) {
      setIsDeleteLoading(false);
      const error = err?.error || "Label could not be deleted. Please try again.";
      setToast({
        type: TOAST_TYPE.ERROR,
        title: "Error!",
        message: error,
      });
    }
  };

  return (
    <AlertModalCore
      handleClose={handleClose}
      handleSubmit={handleDeletion}
      isSubmitting={isDeleteLoading}
      isOpen={isOpen}
      title="Delete Label"
      content={
        <div className="flex flex-col gap-2">
          <span>Are you sure you want to delete the label?</span>
          <span>This action cannot be undone. All the issues with this label will lose it.</span>
        </div>
      }
      variant="danger"
    />
  );
});
