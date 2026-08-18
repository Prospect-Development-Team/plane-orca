/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { useEffect, useRef, useState, useCallback } from "react";
import type { Placement } from "@popperjs/core";
import { Loader } from "lucide-react";
import { observer } from "mobx-react";
import { useParams } from "next/navigation";
import { usePopper } from "react-popper";
// components
import { Combobox } from "@headlessui/react";
// i18n
import { useTranslation } from "@plane/i18n";
// icon
import { CheckIcon, CycleGroupIcon, CycleIcon, SearchIcon } from "@plane/propel/icons";
import { EUserPermissionsLevel } from "@plane/constants";
import type { TCycleGroups } from "@plane/types";
import { EUserProjectRoles } from "@plane/types";
// ui
// store hooks
import { useCycle } from "@/hooks/store/use-cycle";
import { useUserPermissions } from "@/hooks/store/user";
import { usePlatformOS } from "@/hooks/use-platform-os";
// types

type DropdownOptions =
  | {
      value: string | null;
      query: string;
      content: React.ReactNode;
    }[]
  | undefined;

type CycleOptionsProps = {
  projectId: string;
  referenceElement: HTMLButtonElement | null;
  placement: Placement | undefined;
  isOpen: boolean;
  canRemoveCycle: boolean;
  currentCycleId?: string;
  createCycleEnabled?: boolean;
  onChange?: (val: string | null) => void;
};

