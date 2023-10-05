### 图像检测

from AiBot import WinBotMain
import random
from utils.IO import *
import os

map_name_id = {
    875: '静风神殿',
    1305: '巨灵领域',
    549: '凯洛城之战',
    795: '炼狱的遗产',
    1163: '摩羯号的复仇',
    554: '尼菲尔森林',
    900: '天空巨锤',
    1171: '永恒大剧场',
    894: '众灵守望',
    1011: '末日英雄之战',
}



class ScreenshotScript(WinBotMain):
    wait_timeout = 0.1
    interval_timeout = 0.1
    log_level = "INFO"
    raise_err = False
    gw2_hwnd = 0
    Qcase = ''
    Qresult = ''

    def script_main(self):  # begin
        while(1):
            dresult = {}            # 结果
            a = self.Qcase.get()
            if a == 'before_game_1':    # 队长模式
                dresult['info'] = 'before_game_1'
                dresult['likaipvp'] = self.find_images(self.gw2_hwnd, './src/likaipvp.png', mode=True, similarity=0.7)
                dresult['pvp'] = self.find_images(self.gw2_hwnd, './src/pvp.png', mode=True, similarity=0.7)
                dresult['jingji'] = self.find_images(self.gw2_hwnd, './src/jingji.png', mode=True, similarity=0.7)
                dresult['pipei'] = self.find_images(self.gw2_hwnd, './src/pipei.png', mode=True, similarity=0.7)
                dresult['jixu'] = self.find_images(self.gw2_hwnd, './src/jixu.png', mode=True, similarity=0.7, region=(0, 0, 535, 660))
                self.Qresult.put(dresult)
            elif a == 'before_game_2':  # 队员模式
                dresult['info'] = 'before_game_2'
                dresult['rudui'] = self.find_images(self.gw2_hwnd, './src/rudui.png', mode=True, similarity=0.7)
                dresult['zhunbei'] = self.find_images(self.gw2_hwnd, './src/zhunbei.png', mode=True, similarity=0.7)
                dresult['jixu'] = self.find_images(self.gw2_hwnd, './src/jixu.png', mode=True, similarity=0.7)
                self.Qresult.put(dresult)
            elif a == 'before_game_3':  # 此while用于进入比赛地图前
                dresult['info'] = 'before_game_3'
                dresult['queren'] = self.find_images(self.gw2_hwnd, './src/queren.png', mode=True, similarity=0.7)
                dresult['dituxuanze'] = self.find_images(self.gw2_hwnd, './src/dituxuanze.png', mode=True, similarity=0.7)
                self.Qresult.put(dresult)
            elif a == 'middle_game':
                dresult['info'] = 'middle_game'
                dresult['guanbi'] = self.find_images(self.gw2_hwnd, './src/guanbi.png', mode=True, similarity=0.9, region=(624,0,1217,817))
                dresult['defen'] = self.find_images(self.gw2_hwnd, './src/defen.png', mode=True, similarity=0.7)
                dresult['likaibisai'] = self.find_images(self.gw2_hwnd, './src/likaibisai.png', mode=True, similarity=0.7)
                dresult['dengdai'] = self.find_images(self.gw2_hwnd, './src/dengdai.png', mode=True, similarity=0.6)
                dresult['shi'] = self.find_images(self.gw2_hwnd, './src/shi.png', mode=True, similarity=0.6)
                dresult['techang'] = self.find_images(self.gw2_hwnd, './src/techang.png', mode=True, similarity=0.7)
                dresult['daojishi'] = self.find_images(self.gw2_hwnd, './src/daojishi.png', mode=True, similarity=0.7)
                self.Qresult.put(dresult)
            elif a in ['875', '1305', '549', '795', '1163', '554', '900', '1171', '894']:
                dresult['info'] = a
                path = 'src/map_icon/' + map_name_id[int(a)] + '/'
                pics = os.listdir(path)
                for i in pics:
                    name = i.split('.')[0]
                    ppath = path + i
                    dresult[name] = self.find_images(self.gw2_hwnd, ppath, mode=True, similarity=0.87)
                color_print("DBUG", f"{dresult}")
                self.Qresult.put(dresult)


def beginshot(Qcase, Qresult, hwnd):
    Sss = ScreenshotScript
    Sss.gw2_hwnd = hwnd
    Sss.Qcase = Qcase
    Sss.Qresult = Qresult
    random_port = random.randint(100, 65000)
    color_print('INFO', f"随机端口号{random_port}")
    Sss.execute(random_port, local=True)


if __name__ == '__main__':
    beginshot(68310, './Temp/1.jpg')
