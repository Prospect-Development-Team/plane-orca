# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

import os
import time
import requests
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
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

# Override requests.Session.request to globally handle HTTP 429 (Rate Limit Exceeded)
_original_request = requests.Session.request

def rate_limited_request(self, method, url, *args, **kwargs):
    max_retries = 10
    backoff = 30
    for attempt in range(max_retries):
        res = _original_request(self, method, url, *args, **kwargs)
        if res.status_code == 429:
            print(f"        [!] HTTP 429 RATE_LIMIT_EXCEEDED on {url}. Sleeping {backoff} seconds and retrying (attempt {attempt + 1}/{max_retries})...")
            time.sleep(backoff)
            continue
        return res
    return _original_request(self, method, url, *args, **kwargs)

requests.Session.request = rate_limited_request

# Session setup for connection pooling
old_session = requests.Session()
old_session.headers.update(old_headers)

new_session = requests.Session()
new_session.headers.update(new_headers)


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


def get_clean_url(url, base_url):
    """
    Rewrites any absolute API url to use the provided base_url, preserving path and query parameters.
    Handles cursor-based and offset-based pagination links securely.
    """
    if not url:
        return None
    parsed = urlparse(url)
    rebuilt_url = f"{base_url.rstrip('/')}{parsed.path}"
    if parsed.query:
        rebuilt_url += f"?{parsed.query}"
    return rebuilt_url


def get_next_cursor_url(current_url, next_cursor):
    """
    Updates the 'cursor' query parameter in current_url to next_cursor, returning the new URL.
    """
    parsed = urlparse(current_url)
    query_params = parse_qs(parsed.query)
    query_params['cursor'] = [next_cursor]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))


def fetch_all_paginated_results(url, headers, base_url):
    results = []
    current_url = url
    session = old_session if headers == old_headers else new_session
    while current_url:
        try:
            res = session.get(current_url, timeout=30)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    results.extend(data)
                    break
                elif isinstance(data, dict):
                    results.extend(data.get("results", []))
                    
                    # Check for cursor-based pagination
                    if "next_cursor" in data:
                        if data.get("next_page_results") and data.get("next_cursor"):
                            current_url = get_next_cursor_url(current_url, data.get("next_cursor"))
                        else:
                            current_url = None
                    else:
                        # Standard offset/page-based next link pagination
                        next_url = data.get("next")
                        current_url = get_clean_url(next_url, base_url)
                else:
                    break
            else:
                print(f"        [!] API request failed for {current_url}: HTTP {res.status_code} - {res.text[:200]}")
                break
        except Exception as e:
            print(f"        [!] Exception during API request for {current_url}: {e}")
            break
    return results


def get_list_from_response(res_data):
    """
    Safely retrieves a list from an API response which could be a raw list or a paginated dict.
    """
    if isinstance(res_data, list):
        return res_data
    if isinstance(res_data, dict):
        return res_data.get("results", [])
    return []


