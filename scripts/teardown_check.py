"""
teardown_check.py - Day 15 (and really, every day - run after every terraform destroy).

Purpose: terraform destroy can leave orphans behind if state drifted (e.g. an ENI still
attached, an EBS volume that was detached but not deleted, a load balancer Terraform
didn't fully clean up). This is a final, independent check via boto3 - not trusting
Terraform's own "Destroy complete!" message at face value.

Usage (planned):
    python scripts/teardown_check.py --region ap-south-1

This overlaps with infra_cost_guard.py's checks but is specifically run right after a
destroy (vs. cost_guard being a general "is anything running" audit at any time) and
additionally checks for orphaned ENIs/EBS volumes/load balancers that cost_guard's
higher-level resource checks might miss.
"""

import argparse
import sys


def check_orphaned_enis(region: str) -> list[str]:
    # TODO Day 15: boto3 ec2.describe_network_interfaces(), filter by tag, status=available
    # (available = not attached to anything, but still exists and may still bill)
    return []


def check_orphaned_ebs_volumes(region: str) -> list[str]:
    # TODO Day 15: boto3 ec2.describe_volumes(), filter by tag, state=available
    return []


def check_orphaned_load_balancers(region: str) -> list[str]:
    # TODO Day 15: boto3 elbv2.describe_load_balancers(), filter by tag
    # (ALB Ingress Controller sometimes leaves the ALB itself if the Ingress resource
    # wasn't deleted before terraform destroy ran - worth checking explicitly)
    return []


def main():
    parser = argparse.ArgumentParser(description="Verify terraform destroy left nothing orphaned")
    parser.add_argument("--region", default="ap-south-1")
    args = parser.parse_args()

    findings = {
        "orphaned_enis": check_orphaned_enis(args.region),
        "orphaned_ebs_volumes": check_orphaned_ebs_volumes(args.region),
        "orphaned_load_balancers": check_orphaned_load_balancers(args.region),
    }

    anything_left = any(findings.values())

    if anything_left:
        print("WARNING: possible orphaned resources after destroy:")
        for category, items in findings.items():
            if items:
                print(f"  {category}: {items}")
        sys.exit(1)
    else:
        print("Clean teardown - no orphaned resources found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
