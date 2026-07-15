# Agent Development Guide

## Commands

- `pnpm dev` - Start all dev servers (web:3000, admin:3001)
- `pnpm build` - Build all packages and apps
- `pnpm check` - Run all checks (format, lint, types)
- `pnpm check:lint` - OxLint across all packages
- `pnpm check:types` - TypeScript type checking
- `pnpm fix` - Auto-fix format and lint issues
- `pnpm turbo run <command> --filter=<package>` - Target specific package/app
- `pnpm --filter=@plane/ui storybook` - Start Storybook on port 6006

## Code Style

- **Imports**: Use `workspace:*` for internal packages, `catalog:` for external deps
- **TypeScript**: Strict mode enabled, all files must be typed
- **Formatting**: oxfmt, run `pnpm fix:format` (Frontend); Ruff is configured for Python formatting (`line-length = 120`, double quotes).
- **Linting**: OxLint with shared `.oxlintrc.json` config (Frontend); Ruff is used for Python linting (`E`, `F` rules) under `apps/api/`.
- **Naming**: camelCase for variables/functions, PascalCase for components/types
- **Error Handling**: Use try-catch with proper error types, log errors appropriately
- **State Management**: MobX stores in `packages/shared-state`, reactive patterns
- **Testing**: All features require unit tests, use existing test framework per package
- **Components**: Build in `@plane/ui` with Storybook for isolated development
- **Copyright Headers**: All new Python/TS/TSX files must include the standard copyright header via `addlicense` (see [COPYRIGHT_CHECK.md](./COPYRIGHT_CHECK.md)).

## Fork & Customization Strategy

All changes must follow the upstream compatibility model detailed in [FORK.md](./FORK.md):

- **Upstream Syncing**: Never commit custom logic or branding changes directly to the `main` branch. As an agent, always read and explicitly verify [FORK.md](./FORK.md) before implementing changes.

- **Non-Destructive Branding**: Do not rewrite React component imports for logos/assets. Instead, use asset overrides or inject custom CSS.
  - Logo SVG react components are located in [packages/propel/src/icons/brand](./packages/propel/src/icons/brand) (e.g. `plane-logo.tsx`, `plane-lockup.tsx`, `plane-wordmark.tsx`).
  - Public branding assets are located in [apps/web/public/plane-logos](./apps/web/public/plane-logos).

- **Wrapper Architecture**: Implement large/complex custom features as external sidecars/services, communicating with Plane via REST APIs and Webhooks.
- **Feature Toggles**: Disable unwanted core features using config or `.env` flags instead of deleting code blocks. Note that the frontend is a Vite-based react app, and env variables must be prefixed with `VITE_`.
  - _UI_: Hide unwanted elements using CSS or React display conditions.
  - _Backend_: NEVER delete database migration files or drop core tables directly to disable a feature.
- **Database Schema**: Do not modify core database tables. Prefer storing metadata in JSON fields or creating a separate relational sidecar model (e.g. `CustomIssueProperties`) to avoid migration conflicts.
- **Custom API Routes**: Register custom endpoints under a unique routing prefix (e.g., `/api/v1/custom/`) rather than modifying standard Plane route registries directly.
- **Versioning**: Tag custom releases using the format `v[UpstreamVersion]-orca.[ForkVersion]` (e.g. `v1.2.0-orca.1.0.0`) to track both upstream and custom releases.
- **Commit Prefixes**: Prefix custom changes based on category:
  - `orca(ui): [short description]` — Branding, logo, or color changes.
  - `orca(strip): [short description]` — Disabling/removing telemetry, upgrade prompts, or unused pages.
  - `orca(feat): [short description]` — Custom integrations, sidecars, or internal tools.
- **Atomic Commits**: Keep edits small and write semantic, isolated commits to make merging upstream updates easier.

## Token Efficiency & Command Guidelines

- **Minimize Output**: To conserve token usage, avoid running commands that generate large volumes of terminal output (e.g. `pnpm check`, long builds, full tests) directly through the agent context unless strictly necessary. Instead, the agent should list the commands for the developer to run locally.
- **Database Migrations**: When changes involve Django database models or backend updates that require schema changes, always remind the user to run the migration commands (e.g., `python apps/api/manage.py migrate` or similar docker-compose commands).
