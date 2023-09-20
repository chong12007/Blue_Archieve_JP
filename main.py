import webbrowser

import utils
import PySimpleGUI as sg
from momotalk import momotalk_main
from main_quest import main_quest_main


def display_ui():
    # Set a Layout
    layout = [
        [sg.Text("Stay on the Page then activate", key="row1", text_color="#509296", font=("Helvetica", 14, "bold"),
                 background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2", text_color="#509296",
                 font=("Helvetica", 12, "bold"), background_color="#f0f0f0")],
        [],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],
        [sg.Button("Adjust Screen", key="adjust_screen", button_color="#509296")],
        [sg.Button("Momotalk", key="Momotalk", button_color="#509296")] +
        [sg.Button("Main Quest", key="main_quest", button_color="#509296")],
        [sg.Text("Please leave a star on my github if this script helps you T^T,Click me to github", key="github",
                 enable_events=True, text_color='blue', background_color="#f0f0f0")]
    ]

    # window setting
    window_location = (0, 200)  # Specify the desired coordinates of the window
    window_size = (400, 350)  # Width, Height
    theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(theme)

    window = sg.Window("Blue Archieve JP", layout, location=window_location, keep_on_top=True, size=window_size)

    # Main content
    ui_content(window)

    window.close()



def ui_content(window):

    while True:
        event, values = window.read()
        # if click momotalk
        if event == "Momotalk":
            momotalk_main(window)

        # if click main quest
        if event == "main_quest":
            main_quest_main(window)

        # if click reset
        if event == "adjust_screen":
            window["row1"].update("Adjust Screen...")
            window.refresh()
            utils.adjust_screen(window)
        if event == "github":
            webbrowser.open("https://github.com/chong12007/Blue_Archieve_JP.git")

        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break


if __name__ == '__main__':
    display_ui()
