import sqlite3


def sqlite():
    global cur
    global conn
    global finalthing
    conn = sqlite3.connect('data.db')
    conn.commit

# conn.execute("INSERT INTO games(gamename, codename, runner) VALUES ('HITMAN', 'Barbet', '/usr/bin/wine')")
