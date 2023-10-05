### 路径录制保存与解密解析

from pynput import keyboard
from utils.IO import *
from cryptography.fernet import Fernet
import json

import time

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


def savePois(M, path):
    '''保存节点
    M:        class Memory
    path:     保存到文件
    '''
    pointlist = []
    t1 = time.time()
    xx, yy, zz, Pa = M.getMoveAttribute()
    while(1):
        with keyboard.Events() as event:
            for i in event:
                key_event = i
                break
            key_event = event.get()
            try:
                x, y, z, Pa = M.getMoveAttribute()
                if xx != x and yy != y:
                    if time.time() - t1 > 0.35:
                        color_print('INFO', str([x, y, z]))
                        pointlist.append([x, y, z])
                        t1 = time.time()
                        xx = x
                        yy = y
                        zz = z

                if key_event.key.char == 'q':
                    file = open(path, "w")
                    for i in pointlist:
                        aa = str(i[0]) + ',' + str(i[1])
                        file.write(aa+'\n')
                    file.close()
                    return pointlist
            except:
                pass


def readpoints(mapid):
    '''读取节点
    mapid:     id
    '''
    try:
        fpath = './src/data/' + map_name_id[mapid] + '.json'
        fernet = Fernet(b'KjdPx1gkDdR2J2CKMgfhVfZhhW4NPj9aCGT2ZNZzFmg=')
        with open(fpath, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
        decrypted_dict = json.loads(decrypted_data)
        return decrypted_dict, map_name_id[mapid]
    except:
        color_print('ERRO', '地图解析失败')
        return False
