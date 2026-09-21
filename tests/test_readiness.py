from app.services.readiness import calculate_readiness


def test_readiness_requires_complete_evidence_and_no_blocker():
    items = [
        {
            "status": "Complete",
            "required": True,
            "evidence_links": ["https://example.org/1"],
            "open_blocking_feedback": False,
            "overdue": False,
        },
        {
            "status": "Complete",
            "required": True,
            "evidence_links": [],
            "open_blocking_feedback": False,
            "overdue": False,
        },
        {
            "status": "Complete",
            "required": True,
            "evidence_links": ["https://example.org/3"],
            "open_blocking_feedback": True,
            "overdue": False,
        },
        {
            "status": "Complete",
            "required": True,
            "evidence_links": ["https://example.org/4"],
            "open_blocking_feedback": False,
            "overdue": False,
        },
    ]

    result = calculate_readiness(items)

    assert result["configured"] is True
    assert result["ready_count"] == 2
    assert result["required_count"] == 4
    assert result["readiness_percent"] == 50
    assert result["missing_evidence_count"] == 1
    assert result["blocking_feedback_count"] == 1


def test_optional_items_do_not_change_denominator():
    items = [
        {
            "status": "Complete",
            "required": True,
            "evidence_links": ["https://example.org/required"],
            "open_blocking_feedback": False,
            "overdue": False,
        },
        {
            "status": "In progress",
            "required": False,
            "evidence_links": [],
            "open_blocking_feedback": True,
            "overdue": True,
        },
    ]

    result = calculate_readiness(items)

    assert result["required_count"] == 1
    assert result["readiness_percent"] == 100


def test_zero_required_items_are_not_configured():
    result = calculate_readiness(
        [
            {
                "status": "Complete",
                "required": False,
                "evidence_links": [],
                "open_blocking_feedback": False,
                "overdue": False,
            }
        ]
    )

    assert result["configured"] is False
    assert result["readiness_percent"] is None
    assert result["required_count"] == 0
