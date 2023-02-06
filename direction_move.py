import time

import directkeys
from directkeys import PressKey, ReleaseKey

direct_dic = directkeys.direct_dic


def move(direct, material=False, action_cache=None, press_delay=0.1, release_delay=0.1):
    if direct == "RIGHT":
        if action_cache is not None:
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
            print("向右移动21")
            action_cache = "RIGHT"
        else:
            PressKey(direct_dic["RIGHT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
            action_cache = "RIGHT"
            print("向右移动30")
        return action_cache

    elif direct == "LEFT":
        if action_cache is not None:
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
            print("向左移动")
        else:
            PressKey(direct_dic["LEFT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
            action_cache = "LEFT"
            print("向左移动")
        return action_cache

    elif direct == "UP":
        if action_cache is not None:
            if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
            else:
                ReleaseKey(direct_dic[action_cache])
            PressKey(direct_dic["UP"])
            action_cache = "UP"
            print("向上移动")
        else:
            PressKey(direct_dic["UP"])
            action_cache = "UP"
            print("向上移动")
        return action_cache

    elif direct == "DOWN":
        if action_cache is not None:
            if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
            else:
                ReleaseKey(direct_dic[action_cache])
            PressKey(direct_dic["DOWN"])
            action_cache = "DOWN"
            print("向下移动108")
        else:
            PressKey(direct_dic["DOWN"])
            action_cache = "DOWN"
            print("向下移动118")
        return action_cache

    elif direct == "RIGHT_UP":
        if action_cache is not None:
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
            print("右上移动")
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
            print("右上移动")
        return action_cache

    elif direct == "RIGHT_DOWN":
        if action_cache is not None:
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
            print("右上移动")
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
            print("右上移动")
        return action_cache

    elif direct == "LEFT_UP":
        if action_cache is not None:
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
            print("左上移动")
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
            # time.sleep(press_delay)
            action_cache = "LEFT_UP"
            print("左上移动")
        return action_cache

    elif direct == "LEFT_DOWN":
        if action_cache is not None:
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
            print("左下移动")
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
            print("左下移动")
        return action_cache
