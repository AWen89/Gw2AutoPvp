### 程序初始化

import win32gui
import ctypes
from utils.IO import *
from utils.Keyboard import*
from utils.Mouse import*
from utils.Memory import*
import win32process

def enum_windows_callback(hwnd, windows_list):
    window_text = win32gui.GetWindowText(hwnd)
    if window_text:
        windows_list.append((hwnd, window_text))

# 选择进程
def get_gw2_window_hwnd():
    windows = []
    gw2_hwnds = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    for hwnd, window_text in windows:   # 选择激战2窗口
        if window_text == "激战2":
            gw2_hwnds.append(hwnd)
    del windows

    if len(gw2_hwnds) == 0:
        color_print('ERRO', '请先打开游戏后，再运行此脚本!!!')
        return 0
    elif len(gw2_hwnds) == 1:
        gw2_hwnd = gw2_hwnds[0]
        color_print('INFO', f"单开游戏，游戏句柄为{gw2_hwnds[0]}")
        return gw2_hwnd
    else:
        color_print('INFO', '请选择需要窗口句柄，输入前面的编号并按回车键结束....')
        for i in range(len(gw2_hwnds)):
            print(f"\t{i+1}. {gw2_hwnds[i]}")
        select_id = int(color_input())
        while(select_id > len(gw2_hwnds)):
            color_print('WARN', '输入有误，请重新选择窗口句柄id...')
            select_id = int(color_input())
        gw2_hwnd = gw2_hwnds[select_id - 1]
        return gw2_hwnd


# 选择模式
def leader_mode_select():
    color_print('INFO', '请选择 队长/队员 模式，单排请选择 队长模式...')
    color_print('INFO', '输入数字 1 或 2 ，按回车键确定')
    color_print('INFO', '\t 1.队长模式')
    color_print('INFO', '\t 2.队员模式')
    while(1):
        is_leader = color_input()
        if is_leader not in ['1', '2']:
            color_print('WARN', '输入有误！请重新输入！')
        else:
            if is_leader == '1':
                color_print('INFO', '\t已选择队长模式！')
                time.sleep(0.5)
            else:
                color_print('INFO', '\t已选择队员模式！')
                time.sleep(0.5)
            return is_leader


# 设置窗口大小
def set_win_locat(hwnd):
    client_rect = win32gui.GetClientRect(hwnd)
    rect_fake = win32gui.GetWindowRect(hwnd)        # 假的rect
    f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    rect = ctypes.wintypes.RECT()                   # 真的rect,不受缩放影响
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    f(ctypes.wintypes.HWND(hwnd), ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS), ctypes.byref(rect), ctypes.sizeof(rect))
    win32gui.MoveWindow(hwnd, rect_fake[0], rect_fake[1], 1260, 850, True)       # 设定窗口位置
    return rect.bottom - rect.top - client_rect[3]  # 返回标题栏高度

# 初始化类
def init_class(hwnd):
    keyboard = Keyboard(hwnd)
    mouse = Mouse(hwnd)
    memory = Memory(win32process.GetWindowThreadProcessId(hwnd)[1])
    return keyboard, mouse, memory
