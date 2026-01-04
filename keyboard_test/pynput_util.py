# 尝试 pynput 的高级模式
from pynput import keyboard

listener = keyboard.Listener(on_press=on_press)
listener.start()