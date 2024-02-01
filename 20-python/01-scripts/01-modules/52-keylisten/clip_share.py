from time import sleep
from datetime import datetime

import requests as rq
import pyperclip as clip
# from winotify import Notification
from pynput.keyboard import Key, Controller, GlobalHotKeys


keyboard = Controller()


push_url = 'http://127.0.0.1:8050/sharetext'  # 发送
pull_url = 'http://127.0.0.1:8050/readtext'  # 读取

'''
pyperclip: 封装了系统剪贴板调用.
    如 windows 下实际上是 ctypes.windll.user32
        - OpenClipboard/CloseClipboard
        - EmptyClipboard
        - GetClipboardData/SetClipboardData
        - ...
'''
# toast = Notification(
#     app_id="Clip Share",
#     title="Clip Share",
#     msg="Clip Share...",
# )


def notification(msg: str, success: bool):
    print(msg.replace('\n', ' '))
    pass
    # toast.msg = msg
    # toast.show()


def push_clip():
    '''复制并发送剪贴板数据到 web'''
    time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    keyboard.release(Key.alt)
    with keyboard.pressed(Key.ctrl):
        keyboard.press('c')
        keyboard.release('c')
    sleep(0.1)
    data = clip.paste().replace('\r', '')
    try:
        resp = rq.post(push_url, json={'data': data})
        if resp.status_code == 200:
            notification(f"{time} \nPush Success", True)
        else:
            notification(f"{time} \nPush Error", False)
    except Exception as e:
        notification(f"{time} \nPush Error, msg: \n{e}", False)


def pull_paste():
    '''读取 web 数据到剪贴板并直接粘贴'''
    time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    try:
        resp = rq.get(pull_url)
        if resp.status_code == 200 and resp.json().get('data'):
            clip.copy(resp.json().get('data'))
            sleep(0.01)
            keyboard.release(Key.alt)
            with keyboard.pressed(Key.ctrl):
                keyboard.press('v')
                keyboard.release('v')
            notification(f"{time} \nPull Success", True)
        else:
            notification(f"{time} \nPull Error", False)
    except Exception as e:
        notification(f"{time} \nPush Error, msg: \n{e}", False)


def main():
    hotkeys = {
        '<ctrl>+<alt>+c': push_clip,
        '<ctrl>+<alt>+v': pull_paste
    }
    listener = GlobalHotKeys(hotkeys, daemon=True)
    listener.start()

    notification("listening", True)


if __name__ == '__main__':
    main()
    while True:
        sleep(10)
