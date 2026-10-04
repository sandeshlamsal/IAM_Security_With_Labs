# 05. Identity governance and administration (IGA)

## In one sentence

IGA manages the full life of access: how it is requested, approved, granted, reviewed and removed, with evidence that each step happened.

## Everyday analogy

A gym membership desk. Someone signs you up, decides which classes your plan includes, checks every year that you still want it, and cancels your card when you leave. Without the desk, old cards would work forever.

## Baby steps

### Step 1. Why governance exists

Authentication and authorization answer "can Priya do this *now*?" Governance answers:

- **Should** she have this access at all?
- Who approved it, and when?
- Does she still need it?
- Was it removed when she left?

Auditors ask exactly these questions.

### Step 2. HR is the source of truth

Automated lifecycle starts from the HR system.

```mermaid
flowchart LR
    HR["HR system<br/>(Workday, SAP)"] -->|"hire / move / leave event"| IGA["IGA platform<br/>(SailPoint, Saviynt,<br/>Entra ID Governance)"]
    IGA -->|create account| AD["Active Directory"]
    IGA -->|create account| APP1["Email"]
    IGA -->|assign role| APP2["Finance app"]
```

### Step 3. Joiner, mover, leaver in detail

```mermaid
flowchart TD
    J["<b>Joiner</b><br/>HR creates the record"] --> J2["Accounts created automatically.<br/><b>Birthright access</b> given<br/>(email, intranet, team tools)"]
    J2 --> M["<b>Mover</b><br/>changes department"]
    M --> M2["New role's access added.<br/><b>Old access removed.</b>"]
    M2 --> L["<b>Leaver</b><br/>last working day"]
    L --> L2["Accounts disabled the same day.<br/>Deleted after a retention period."]
```

- **Birthright access:** what everyone in a role gets automatically on day one.
- The mover step is where things go wrong. If old access is not removed, people accumulate permissions over the years. This is **privilege creep**.

### Step 4. Access requests

For anything beyond birthright, the user asks.

```mermaid
sequenceDiagram
    participant U as User
    participant IGA as IGA portal
    participant M as Manager
    participant O as App owner
    U->>IGA: Request "Finance app: approver"
    IGA->>IGA: SoD check: any conflict with existing access?
    IGA->>M: Approve?
    M->>IGA: Yes
    IGA->>O: Approve?
    O->>IGA: Yes
    IGA->>U: Access granted and logged
```

### Step 5. Separation of duties (SoD)

Some combinations of access are **toxic** because together they let one person commit fraud.

| Access A | Access B | Why it is toxic |
|---|---|---|
| Create vendor | Approve payment | Could pay a fake vendor |
| Write code | Deploy to production | Could ship unreviewed changes |
| Request access | Approve access | Could self-approve |

The IGA tool blocks or flags requests that would create such a pair.

### Step 6. Access reviews (certifications)

Every quarter or year, managers and app owners look at a list and confirm or revoke.

```mermaid
flowchart LR
    C["Campaign starts"] --> R["Reviewer sees:<br/>Priya, Finance app, approver"]
    R -->|still needed| K["Keep"]
    R -->|not needed| X["Revoke"]
    X --> D["Access removed automatically"]
    K --> E["Decision recorded as audit evidence"]
    D --> E
```

The well-known failure is **rubber-stamping**: a manager clicking "approve all" on 400 lines without reading them.

### Step 7. Role mining and orphaned accounts

- **Role mining:** analysing who already has what to discover sensible roles.
- **Orphaned account:** an account with no known owner, usually a leaver's account that was missed. A favourite of attackers.
- **Reconciliation:** comparing what the IGA tool thinks exists with what actually exists in each app, to catch access granted behind its back.

## Key terms

| Term | Plain meaning |
|---|---|
| Entitlement | One grantable item of access |
| Access certification | A formal periodic review of who has what |
| Provisioning connector | The integration that lets the IGA tool create accounts in an app |
| Attestation | A signed-off statement that access is correct |
| SOX, PCI DSS, HIPAA | Regulations that require access controls and reviews |

## Common mistakes

- Handling joiners and leavers well and forgetting movers.
- Disabling the main account on departure but missing accounts in apps outside SSO.
- Treating access reviews as a tick-box exercise.

## Check yourself

1. What is privilege creep and which lifecycle stage causes it?
2. Give one example of a toxic combination.
3. What is an orphaned account?

<details><summary>Answers</summary>

1. Accumulating access over time because old access is not removed. Caused by the mover stage.
2. Creating a vendor and approving its payments.
3. An account with no valid owner, often left behind by a leaver.
</details>

Next: [06. Privileged access](06-privileged-access.md)
