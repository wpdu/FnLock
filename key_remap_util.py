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
