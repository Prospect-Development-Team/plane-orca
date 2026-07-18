# Plane Migration Tools

Utility scripts for migrating and manipulating workspaces, projects, pages, and issues between Plane installations.

## Migration Script (`migrate_data.py`)

This script connects to a source (old) Plane instance using API tokens, retrieves its projects, pages, and issues, and creates/syncs them into the target (new) Plane Orca instance.

### Migrated Entities Status

| Entity / Resource           | Migrated? | Notes / Behavior                                                                                                                         |
| :-------------------------- | :-------: | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Projects**                |  ✅ Yes   | Recreated with the same name, identifier, and description.                                                                               |
| **Project Settings**        |  ✅ Yes   | Toggles for cycle, module, page, views, and intake layouts are synced.                                                                   |
| **Cycles**                  |  ✅ Yes   | Recreated with name, description, start date, and end date.                                                                              |
| **Modules**                 |  ✅ Yes   | Recreated with name, description, status, start date, and end date.                                                                      |
| **Views**                   |  ✅ Yes   | Recreated with name, description, access controls, and query filters.                                                                    |
| **Issues / Work Items**     |  ✅ Yes   | Copied with title, description (HTML), and priority. Mapped to their respective cycle/modules.                                           |
| **Project Pages**           |  ✅ Yes   | Copied with page title, description (HTML), and access control settings.                                                                 |
| **Embedded Images / Files** |  ✅ Yes   | Scanned from page/issue descriptions, downloaded from the old server, uploaded to the new server's storage, and target URLs are updated. |
| **Users / Members**         |  ✅ Yes   | Workspace members are matched by email. If they don't exist, an invitation is sent to their email with their mapped role.                |
| **Project Memberships**     |  ✅ Yes   | Maps project members with their respective roles.                                                                                        |
| **User Stickies**           |  ✅ Yes   | Migrates personal workspace dashboard sticky notes (title, description, colors).                                                         |
| **Stand-alone Attachments** |   ❌ No   | Attachments not directly referenced inside the page/issue content editor (like raw sidecar files) are not copied.                        |
| **Comments & History**      |   ❌ No   | Discarded to keep the migration footprint clean.                                                                                         |

---

## Setup & Execution

### 1. Install Dependencies

Create a virtual environment, activate it, and install the required dependencies:

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

### 3. Pre-create User Accounts in target database

To assign issues and project roles to the correct users, their email accounts must exist in the target database first. We can automate querying the old server and seeding them using `create_users.py`:

Run this command inside your target Plane `api` container (you can copy-paste this in the terminal):

```bash
docker exec -i <new-plane-api-container-name> python3 - < tools/migration/create_users.py
```

_(If you are using Coolify, replace `<new-plane-api-container-name>` with the name of the container running your new Plane `api` service)._

### 4. Run the Migration Script

Ensure your virtual environment is active, then run the script:

```bash
# If not already activated:
source tools/migration/.venv/bin/activate

# Run the script
python tools/migration/migrate_data.py
```
