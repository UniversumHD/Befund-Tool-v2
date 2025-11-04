CREATE TABLE kategorien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
CREATE TABLE bausteine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kategorie INTEGER NOT NULL,
    text TEXT NOT NULL,
    kuerzel TEXT,
    FOREIGN KEY (kategorie) REFERENCES kategorien(id)
);
CREATE TABLE befundverlauf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    geburtsdatum TEXT NOT NULL,
    befund TEXT NOT NULL
);
INSERT INTO kategorien (id, name) VALUES (0, 'nicht Kategorisiert');