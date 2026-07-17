## 🚀 Release Candidate Promotion Checklist

This pull request promotes code changes from the **`stage`** branch to the **`prod`** (Production) branch.

### 📝 Release Details

- **Target Version**: `v1.3.1-orca.X.Y.Z` (Check package.json / update version)
- **Release Branch**: `stage` -> `prod`

### 🚀 QA Verification Checklist

- [ ] **Staging Verified**: The latest staging deployment has been fully tested and verified to be stable.
- [ ] **Docker Images Built**: The staging builds completed successfully on GHCR.
- **Database Migrations Check**:
  - [ ] Checked if database migrations were generated (`makemigrations`) and applied (`migrate`) successfully in the staging environment.
  - [ ] Verified that migrations are non-destructive and safe for production data.
- **Secrets & Environment Check**:
  - [ ] Checked if any new secrets or environment variables were introduced.
  - [ ] Added/updated new variables in the Coolify Production environment variables tab.
- **Rollback Strategy**:
  - [ ] Verified that a rollback plan is ready (e.g. pinning image tag back to previous version in Coolify).

### 🔍 Changelog & Commit Hygiene

- [ ] All commits included in this promotion use the correct Conventional Commit prefixes (`orca-feat:`, `orca-fix:`, `orca-ui:`, etc.).
- [ ] Verified that `release-please` generated/updated the changelog correctly.
