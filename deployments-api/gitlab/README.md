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

# plandek-api-scripts - deployments-api - gitlab

Please place in here any scripts that you have found useful when using gitlab

## Available Scripts

### [Send Deployment Example](./send-deployment-example)
A complete integration for sending deployment data from GitLab CI pipelines to Plandek's Deployments API. Includes:
- Python script for sending deployment data
- GitLab CI configuration that automatically tracks both production (tag-based) and staging (branch-based) deployments
- Detailed documentation and setup instructions
