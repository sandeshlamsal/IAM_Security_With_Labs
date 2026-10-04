#!/usr/bin/env python3
"""A tiny identity governance engine for learning IGA concepts.

It keeps identities and their access in state.json and mimics what a product
such as SailPoint does: aggregate an HR source, apply birthright roles, take
access requests, enforce separation-of-duties policies, run a certification
and reconcile against a target application.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
STATE_FILE = HERE / "state.json"
CONFIG = json.loads((HERE / "config.json").read_text())


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"identities": {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def birthright_for(department):
    """Access everyone gets, plus access everyone in this department gets."""
    roles = CONFIG["birthright"]
    return set(roles.get("*", [])) | set(roles.get(department, []))


def sod_violations(entitlements):
    """Return the SoD policies broken by holding this set of entitlements."""
    return [
        p for p in CONFIG["sod_policies"]
        if p["left"] in entitlements and p["right"] in entitlements
    ]


def get_identity(state, identity_id):
    identity = state["identities"].get(identity_id)
    if identity is None:
        sys.exit(f"No identity with id {identity_id}")
    return identity


def cmd_aggregate(args):
    """Read the HR feed and work out who joined, moved or left."""
    state = load_state()
    identities = state["identities"]
    with open(args.feed, newline="") as f:
        feed = {row["id"]: row for row in csv.DictReader(f)}

    for identity_id, row in feed.items():
        current = identities.get(identity_id)
        if current is None or current["status"] == "inactive":
            access = {e: "birthright" for e in birthright_for(row["department"])}
            identities[identity_id] = {**row, "status": "active", "access": access}
            print(f"JOINER  {identity_id} {row['name']}: {row['department']}")
            for e in sorted(access):
                print(f"          + {e} (birthright)")
        elif current["department"] != row["department"]:
            old, new = current["department"], row["department"]
            print(f"MOVER   {identity_id} {row['name']}: {old} -> {new}")
            access = current["access"]
            keep = birthright_for(new)
            for e in sorted(e for e, src in access.items() if src == "birthright" and e not in keep):
                del access[e]
                print(f"          - {e} (old birthright removed)")
            for e in sorted(keep - set(access)):
                access[e] = "birthright"
                print(f"          + {e} (birthright)")
            for e in sorted(e for e, src in access.items() if src == "requested"):
                print(f"          ? {e} (requested earlier, kept: needs review)")
            current.update({k: row[k] for k in ("name", "department", "manager", "type")})

    # Anyone we know about who is missing from the feed has left.
    for identity_id, current in identities.items():
        if identity_id not in feed and current["status"] == "active":
            print(f"LEAVER  {identity_id} {current['name']}")
            for e in sorted(current["access"]):
                print(f"          - {e}")
            current["status"] = "inactive"
            current["access"] = {}

    save_state(state)


def cmd_show(args):
    for identity_id, i in sorted(load_state()["identities"].items()):
        print(f"{identity_id} {i['name']:<12} {i['type']:<10} {i['department']:<12} {i['status']}")
        for e, src in sorted(i["access"].items()):
            print(f"      {e} ({src})")


def cmd_request(args):
    """Access request with a preventive SoD check."""
    state = load_state()
    identity = get_identity(state, args.identity)
    if identity["status"] != "active":
        sys.exit(f"DENIED  {args.identity} is not active")
    broken = sod_violations(set(identity["access"]) | {args.entitlement})
    if broken:
        for p in broken:
            print(f"BLOCKED by SoD policy '{p['name']}': {p['left']} + {p['right']}")
        sys.exit(1)
    identity["access"][args.entitlement] = "requested"
    save_state(state)
    print(f"GRANTED {args.entitlement} to {args.identity} {identity['name']} (approved by manager {identity['manager']})")


def cmd_sod(args):
    """Detective SoD scan: find violations that already exist."""
    found = False
    for identity_id, i in sorted(load_state()["identities"].items()):
        for p in sod_violations(set(i["access"])):
            found = True
            print(f"VIOLATION {identity_id} {i['name']}: '{p['name']}' ({p['left']} + {p['right']})")
    if not found:
        print("No SoD violations")


def cmd_certify(args):
    """Certification campaign: list access for review, or record a revoke decision."""
    state = load_state()
    if args.revoke:
        identity_id, entitlement = args.revoke
        identity = get_identity(state, identity_id)
        if entitlement not in identity["access"]:
            sys.exit(f"{identity_id} does not hold {entitlement}")
        del identity["access"][entitlement]
        save_state(state)
        print(f"REVOKED {entitlement} from {identity_id} {identity['name']}")
        return
    print("Certification campaign: requested (non-birthright) access to review")
    for identity_id, i in sorted(state["identities"].items()):
        for e, src in sorted(i["access"].items()):
            if src == "requested":
                flag = "  <-- SoD violation" if sod_violations(set(i["access"])) else ""
                print(f"  reviewer {i['manager']}: {identity_id} {i['name']} ({i['department']}) holds {e}{flag}")


def cmd_reconcile(args):
    """Compare what the application really has with what the IGA engine expects."""
    identities = load_state()["identities"]
    app = args.app
    with open(args.accounts, newline="") as f:
        for row in csv.DictReader(f):
            entitlement = f"{app}:{row['entitlement']}"
            owner = identities.get(row["identity_id"])
            if owner is None:
                print(f"ORPHAN        {row['account']}: no owning identity, holds {entitlement}")
            elif owner["status"] != "active":
                print(f"LEAVER ACTIVE {row['account']}: owner {row['identity_id']} has left, still holds {entitlement}")
            elif entitlement not in owner["access"]:
                print(f"OUT OF BAND   {row['account']}: holds {entitlement}, never granted through IGA")
            else:
                print(f"ok            {row['account']}: {entitlement}")


def cmd_reset(args):
    STATE_FILE.unlink(missing_ok=True)
    print("State cleared")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("aggregate", help="load an HR feed and process joiners, movers, leavers")
    p.add_argument("feed")
    p.set_defaults(func=cmd_aggregate)

    p = sub.add_parser("show", help="list identities and their access")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("request", help="request an entitlement for an identity")
    p.add_argument("identity")
    p.add_argument("entitlement")
    p.set_defaults(func=cmd_request)

    p = sub.add_parser("sod", help="scan for separation-of-duties violations")
    p.set_defaults(func=cmd_sod)

    p = sub.add_parser("certify", help="run an access review")
    p.add_argument("--revoke", nargs=2, metavar=("IDENTITY", "ENTITLEMENT"))
    p.set_defaults(func=cmd_certify)

    p = sub.add_parser("reconcile", help="compare an application's accounts with expected access")
    p.add_argument("app")
    p.add_argument("accounts")
    p.set_defaults(func=cmd_reconcile)

    p = sub.add_parser("reset", help="delete state.json")
    p.set_defaults(func=cmd_reset)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
