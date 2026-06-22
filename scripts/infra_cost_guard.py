"""
infra_cost_guard.py - Day 1-3.

Purpose: check AWS for resources tagged Project=imgproc that are currently running,
and warn if anything's been left up (e.g. forgot to terraform destroy after a session).

Real problem this solves: EKS control plane costs ~$0.10/hr regardless of usage - the
single biggest risk to this project's cost budget is forgetting to tear it down
overnight. This script is meant to be run manually (or via cron) to catch that.

Usage (planned):
    python scripts/infra_cost_guard.py --region ap-south-1

Checks planned:
  - EKS clusters with tag Project=imgproc -> should be 0 outside work sessions
  - EC2 instances (covers both on-demand + spot node groups) with the same tag
  - RDS instances with the same tag
  - NAT gateways (easy to forget, not destroyed by `terraform destroy` if state drifted)

Exit code: 0 if nothing found running, 1 if resources found (so this can be used in
a pre-commit hook or just checked manually before closing the laptop).
"""

import argparse
import sys


def check_eks_clusters(region: str) -> list[str]:
    # TODO Day 1-3: boto3 eks.list_clusters(), filter by tag
    return []


def check_ec2_instances(region: str) -> list[str]:
    # TODO Day 1-3: boto3 ec2.describe_instances() with Filters on tag:Project + running state
    return []


def check_rds_instances(region: str) -> list[str]:
    # TODO Day 1-3: boto3 rds.describe_db_instances(), filter by tag
    return []


def main():
    parser = argparse.ArgumentParser(description="Audit AWS for resources left running")
    parser.add_argument("--region", default="ap-south-1")
    args = parser.parse_args()

    findings = {
        "eks_clusters": check_eks_clusters(args.region),
        "ec2_instances": check_ec2_instances(args.region),
        "rds_instances": check_rds_instances(args.region),
    }

    anything_running = any(findings.values())

    if anything_running:
        print("WARNING: resources still running:")
        for category, items in findings.items():
            if items:
                print(f"  {category}: {items}")
        sys.exit(1)
    else:
        print("Clean - nothing tagged Project=imgproc is currently running.")
        sys.exit(0)


if __name__ == "__main__":
    main()
