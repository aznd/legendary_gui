import sqlite3


def sqlite():
    global conn
    conn = sqlite3.connect('data.db')
    conn.commit

# conn.execute("INSERT INTO games(gamename, codename, runner) VALUES ('HITMAN', 'Barbet', '/usr/bin/wine')")
