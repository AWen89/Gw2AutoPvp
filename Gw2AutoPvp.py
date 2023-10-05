### 主函数入口
from utils.FindImgs import*
from utils.Register import*
from utils.IO import*
from utils.InitSet import*
from utils.AutoSkill import*
import utils.config as uconfig
from utils.MoveControl import*
from utils.Points import*
import multiprocessing as mp
import threading
import random
import time

class MainControl():
    def __init__(self) -> None:
        self.keyboard = 0            # 键盘类
        self.mouse = 0               # 鼠标类
        self.memory = 0              # 内存类
        self.gw2_hwnd = 0            # 窗口hwnd
        self.pvp_nums = 0            # pvp场数
        self.autokey_flag = False    # 开启按键脚本
        self.autowalk_flag = False   # 开始自动寻路
        self.dead = 0                # 1 死亡 | 2 活着
        self.skill_plan = []         # 按键方案
        self.is_leader = 0           # 是否队长模式  1 队长 | 2 队员
        self.Qcase = mp.Queue(1)     # 图像检测模式
        self.Qresult = mp.Queue(1)   # 图像检测结果
        self.title_h = 0             # 标题栏高度
        self.is_attacked = False     # 受到攻击
    
    # 获取识图结果(多进程)
    def get_det_result(self, case_str):
        if self.Qresult.full():     # 满了先清空结果
            self.Qresult.get()
        while(1):
            if self.Qcase.empty():
                self.Qcase.put(case_str)    # 空了再加入检测组别
            while(1):
                time.sleep(0.01)    
                if not self.Qresult.empty():
                    return self.Qresult.get()

    # 控制自动寻路以及决策
    def control_walk(self):
        cur_locat = 'reset'  # 当前节点
        continue_walk = 0    # 继续自动寻路标志      0 关闭 | 1 开启
        end_locat_old = '0'  # 历史节点
        mc = MoveControl(self.memory, self.keyboard)
        while(1):
            try:
                if self.autowalk_flag == True:
                    if continue_walk == 0:      # 不继承寻路时，才开启新的节点
                        maping, mapend = self.memory.getMapId()
                        map_points, map_name = readpoints(mapend)     # 地图节点
                        x, y, _, _ = self.memory.getMoveAttribute()
                        if cur_locat == 'reset':   # 只有在家里才读取位置
                            if map_points['红色家'][0] < x < map_points['红色家'][1] and map_points['红色家'][2] < y <map_points['红色家'][3]:
                                cur_locat = '红色'  # 当前位置
                                home_color = '红' # 阵营颜色
                            elif map_points['蓝色家'][0] < x < map_points['蓝色家'][1] and map_points['蓝色家'][2] < y <map_points['蓝色家'][3]:
                                cur_locat = '蓝色'  # 当前位置
                                home_color = '蓝'  # 阵营颜色
                        if cur_locat == 'reset':    # 防止路失败
                            continue
                        # 随机计算终点,当检测失效或己方已占领所有点位等到20s              
                        while(1):   # 随机计算终点，并且防止起点终点重复, 与上一次终点重复
                            end_locat = map_points['顺序'][random.randint(0, len(map_points['顺序'])-1)]
                            if end_locat != cur_locat and end_locat != end_locat_old:
                                end_locat_old = cur_locat
                                break
                        walk_path = cur_locat + '到' + end_locat
                        walk_list = map_points[walk_path]
                        color_print('INFO', f'阵营：{home_color}色 | 自动寻路：{cur_locat} --> {end_locat}')

                    walk_list, x_old, y_old = mc.walk(walk_list, angleErr=30)  # 寻路, 如果暂停则返回剩下的节点
                    if walk_list != True:   # 没寻路完成
                        while(1):   # 
                            time.sleep(0.5)
                            hp, _ = self.memory.gethp()
                            maping, _ = self.memory.getMapId()
                            if hp == 0 or maping == 350:           # 死亡或者结束比赛，恢复默认在家状态
                                cur_locat = 'reset'
                                continue_walk = 0                  # 不再继续上次寻路
                                break
                            elif self.autowalk_flag == True:
                                Px, Py, Pz, Pa = self.memory.getMoveAttribute()
                                if abs(Px - x_old) < 20 and abs(Py - y_old) < 20:
                                    continue_walk = 1              # 复活 继续上次寻路
                                    break

                    elif walk_list == True:     # 寻路到了终点
                        continue_walk = 0       # 不再继续上次寻路
                        for i in range(20):     # 等待20秒站点
                            time.sleep(1)
                            if self.autowalk_flag == False:
                                break
                        cur_locat = end_locat   # 当前节点等于终点
                else:
                    cur_locat = 'reset'
                    time.sleep(0.5)
            except:
                color_print('ERRO', '自动寻路失败!')
                time.sleep(10)
                continue

    # 进图前开始匹配
    def before_game(self):
        self.pvp_nums = self.pvp_nums + 1
        color_print('INFO', f' <{self.gw2_hwnd}> 开始第 <{self.pvp_nums}> 场游戏')
        maping, mapend = self.memory.getMapId()
        while(maping == 350):           
            if self.is_leader == '1':   # 队长模式
                result = self.get_det_result('before_game_1')
                if result['likaipvp'] == []:  # 点击pvp图标的条件
                    self.mouse.check_click_mouse(result['pvp'], self.title_h, 1)
                    time.sleep(0.5)
                self.mouse.check_click_mouse(result['jingji'], self.title_h)    # 先点排位再点匹配
                time.sleep(1)
                self.mouse.check_click_mouse(result['pipei'], self.title_h)     # 匹配
                self.mouse.check_click_mouse(result['jixu'], self.title_h)      # 配置丢失
            elif self.is_leader == '2':  # 队员模式
                result = self.get_det_result('before_game_2')
                self.mouse.check_click_mouse(result['rudui'], self.title_h)  # 加入队伍
                self.mouse.check_click_mouse(result['zhunbei'], self.title_h)  # 确认准备
                self.mouse.check_click_mouse(result['jixu'], self.title_h)  # 放弃比赛点继续
                self.mouse.check_click_mouse(result['jixu'], self.title_h) # 配置不全，继续

            result = self.get_det_result('before_game_3')
            self.mouse.check_click_mouse(result['queren'], self.title_h, 1) # 确认准备
            ### 地图选择
            if result['dituxuanze'] != []:
                self.mouse.left_down(487, 404)
                self.mouse.left_up(487, 404)
                color_print('INFO', '准备进入比赛地图')
            maping, mapend = self.memory.getMapId()

    # 比赛中-进入地图开始比赛
    def middle_game(self):
        self.dead = 3     # 1 死亡 | 2 活着 | 3 开局至位
        maping, mapend = self.memory.getMapId()
        hp_max_old = 999999 # 初始化最大血量
        while(maping != 350):
            maping, mapend = self.memory.getMapId()
            if maping == mapend:    # 已经加载完成地图 执行
                ### 判定死亡状态
                hp, hp_max = self.memory.gethp()
                if hp_max > hp_max_old: # 血量突然变大，倒地
                    self.dead = 1
                    self.is_attacked = uconfig.is_attacked = False
                elif hp_max < hp_max_old and self.dead != 3: # 非游戏开始时,血量突然减少，复活
                    self.dead = 0
                hp_max_old = hp_max
                ### 检测比赛是否结束，并离开比赛
                result = self.get_det_result('middle_game')
                if result['defen'] != []:
                    self.autokey_flag = uconfig.autokey_flag =  False   # 出现得分，停止自动按键
                    self.autowalk_flag = uconfig.autowalk_flag =  False   # 出现得分，停止自动寻路
                    self.is_attacked = uconfig.is_attacked = False
                    while(result['defen'] != []):
                        result = self.get_det_result('middle_game')
                        self.mouse.check_click_mouse(result['likaibisai'], self.title_h)
                    break
                else:
                    if result['dengdai'] != []:   # 有等待了才点准备，防止误触加入队伍
                        # 进图后确认准备, 没有得分的界面再点，防止误触加入队伍
                        self.mouse.check_click_mouse(result['shi'], self.title_h)
                ### 小号出现特长则关闭 \ 关闭首领pvp配置\说明界面
                if result['techang'] or result['guanbi'] != []:
                    self.mouse.check_click_mouse(result['techang'], self.title_h, 1)
                    self.mouse.check_click_mouse(result['guanbi'], self.title_h, 1)
                    time.sleep(0.5)
                ### 游戏进入倒计时，准备自动按键与寻路
                # 游戏刚开始或者是复活了,排除得分遮挡死亡
                # 注意此处只检测了一个auto
                # if not self.autowalk_flag and result['defen'] == []:
                if (self.dead == 3 or self.dead == 0) and not self.autowalk_flag and result['defen'] == []:
                    color_print('INFO', '开始自动按键/寻路策略')
                    self.dead = 0           # 关闭至高位
                    time.sleep(4)     # 复活等待1.5s
                    self.autokey_flag = uconfig.autokey_flag = True
                    self.autowalk_flag = uconfig.autowalk_flag = True
                    self.is_attacked = uconfig.is_attacked = True
                ### 已经死亡，结束自杀按键
                if self.dead == 1 and self.autowalk_flag:
                    color_print('INFO', '结束自动按键/寻路策略')
                    self.autokey_flag = uconfig.autokey_flag = False
                    self.autowalk_flag = uconfig.autowalk_flag = False
                    self.is_attacked = uconfig.is_attacked = False

    # 比赛后-退出地图
    def end_game(self):
        while(1):   # 此while用于比赛后等待过图
            maping, mapend = self.memory.getMapId()
            time.sleep(0.5)
            if mapend == 350:
                color_print('INFO', '\t返回主城成功')
                break

    # 开始pvp
    def begin_pvp(self):
        while(1):
            self.before_game()  # 进图前开始匹配
            self.middle_game()  # 比赛中-进入地图开始比赛
            self.end_game()     # 比赛后-退出地图

    # main
    def script_main(self):
        # registration()                                                        # 软件注册,因开源-已取消注册
        self.gw2_hwnd = get_gw2_window_hwnd()                                   # 选择游戏窗口句柄
        self.is_leader = leader_mode_select()                                   # 选择队长/队员模式
        self.title_h = set_win_locat(self.gw2_hwnd)                             # 设置窗口大小及位置
        self.keyboard, self.mouse, self.memory = init_class(self.gw2_hwnd)      # 类初始化
        self.skill_plan = read_suicide_method()                                 # 按键方案
        detectpic = mp.Process(target=beginshot, args=(self.Qcase, self.Qresult, self.gw2_hwnd))
        detectpic.start()                                                       # 多进程-图像检测
        autowalk = threading.Thread(target=self.control_walk)                   # 多线程-自动寻路
        autowalk.start()
        autokey = threading.Thread(target=autoskill, args=(self.keyboard, self.skill_plan))
        autokey.start()                                                         # 多线程-自动按键
        time.sleep(1.5)                                                         # 等待进程启动
        self.begin_pvp()                                                        # 开启pvp

if __name__ == '__main__':
    T = MainControl()
    T.script_main()
