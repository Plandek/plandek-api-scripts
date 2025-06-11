<!--
Copyright 2025 Plandek Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# GitLab to Plandek Deployment Data Sender

This example demonstrates how to send deployment data from GitLab to Plandek's Deployments API.

## send_deployment.py

A Python script to send deployment data from GitLab to Plandek's Deployments API.

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Plandek API token either:
   - As an environment variable: `PLANDEK_API_TOKEN=your_token`
   - Or pass it directly using the `--api-token` argument

### Usage

```bash
python send_deployment.py \
  --client-key YOUR_CLIENT_KEY \
  --pipeline pipeline_name \
  --build build_id \
  --status success \
  --commits commit1,commit2 \
  --environment production \
  --is-prod \
  --service-name my-service \
  --release-id v1.0.0
```

#### Required Arguments
- `--client-key`: Your Plandek client key
- `--pipeline`: Pipeline identifier
- `--build`: Build identifier
- `--status`: Deployment status (success/failure)
- `--commits`: Comma-separated list of commit hashes

#### Optional Arguments
- `--branch-name`: Branch name
- `--environment`: Environment name (e.g., production, staging)
- `--is-prod`: Flag to indicate if this is a production deployment
- `--service-name`: Application or service name
- `--release-id`: Application or service release ID
- `--context`: Additional context for the deployment
- `--api-token`: Plandek API token (can also be set via PLANDEK_API_TOKEN env var)

## GitLab CI Integration

A `.gitlab-ci.yml` file is provided to automatically send deployment data to Plandek when deployments occur.

### Setup

1. Add the following variables in your GitLab project's CI/CD settings (Settings > CI/CD > Variables):
   - `PLANDEK_API_TOKEN`: Your Plandek API token
   - `PLANDEK_CLIENT_KEY`: Your Plandek client key

### How it Works

The pipeline automatically sends deployment data to Plandek in two scenarios:

1. **Production Deployments**
   - Triggered when: A new tag is created
   - Environment: production
   - IS_PROD flag: true

2. **Staging Deployments**
   - Triggered when: Changes are merged to the default branch
   - Environment: staging
   - IS_PROD flag: false

The pipeline uses GitLab's built-in CI variables to populate the deployment data:
- Pipeline ID from `CI_PIPELINE_ID`
- Build ID from `CI_JOB_ID`
- Commit hash from `CI_COMMIT_SHA`
- Branch name from `CI_COMMIT_REF_NAME`
- Service name from `CI_PROJECT_NAME`
- Release ID from `CI_COMMIT_TAG` (when available)
