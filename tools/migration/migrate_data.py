# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

import os
import re
import mimetypes
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

OLD_PLANE_URL = os.getenv("MIGRATION_OLD_PLANE_URL", "").rstrip("/")
OLD_API_TOKEN = os.getenv("MIGRATION_OLD_API_TOKEN", "")
OLD_WORKSPACE_SLUG = os.getenv("MIGRATION_OLD_WORKSPACE_SLUG", "")

NEW_PLANE_URL = os.getenv("MIGRATION_NEW_PLANE_URL", "").rstrip("/")
NEW_API_TOKEN = os.getenv("MIGRATION_NEW_API_TOKEN", "")
NEW_WORKSPACE_SLUG = os.getenv("MIGRATION_NEW_WORKSPACE_SLUG", "")

# Headers setup
old_headers = {
    "Authorization": f"Bearer {OLD_API_TOKEN}",
    "x-api-key": OLD_API_TOKEN,
    "Content-Type": "application/json",
}
new_headers = {
    "Authorization": f"Bearer {NEW_API_TOKEN}",
    "x-api-key": NEW_API_TOKEN,
    "Content-Type": "application/json",
}


def check_config():
    missing = []
    if not OLD_PLANE_URL or "your-old-plane" in OLD_PLANE_URL:
        missing.append("MIGRATION_OLD_PLANE_URL")
    if not OLD_API_TOKEN or "your-old-api" in OLD_API_TOKEN:
        missing.append("MIGRATION_OLD_API_TOKEN")
    if not OLD_WORKSPACE_SLUG or "your-old-workspace" in OLD_WORKSPACE_SLUG:
        missing.append("MIGRATION_OLD_WORKSPACE_SLUG")
    if not NEW_PLANE_URL or "your-new-orca" in NEW_PLANE_URL:
        missing.append("MIGRATION_NEW_PLANE_URL")
    if not NEW_API_TOKEN or "your-new-api" in NEW_API_TOKEN:
        missing.append("MIGRATION_NEW_API_TOKEN")
    if not NEW_WORKSPACE_SLUG or "your-new-workspace" in NEW_WORKSPACE_SLUG:
        missing.append("MIGRATION_NEW_WORKSPACE_SLUG")

    if missing:
        print("[-] Error: Please set the following variables in your .env file:")
        for var in missing:
            print(f"    - {var}")
        return False
    return True


def upload_asset_to_new_plane(project_id, file_name, file_bytes, content_type):
    """
    Generates a presigned URL on the new Plane Orca instance, uploads the asset
    binary, and marks it as uploaded. Returns the new asset URL.
    """
    try:
        payload = {
            "name": file_name,
            "type": content_type,
            "size": len(file_bytes),
            "project_id": project_id
        }
        res = requests.post(
            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/user-assets/",
            headers=new_headers,
            json={
                "name": file_name,
                "type": content_type,
                "size": len(file_bytes),
                "entity_type": "USER_COVER"
            }
        )
        if res.status_code not in [200, 201]:
            res = requests.post(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{project_id}/sources/",
                headers=new_headers,
                json=payload
            )

        if res.status_code not in [200, 201]:
            print(f"        [-] Failed to get presigned URL for {file_name}: {res.text}")
            return None

        data = res.json()
        upload_data = data.get("upload_data", {})
        asset_id = data.get("asset_id")
        asset_url = data.get("asset_url")

        url = upload_data.get("url")
        fields = upload_data.get("fields", {})
        files = {"file": (file_name, file_bytes, content_type)}

        upload_res = requests.post(url, data=fields, files=files)
        if upload_res.status_code not in [200, 201, 204]:
            print(f"        [-] Failed to upload asset bytes to storage: {upload_res.text}")
            return None

        patch_res = requests.patch(
            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/user-assets/{asset_id}/",
            headers=new_headers,
            json={"attributes": {"name": file_name, "type": content_type, "size": len(file_bytes)}}
        )
        if patch_res.status_code not in [200, 201, 204]:
            requests.patch(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{project_id}/sources/{asset_id}/",
                headers=new_headers,
                json={"is_uploaded": True}
            )

        return asset_url

    except Exception as e:
        print(f"        [-] Error uploading asset: {e}")
        return None


