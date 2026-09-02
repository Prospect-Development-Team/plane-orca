# Plane Migration Tools

Utility scripts for migrating workspace data between Plane installations.

## Migrated Entities Status

| Entity / Resource           | Migrated? | Notes / Behavior                                                                                                              |
| :-------------------------- | :-------: | :---------------------------------------------------------------------------------------------------------------------------- |
| **Projects**                |  ✅ Yes   | Recreated with the same name, identifier, and description.                                                                    |
| **Project Settings**        |  ✅ Yes   | Toggles for cycle, module, page, views, and intake layouts are synced.                                                        |
| **Workflow States**         |  ✅ Yes   | Syncs custom project workflow states (name, color, group). Maps issues to their correct state.                                |
| **Project Labels**          |  ✅ Yes   | Syncs custom project labels (name, color, description). Maps issues to their correct labels.                                  |
| **Cycles**                  |  ✅ Yes   | Recreated with name, description, start date, and end date.                                                                   |
| **Modules**                 |  ✅ Yes   | Recreated with name, description, status, start date, and end date.                                                           |
| **Issues / Work Items**     |  ✅ Yes   | Copied with title, description (HTML), and priority. Mapped to their respective state, labels, cycle, modules, and assignees. |
| **Users / Members**         |  ✅ Yes   | Workspace members are matched by email. If they don't exist, an invitation is sent to their email with their mapped role.     |
| **Project Memberships**     |  ✅ Yes   | Syncs project members with their correct matching role.                                                                       |
| **Estimates**               |  ✅ Yes   | Recreates project estimate point systems and links issues to their respective `estimate_point`.                               |
| **Comments**                |  ✅ Yes   | Syncs issue comment threads, mapping commentator user accounts where possible.                                                |
| **Issue Links**             |  ✅ Yes   | Syncs external links (GitHub PRs, reference URLs) associated with issues.                                                     |
| **Intake / Inbox Items**    |  ✅ Yes   | Syncs automatically when issues are migrated in their respective `triage` workflow states.                                    |
| **Stand-alone Attachments** |   ❌ No   | Downloads raw sidecar files from the source, uploads them to the target workspace generic asset store, and links to issues.   |
| **Views**                   |   ❌ No   | Saved views are not migrated. They require session authentication instead of API tokens.                                      |
| **Project Pages**           |   ❌ No   | Pages are not migrated. They require session authentication instead of API tokens.                                            |
| **Embedded Images / Files** |   ❌ No   | Inline images/files in issue descriptions are not re-uploaded; original URLs are preserved as-is in the description HTML.     |
| **User Stickies**           |   ❌ No   | Workspace sticky notes are not migrated.                                                                                      |

---

## Part 1: Pre-create User Accounts (On the Server hosting the new Plane database)

To assign issues, module leads, and project roles to the correct users, their email accounts must exist in the target database first. We can automate querying the old server and seeding them using `create_users.py`.

Because this script directly writes to the database using the Django ORM, **it must be run inside the new Plane container on your server**.

### Step A: Run from your server shell (via Docker pipe)

Run this command on your hosting server terminal where the container is running:

```bash
docker exec -i <new-plane-api-container-name> python3 - < tools/migration/create_users.py
```

_(If you are using Coolify, replace `<new-plane-api-container-name>` with the name of the container running your new Plane `api` service)._

### Step B (Alternative): Manual Copy-Paste inside the container

If you are already inside the container shell (`docker exec -it <container> sh`):

1. Run `cat > create_users.py` inside the container shell.
2. Paste the contents of `tools/migration/create_users.py` into the terminal.
3. Press `Ctrl + D` to save the file.
4. Run `python3 create_users.py`.
5. Remove the temp file when done: `rm create_users.py`.

_Note: Pre-created users are set with a temporary password `TemporaryOrca123!`. They can change this password under their profile settings upon logging in._

---

## Part 2: Run the Migration Script (On your local machine / client machine)

The data migration script (`migrate_data.py`) communicates purely over Plane's HTTP APIs, meaning **you can run it on your local developer machine** without having server access.

### 1. Install Dependencies

Make sure you have python virtual environment set up and dependencies installed:

```bash
# Create a virtual environment in the tools directory
python3 -m venv tools/migration/.venv

# Activate the virtual environment
source tools/migration/.venv/bin/activate

# Install dependencies
pip install requests python-dotenv
```

### 2. Configure Environment Variables

Make sure to add the following block to your `.env` file at the root of the project:

```env
# Migration Settings
MIGRATION_OLD_PLANE_URL="https://your-old-plane-domain.com"
MIGRATION_OLD_API_TOKEN="your-old-api-token"
MIGRATION_OLD_WORKSPACE_SLUG="your-old-workspace-slug"

MIGRATION_NEW_PLANE_URL="https://your-new-orca-domain.com"
MIGRATION_NEW_API_TOKEN="your-new-api-token"
MIGRATION_NEW_WORKSPACE_SLUG="your-new-workspace-slug"
```

### 3. Run the Script

Ensure your virtual environment is active, then run the script:

```bash
# If not already activated:
source tools/migration/.venv/bin/activate

# Run the script
python tools/migration/migrate_data.py
```
