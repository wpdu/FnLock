import time
import keyboard
from threading import Thread


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

    def on_press(self, e):
        if self.key_index > len(self.src_keys):
            self.reset()
            return

        src_key = self.src_keys[self.key_index]
        delay = e.time - self.last_time
        if e.name == src_key and not self.is_release:
            if self.key_index == 0 or delay < 0.05: # 非人工操作
                self.last_time = e.time
                self.key_index = self.key_index + 1
                # print(self.key_index)
                if self.is_end():
                    self.is_release = True
                    self.key_index = 0
                    # print('suppress')
                    if self.src_keys[0] == 'left windows':
                        keyboard.press('ctrl')
                    return True
                else:
                    return
        self.reset()

    def on_release(self, e):
        if self.key_index > len(self.src_keys):
            self.reset()
            return

        src_key = self.src_keys[self.key_index]
        delay = e.time - self.last_time
        if e.name == src_key and self.is_release:
            if delay < 0.15:
                self.last_time = e.time
                self.key_index = self.key_index + 1
                # print(self.key_index)
                if self.is_end():
                    # print('suppress')
                    if self.src_keys[0] == 'left windows':
                        keyboard.release('ctrl')
                    self.trigger()
                    self.reset()
                    return True
                else:
                    return
        self.reset()

    def trigger(self):
        for key in self.dst_keys:
            # print(f'trigget {key}')
            keyboard.press(key)
            time.sleep(0.1)
            keyboard.release(key)


key_maps = [
    (['volume mute'], ['f1']),
    (['volume down'], ['f2']),
    (['volume up'], ['f3']),
    (['previous track'], ['f4']),
    (['play/pause media'], ['f5']),
    (['next track'], ['f6']),

    (['shift', 'left windows', 'f21'], ['f9']),
    (['left windows', 'tab'], ['f10']),
    (['ctrl', 'left windows', 'f21'], ['f11']),
    (['left windows', 'f21'], ['f12']),
]

kms = []
for srckeys, dstkeys in key_maps:
    km = KeyboardMapping(srckeys, dstkeys)
    kms.append(km)


def printe(e):
    print(f'{e.event_type} \t {e.name} \t {e.time}')


def press(e):
    '''
    return: True: 不拦截， False: 拦截
    '''
    # printe(e)
    # 只要有一个返回 True, 则说明拦截
    supress = any(km.on_press(e) for km in kms)
    return not supress


def release(e):
    # printe(e)
    supress = any(km.on_release(e) for km in kms)
    return not supress


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
