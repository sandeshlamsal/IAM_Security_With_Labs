# Glossary

| Term | Meaning | Chapter |
|---|---|---|
| AAL | Authenticator Assurance Level: how strong a login is (NIST SP 800-63) | 19 |
| ABAC | Attribute-based access control: decisions from attributes and context | 04 |
| Access token | Token an API accepts, stating what the client may do | 03 |
| ACL | Access control list on a resource | 04 |
| AD | Active Directory, Microsoft's on-premises directory | 01 |
| ADCS | Active Directory Certificate Services, Microsoft's CA | 09 |
| ARN | Amazon Resource Name | 10 |
| Assertion | Signed SAML statement about a user | 03 |
| ATO | Authorization to operate: formal approval of a federal system | 19 |
| ATO | Account takeover | 07 |
| AuthN | Authentication: proving who you are | 00, 02 |
| AuthZ | Authorization: deciding what you may do | 00, 04 |
| Birthright access | Access given automatically on joining | 05 |
| Break-glass account | Emergency admin account | 06 |
| CA | Certificate authority | 09 |
| CAC | Common Access Card: Department of Defense smart card | 19 |
| CIAM | Customer identity and access management | 07 |
| CIEM | Cloud infrastructure entitlement management | 10 |
| Claim | One statement inside a token, such as `sub` or `aud` | 03 |
| Conditional access | Policy that uses context to allow, challenge or block | 02 |
| Credential | What is used to prove identity | 00 |
| DN | Distinguished name: full path of a directory object | 01 |
| Entitlement | One grantable item of access | 05 |
| FAL | Federation Assurance Level | 19 |
| Federation | One system trusting another's authentication | 03 |
| FedRAMP | Programme authorizing cloud services for federal use | 19 |
| FICAM | Federal identity, credential and access management architecture | 19 |
| FIDO2 / WebAuthn | Standards behind passkeys | 02 |
| GPO | Group Policy Object | 01 |
| HSM | Hardware security module | 09 |
| IAL | Identity Assurance Level: how well identity was proofed | 19 |
| ICAM | Identity, credential and access management | 19 |
| ID token | OIDC token telling the client who the user is | 03 |
| IdP | Identity provider | 03 |
| IGA | Identity governance and administration | 05 |
| ITDR | Identity threat detection and response | 11 |
| JIT | Just-in-time access | 06 |
| JML | Joiner, mover, leaver | 00, 05 |
| JWT | JSON Web Token | 03 |
| KDC | Kerberos key distribution center | 02 |
| Kerberos | Ticket-based authentication used by AD | 02 |
| LDAP | Protocol for querying directories | 01 |
| Least privilege | Minimum access needed, for the minimum time | 00 |
| MFA | Multi-factor authentication | 02 |
| mTLS | Mutual TLS: both sides present certificates | 09 |
| NHI | Non-human identity | 08 |
| OAuth 2.0 | Framework for delegated access to APIs | 03 |
| OIDC | OpenID Connect: authentication layer on OAuth 2.0 | 03 |
| OU | Organizational unit | 01 |
| PAM | Privileged access management | 06 |
| Passkey | Phishing-resistant credential based on a key pair | 02 |
| PDP / PEP | Policy decision point / policy enforcement point | 04 |
| PIV | Personal Identity Verification: federal smart card credential | 19 |
| PKCE | Protection for the OAuth authorization code | 03 |
| PKI | Public key infrastructure | 09 |
| POA&M | Plan of action and milestones: tracked remediation list | 19, 20 |
| Principal | Whoever is requesting access | 00 |
| Provisioning | Creating accounts and granting access | 00, 05 |
| RBAC | Role-based access control | 04 |
| ReBAC | Relationship-based access control | 04 |
| Refresh token | Token used to obtain new access tokens | 03 |
| RMF | Risk Management Framework | 19 |
| RP / SP | Relying party / service provider: the application | 03 |
| SAML | XML-based SSO protocol | 03 |
| SCIM | Standard API for provisioning users | 03 |
| Scope | Named slice of access an OAuth client requests; also "where a role applies" in cloud IAM | 03, 10 |
| SCP | AWS service control policy | 10 |
| SoD | Separation of duties | 00, 05 |
| SPIFFE | Standard for workload identities | 08 |
| SSO | Single sign-on | 03 |
| STS | AWS Security Token Service | 10 |
| TGT | Kerberos ticket-granting ticket | 02 |
| Tier 0 | The systems that control identity itself | 06 |
| Trust policy | AWS policy stating who may assume a role | 10 |
| Zero trust | Verify every request; no implicit trust from network location | 11 |
| ZSP | Zero standing privilege | 06 |
