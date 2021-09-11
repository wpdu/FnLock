
import time
import keyboard
from threading import Thread


# 记录录入的按键，esc 结束并返回
# ret = keyboard.record()
# print('\n'.join(ret))

# 自己实现的键盘映射，没想到库中已经实现
class KeyboardMapping(object):
    """
    按键状态机
    """

    def __init__(self, src_keys, dst_keys):
        self.src_keys = src_keys
        self.dst_keys = dst_keys
        self.key_index = 0
        self.last_time = 0
        self.is_release = False
        self.win_press_time = 0

    def is_end(self):
        if self.key_index == len(self.src_keys):
            return True
        else:
            return False

    def reset(self):
        self.key_index = 0
        self.last_time = 0
        self.is_release = False

    def on_press(self, e):
        if self.key_index > len(self.src_keys):
            self.reset()
            return

        src_key = self.src_keys[self.key_index]
        delay = e.time - self.last_time
        if e.name == src_key and not self.is_release:
            if self.key_index == 0 or delay < 0.2:
                self.last_time = e.time
                self.key_index = self.key_index + 1
                # print(self.key_index)
                if self.is_end():
                    self.is_release = True
                    self.key_index = 0
                    # print('suppress')
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
            if delay < 0.2:
                self.last_time = e.time
                self.key_index = self.key_index + 1
                # print(self.key_index)
                if self.is_end():
                    # print('suppress')
                    self.reset()
                    self.trigger()
                    return True
                else:
                    return

        self.reset()

    def trigger(self):
        for key in self.dst_keys:
            print(f'trigget {key}')
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

    # 因以windows开始的快捷键，无法在不影响其他组合键下进行屏蔽，只好放弃
    # 使用f9 替代 f10， 使用 printscreen 替代 f12
    # (['shift', 'left windows', 'f21'], ['f9']),
    (['shift', 'left windows', 'f21'], ['f10']),
    # (['left windows', 'tab'], ['f10']),
    (['ctrl', 'left windows', 'f21'], ['f11']),
    # (['left windows', 'f21'], ['f12']),
    (['print screen'], ['f12']),
]

kms = []
for srckeys, dstkeys in key_maps:
    km = KeyboardMapping(srckeys, dstkeys)
    kms.append(km)


def printe(e):
    print(f'{e.event_type} {e.is_keypad} {e.name} {e.scan_code} {e.time}')


def press(e):
    # 只要有一个返回 True, 则说明拦截
    # True: 不拦截， False: 拦截
    # printe(e)
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

# keyboard.send('shift+left windows+f21')

# keyboard.press('shift')
# keyboard.press('windows')
# keyboard.press('f21')
# time.sleep(0.1)
# keyboard.release('shift')
# keyboard.release('windows')
# keyboard.release('f21')


if __name__ == "__main__":
    remap_keys()
    time.sleep(4)
    remove_remap_keys()
    time.sleep(9999)
