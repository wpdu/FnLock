import os
import win32gui
import win32con
import win32api
import ctypes
import ctypes.wintypes
user32 = ctypes.windll.user32

user32.RegisterHotKey(None, 98, win32con.MOD_WIN, win32con.VK_F9)

