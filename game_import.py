import tkinter as tk
import subprocess

input_name = """Enter the name of the game you want to import.
                \n(Hint: You can find the names in the game list"""


def topwindow_import_game():
    global topwindow
    global entry_game_name_import
    global entry_game_dir_import
    topwindow = tk.Toplevel()
    topwindow.wm_title("Import a Game")
    topwindow.geometry("600x300")
    label1 = tk.Label(topwindow,
                      text=input_name)
    label1.grid(row=0, column=0)
    entry_game_name_import = tk.Entry(topwindow)
    entry_game_name_import.grid(row=0, column=1)
    label2 = tk.Label(
        topwindow, text="Enter the path where the game is located")
    label2.grid(row=1, column=0)
    entry_game_dir_import = tk.Entry(topwindow)
    entry_game_dir_import.grid(row=1, column=1)
    submit_import_btn = tk.Button(topwindow,
                                  text="Submit",
                                  command=lambda: submit_import())
    submit_import_btn.grid(row=2, column=1)


def submit_import():
    entry1 = entry_game_name_import.get()
    entry2 = entry_game_dir_import.get()
    topwindow.destroy()
    subprocess.Popen(['legendary', 'import-game', entry1, entry2])
