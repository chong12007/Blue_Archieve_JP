import cv2
import time
import utils
import pyautogui


def routine(window):
    while True:
        new_icon_coordinate = find_new_event_story()
        # if new_icon_coordinate is 0 means no new story found
        if new_icon_coordinate[0] == 0:
            utils.update_gui_msg("No new story found\n", window)
            return

        utils.click(new_icon_coordinate, "event found\n", window)
        event_start_coordinate = utils.get_icon_coordinate_fullscreen("img/event_story_start.png")
        utils.click(event_start_coordinate, "event story started\n", window)
        utils.update_gui_msg("Sleep 15 for animation\n", window)
        time.sleep(5)

        try:
            while True:
                utils.update_gui_msg("hello\n",window)
                time.sleep(10)
                isBattle = isBattleEvent()
                isStory = isStoryEvent()
                if isBattle and not isStory:
                    battle_routine(window)
                if isStory and not isBattle:
                    story_routine(window)
                if not isStory and not isStory:
                    time.sleep(2)
                    coordinate = utils.get_icon_coordinate_fullscreen("img/event_story_ok.png")
                    if coordinate[0] != 0:
                        utils.click(coordinate, "Skip Event\n", window)
                    utils.update_gui_msg("Story ended sleep 10\n",window)
                    time.sleep(10)
                    break

        except Exception as e:
            pass


def isBattleEvent():
    coordinate = utils.get_icon_coordinate("img/engage_icon_jp.png")
    if coordinate[0] == 0:
        return False
    return True


def battle_routine(window):
    coordinate = utils.get_icon_coordinate_fullscreen("img/engage_icon_jp.png")
    utils.click(coordinate, "Battle detected\n", window)
    # Enter battle
    utils.update_gui_msg("Sleep 70 Seconds\n", window)
    time.sleep(70)
    while True:
        # Every 45 seconds check if the battle end
        coordinate = utils.get_icon_coordinate_fullscreen("img/okay_icon.png")

        if coordinate[0] != 0:
            utils.click(coordinate, "Battle ended\n", window)
            coordinate = utils.get_icon_coordinate_fullscreen("img/event_story_ok.png")
            utils.click(coordinate,"Sleep 10 Seconds\n", window)
            time.sleep(10)
            break

        utils.update_gui_msg("Battle still not ended,Sleep 20 Seconds\n", window)
        time.sleep(20)




def isStoryEvent():
    coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")
    if coordinate[0] == 0:
        return False
    return True


def story_routine(window):
    coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")
    if coordinate[0] != 0:
        utils.click(coordinate, "Display Skip Event\n", window)

    coordinate = utils.get_icon_coordinate_fullscreen("img/skip_icon.png")
    if coordinate[0] != 0:
        utils.click(coordinate, "", window)
    coordinate = utils.get_icon_coordinate_fullscreen("img/ok_icon.png")
    if coordinate[0] != 0:
        utils.click(coordinate, "Skip Event\n", window)
        time.sleep(5)




def find_new_event_story():
    # Get the new icon coordinate
    new_icon_coordinate = utils.get_icon_coordinate_fullscreen("img/star.png")
    print(new_icon_coordinate)
    # if coordinate is 0 means no new story detected
    if new_icon_coordinate[0] == 0:
        return 0, 0
    new_icon_coordinate = (new_icon_coordinate[0] + 300, new_icon_coordinate[1])
    return new_icon_coordinate


def event_story_main(window):
    app_found, app_window = utils.detect_app()
    if app_found:
        routine(window)
    else:
        utils.app_not_found(window)
