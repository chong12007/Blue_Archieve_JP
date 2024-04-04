import time
import utils
import ctypes
import webbrowser
import PySimpleGUI as sg
from momotalk import momotalk_main
from main_quest import main_quest_main
from event_story import event_story_main


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
        [sg.Button("Main Quest", key="main_quest", button_color="#509296")] +
        [sg.Button("Event Story", key="event", button_color="#509296")],
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

            def adjust_screen(window):
                app_found, app_window = utils.detect_app()

                if app_found:
                    # Resize the window
                    app_window.resizeTo(998, 577)

                    # Get Screen Center
                    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
                    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

                    window_width = app_window.width
                    window_height = app_window.height

                    screen_center_x = (screen_width - window_width) // 2
                    screen_center_y = (screen_height - window_height) // 2

                    app_window.activate()

                    # Select app
                    time.sleep(2)
                    # Move the window to the center of the screen
                    app_window.moveTo(screen_center_x, screen_center_y)

                    window["row1"].update("Screen Adjusted!!", text_color="#509296", font=("Helvetica", 16, "bold"),
                                          background_color="#f0f0f0")
                    window["row2"].update("yay d >w< b yay", text_color="#509296", font=("Helvetica", 12, "bold"),
                                          background_color="#f0f0f0")
                    window.refresh()

                else:
                    utils.app_not_found(window)

            adjust_screen(window)

        if event == "github":
            webbrowser.open("https://github.com/chong12007/Blue_Archieve_JP.git")

        if event == "event":
            event_story_main(window)
        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break


if __name__ == '__main__':
    display_ui()
