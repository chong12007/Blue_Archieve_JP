import cv2
import time
import utils
import pyautogui
import numpy as np

# a list of student coordinate to avoid clicking same student
student_coordinate_list = []


def momotalk_routine(window):
    count = 0

    window["row1"].update(f"Momotalk Cleared : {count}", text_color="#509296", font=("Helvetica", 16, "bold"),
                          background_color="#f0f0f0")
    window["row2"].update("Click the exit on top right to stop", text_color="#509296", font=("Helvetica", 10, "bold"),
                          background_color="#f0f0f0")
    window.refresh()

    # # Keep loop momotalk until quit program
    while True:
        window["row1"].update(f"Momotalk Cleared : {count}", text_color="#509296", font=("Helvetica", 16, "bold"),
                              background_color="#f0f0f0")
        window.refresh()

        def click_student(window):
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

            # Get student coordinate
            student_coordinate = get_student_coordinate("img/new_msg_icon.png")

            for stu_coord in student_coordinate_list:
                # if same coordinate in list add y 50
                if student_coordinate[1] == stu_coord[1]:
                    student_coordinate = (student_coordinate[0], + student_coordinate[1] + 50)
                # if y exceed 740, scroll down student page and clear the list
                if student_coordinate[1] >= 740:
                    def scroll_student(click_coordinate):
                        pyautogui.doubleClick(click_coordinate[0], click_coordinate[1], button="left")
                        time.sleep(2)
                        pyautogui.scroll(-200)

                    scroll_student((student_coordinate[0], student_coordinate[1]))
                    student_coordinate_list.clear()
                    click_student(window)
                    break

            # add clicked student into list to avoid clicking same student
            student_coordinate_list.append(student_coordinate)
            utils.click(student_coordinate, "Clicking Student\n", window)

        # Click student
        click_student(window)

        diff = None
        threshold = 2
        # if no new Msg then go select Student
        while diff is None or diff > threshold:

            utils.take_screenshot()

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

            # using color to determine is normal msg or relationship event
            coord_x, coord_y, relationship_event = detect_color()
            coordinate = (coord_x, coord_y)

            if relationship_event:
                utils.update_gui_msg("Relationship_Event detected\n", window)
                utils.click(coordinate, "", window)

                coordinate = utils.get_icon_coordinate("img/relationship_event_entry_icon_jp.png")
                utils.click(coordinate, "Sleep 15 seconds for animation\n", window)

                time.sleep(15)

                def relationship_route(window):

                    try:
                        coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")
                        if coordinate[0] != 0:
                            utils.click(coordinate, "Display Skip Event\n", window)

                        coordinate = utils.get_icon_coordinate_fullscreen("img/skip_icon.png")
                        if coordinate[0] != 0:
                            utils.click(coordinate, "", window)

                        time.sleep(2)
                        coordinate = utils.get_icon_coordinate("img/ok_icon.png")
                        if coordinate[0] != 0:
                            utils.click(coordinate, "Skip Event", window)

                        time.sleep(3)
                        utils.click(coordinate, "", window)
                    except Exception as e:
                        print(f"error is {e}")
                        relationship_route(window)

                relationship_route(window)

            else:
                def reply_msg_route(window):
                    utils.update_gui_msg("", window)
                    coordinate = utils.get_icon_coordinate("img/reply_icon_jp.png")
                    coordinate = (coordinate[0], coordinate[1] + 30)

                    # if reply button found then click
                    if coordinate != (0, 30):
                        utils.click(coordinate, "Reply Msg\n", window)
                    else:
                        # reply button dont found, wait for msg to run
                        utils.update_gui_msg("No action  found!...\n", window)
                        time.sleep(5)

                reply_msg_route(window)

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

            # if diff > 2 then read the msg again
            diff = check_conversation_end()
            utils.update_gui_msg("Checking any new Msg...\n", window)

        # diff < 2, consider conversation ended, back to select new student
        time.sleep(5)
        count += 1
        utils.update_gui_msg("Conversation ended...\n\n", window)


def momotalk_main(window):
    app_found, app_window = utils.detect_app()
    if app_found:
        momotalk_routine(window)
    else:
        utils.app_not_found(window)
