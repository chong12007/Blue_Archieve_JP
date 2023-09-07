import utils
import PySimpleGUI as sg
import momotalk


def display_ui() :

    # Set a Layout
    layout = [
        [sg.Text("Stay on the Page then activate", key="row1",text_color="#509296",font=("Helvetica", 14, "bold"),background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2",text_color="#509296", font=("Helvetica", 12, "bold"),background_color="#f0f0f0")],
        [],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],
        [sg.Button("Adjust Screen", key="adjust_screen",button_color="#509296")],
        [sg.Button("Momotalk", key="Momotalk",button_color="#509296")] +
        [sg.Button("Main Quest", key="main_Quest",button_color="#509296")]
    ]

    # window setting
    window_location = (0, 200)  # Specify the desired coordinates of the window
    window_size = (400, 300)  # Width, Height
    theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(theme)

    window = sg.Window("Blue Archieve JP", layout, location=window_location, keep_on_top=True, size=window_size)

    # Main content
    ui_content(window)

    window.close()


def ui_content(window) :
    while True:
        event, values = window.read()
        # if click momotalk
        if event == "Momotalk":
            momotalk.momotalk_routine(window)

        # if click main quest
        if event == "main_quest" :
            utils.update_gui_msg("aaa\n",window)

        # if click reset
        if event == "adjust_screen" :
            window["row1"].update("Adjust Screen...")
            window.refresh()
            utils.adjust_screen(window)


        # Close app
        if event == None or event == sg.WINDOW_CLOSED:
            break

display_ui()



