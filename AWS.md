# AWS Cloud Setup 

This document covers a full CI/CD deployment flow using:
- GitHub Actions
- Amazon ECR (Docker image registry)
- EC2 Ubuntu (self-hosted runner + app host)

## 1) Create IAM User and Access Keys

1. Open AWS Console and go to `IAM`.
2. Create a new user.
3. Attach required policies (choose least privilege for production):
   - ECR access (push/pull)
   - EC2 access (if needed)
   - Additional service permissions used by your app
4. Create an access key for CLI usage.
5. Save:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## 2) Create ECR Repository

1. Open `ECR` -> `Create repository`.
2. Repository name example: `my-app` or `my-app-image`.
3. Keep tag mutability according to your strategy (`latest` requires mutable tags).
4. Create repository.

Important naming:
- `AWS_ECR_LOGIN_URI` example: `<account-id>.dkr.ecr.<region>.amazonaws.com`
- `ECR_REPOSITORY_NAME` example: `my-app-image`

Do not include full URI inside repository name.

## 3) Launch EC2 Ubuntu Instance

1. Open `EC2` -> `Launch instance`.
2. Choose Ubuntu AMI.
3. Choose instance type based on load (`t3.small` is safer than micro for Docker apps).
4. Attach/create key pair for SSH.
5. Security group inbound:
   - SSH (22)
   - HTTP (80)
   - HTTPS (443)
6. Launch and connect.

For app access, add your application port (example `5000`) to inbound rules.

## 4) Install Docker and AWS CLI on Ubuntu EC2

```bash
sudo apt update
sudo apt install -y docker.io awscli
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu
newgrp docker
docker --version
aws --version
```

## 5) Configure AWS CLI on EC2

```bash
aws configure
```

Provide:
- Access key ID
- Secret access key
- Default region (same region as ECR)
- Output format (`json`)

## 6) GitHub Repository Secrets

In GitHub:
`Repository -> Settings -> Secrets and variables -> Actions`

Add at least:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AWS_ECR_LOGIN_URI`
- `ECR_REPOSITORY_NAME`
- App secrets (examples):
  - `GROQ_API_KEY`
  - `ASTRA_DB_API_ENDPOINT`
  - `ASTRA_DB_APPLICATION_TOKEN`
  - `ASTRA_DB_KEYSPACE`
  - `HUGGINGFACEHUB_API_TOKEN`

Use secret names exactly as referenced in your workflow and app code.

## 7) Setup GitHub Self-Hosted Runner on EC2

1. In GitHub: `Settings -> Actions -> Runners -> New self-hosted runner`.
2. Select Linux and copy commands.
3. On EC2:

```bash
mkdir -p ~/actions-runner && cd ~/actions-runner
curl -o actions-runner-linux-x64-<version>.tar.gz -L https://github.com/actions/runner/releases/download/v<version>/actions-runner-linux-x64-<version>.tar.gz
tar xzf actions-runner-linux-x64-<version>.tar.gz
```

4. Configure with your repo URL and fresh token:

```bash
./config.sh --url https://github.com/<owner>/<repo> --token <RUNNER_TOKEN>
```

Prompt guidance:
- Runner group: press Enter for default unless custom group exists
- Runner name: Enter or accept default
- Labels: Enter or skip
- Work folder: Enter for default

5. Run runner:

```bash
./run.sh
```

Or install as service:

```bash
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```

## 8) CI/CD Workflow Trigger

Workflow path:
- `.github/workflows/main.yaml`

Trigger options:
- Push to configured branch (example `master` or `main`)
- Manual run from GitHub `Actions` tab (`workflow_dispatch`)

## 9) Security Best Practices

- Never commit `.env`, key files, or access credentials to Git.
- Rotate any exposed keys/tokens immediately.
- Prefer least-privilege IAM policies for production.
- Use short-lived tokens where possible.