export const CycleOptions = observer(function CycleOptions(props: CycleOptionsProps) {
  const {
    projectId,
    isOpen,
    referenceElement,
    placement,
    canRemoveCycle,
    currentCycleId,
    createCycleEnabled,
    onChange,
  } = props;
  // i18n
  const { t } = useTranslation();
  //state hooks
  const [query, setQuery] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [popperElement, setPopperElement] = useState<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  // store hooks
  const { workspaceSlug } = useParams();
  const { getProjectCycleIds, fetchAllCycles, getCycleById, createCycle } = useCycle();
  const { allowPermissions } = useUserPermissions();
  const { isMobile } = usePlatformOS();

  const isPermittedToCreate =
    projectId && workspaceSlug
      ? allowPermissions(
          [EUserProjectRoles.ADMIN, EUserProjectRoles.MEMBER],
          EUserPermissionsLevel.PROJECT,
          workspaceSlug.toString(),
          projectId
        )
      : true;
  const canCreateCycle = createCycleEnabled ?? isPermittedToCreate;

  const cycleIds = (getProjectCycleIds(projectId) ?? [])?.filter((cycleId) => {
    if (currentCycleId && currentCycleId === cycleId) return false;
    return true;
  });

  const onOpen = useCallback(() => {
    if (workspaceSlug && !cycleIds) fetchAllCycles(workspaceSlug.toString(), projectId);
  }, [workspaceSlug, cycleIds, fetchAllCycles, projectId]);

  useEffect(() => {
    if (isOpen) {
      onOpen();
      if (!isMobile) {
        inputRef.current?.focus();
      }
    }
  }, [isOpen, isMobile, onOpen]);

  // popper-js init
  const { styles, attributes } = usePopper(referenceElement, popperElement, {
    placement: placement ?? "bottom-start",
    modifiers: [
      {
        name: "preventOverflow",
        options: {
          padding: 12,
        },
      },
    ],
  });

  /**
   * @description Handles creating a new cycle inline or selecting an existing cycle with matching name
   * @param {string} cycleName - Name of the cycle to create or select
   * @returns {Promise<void>}
   */
  const handleAddCycle = async (cycleName: string) => {
    if (!projectId || !workspaceSlug || submitting) return;
    const name = cycleName.trim();
    if (!name) return;
    setSubmitting(true);
    try {
      const existingCycle = cycleIds
        ?.map((id) => getCycleById(id))
        .find((c) => c?.name.toLowerCase() === name.toLowerCase());

      let selectedId: string;
      if (existingCycle) {
        selectedId = existingCycle.id;
      } else {
        const newCycle = await createCycle(workspaceSlug.toString(), projectId, { name });
        selectedId = newCycle.id;
      }
      onChange?.(selectedId);
      setQuery("");
    } catch (error) {
      console.error("Failed to create cycle", error);
    } finally {
      setSubmitting(false);
    }
  };

  /**
   * @description Handles keyboard shortcuts for cycle search input (Escape to clear, Enter to create/select)
   * @param {React.KeyboardEvent<HTMLInputElement>} e - Input keyboard event
   * @returns {Promise<void>}
   */
  const searchInputKeyDown = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    const q = query.trim();
    if (q !== "" && e.key === "Escape") {
      e.stopPropagation();
      setQuery("");
      return;
    }

    if (
      q !== "" &&
      e.key === "Enter" &&
      !e.nativeEvent.isComposing &&
      canCreateCycle &&
      filteredOptions?.length === 0 &&
      !submitting
    ) {
      e.preventDefault();
      e.stopPropagation();
      await handleAddCycle(q);
    }
  };

  const options: DropdownOptions = cycleIds?.map((cycleId) => {
    const cycleDetails = getCycleById(cycleId);
    const cycleStatus = cycleDetails?.status ? (cycleDetails.status.toLocaleLowerCase() as TCycleGroups) : "draft";

    return {
      value: cycleId,
      query: `${cycleDetails?.name}`,
      content: (
        <div className="flex items-center gap-2">
          <CycleGroupIcon cycleGroup={cycleStatus} className="h-3.5 w-3.5 flex-shrink-0" />
          <span className="flex-grow truncate">{cycleDetails?.name}</span>
        </div>
      ),
    };
  });

  if (canRemoveCycle) {
    options?.unshift({
      value: null,
      query: t("cycle.no_cycle"),
      content: (
        <div className="flex items-center gap-2">
          <CycleIcon className="h-3 w-3 flex-shrink-0" />
          <span className="flex-grow truncate">{t("cycle.no_cycle")}</span>
        </div>
      ),
    });
  }

  const filteredOptions =
    query === "" ? options : options?.filter((o) => o.query.toLowerCase().includes(query.toLowerCase()));

  return (
    <Combobox.Options className="fixed z-10" static>
      <div
        className="my-1 w-48 rounded-sm border-[0.5px] border-strong bg-surface-1 px-2 py-2.5 text-11 shadow-raised-200 focus:outline-none"
        ref={setPopperElement}
        style={styles.popper}
        {...attributes.popper}
      >
        <div className="flex items-center gap-1.5 rounded-sm border border-subtle bg-surface-2 px-2">
          <SearchIcon className="h-3.5 w-3.5 text-placeholder" strokeWidth={1.5} />
          <Combobox.Input
            as="input"
            ref={inputRef}
            className="w-full bg-transparent py-1 text-11 text-secondary placeholder:text-placeholder focus:outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t("common.search.label")}
            displayValue={(assigned: any) => assigned?.name}
            onKeyDown={searchInputKeyDown}
          />
        </div>
        <div className="mt-2 max-h-48 space-y-1 overflow-y-scroll">
          {filteredOptions ? (
            filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <Combobox.Option
                  key={option.value}
                  value={option.value}
                  className={({ active, selected }) =>
                    `flex w-full cursor-pointer items-center justify-between gap-2 truncate rounded-sm px-1 py-1.5 select-none ${
                      active ? "bg-layer-transparent-hover" : ""
                    } ${selected ? "text-primary" : "text-secondary"}`
                  }
                >
                  {({ selected }) => (
                    <>
                      <span className="flex-grow truncate">{option.content}</span>
                      {selected && <CheckIcon className="h-3.5 w-3.5 flex-shrink-0" />}
                    </>
                  )}
                </Combobox.Option>
              ))
            ) : submitting ? (
              <div className="flex items-center justify-center p-2">
                <Loader className="h-3.5 w-3.5 animate-spin text-tertiary" />
              </div>
            ) : canCreateCycle ? (
              <button
                type="button"
                onClick={() => {
                  if (!query.trim().length) return;
                  handleAddCycle(query);
                }}
                className={`w-full px-1.5 py-1 text-left text-caption-sm-regular text-secondary ${
                  query.trim().length ? "cursor-pointer rounded-sm hover:bg-layer-1" : "cursor-default"
                }`}
              >
                {query.trim().length ? (
                  <>
                    + Add <span className="text-primary">&quot;{query.trim()}&quot;</span> to cycles
                  </>
                ) : (
                  t("cycle.create.type")
                )}
              </button>
            ) : (
              <p className="px-1.5 py-1 text-placeholder italic">{t("common.search.no_matches_found")}</p>
            )
          ) : (
            <p className="px-1.5 py-1 text-placeholder italic">{t("common.loading")}</p>
          )}
        </div>
      </div>
    </Combobox.Options>
  );
});
