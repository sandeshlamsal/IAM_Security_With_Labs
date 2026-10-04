# 01. Screens and fundamentals

The first two conversations: a recruiter screen about you, then a technical screen of short questions. Answers here are written to be **spoken**, at roughly 30 to 60 seconds each.

Say your own answer aloud before opening each model answer.

## Part A. The recruiter screen

### "Tell me about yourself"

Have this ready word for word. Keep it under 90 seconds. Fill the brackets from your real experience; do not claim anything you have not done.

> "I'm a [current role] with [N years] in [area]. Most recently I [one concrete thing you built or ran, with a result].
>
> The part of that work I've gone deepest on is identity: [what you have actually done, for example secrets management with OpenBao, SSO integrations, access automation].
>
> I'm looking at this role because [specific reason tied to the job: lifecycle automation, scale, the mix of engineering and security]. What I'd bring is [one or two strengths], and what I'm keen to grow in is [honest area]."

### "Why IAM?"

<details><summary>Model answer</summary>

"Identity is where most attacks now start: people log in with stolen credentials more often than they break in. It's also the one security control every employee touches every day, so getting it right improves security and how fast people can work at the same time. I like that it's both an engineering problem and a people problem."
</details>

### "What are you looking for in your next role?"

Tie it to the posting: hands-on design and build, broad populations, working across teams and vendors.

### Questions about gaps

If you lack a listed requirement, say so and bridge:

> "I haven't run [X] in production. I've [closest real experience], and I've built [lab or project] to learn it. The concepts I'd carry over are [two specifics]."

## Part B. Rapid fundamentals

Interviewers move quickly here. Short, correct and structured wins.

### Core concepts

**1. What is the difference between authentication and authorization?**

<details><summary>Model answer</summary>

"Authentication proves who you are; the output is an identity. Authorization decides what that identity may do; the output is allow or deny. You authenticate once per session but you're authorized on every action. A classic bug is treating a successful login as permission to do everything."
</details>

**2. What is least privilege, and why is it hard in practice?**

<details><summary>Model answer</summary>

"Giving each identity only the access its job needs, for only as long as it needs it. It's hard because access is easy to grant and nobody asks for it to be removed. People change roles and keep the old access. So in practice you need automation: access derived from HR attributes, time limits on anything extra, and reviews that focus on unusual or unused access."
</details>

**3. Explain joiner, mover, leaver.**

<details><summary>Model answer</summary>

"The three stages of a workforce identity. Joiner: the HR record creates the account and birthright access. Mover: a job change adds new access and should remove the old. Leaver: access is removed when employment ends. Mover is where it usually fails, because the old access stays, and leaver is where the risk is highest if it's slow."
</details>

**4. What is separation of duties?**

<details><summary>Model answer</summary>

"Making sure no one person can complete a risky process alone, like creating a vendor and approving its payment. You enforce it twice: preventively when access is requested, and detectively with a scan afterwards, because a job move can create the conflict from two grants that were each fine on their own."
</details>

### Protocols

**5. SAML, OAuth and OpenID Connect: what is each for?**

<details><summary>Model answer</summary>

"SAML is XML-based single sign-on, common in enterprise apps: the identity provider sends a signed assertion saying who the user is. OAuth 2.0 is delegated authorization: it issues access tokens so a client can call an API on someone's behalf. It doesn't say who the user is. OpenID Connect adds that identity layer on top of OAuth with an ID token. So: SAML and OIDC for login, OAuth for API access."
</details>

**6. What is the difference between an ID token and an access token?**

<details><summary>Model answer</summary>

"The ID token is for the client application and tells it who signed in. The access token is for the API and says what the client may do. A common mistake is sending the ID token to an API; the API should only accept access tokens meant for it, which it checks with the audience claim."
</details>

**7. What do you validate in a JWT?**

<details><summary>Model answer</summary>

"The signature against the issuer's published keys, the issuer, the audience, and the expiry. Then the scopes or claims the endpoint needs. Skipping the audience check is the common mistake: it means a token issued for a different API would be accepted."
</details>

**8. What is PKCE and why does it exist?**

<details><summary>Model answer</summary>

"It protects the authorization code flow. The client creates a random secret, sends a hash of it at the start, and sends the secret itself when exchanging the code for tokens. If someone intercepts the code they can't redeem it, because they don't have the secret. It's now recommended for all clients, not just mobile apps."
</details>

**9. What is SCIM?**

<details><summary>Model answer</summary>

"A standard REST API for provisioning. The identity provider calls the application to create, update and deactivate users and groups. SSO lets people in; SCIM makes sure the account exists and, more importantly, gets removed. The thing I always test is deactivation, because some vendors support create and quietly don't support that."
</details>

**10. Where does LDAP still show up?**

<details><summary>Model answer</summary>

"It's the protocol for querying directories like Active Directory. Older and infrastructure software still authenticates with it: network devices, Linux servers, some databases. The pattern is a low-privilege bind account, always over TLS, and replacing it with SAML or OIDC when the application allows."
</details>

**11. How does SAML SSO work, briefly?**

<details><summary>Model answer</summary>

"The user opens the app. The app redirects the browser to the identity provider with a request. The user signs in there. The identity provider returns a signed assertion through the browser. The app checks the signature, the audience and the time window, then creates a session. Trust was set up beforehand by exchanging metadata and the signing certificate."
</details>

**12. What is the difference between IdP-initiated and SP-initiated SSO?**

<details><summary>Model answer</summary>

