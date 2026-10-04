#!/usr/bin/env python3
"""A minimal SCIM 2.0 server: the application (vendor) side of provisioning.

Users are held in memory and lost when the server stops. Lab use only.

Environment variables:
  SCIM_TOKEN          bearer token clients must send (default: lab-token)
  SCIM_NO_DEACTIVATE  set to 1 to imitate a vendor that accepts a deactivate
                      request, answers 200, and leaves the user active
"""
import json
import os
import re
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST, PORT = "127.0.0.1", 8081
BASE = "/scim/v2"
TOKEN = os.environ.get("SCIM_TOKEN", "lab-token")
NO_DEACTIVATE = os.environ.get("SCIM_NO_DEACTIVATE") == "1"

USER_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:User"
LIST_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:ListResponse"
ERROR_SCHEMA = "urn:ietf:params:scim:api:messages:2.0:Error"

users = {}  # id -> SCIM user resource


class ScimHandler(BaseHTTPRequestHandler):
    def send_json(self, status, body=None):
        payload = json.dumps(body).encode() if body is not None else b""
        self.send_response(status)
        self.send_header("Content-Type", "application/scim+json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def send_error_json(self, status, detail):
        self.send_json(status, {"schemas": [ERROR_SCHEMA], "status": str(status), "detail": detail})

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def route(self):
        """Check the bearer token, then return (path under BASE, query) or None."""
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self.send_error_json(401, "Missing or wrong bearer token")
            return None
        url = urlparse(self.path)
        if not url.path.startswith(BASE):
            self.send_error_json(404, "Not a SCIM path")
            return None
        return url.path[len(BASE):], parse_qs(url.query)

    def find_user(self, path):
        user = users.get(path.rsplit("/", 1)[-1])
        if user is None:
            self.send_error_json(404, "User not found")
        return user

    def do_GET(self):
        routed = self.route()
        if routed is None:
            return
        path, query = routed
        if path == "/ServiceProviderConfig":
            self.send_json(200, {"patch": {"supported": True}, "filter": {"supported": True}})
        elif path == "/Users":
            found = list(users.values())
            # Only the filter identity providers rely on: userName eq "value"
            match = re.fullmatch(r'userName eq "(.*)"', query.get("filter", [""])[0])
            if match:
                found = [u for u in found if u["userName"] == match.group(1)]
            self.send_json(200, {"schemas": [LIST_SCHEMA], "totalResults": len(found), "Resources": found})
        elif path.startswith("/Users/"):
            user = self.find_user(path)
            if user:
                self.send_json(200, user)
        else:
            self.send_error_json(404, "Unknown endpoint")

    def do_POST(self):
        routed = self.route()
        if routed is None:
            return
        if routed[0] != "/Users":
            return self.send_error_json(404, "Unknown endpoint")
        body = self.read_json()
        if any(u["userName"] == body.get("userName") for u in users.values()):
            return self.send_error_json(409, "userName already exists")
        user = {**body, "schemas": [USER_SCHEMA], "id": uuid.uuid4().hex[:8]}
        user.setdefault("active", True)
        users[user["id"]] = user
        self.send_json(201, user)

    def do_PUT(self):
        routed = self.route()
        if routed is None:
            return
        user = self.find_user(routed[0])
        if user:
            replacement = {**self.read_json(), "schemas": [USER_SCHEMA], "id": user["id"]}
            users[user["id"]] = replacement
            self.send_json(200, replacement)

    def do_PATCH(self):
        routed = self.route()
        if routed is None:
            return
        user = self.find_user(routed[0])
        if not user:
            return
        for op in self.read_json().get("Operations", []):
            if op.get("op", "").lower() != "replace":
                return self.send_error_json(400, "Only the replace operation is supported")
            changes = {op["path"]: op["value"]} if "path" in op else op["value"]
            if NO_DEACTIVATE and changes.get("active") is False:
                del changes["active"]
            user.update(changes)
        self.send_json(200, user)

    def do_DELETE(self):
        routed = self.route()
        if routed is None:
            return
        user = self.find_user(routed[0])
        if user:
            del users[user["id"]]
            self.send_json(204)


if __name__ == "__main__":
    mode = " (deactivate requests are ignored)" if NO_DEACTIVATE else ""
    print(f"SCIM server on http://{HOST}:{PORT}{BASE}{mode}. Stop with Ctrl+C.")
    HTTPServer((HOST, PORT), ScimHandler).serve_forever()