def migrate():
    if not check_config():
        return

    print("="*60)
    print("MIGRATION DETAILS SUMMARY:")
    print(f"  - Source URL            : {OLD_PLANE_URL}")
    print(f"  - Source Workspace Slug : {OLD_WORKSPACE_SLUG}")
    print(f"  - Target URL            : {NEW_PLANE_URL}")
    print(f"  - Target Workspace Slug : {NEW_WORKSPACE_SLUG}")
    print("="*60)
    confirm = input("[?] Proceed with migration? (Y/n): ").strip().lower()
    if confirm not in ["", "yes", "y"]:
        print("[-] Migration cancelled by user.")
        return

    # Ask user if they want to wipe the workspace
    wipe_choice = input("[?] Do you want to wipe the target workspace before migrating? (y/N): ").strip().lower()
    
    ask_per_project = True
    if wipe_choice not in ["yes", "y"]:
        ask_per_project_choice = input("[?] Ask/confirm before syncing each existing project? (Y/n): ").strip().lower()
        if ask_per_project_choice in ["no", "n"]:
            ask_per_project = False

    if wipe_choice in ["yes", "y"]:
        print("\n[!] Wiping target workspace...")
        # Delete projects (and their labels first to avoid ghost records)
        try:
            projects_to_delete = fetch_all_paginated_results(f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/?per_page=100", headers=new_headers, base_url=NEW_PLANE_URL)
            if projects_to_delete:
                for p in projects_to_delete:
                    p_id = p["id"]
                    p_name = p["name"]
                    # Delete all project labels first so they don't linger as ghost records
                    try:
                        lbl_res = requests.get(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{p_id}/labels/?per_page=500",
                            headers=new_headers
                        )
                        if lbl_res.status_code == 200:
                            for lbl in lbl_res.json().get("results", []):
                                requests.delete(
                                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{p_id}/labels/{lbl['id']}/",
                                    headers=new_headers
                                )
                    except Exception:
                        pass
                    # Rename the project before deleting — Plane soft-deletes and keeps the
                    # original name/identifier reserved, which would block re-creation.
                    # Renaming first frees the name+identifier immediately.
                    # NOTE: Plane identifiers must be 1-12 uppercase alphanumeric chars.
                    short_id = f"Z{int(time.time()) % 9999:04d}"  # e.g. Z1234 — always 5 chars
                    rename_res = requests.patch(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{p_id}/",
                        headers=new_headers,
                        json={"name": f"_wipe_{short_id}", "identifier": short_id}
                    )
                    if rename_res.status_code not in [200, 201]:
                        print(f"    [!] Pre-delete rename failed for {p_name}: {rename_res.text[:80]}")
                    del_res = requests.delete(f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{p_id}/", headers=new_headers)
                    if del_res.status_code == 204:
                        print(f"    [+] Deleted project: {p_name}")
                    else:
                        print(f"    [-] Failed to delete project {p_name}: {del_res.text}")
        except Exception as e:
            print(f"    [-] Error deleting projects: {e}")

        # Also purge workspace-level labels to avoid name conflicts on the next run
        try:
            ws_lbl_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/labels/?per_page=500",
                headers=new_headers
            )
            if ws_lbl_res.status_code == 200:
                ws_lbl_data = ws_lbl_res.json()
                ws_lbl_list = ws_lbl_data.get("results", []) if isinstance(ws_lbl_data, dict) else ws_lbl_data
                if isinstance(ws_lbl_list, list):
                    for lbl in ws_lbl_list:
                        requests.delete(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/labels/{lbl['id']}/",
                            headers=new_headers
                        )
                print("    [+] Purged workspace-level labels.")
        except Exception as e:
            print(f"    [-] Error purging workspace labels: {e}")

        print("[!] Target workspace wiped successfully.\n")

    # Statistics Summary Tracking
    stats = {
        "workspace_members_invited": 0,
        "workspace_members_failed": 0,
        "projects_migrated": 0,
        "cycles_migrated": 0,
        "cycles_failed": 0,
        "modules_migrated": 0,
        "modules_failed": 0,
        "states_migrated": 0,
        "states_failed": 0,
        "labels_migrated": 0,
        "labels_failed": 0,
        "issues_migrated": 0,
        "issues_failed": 0,
        "errors": []
    }

    # 1. Sync Workspace Users, Members, and Roles
    print("[+] Syncing workspace members...")
    user_email_to_new_id = {}
    old_user_id_to_email = {}
    
    try:
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

            if email in user_email_to_new_id:
                print(f"    [-] Member {email} already exists on target. Mapped.")
            else:
                invite_payload = {"email": email, "role": role}
                invite_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/invitations/",
                    headers=new_headers,
                    json=invite_payload,
                )
                if invite_res.status_code in [200, 201]:
                    print(f"    [+] Invited member {email} with role {role} to workspace.")
                    stats["workspace_members_invited"] += 1
                else:
                    err_msg = f"Failed to invite member {email}: {invite_res.text}"
                    stats["workspace_members_failed"] += 1
                    stats["errors"].append(err_msg)
                    print(f"    [-] {err_msg}")
    except Exception as e:
        stats["errors"].append(f"Error syncing workspace members: {e}")
        print(f"    [-] Error syncing workspace members: {e}")

    def map_user_id(old_uid):
        if not old_uid:
            return None
        email = old_user_id_to_email.get(old_uid)
        if email and email in user_email_to_new_id:
            return user_email_to_new_id[email]
        return None

    current_new_user_id = None
    try:
        user_me_res = requests.get(f"{NEW_PLANE_URL}/api/v1/users/me/", headers=new_headers)
        if user_me_res.status_code == 200:
            current_new_user_id = user_me_res.json().get("id")
    except Exception:
        pass

    # 3. Fetch projects from old Plane
    print(f"[+] Fetching projects from old Plane ({OLD_PLANE_URL})...")
    try:
        projects = fetch_all_paginated_results(
            f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/?per_page=100",
            old_headers,
            OLD_PLANE_URL
        )
        if not projects:
            print("[-] No projects found on old Plane (or request failed).")
    except Exception as e:
        print(f"[-] Failed to fetch projects from old Plane: {e}")
        return

    # Fetch existing projects from target Plane
    print(f"[+] Fetching existing projects from target ({NEW_PLANE_URL})...")
    existing_target_projs_map = {}
    try:
        target_projects = fetch_all_paginated_results(
            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/?per_page=100",
            new_headers,
            NEW_PLANE_URL
        )
        for tp in target_projects:
            if isinstance(tp, dict) and tp.get("identifier"):
                existing_target_projs_map[tp["identifier"]] = tp
    except Exception as e:
        print(f"[!] Warning: Could not fetch existing projects from target: {e}")

    for proj in projects:
        proj_name = proj["name"]
        proj_identifier = proj["identifier"]
        print(f"\n[+] Migrating project: {proj_name} ({proj_identifier})...")

        new_proj_id = None
        existing_proj = existing_target_projs_map.get(proj_identifier)
        if existing_proj:
            if ask_per_project:
                ans = input(f"    [?] Project '{proj_name}' ({proj_identifier}) already exists on target. Sync/update it? (y/N): ").strip().lower()
                if ans not in ['y', 'yes']:
                    print(f"    [-] Skipping project sync.")
                    continue
            new_proj_id = existing_proj["id"]
            print(f"    [+] Updating existing project: {proj_name}")

        # 4. Create Project in New Plane (Orca)
        if not new_proj_id:
            new_proj_payload = {
                "name": proj_name,
                "identifier": proj_identifier,
                "description": proj.get("description", ""),
                "network": proj.get("network", 2),
                "inbox_view": proj.get("inbox_view", proj.get("intake_view", True)),
            }
            # Only include optional fields when they have a real value — Plane rejects
            # null/empty for project_lead, emoji, and icon_prop with a generic error.
            mapped_lead = map_user_id(proj.get("project_lead"))
            if mapped_lead:
                new_proj_payload["project_lead"] = mapped_lead
            if proj.get("emoji"):
                new_proj_payload["emoji"] = proj["emoji"]
            if proj.get("icon_prop"):
                new_proj_payload["icon_prop"] = proj["icon_prop"]
            try:
                create_proj_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/",
                    headers=new_headers,
                    json=new_proj_payload,
                )
                if create_proj_res.status_code in [200, 201]:
                    new_proj = create_proj_res.json()
                    new_proj_id = new_proj["id"]
                    print(f"    [+] Created project on Orca: {proj_name}")
                    stats["projects_migrated"] += 1
                else:
                    # The Orca API sometimes creates the project but returns an error status.
                    # Check if the response body contains an 'id' before doing a GET lookup.
                    try:
                        resp_body = create_proj_res.json()
                        if resp_body.get("id"):
                            new_proj_id = resp_body["id"]
                            print(f"    [+] Created project on Orca: {proj_name} (HTTP {create_proj_res.status_code}, project was still created)")
                            stats["projects_migrated"] += 1
                    except Exception:
                        pass

                    if not new_proj_id:
                        new_proj_id_res = requests.get(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/",
                            headers=new_headers,
                        )
                        matching_projs = [p for p in new_proj_id_res.json().get("results", []) if p["identifier"] == proj_identifier]
                        if matching_projs:
                            new_proj_id = matching_projs[0]["id"]
                            print(f"    [!] Project creation error but project found by identifier: {new_proj_id} ({create_proj_res.text[:80]})")
                            stats["projects_migrated"] += 1
                        else:
                            print(f"    [-] Could not create or find project {proj_name} on Orca. Skipping. ({create_proj_res.text[:80]})")
            except Exception as e:
                print(f"    [-] Error creating project {proj_name}: {e}")

        if not new_proj_id:
            continue


        # Ensure the migrating token user is a member of the project on target (required for listing labels, cycles, etc.)
        if current_new_user_id:
            try:
                requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/project-members/",
                    headers=new_headers,
                    json={"member": current_new_user_id, "role": 20}
                )
            except Exception:
                pass

        # Update Project Feature Toggles
        try:
            patch_data = {
                "cycle_view": proj.get("cycle_view", True),
                "module_view": proj.get("module_view", True),
                "issue_views_view": proj.get("issue_views_view", True),
                "page_view": proj.get("page_view", True),
                "inbox_view": proj.get("inbox_view", proj.get("intake_view", True)),
                "intake_view": proj.get("intake_view", proj.get("inbox_view", True)),
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
            old_pms = get_list_from_response(old_pm_res.json()) if old_pm_res.status_code == 200 else []

            new_pm_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/members/",
                headers=new_headers,
            )
            new_pms = get_list_from_response(new_pm_res.json()) if new_pm_res.status_code == 200 else []
            new_pm_emails = {m.get("member", {}).get("email"): m for m in new_pms if isinstance(m, dict) and m.get("member", {}).get("email")}

            for opm in old_pms:
                email = opm.get("member", {}).get("email") or opm.get("email")
                role = opm.get("role", 15)
                if not email:
                    continue

                if email in new_pm_emails:
                    target_pm = new_pm_emails[email]
                    if target_pm.get("role") != role:
                        requests.patch(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/members/{target_pm['id']}/",
                            headers=new_headers,
                            json={"role": role}
                        )
                        print(f"        [+] Updated role for project member: {email} -> {role}")
                else:
                    if email in user_email_to_new_id:
                        member_payload = {"member": user_email_to_new_id[email], "role": role}
                        pm_add_res = requests.post(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/members/",
                            headers=new_headers,
                            json=member_payload
                        )
                        if pm_add_res.status_code in [200, 201]:
                            print(f"        [+] Added project member: {email} with role {role}")
        except Exception as e:
            print(f"        [!] Failed to sync project members: {e}")

        # Migrate Project Estimates
        print("    [+] Syncing project estimates and points...")
        estimate_mapping = {}
        estimate_point_mapping = {}
        try:
            # Fetch existing estimates on target
            target_estimates_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/estimates/",
                headers=new_headers,
                timeout=30
            )
            existing_estimates = {}
            if target_estimates_res.status_code == 200:
                est_list = get_list_from_response(target_estimates_res.json())
                existing_estimates = {e["name"]: e for e in est_list if isinstance(e, dict) and e.get("name")}

            # Fetch source estimates
            source_estimates_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/estimates/",
                headers=old_headers,
                timeout=30
            )
            source_estimates = get_list_from_response(source_estimates_res.json()) if source_estimates_res.status_code == 200 else []
            
            for est in source_estimates:
                est_name = est["name"]
                target_est_id = None
                if est_name in existing_estimates:
                    print(f"        [-] Estimate '{est_name}' already exists on Orca. Mapping.")
                    target_est_id = existing_estimates[est_name]["id"]
                    estimate_mapping[est["id"]] = target_est_id
                else:
                    est_payload = {
                        "name": est_name,
                        "description": est.get("description", ""),
                    }
                    create_est_res = requests.post(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/estimates/",
                        headers=new_headers,
                        json=est_payload,
                        timeout=30
                    )
                    if create_est_res.status_code in [200, 201]:
                        new_est = create_est_res.json()
                        target_est_id = new_est["id"]
                        estimate_mapping[est["id"]] = target_est_id
                        print(f"        [+] Created estimate system: {est_name}")
                    else:
                        print(f"        [-] Failed to create estimate system {est_name}: {create_est_res.text}")

                if target_est_id:
                    # Sync estimate points
                    # Fetch existing target points
                    target_pts_res = requests.get(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/estimates/{target_est_id}/estimate-points/",
                        headers=new_headers,
                        timeout=30
                    )
                    existing_pts = {}
                    if target_pts_res.status_code == 200:
                        pts_list = get_list_from_response(target_pts_res.json())
                        existing_pts = {str(p["key"]): p for p in pts_list if isinstance(p, dict) and p.get("key") is not None}

                    # Fetch source points
                    source_pts_res = requests.get(
                        f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/estimates/{est['id']}/estimate-points/",
                        headers=old_headers,
                        timeout=30
                    )
                    source_pts = get_list_from_response(source_pts_res.json()) if source_pts_res.status_code == 200 else []
                    
                    for pt in source_pts:
                        pt_key = str(pt["key"])
                        if pt_key in existing_pts:
                            estimate_point_mapping[pt["id"]] = existing_pts[pt_key]["id"]
                        else:
                            pt_payload = {
                                "key": pt["key"],
                                "value": pt.get("value", 0),
                            }
                            create_pt_res = requests.post(
                                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/estimates/{target_est_id}/estimate-points/",
                                headers=new_headers,
                                json=pt_payload,
                                timeout=30
                            )
                            if create_pt_res.status_code in [200, 201]:
                                new_pt = create_pt_res.json()
                                estimate_point_mapping[pt["id"]] = new_pt["id"]
                            else:
                                print(f"        [-] Failed to create estimate point {pt_key}: {create_pt_res.text}")
        except Exception as e:
            print(f"        [!] Failed to sync project estimates: {e}")

        # Migrate Project States
        print("    [+] Syncing project workflow states...")
        state_mapping = {}
        try:
            target_states_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/states/",
                headers=new_headers,
            )
            existing_states = {}
            if target_states_res.status_code == 200:
                s_list = get_list_from_response(target_states_res.json())
                existing_states = {s["name"]: s for s in s_list if isinstance(s, dict) and s.get("name")}

            states_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/states/",
                headers=old_headers,
            )
            states = get_list_from_response(states_res.json()) if states_res.status_code == 200 else []
            for state in states:
                state_name = state["name"]
                if state_name in existing_states:
                    print(f"        [-] State '{state_name}' already exists on Orca. Mapping.")
                    state_mapping[state["id"]] = existing_states[state_name]["id"]
                    
                    target_state = existing_states[state_name]
                    if target_state.get("color") != state.get("color") or target_state.get("group") != state.get("group"):
                        requests.patch(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/states/{target_state['id']}/",
                            headers=new_headers,
                            json={"color": state.get("color"), "group": state.get("group")}
                        )
                    continue

                state_payload = {
                    "name": state_name,
                    "color": state.get("color", "#CCCCCC"),
                    "group": state.get("group", "backlog"),
                    "description": state.get("description", ""),
                    "project_id": new_proj_id,
                    "default": False
                }
                st_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/states/",
                    headers=new_headers,
                    json=state_payload
                )
                if st_res.status_code in [200, 201]:
                    new_st = st_res.json()
                    state_mapping[state["id"]] = new_st["id"]
                    stats["states_migrated"] += 1
                    print(f"        [+] Created state: {state_name}")
                else:
                    err_msg = f"Failed to create state {state_name}: {st_res.text}"
                    stats["states_failed"] += 1
                    stats["errors"].append(err_msg)
                    print(f"        [-] {err_msg}")
        except Exception as e:
            print(f"        [-] Error migrating states: {e}")

        # Migrate Project Labels
        print("    [+] Syncing project labels...")
        label_mapping = {}
        try:
            target_labels_res = requests.get(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/labels/",
                headers=new_headers,
            )
            existing_labels = {}
            if target_labels_res.status_code == 200:
                l_list = get_list_from_response(target_labels_res.json())
                existing_labels = {l["name"]: l for l in l_list if isinstance(l, dict) and l.get("name")}

            labels_res = requests.get(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/labels/",
                headers=old_headers,
            )
            labels = get_list_from_response(labels_res.json()) if labels_res.status_code == 200 else []
            for label in labels:
                label_name = label["name"]
                if label_name in existing_labels:
                    print(f"        [-] Label '{label_name}' already exists on Orca. Mapping.")
                    label_mapping[label["id"]] = existing_labels[label_name]["id"]
                    continue

                lbl_payload = {
                    "name": label_name,
                    "color": label.get("color", "#CCCCCC"),
                }
                lbl_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/labels/",
                    headers=new_headers,
                    json=lbl_payload
                )
                if lbl_res.status_code in [200, 201]:
                    new_lbl = lbl_res.json()
                    label_mapping[label["id"]] = new_lbl["id"]
                    stats["labels_migrated"] += 1
                    print(f"        [+] Created label: {label_name}")
                else:
                    # Fallback to checking if workspace-level label matches
                    workspace_labels_res = requests.get(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/labels/",
                        headers=new_headers
                    )
                    workspace_labels = get_list_from_response(workspace_labels_res.json()) if workspace_labels_res.status_code == 200 else []
                    matching_labels = [wl for wl in workspace_labels if wl.get("name") == label_name]
                    if matching_labels:
                        label_mapping[label["id"]] = matching_labels[0]["id"]
                        print(f"        [~] Label '{label_name}' found on Orca (workspace-level). Mapped.")
                    else:
                        err_msg = f"Failed to create label {label_name}: {lbl_res.text}"
                        stats["labels_failed"] += 1
                        stats["errors"].append(err_msg)
                        print(f"        [-] {err_msg}")
        except Exception as e:
            print(f"        [-] Error migrating labels: {e}")

        # 5. Migrate Cycles
        print("    [+] Syncing project cycles...")
        cycle_mapping = {}
        cycle_id_to_name = {}
        cycle_issue_mapping = {}
        try:
            target_cycles = fetch_all_paginated_results(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/cycles/?per_page=100",
                new_headers,
                NEW_PLANE_URL
            )
            existing_cycles = {c["name"]: c["id"] for c in target_cycles}
            for c in target_cycles:
                cycle_id_to_name[c["id"]] = c["name"]

            cycles = fetch_all_paginated_results(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/cycles/?per_page=100",
                old_headers,
                OLD_PLANE_URL
            )
            for cycle in cycles:
                try:
                    cycle_issues = fetch_all_paginated_results(
                        f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/cycles/{cycle['id']}/cycle-issues/?per_page=100",
                        old_headers,
                        OLD_PLANE_URL
                    )
                    for ci in cycle_issues:
                        old_issue_id = ci.get("id") or ci.get("issue") or ci.get("issue_detail", {}).get("id") or ci.get("issue_id")
                        if old_issue_id:
                            cycle_issue_mapping[old_issue_id] = cycle["id"]
                except Exception as e:
                    print(f"        [!] Error pre-fetching issues for old cycle {cycle['name']}: {e}")

                if cycle["name"] in existing_cycles:
                    print(f"        [-] Cycle '{cycle['name']}' already exists on Orca. Mapping to existing ID.")
                    cycle_mapping[cycle["id"]] = existing_cycles[cycle["name"]]
                    continue

                start_date = cycle.get("start_date")
                end_date = cycle.get("end_date")
                if start_date and end_date and start_date > end_date:
                    start_date, end_date = end_date, start_date

                cycle_payload = {
                    "name": cycle["name"],
                    "description": cycle.get("description", ""),
                    "start_date": start_date,
                    "end_date": end_date,
                    "project_id": new_proj_id,
                }
                cy_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/cycles/",
                    headers=new_headers,
                    json=cycle_payload
                )
                if cy_res.status_code in [200, 201]:
                    new_cy = cy_res.json()
                    cycle_mapping[cycle["id"]] = new_cy["id"]
                    cycle_id_to_name[new_cy["id"]] = cycle["name"]
                    stats["cycles_migrated"] += 1
                    print(f"        [+] Created cycle: {cycle['name']}")
                else:
                    err_msg = f"Failed to create cycle {cycle['name']}: {cy_res.text}"
                    stats["cycles_failed"] += 1
                    stats["errors"].append(err_msg)
                    print(f"        [-] {err_msg}")
        except Exception as e:
            print(f"        [-] Error migrating cycles: {e}")

        # 6. Migrate Modules
        print("    [+] Syncing project modules...")
        module_mapping = {}
        module_id_to_name = {}
        module_issue_mapping = {}
        try:
            target_modules = fetch_all_paginated_results(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/?per_page=100",
                new_headers,
                NEW_PLANE_URL
            )
            existing_modules = {m["name"]: m["id"] for m in target_modules}
            for m in target_modules:
                module_id_to_name[m["id"]] = m["name"]

            modules = fetch_all_paginated_results(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/modules/?per_page=100",
                old_headers,
                OLD_PLANE_URL
            )
            for module in modules:
                try:
                    module_issues = fetch_all_paginated_results(
                        f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/modules/{module['id']}/module-issues/?per_page=100",
                        old_headers,
                        OLD_PLANE_URL
                    )
                    for mi in module_issues:
                        old_issue_id = mi.get("id") or mi.get("issue") or mi.get("issue_detail", {}).get("id") or mi.get("issue_id")
                        if old_issue_id:
                            if old_issue_id not in module_issue_mapping:
                                module_issue_mapping[old_issue_id] = []
                            module_issue_mapping[old_issue_id].append(module["id"])
                except Exception as e:
                    print(f"        [!] Error pre-fetching issues for old module {module['name']}: {e}")

                if module["name"] in existing_modules:
                    print(f"        [-] Module '{module['name']}' already exists on Orca. Mapping to existing ID.")
                    module_mapping[module["id"]] = existing_modules[module["name"]]
                    continue

                module_payload = {
                    "name": module["name"],
                    "description": module.get("description", ""),
                    "start_date": module.get("start_date"),
                    "target_date": module.get("target_date"),
                }
                m_res = requests.post(
                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/",
                    headers=new_headers,
                    json=module_payload
                )
                if m_res.status_code in [200, 201]:
                    new_m = m_res.json()
                    module_mapping[module["id"]] = new_m["id"]
                    module_id_to_name[new_m["id"]] = module["name"]
                    stats["modules_migrated"] += 1
                    print(f"        [+] Created module: {module['name']}")
                else:
                    err_msg = f"Failed to create module {module['name']}: {m_res.text}"
                    stats["modules_failed"] += 1
                    stats["errors"].append(err_msg)
                    print(f"        [-] {err_msg}")
        except Exception as e:
            print(f"        [-] Error migrating modules: {e}")



        # 9. Fetch Issues for the project from Old Plane
        print(f"    [+] Fetching issues for project: {proj_name}...")
        try:
            # Fetch all existing issues from the target (paginated) to detect duplicates/changes
            existing_issues = fetch_all_paginated_results(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/?per_page=100",
                new_headers,
                NEW_PLANE_URL
            )
            existing_issues_map = {i["name"]: i for i in existing_issues if i.get("name")}

            # Fetch existing intake issues on the target project to prevent duplicates/changes
            existing_intake_issues = fetch_all_paginated_results(
                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/intake-issues/?per_page=100",
                new_headers,
                NEW_PLANE_URL
            )
            existing_intake_map = {}
            for ei in existing_intake_issues:
                det = ei.get("issue_detail")
                if isinstance(det, dict) and det.get("name"):
                    existing_intake_map[det["name"]] = ei

            # Fetch ALL source issues across all pages using clean cursor/offset navigation
            issues = fetch_all_paginated_results(
                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/?per_page=100",
                old_headers,
                OLD_PLANE_URL
            )

            # Fetch old intake issues — build a map keyed by inner issue ID
            old_intake_issue_map = {}
            try:
                old_intake_issues = fetch_all_paginated_results(
                    f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/intake-issues/?per_page=100",
                    old_headers,
                    OLD_PLANE_URL
                )
                issues_ids_in_main = {i.get("id") for i in issues if i.get("id")}
                for oi in old_intake_issues:
                    issue_detail = oi.get("issue_detail") if isinstance(oi.get("issue_detail"), dict) else None
                    issue_id = oi.get("issue") or oi.get("issue_id") or (issue_detail or {}).get("id")
                    if issue_id:
                        old_intake_issue_map[issue_id] = oi
                        # Pending intake issues (status=-2) are NOT in the main /issues/ list.
                        # Inject their issue_detail into our issues list so they get migrated.
                        if issue_id not in issues_ids_in_main and issue_detail:
                            issues.append(issue_detail)
                            issues_ids_in_main.add(issue_id)
                print(f"    [+] Found {len(old_intake_issue_map)} intake issues ({sum(1 for oi in old_intake_issues if oi.get('status', -2) == -2)} pending).")
            except Exception as e:
                print(f"        [!] Error pre-fetching old intake issues: {e}")

            # Map user new ID back to email for printing assignees
            user_id_to_email = {uid: email for email, uid in user_email_to_new_id.items()}

            cycle_associations = {}
            module_associations = {}

            print(f"    [+] Found {len(issues)} issues to migrate (including intake-only).")
            for idx, issue in enumerate(issues, start=1):
                old_issue_id = issue.get("id")
                is_intake_issue = old_issue_id in old_intake_issue_map
                old_desc = issue.get("description_html", "")

                # Map cycle (handle relationship pre-fetch mapping first, then fallback to API keys)
                mapped_cycle_id = None
                old_issue_id = issue.get("id")
                old_cycle_id = cycle_issue_mapping.get(old_issue_id)
                if not old_cycle_id:
                    cycle_data = issue.get("cycle_id") or issue.get("cycle")
                    if cycle_data:
                        old_cycle_id = cycle_data.get("id") if isinstance(cycle_data, dict) else cycle_data
                if old_cycle_id and old_cycle_id in cycle_mapping:
                    mapped_cycle_id = cycle_mapping[old_cycle_id]

                # Map modules (handle relationship pre-fetch mapping first, then fallback to API keys)
                mapped_module_ids = []
                old_module_ids = module_issue_mapping.get(old_issue_id, [])
                if not old_module_ids:
                    modules_data = issue.get("module_ids") or issue.get("modules")
                    if modules_data:
                        for m in modules_data:
                            m_id = m.get("id") if isinstance(m, dict) else m
                            if m_id:
                                old_module_ids.append(m_id)
                for om_id in old_module_ids:
                    if om_id in module_mapping:
                        mapped_module_ids.append(module_mapping[om_id])

                # Map assignees (handle both assignee_ids list and nested assignees objects)
                mapped_assignees = []
                assignees_data = issue.get("assignee_ids") or issue.get("assignees")
                if assignees_data:
                    for old_uid in assignees_data:
                        uid = old_uid.get("id") if isinstance(old_uid, dict) else old_uid
                        new_uid = map_user_id(uid)
                        if new_uid:
                            mapped_assignees.append(new_uid)

                # Map state (handle both state_id and nested state object)
                mapped_state_id = None
                state_data = issue.get("state_id") or issue.get("state")
                if state_data:
                    old_state_id = state_data.get("id") if isinstance(state_data, dict) else state_data
                    if old_state_id and old_state_id in state_mapping:
                        mapped_state_id = state_mapping[old_state_id]

                # Map issue labels (handle both label_ids list and nested labels objects)
                mapped_labels = []
                labels_data = issue.get("label_ids") or issue.get("labels")
                if labels_data:
                    for old_lbl in labels_data:
                        lbl_id = old_lbl.get("id") if isinstance(old_lbl, dict) else old_lbl
                        if lbl_id and lbl_id in label_mapping:
                            mapped_labels.append(label_mapping[lbl_id])
                
                # Map estimate point
                mapped_estimate_point = None
                old_est_pt = issue.get("estimate_point")
                if old_est_pt and old_est_pt in estimate_point_mapping:
                    mapped_estimate_point = estimate_point_mapping[old_est_pt]

                # Map issue creator
                old_created_by = issue.get("created_by")
                if isinstance(old_created_by, dict):
                    old_created_by = old_created_by.get("id")
                mapped_created_by = map_user_id(old_created_by) or current_new_user_id

                new_issue_payload = {
                    "name": issue["name"],
                    "description_html": old_desc,
                    "priority": issue.get("priority", "none"),
                    "assignees": mapped_assignees,
                    "assignee_ids": mapped_assignees,
                    "labels": mapped_labels,
                    "label_ids": mapped_labels,
                }
                
                if mapped_created_by:
                    new_issue_payload["created_by"] = mapped_created_by

                if mapped_estimate_point:
                    new_issue_payload["estimate_point"] = mapped_estimate_point
                
                if mapped_state_id:
                    new_issue_payload["state"] = mapped_state_id
                    new_issue_payload["state_id"] = mapped_state_id

                is_intake_issue = old_issue_id in old_intake_issue_map

                # Check if the issue already exists on target (Orca) to update if needed
                existing_record = existing_intake_map.get(issue["name"]) if is_intake_issue else existing_issues_map.get(issue["name"])
                if existing_record:
                    target_issue_obj = existing_record.get("issue_detail") if is_intake_issue else existing_record
                    target_issue_id = target_issue_obj.get("id")
                    
                    changes = {}
                    
                    # 1. Compare description_html
                    desc_target = target_issue_obj.get("description_html") or ""
                    desc_source = old_desc or ""
                    if desc_target != desc_source:
                        changes["description_html"] = desc_source
                        
                    # 2. Compare priority
                    if target_issue_obj.get("priority") != issue.get("priority", "none"):
                        changes["priority"] = issue.get("priority", "none")
                        
                    # 3. Compare state
                    if mapped_state_id:
                        target_state = target_issue_obj.get("state")
                        target_state_id = target_state.get("id") if isinstance(target_state, dict) else target_state
                        if target_state_id != mapped_state_id:
                            changes["state"] = mapped_state_id
                            changes["state_id"] = mapped_state_id

                    # 4. Compare estimate point
                    if mapped_estimate_point:
                        target_est = target_issue_obj.get("estimate_point")
                        target_est_id = target_est.get("id") if isinstance(target_est, dict) else target_est
                        if target_est_id != mapped_estimate_point:
                            changes["estimate_point"] = mapped_estimate_point

                    # 5. Compare assignees
                    target_assignees = target_issue_obj.get("assignee_ids") or target_issue_obj.get("assignees") or []
                    target_assignee_ids = [
                        a.get("id") if isinstance(a, dict) else a
                        for a in target_assignees
                    ]
                    target_assignee_ids = [uid for uid in target_assignee_ids if uid]
                    if sorted(target_assignee_ids) != sorted(mapped_assignees):
                        changes["assignees"] = mapped_assignees
                        changes["assignee_ids"] = mapped_assignees

                    # 6. Compare labels
                    target_labels = target_issue_obj.get("label_ids") or target_issue_obj.get("labels") or []
                    target_label_ids = [
                        l.get("id") if isinstance(l, dict) else l
                        for l in target_labels
                    ]
                    target_label_ids = [lid for lid in target_label_ids if lid]
                    if sorted(target_label_ids) != sorted(mapped_labels):
                        changes["labels"] = mapped_labels
                        changes["label_ids"] = mapped_labels

                    if not changes:
                        print(f"        [-] ({idx}/{len(issues)}) Issue '{issue['name']}' already exists on Orca and is up to date. Skipping.")
                    else:
                        print(f"        [+] ({idx}/{len(issues)}) Issue '{issue['name']}' has changes. Updating...")
                        if target_issue_id:
                            patch_res = new_session.patch(
                                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{target_issue_id}/",
                                json=changes,
                                timeout=30
                            )
                            if patch_res.status_code in [200, 201]:
                                print(f"            [+] Successfully updated fields: {list(changes.keys())}")
                            else:
                                print(f"            [!] Failed to update fields: {patch_res.text}")

                    # Associate cycles and modules even if skipped or updated
                    if target_issue_id:
                        if mapped_cycle_id:
                            if mapped_cycle_id not in cycle_associations:
                                cycle_associations[mapped_cycle_id] = []
                            cycle_associations[mapped_cycle_id].append(target_issue_id)
                        if mapped_module_ids:
                            for mod_id in mapped_module_ids:
                                if mod_id not in module_associations:
                                    module_associations[mod_id] = []
                                module_associations[mod_id].append(target_issue_id)
                    continue

                max_retries = 5
                retry_delay = 2
                for attempt in range(max_retries):
                    if is_intake_issue:
                        intake_payload = {
                            "issue": {
                                "name": issue["name"],
                                "description_html": old_desc,
                                "priority": issue.get("priority", "none"),
                            }
                        }
                        create_issue_res = new_session.post(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/intake-issues/",
                            json=intake_payload,
                            timeout=30
                        )
                    else:
                        create_issue_res = new_session.post(
                            f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/",
                            json=new_issue_payload,
                            timeout=30
                        )
                    
                    if create_issue_res.status_code in [200, 201]:
                        target_data = create_issue_res.json()
                        if is_intake_issue:
                            new_issue_id = (target_data.get("issue_detail", {}) or {}).get("id") or target_data.get("issue")
                            
                            # 1. Update IntakeIssue status/snoozed_till via the correct PATCH URL
                            # The endpoint uses issue_id (not the intake record ID) in the URL.
                            old_oi = old_intake_issue_map[old_issue_id]
                            intake_patch_payload = {
                                "status": old_oi.get("status", -2),
                                "snoozed_till": old_oi.get("snoozed_till"),
                            }
                            patch_res = new_session.patch(
                                f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/intake-issues/{new_issue_id}/",
                                json=intake_patch_payload,
                                timeout=30
                            )
                            if patch_res.status_code not in [200, 201]:
                                print(f"        [!] Failed to sync intake status for '{issue['name']}': {patch_res.text}")

                            # 2. Patch newly created Issue to apply assignees, labels, state, estimate points.
                            # IMPORTANT: Skip this for accepted intakes (status=1) because the intake PATCH
                            # above already transitions state from TRIAGE → default. If we patch the issue
                            # state again here it would reset it back to TRIAGE (the old mapped state),
                            # making the intake appear as "pending" in the UI.
                            old_intake_status = old_oi.get("status", -2)
                            if old_intake_status != 1:
                                new_session.patch(
                                    f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{new_issue_id}/",
                                    json=new_issue_payload,
                                    timeout=30
                                )
                        else:
                            new_issue_id = target_data.get("id")
                        
                        print(f"        [+] ({idx}/{len(issues)}) Imported issue: {issue['name']}")
                        stats["issues_migrated"] += 1

                        # Migrate Comments for this issue
                        try:
                            comments_res = old_session.get(
                                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/{issue['id']}/comments/",
                                timeout=30
                            )
                            if comments_res.status_code == 200:
                                comments = get_list_from_response(comments_res.json())
                                for comment in comments:
                                    comment_payload = {
                                        "comment_html": comment.get("comment_html", ""),
                                        "comment_json": comment.get("comment_json", {}),
                                        "comment_stripped": comment.get("comment_stripped", ""),
                                    }
                                    actor_id = comment.get("actor") or comment.get("commented_by") or comment.get("created_by")
                                    mapped_actor = map_user_id(actor_id)
                                    if mapped_actor:
                                        comment_payload["actor"] = mapped_actor
                                        comment_payload["commented_by"] = mapped_actor
                                        comment_payload["created_by"] = mapped_actor
                                    
                                    new_session.post(
                                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{new_issue_id}/comments/",
                                        json=comment_payload,
                                        timeout=30
                                    )
                        except Exception as e:
                            print(f"        [!] Failed to sync comments for issue '{issue['name']}': {e}")

                        # Migrate Links for this issue
                        try:
                            links_res = old_session.get(
                                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/{issue['id']}/links/",
                                timeout=30
                            )
                            if links_res.status_code == 200:
                                links = get_list_from_response(links_res.json())
                                for link in links:
                                    link_payload = {
                                        "title": link.get("title", ""),
                                        "url": link.get("url", ""),
                                        "metadata": link.get("metadata", {}),
                                    }
                                    old_link_creator = link.get("created_by")
                                    if isinstance(old_link_creator, dict):
                                        old_link_creator = old_link_creator.get("id")
                                    mapped_link_creator = map_user_id(old_link_creator)
                                    if mapped_link_creator:
                                        link_payload["created_by"] = mapped_link_creator
                                    new_session.post(
                                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{new_issue_id}/links/",
                                        json=link_payload,
                                        timeout=30
                                    )
                        except Exception as e:
                            print(f"        [!] Failed to sync links for issue '{issue['name']}': {e}")

                        # Migrate Attachments for this issue
                        try:
                            attachments_res = old_session.get(
                                f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/{issue['id']}/issue-attachments/",
                                timeout=30
                            )
                            if attachments_res.status_code == 200:
                                attachments = get_list_from_response(attachments_res.json())
                                for att in attachments:
                                    att_id = att.get("id")
                                    if not att_id:
                                        continue

                                    file_name = att.get("attributes", {}).get("name", "attachment")
                                    file_type = att.get("attributes", {}).get("type", "application/octet-stream")
                                    file_size = int(att.get("attributes", {}).get("size", 1024))

                                    # Step 1: Create attachment record on the TARGET issue.
                                    # This endpoint (POST /issue-attachments/) creates a FileAsset with
                                    # issue_id set correctly and returns a presigned S3 upload URL.
                                    create_att_res = new_session.post(
                                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{new_issue_id}/issue-attachments/",
                                        json={"name": file_name, "type": file_type, "size": file_size},
                                        timeout=30
                                    )
                                    if create_att_res.status_code not in [200, 201]:
                                        print(f"          [!] Failed to create attachment slot for '{file_name}': {create_att_res.text}")
                                        continue

                                    att_info = create_att_res.json()
                                    upload_data = att_info.get("upload_data", {})
                                    target_asset_id = att_info.get("asset_id")
                                    upload_url = upload_data.get("url")
                                    upload_fields = upload_data.get("fields", {})

                                    if not upload_url or not target_asset_id:
                                        print(f"          [!] No upload URL returned for '{file_name}', skipping.")
                                        continue

                                    # Step 2: Download the binary from the SOURCE server.
                                    # The Plane API redirect endpoint returns a 302 to a presigned S3 URL.
                                    # We must NOT follow the redirect with auth headers (S3 presigned URLs
                                    # reject requests that carry an Authorization header). Instead:
                                    # a) get the redirect location without following it,
                                    # b) then fetch the binary from S3 without any auth headers.
                                    download_url = f"{OLD_PLANE_URL}/api/v1/workspaces/{OLD_WORKSPACE_SLUG}/projects/{proj['id']}/issues/{issue['id']}/issue-attachments/{att_id}/"
                                    redir_res = old_session.get(download_url, timeout=30, allow_redirects=False)
                                    if redir_res.status_code in [301, 302, 303, 307, 308]:
                                        # Follow the redirect manually without auth headers
                                        s3_download_url = redir_res.headers.get("Location")
                                        file_res = requests.get(s3_download_url, timeout=60)
                                    elif redir_res.status_code == 200:
                                        # Direct response (e.g. local storage returns file directly)
                                        file_res = redir_res
                                    else:
                                        print(f"          [!] Failed to get download URL for '{file_name}': HTTP {redir_res.status_code}")
                                        continue
                                    if file_res.status_code not in [200, 206]:
                                        print(f"          [!] Failed to download source attachment '{file_name}': HTTP {file_res.status_code}")
                                        continue

                                    # Step 3: POST binary to the presigned target S3/MinIO URL (unauthenticated).
                                    multipart_fields = dict(upload_fields)
                                    multipart_files = {"file": (file_name, file_res.content, file_type)}
                                    s3_res = requests.post(upload_url, data=multipart_fields, files=multipart_files, timeout=60)
                                    if s3_res.status_code not in [200, 201, 204]:
                                        print(f"          [!] S3 upload failed for '{file_name}': HTTP {s3_res.status_code}")
                                        continue

                                    # Step 4: Confirm upload is complete via PATCH.
                                    confirm_res = new_session.patch(
                                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/issues/{new_issue_id}/issue-attachments/{target_asset_id}/",
                                        json={"is_uploaded": True},
                                        timeout=30
                                    )
                                    if confirm_res.status_code == 204:
                                        print(f"          [+] Attachment synced: {file_name}")
                                    else:
                                        print(f"          [!] Failed to confirm upload for '{file_name}': {confirm_res.text}")
                        except Exception as e:
                            print(f"        [!] Failed to sync attachments for issue '{issue['name']}': {e}")



                        if mapped_cycle_id:
                            if mapped_cycle_id not in cycle_associations:
                                cycle_associations[mapped_cycle_id] = []
                            cycle_associations[mapped_cycle_id].append(new_issue_id)

                        if mapped_module_ids:
                            for mod_id in mapped_module_ids:
                                if mod_id not in module_associations:
                                    module_associations[mod_id] = []
                                module_associations[mod_id].append(new_issue_id)
                        break
                    elif create_issue_res.status_code == 429 or "RATE_LIMIT_EXCEEDED" in create_issue_res.text:
                        print(f"        [!] Rate limit hit. Waiting {retry_delay}s (Attempt {attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        err_msg = f"Failed to import issue '{issue['name']}' in project '{proj_name}': {create_issue_res.text}"
                        stats["issues_failed"] += 1
                        stats["errors"].append(err_msg)
                        print(f"        [-] {err_msg}")
                        break
                else:
                    err_msg = f"Exceeded maximum retries for issue '{issue['name']}' in project '{proj_name}'"
                    stats["issues_failed"] += 1
                    stats["errors"].append(err_msg)
 
            # Bulk associate issues to cycles
            if cycle_associations:
                print("    [+] Linking work items to cycles in bulk...")
                for cycle_id, issue_ids in cycle_associations.items():
                    c_res = new_session.post(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/cycles/{cycle_id}/cycle-issues/",
                        json={"issues": issue_ids},
                        timeout=30
                    )
                    if c_res.status_code in [200, 201]:
                        print(f"        [+] Linked {len(issue_ids)} work items to cycle '{cycle_id_to_name.get(cycle_id, cycle_id)}' in bulk.")
                    else:
                        print(f"        [-] Failed to bulk associate issues to cycle {cycle_id}: {c_res.text}")

            # Bulk associate issues to modules
            if module_associations:
                print("    [+] Linking work items to modules in bulk...")
                for mod_id, issue_ids in module_associations.items():
                    m_res = new_session.post(
                        f"{NEW_PLANE_URL}/api/v1/workspaces/{NEW_WORKSPACE_SLUG}/projects/{new_proj_id}/modules/{mod_id}/module-issues/",
                        json={"issues": issue_ids},
                        timeout=30
                    )
                    if m_res.status_code in [200, 201]:
                        print(f"        [+] Linked {len(issue_ids)} work items to module '{module_id_to_name.get(mod_id, mod_id)}' in bulk.")
                    else:
                        print(f"        [-] Failed to bulk associate issues to module {mod_id}: {m_res.text}")

        except Exception as e:
            stats["errors"].append(f"Error migrating issues for project {proj_name}: {e}")
            print(f"    [-] Error migrating issues for project {proj_name}: {e}")

    # Output Migration Summary Report
    print("\n" + "="*50)
    print("MIGRATION PROCESS COMPLETED - SUMMARY REPORT")
    print("="*50)
    print(f"Projects migrated:             {stats['projects_migrated']}")
    print(f"Workspace members invited:     {stats['workspace_members_invited']} (Failed: {stats['workspace_members_failed']})")
    print(f"Project states synced:         {stats['states_migrated']} (Failed: {stats['states_failed']})") 
    print(f"Project labels synced:         {stats['labels_migrated']} (Failed: {stats['labels_failed']})")
    print(f"Project cycles synced:         {stats['cycles_migrated']} (Failed: {stats['cycles_failed']})")
    print(f"Project modules synced:        {stats['modules_migrated']} (Failed: {stats['modules_failed']})")
    print(f"Issues / Work items imported:  {stats['issues_migrated']} (Failed: {stats['issues_failed']})")
    print("="*50)
    
    if stats["errors"]:
        print(f"\n[!] Warnings/Errors encountered during migration ({len(stats['errors'])}):")
        for err in stats["errors"][:15]:  # Show first 15 errors to keep screen clean
            print(f"  - {err}")
        if len(stats["errors"]) > 15:
            print(f"  ... and {len(stats['errors']) - 15} more. Review logs above.")
    else:
        print("\n[+] Migration completed successfully with zero errors!")
    print("="*50 + "\n")


if __name__ == "__main__":
    migrate()
