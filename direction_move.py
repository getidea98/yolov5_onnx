import time

import directkeys
from directkeys import PressKey, ReleaseKey

direct_dic = directkeys.direct_dic


def move(direct, material=False, action_cache=None, press_delay=0.1, release_delay=0.1):
    if direct == "RIGHT":
        if action_cache != None:
            if action_cache != "RIGHT":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["RIGHT"])
                if not material:
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                action_cache = "RIGHT"
        else:
            PressKey(direct_dic["RIGHT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
            action_cache = "RIGHT"
        return action_cache

    elif direct == "LEFT":
        if action_cache != None:
            if action_cache != "LEFT":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["LEFT"])
                if not material:
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                action_cache = "LEFT"
        else:
            PressKey(direct_dic["LEFT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
            action_cache = "LEFT"
        return action_cache

    elif direct == "UP":
        if action_cache != None:
            if action_cache != "UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["UP"])
                action_cache = "UP"

        else:
            PressKey(direct_dic["UP"])
            action_cache = "UP"
        return action_cache

    elif direct == "DOWN":
        if action_cache != None:
            if action_cache != "DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["DOWN"])
                action_cache = "DOWN"
        else:
            PressKey(direct_dic["DOWN"])
            action_cache = "DOWN"
        return action_cache

    elif direct == "RIGHT_UP":
        if action_cache != None:
            if action_cache != "RIGHT_UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["RIGHT"])
                PressKey(direct_dic["UP"])
                action_cache = "RIGHT_UP"
        else:
            if not material:
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["RIGHT"])
            PressKey(direct_dic["UP"])
            action_cache = "RIGHT_UP"
        return action_cache

    elif direct == "RIGHT_DOWN":
        if action_cache != None:
            if action_cache != "RIGHT_DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["RIGHT"])
                PressKey(direct_dic["DOWN"])
                action_cache = "RIGHT_DOWN"
        else:
            if not material:
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["RIGHT"])
            PressKey(direct_dic["DOWN"])
            action_cache = "RIGHT_DOWN"
        return action_cache

    elif direct == "LEFT_UP":
        if action_cache != None:
            if action_cache != "LEFT_UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["LEFT"])
                PressKey(direct_dic["UP"])
                action_cache = "LEFT_UP"
        else:
            if not material:
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["LEFT"])
            PressKey(direct_dic["UP"])
            action_cache = "LEFT_UP"
        return action_cache

    elif direct == "LEFT_DOWN":
        if action_cache != None:
            if action_cache != "LEFT_DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["LEFT"])
                PressKey(direct_dic["DOWN"])
                action_cache = "LEFT_DOWN"
        else:
            if not material:
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["LEFT"])
            PressKey(direct_dic["DOWN"])
            action_cache = "LEFT_DOWN"
        return action_cache
