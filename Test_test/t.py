import pyautogui
import pyperclip
import time

def get_msg():  #内容输入函数
    contents = "讨打 骗你的 不舍得打你 但是呢 你确实"  #空格表示的是下一条短信
    return contents.split(" ")

def send(msg):
    pyperclip.copy(msg)             # 复制需要发送的内容到粘贴板
    pyautogui.hotkey('ctrl', 'v')   # 模拟键盘 ctrl + v 粘贴内容
    pyautogui.press('enter')        # 发送消息

def send_msg(friend):
    pyautogui.hotkey('ctrl', 'alt', 'w')    # Ctrl + alt + w 打开微信
    pyautogui.hotkey('ctrl', 'f')           # 搜索好友v
    vars
    pyperclip.copy(friend)                  # 复制好友昵称到粘贴板
    pyautogui.hotkey('ctrl', 'v')           # 模拟键盘 ctrl + v 粘贴
    time.sleep(1)
    pyautogui.press('enter')                # 回车进入好友消息界面
    # 一条一条发送消息
    while(1):
        for msg in get_msg():
            send(msg)
            time.sleep(3)    # 每条消息间隔 1 秒

if __name__ == '__main__':

    friend_name = "TestLL001"  #对方用户名称：与微信备注保持一致，尽量使用英文
    send_msg(friend_name)
