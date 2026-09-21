def calculate_readiness(items):
    """Calculate explained checkpoint readiness for required items.

    A required item is ready only when:
    - status is Complete,
    - at least one evidence link exists, and
    - no blocking feedback remains open.
    """
    required_items = [item for item in items if item.get("required", True)]

    if not required_items:
        return {
            "configured": False,
            "readiness_percent": None,
            "ready_count": 0,
            "required_count": 0,
            "missing_evidence_count": 0,
            "blocking_feedback_count": 0,
            "overdue_incomplete_count": 0,
        }

    ready_count = 0
    missing_evidence_count = 0
    blocking_feedback_count = 0
    overdue_incomplete_count = 0

    for item in required_items:
        status_complete = item.get("status") == "Complete"
        has_evidence = bool(item.get("evidence_links"))
        has_blocker = bool(item.get("open_blocking_feedback"))
        is_overdue = bool(item.get("overdue"))

        if not has_evidence:
            missing_evidence_count += 1
        if has_blocker:
            blocking_feedback_count += 1
        if is_overdue and not status_complete:
            overdue_incomplete_count += 1

        if status_complete and has_evidence and not has_blocker:
            ready_count += 1

    readiness_percent = round((ready_count / len(required_items)) * 100)

    return {
        "configured": True,
        "readiness_percent": readiness_percent,
        "ready_count": ready_count,
        "required_count": len(required_items),
        "missing_evidence_count": missing_evidence_count,
        "blocking_feedback_count": blocking_feedback_count,
        "overdue_incomplete_count": overdue_incomplete_count,
    }
