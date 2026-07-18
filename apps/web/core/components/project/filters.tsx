/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useCallback } from "react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
import { ListFilter, LayoutGrid } from "lucide-react";
// plane imports
import { useTranslation } from "@plane/i18n";
import type { TProjectFilters } from "@plane/types";
import { cn, calculateTotalFilters } from "@plane/utils";
import { useLocalStorage } from "@plane/hooks";
import { CustomMenu } from "@plane/ui";
import { getButtonStyling } from "@plane/propel/button";
import { CheckIcon } from "@plane/propel/icons";
// components
import { FiltersDropdown } from "@/components/issues/issue-layouts/filters";
// hooks
import { useMember } from "@/hooks/store/use-member";
import { useProjectFilter } from "@/hooks/store/use-project-filter";
// local imports
import { ProjectFiltersSelection } from "./dropdowns/filters";
import { ProjectOrderByDropdown } from "./dropdowns/order-by";

type Props = {
  filterMenuButton?: React.ReactNode;
  classname?: string;
  filterClassname?: string;
  isMobile?: boolean;
};

const HeaderFilters = observer(function HeaderFilters({
  filterMenuButton,
  isMobile,
  classname = "",
  filterClassname = "",
}: Props) {
  // i18n
  const { t } = useTranslation();
  // router
  const { workspaceSlug } = useParams();
  const {
    currentWorkspaceDisplayFilters: displayFilters,
    currentWorkspaceFilters: filters,
    updateFilters,
    updateDisplayFilters,
  } = useProjectFilter();
  const {
    workspace: { workspaceMemberIds },
  } = useMember();
  const handleFilters = useCallback(
    (key: keyof TProjectFilters, value: string | string[]) => {
      if (!workspaceSlug) return;
      let newValues = filters?.[key] ?? [];
      if (Array.isArray(value)) {
        if (key === "created_at" && newValues.find((v) => v.includes("custom"))) newValues = [];
        value.forEach((val) => {
          if (!newValues.includes(val)) newValues.push(val);
          else newValues.splice(newValues.indexOf(val), 1);
        });
      } else {
        if (filters?.[key]?.includes(value)) newValues.splice(newValues.indexOf(value), 1);
        else {
          if (key === "created_at") newValues = [value];
          else newValues.push(value);
        }
      }

      updateFilters(workspaceSlug.toString(), { [key]: newValues });
    },
    [filters, updateFilters, workspaceSlug]
  );
  const { setValue: setGroupBy, storedValue: groupBy } = useLocalStorage<"none" | "label">(
    "project_list_group_by",
    "none"
  );
  const isFiltersApplied = calculateTotalFilters(filters ?? {}) !== 0;

  return (
    <div className={cn("flex gap-3", classname)}>
      <CustomMenu
        className={`${isMobile ? "flex w-full justify-center" : ""}`}
        customButton={
          <div className={getButtonStyling("secondary", "lg")}>
            <LayoutGrid className="size-3.5 shrink-0" strokeWidth={2} />
            Group By: {groupBy === "label" ? "Label" : "None"}
          </div>
        }
        placement="bottom-end"
        closeOnSelect
      >
        <CustomMenu.MenuItem className="flex items-center justify-between gap-2" onClick={() => setGroupBy("none")}>
          None
          {groupBy === "none" && <CheckIcon className="h-3 w-3" />}
        </CustomMenu.MenuItem>
        <CustomMenu.MenuItem className="flex items-center justify-between gap-2" onClick={() => setGroupBy("label")}>
          Label
          {groupBy === "label" && <CheckIcon className="h-3 w-3" />}
        </CustomMenu.MenuItem>
      </CustomMenu>

      <ProjectOrderByDropdown
        value={displayFilters?.order_by}
        onChange={(val) => {
          if (!workspaceSlug || val === displayFilters?.order_by) return;
          updateDisplayFilters(workspaceSlug.toString(), {
            order_by: val,
          });
        }}
        isMobile={isMobile}
      />
      <div className={cn(filterClassname)}>
        <FiltersDropdown
          icon={<ListFilter className="h-3 w-3" />}
          title={t("common.filters")}
          placement="bottom-end"
          isFiltersApplied={isFiltersApplied}
          menuButton={filterMenuButton || null}
        >
          <ProjectFiltersSelection
            displayFilters={displayFilters ?? {}}
            filters={filters ?? {}}
            handleFiltersUpdate={handleFilters}
            handleDisplayFiltersUpdate={(val) => {
              if (!workspaceSlug) return;
              updateDisplayFilters(workspaceSlug.toString(), val);
            }}
            memberIds={workspaceMemberIds ?? undefined}
          />
        </FiltersDropdown>
      </div>
    </div>
  );
});
export default HeaderFilters;