def process_html_assets(html_content, project_id):
    """
    Parses HTML content, finds all images/files pointing to the old server,
    downloads them, uploads them to the new server, and updates the URLs.
    """
    if not html_content:
        return html_content

    url_pattern = re.compile(rf'"{re.escape(OLD_PLANE_URL)}/api/v1/[^"]+assets/[^"]+"')
    urls_found = url_pattern.findall(html_content)
    if not urls_found:
        return html_content

    print(f"        [+] Found {len(urls_found)} asset references in content. Migrating them...")

    for old_url_with_quotes in set(urls_found):
        old_url = old_url_with_quotes.strip('"')
        try:
            asset_res = requests.get(old_url, headers=old_headers)
            if asset_res.status_code != 200:
                print(f"        [-] Could not download old asset: {old_url}")
                continue

            file_bytes = asset_res.content
            content_type = asset_res.headers.get("Content-Type", "image/jpeg")
            ext = mimetypes.guess_extension(content_type) or ".jpg"
            file_name = f"migrated_asset_{hash(old_url)}{ext}"

            new_url = upload_asset_to_new_plane(project_id, file_name, file_bytes, content_type)
            if new_url:
                print(f"        [+] Migrated asset: {old_url} -> {new_url}")
                html_content = html_content.replace(old_url, new_url)

        except Exception as e:
            print(f"        [-] Failed to process asset URL {old_url}: {e}")

    return html_content


