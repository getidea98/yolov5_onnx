import win32gui


class Win32guiUtil:

    def __init__(self, title_name='地下城与勇士'):
        self.titleName = title_name
        self.hwnd = win32gui.FindWindow(0, title_name)

    # 获取窗口的位置
    def get_window_pos(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        return left, top, right, bottom

    # 将窗口放到最上层
    def set_foreground_window(self):
        win32gui.SetForegroundWindow(self.hwnd)
