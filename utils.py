import cv2
import time
import pyautogui
import pygetwindow as gw

pyautogui.FAILSAFE = False


def detect_app():
    app_titles = ["Bluestack", "Memu", "Nox"]

    # Find the window with a matching title
    app_window = None
    for title in app_titles:
        try:
            app_window = gw.getWindowsWithTitle(title)[0]
            break
        except IndexError:
            pass

    if app_window:
        return True, app_window
    else:
        return False, None


def app_not_found(window):
    window["row1"].update("Error :(", text_color="red", font=("Helvetica", 16, "bold"), background_color="#f0f0f0")
    window["row2"].update("Unable to detect Emulator", text_color="red", font=("Helvetica", 12, "bold"),
                          background_color="#f0f0f0")
    update_gui_msg("Supported Emulator :\nBluestack(Tested)\nMEmu\nNox\n\n\n", window)
    window.refresh()


def take_screenshot():
    screenshot = pyautogui.screenshot(region=(450, 300, 1000, 520))
    screenshot.save("img/screenshot.png")


def get_icon_coordinate(icon_path):
    screenshot = pyautogui.screenshot(region=(1000, 430, 450, 390))
    screenshot.save("img/screenshot1.png")
    screenshot_path = "img/screenshot1.png"
    screenshot = cv2.imread(screenshot_path)

    # Load template image
    template = cv2.imread(icon_path)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.02

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0] + 1000, center[1] + 430)
        return click_coordinate
    else:
        return 0, 0


def get_icon_coordinate_fullscreen(icon_path):
    screenshot = pyautogui.screenshot(region=(460, 250, 1000, 600))
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"
    screenshot = cv2.imread(screenshot_path)

    # Load template image
    template = cv2.imread(icon_path)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.1

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0] + 460, center[1] + 250)
        print(click_coordinate)
        return click_coordinate
    else:
        return 0, 0


msg_history = ''


def update_gui_msg(msg, window):
    global msg_history

    msg_history += msg
    window.Element('_Multiline_').Update(msg_history, font=("Helvetica", 10, "bold"))
    window.refresh()


def click(coordinate, msg, window):
    update_gui_msg(msg, window)
    window.refresh()
    pyautogui.click(coordinate[0], coordinate[1], button="left")
    time.sleep(1)


def check_if_event_end():
    event_end = False
    coordinate = get_icon_coordinate_fullscreen("img/touch_icon.png")
    if coordinate[0] != 0:
        event_end = True
    return event_end, coordinate

if __name__ == '__main__':
    new_icon_coordinate = get_icon_coordinate_fullscreen("img/star.png")
    print(new_icon_coordinate)
    pyautogui.click(new_icon_coordinate)
    # if coordinate is 0 means no new story detected



