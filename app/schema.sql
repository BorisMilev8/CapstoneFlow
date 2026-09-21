DROP TABLE IF EXISTS requirements;

CREATE TABLE requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    acceptance_criteria TEXT NOT NULL,
    checkpoint TEXT NOT NULL CHECK (checkpoint IN ('Proposal', 'Alpha', 'Beta', 'Final')),
    priority TEXT NOT NULL CHECK (priority IN ('Must', 'Should', 'Could')),
    status TEXT NOT NULL CHECK (status IN ('Planned', 'In progress', 'Complete')),
    required INTEGER NOT NULL DEFAULT 1 CHECK (required IN (0, 1)),
    evidence_url TEXT NOT NULL DEFAULT '',
    blocking_feedback INTEGER NOT NULL DEFAULT 0 CHECK (blocking_feedback IN (0, 1)),
    overdue INTEGER NOT NULL DEFAULT 0 CHECK (overdue IN (0, 1)),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
