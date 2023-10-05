### 自动按键

import time
import random
from utils.IO import*
import utils.config as uconfig


def read_suicide_method(path='./config/suicide.txt'):
    skill_plan = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            buf = line.rstrip()
            if "相隔" in buf:
                wait_time = buf.split("\"")[1]
                key_vk = buf.split("\"")[3]
                skill_plan.append([wait_time, key_vk])
    color_print('INFO', '******* 自动按键方案如下：*******')
    for i in skill_plan:
        color_print('INFO', f"***\t相隔{i[0]}秒，\t按下{i[1]}键\t***")
    color_print('WARN', '可修改<config>文件夹下的<suicide.txt>\n')
    return skill_plan


def autoskill(keyb, skill_plan):
    while(1):
        random_t = random.randint(1, 3)
        time.sleep(random_t)
        # time.sleep(1.5)
        if uconfig.autokey_flag:    # 自动按键
            if uconfig.is_attacked == True:
                for i in skill_plan:
                    time.sleep(float(i[0]))
                    keyb.key_down(i[1])
                    time.sleep(0.1)
                    keyb.key_up(i[1])
        else:
            random_t = random.randint(7, 17)
            time.sleep(random_t)
            # 自动跳跃
            # random_t = random.randint(0, 20)
            # if random_t < 2:        # 跳跃
            #     keyb.key_down('space')
            #     keyb.key_up('space')
