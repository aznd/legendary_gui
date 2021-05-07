#!/usr/bin/python
import subprocess
import tkinter as tk
import os
import menubar_settings
import sqlite3
import sqlite
import game_import
import re
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
color_light_black = "#2f2f2f"
color_white = "#ffffff"

conn = sqlite3.connect('Development/gui_legendary/data.db')
cur = conn.cursor()
#cur.execute("""CREATE TABLE games (title str, app_id str)""")
#cur.execute("ALTER TABLE games ADD COLUMN 'runner' TEXT")
#cur.execute("INSERT INTO games (title) VALUES ('globalrunner');")
# conn.commit()

cur.execute("INSERT INTO games (runner) VALUES ('/usr/bin/wine');")
conn.commit()
root = tk.Tk()
root.geometry("1300x800")
root.title("gui_legendary")
root.iconphoto(True, tk.PhotoImage(
    file='/home/jack/Development/gui_legendary/icon.png'))
root.configure(bg=color_light_black)



# FRAMES
frame_left = tk.Frame(root, bg=color_light_black)
frame_left.grid(row=0, column=0, pady=0, padx=0)
frame_right = tk.Frame(root, bg=color_light_black)
frame_right.grid(row=0, column=1, pady=0, padx=0)


# GETTING OWNED GAMES IN A VARIABLE
#list_owned_games = os.popen('legendary list-games')
#output_list_games = list_owned_games.read()
#list_owned_games.close()

# GETTING OWNED GAMES IN DB
refresh_button = tk.Button(
    frame_right, text="Get your games into the db. \n(Don't click this more than once, have to change this)",
    command=lambda: get_owned_games_sqlite())
refresh_button.grid(row=2, column=0)

# FUNCTION FOR THE LAUNCH GAME BUTTON
def convertTuple(tup):
    str = ''.join(tup)
    return str

def launch_game():
    for i in listbox_all_games.curselection():
        sel_game = listbox_all_games.get(i)
    conn = sqlite3.connect('/home/jack/Development/gui_legendary/data.db')
    cur = conn.cursor()
    cur.execute("SELECT app_id FROM games WHERE title=?", (sel_game,))
    finalthing2 = cur.fetchone()
    cur.execute("SELECT runner FROM games WHERE title=?",
                ('globalrunner',))
    sel_global_runner = cur.fetchone()
    str_converted_runner = convertTuple(sel_global_runner)
    str_converted_sel_game = convertTuple(finalthing2)
    subprocess.Popen(
        ['legendary', 'launch', str_converted_sel_game, '--wine', str_converted_runner])


# LISTBOX FOR ALL GAMES
listbox_all_games = tk.Listbox(frame_left, selectmode="SINGLE", bg=color_light_black,
                               fg=color_white, height=38, width=50)
listbox_all_games.grid(row=0, column=0)
listbox_all_games.bind('<Double-1>', launch_game)
x = 1
#lines = output_list_games.split('\n')
cur.execute("SELECT title from games")
title_db = cur.fetchall()
for items in title_db:
    listbox_all_games.insert('end', items[0])


listbox_all_games_btn = tk.Button(root, text="launch selected",
                                  command=lambda: launch_game())
listbox_all_games_btn.grid(row=1, column=0)
#for line in lines:
#    match = re.match(
#        r'^ \* (?P<title>.*) \(App name: (?P<appId>.*) \| Version: (?P<version>.*)\)$', line)
#    if not match:
#        continue
#    title = match.group('title')
#app_id = match.group('appId')
#
#x += 1


# FUNCTION FOR GETTING GAMES INTO THE DB

def get_owned_games_sqlite():
    # sqlite.conn.execute(
    # "SELECT gamename FROM tasks WHERE gamename=?", (priority,))
    lines = output_list_games.split('\n')
    for line in lines:
        match = re.match(
            r'^ \* (?P<title>.*) \(App name: (?P<appId>.*) \| Version: (?P<version>.*)\)$', line)
        if not match:
            continue
        title = match.group('title')
        app_id = match.group('appId')
        # UNUSED, MAYBE IN THE FUTURE THIS WILL BE USED
        # version = match.group('version')
        cur.execute(
            "INSERT INTO games(title, app_id) VALUES (?,?);", (title, app_id))
    # sqlite.conn.execute("INSERT INTO games(gamename) VALUES ('done')")
    sqlite.conn.commit()



# GETTING INSTALLED GAMES IN A VARIABLE
list_installed_games = os.popen('legendary list-installed')
output_list_installed_games = list_installed_games.read()
list_installed_games.close()


# WIDGET FOR LIST OF INSTALLED GAMES
widget_list_installed_games = tk.Text(
    frame_right,
    bg=color_light_black,
    cursor="xterm",
    height=45,
    width=85,
    fg=color_white)
widget_list_installed_games.grid(row=0, column=0)
widget_list_installed_games.insert("1.0", output_list_installed_games)
widget_list_installed_games['state'] = 'disabled'


# FUNCTION TO CHANGE GLOBAL RUNNER
def change_global_runner_func():
    file_globalrunner_chosen = askopenfilename()
    cur.execute(
        "UPDATE games SET runner = (?) WHERE title = 'globalrunner';", (file_globalrunner_chosen,))
    conn.commit()


# WIDGET TO CHANGE THE GLOBAL RUNNER
change_global_runner = tk.Button(
    root, text="Change the global runner", command=lambda: change_global_runner_func())
change_global_runner.grid(row=1, column=1)


# MENUBAR
menubar = tk.Menu(root)
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="Exit", command=root.destroy)
file.add_command(label="Settings",
                 command=lambda: menubar_settings.topwindow_settings())

# IMPORT GAMES
import_games_btn = tk.Button(frame_right, text="Import a game",
                             command=lambda: game_import.topwindow_import_game())
import_games_btn.grid(row=1, column=0, padx=0, pady=0)

# CHANGE RUNNER FOR A SINGLE GAME
def change_single_game():
    toplevel_change_single_game = tk.Toplevel()
    


root.config(menu=menubar)
root.mainloop()
