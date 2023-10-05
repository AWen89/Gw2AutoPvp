### 根据坐标自动寻路类

'''
'静风神殿': 875
'巨灵领域': 1305
'凯洛城之战': 549
'炼狱的遗产': 795
'摩羯号的复仇': 1163
'尼菲尔森林': 554
'天空巨锤': 900
'永恒大剧场': 1171
'众灵守望': 894
'末日英雄之战': 1011
'''

import time
from utils.IO import *
import utils.config as uconfig

class MoveControl():
    def __init__(self, OMemory, OKeyboard):
        '''
        Args:
            OMemory: Object Memory
            OKeyboard: Object Keyboard
        '''
        self.Me = OMemory
        self.K = OKeyboard
        self.t_left_key = 'j'
        self.t_rig_key = 'k'
        self.go_ah_key = 'w'

    def turnView(self, angle, direct):
        '''旋转视角
        Args:

            angle: 旋转角度
            direct: 旋转方向, left or right
        '''
        c_time = angle/360*3    # 时间
        if direct == 'left':
            self.K.key_down(self.t_left_key)
            time.sleep(c_time)
            self.K.key_up(self.t_left_key)
            time.sleep(0.03)
        elif direct == 'right':
            self.K.key_down(self.t_rig_key)
            time.sleep(c_time)
            self.K.key_up(self.t_rig_key)
            time.sleep(0.03)

    def walk(self, PoiList, angleErr=50, disErr=3):
        '''自动寻路

        Args:
            PoiList: 节点列表
            angleErr: 允许的角度误差, >0
            disErr: 允许目的点与人物之间的误差
        '''
        for i in range(len(PoiList)):
            TarX = PoiList[i][0]    # 目标点 x
            TarY = PoiList[i][1]    # 目标点 y
            # color_print('DBUG', "Next Point: Id:{z} ({x}, {y})".format(z=i+1, x=TarX, y=TarY), 1)
            while(1):       # 到达点之前一直循环
                if uconfig.autowalk_flag == False:  # 控制中途退出
                    # color_print('INFO', '已结束自动寻路')
                    self.K.key_up(self.go_ah_key) 
                    self.K.key_up(self.t_left_key)  
                    self.K.key_up(self.t_rig_key)
                    Px, Py, Pz, Pa = self.Me.getMoveAttribute()
                    return PoiList[i:], Px, Py

                # while(uconfig.is_attacked):     # 收到攻击时暂停寻路
                #     self.K.key_up(self.go_ah_key)
                #     self.K.key_up(self.t_left_key)
                #     self.K.key_up(self.t_rig_key)
                #     time.sleep(1)

                Px, Py, Pz, Pa = self.Me.getMoveAttribute()
                if ((abs(TarX - Px) <= disErr) and (abs(TarY - Py) <= disErr)):  # 到达点位
                    if i == len(PoiList) - 1:
                        self.K.key_up(self.go_ah_key)  # 弹起 w 前进
                        # color_print('INFO', "已到达寻路终点")
                    break
                TarAngle = self.Me.calAngle(Px, Py, TarX, TarY)     # 与目标点的角度
                abs_ang_ofs = abs(TarAngle - Pa)                    # 绝对值差值
                if abs_ang_ofs <= 180:  # 平角范围内
                    if abs_ang_ofs > angleErr:                      # 角度偏差过大停止前进
                        self.K.key_up(self.go_ah_key)             
                    if TarAngle - Pa < 0:
                        self.turnView(abs_ang_ofs, 'left')
                    else:
                        self.turnView(abs_ang_ofs, 'right')
                else:                   # 平角范围外
                    if TarAngle > Pa:
                        cash = 360-TarAngle+Pa
                        if cash > angleErr:                  # 角度偏差过大停止前进
                            self.K.key_up(self.go_ah_key)
                        self.turnView(cash, 'left')
                    else:
                        cash = 360+TarAngle-Pa
                        if cash > angleErr:                  # 角度偏差过大停止前进
                            self.K.key_up(self.go_ah_key)
                        self.turnView(cash, 'right')
                self.K.key_down(self.go_ah_key)  # 弹起 w 前进
        return True, 0, 0     # 返回已经完成寻路
