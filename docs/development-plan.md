# CapstoneFlow Development Plan

## Purpose

This plan converts the proposal direction into incremental, testable work. Dates are planning targets for Fall 2026 and may be adjusted after instructor or client feedback.

## Milestones

| Target | Milestone | Planned result |
| --- | --- | --- |
| Sep 22 | Proposal and UI prototype | Proposal submitted, repository active, prototype available |
| Sep 23–25 | Client validation and scope review | Confirm need, sponsor/client path, and required agreements |
| Sep 28–Oct 2 | Foundation | Backlog, schema, project setup, authorization test plan |
| Oct 5–16 | Planning workflow | R1–R4 demonstrated and reviewed |
| Oct 19–30 | Alpha target | R1–R7 plus basic R12 safeguards; core workflow testable |
| Nov 2–13 | Feedback and evidence | R8–R9 implemented and tested |
| Nov 16–27 | Beta target | R10–R12 verified; all required workflows present |
| Nov 30–Dec 11 | Final stabilization | Acceptance results, user guide, source archive, report, presentation |

## Development method

Work will be completed in short iterations. Each iteration will:

1. Select a small set of user stories.
2. Confirm acceptance criteria and dependencies.
3. Update the UI or prototype before implementation when needed.
4. Implement one working vertical slice.
5. Add tests before marking the story complete.
6. Demonstrate the work and record feedback.
7. Update issues, risks, and documentation.

## Definition of done

A user story is complete only when its acceptance criteria pass, relevant tests pass, documentation is updated, and unresolved feedback is either closed or recorded as an accepted limitation.

## Testing priorities

Highest-risk areas will be tested early:

- project membership and authorization
- cross-project access denial
- readiness calculation rules
- evidence-link validation
- feedback blocking/resolution state
- database persistence and invalid input
- end-to-end workflow stability

## Data approach

Development and demonstrations will use fictional records until approved access to participant data exists. Secrets and confidential participant material will not be committed to the repository.
