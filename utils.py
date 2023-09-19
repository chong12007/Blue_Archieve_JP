import time
import pygetwindow as gw
import PySimpleGUI as sg
from pygetwindow import Win32Window
import ctypes
import numpy as np
import pyautogui
import cv2


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


def adjust_screen(window):
    app_found, app_window = detect_app()

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
        time.sleep(1)
        # Move the window to the center of the screen
        app_window.moveTo(screen_center_x, screen_center_y)

        window["row1"].update("Screen Adjusted!!", text_color="#509296", font=("Helvetica", 16, "bold"),
                              background_color="#f0f0f0")
        window["row2"].update("yay d >w< b yay", text_color="#509296", font=("Helvetica", 12, "bold"),
                              background_color="#f0f0f0")
        window.refresh()

    else:
        app_not_found(window)


def app_not_found(window):
    window["row1"].update("Error :(", text_color="red", font=("Helvetica", 16, "bold"), background_color="#f0f0f0")
    window["row2"].update("Unable to detect Emulator", text_color="red", font=("Helvetica", 12, "bold"),
                          background_color="#f0f0f0")
    update_gui_msg("Supported Emulator :\nBluestack(Tested)\nMEmu\nNox\n\n\n", window)
    window.refresh()


def get_screen_resolution():
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    return screen_width, screen_height


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
        return click_coordinate
    else:
        return 0, 0


def get_student_coordinate(icon_path):
    # Find left side
    screenshot = pyautogui.screenshot(region=(910, 430, 50, 350))
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"

    screenshot = cv2.imread(screenshot_path)

    icon = icon_path

    # Load template image
    template = cv2.imread(icon)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.8

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0] + 910, center[1] + 430)

        return click_coordinate


def detect_color():
    # RGB values for the color to detect
    color_to_detect = (255, 131, 153)  # Replace R, G, B with the desired RGB values

    screenshot = pyautogui.screenshot(region=(1035, 430, 450, 330))
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"

    # Load screenshot
    screenshot = cv2.imread(screenshot_path)

    # Convert the image or video frame to RGB format
    screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

    # Calculate the color difference threshold
    color_difference_threshold = 5

    # Create a mask for the specified color using the calculated threshold
    lower_color = np.array([color_to_detect[0] - color_difference_threshold,
                            color_to_detect[1] - color_difference_threshold,
                            color_to_detect[2] - color_difference_threshold])
    upper_color = np.array([color_to_detect[0] + color_difference_threshold,
                            color_to_detect[1] + color_difference_threshold,
                            color_to_detect[2] + color_difference_threshold])
    mask = cv2.inRange(screenshot_rgb, lower_color, upper_color)

    # Find the coordinates of the color within the mask
    non_zero_points = np.nonzero(mask)
    if len(non_zero_points[0]) > 0:

        y, x = non_zero_points[0][0], non_zero_points[1][0]
        x = x + 1035
        y = y + 430

        # if found then get coordinate and set return true
        return x, y, True
    else:
        return 0, 0, False


def scroll_student(click_coordinate):
    pyautogui.doubleClick(click_coordinate[0], click_coordinate[1], button="left")
    time.sleep(2)
    pyautogui.scroll(-200)


msg_history = ''


def update_gui_msg(msg, window):
    global msg_history

    msg_history += msg
    window.Element('_Multiline_').Update(msg_history, font=("Helvetica", 10, "bold"))
    window.refresh()


def update_gui_msg_color(color, window):
    window.Element('_Multiline_').Update(text_color=color)
    window.refresh()


def click(coordinate, msg, window):
    update_gui_msg(msg, window)
    window.refresh()
    pyautogui.click(coordinate[0], coordinate[1], button="left")
    time.sleep(1)


def check_conversation_end():
    # Take a screenshot
    screenshot = pyautogui.screenshot(region=(1000, 430, 450, 390))
    screenshot.save("img/screenshotCompare.png")
    screenshot_path = "img/screenshotCompare.png"

    screenshot1 = cv2.imread(screenshot_path)
    screenshot2 = cv2.imread("img/screenshot1.png")
    # Compare 2 screeshot
    diff = cv2.absdiff(screenshot1, screenshot2)

    # Apply thresholding to the difference image
    threshold = 30  # Adjust the threshold value as needed
    thresholded_diff = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # Convert the thresholded difference image to grayscale
    thresholded_diff_gray = cv2.cvtColor(thresholded_diff, cv2.COLOR_BGR2GRAY)

    # Count the number of non-zero pixels in the grayscale image
    non_zero_pixels = cv2.countNonZero(thresholded_diff_gray)

    # Calculate the percentage of non-zero pixels
    total_pixels = thresholded_diff_gray.shape[0] * thresholded_diff_gray.shape[1]
    similarity_percentage = (non_zero_pixels / total_pixels) * 100

    return similarity_percentage


if __name__ == '__main__':
    screenshot = pyautogui.screenshot(region=(460, 250, 1000, 600))
    screenshot.save("img/screenshot.png")
