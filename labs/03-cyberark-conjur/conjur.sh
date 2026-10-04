# Helper functions for the Conjur REST API. Load with: source conjur.sh

CONJUR_URL="${CONJUR_URL:-http://localhost:8080}"
CONJUR_ACCOUNT="${CONJUR_ACCOUNT:-lab}"

# Identities and variable names contain "/" and "@", which must be encoded in a URL path.
_conjur_encode() {
  printf '%s' "$1" | jq -sRr @uri
}

# conjur_login <identity> <api-key>
# Exchanges the long-lived API key for an access token that expires in a few minutes.
conjur_login() {
  local token
  token=$(curl -sS --fail -X POST \
    -H "Accept-Encoding: base64" \
    --data "$2" \
    "$CONJUR_URL/authn/$CONJUR_ACCOUNT/$(_conjur_encode "$1")/authenticate") || {
      echo "Login failed for $1" >&2
      return 1
    }
  CONJUR_TOKEN="$token"
  echo "Logged in as $1"
}

_conjur_auth() {
  printf 'Authorization: Token token="%s"' "$CONJUR_TOKEN"
}

# conjur_policy <file>
conjur_policy() {
  curl -sS -X POST -H "$(_conjur_auth)" \
    --data-binary "@$1" \
    "$CONJUR_URL/policies/$CONJUR_ACCOUNT/policy/root"
  echo
}

# conjur_set <variable> <value>
conjur_set() {
  curl -sS -o /dev/null -w "HTTP %{http_code}\n" -X POST -H "$(_conjur_auth)" \
    --data "$2" \
    "$CONJUR_URL/secrets/$CONJUR_ACCOUNT/variable/$(_conjur_encode "$1")"
}

# conjur_get <variable>
conjur_get() {
  curl -sS -w "\nHTTP %{http_code}\n" -H "$(_conjur_auth)" \
    "$CONJUR_URL/secrets/$CONJUR_ACCOUNT/variable/$(_conjur_encode "$1")"
}
