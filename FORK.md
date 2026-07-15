# Fork Customization & Upstream Compatibility Guide

This repository is a custom fork of **Plane (Community Edition)**, optimized for our team's workflow. To ensure that we can easily merge upstream updates from the main Plane repository with minimal merge conflicts, all developers and AI agents must adhere to the following principles.

---

## 1. Customization Architecture Guidelines

### A. Non-Destructive Branding (CSS/Asset Overrides)

Instead of deleting or rewriting imports in Plane's core React files:

- **Brand Icon Components**: Main branding SVG assets are compiled as React components in:
  - `packages/propel/src/icons/brand/plane-logo.tsx` (Contains the main logo `PlaneLogo`)
  - `packages/propel/src/icons/brand/plane-lockup.tsx`
  - `packages/propel/src/icons/brand/plane-wordmark.tsx`
    _Guidelines_: Do not edit the imports in core layouts. Instead, maintain overrides in a workspace-level folder (e.g., `.branding/`) and overwrite the files under `packages/propel/src/icons/brand/` as part of a `prebuild` phase.
- **Public Assets & Icons**: Public files and favicons are stored in:
  - `apps/web/public/plane-logos/`
  - `apps/web/public/icons/`
  - `apps/web/public/favicon/`
- **Styling overrides**: Target default CSS rules in `apps/web/styles/` or inject custom classes.
- **Design Cohesion**: Always reuse existing UI components (from `@plane/ui` and `@plane/propel`), layouts, utility classes, and styling themes. Avoid writing separate or ad-hoc custom designs/stylesheets that deviate from the repository's current structure.

### B. "Wrapper" Architecture for Extra Features (The Sidecar Approach)

Rather than hacking core Django APIs or Next.js layout logic:

- **UI Customization**: Keep components focused in `@plane/ui` (`packages/ui`) and verify styles via Storybook on port 6006.
- **External Sidecar Services**: Develop new logic (e.g., custom automation, notifications, AI schedulers) as separate microservices.
- **API & Webhooks Integration**: Integrate sidecars with Plane strictly using Plane's REST APIs (handled via `apps/api/`) and Webhooks (configured in-app or via settings).
- **Loose Coupling**: Keep `apps/api/plane` and `apps/web` as close to upstream as possible.

#### C. Feature Toggles & Feature Deactivation

The golden rule of customizing a platform fork: **Disable, don't destroy.**

- **Backend Settings**: Managed in `apps/api/plane/settings/common.py`.
- **Frontend Env Variables**: Frontend apps (e.g., `apps/web`, `apps/admin`) use Vite, so environment variables are prefixed with `VITE_` (see `apps/web/.env.example`).
- **UI Elements**: If you want to remove a feature (like default "Plane AI" or "Analytics"), hide it by modifying CSS/Tailwind rules or setting React display conditions instead of deleting component files.
- **Backend & DB Schemas**: Never delete database migration files (django migrations) or drop tables from the database to remove a feature. Doing so will permanently corrupt the database schema mapping, preventing you from running future database migrations when upgrading upstream Plane versions.

### D. Database Schema & Migration Safety

Modifying core database tables directly leads to catastrophic migration conflicts during upstream syncs:

- **JSON Metadata Fields**: If a core model (like `Issue` or `Workspace`) supports custom metadata/extra fields via a JSON field, utilize that first.
- **Relational Sidecar Tables**: If schema changes are required, design a new table/model linked via a one-to-one or foreign key relation (e.g., `CustomIssueProperties` or `TeamWorkspaceSettings`) rather than modifying the core models directly.
- **Namespace Migrations**: Ensure custom Django migrations do not conflict with upstream numbering.

### E. API Endpoint Routing & Custom Namespaces

- **Routing Namespace**: Register any custom Django rest-framework routes under a distinct prefix or helper router (e.g. `/api/v1/custom/...`) to avoid route collisions when upstream adds new viewsets or action endpoints.

### F. Docker & Compose Overrides

- **Override Configurations**: Use `docker-compose.override.yml` for adding custom local services, environment setups, or mapping volumes. Avoid committing changes to the primary `docker-compose.yml` unless the core architecture itself changes.

---

## 2. Monorepo & Tooling Standards

### A. Monorepo Dependency Management (PNPM Catalogs)