"SP-initiated starts at the application, which sends a request to the identity provider. IdP-initiated starts from the identity provider's dashboard, with no request from the app. SP-initiated is preferred because the response is tied to a request, which protects against some replay and injection attacks."
</details>

### Authentication

**13. Why is SMS a weak second factor? What is better?**

<details><summary>Model answer</summary>

"SMS can be intercepted or redirected by SIM swapping, and like any one-time code it can be phished in real time. Better is something phishing-resistant: FIDO2 security keys or passkeys, where the credential is bound to the real site's domain, so a fake site gets nothing usable."
</details>

**14. What is MFA fatigue?**

<details><summary>Model answer</summary>

"An attacker who has the password triggers push prompts repeatedly until the user approves one to make it stop. Number matching helps, and phishing-resistant factors remove the problem because there's nothing to approve by mistake."
</details>

**15. A user's account is disabled. Can they still access things?**

<details><summary>Model answer</summary>

"Possibly. Existing sessions and refresh tokens can keep working until they expire or are revoked. API keys and personal tokens they created aren't tied to their login. And any app with its own local password isn't affected at all. So deprovisioning means disable, revoke sessions and tokens, deactivate in each app, and revoke anything SSO never covered."
</details>

### Lifecycle and platform

**16. Why should the HR system be the source of truth?**

<details><summary>Model answer</summary>

"Because HR is where employment facts are decided: who works here, in what job, reporting to whom, and when they leave. If access is derived from that record, it's correct by default and changes automatically. If identity is managed by tickets, it's only as good as people remembering to raise them."
</details>

**17. What key do you match identities on?**

<details><summary>Model answer</summary>

"The worker ID from the HR system. It's unique, it never changes and it's never reused. Email and name both change, and matching on them creates duplicates on rename, rehire or contractor conversion."
</details>

**18. What is just-in-time provisioning, and what is its weakness?**

<details><summary>Model answer</summary>

"The application creates the account on first SSO login from the attributes in the assertion. It's easy to set up, but nothing ever removes the account. A leaver can't log in, but their account, data, licence and any API tokens remain. So it needs a reconciliation process or it's only suitable for low-risk apps."
</details>

**19. In Okta, how does an HR attribute become access to an app?**

<details><summary>Model answer</summary>

"The attribute comes in from the HR source. A group rule puts the user in a group based on it. The group is assigned to the application. That assignment gives the SSO tile and triggers provisioning to create the account. Change the attribute and the rest follows."
</details>

**20. What is an authentication policy in Okta Identity Engine?**

<details><summary>Model answer</summary>

"A per-application rule set for what's needed to open that app: which factor types, how recently, and from what kind of device. It lets a wiki need less than payroll. It sits under the global session policy, which decides whether a session can exist at all."
</details>

### Cloud and engineering

**21. In AWS, what is the difference between a role's trust policy and its permission policy?**

<details><summary>Model answer</summary>

"The trust policy says who may assume the role. The permission policy says what the role may do once assumed. Both must allow. I've seen 'access denied' where the permissions were right and the trust policy didn't name the caller."
</details>

**22. How is an AWS access decision made?**

<details><summary>Model answer</summary>

"Default is deny. An explicit deny anywhere wins. Guardrails like service control policies and permission boundaries set a ceiling. Then there has to be an allow in an identity or resource policy. So when something's denied I check for explicit denies and guardrails before I look at the allow."
</details>

**23. How should people get access to AWS accounts?**

<details><summary>Model answer</summary>

"Through federation from the identity provider into IAM Identity Center, with users and groups pushed by SCIM. Group membership maps to permission sets, which become roles in each account. People get temporary credentials. Nobody has an IAM user or a long-lived access key, and AWS access follows the same joiner-mover-leaver process as everything else."
</details>

**24. Why manage identity configuration as code?**

<details><summary>Model answer</summary>

"Every change gets a reviewer, a history and a rollback. Test and production stay the same. And the Git history is your change-control evidence for audit. The pipeline that applies it becomes highly privileged, so it needs short-lived credentials and protected branches."
</details>

**25. What makes a provisioning job safe?**

<details><summary>Model answer</summary>

"Five things. It's idempotent, so it can be re-run. It retries temporary failures. It has a dry run. It refuses to proceed if it would deactivate an unusual number of accounts, which protects against a bad HR feed. And it verifies results instead of trusting a success response."
</details>

### Explaining simply

These test the communication requirement directly. Aim for two sentences with no jargon.

**26. Explain SSO to a non-technical executive.**

<details><summary>Model answer</summary>

"You sign in once with your company account and that opens all your work tools. For us it means one place to protect, and one switch to turn off when someone leaves."
</details>

**27. Explain why we need SCIM to an engineering leader who thinks SSO is enough.**

<details><summary>Model answer</summary>

"SSO controls the front door. It doesn't remove the account inside. Without provisioning, a leaver's account, data and API tokens stay in the tool, and we pay for the licence. SCIM removes them automatically, and it also means your new hires have accounts before their first login."
</details>

**28. Explain OAuth to a product manager.**

<details><summary>Model answer</summary>

"It's a way to let one app do specific things in another on your behalf without giving it your password. Like a valet key: it starts the car but doesn't open the boot, and you can cancel it without changing your own key."
</details>

## Self-check

After a pass through this file, you should be able to answer any ten of these in ten minutes, aloud, without notes. If an answer runs past 90 seconds, cut the mechanism and keep the failure mode.

Next: [02. Technical deep dive](02-technical-deep-dive.md)
