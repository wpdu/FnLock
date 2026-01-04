import os
import win32gui
import win32con
import win32api
import ctypes
import ctypes.wintypes
# user32 = ctypes.windll.user32

# user32.RegisterHotKey(None, 98, win32con.MOD_WIN, win32con.VK_F9)

import ctypes
from ctypes import wintypes

# 注册原始键盘输入（可能捕获到硬件级事件）
def register_raw_input():
    rid = ctypes.Structure()
    rid.usUsagePage = 0x01
    rid.usUsage = 0x06  # Keyboard
    rid.dwFlags = 0
    rid.hwndTarget = None
    
    ctypes.windll.user32.RegisterRawInputDevices(
        ctypes.byref(rid), 1, ctypes.sizeof(rid)
    )