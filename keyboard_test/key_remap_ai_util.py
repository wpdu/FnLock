import keyboard
import time

# Fn+Fx 按键的媒体键码映射到标准 F1-F12
fn_fx_to_standard = {
    -173: 'f1',      # Fn+F1 → F1
    -174: 'f2',      # Fn+F2 → F2
    -175: 'f3',      # Fn+F3 → F3
    -177: 'f4',      # Fn+F4 → F4
    -179: 'f5',      # Fn+F5 → F5
    -176: 'f6',      # Fn+F6 → F6
}

fn_fx_to_standard = {
    32: 'f1',      # Fn+F1 → F1
    46: 'f2',      # Fn+F2 → F2
    48: 'f3',      # Fn+F3 → F3
    16: 'f4',      # Fn+F4 → F4
    34: 'f5',      # Fn+F5 → F5
    25: 'f6',      # Fn+F6 → F6
}
# F7-F8 未找到映射
# F9-F12 的快捷键映射
f_key_to_hotkey = {
    'f9': 'shift+windows+f21',
    'f10': 'windows+tab',
    'f11': 'ctrl+windows+f21',
    'f12': 'windows+f21',
}
# 检测到按键事件: shift (扫描码: 42, 类型: down)
# 检测到按键事件: left windows (扫描码: 91, 类型: down)
# 检测到按键事件: f21 (扫描码: 108, 类型: down)

# 检测到按键事件: left windows (扫描码: 91, 类型: down)
# 检测到按键事件: tab (扫描码: 15, 类型: down)

# 检测到按键事件: ctrl (扫描码: 29, 类型: down)
# 检测到按键事件: left windows (扫描码: 91, 类型: down)
# 检测到按键事件: f21 (扫描码: 108, 类型: down)

# 检测到按键事件: left windows (扫描码: 91, 类型: down)
# 检测到按键事件: f21 (扫描码: 108, 类型: down)

# 用于追踪当前监听的按键钩子
active_hooks = []


def intercept_fn_fx_keys():
    """
    拦截 Fn+Fx 产生的媒体键码，并模拟按下对应的 F1-F12 按键
    """
    def on_media_key(event):
        # 获取按键的扫描码
        scan_code = event.scan_code
        print(f"检测到按键事件: {event.name} (扫描码: {scan_code}, 类型: {event.event_type})")
        # 检查是否是 Fn+Fx 的媒体键码
        if scan_code in fn_fx_to_standard:
            target_key = fn_fx_to_standard[scan_code]
            
            # 防止按键循环触发
            if event.event_type == 'down':
                print(f"拦截到 Fn+{target_key.upper()}，模拟按下 {target_key.upper()}")
                # 模拟按下对应的 F 键
                keyboard.press_and_release(target_key)
            
            # 阻止原始的媒体键事件继续传播
            return False
    
    # 使用 keyboard 的事件监听
    # hook = keyboard.on_release(on_media_key)
    hook = keyboard.on_press(on_media_key)
    active_hooks.append(hook)
    print("已启动 Fn+Fx 拦截")


def remap_f_keys_to_hotkeys():
    """
    将 F9-F12 重映射到自定义快捷键
    """
    for f_key, hotkey in f_key_to_hotkey.items():
        def make_handler(hk):
            def handler():
                print(f"执行快捷键: {hk}")
                keyboard.write(hk, interval=0.1)
            return handler
        
        # 注册 F 键的快捷键处理
        hook = keyboard.on_press_key(f_key, lambda: make_handler(f_key_to_hotkey[f_key])())
        active_hooks.append(hook)
    
    print("已启动 F9-F12 快捷键映射")


def start_fn_lock():
    """
    启动 FnLock 功能
    """
    intercept_fn_fx_keys()
    # remap_f_keys_to_hotkeys()
    print("FnLock 已启动")


def stop_fn_lock():
    """
    停止 FnLock 功能
    """
    for hook in active_hooks:
        keyboard.remove_hotkey(hook)
    active_hooks.clear()
    print("FnLock 已停止")


if __name__ == '__main__':
    start_fn_lock()
    try:
        print("按 Ctrl+C 停止...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_fn_lock()