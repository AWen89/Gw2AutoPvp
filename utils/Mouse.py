### 鼠标后台类
'''
所有的点击都是不包含标题栏的宽度！
'''
from ctypes import windll, byref
from ctypes.wintypes import POINT
import time


class Mouse():
    def __init__(self, hwnd) -> None:
        import sys
        if not windll.shell32.IsUserAnAdmin():
            # 需要和目标窗口同一权限，游戏窗口通常是管理员权限
            # 不是管理员就提权
            windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
        self.handle = hwnd
        self.PostMessageW = windll.user32.PostMessageW
        self.ClientToScreen = windll.user32.ClientToScreen
        self.WM_MOUSEMOVE = 0x0200
        self.WM_LBUTTONDOWN = 0x0201
        self.WM_LBUTTONUP = 0x202
        self.WM_RBUTTONDOWN = 0x0204
        self.WM_RBUTTONUP = 0x0205
        self.WM_MOUSEWHEEL = 0x020A
        self.WHEEL_DELTA = 120

    def move_to(self, x: int, y: int):
        """移动鼠标到坐标（x, y)

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousemove
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(self.handle, self.WM_MOUSEMOVE, wparam, lparam)

    def left_down(self, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(self.handle, self.WM_LBUTTONDOWN, wparam, lparam)

    def left_up(self, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(self.handle, self.WM_LBUTTONUP, wparam, lparam)

    def right_down(self, x: int, y: int):
        """在坐标(x, y)按下鼠标右键

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttondown
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(self.handle, self.WM_RBUTTONDOWN, wparam, lparam)

    def right_up(self, x: int, y: int):
        """在坐标(x, y)放开鼠标右键

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-lbuttonup
        wparam = 0
        lparam = y << 16 | x
        self.PostMessageW(self.handle, self.WM_RBUTTONUP, wparam, lparam)

    def scroll(self, delta: int, x: int, y: int):
        """在坐标(x, y)滚动鼠标滚轮

        Args:
            delta (int): 为正向上滚动，为负向下滚动
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.move_to(x, y)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-mousewheel
        wparam = delta << 16
        p = POINT(x, y)
        self.ClientToScreen(self.handle, byref(p))
        lparam = p.y << 16 | p.x
        self.PostMessageW(self.handle, self.WM_MOUSEWHEEL, wparam, lparam)

    def scroll_up(self, x: int, y: int):
        """在坐标(x, y)向上滚动鼠标滚轮

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.scroll(self.WHEEL_DELTA, x, y)

    def scroll_down(self, x: int, y: int):
        """在坐标(x, y)向下滚动鼠标滚轮

        Args:
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.scroll(-self.WHEEL_DELTA, x, y)

    def check_click_mouse(self, poi, title_h, click_num = 2):
        """涵盖检查数据有效性的点击

        Args:
            x (int): 横坐标
            y (int): 纵坐标
            title_h: 标题栏高度
        """
        if poi == []:
                return False
        else:
            x = int(poi[0].x)
            y = int(poi[0].y - title_h)
            if click_num == 1:    # pvp图标只按一次
                self.left_down(x, y)
                self.left_up(x, y)
            elif click_num == 2:
                self.left_down(x, y)
                self.left_up(x, y)
                self.left_down(x, y)
                self.left_up(x, y)
