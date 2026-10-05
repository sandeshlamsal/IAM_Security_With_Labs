# Lab 06. Active Directory troubleshooting

**Status: work in progress. Not yet working end to end.**

## Goal

Run an Active Directory-compatible domain controller locally (Samba, in Docker) and practise the diagnosis an IAM systems engineer does: DNS, Kerberos, LDAP, certificates, service accounts, lockouts and nested groups.

## What is here so far

| File | Purpose |
|---|---|
| `Dockerfile` | Builds a Samba domain controller image with Kerberos, LDAP and DNS tools |
| `docker-compose.yml` | Runs it as `dc1.lab.example.com` |
| `entrypoint.sh` | Provisions the domain on first start |
| `seed.sh` | Creates users, groups (including nested ones) and service accounts |
| `scenario.sh` | Introduces six faults to diagnose, and resets them |

## What has and has not been tested

- The image builds.
- The first run failed at domain provisioning because a package was missing. That package (`samba-ad-provision`) has since been added to the `Dockerfile`, and the fix has **not** been re-tested.
- `seed.sh`, `scenario.sh` and every exercise are untested.

Do not rely on this lab until this notice is removed. The step-by-step exercises will be written once the container is confirmed working.

Until then, the reference material for this topic is the cheat sheet in the [IAM systems engineer interview guide](../../interview/08-iam-systems-engineer-interview.md).
