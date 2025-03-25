#!/usr/bin/env python3

import os
import sys
import json
import argparse
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PlandekDeploymentAPI:
    def __init__(self, api_token=None):
        self.base_url = "https://api.plandek.com/deployments/v1"
        self.api_token = api_token or os.getenv("PLANDEK_API_TOKEN")
        if not self.api_token:
            raise ValueError("Plandek API token is required. Set PLANDEK_API_TOKEN environment variable or pass it as an argument.")

    def send_deployment(self, deployment_data):
        """Send deployment data to Plandek API"""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        response = requests.post(
            f"{self.base_url}/deployment",
            headers=headers,
            json=deployment_data
        )

        if response.status_code == 401:
            raise Exception("Authentication failed. Please check your API token.")
        
        response.raise_for_status()
        return response.json()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Send GitLab deployment data to Plandek API")
    parser.add_argument("--client-key", required=True, help="Plandek client key")
    parser.add_argument("--pipeline", required=True, help="Pipeline identifier")
    parser.add_argument("--build", required=True, help="Build identifier")
    parser.add_argument("--status", required=True, choices=["success", "failure"], help="Deployment status")
    parser.add_argument("--commits", required=True, help="Comma-separated list of commit hashes")
    parser.add_argument("--branch-name", help="Branch name")
    parser.add_argument("--environment", help="Environment name (e.g., production, staging)")
    parser.add_argument("--is-prod", action="store_true", help="Flag to indicate if this is a production deployment")
    parser.add_argument("--service-name", help="Application or service name")
    parser.add_argument("--release-id", help="Application or service release ID")
    parser.add_argument("--context", help="Additional context for the deployment")
    parser.add_argument("--api-token", help="Plandek API token (can also be set via PLANDEK_API_TOKEN env var)")
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Initialize API client
    api = PlandekDeploymentAPI(api_token=args.api_token)
    
    # Prepare deployment data
    deployment_data = {
        "client_key": args.client_key,
        "pipeline": args.pipeline,
        "build": args.build,
        "status": args.status,
        "commits": args.commits.split(","),
        "calculate_commits_in_build": False,
        "deployed_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    # Add optional fields if provided
    if args.branch_name:
        deployment_data["branch_name"] = args.branch_name
    if args.environment:
        deployment_data["environment_name"] = args.environment
        deployment_data["is_prod_environment"] = args.is_prod
    if args.service_name:
        deployment_data["application_or_service_name"] = args.service_name
    if args.release_id:
        deployment_data["application_or_service_release_id"] = args.release_id
    if args.context:
        deployment_data["context"] = args.context

    try:
        response = api.send_deployment(deployment_data)
        print(json.dumps(response, indent=2))
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
