# 09. Secrets and certificates

## In one sentence

Secrets management stores and rotates credentials safely, and public key infrastructure (PKI) issues the certificates that let machines and people prove identity cryptographically.

## Everyday analogy

A secret is a house key: whoever holds a copy gets in. A certificate is a passport: it states who you are and is stamped by an authority others trust, so it can be checked without phoning anyone.

## Part A. Secrets

### Step 1. What counts as a secret

Passwords, API keys, database connection strings, tokens, private keys, encryption keys.

### Step 2. Where secrets should not be

Source code, config files in Git, container images, chat messages, wiki pages, environment files on shared drives.

### Step 3. A secrets manager

```mermaid
flowchart LR
    APP["Application"] -->|"1. authenticate<br/>(workload identity)"| V["<b>Secrets manager</b><br/>Vault, AWS Secrets Manager,<br/>Azure Key Vault"]
    V -->|"2. policy check:<br/>may this app read db/prod?"| V
    V -->|"3. return the secret"| APP
    APP -->|"4. connect"| DB["Database"]
    V -.->|"audit log of<br/>every read"| LOG["Logs"]
```

What it gives you: one encrypted store, access control on each secret, an audit trail and automatic rotation.

### Step 4. Static versus dynamic secrets

| | Static secret | Dynamic secret |
|---|---|---|
| Created | Once, by a human | On demand, by the secrets manager |
| Lifetime | Until someone rotates it | Minutes or hours |
| Shared? | Often by many apps | Unique per request |
| If leaked | Works until noticed | Expires on its own |

With dynamic secrets, Vault creates a brand-new database user for each application request and deletes it when the lease ends.

### Step 5. Rotation

Changing a secret on a schedule or after each use. Rotation limits how long a stolen secret remains useful. It only works if applications fetch the secret at run time rather than having it baked in.

## Part B. Certificates and PKI

### Step 6. Key pairs

Public key cryptography uses two mathematically linked keys.

```mermaid
flowchart LR
    PR["<b>Private key</b><br/>kept secret,<br/>used to <b>sign</b>"] --- PU["<b>Public key</b><br/>shared freely,<br/>used to <b>verify</b>"]
```

If a signature verifies with your public key, it must have been made with your private key. That is proof of identity without revealing any secret.

### Step 7. What a certificate is

A certificate binds a **public key** to a **name**, and is signed by a **certificate authority (CA)**.

| Field | Example |
|---|---|
| Subject | `www.example.com` |
| Public key | (the key) |
| Issuer | Example Issuing CA |
| Valid from / to | 1 Jan 2026 to 1 Apr 2026 |
| Signature | The CA's signature over all of the above |

### Step 8. The chain of trust

```mermaid
flowchart TD
    ROOT["<b>Root CA</b><br/>self-signed, kept offline,<br/>pre-installed in trust stores"] -->|signs| INT["<b>Intermediate CA</b><br/>online, issues day to day"]
    INT -->|signs| LEAF["<b>Leaf certificate</b><br/>www.example.com"]
```

Your browser trusts the leaf because it trusts the root and can follow the signatures down. The root stays offline so that a compromise of the intermediate can be recovered from.

### Step 9. TLS and mutual TLS

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    Note over C,S: TLS - only the server proves identity
    C->>S: Hello
    S->>C: Server certificate
    Note over C: Verify chain, name and expiry
    Note over C,S: Mutual TLS (mTLS) - the client proves identity too
    S->>C: Please send your certificate
    C->>S: Client certificate
    Note over S: Verify the client
    C->>S: Encrypted traffic
```

mTLS is common between microservices and is the basis of smart card login.

### Step 10. Certificate lifecycle

```mermaid
flowchart LR
    A["Request (CSR)"] --> B["Issue"] --> C["Deploy"] --> D["Monitor expiry"] --> E["Renew"] --> C
    D --> F["Revoke if compromised<br/>(CRL / OCSP)"]
```

The most common PKI incident is the dullest one: **a certificate expired and nobody noticed**, taking a service down. Automation (the ACME protocol, cert-manager) exists to prevent it.

### Step 11. Active Directory Certificate Services (ADCS)

ADCS is Microsoft's on-premises CA, used for smart cards, Wi-Fi and device certificates. Misconfigured **certificate templates** are a well-known route for attackers to become domain admin, so ADCS is treated as a Tier 0 system.

## Key terms

| Term | Plain meaning |
|---|---|
| KMS | Key management service: holds encryption keys, performs crypto operations |
| HSM | Hardware security module: tamper-resistant hardware that holds keys |
| CSR | Certificate signing request |
| CRL / OCSP | Ways to check whether a certificate has been revoked |
| Envelope encryption | Encrypt data with a data key, then encrypt that key with a master key |

## Common mistakes

- Encrypting a secret and storing the decryption key beside it.
- Wildcard certificates copied onto dozens of servers.
- No inventory of certificates and their expiry dates.

## Check yourself

1. What is the difference between a static and a dynamic secret?
2. Why is the root CA kept offline?
3. What does mTLS add to ordinary TLS?

<details><summary>Answers</summary>

1. A static secret is long-lived and shared; a dynamic secret is generated on demand and expires quickly.
2. If it were compromised, every certificate beneath it would be untrustworthy and there would be no way to recover.
3. The client also presents a certificate, so both sides are authenticated.
</details>

Next: [10. Cloud IAM](10-cloud-iam.md)
