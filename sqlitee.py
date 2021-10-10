import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

# SOME EXAMPLES HOW TO WORK WITH SQLITE
#cur.execute("""CREATE TABLE games (title str, app_id str)""")
#cur.execute("ALTER TABLE games ADD COLUMN 'runner' TEXT")
#cur.execute("INSERT INTO games (title) VALUES ('globalrunner');")
#sqlitee.cur.execute("DELETE FROM games WHERE runner='/usr/bin/wine';")
