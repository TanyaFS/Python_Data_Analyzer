-- ФИО, тел, почта, отдел, должность

CREATE TABLE IF NOT EXISTS  users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT NOT NULL,
    name TEXT NOT NULL,
    middle_name TEXT NOT NULL DEFAULT '',
    phone INTEGER NOT NULL,
    email TEXT NOT NULL,
    department_id INTEGER NOT NULL DEFAULT 1,
    position_id INTEGER NOT NULL DEFAULT 1,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);