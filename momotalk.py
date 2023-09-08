import pyautogui
import time
import utils

# a list of student coordinate to avoid clicking same student
student_coordinate_list = []


def click_student(window):
    # Get student coordinate
    student_coordinate = utils.get_student_coordinate("img/new_msg_icon.png")

    for stu_coord in student_coordinate_list:
        # if same coordinate in list add y 50
        if student_coordinate[1] == stu_coord[1]:
            student_coordinate = (student_coordinate[0], + student_coordinate[1] + 50)
        # if y exceed 740, scroll down student page and clear the list
        if student_coordinate[1] >= 740:
            utils.scroll_student((student_coordinate[0], student_coordinate[1]))
            student_coordinate_list.clear()
            click_student(window)
            break

    # add clicked student into list to avoid clicking same student
    student_coordinate_list.append(student_coordinate)
    utils.click(student_coordinate, "Clicking Student\n", window)


def relationship_route(coordinate, window):
    utils.update_gui_msg("Relationship_Event detected\n", window)
    utils.click(coordinate, "", window)

    coordinate = utils.get_icon_coordinate("img/relationship_event_entry_icon_jp.png")
    utils.click(coordinate, "Sleep 15 seconds for animation\n", window)

    time.sleep(15)
    utils.update_gui_msg("Display Skip Event", window)
    pyautogui.typewrite(['esc'])

    time.sleep(2)
    coordinate = utils.get_icon_coordinate("img/ok_icon.png")
    utils.click(coordinate, "Skip Event", window)

    time.sleep(3)
    utils.click(coordinate, "", window)


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
        # active bluestack
        window.active_windows()

        # Click student
        click_student(window)

        diff = None
        threshold = 2
        # if no new Msg then go select Student
        while diff is None or diff > threshold:

            utils.take_screenshot()
            # using color to determine is normal msg or relationship event
            coord_x, coord_y, relationship_event = utils.detect_color()
            coordinate = (coord_x, coord_y)

            if relationship_event:
                relationship_route(coordinate, window)

            else:
                reply_msg_route(window)

            # if diff > 2 then read the msg again
            diff = utils.check_conversation_end()
            utils.update_gui_msg("Checking any new Msg...\n", window)

        # diff < 2, consider conversation ended, back to select new student
        time.sleep(5)
        count += 1
        utils.update_gui_msg("Conversation ended...\n\n", window)
