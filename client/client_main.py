# coding: utf-8
# Author: mark
# description: xxxx
# contact:
# tkinter在线可视化工具
# https://www.pytk.net/tkinter-helper/

import tkinter as tk
from tkinter import messagebox
import requests
import os

exe_md5 = "fdafdsaafrtqefqafafdafd"
current_version = '1.0.1'


def remote_md5():
    # 获取服务器上的MD5值
    url = "http://127.0.0.1:5000/check_version"
    r = requests.get(url)
    latest_version = r.json()
    return latest_version['version']


def check_server_status() -> bool:
    """
    检查服务器是否正常运行
    :return: True or False
    """
    url = "http://127.0.0.1:5000/ping"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


class App:
    def __init__(self, master):
        # 设置主窗口
        self.master = master
        self.master.title(f"yibutong_{current_version}.exe")
        self.master.geometry("700x600")
        # 判断远端服务器是否连接成功
        if not check_server_status():
            messagebox.showerror("错误", "程序连接服务器失败，请联系管理员")
            return
        # 获取服务器端最新版本号
        latest_version_url = requests.get("http://127.0.0.1:5000/check_version")
        latest_version = latest_version_url.json()
        # 判断本地版本号和服务器端版本号是否一致
        if latest_version['version'] != self.master.title().split('_')[1].replace('.exe', ''):
            # 如果不一致，则弹出升级提示框
            self.master.title(f"yibutong_{current_version}.exe")
            if messagebox.askyesno("提示", "检测到新版本，是否升级？"):
                self.upgrade1()

        # 添加label
        self.label = tk.Label(self.master, text="欢迎使用客户端")
        # 设置label的字体和大小，并加粗
        self.label.config(font=("Courier", 20, "bold"))
        self.label.pack(pady=10)

        # 添加button
        self.button = tk.Button(self.master, text="升级", command=self.upgrade)
        self.button.pack(pady=10)

        # 添加信息弹出框
        self.text = tk.Text(self.master, width=20, height=20)
        self.text.pack(pady=10)

    def upgrade(self):
        # 手动更新
        self.text.insert(tk.END, "当前已是最新版本\n")

    def upgrade1(self):
        # 实现升级逻辑
        # 1. 向服务器发送请求，获取最新版本号和文件MD5值
        url = "http://127.0.0.1:5000/check_version"
        r = requests.get(url)
        latest_version = r.json()
        # 获取版本是否为空
        if not latest_version['version']:
            self.text.insert(tk.END, "当前已是最新版本\n")
            return
        # 当前的本版本和服务的版本进行比较
        if latest_version['version'] == self.master.title().split('_')[1]:
            self.text.insert(tk.END, "当前已是最新版本\n")
            return
        # 2. 如果版本不一致，则向服务器发送请求，下载最新客户端程序文件
        url = "http://127.0.0.1:5000/download_client"
        r = requests.get(url)
        # 3. 将下载的文件保存到本地
        filename = "yibutong" + "_1.0.2" + '.exe'
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'wb') as f:
            f.write(r.content)
        # 4. 打开新的客户端程序
        os.system(filepath)
        # 5. 关闭当前客户端程序
        self.master.destroy()
        return


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    root.destroy()
