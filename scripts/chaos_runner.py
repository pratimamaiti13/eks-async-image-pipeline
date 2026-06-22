"""
chaos_runner.py - Day 13-14.

Purpose: a small, deliberate chaos engineering tool. Not randomized/continuous like a
real Chaos Monkey - for a 15-day solo project, each chaos scenario should be run
on-demand, observed carefully, and written up as a war story. Randomness would just
make it harder to correlate cause and effect while learning.

Usage (planned):
    python scripts/chaos_runner.py --scenario kill-pod --namespace imgproc
    python scripts/chaos_runner.py --scenario drain-node
    python scripts/chaos_runner.py --scenario bad-deploy
    python scripts/chaos_runner.py --scenario rds-failover

Each scenario, when run, should:
  1. Print exactly what it's about to do and why (so this doubles as documentation)
  2. Execute it (via kubectl/boto3 subprocess calls or SDK)
  3. Print a timestamp marker - used afterward by incident_diagnose.py to know what
     time window of logs/events to pull
"""

import argparse
import datetime
import subprocess


def kill_pod(namespace: str):
    # TODO Day 13-14: kubectl get pods -l app=api-service, pick one, kubectl delete pod <name>
    # Expected: K8s reschedules it, ALB stops routing to it once readiness probe fails,
    # in-flight requests to OTHER pods are unaffected.
    raise NotImplementedError


def drain_node():
    # TODO Day 13-14: kubectl cordon + kubectl drain on one node
    # Expected: pods reschedule onto remaining nodes; if Cluster Autoscaler is sized
    # tight, this might trigger a scale-up.
    raise NotImplementedError


def bad_deploy(namespace: str):
    # TODO Day 13-14: kubectl set image with an intentionally broken tag, observe
    # rollout status, then kubectl rollout undo
    raise NotImplementedError


def rds_failover():
    # TODO Day 13-14: boto3 rds.reboot_db_instance(... ForceFailover=True) - requires
    # multi_az=true to actually be set in Terraform first (Day 11-12 step)
    raise NotImplementedError


SCENARIOS = {
    "kill-pod": kill_pod,
    "drain-node": drain_node,
    "bad-deploy": bad_deploy,
    "rds-failover": rds_failover,
}


def main():
    parser = argparse.ArgumentParser(description="Run a deliberate chaos scenario")
    parser.add_argument("--scenario", choices=SCENARIOS.keys(), required=True)
    parser.add_argument("--namespace", default="imgproc")
    args = parser.parse_args()

    print(f"[{datetime.datetime.now().isoformat()}] Running scenario: {args.scenario}")
    # TODO: dispatch to the right function with the right args


if __name__ == "__main__":
    main()
