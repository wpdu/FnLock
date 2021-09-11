import time
import keyboard


key_maps = {
    'f1': -173,
    'f2': -174,
    'f3': -175,
    'f4': -177,
    'f5': -179,
    'f6': -176,
}

hotkey_maps = {
    'f9': 'shift+windows+f21',
    'f10': 'windows+tab',
    'f11': 'ctrl+windows+f21',
    'f12': 'windows+f21',
}


def remap_keys():

    for dst, src in key_maps.items():
        keyboard.remap_key(src, dst)

    for dst, src in hotkey_maps.items():
        keyboard.remap_hotkey(src, dst)


def remove_remap_keys():
    keyboard.unhook_all()
    # keyboard.unhook_all_hotkeys()


# 记录录入的按键，esc 结束并返回
# ret = keyboard.record()
# print('\n'.join(ret))

# 自己实现的键盘映射，没想到库中已经实现
# class KeyboardMapping(object):
#     """
#     按键状态机
#     """

#     def __init__(self, src_keys, dst_keys):
#         self.src_keys = src_keys
#         self.dst_keys = dst_keys
#         self.key_index = 0
#         self.last_time = 0
#         self.is_reverse = False

#     def is_end(self):
#         if self.key_index == len(self.src_keys):
#             return True
#         else:
#             return False

#     def reset(self):
#         self.key_index = 0
#         self.last_time = 0
#         self.is_reverse = False

#     def on_press(self, e):
#         src_key = self.src_keys[self.key_index]
#         delay = e.time - self.last_time
#         if e.name == src_key and not self.is_reverse:
#             if self.key_index == self.last_time or delay < 0.2:
#                 self.last_time = e.time
#                 self.key_index = self.key_index + 1
#                 if self.is_end():
#                     self.is_reverse = True
#                 return True
#         self.reset()

#     def on_release(self, e):
#         src_key = self.src_keys[self.key_index - 1]
#         delay = e.time - self.last_time
#         if e.name == src_key and self.is_reverse:
#             if delay < 0.2:
#                 self.last_time = e.time
#                 self.key_index = self.key_index - 1
#                 if self.key_index != 0:
#                     return True
#                 else:
#                     self.trigger()
#         self.reset()

#     def trigger(self):
#         for key in self.dst_keys:
#             keyboard.press(key)
#             time.sleep(0.1)
#             keyboard.release(key)


# key_maps = [
#     (['volume mute'], ['f1']),
# ]

# kms = []
# for srckeys, dstkeys in key_maps:
#     km = KeyboardMapping(srckeys, dstkeys)
#     kms.append(km)


# def press(e):
#     for km in kms:
#         km.on_press(e)


# def release(e):
#     for km in kms:
#         km.on_release(e)
