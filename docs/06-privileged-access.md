# 06. Privileged access management (PAM)

## In one sentence

PAM protects the small number of accounts that can do the most damage, by locking up their credentials, granting their power only when needed and recording what is done with it.

## Everyday analogy

A bank's master key is not on anyone's keyring. It sits in a safe. To use it you sign it out, a camera records you, and it goes back afterwards, at which point the lock is changed.

## Baby steps

### Step 1. What makes an account "privileged"

An account is privileged if it can change security settings, read everyone's data or control other accounts.

| Privileged account | Where |
|---|---|
| Domain Admin | Active Directory |
| root | Linux |
| Local Administrator | Windows machines |
| Global Administrator | Microsoft Entra ID |
| AWS account root user | AWS |
| Database admin (`sa`, `sys`) | Databases |
| Service accounts with broad rights | Everywhere |

Attackers aim for these. A normal breach becomes a disaster at the moment a privileged account is taken.

### Step 2. The problems PAM solves

- Admin passwords written in spreadsheets or shared between a team.
- The same local admin password on every laptop.
- Admins who have full power all day, even while reading email.
- No record of who did what while logged in as `root`.

### Step 3. The four core PAM controls

```mermaid
flowchart TD
    PAM["PAM"] --> V["<b>1. Vaulting</b><br/>passwords stored in a vault,<br/>humans never know them"]
    PAM --> R["<b>2. Rotation</b><br/>password changed automatically<br/>after every use"]
    PAM --> S["<b>3. Session management</b><br/>connection goes through a proxy<br/>and is recorded"]
    PAM --> J["<b>4. Just-in-time (JIT)</b><br/>privilege granted for a short<br/>window, then removed"]
```

### Step 4. Checking out a privileged session

```mermaid
sequenceDiagram
    participant A as Admin
    participant P as PAM vault
    participant M as Approver
    participant S as Server
    A->>P: 1. Log in with own account + MFA
    A->>P: 2. Request access to prod-db-01, reason: ticket 4521
    P->>M: 3. Approve?
    M->>P: 4. Approved for 1 hour
    P->>S: 5. PAM opens the session and injects the password
    Note over A,S: Admin works through the PAM proxy.<br/>The session is recorded.<br/>Admin never sees the password.
    P->>S: 6. Hour ends: session closed, password rotated
```

### Step 5. Standing privilege versus just-in-time

| | Standing privilege | Just-in-time |
|---|---|---|
| When is the power active? | Always | Only when requested |
| If the account is phished | Attacker is admin immediately | Attacker has an ordinary account |
| Example | Permanent Domain Admin | Entra PIM: activate Global Admin for 1 hour |

The goal is **zero standing privilege (ZSP)**: nobody is an admin by default.

### Step 6. Separate admin accounts and tiering

An admin should have two accounts: `priya` for email and browsing, `priya-adm` for administration. If `priya` opens a malicious attachment, the admin credentials are not on that session.

**Tiering** takes this further: credentials for the most critical systems are never used on less trusted machines.

```mermaid
flowchart TD
    T0["<b>Tier 0</b><br/>Identity systems: domain controllers, IdP, PKI"]
    T1["<b>Tier 1</b><br/>Servers and applications"]
    T2["<b>Tier 2</b><br/>Workstations and user devices"]
    T0 --- T1 --- T2
    N["Rule: a higher-tier credential<br/>never logs in to a lower tier"] -.-> T0
```

### Step 7. Break-glass accounts

If the identity provider or MFA is down, nobody can log in to fix it. A **break-glass account** is an emergency admin account that bypasses the usual path. It has a very long password stored offline (often split between two people), is excluded from normal policies, and raises a loud alert whenever it is used.

## Key terms

| Term | Plain meaning |
|---|---|
| Vault | Secure store for privileged credentials |
| Jump host / bastion | A hardened server you must pass through to reach others |
| PAW | Privileged access workstation: a locked-down machine used only for admin work |
| LAPS | Microsoft tool that gives every machine a unique, rotated local admin password |
| Privilege escalation | An attacker going from ordinary user to admin |
| Lateral movement | An attacker hopping from machine to machine using stolen credentials |

## Products you will hear about

CyberArk, BeyondTrust, Delinea, HashiCorp Vault (secrets and dynamic credentials), Microsoft Entra PIM, AWS IAM Identity Center with temporary elevation.

## Common mistakes

- Vaulting human admin passwords and ignoring service accounts.
- Using the admin account for email and web browsing.
- Having no tested break-glass account.

## Check yourself

1. Name the four core PAM controls.
2. Why does JIT reduce the damage from phishing?
3. What is a break-glass account for?

<details><summary>Answers</summary>

1. Vaulting, rotation, session management, just-in-time access.
2. The phished account has no admin rights unless someone has activated them, and activation needs approval or MFA.
3. Emergency access when the normal login path is unavailable.
</details>

Next: [07. Customer identity](07-customer-identity.md)
