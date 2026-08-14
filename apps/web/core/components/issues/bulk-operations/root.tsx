/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observer } from "mobx-react";
// components
import { BulkOperationsActionBar } from "@/plane-web/components/issues/bulk-operations/action-bar";
// hooks
import { useMultipleSelectStore } from "@/hooks/store/use-multiple-select-store";
import type { TSelectionHelper } from "@/hooks/use-multiple-select";

type Props = {
  className?: string;
  wrapperClassName?: string;
  selectionHelpers: TSelectionHelper;
};

export const IssueBulkOperationsRoot = observer(function IssueBulkOperationsRoot(props: Props) {
  const { className, wrapperClassName, selectionHelpers } = props;
  // store hooks
  const { isSelectionActive, clearSelection } = useMultipleSelectStore();

  if (!isSelectionActive || selectionHelpers.isSelectionDisabled) return null;

  return (
    <BulkOperationsActionBar
      className={className}
      wrapperClassName={wrapperClassName}
      onClearSelection={() => {
        clearSelection();
        selectionHelpers.handleClearSelection();
      }}
    />
  );
});
