import tkinter as tk
import subprocess
import webbrowser
import re
import os
import sqlitee

color_light_black = "#2f2f2f"
color_white = "#ffffff"
color_light_blue = "#63b8ff"


def callback(url):
    webbrowser.open_new(url)


file_loc = '/home/jack/legendary_gui/is_auth_complete.txt'


def topwindow_settings():
    global entry_for_token
    global settings_window
    settings_window = tk.Toplevel()
    settings_window.wm_title("Settings")
    settings_window.configure(bg=color_light_black)
    settings_window.geometry('800x600')

    label_authentication_section = tk.Label(
        settings_window, text="Connect your Epic Games Account", anchor=tk.W, bg=color_light_black, fg=color_white)
    label_authentication_section.grid(row=0, column=0)

    label_text = tk.Label(
        settings_window, text="Paste the token here", anchor=tk.W, bg=color_light_black, fg=color_white)
    label_text.grid(row=1, column=0)
    hyperlink = tk.Label(
        settings_window, text="Click here to get your token", bg=color_light_black, fg=color_light_blue, cursor="hand2", anchor=tk.W)
    hyperlink.grid(row=2, column=0)
    hyperlink.bind(
        "<Button-1>", lambda e: callback("https://www.epicgames.com/id/api/redirect"))

    submit_button = tk.Button(
        settings_window, text="Submit", command=auth_button, bg=color_light_black, anchor=tk.W, fg=color_white)
    submit_button.grid(row=4, column=0)
    entry_for_token = tk.Entry(
        settings_window, bg=color_light_black, fg=color_white)
    entry_for_token.grid(row=3, column=0)
    
    # NEW WAY TO CHECK IF USER IS ALREADY LOGGED IN
    auth_check = os.path.isfile('/home/jack/.config/legendary/user.json')
    if auth_check == True:
        auth_already_complete = tk.Label(
            settings_window, bg=color_light_black, text="You are already connected with your Epic Games Account!", fg=color_white)
        auth_already_complete.grid(row=5, column=0)
    elif auth_check == False:
        auth_not_complete = tk.Label(
            settings_window, text="You are currently not connected to a Epic Games Account!", bg=color_light_black, fg=color_white)
        auth_not_complete.grid(row=5, column=0)


    button_change_runner = tk.Button(
        settings_window, text="Click", command=lambda: change_globalrunner())
    button_change_runner.grid(row=3, column=2)
    label_change_runner = tk.Label(
        settings_window, text="Change the runner")
    label_change_runner.grid(row=2, column=2)


# CHANGE THE CURRENT RUNNER


def auth_button():
    global entry
    global entry_for_token
    global settings_window
    entry = entry_for_token.get()
    settings_window.destroy()
    pattern_auth_token = "(.{32})"
    if(re.search(pattern_auth_token, entry)):
        with subprocess.Popen(['legendary', 'auth'], stdin=subprocess.PIPE, text=True) as popen:
            popen.communicate(str(entry))
        auth_succesfull_toplevel = tk.Toplevel()
        auth_succesfull_label = tk.Label(auth_succesfull_toplevel, text="Successfully logged in!")
        auth_succesfull_label.grid(row=0,column=0)
    else:
        auth_not_succesful = tk.Toplevel()
        auth_not_succesful_label = tk.Label(auth_not_succesful, text="Something went wrong")
        auth_not_succesful_label.grid(row=0,column=0)
        auth_not_succesful_try_again = tk.Button(auth_not_succesful, text="Try Again", command=lambda:topwindow_settings())
        auth_not_succesful_try_again.grid(row=1, column=0)

def change_globalrunner_submit_button_func():
    input_entry_change_globalrunner = entry_change_runner.get()
    print(input_entry_change_globalrunner)
    topwindow_change_runner.destroy()
    data = str(input_entry_change_globalrunner)
    sql_update_query = "UPDATE games WHERE gamename = 'globalrunner' SET runner (?);", (
        data)
    # "INSERT INTO games(gamename, codename) VALUES (?,?);", (title, app_id))

    sqlitee.cur.execute(sql_update_query)
    sqlitee.conn.commit()


def change_globalrunner():
    global entry_change_runner
    global topwindow_change_runner
    topwindow_change_runner = tk.Toplevel(settings_window)
    topwindow_change_runner.configure(bg=color_light_black)
    label_idk = tk.Label(topwindow_change_runner,
                         text="Type in the path of the runner")
    label_idk.grid(row=0, column=0)
    entry_change_runner = tk.Entry(topwindow_change_runner)
    entry_change_runner.grid(row=1, column=0)
    submit_button_change_runner = tk.Button(
        topwindow_change_runner, text="Submit", command=lambda: change_globalrunner_submit_button_func())
    submit_button_change_runner.grid(row=2, column=0)
