import time
import keyboard
from threading import Thread
from log_util import logger


# 记录录入的按键，esc 结束并返回
# ret = keyboard.record()
# # print('\n'.join(ret))


class KeyboardMapping(object):
    """
    案件映射工具，自己实现的键盘映射，自带的remap会导致其他快捷键失效
    """

    def __init__(self, src_keys, dst_keys):
        self.src_keys = src_keys
        self.dst_keys = dst_keys
        self.key_index = 0
        self.last_time = 0
        self.is_release = False

    def is_end(self):
        if self.key_index == len(self.src_keys):
            return True
        else:
            return False

    def reset(self):
        self.key_index = 0
        self.last_time = 0
        self.is_release = False
        # print(f'reset {self.dst_keys}')

    def release_reset(self):
        '''如果进入release，且最终没有触发，执行回撤操作'''
        for i in range(self.key_index):
            pass
        self.reset()


    def on_press(self, e):
        if self.key_index > len(self.src_keys):
            self.reset()
            return

        src_key = self.src_keys[self.key_index]
        delay = e.time - self.last_time
        if e.name == src_key and not self.is_release:
            if self.key_index == 0:
                self.last_time = e.time
            self.key_index = self.key_index + 1
            if self.is_end() and (len(self.src_keys) == 1 or delay < 0.1):
                # 组合键被确认按下
                self.is_release = True
                self.key_index = 0
                self.log(f'cancel press {self.src_keys}')
                if self.src_keys[0] == 'left windows':
                    keyboard.press('ctrl')
                return True
            else:
                self.log(f'press {src_key}')
                return
        self.reset()

    def on_release(self, e):
        if not self.is_release:
            self.reset()
            return
        
        if self.key_index > len(self.src_keys):
            self.reset()
            return

        src_key = self.src_keys[self.key_index]
        delay = e.time - self.last_time
        self.key_index = self.key_index + 1
        if self.is_end():
            # if self.src_keys[0] == 'left windows':
            keyboard.release('ctrl')
            
            self.trigger()
            self.reset()
            return True
        else:
            self.log(f'release {src_key}')
            if len(self.src_keys) == 1:
                self.reset()
            if delay > 0.3:
                keyboard.release('left windows')
            return

    def trigger(self):
        for key in self.dst_keys:
            print(f'trigget {key}')
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)

    def log(self, msg):
        logger.debug(f'{self.dst_keys[0]} {msg}')


key_maps = [
    (['volume mute'], ['f1']),
    (['volume down'], ['f2']),
    (['volume up'], ['f3']),
    (['previous track'], ['f4']),
    (['play/pause media'], ['f5']),
    (['next track'], ['f6']),

    # # 组合键场景如果最后一个按键撤回很可能导致
    (['shift', 'left windows', 'f21'], ['f9']),
    (['left windows', 'tab'], ['f10']),
    (['ctrl', 'left windows', 'f21'], ['f11']),
    (['left windows', 'f21'], ['f12']),
]

kms = []
for srckeys, dstkeys in key_maps:
    km = KeyboardMapping(srckeys, dstkeys)
    kms.append(km)


def formate(e):
    return f'{e.event_type} \t {e.name} \t {e.time}'


def press(e):
    '''
    return: True: 不拦截， False: 拦截
    '''
    # logger.info('press: ' + formate(e))
    # return True
    try:
        # 只要有一个返回 True, 则说明拦截
        suppress = any(km.on_press(e) for km in kms)
        return not suppress
    except Exception as ex:
        logger.exception(ex)

def release(e):
    # logger.info('release: '+ formate(e))
    # return True
    try:
        suppress = any(km.on_release(e) for km in kms)
        return not suppress
    except Exception as ex:
        logger.exception(ex)


def remap_keys():
    keyboard.on_press(press, True)
    keyboard.on_release(release, True)


def remove_remap_keys():
    keyboard.unhook_all()


if __name__ == "__main__":
    remap_keys()
    time.sleep(4)
    # remove_remap_keys()
    time.sleep(9999)
