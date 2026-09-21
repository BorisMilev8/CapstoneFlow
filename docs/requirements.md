# Baseline Requirements

| ID | User story | Target | Complexity | Risk |
| --- | --- | --- | --- | --- |
| R1 | As a student, I want to create and edit a project profile so that title, scope, and contacts stay in one place. | Oct 2 | Medium | Low |
| R2 | As a student, I want to view requirements by checkpoint so that I can identify work due at each phase. | Oct 9 | Low | Low |
| R3 | As a student, I want to add and prioritize user stories with acceptance criteria so that planned work can be tested. | Oct 16 | High | Medium |
| R4 | As an assigned reviewer, I want to inspect project scope and planned requirements so that I can identify gaps before implementation. | Oct 16 | Medium | Medium |
| R5 | As a student, I want to submit a weekly status report so that project progress is recorded consistently. | Oct 23 | Medium | Low |
| R6 | As a student, I want to record blockers and help needed so that unresolved issues are visible. | Oct 23 | Low | Low |
| R7 | As a student, I want to view prior weekly status reports so that project history is traceable. | Oct 30 | Medium | Low |
| R8 | As a reviewer, I want to leave item-specific feedback so that requested changes are connected to the affected work. | Nov 6 | High | Medium |
| R9 | As a student, I want to link evidence to a requirement so that completion claims are traceable. | Nov 13 | Medium | Medium |
| R10 | As a student, I want the system to identify missing required items so that incomplete checkpoint work is visible. | Nov 20 | High | High |
| R11 | As a student, I want an explained checkpoint readiness summary so that I know why a checkpoint is or is not ready. | Nov 20 | High | High |
| R12 | As an authorized user, I want protected project access so that users cannot view or change projects outside their membership. | Nov 27 | High | High |

## Readiness rule

A required item is considered ready only when:

- its status is **Complete**,
- it has at least one evidence link, and
- it has no open blocking feedback.

Readiness is the number of ready required items divided by the number of required items. Optional items are excluded. If a checkpoint has zero required items, the interface displays **Not configured** rather than 100%.

The readiness indicator is a workflow aid, not a grade and not faculty approval.
