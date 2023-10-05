### 因开源，已无效

import wmi
import pyDes


def get_disk_sn():
    """
        获取硬盘序列号
        :return: 硬盘序列号列表
        """
    c = wmi.WMI()

    disk_sn_list = []
    for physical_disk in c.Win32_DiskDrive():
        disk_sn_list.append(physical_disk.SerialNumber.replace(" ", ""))
    return disk_sn_list


def get_baseboard_sn():
    """
        获取主板序列号
        :return: 主板序列号
        """
    c = wmi.WMI()
    for board_id in c.Win32_BaseBoard():
        # print(board_id.SerialNumber)
        return board_id.SerialNumber

def get_cpu_sn():
    """
    获取CPU序列号
    :return: CPU序列号
    """
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        # print(cpu.ProcessorId.strip())
        return cpu.ProcessorId.strip()


# a = get_baseboard_sn() + get_cpu_sn()
print("输入机器号：")
a = input()
k = pyDes.des('q4v5n7g1', pyDes.CBC, 'q4v5n7g1', pad=None, padmode=pyDes.PAD_PKCS5)
data = k.encrypt(a, padmode=pyDes.PAD_PKCS5).hex()
print(data)

des_key = pyDes.des(b"q4v5n7g1", pyDes.CBC, b"q4v5n7g1", pad=None, padmode=pyDes.PAD_PKCS5)
decrypted_text = des_key.decrypt(bytes.fromhex(data))


if str(decrypted_text.decode()) == a:
    print('验证成功')

