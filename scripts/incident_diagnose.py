"""
incident_diagnose.py - Day 13-14.

Purpose: the one legitimate "AI for ops" piece in this project (see project notes -
predictive scaling and trained anomaly detection were deliberately excluded as not
honest/buildable at this scale; this is the slice that is). After running a chaos
scenario, pull the relevant logs/events and ask an LLM to reason over them and produce
a structured root-cause writeup - then compare it against what you know actually
happened, since you triggered it yourself. That comparison IS the validation.

Usage (planned):
    python scripts/incident_diagnose.py --namespace imgproc --since "5m"

Context gathered (planned):
  - kubectl describe on recently-changed pods
  - kubectl get events --sort-by=.lastTimestamp
  - pod logs (kubectl logs, last N lines) for api-service and worker-service
  - optionally: relevant CloudWatch metrics around the same time window

This is explicitly NOT claiming the model "detected" an anomaly - it's reasoning over
text you hand it, the same way a human would grep logs, just faster. Worth stating
that distinction plainly in the README.
"""

import argparse
import subprocess


def gather_kubectl_events(namespace: str) -> str:
    # TODO Day 13-14: subprocess.run(["kubectl", "get", "events", "-n", namespace,
    #   "--sort-by=.lastTimestamp"], capture_output=True, text=True).stdout
    raise NotImplementedError


def gather_pod_logs(namespace: str, label_selector: str, tail_lines: int = 200) -> str:
    # TODO Day 13-14: kubectl logs -l {label_selector} -n {namespace} --tail={tail_lines}
    # --all-containers --prefix
    raise NotImplementedError


def gather_pod_describe(namespace: str, pod_name: str) -> str:
    # TODO Day 13-14: kubectl describe pod {pod_name} -n {namespace}
    raise NotImplementedError


def ask_llm_for_diagnosis(context: str) -> str:
    # TODO Day 13-14: call the Anthropic API (see anthropic_api_in_artifacts notes /
    # standard SDK usage) with a system prompt establishing the role ("you are
    # assisting with infrastructure incident triage") and the gathered context,
    # asking for: likely root cause, supporting evidence from the logs, suggested
    # remediation. Keep this structured (e.g. ask for a short JSON or clearly
    # labeled sections) so it's easy to compare against the real cause afterward.
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="Gather context and ask an LLM to diagnose an incident")
    parser.add_argument("--namespace", default="imgproc")
    parser.add_argument("--since", default="5m")
    args = parser.parse_args()

    events = gather_kubectl_events(args.namespace)
    api_logs = gather_pod_logs(args.namespace, "app=api-service")
    worker_logs = gather_pod_logs(args.namespace, "app=worker-service")

    context = f"EVENTS:\n{events}\n\nAPI LOGS:\n{api_logs}\n\nWORKER LOGS:\n{worker_logs}"
    diagnosis = ask_llm_for_diagnosis(context)

    print("=== LLM diagnosis ===")
    print(diagnosis)
    print("\n(Compare this against the chaos scenario you actually ran.)")


if __name__ == "__main__":
    main()
