### 格式化输出

import time


def color_print(infor, str, debug = 1):
    ''' 输出
    infor: INFO | WARN | DBUG | ERRO
    str  : To show
    debug: For debug
    '''
    if debug ==1 :
        print(f"[{infor}]~[{time.strftime('%H:%M:%S', time.localtime(time.time()))}] {str}")


def color_input():
    ''' 输入
    '''
    print(
        f"[IN<<]~[{time.strftime('%H:%M:%S', time.localtime(time.time()))}] ", end='')
    inp = input()
    return inp
