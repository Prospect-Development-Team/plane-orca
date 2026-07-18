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

### 3. End-to-End Git, CI/CD & Deployment Workflow

To maintain upstream compatibility while shipping custom features, all developers must follow this unified lifecycle:

| Lifecycle Phase          | Action / Trigger             | Source ➡️ Target                            | Automation & Behavior                                                                                                 |
| :----------------------- | :--------------------------- | :------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------- |
| **1. Feature Dev**       | Developer codes locally      | `stage` ➡️ `feature/*`                      | Code custom overrides/features. Maintain Conventional Commit prefixes.                                                |
| **2. Staging PR**        | Open PR targeting Staging    | `feature/*` ➡️ `stage`                      | Auto-labeled `stage-pr` and gets the `basic.md` template checklist injected in 5s.                                    |
| **3. Staging Deploy**    | Merge PR into Staging        | `stage`                                     | Triggers `stage.yml` CI, runs path-based matrix builds for changed folders, and redeploys Staging environment.        |
| **4. Release Candidate** | Open PR targeting Production | `stage` ➡️ `prod`                           | Auto-labeled `release-candidate`, title set with version name, and gets `release_candidate.md` checklist in 5s.       |
| **5. Production Deploy** | Merge RC PR into Production  | `prod`                                      | Triggers `prod.yml` to tag/promote GHCR images to `latest` and release version, and redeploys Production environment. |
| **6. Upstream Sync**     | Pull Upstream CE updates     | `upstream` ➡️ `main` ➡️ `sync/*` ➡️ `stage` | Fetch updates into mirror (`main`), branch off `stage` to resolve conflicts in a `sync/*` branch, and merge back.     |

### Automation Details (What is Managed Automatically)

To save development time and maintain consistency, several processes are completely automated:

| Automated Feature           | Powered By                   | Action / Trigger         | Detailed Behavior                                                                                                                             |
| :-------------------------- | :--------------------------- | :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Changelog & Releases**    | `release-please.yml`         | Push/merge to `prod`     | Parses conventional commits (`orca-*`), updates `CHANGELOG.md` with structured tables, bumps the package version, and drafts GitHub Releases. |
| **Path-Based Building**     | `stage.yml` + `paths-filter` | PR or push to `stage`    | Analyzes changed folders and builds only the modified applications using a parallel matrix. Unchanged services are skipped.                   |
| **PR Labeling & Templates** | `labeler.yml`                | Opening/synchronizing PR | Automatically labels PRs, renames RC PR titles with target version from `package.json`, and applies the correct template body.                |
| **Versioned Tagging**       | `prod.yml`                   | Push/merge to `prod`     | Reads release version from `package.json`, tags promoted GHCR images with `:v[Version]` and `:latest`, and pushes them.                       |

---

### Phase 1: Local Development & Feature Branching

1. **Branching**: Always branch off the **`stage`** branch:
   ```bash
   git checkout stage
   git pull origin stage
   git checkout -b feature/your-custom-feature
   ```
2. **Commit Hygiene**: Small, isolated commits. Use correct prefixes so **Release Please** can categorize your changes:
   | Commit Prefix | Description | Release Please Bump | Changelog Section |
   | :--------------------- | :----------------------------------------- | :------------------ | :---------------------- |
   | `orca-feat: [msg]` | Custom features, integrations, or sidecars | **Minor** | Features (Orca) |
   | `orca-fix: [msg]` | Bug fixes for custom code | **Patch** | Bug Fixes (Orca) |
   | `orca-ui: [msg]` | Branding, logo, or asset overrides | **Patch** | Branding & UI (Orca) |
   | `orca-style: [msg]` | Custom UI spacing or style improvements | _None_ | Styles (Orca) |
   | `orca-docs: [msg]` | Documentation updates | _None_ | Documentation (Orca) |
   | `orca-chore: [msg]` | Development setup and dependency changes | _None_ | Chores (Orca) |
   | `orca-refactor: [msg]` | Code refactoring or cleanup | _None_ | Code Refactoring (Orca) |

---

### Phase 2: Pull Request to Staging (`stage-pr`)

1. **Open the PR**: Create a PR targeting the **`stage`** branch.
2. **PR Naming**: Give the PR a title starting with your commit prefix (e.g. `orca-feat: hide upgrade button`).
3. **PR Description Warning**: Leave the description block empty (containing only the default warning comment) and click **"Create pull request"**.
4. **Auto-Templating**: Within 5 seconds, a background GitHub Action (`labeler.yml`) will:
   - Label the PR with `stage-pr`.
   - Overwrite the description with the standard **`basic.md`** template checklist.
5. **Fill out details**: Click "Edit" on the PR description and check off the items.

---

### Phase 3: Integration, CI Checks & Staging Deployment

Once you merge the PR into the **`stage`** branch, the **`stage.yml`** workflow triggers:

1. **Lint/Format checks**: Runs `pnpm check:format` and `pnpm check:lint` on workspace packages.
2. **Path-Based Change Detection**: Analyzes modified paths. It skips docker compilation for any application directories (`apps/web`, `apps/api`, etc.) that were not modified.
3. **Parallel Docker Builds**: Runs matrix builds concurrently on separate GitHub runners for modified services.
4. **Staging Deploy**: Triggers your staging Coolify server to redeploy using the newly built images from GHCR.

---

### Phase 4: Release Candidate & Production Promotion

When staging is verified and you are ready to release to production:

1. **Open the PR**: Create a PR from **`stage`** targeting the **`prod`** branch.
2. **PR Creation**: Do **NOT** edit the title or description when creating. Just click **"Create pull request"**.
3. **Auto-Templating & PR Naming**: The automation workflow will:
   - Label the PR with `release-candidate`.
   - Inspect `package.json`, read the new version number, and rename the PR title to: `orca-release: Promote Release Candidate v[Version]`.
   - Replace the description with the **`release_candidate.md`** QA checklist.
4. **Verify release**: Reviewers verify staging builds, check off database migration safety, confirm production environment variables are updated, and sign off on the QA items.
5. **Production Deploy**: Merging the PR into **`prod`** triggers the **`prod.yml`** workflow:
   - Pulls the built `:stage` images from GHCR.
   - Retags all images to `:latest` and the release version tag `:[Version]`.
   - Pushes them to GHCR and triggers Coolify to redeploy the production server.

---

### Phase 5: Upstream Syncing

To sync new releases from official Plane CE upstream into our fork:

1. Fetch upstream changes into your local mirror:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```
2. Create a temporary sync branch off **`stage`**:
   ```bash
   git checkout stage
   git pull origin stage
   git checkout -b sync/upstream-merge-[date]
   ```
3. Merge the mirror branch (`main`) into your sync branch:
   ```bash
   git merge main
   # Resolve any code, asset, or styling conflicts locally
   ```
4. Verify the build and check-in your fixes, then merge back to **`stage`**:
   ```bash
   # Once resolved and committed:
   git checkout stage
   git merge sync/upstream-merge-[date]
   git push origin stage
   git branch -d sync/upstream-merge-[date]
   ```
