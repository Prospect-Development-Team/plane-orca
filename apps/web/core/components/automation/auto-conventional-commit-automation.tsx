/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observer } from "mobx-react";
import { useParams } from "next/navigation";
import { GitCommit } from "lucide-react";
// plane imports
import { EUserPermissions, EUserPermissionsLevel } from "@plane/constants";
import type { IProject } from "@plane/types";
import { ToggleSwitch } from "@plane/ui";
// component
import { SettingsControlItem } from "@/components/settings/control-item";
// hooks
import { useProject } from "@/hooks/store/use-project";
import { useUserPermissions } from "@/hooks/store/user";

const CONVENTIONAL_COMMIT_TAGS = [
  { name: "feat", color: "#3B82F6" },
  { name: "fix", color: "#EF4444" },
  { name: "docs", color: "#8B5CF6" },
  { name: "style", color: "#EC4899" },
  { name: "refactor", color: "#F59E0B" },
  { name: "perf", color: "#10B981" },
  { name: "test", color: "#6366F1" },
  { name: "build", color: "#F97316" },
  { name: "ci", color: "#06B6D4" },
  { name: "chore", color: "#64748B" },
  { name: "revert", color: "#6B7280" },
];

type Props = {
  handleChange: (formData: Partial<IProject>) => Promise<void>;
};

export const AutoConventionalCommitAutomation = observer(function AutoConventionalCommitAutomation(props: Props) {
  const { handleChange } = props;
  // router
  const { workspaceSlug } = useParams();
  // store hooks
  const { allowPermissions } = useUserPermissions();
  const { currentProjectDetails } = useProject();

  const isAdmin = allowPermissions(
    [EUserPermissions.ADMIN],
    EUserPermissionsLevel.PROJECT,
    workspaceSlug?.toString(),
    currentProjectDetails?.id
  );

  const autoConventionalStatus = currentProjectDetails?.auto_conventional_commit_labels ?? false;

  const handleToggle = async () => {
    await handleChange({ auto_conventional_commit_labels: !autoConventionalStatus });
  };

  return (
    <div className="flex flex-col gap-3 border-b border-subtle py-2">
      <div className="flex items-center gap-3">
        <div className="grid size-10 shrink-0 place-items-center rounded-sm bg-layer-2">
          <GitCommit className="text-custom-primary size-4 shrink-0" />
        </div>
        <SettingsControlItem
          title="Auto-label conventional commits"
          description="Automatically assign conventional commit labels to work items based on their title prefix. Activating this will scan and label existing unlabeled work items."
          control={
            <ToggleSwitch value={autoConventionalStatus} onChange={handleToggle} size="sm" disabled={!isAdmin} />
          }
        />
      </div>

      <div className="mb-1 ml-13 flex flex-wrap items-center gap-1.5 rounded-sm border border-subtle bg-surface-2 px-3 py-2">
        <span className="text-[11px] font-medium text-secondary">Supported:</span>
        {CONVENTIONAL_COMMIT_TAGS.map((tag) => (
          <span
            key={tag.name}
            className="font-mono inline-flex items-center gap-1 rounded bg-layer-2 px-1.5 py-0.5 text-[11px] font-medium text-primary"
          >
            <span className="size-1.5 shrink-0 rounded-full" style={{ backgroundColor: tag.color }} />
            <span>{tag.name}</span>
          </span>
        ))}
      </div>
    </div>
  );
});
