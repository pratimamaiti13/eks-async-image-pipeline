# Architecture

(To be filled in on Day 15, once the system is actually built and tested - this file
should reflect what was really built and observed, not the plan. Plan lives in commit
history / project notes.)

## Sections to fill in

- Diagram (exported from the planning conversation, or redrawn)
- Why async via SQS, not a direct call (the core design decision)
- Why queue depth, not CPU, drives worker autoscaling
- Fault tolerance: what was tested, what happened, what surprised me
- High availability: multi-AZ choices and what failover actually looked like
- Cost notes: real numbers from this project, not estimates
- What I'd do differently / what doesn't scale beyond this project's size (honest
  limitations section - see assessment notes on what this project does and doesn't
  demonstrate)
