# Lab 00. Setup

## Goal

Get the tools and accounts ready, with cost guardrails in place before anything is created.

## Step 1. Install the tools

On macOS with Homebrew:

```bash
brew install awscli azure-cli kubectl jq
```

Install Docker Desktop from docker.com (needed for lab 03). Python 3 ships with macOS developer tools.

Check everything:

```bash
aws --version && az version --query '"azure-cli"' && kubectl version --client && docker --version && python3 --version
```

## Step 2. Which labs need which account

| Lab | Needs |
|---|---|
| 01 AWS IAM | An AWS account |
| 02 AKS identity | An Azure subscription |
| 03 Conjur | Docker only |
| 04 IGA | Python only |

You create the accounts yourself; a free-tier AWS account and a free Azure account are enough.

## Step 3. AWS: sign in safely

1. After creating the account, turn on MFA for the **root user**, then stop using it.
2. In **IAM Identity Center**, create a user for yourself with the `AdministratorAccess` permission set.
3. Configure the CLI to use it:

```bash
aws configure sso
```

4. Confirm who you are:

```bash
aws sts get-caller-identity
```

You should see your account ID and an ARN containing your user name, not `root`.

## Step 4. AWS: budget alert

In the console: **Billing and Cost Management > Budgets > Create budget > Zero spend budget**. It emails you as soon as anything costs money.

## Step 5. Azure: sign in

```bash
az login
```

```bash
az account show --query "{subscription:name, tenant:tenantId, user:user.name}"
```

## Step 6. Azure: budget alert

In the portal: **Cost Management > Budgets > Add**. Set a small monthly amount with an alert at 50%.

## What you proved

You have a non-root admin identity in each cloud, you can show which identity the CLI is using, and you will be told if a lab starts costing money.

Next: [Lab 01. AWS IAM](../01-aws-iam/README.md)
