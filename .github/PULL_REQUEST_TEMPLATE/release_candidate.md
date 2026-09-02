## 🚀 Release Candidate Promotion

This pull request promotes tested code changes from the **`stage`** branch to the **`prod`** (Production) branch.

### 📝 Release Info

- **Source:** `stage` ➡️ **Destination:** `prod`
- **Release Version:** _Automated after merge via `release-please`_

---

### 🚀 QA & Production Readiness Checklist

- [ ] **Staging Verified**: Staging environment build and deployment have been fully verified and tested.
- [ ] **Database Migrations**: Any database migrations (Django) have been reviewed, are safe to apply, and have been prepared.
- [ ] **Coolify Environment variables**: New environment variables (if any) are configured in the Coolify production application.
- [ ] **Commit Hygiene**: Checked that all custom commits use correct Conventional Commit format with `orca` scoping (e.g., `feat(orca):`, `fix(orca):`, etc.) so the changelog generates correctly.

---

> [!NOTE]
> **Post-Merge Automation:**
>
> 1. Merging this PR triggers `release-please` to open or update the official Release PR with the bumped version and changelog.
> 2. Merging the Release PR triggers `prod.yml` to build production Docker images directly from `prod`, push tagged images to GHCR, and redeploy the production environment in Coolify.
> 3. Staging (`stage`) is automatically synced back with `prod` via background GitHub Actions.
