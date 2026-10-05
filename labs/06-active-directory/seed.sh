#!/bin/bash
# Create the users, groups and service accounts the exercises use.
set -e
P="$LAB_PASSWORD"

samba-tool domain passwordsettings set --complexity=on --min-pwd-age=0 --max-pwd-age=0 \
    --account-lockout-threshold=3 --account-lockout-duration=30 --reset-account-lockout-after=30

for u in priya:Priya:Shah:Finance tom:Tom:Lee:Engineering asha:Asha:Rao:Procurement lena:Lena:Park:Finance; do
    IFS=: read -r sam given sur dept <<<"$u"
    samba-tool user create "$sam" "$P" --given-name="$given" --surname="$sur" --department="$dept"
done

# Service accounts
samba-tool user create svc-web "$P" --description="Runs the intranet web application"
samba-tool user create svc-scan "$P" --description="Read-only account used by the scanning product"
samba-tool user create svc-old "$P" --description="Purpose unknown"

# Groups, with nesting: Finance-Readers is a member of App-Finance
samba-tool group add Finance-Readers
samba-tool group add App-Finance
samba-tool group addmembers Finance-Readers priya,lena
samba-tool group addmembers App-Finance Finance-Readers,tom

# A privileged account hidden behind a nested group
samba-tool group add Server-Operators-Custom
samba-tool group addmembers "Domain Admins" Server-Operators-Custom
samba-tool group addmembers Server-Operators-Custom svc-old

samba-tool user setexpiry svc-old --noexpiry
