#!/usr/bin/python
import subprocess
import tkinter as tk
import os
import menubar_settings
import game_import
import re
import sqlitee
import logging
from tkinter.filedialog import askopenfilename

color_light_black = "#2f2f2f"
color_white = "#ffffff"
get_games_in_db_text = """Get your games into the db. \n
                          (Don't click this more than once,
                          have to change this)"""


class App:
    def __init__(self, geometry, title, listbox_all_games, title_db):
        self.geometry = geometry
        self.title = title
        self.listbox_all_games = listbox_all_games
        self.title_db = title_db

    def setup(self):
        root = tk.Tk()
        root.geometry("1300x800")
        root.title("Legendary GUI")
        root.iconphoto(True, tk.PhotoImage(file="./icon.png"))

        # FRAMES
        frame_left = tk.Frame(root, bg=color_light_black)
        frame_left.grid(row=0, column=0, pady=0, padx=0)
        frame_right = tk.Frame(root, highlightbackground="white",
                               bg=color_light_black,
                               borderwidth=4)
        frame_right.grid(row=0, column=1, pady=0, padx=0)

        refresh_button = tk.Button(frame_right,
                                   text=get_games_in_db_text,
                                   command=lambda: self.get_owned_games())
        refresh_button.grid(row=2, column=0)

        # LISTBOX FOR ALL GAMES
        self.listbox_all_games = tk.Listbox(frame_left,
                                            selectmode="SINGLE",
                                            bg=color_light_black,
                                            fg=color_white, height=38, width=50)
        self.listbox_all_games.grid(row=1, column=0)
        self.listbox_all_games.bind('<Double-1>', lambda x: self.launch_game())

        # Unsorted things
        sqlitee.cur.execute("SELECT title from games")
        self.title_db = sqlitee.cur.fetchall()
        for items in self.title_db:
            self.listbox_all_games.insert('end', items[0])
        text_hint_launch = tk.Label(
            frame_left, text="To launch a game, double click on it.")
        text_hint_launch.grid(row=0, column=0, pady=10)

        """
        for line in lines:
            match = re.match(
                r'^ \* (?P<title>.*) \(App name: (?P<appId>.*) \| Version: (?P<version>.*)\)$', line)
            if not match:
                continue
            title = match.group('title')
        app_id = match.group('appId')
        """

        # WIDGET TO CHANGE THE GLOBAL RUNNER
        change_global_runner = tk.Button(root,
                                         text="Change the global runner",
                                         command=lambda: change_global_runner_func())
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

        change_runner_single_button = tk.Button(
            root, text="Change the runner for a specific game",
            command=lambda: self.change_single_runner())
        change_runner_single_button.grid(row=2, column=1)

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

    def setupsql(self):
        try:
            sqlitee.cur.execute("SELECT title from games")
        except Exception:
            print("Something went wrong with the database...")

    # Maybe this could be solved by just using the str() func?
    def convertTuple(self, tup):
        string = ''.join(tup)
        return string

    def launch_game(self):
        for i in self.listbox_all_games.curselection():
            sel_game = self.listbox_all_games.get(i)
        sqlitee.cur.execute(f"SELECT app_id FROM games WHERE title={sel_game}")
        finalthing2 = sqlitee.cur.fetchone()
        str_converted_sel_game = self.convertTuple(finalthing2)
        sqlitee.cur.execute(
            f"SELECT runner FROM games WHERE app_id={str_converted_sel_game}")
        runner_sqlite = sqlitee.cur.fetchone()
        runner_final = self.convertTuple(runner_sqlite)
        subprocess.Popen(
            ['legendary', 'launch', str_converted_sel_game, '--wine', runner_final])

    # FUNCTION FOR GETTING GAMES INTO THE DB
    def get_owned_games(self):
        # sqlite.conn.execute(
        # "SELECT gamename FROM tasks WHERE gamename=?", (priority,))
        list_owned_games = os.popen('legendary list-games')
        output_list_games = list_owned_games.read()
        list_owned_games.close()
        lines = output_list_games.split('\n')
        for line in lines:
            match = re.match(
                fr'^ \* (?P<title>.*) \(App name: (?P<appId>.*) \| Version: (?P<version>.*)\){line}')
            if not match:
                continue
            title = match.group('title')
            app_id = match.group('appId')
            # UNUSED, MAYBE IN THE FUTURE THIS WILL BE USED
            # version = match.group('version')
            sqlitee.cur.execute(
                f"INSERT INTO games(title, app_id) VALUES ({title},{app_id});")
        sqlitee.conn.commit()

    # FUNCTION TO CHANGE GLOBAL RUNNER
    def change_global_runner_func(self):
        file_globalrunner_chosen = askopenfilename()
        sqlitee.cur.execute(
            f"UPDATE games SET runner=({file_globalrunner_chosen}) WHERE title='globalrunner';")
        sqlitee.conn.commit()

    # CHANGE RUNNER FOR A SINGLE GAME
    def change_single_runner(self):
        global toplevel_change_single_game
        global listbox_all_games2
        toplevel_change_single_game = tk.Toplevel()
        toplevel_change_single_game.wm_title("Change runner for specific game")
        button_submit_change_single = tk.Button(
            toplevel_change_single_game,
            text="Submit new runner",
            command=lambda: self.submit_change_single())
        button_submit_change_single.grid(row=0, column=3)

        listbox_all_games2 = tk.Listbox(toplevel_change_single_game)
        listbox_all_games2.grid(row=0, column=1)
        for items in self.title_db:
            listbox_all_games2.insert('end', items[0])

    def submit_change_single(self):
        global listbox_all_games2
        selection_game = listbox_all_games2.get(listbox_all_games2.curselection())
        file_new_single_runner = askopenfilename()
        toplevel_change_single_game.destroy()
        sqlitee.cur.execute("UPDATE games SET runner = ? WHERE title = (?)",
                            (file_new_single_runner, selection_game))
        sqlitee.conn.commit()


root.config(menu=menubar)
root.mainloop()
