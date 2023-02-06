import time

import win32api
import win32con


def mouse_click(x, y, delay=0.2):
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 点击游戏菜单
def mouse_click_game_menu(x_base, y_base):
    mouse_click(x_base + 1040, y_base + 740)


# 点击选择角色
def mouse_click_select_role(x_base, y_base):
    mouse_click(x_base + 610, y_base + 530)


# 点击返回城镇
def mouse_click_back_city(x_base, y_base):
    mouse_click(x_base + 770, y_base + 530)
