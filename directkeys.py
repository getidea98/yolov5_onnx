# coding=utf-8
import win32api
import win32con
import ctypes
import time

key_map = {
    "0": 49, "1": 50, "2": 51, "3": 52, "4": 53, "5": 54, "6": 55, "7": 56, "8": 57, "9": 58,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "LEFT": 37, "UP": 38, "RIGHT": 39,
    "DOWN": 40, "CTRL": 17, "ALT": 18, 'F1': 112, "F2": 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 116, 'F7': 118,
    'F8': 119, 'F9': 12, 'F10': 121, 'F11': 122, 'F12': 123, "ESC": 27, "SPACE": 32, "NUM0": 96
}


direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD, 'W': 0x11, 'A': 0x1E, 'S': 0x1F,
              'D': 0x20, 'M': 0x32, 'J': 0x24, 'K': 0x25, 'LSHIFT': 0x2A, 'R': 0x13, 'V': 0x2F, 'Q': 0x10, 'I': 0x17,
              'O': 0x18, 'P': 0x19, 'C': 0x2E, 'F': 0x21, 'ESC': 0x01}


MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def key_down(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, MapVirtualKey(vk_code, 0), 0, 0)  #


def key_up(key):
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def key_press(key, press_time=0.02):
    key_down(key)
    time.sleep(press_time)
    key_up(key)
    time.sleep(press_time)


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
