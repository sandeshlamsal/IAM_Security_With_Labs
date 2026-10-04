# Labs

Hands-on practice for the [concept chapters](../README.md#learning-path). Each lab is small, uses copy-and-paste commands and ends with a clean-up step.

## Labs available now

| # | Lab | Platform | Chapters | Cost | Time |
|---|---|---|---|---|---|
| 00 | [Setup](00-setup/README.md) | Your laptop | -- | Free | 30 min |
| 01 | [AWS IAM: policies, roles and AssumeRole](01-aws-iam/README.md) | AWS | 10 | Free (IAM and STS are free; a few KB in S3) | 45 min |
| 02 | [AKS identity: Entra ID, Kubernetes RBAC, workload identity](02-aks-identity/README.md) | Azure | 04, 08, 10 | **Paid:** one small VM while the cluster exists | 60 min |
| 03 | [CyberArk Conjur: secrets under policy](03-cyberark-conjur/README.md) | Docker (local) | 06, 08, 09 | Free | 45 min |
| 04 | [SailPoint-style IGA: joiner, mover, leaver, SoD, certification](04-sailpoint-iga/README.md) | Python (local) | 05 | Free | 45 min |

Do them in order. Lab 04 needs nothing but Python, so start there if you have no cloud account yet.

## About CyberArk and SailPoint

Both are commercial products with no free self-service edition, so these labs use the closest thing you can run yourself:

- **CyberArk:** lab 03 uses **Conjur Open Source**, CyberArk's own secrets manager. It teaches the policy, least-privilege and machine-identity ideas. The lab's README also maps what you learn to CyberArk PAM (Vault, Safes, CPM, PSM).
- **SailPoint:** lab 04 is a small IGA engine you run locally. It uses SailPoint's vocabulary (source, aggregation, identity, access profile, role, SoD policy, certification) so the concepts transfer directly. The README shows the equivalent API calls for when you have access to a real tenant.

## Labs by job role

| Role | What the job involves | Labs |
|---|---|---|
| **IAM Analyst** | Access requests, access reviews, onboarding and offboarding, audit evidence | 04 |
| **IGA Engineer** (SailPoint, Saviynt) | Lifecycle automation, sources, roles, SoD, certifications | 04 |
| **PAM Engineer** (CyberArk, BeyondTrust) | Vaulting, rotation, least privilege for machines and admins | 03 |
| **Cloud IAM Engineer** | Cloud policies, roles, guardrails, workload identity | 01, 02 |
| **Platform / Kubernetes security** | Cluster access, RBAC, pod identity | 02, 03 |
| **IAM Architect** | How the pieces fit; trade-offs and resilience | All, plus write a one-page design after each |

## Lab format

1. **Goal** in one sentence
2. **Picture** of what you are building
3. **Steps**, each with the expected result
4. **Break it:** misconfigure something on purpose and read the error
5. **What you proved:** how to describe it at work or in an interview
6. **Clean up**

## Coming next

| Lab | Tool |
|---|---|
| OIDC and SAML login end to end | Keycloak |
| Policy as code | Open Policy Agent |
| Dynamic database credentials | HashiCorp Vault |
| Build a small PKI and mTLS | OpenSSL / step-ca |
| Keyless CI/CD from GitHub Actions to AWS | GitHub OIDC |
| Entra ID conditional access and PIM | Entra ID |
| Cross-cloud: AKS workload reaching AWS with no stored keys | AKS + AWS STS |

## Safety and cost rules

- Never use the AWS root user or a production account for labs.
- Set a budget alert before creating anything (see lab 00).
- Run the clean-up step the same day. Lab 02 costs money for as long as the cluster exists.
- Never commit credentials. The `.gitignore` in this repo excludes the files the labs generate.
