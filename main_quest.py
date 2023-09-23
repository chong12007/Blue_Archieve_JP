import cv2
import time
import utils
import pyautogui


def routine(window):
    while True:
        def find_new_story():
            # Get the new icon coordinate
            new_icon_coordinate = utils.get_icon_coordinate_fullscreen("img/new_story_icon.png")
            # if coordinate is 0 means no new story detected
            if new_icon_coordinate[0] == 0:
                return 0, 0
            return new_icon_coordinate

        new_icon_coordinate = find_new_story()
        # if new_icon_coordinate is 0 means no new story found

        if new_icon_coordinate[0] != 0:
            def determine_battle_story(new_icon_coordinate):
                # Get new icon coordinate then get a screenshot of entry area
                screenshot_area = (new_icon_coordinate[0] + 295, new_icon_coordinate[1])

                screenshot = pyautogui.screenshot(region=(screenshot_area[0], screenshot_area[1], 60, 20))
                screenshot.save("img/screenshot.png")
                screenshot_path = "img/screenshot.png"
                screenshot = cv2.imread(screenshot_path)
                template = cv2.imread("img/story_battle_icon_jp.png")

                result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

                threshold = 0.3

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                print(min_val)
                if min_val < threshold:
                    return True, screenshot_area
                else:
                    return False, screenshot_area

            # determine if the story require battle
            battle, screenshot_area = determine_battle_story(new_icon_coordinate)

            def story(window, battle, screenshot_area):
                def get_entry_coordinate(screenshot_area):
                    return (screenshot_area[0] + 50, screenshot_area[1] + 30)

                try:
                    coordinate = get_entry_coordinate(screenshot_area)
                    utils.click(coordinate, "New Story Clicked\n", window)

                    coordinate = utils.get_icon_coordinate_fullscreen("img/entry_jp_icon.png")
                    if coordinate[0] != 0:
                        utils.click(coordinate, "Sleep 15 Seconds for animation\n", window)
                        time.sleep(15)

                    coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")
                    if coordinate[0] != 0:
                        utils.click(coordinate, "Display Skip Event\n", window)

                    coordinate = utils.get_icon_coordinate_fullscreen("img/skip_icon.png")
                    if coordinate[0] != 0:
                        utils.click(coordinate, "", window)

                    time.sleep(2)
                    coordinate = utils.get_icon_coordinate("img/ok_icon.png")
                    if coordinate[0] != 0:
                        utils.click(coordinate, "Skip Event\n", window)
                except Exception as e:
                    print(e)
                    story(window, battle, screenshot_area)

                if battle:

                    def battle_routine(window):
                        time.sleep(10)

                        coordinate = utils.get_icon_coordinate("img/engage_icon_jp.png")
                        if coordinate[0] != 0:
                            utils.click(coordinate, "Engage\n", window)

                        # Enter battle
                        utils.update_gui_msg("Sleep 90 Seconds\n", window)
                        time.sleep(90)
                        while True:

                            # Every 45 seconds check if the battle end
                            coordinate = utils.get_icon_coordinate("img/okay_icon.png")

                            if coordinate[0] != 0:
                                utils.click(coordinate, "Battle ended\n", window)
                                utils.update_gui_msg("Sleep 20 Seconds\n", window)
                                time.sleep(20)
                                coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")

                                if coordinate[0] != 0:
                                    coordinate = utils.get_icon_coordinate_fullscreen("img/menu_icon_jp.png")
                                    if coordinate[0] != 0:
                                        utils.click(coordinate, "Display Skip Event\n", window)

                                    coordinate = utils.get_icon_coordinate_fullscreen("img/skip_icon.png")
                                    if coordinate[0] != 0:
                                        utils.click(coordinate, "", window)

                                    time.sleep(2)
                                    coordinate = utils.get_icon_coordinate("img/ok_icon.png")
                                    if coordinate[0] != 0:
                                        utils.click(coordinate, "Skip Event\n", window)
                                    break

                            utils.update_gui_msg("Battle still not ended,Sleep 45 Seconds\n", window)
                            time.sleep(45)

                            event_end, coordinate = utils.check_if_event_end()
                            if event_end:
                                break

                    battle_routine(window)

                time.sleep(10)
                event_end, coordinate = utils.check_if_event_end()

                utils.click(coordinate, "Story ended Sleep 15 second\n", window)
                time.sleep(15)

            # clear the story
            story(window, battle, screenshot_area)
        else:
            utils.update_gui_msg("No new story found\n", window)
            break


def main_quest_main(window):
    app_found, app_window = utils.detect_app()
    if app_found:
        routine(window)
    else:
        utils.app_not_found(window)
