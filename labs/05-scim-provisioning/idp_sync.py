#!/usr/bin/env python3
"""The identity provider side of provisioning: push an HR feed to an app over SCIM.

Reads the workers who should have an account, compares them with the accounts
the application actually has, and creates, updates, reactivates or deactivates
to make the two match. Safe to run repeatedly.
"""
import argparse
import csv
import json
import sys
import urllib.error
import urllib.request

USER_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:User"
ENTERPRISE = "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
PATCH_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:PatchOp"


class Scim:
    def __init__(self, base_url, token):
        self.base_url, self.token = base_url, token

    def call(self, method, path, body=None):
        request = urllib.request.Request(
            self.base_url + path,
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/scim+json"},
        )
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read() or b"{}")
        except urllib.error.HTTPError as e:
            detail = json.loads(e.read() or b"{}").get("detail", "")
            sys.exit(f"SCIM {method} {path} failed: HTTP {e.code} {detail}")
        except urllib.error.URLError as e:
            sys.exit(f"Cannot reach the SCIM server at {self.base_url}: {e.reason}")


def to_scim(worker):
    """Map an HR record to the SCIM user the application should hold."""
    given, _, family = worker["name"].partition(" ")
    return {
        "schemas": [USER_SCHEMA, ENTERPRISE],
        "externalId": worker["id"],  # the worker ID is the matching key, never the email
        "userName": worker["email"],
        "name": {"givenName": given, "familyName": family},
        ENTERPRISE: {"department": worker["department"]},
        "active": True,
    }


def build_plan(feed, existing):
    """Compare desired state (the feed) with actual state (the app)."""
    by_external_id = {u.get("externalId"): u for u in existing}
    plan = []
    for worker in feed:
        desired = to_scim(worker)
        current = by_external_id.get(worker["id"])
        if current is None:
            plan.append(("CREATE", desired, None))
        elif not current.get("active", True):
            plan.append(("REACTIVATE", desired, current))
        elif any(current.get(k) != desired[k] for k in ("userName", "name", ENTERPRISE)):
            plan.append(("UPDATE", desired, current))
    wanted = {w["id"] for w in feed}
    for user in existing:
        if user.get("active", True) and user.get("externalId") not in wanted:
            plan.append(("DEACTIVATE", None, user))
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("feed", help="CSV of workers who should have an account")
    parser.add_argument("--dry-run", action="store_true", help="show the plan, change nothing")
    parser.add_argument("--max-deactivate-pct", type=int, default=50,
                        help="refuse to run if more than this share of active accounts would be deactivated")
    parser.add_argument("--url", default="http://127.0.0.1:8081/scim/v2")
    parser.add_argument("--token", default="lab-token")
    args = parser.parse_args()

    with open(args.feed, newline="") as f:
        feed = list(csv.DictReader(f))
    scim = Scim(args.url, args.token)
    existing = scim.call("GET", "/Users")["Resources"]
    plan = build_plan(feed, existing)

    if not plan:
        print("In sync: nothing to do")
        return
    for action, desired, current in plan:
        print(f"{action:<10} {(desired or current)['userName']}")

    # Safety guard: a truncated or empty HR feed must not be read as "everyone left".
    active = sum(1 for u in existing if u.get("active", True))
    deactivations = sum(1 for action, _, _ in plan if action == "DEACTIVATE")
    if active and deactivations * 100 > active * args.max_deactivate_pct:
        sys.exit(f"HALTED: this run would deactivate {deactivations} of {active} active accounts, "
                 f"above the {args.max_deactivate_pct}% limit. Check the feed.")

    if args.dry_run:
        print("Dry run: no changes made")
        return

    failed = 0
    for action, desired, current in plan:
        if action == "CREATE":
            scim.call("POST", "/Users", desired)
        elif action in ("UPDATE", "REACTIVATE"):
            scim.call("PUT", f"/Users/{current['id']}", desired)
        else:
            result = scim.call("PATCH", f"/Users/{current['id']}", {
                "schemas": [PATCH_SCHEMA],
                "Operations": [{"op": "replace", "path": "active", "value": False}],
            })
            # Trust, but verify: a 200 response is not proof the account is disabled.
            if result.get("active", True):
                failed += 1
                print(f"FAILED     {current['userName']}: the app answered 200 but the account is still active")
    print(f"Applied {len(plan) - failed} of {len(plan)} changes")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
