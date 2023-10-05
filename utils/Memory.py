### 内存类

from pymem import Pymem
from pymem.ptypes import RemotePointer
import math


class Memory():
    def __init__(self, exename):
        self.process_name = Pymem(exename)
        self.process_lp = self.process_name.base_address
        self.Maping_base_adr = 0x2A2172C            # 加载中地图id基址
        self.Mapend_base_adr = 0x25540C0            # 加载完成地图id基址
        self.hp_base_adr = 0x29C3678                # 血量基址
        self.coordinate_base_adr = 0x2A6E600        # 人物坐标基址
        self.face_x_base_adr = 0x2A21798            # 人物x面向基址
        self.face_y_base_adr = 0x2A2179C            # 人物y面向基址

    def getPointerAddress(self, base, offsets):
        '''读取内存

        Args:
            process_name: Gw2-64.exe
            base: Gw2_base_lp + 偏移
            offsets: 多级偏移
            return: 地址
        '''
        remote_pointer = RemotePointer(self.process_name.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(
                    self.process_name.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset
        if len(offsets) == 0:
            return RemotePointer(self.process_name.process_handle, remote_pointer.value)

    def calAngle(self, x1, y1, x2, y2):
        '''计算人物朝向角度

        Args:
            x1: x1
            y1: y1
            x2: x2
            y2: y2
            return: angle (North-0°, 0~360°)
        '''
        if x1 == x2 and y2 >= y1:
            return 0
        if x1 == x2 and y2 < y1:
            return 180
        if y1 == y2 and x1 > x2:
            return 90
        if y1 == y2 and x1 < x2:
            return 270
        k = -(y2-y1)/(x2-x1)
        result = math.atan(k)*57.29577
        if x1 > x2:
            result += 270
        else:
            result += 90
        return result

    def getMapId(self):
        '''获取当前地图id
            return: 加载中，加载完毕
        '''
        try:
            Maping = self.process_name.read_int(
                self.process_lp + self.Maping_base_adr)    # 加载中
            Mapend = self.process_name.read_int(
                self.process_lp + self.Mapend_base_adr)    # 加载完成
            return Maping, Mapend
        except:
            pass

    def gethp(self):
        '''获取当前血量
            return: 当前血量，最大血量
        '''
        try:
            hp = int(self.process_name.read_float(
                self.getPointerAddress(self.process_lp + self.hp_base_adr, [0xB4])))
            hp_max = int(self.process_name.read_float(
                self.getPointerAddress(self.process_lp + self.hp_base_adr, [0xB8])))
            return hp, hp_max
        except:
            pass

    def getMoveAttribute(self):
        '''获取坐标及面向

        Args:
            process_name: ...
            process_lp: Gw2.base_address
            return: x y z angle
        '''
        # 先找两个+30的，然后加第一个最慢+50
        # X : 3, 1  //  Fy: Search-Direct
        P_x = round(self.process_name.read_float(self.getPointerAddress(
            self.process_lp + self.coordinate_base_adr, [0x50, 0x30])), 3)
        P_y = round(self.process_name.read_float(self.getPointerAddress(
            self.process_lp + self.coordinate_base_adr, [0x50, 0x34])), 3)
        P_z = round(self.process_name.read_float(self.getPointerAddress(
            self.process_lp + self.coordinate_base_adr, [0x50, 0x38])), 3)
        Face_x = round(self.process_name.read_float(
            self.process_lp + self.face_x_base_adr), 3)        # 第一个是x
        Face_y = round(self.process_name.read_float(
            self.process_lp + self.face_y_base_adr), 3)        # 第二个是y
        P_a = self.calAngle(0, 0, Face_x, Face_y)
        return P_x, P_y, P_z, P_a


if __name__ == '__main__':
    import win32gui
    import win32process
    import time

    def enum_windows_callback(hwnd, windows_list):
        window_text = win32gui.GetWindowText(hwnd)
        if window_text:
            windows_list.append((hwnd, window_text))

    def get_gw2_window_hwnd():
        windows = []
        gw2_hwnds = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        for hwnd, window_text in windows:   # 选择激战2窗口
            if window_text == "激战2":
                gw2_hwnds.append(hwnd)
        return gw2_hwnds[0]

    hwnd = get_gw2_window_hwnd()
    memory = Memory(win32process.GetWindowThreadProcessId(hwnd)[1])
    while(1):
        time.sleep(0.1)
        print(memory.getMoveAttribute())
        # print(memory.getMapId())
        # print(memory.gethp())