def migrate():
    if not check_config():
        return

    # 1. Sync Workspace Users, Members, and Roles
    print("[+] Syncing workspace members...")
    user_email_to_new_id = {}  # email -> new_user_id
    old_user_id_to_email = {}  # old_user_id -> email
    
    try:
        # Fetch existing workspace members on target Plane Orca
        target_members_res = requests.get(
            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/members/",
            headers=new_headers,
        )
        target_members = target_members_res.json() if target_members_res.status_code == 200 else []
        for m in target_members:
            if m.get("member", {}).get("email"):
                user_email_to_new_id[m["member"]["email"]] = m["member"]["id"]
            elif m.get("email"):
                user_email_to_new_id[m["email"]] = m["id"]

        # Fetch old workspace members
        old_members_res = requests.get(
            f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/members/",
            headers=old_headers,
        )
        old_members = old_members_res.json() if old_members_res.status_code == 200 else []

        for om in old_members:
            email = om.get("member", {}).get("email") or om.get("email")
            role = om.get("role")
            old_id = om.get("member", {}).get("id") or om.get("id")
            
            if not email:
                continue

            old_user_id_to_email[old_id] = email

            # If user already exists in target workspace, map them
            if email in user_email_to_new_id:
                print(f"    [-] Member {email} already exists on target. Mapped.")
            else:
                # Invite member to the workspace
                invite_payload = {"email": email, "role": role}
                invite_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/invitations/",
                    headers=new_headers,
                    json=invite_payload,
                )
                if invite_res.status_code in [200, 201]:
                    print(f"    [+] Invited member {email} with role {role} to workspace.")
                else:
                    print(f"    [-] Failed to invite member {email}: {invite_res.text}")
    except Exception as e:
        print(f"    [-] Error syncing workspace members: {e}")

    # Helper function to map old user IDs to new user IDs
    def map_user_id(old_uid):
        if not old_uid:
            return None
        email = old_user_id_to_email.get(old_uid)
        if email and email in user_email_to_new_id:
            return user_email_to_new_id[email]
        return None

    # 2. Sync User Stickies
    print("[+] Syncing stickies...")
    try:
        target_stickies_res = requests.get(
            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/stickies/",
            headers=new_headers,
        )
        target_stickies_data = target_stickies_res.json()
        target_stickies = target_stickies_data.get("results", []) if isinstance(target_stickies_data, dict) else target_stickies_data
        existing_sticky_titles = {s.get("title") for s in target_stickies if s.get("title")}

        old_stickies_res = requests.get(
            f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/stickies/",
            headers=old_headers,
        )
        old_stickies_data = old_stickies_res.json()
        old_stickies = old_stickies_data.get("results", []) if isinstance(old_stickies_data, dict) else old_stickies_data

        for os in old_stickies:
            title = os.get("title")
            if not title or title in existing_sticky_titles:
                continue

            sticky_payload = {
                "title": title,
                "description": os.get("description", ""),
                "color": os.get("color", "#F5C146"),
            }
            requests.post(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/stickies/",
                headers=new_headers,
                json=sticky_payload
            )
            print(f"    [+] Synced sticky: {title}")
    except Exception as e:
        print(f"    [-] Error syncing stickies: {e}")

    # 3. Fetch projects from old Plane
    print(f"[+] Fetching projects from old Plane ({OLD_PLANE_URL})...")
    try:
        projects_res = requests.get(
            f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/",
            headers=old_headers,
        )
        projects_res.raise_for_status()
        projects = projects_res.json().get("results", [])
    except Exception as e:
        print(f"[-] Failed to fetch projects from old Plane: {e}")
        return

    for proj in projects:
        proj_name = proj["name"]
        proj_identifier = proj["identifier"]
        print(f"\n[+] Migrating project: {proj_name} ({proj_identifier})...")

        # 4. Create Project in New Plane (Orca)
        new_proj_payload = {
            "name": proj_name,
            "identifier": proj_identifier,
            "description": proj.get("description", ""),
            "network": proj.get("network", 2),
            "project_lead": map_user_id(proj.get("project_lead")),
            "emoji": proj.get("emoji", ""),
            "icon_prop": proj.get("icon_prop", None),
        }
        try:
            create_proj_res = requests.post(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/",
                headers=new_headers,
                json=new_proj_payload,
            )
            if create_proj_res.status_code in [200, 201]:
                new_proj = create_proj_res.json()
                new_proj_id = new_proj["id"]
                print(f"    [+] Created/found project on Orca: {proj_name}")
            else:
                print(f"    [!] Project creation response: {create_proj_res.status_code}. Attempting to fetch existing project ID...")
                new_proj_id_res = requests.get(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/",
                    headers=new_headers,
                )
                matching_projs = [p for p in new_proj_id_res.json().get("results", []) if p["identifier"] == proj_identifier]
                if matching_projs:
                    new_proj_id = matching_projs[0]["id"]
                    print(f"    [+] Found existing project ID on Orca: {new_proj_id}")
                else:
                    print(f"    [-] Could not create or find project {proj_name} on Orca. Skipping project.")
                    continue
        except Exception as e:
            print(f"    [-] Error migrating project {proj_name}: {e}")
            continue

        # Sync Project Cover Image
        if proj.get("cover_image"):
            old_cover_url = proj["cover_image"]
            try:
                cover_res = requests.get(old_cover_url, headers=old_headers)
                if cover_res.status_code == 200:
                    cover_bytes = cover_res.content
                    content_type = cover_res.headers.get("Content-Type", "image/jpeg")
                    new_cover_url = upload_asset_to_new_plane(new_proj_id, "project_cover.jpg", cover_bytes, content_type)
                    if new_cover_url:
                        requests.patch(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/",
                            headers=new_headers,
                            json={"cover_image": new_cover_url}
                        )
                        print("    [+] Synced project cover image.")
            except Exception as e:
                print(f"    [!] Failed to sync project cover image: {e}")

        # Update Project Feature Toggles
        try:
            patch_data = {
                "cycle_view": proj.get("cycle_view", True),
                "module_view": proj.get("module_view", True),
                "issue_views_view": proj.get("issue_views_view", True),
                "page_view": proj.get("page_view", True),
                "inbox_view": proj.get("inbox_view", True),
            }
            requests.patch(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/",
                headers=new_headers,
                json=patch_data
            )
            print("    [+] Synced project feature toggles.")
        except Exception as e:
            print(f"    [!] Failed to sync project feature toggles: {e}")

        # Sync Project Members
        print("    [+] Syncing project members...")
        try:
            old_pm_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/members/",
                headers=old_headers,
            )
            old_pms = old_pm_res.json() if old_pm_res.status_code == 200 else []

            new_pm_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/members/",
                headers=new_headers,
            )
            new_pms = new_pm_res.json() if new_pm_res.status_code == 200 else []
            new_pm_emails = {m.get("email") for m in new_pms if m.get("email")}

            for opm in old_pms:
                email = opm.get("member", {}).get("email") or opm.get("email")
                role = opm.get("role", 15)
                if not email or email in new_pm_emails:
                    continue

                if email in user_email_to_new_id:
                    member_payload = {"member": user_email_to_new_id[email], "role": role}
                    pm_add_res = requests.post(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/members/",
                        headers=new_headers,
                        json=member_payload
                    )
                    if pm_add_res.status_code in [200, 201]:
                        print(f"        [+] Added project member: {email}")
        except Exception as e:
            print(f"        [!] Failed to sync project members: {e}")

        # 5. Migrate Cycles
        print(f"    [+] Fetching cycles for project: {proj_name}...")
        cycle_mapping = {}
        try:
            target_cycles_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/cycles/",
                headers=new_headers,
            )
            existing_cycles = {c["name"]: c["id"] for c in target_cycles_res.json().get("results", [])} if target_cycles_res.status_code == 200 else {}

            cycles_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/cycles/",
                headers=old_headers,
            )
            cycles = cycles_res.json().get("results", [])
            for cycle in cycles:
                if cycle["name"] in existing_cycles:
                    print(f"        [-] Cycle '{cycle['name']}' already exists on Orca. Mapping to existing ID.")
                    cycle_mapping[cycle["id"]] = existing_cycles[cycle["name"]]
                    continue

                cycle_payload = {
                    "name": cycle["name"],
                    "description": cycle.get("description", ""),
                    "start_date": cycle.get("start_date", None),
                    "end_date": cycle.get("end_date", None),
                }
                c_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/cycles/",
                    headers=new_headers,
                    json=cycle_payload
                )
                if c_res.status_code in [200, 201]:
                    new_c = c_res.json()
                    cycle_mapping[cycle["id"]] = new_c["id"]
                    print(f"        [+] Created cycle: {cycle['name']}")
                else:
                    print(f"        [-] Failed to create cycle: {cycle['name']}: {c_res.text}")
        except Exception as e:
            print(f"        [-] Error migrating cycles: {e}")

        # 6. Migrate Modules
        print(f"    [+] Fetching modules for project: {proj_name}...")
        module_mapping = {}
        try:
            target_modules_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/",
                headers=new_headers,
            )
            existing_modules = {m["name"]: m["id"] for m in target_modules_res.json().get("results", [])} if target_modules_res.status_code == 200 else {}

            modules_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/modules/",
                headers=old_headers,
            )
            modules = modules_res.json().get("results", [])
            for module in modules:
                if module["name"] in existing_modules:
                    print(f"        [-] Module '{module['name']}' already exists on Orca. Mapping to existing ID.")
                    module_mapping[module["id"]] = existing_modules[module["name"]]
                    continue

                module_payload = {
                    "name": module["name"],
                    "description": module.get("description", ""),
                    "start_date": module.get("start_date", None),
                    "end_date": module.get("end_date", None),
                    "lead": map_user_id(module.get("lead")),
                    "status": module.get("status", "backlog"),
                }
                m_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/",
                    headers=new_headers,
                    json=module_payload
                )
                if m_res.status_code in [200, 201]:
                    new_m = m_res.json()
                    module_mapping[module["id"]] = new_m["id"]
                    print(f"        [+] Created module: {module['name']}")
                else:
                    print(f"        [-] Failed to create module: {module['name']}: {m_res.text}")
        except Exception as e:
            print(f"        [-] Error migrating modules: {e}")

        # 7. Migrate Views
        print(f"    [+] Fetching views for project: {proj_name}...")
        try:
            target_views_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/views/",
                headers=new_headers,
            )
            existing_views = {v["name"] for v in target_views_res.json().get("results", [])} if target_views_res.status_code == 200 else set()

            views_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/views/",
                headers=old_headers,
            )
            views = views_res.json().get("results", [])
            for view in views:
                if view["name"] in existing_views:
                    print(f"        [-] View '{view['name']}' already exists on Orca. Skipping.")
                    continue

                view_payload = {
                    "name": view["name"],
                    "description": view.get("description", ""),
                    "query": view.get("query", {}),
                    "access": view.get("access", "public"),
                }
                requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/views/",
                    headers=new_headers,
                    json=view_payload
                )
                print(f"        [+] Created view: {view['name']}")
        except Exception as e:
            print(f"        [-] Error migrating views: {e}")

        # 8. Migrate Project Pages
        print(f"    [+] Fetching pages for project: {proj_name}...")
        try:
            target_pages_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/pages/",
                headers=new_headers,
            )
            existing_page_names = {p["name"] for p in target_pages_res.json().get("results", [])} if target_pages_res.status_code == 200 else set()

            pages_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/pages/",
                headers=old_headers,
            )
            pages = pages_res.json().get("results", [])
            for page in pages:
                if page["name"] in existing_page_names:
                    print(f"        [-] Page '{page['name']}' already exists on Orca. Skipping.")
                    continue

                old_desc = page.get("description_html", "")
                new_desc = process_html_assets(old_desc, new_proj_id)

                new_page_payload = {
                    "name": page["name"],
                    "description_html": new_desc,
                    "access": page.get("access", 0),
                }
                create_page_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/pages/",
                    headers=new_headers,
                    json=new_page_payload,
                )
                if create_page_res.status_code in [200, 201]:
                    print(f"        [+] Imported page: {page['name']}")
                else:
                    print(f"        [-] Failed to import page {page['name']}: {create_page_res.text}")
        except Exception as e:
            print(f"        [-] Error migrating pages for project {proj_name}: {e}")

        # 9. Fetch Issues for the project from Old Plane
        print(f"    [+] Fetching issues for project: {proj_name}...")
        try:
            target_issues_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/",
                headers=new_headers,
            )
            existing_issue_names = {i["name"] for i in target_issues_res.json().get("results", [])} if target_issues_res.status_code == 200 else set()

            issues_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/",
                headers=old_headers,
            )
            issues = issues_res.json().get("results", [])
            print(f"    [+] Found {len(issues)} issues to migrate.")
            for issue in issues:
                if issue["name"] in existing_issue_names:
                    print(f"        [-] Issue '{issue['name']}' already exists on Orca. Skipping.")
                    continue

                old_desc = issue.get("description_html", "")
                new_desc = process_html_assets(old_desc, new_proj_id)

                mapped_cycle_id = None
                if issue.get("cycle") and issue["cycle"] in cycle_mapping:
                    mapped_cycle_id = cycle_mapping[issue["cycle"]]

                mapped_module_ids = []
                if issue.get("modules"):
                    for m_id in issue["modules"]:
                        if m_id in module_mapping:
                            mapped_module_ids.append(module_mapping[m_id])

                # Map assignees list
                mapped_assignees = []
                if issue.get("assignees"):
                    for old_uid in issue["assignees"]:
                        new_uid = map_user_id(old_uid)
                        if new_uid:
                            mapped_assignees.append(new_uid)

                new_issue_payload = {
                    "name": issue["name"],
                    "description_html": new_desc,
                    "priority": issue.get("priority", "none"),
                    "assignees": mapped_assignees,
                }
                
                if mapped_cycle_id:
                    new_issue_payload["cycle"] = mapped_cycle_id

                max_retries = 5
                retry_delay = 2
                for attempt in range(max_retries):
                    create_issue_res = requests.post(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/",
                        headers=new_headers,
                        json=new_issue_payload,
                    )
                    
                    if create_issue_res.status_code in [200, 201]:
                        new_issue = create_issue_res.json()
                        new_issue_id = new_issue["id"]
                        print(f"        [+] Imported issue: {issue['name']}")

                        if mapped_module_ids:
                            for mod_id in mapped_module_ids:
                                requests.post(
                                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/{mod_id}/module-issues/",
                                    headers=new_headers,
                                    json={"issues": [new_issue_id]}
                                )
                        break
                    elif create_issue_res.status_code == 429 or "RATE_LIMIT_EXCEEDED" in create_issue_res.text:
                        import time
                        print(f"        [!] Rate limit hit. Waiting {retry_delay}s (Attempt {attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        print(f"        [-] Failed to import issue {issue['name']}: {create_issue_res.text}")
                        break
                else:
                    print(f"        [-] Exceeded maximum retries for issue: {issue['name']}")

        except Exception as e:
            print(f"    [-] Error migrating issues for project {proj_name}: {e}")

    print("\n[+] Migration process completed!")


if __name__ == "__main__":
    migrate()
