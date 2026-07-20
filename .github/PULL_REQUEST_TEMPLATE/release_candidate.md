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
- [ ] **Commit Hygiene**: Checked that all custom commits use correct `orca-*` prefixes (`orca-feat`, `orca-fix`, `orca-ui`, etc.) so the changelog generates correctly.

---

> [!NOTE]
> **Post-Merge Automation:**
>
> 1. Merging this PR triggers the `prod.yml` workflow, promoting staging Docker images to `latest` and triggering the production deployment in Coolify.
> 2. `release-please` will automatically trigger to generate the correct version tag and changelog entries.
> 3. Staging (`stage`) will be automatically synced with `prod` via background GitHub Actions.
