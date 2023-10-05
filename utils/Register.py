### 激活码,因开源已失效


import pyDes
import wmi
import datetime
from utils.IO import *

def registration():
    c = wmi.WMI()
    for board_id in c.Win32_BaseBoard():
        a = board_id.SerialNumber              
    for cpu in c.Win32_Processor():
        b = cpu.ProcessorId.strip()             
    ids = a + b
    need_input = False
    try:    # 读取预留钥密
        with open('./config/key.txt', "r", encoding="utf-8") as file:
            for line in file:
                input_text = line.rstrip()
    except:
        input_text = ""

    print(f"/*****您的机器码如下，复制后请联系作者获取激活码：*****/\n{ids}\n/*****请输入激活码，按回车键结束*****/")
    des_key = pyDes.des(b"q4v5n7g1", pyDes.CBC, b"q4v5n7g1",pad=None, padmode=pyDes.PAD_PKCS5)
    while(1):
        if need_input == False and input_text != "":
            need_input = True
        else:
            input_text = color_input()
        try:
            decrypted_text = des_key.decrypt(bytes.fromhex(input_text))
        except:
            color_print('WARN', '注册码错误，请重新输入')
            continue
        try:
            if decrypted_text.decode() == ids:
                color_print('INFO', '注册成功！欢迎使用')
                with open('./config/key.txt', 'w') as file:
                    file.write(input_text)
                return True
        except:
            color_print('WARN', '注册码错误，请重新输入')
            continue

def registertime():
    current_time = datetime.datetime.now()
    user_datetime = datetime.datetime(2023, 9, 3, 12, 00)
    if current_time < user_datetime:
        color_print('INFO', f'到期时间：{user_datetime}')
        return True
    else:
        color_print('WARN', f'已过期，请联系开发者')
        return False

