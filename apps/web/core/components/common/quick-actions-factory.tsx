/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { Pencil, ExternalLink, Link, Trash2, ArchiveRestoreIcon, PlayCircle, StopCircle } from "lucide-react";
import { useTranslation } from "@plane/i18n";
import { ArchiveIcon } from "@plane/propel/icons";
import type { TContextMenuItem } from "@plane/ui";

/**
 * Unified factory for creating menu items across all entities (cycles, modules, views, epics)
 */
export const useQuickActionsFactory = () => {
  const { t } = useTranslation();

  return {
    // Common menu items
    createEditMenuItem: (handler: () => void, shouldRender: boolean = true): TContextMenuItem => ({
      key: "edit",
      title: t("edit"),
      icon: Pencil,
      action: handler,
      shouldRender,
    }),

    createOpenInNewTabMenuItem: (handler: () => void): TContextMenuItem => ({
      key: "open-new-tab",
      title: t("open_in_new_tab"),
      icon: ExternalLink,
      action: handler,
    }),

    createCopyLinkMenuItem: (handler: () => void): TContextMenuItem => ({
      key: "copy-link",
      title: t("copy_link"),
      icon: Link,
      action: handler,
    }),

    createArchiveMenuItem: (
      handler: () => void,
      opts: { shouldRender?: boolean; disabled?: boolean; description?: string }
    ): TContextMenuItem => ({
      key: "archive",
      title: t("archive"),
      icon: ArchiveIcon,
      action: handler,
      className: "items-start",
      iconClassName: "mt-1",
      description: opts.description,
      disabled: opts.disabled,
      shouldRender: opts.shouldRender,
    }),

    createRestoreMenuItem: (handler: () => void, shouldRender: boolean = true): TContextMenuItem => ({
      key: "restore",
      title: t("restore"),
      icon: ArchiveRestoreIcon,
      action: handler,
      shouldRender,
    }),

    createDeleteMenuItem: (handler: () => void, shouldRender: boolean = true): TContextMenuItem => ({
      key: "delete",
      title: t("delete"),
      icon: Trash2,
      action: handler,
      shouldRender,
    }),

    /**
     * Orca Custom: "Start Cycle" menu item — shown on upcoming/draft cycles.
     * Triggers the CycleStartStopModal in "start" mode.
     * @param handler - opens the start confirmation modal
     * @param shouldRender - visibility control based on cycle status
     */
    createStartCycleMenuItem: (handler: () => void, shouldRender: boolean = true): TContextMenuItem => ({
      key: "start-cycle",
      title: "Start cycle",
      icon: PlayCircle,
      action: handler,
      shouldRender,
    }),

    /**
     * Orca Custom: "Complete Cycle" menu item — shown on active (current) cycles.
     * Triggers the CycleStartStopModal in "end" mode.
     * @param handler - opens the end confirmation modal
     * @param shouldRender - visibility control based on cycle status
     */
    createEndCycleMenuItem: (handler: () => void, shouldRender: boolean = true): TContextMenuItem => ({
      key: "end-cycle",
      title: "Complete cycle",
      icon: StopCircle,
      action: handler,
      shouldRender,
    }),

    // Layout-level actions (for work item list views)
    createOpenInNewTab: (handler: () => void): TContextMenuItem => ({
      key: "open-in-new-tab",
      title: "Open in new tab",
      icon: ExternalLink,
      action: handler,
    }),

    createCopyLayoutLinkMenuItem: (handler: () => void): TContextMenuItem => ({
      key: "copy-link",
      title: "Copy link",
      icon: Link,
      action: handler,
    }),
  };
};
