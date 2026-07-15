/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

import { observer } from "mobx-react";
const prospectDevelopmentTeamLogo = "/plane-logos/pdt-logo.svg";

export const WorkspaceEditionBadge = observer(function WorkspaceEditionBadge() {
  return (
    <a
      href="https://github.com/Prospect-Development-Team"
      target="_blank"
      rel="noopener noreferrer"
      className="mx-auto flex items-center gap-2 rounded-full px-3 py-1 transition-colors select-none hover:bg-layer-2"
    >
      <img
        src={prospectDevelopmentTeamLogo}
        alt="Prospect Development Team"
        className="h-6 w-6 rounded-sm object-cover"
      />
      <span className="text-12 font-semibold whitespace-nowrap text-[#D4AF37]">Prospect Development Team</span>
    </a>
  );
});