To avoid dependency hell and package mismatches:

- **Internal Packages**: Reference monorepo-internal packages using `workspace:*` (e.g., `@plane/ui`, `@plane/types`).
- **External Dependencies**: Use PNPM Catalogs syntax (`catalog:`) for shared external packages (defined in `pnpm-workspace.yaml`), ensuring all monorepo workspaces resolve to the exact same version.

### B. Formatting & Linting

All custom code must pass validation before commits or merges:

- **Frontend**: Format using `oxfmt` (`pnpm fix:format`) and lint using `oxlint` with shared config (`.oxlintrc.json`). Avoid introducing lint bypasses unless strictly justified.
- **Backend (Python)**: Format and lint using `ruff` (configured in `apps/api/pyproject.toml` with `line-length = 120` and double quotes).
- **Token Efficiency (Agents)**: Agents must **never** run heavy validation commands (e.g. full workspace type-checks, builds, or database migrations) directly in the workspace. They must provide the commands for developers to run locally.

### C. License & Copyright Header Compliance

The Plane codebase enforces copyright headers. When creating new Python, TS, or TSX files, verify/apply headers:

- **Python files**:
  ```bash
  addlicense -v -f COPYRIGHT.txt -ignore "**/migrations/**" $(git ls-files '*.py')
  ```
- **TypeScript files** (run on a specific package folder to avoid crashing OS processes):
  ```bash
  addlicense -v -f COPYRIGHT.txt -ignore "**/*.config.ts" -ignore "**/*.d.ts" $(git ls-files 'packages/<package-name>/*.ts')
  ```

### D. Documentation & Comments

To maintain a clean and maintainable codebase:

- **JSDoc/Docstring Formats**: Write clear, easy-to-understand JSDoc comments or docstrings for all modifications. Ensure they match existing codebase formats (e.g. using `@description`, `@param`, `@returns` structures).
- **Preserve Existing Documentation**: Never delete or omit existing JSDoc comments/docstrings when refactoring or modifying code.
- **Guidance for Agents & Users**: Clearly comment custom overrides, sidecar functions, and parallel cycle changes to guide subsequent developers and AI agents on what was done and why.

---

## 3. Git Strategy & Upstream Syncing

To keep this fork functional when upstream Plane releases updates, follow these practices:

### A. The Three-Branch Strategy

- **`main`**: Upstream Mirror. Strictly contains unmodified code tracking Plane's official repository. No custom modifications should be committed to this branch.
- **`stage`**: Custom Staging. The branch where custom features, branding, and config overrides are merged, integrated, and verified.
- **`prod`**: Production. The compiled, tested, and deployed branch containing stable releases.

### B. Semantic Commits & Micro-PRs

Because you will be maintaining an active bridge between your local `main` branch (mirroring Plane) and your staging/production branches, commit discipline is critical.

- **Commit Small, Isolated Changes**: A pull request should do one thing (e.g., just hiding the upgrade button). If a developer merges a single giant PR changing many files, it will be nearly impossible to merge upstream security updates without breaking the build.
- **Require Feature Prefixing**: Establish a strict prefixing rule for custom changes so they are easy to search in the Git history:
  - `orca(ui): [short description]` — For branding, logo, asset overrides, or color changes.
  - `orca(strip): [short description]` — For disabling/removing upgrade prompts, telemetry, or unused pages.
  - `orca(feat): [short description]` — For custom integrations, wrapper services, or internal tools.

### C. Versioning Policy

To cleanly track both upstream Plane releases and our custom modifications:

- **Tag & Release Format**: Use `v[UpstreamVersion]-orca.[ForkVersion]` (e.g., `v1.2.0-orca.1.0.0` or `v1.3.1-orca.1.1.2`).
  - `[UpstreamVersion]` represents the exact release version of Plane CE being tracked.
  - `[ForkVersion]` is a standard `MAJOR.MINOR.PATCH` sequence indicating our custom changes:
    - **MAJOR**: Breaking custom API/schema changes, structural sidecar changes, or upgrades to a new upstream major version.
    - **MINOR**: New custom features, modules, or non-breaking sidecar additions.
    - **PATCH**: Bug fixes, styling tweaks, branding updates, or upstream sync merges with no custom logic changes.
