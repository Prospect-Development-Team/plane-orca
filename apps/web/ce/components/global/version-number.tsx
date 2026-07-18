/**
 * Copyright (c) 2023-present Plane Software, Inc. and contributors
 * SPDX-License-Identifier: AGPL-3.0-only
 * See the LICENSE file for details.
 */

// assets
import { useTranslation } from "@plane/i18n";
import packageJson from "package.json";

export function PlaneVersionNumber() {
  const { t } = useTranslation();
  // Custom override: prefer VITE_APP_VERSION injected at Docker build time (root workspace version).
  // Falls back to the local package.json version in local dev without the env var.
  const appVersion = process.env.VITE_APP_VERSION || packageJson.version;
  return (
    <span>
      {t("version")}: v{appVersion}
    </span>
  );
}
