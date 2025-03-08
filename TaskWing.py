# 学翼 - 智能化学习任务管理工具
# Copyright (C) 2025  TiantianYZJ
# 
# 声明：
# 本程序遵循GPLv3协议：您可以在遵守许可证条款的前提下自由使用、修改和分发。
# 完整授权条款请参见项目根目录下的LICENSE文件。

# 更新日志
Version = "V1.1.1"
CHANGELOG = [
    "V0.0.1-2024.01.19 1、“学翼”正式诞生，具备代办管理功能",
    "V0.0.2-2024.01.19 1、添加【任务进度报告】，生成饼图显示任务完成情况",
    "V0.0.3-2024.01.19 1、用户群体细分，包装为任务管理软件；2、建立数据库，实现重进数据不受影响；3、完成情况使用文字（已完成、未完成）",
    "V0.1.0-2024.01.19 1、UI界面焕新，更加现代化；2、主窗口顶部增加时间显示；3、添加深色模式，自动根据时间切换",
    "V0.1.1-2024.01.19 1、接入WindowsMessage API，实现消息系统层级推送",
    "V0.1.2-2024.01.20 1、增加系统托盘图标，实现后台驻留；2、完成情况改用图标",
    "V0.1.4-2024.01.20 1、增加窗口置顶选项；2、新增【设置】，可手动选择主题、配置开机自启动",
    "V0.2.0-2024.01.21 1、页面布局重新排版，各功能区块界线更明显；2、为所有按钮添加图标；3、丰富系统托盘右键菜单",
    "V0.2.1-2024.01.21 1、适配开发环境与封装环境，解决打包.exe后无法调用外部资源的问题",
    "V0.2.2-2024.01.22 1、优化【统计报告】，数据更丰富、更直观；2、添加【关于程序】页面；3、开机自启动支持一键配置",
    "V0.2.3-2024.01.23 1、更换WindowsMessage API库，解决兼容性问题",
    "V0.2.4-2024.02.11 1、增加【AI智答】功能，接入DeepseekAPI，支持单次询问、自定义API Key等功能",
    "V0.2.5-2024.02.12 1、实现对AImarkdown格式回答的渲染",
    "V0.2.6-2024.02.14 1、新增【更新日志】；2、优化API设置界面布局",
    "V0.2.7-2024.02.14 1、增加启动欢迎提示，同时提醒待完成任务项",
    "V0.2.8-2024.02.15 1、【AI设置】添加【私有API配置教程】；2、【AI智答】支持选择服务提供商",
    "V0.2.9-2024.02.15 1、【学习数据统计】任务状态分布情况细分，更加丰富直观；2、启动欢迎提示增加即将截止、已截止任务提醒",
    "V0.3.0-2024.02.15 1、HTML渲染页面全面适配深色模式",
    "V0.3.1-2024.02.15 1、【AI智答】支持设置回答显示方式；2、【API配置教程】改为用浏览器打开，更美观",
    "V0.3.2-2024.02.15 1、【API配置教程】更换渲染风格，响应式布局",
    "V0.3.3-2024.02.16 1、托盘右键菜单优化，新增【统计报告】选项",
    "V1.0.0-2024.02.16 1、“学翼”1.0.0正式版发布！欢迎体验交流",
    "V1.0.1-2024.02.16 1、优化部分窗口尺寸；2、优化通知提示；3、修复了一些已知BUG",
    "V1.0.2-2024.02.16 1、修复了一些已知BUG",
    "V1.0.3-2024.02.16 1、更换高清图标",
    "V1.0.4-2024.02.20 1、优化【清空】代码逻辑；2、正式确定应用名：中文“学翼”，英文“TaskWing”",
    "V1.0.5-2024.02.22 1、新增【专注】，计入统计报告，助力高效学习；2、重要按钮增加悬停提示；3、【设置】新增【删除所有数据】，并优化操作逻辑",
    "V1.0.6-2024.02.22 1、因Deepseek关闭充值入口，【AI智答】暂停提供该渠道共享API，该渠道私有API不受影响；2、优化【专注】；3、优化【设置】",
    "V1.0.7-2024.02.22 1、优化按钮名称；2、主页面字体调整，更显眼；3、【统计报告】优化数据统计逻辑；4、接入日期选择器控件，选择日期更直观",
    "V1.0.8-2024.02.23 1、主题模式新增【跟随系统】；2、浏览器显示回答支持复杂数学公式；3、【专注】新增音量调节；4、【统计报告】优化防溢出",
    "V1.0.9-2024.02.28 1、新增更新检测，从此更新更方便；2、重新设计关于页面；3、取消悬浮提示框的渐显渐隐效果，杜绝了闪烁BUG",
    "V1.1.0-2024.03.02 1、恢复默认API；2、任务列表支持双击和右键操作；3、优化【AI智答】、【关于】；4、添加【通知管理】；5、支持显示AI思考内容；6、【AI智答】支持添加附件",
    "V1.1.1-2024.03.08 1、修复【AI智答】附件解析bug；2、检测更新时显示更新时间；3、浏览器端AI回答适配更多数学公式",
]

import random
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from time import *
import locale
import sys
import importlib
import os
import pystray
from PIL import Image, ImageTk
from pathlib import Path
import winshell
from win10toast import ToastNotifier
from openai import OpenAI
from tkhtmlview import HTMLLabel
import mistune
import requests
from flask import Flask, render_template
import pygame  
from datetime import timedelta
from tkcalendar import Calendar
import darkdetect
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from docx import Document
from win32com.client import Dispatch

# 音频管理配置
def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return round(volume.GetMasterVolumeLevelScalar() * 100)

def set_system_volume(value):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(int(float(value))/100, None)

# Flask配置
flask_app = Flask(__name__, template_folder='templates', static_folder='static')
flask_app.config['TEMPLATES_AUTO_RELOAD'] = True
current_response_html = ""
users_question = ""

# 添加Flask路由
@flask_app.route('/ai-response')
def show_ai_response():
    return render_template('ai_response.html',
                         user_question=users_question,
                         ai_response=current_response_html,
                         bg_color=judge_theme(1),
                         text_color=judge_theme(2))

@flask_app.route('/tutorial')
def show_tutorial():
    return render_template(
        'tutorial.html',
        bg_color=judge_theme(1),
        text_color=judge_theme(2)
    )

def run_flask_server():
    flask_app.run(port=5000, use_reloader=False)

# 判断时间段
clock = int(strftime("%H"))
def judge_time():
    if (clock >= 0 and clock <= 4):
        timenow = "晚上"
    elif (clock >= 5 and clock <= 9):
        timenow = "早上"
    elif (clock >= 10 and clock <= 11):
        timenow = "上午"
    elif (clock >= 12 and clock <= 14):
        timenow = "中午"
    elif (clock >= 15 and clock <= 17):
        timenow = "下午"
    elif (clock >= 18 and clock <= 24):
        timenow = "晚上"
    
    return timenow

# 定义资源路径函数
def resource_path(relative_path):
    try:
        # PyInstaller打包后的临时目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境下的当前目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# WindowsMessage API
icon_path = os.path.abspath(resource_path("LOGO.ico"))
def sent_notice(t,m):
    c.execute("SELECT enable_notifications FROM notice_settings")
    if c.fetchone()[0]:
        toaster = ToastNotifier()
        toaster.show_toast(
            title=t,
            msg=m,
            icon_path=icon_path,
            duration=1,
            threaded=True
        )

        return 0

# 切换窗口置顶状态
def toggle_topmost():
    is_topmost = topmost_var.get()
    root.attributes('-topmost', is_topmost)

# 设置默认编码为 utf-8
locale.setlocale(locale.LC_CTYPE, 'zh_CN.UTF-8')
importlib.reload(sys)

# 获取用户数据目录
user_data_dir = Path(os.getenv('APPDATA')) / "TaskWing"
user_data_dir.mkdir(exist_ok=True)

# 修改数据库连接路径
db_path = user_data_dir / "TaskWing_data.db"
conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# 创建任务表
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             due_date TEXT,
             rest_days INTEGER,
             completed TEXT NOT NULL DEFAULT ' ')''')
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()
conn.commit()

# 创建任务计数器表
c.execute('''CREATE TABLE IF NOT EXISTS task_counter (
             total_tasks INTEGER DEFAULT 0)''')
conn.commit()

# 初始化计数器
c.execute("SELECT COUNT(*) FROM task_counter")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO task_counter (total_tasks) VALUES (0)")
c.execute("SELECT * FROM task_counter")
task_counter = c.fetchall()
conn.commit()

# 主题设置
c.execute('''CREATE TABLE IF NOT EXISTS theme_settings (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             theme_choice TEXT NOT NULL)''')
c.execute("SELECT * FROM theme_settings")
theme_settings = c.fetchall()
conn.commit()

# AI配置
c.execute('''CREATE TABLE IF NOT EXISTS ai_settings (
             api_key TEXT,
             default_model TEXT,
             provider TEXT,
             display_mode TEXT)''')
# 更新初始化数据
c.execute("SELECT COUNT(*) FROM ai_settings")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO ai_settings (api_key, default_model, provider, display_mode) VALUES ('', 'deepseek-chat', 'Deepseek', 'window')")
ai_settings = c.fetchall()
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS notice_settings (
             enable_notifications INTEGER DEFAULT 1,
             check_updates INTEGER DEFAULT 1)''')
# 更新初始化数据
c.execute("SELECT COUNT(*) FROM notice_settings")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO notice_settings (enable_notifications, check_updates) VALUES (1, 1)")
notice_settings = c.fetchall()
conn.commit()

# 在数据库创建部分新增番茄钟记录表
c.execute('''CREATE TABLE IF NOT EXISTS pomodoro_records (
             total_sessions INTEGER DEFAULT 0,
             total_minutes INTEGER DEFAULT 0)''')
c.execute("SELECT COUNT(*) FROM pomodoro_records")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO pomodoro_records (total_sessions, total_minutes) VALUES (0, 0)")
pomodoro_records = c.fetchall() 
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS api_usage
             (date TEXT PRIMARY KEY, count INTEGER)''')
conn.commit()

# 检查读取的数据
print(tasks, task_counter, theme_settings, notice_settings, ai_settings, pomodoro_records)

# 获取任务总量、已完成数量和待完成数量
def get_num(mode):
    conn.commit()
    c.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE completed='✅'")
    completed_tasks = c.fetchone()[0]
    if(mode == 1):
        return total_tasks
    elif(mode == 2):
        return completed_tasks
    elif(mode == 3):
        return total_tasks - completed_tasks

c.execute("SELECT rest_days, completed FROM tasks")
all_tasks = c.fetchall()

completed = 0
pending = 0
upcoming = 0
expired = 0

for task in all_tasks:
    rest_days, completed_status = task[0], task[1]
    if completed_status == '✅':
        pass
    else:
        if rest_days > 1:
            pass
        elif rest_days >= 0:
            upcoming += 1
        else:
            expired += 1
if (get_num(1) == 0):
    sent_notice(f"{judge_time()}好！", f"你没有任务哦，快去添加吧！")
else:
    if (get_num(3) > 0):
        if (upcoming > 0 and expired > 0):
            sent_notice(f"{judge_time()}好！", f"你有{get_num(3)}个任务待完成，其中{expired}个已截止，{upcoming}个即将到期！")
        elif (expired > 0):
            sent_notice(f"{judge_time()}好！", f"你有{get_num(3)}个任务待完成，其中{expired}个已截止!")
        elif (upcoming > 0):
            sent_notice(f"{judge_time()}好！", f"你有{get_num(3)}个任务待完成，其中{upcoming}个即将到期！")
        else:
            sent_notice(f"{judge_time()}好！", f"你有{get_num(3)}个任务待完成")
    elif (get_num(3) == 0):
        sent_notice(f"{judge_time()}好！", f"你没有待完成的任务")

# 主窗口
root = tk.Tk()
root.title("学翼 - 您的一站式智能化学习平台")
width = 1000
height = 600
root.geometry(f"{width}x{height}")

# 创建一个Frame作为容器
frame = tk.Frame(root)
frame.grid(row=0, column=1, sticky="nsew")

# 设置网格的行和列权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 创建并启动Flask线程
flask_thread = threading.Thread(target=run_flask_server, daemon=True)
flask_thread.start()

# 设置窗口图标
def set_icon():
    icon_image = Image.open(resource_path('LOGO.png'))
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
set_icon()

default_font = tkFont.nametofont("TkDefaultFont")

# 加载主题文件
azure_tcl_path = resource_path("azure.tcl")
root.tk.call("source", azure_tcl_path)

# 检查是否已经存在主题设置
c.execute("SELECT * FROM theme_settings")
theme_settings = c.fetchone()

# 如果没有主题设置，插入默认值
if not theme_settings:
    c.execute("INSERT INTO theme_settings (theme_choice) VALUES ('跟随系统')")
    conn.commit()

# 主题适配判断
def judge_theme(mode):
    global theme
    if theme == "light":
        if mode == 1:
            return "#ffffff"
        elif mode == 2:
            return "black"
    elif theme == "dark":
        if mode == 1:
            return "#333333"
        elif mode == 2:
            return "white"

# 设置主题
def set_theme(theme_choice):
    global theme
    if theme_choice == "浅色模式":
        root.tk.call("set_theme", "light")
        theme = "light"
    elif theme_choice == "深色模式":
        root.tk.call("set_theme", "dark")
        theme = "dark"
    elif theme_choice == "自动切换":
        clock = int(strftime("%H"))
        if ((clock >= 0 and clock <= 4) or (clock >= 21 and clock <= 24)):
            root.tk.call("set_theme", "dark")
            theme = "dark"
        else:
            root.tk.call("set_theme", "light")
            theme = "light"
    elif theme_choice == "跟随系统":
        if darkdetect.theme() == "Dark":
            root.tk.call("set_theme", "dark")
            theme = "dark"
        else:
            root.tk.call("set_theme", "light")
            theme = "light"
        
    # 重新应用表格样式
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Microsoft YaHei', 14))
    style.configure("Treeview",font=('Microsoft YaHei', 12))

    style.configure("Large.TLabelframe.Label", font=('Microsoft YaHei', 12, 'bold'),background=judge_theme(1), foreground=judge_theme(2))

    # 更新数据库中的主题设置
    c.execute("UPDATE theme_settings SET theme_choice=? WHERE id=1", (theme_choice,))
    conn.commit()

c.execute("SELECT theme_choice FROM theme_settings")
current_theme = c.fetchone()[0]
conn.commit()
set_theme(current_theme)

def update_theme():
    c.execute("SELECT theme_choice FROM theme_settings")
    cur_theme = c.fetchone()[0]
    if cur_theme == "跟随系统":
        set_theme(cur_theme)
    conn.commit()

    root.after(100, update_theme)

update_theme()

# Tooltip类
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.after_id = None  # 仅保留延迟定时器
        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.schedule_hide)

    def schedule_show(self, event=None):
        """安排延迟显示"""
        self.cancel_pending()
        self.after_id = self.widget.after(500, self.showtip)

    def schedule_hide(self, event=None):
        """立即隐藏"""
        self.cancel_pending()
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

    def cancel_pending(self):
        """取消待执行操作"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def showtip(self):
        """直接显示提示窗口"""
        if self.tipwindow or not self.text:
            return
        
        # 定位计算
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        # 创建普通窗口
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # 样式配置
        bg_color = judge_theme(1)
        text_color = judge_theme(2)
        label = tk.Label(tw, text=self.text, justify='left',
                        background=bg_color, foreground=text_color,
                        relief='solid', borderwidth=1,
                        font=("Microsoft YaHei", 10))
        label.pack()

    def __del__(self):
        """对象销毁时清理资源"""
        if self.tipwindow:
            self.tipwindow.destroy()


# 更新剩余天数
def update_rest_days():
    current_date = datetime.now().strftime("%Y/%m/%d")
    c.execute("SELECT id, due_date FROM tasks")
    tasks = c.fetchall()
    
    for task in tasks:
        task_id, due_date_str = task
        
        due_date = datetime.strptime(due_date_str, "%Y/%m/%d")
        current_date_obj = datetime.strptime(current_date, "%Y/%m/%d")
        rest_days = (due_date - current_date_obj).days
        c.execute("UPDATE tasks SET rest_days=? WHERE id=?", (rest_days, task_id))
    
    conn.commit()
    root.after(1000, update_rest_days)  # 每秒更新

# 更新时间
def update_time():
    timenow = judge_time()
    stime = strftime("%Y/%m/%d %H:%M:%S")
    def adjust_font_size(event):
        height = event.height
        if height / 2 > 55:
            height = 55 * 2
        elif height / 2 < 15:
            height = 15 * 2
        font_size = int(height / 2.5)
        time_label.config(font=("Microsoft YaHei", font_size))

    if not hasattr(root, 'time_label'):
        time_label = ttk.Label(top_frame, text=f"{timenow}好，现在是{stime}", font=("Microsoft YaHei", 21))
        time_label.place(relx=0.5, rely=0.5, anchor="center")
        root.time_label = time_label
        top_frame.bind("<Configure>", adjust_font_size)
    else:
        root.time_label.config(text=f"{timenow}好，现在是{stime}")
    root.after(1000, update_time)

# 版本检测
def version_judge(parent):
    c.execute("SELECT check_updates FROM notice_settings")
    if not c.fetchone()[0]:
        return
    
    github_api = 'https://api.github.com/repos/tiantianyzj/taskwing/releases/latest'

    res = requests.get(github_api).json()
    get_version = res['name']# 最新版本
    get_log = res['body']# 更新日志
    get_time = res['created_at'][0:10]# 发布时间
    if(Version != get_version):
        if parent == root:
            sent_notice("发现新版本", f"{Version} → {get_version}")
        if messagebox.askokcancel("发现新版本", f"有新版本可用：{Version} → {get_version}\n发布时间：{get_time}\n\n更新内容：\n{get_log}\n\n单击【确定】立即下载", parent=parent):
            sent_notice("下载已开始", "您可以继续正常使用学翼")
            get_down_url = res['assets'][0]['browser_download_url']# 下载链接
            # 创建进度窗口
            progress_window = tk.Toplevel(parent)
            progress_window.title("下载进度")
            progress_window.resizable(False, False)
            progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
            progress_bar.pack(padx=20, pady=20)
            progress_label = ttk.Label(progress_window, text="0%")
            progress_label.pack()

            def download_with_progress():
                try:
                    # 新增带进度条的下载代码
                    r = get_down_url
                    response = requests.get(r, stream=True)
                    file_name = r.split('/')[-1]  # 从URL提取文件名
                    total_size = int(response.headers.get('content-length', 0))
                    
                    # 添加时间计算相关变量
                    start_time = time()
                    last_update = 0  # 用于限制更新频率
                    
                    # 设置下载路径为系统下载文件夹
                    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
                    os.makedirs(download_dir, exist_ok=True)  # 确保文件夹存在

                    file_name = r.split('/')[-1]
                    save_path = os.path.join(download_dir, file_name)  # 完整保存路径

                    with open(save_path, 'wb') as f:  # 修改保存路径
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=1024*128):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress = (downloaded / total_size) * 100

                                # 新增剩余时间计算
                                current_time = time()
                                elapsed = current_time - start_time
                                speed = downloaded / elapsed  # 字节/秒
                                remaining = (total_size - downloaded) / speed if speed > 0 else 0
                                
                                # 每0.2秒更新一次时间显示
                                if current_time - last_update >= 0.2 or progress >= 99.9:
                                    # 格式化时间显示
                                    remaining_str = f"{remaining//60:.0f}分{remaining%60:.0f}秒" if remaining > 60 else f"{remaining:.1f}秒"
                                    progress_label.config(text=f"{progress:.1f}% (剩余 {remaining_str})")
                                    last_update = current_time

                                # 更新进度条
                                progress_bar['value'] = progress
                                # progress_label.config(text=f"{progress:.1f}%")
                                root.update_idletasks()
                                print(f"\r下载进度: {progress:.1f}%", end='')
                    progress_window.destroy()
                    sent_notice("下载完成", "请返回学翼进行下一步操作")
                    if messagebox.showinfo("下载完成", "下载完成！\n单击【确定】以进行安装，本程序将自动退出", parent=parent):
                        os.startfile(save_path)  # 打开下载的文件
                        root.destroy()  # 退出程序
                except Exception as e:
                    if str(e) == "invalid command name \".!toplevel.!label\"":
                        messagebox.showerror("下载错误", "您手动关闭了下载窗口，下载被取消\n若为误触，可前往【设置】—【检查更新】重新运行该检查程序", parent=parent)
                    else:
                        messagebox.showerror("下载错误", f"下载失败，可能是服务器繁忙\n错误信息： {str(e)}", parent=parent)
                    progress_window.destroy()
                
            threading.Thread(target=download_with_progress, daemon=True).start()
    elif(Version == get_version and parent != root):      
        messagebox.showinfo("检查完成", f"当前已是最新版本\n当前版本：{Version}\n发布时间{get_time}\n\n此版本更新内容：\n{get_log}", parent=parent)

# 显示托盘图标
def create_tray_icon():
    image = Image.open(resource_path('LOGO.ico'))

    menu = (
        pystray.MenuItem('主页', on_showing),
        pystray.MenuItem('AI智答', open_ai_assistant_window),
        pystray.MenuItem('统计报告', open_progress_window),
        pystray.MenuItem('设置', open_settings_window),
        pystray.MenuItem('关于应用', open_about_window),
        pystray.MenuItem('退出', on_closing)
    )

    if (get_num(1) == 0):
        icon = pystray.Icon("LOGO", image, f"学翼（没有添加任务）", menu)
    else:
        if (get_num(3) > 0):
            icon = pystray.Icon("LOGO", image, f"学翼（{get_num(3)}个任务待完成）", menu)
        elif (get_num(3)  == 0):
            icon = pystray.Icon("LOGO", image, f"学翼（所有任务已完成）", menu)
        
    return icon

# 更新任务列表
def update_task_list():
    task_list.delete(*task_list.get_children())
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    for task in tasks:
        task_list.insert("", "end", values=task)
    
# 添加任务
def add_task():
    current_date = datetime.now().strftime("%Y/%m/%d")
    name = name_entry.get().strip()
    due_date = date_entry.get().strip()
    
    if not name:
        messagebox.showerror("错误", "任务名称不能为空")
        return
    
    try:
        # 先转换为datetime对象再进行计算
        due_date_obj = datetime.strptime(due_date, "%Y/%m/%d")
        current_date_obj = datetime.strptime(current_date, "%Y/%m/%d")
    except ValueError:
        messagebox.showerror("错误", "日期格式无效，请使用YYYY/MM/DD格式")
        return

    # 计算剩余天数（使用datetime对象）
    rest_days = (due_date_obj - current_date_obj).days

    # 插入任务并更新计数器
    c.execute(
    "INSERT INTO tasks (name, due_date, rest_days, completed) VALUES (?, ?, ?, ' ')",
    (name, due_date, rest_days)
    )
    c.execute("UPDATE task_counter SET total_tasks = total_tasks + 1")
    conn.commit()
    
    # 重新编号任务ID
    c.execute("SELECT id FROM tasks ORDER BY id")
    ids = [row[0] for row in c.fetchall()]
    for i, task_id in enumerate(ids):
        c.execute("UPDATE tasks SET id=? WHERE id=?", (i + 1, task_id))
    conn.commit()

    update_task_list()
    name_entry.delete(0, tk.END)
    sent_notice("您添加了一个任务", name)

# 编辑任务
def edit_task():
    selected = task_list.selection()
    if not selected:
        messagebox.showwarning("警告", "请选择一个任务进行修改。")
        return
    item = task_list.item(selected)
    task_id, name, due_date, rest_days, completed, *extra_values = item['values']
    
    edit_window = tk.Toplevel(root)
    edit_window.title("修改任务")
    edit_window.geometry("500x300")
    edit_window.resizable(False, False)
    
    # 主容器框架
    main_frame = ttk.Frame(edit_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # ========== 任务信息部分 ==========
    info_frame = ttk.LabelFrame(main_frame, text="任务详情", padding=10, style="Large.TLabelframe")
    info_frame.pack(fill="x", pady=5)
    
    # 任务名称
    ttk.Label(info_frame, text="任务名称:").grid(row=0, column=0, sticky="w", padx=5)
    name_entry = ttk.Entry(info_frame, width=40)
    name_entry.bind("<Return>", lambda e: save_changes())
    name_entry.insert(0, name)
    name_entry.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

    # ========== 截止日期部分 ==========
    ttk.Label(info_frame, text="截止日期:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    
    # 创建日期输入框
    date_entry = ttk.Entry(info_frame, width=12, font=('Microsoft YaHei', 9))
    date_entry.insert(0, due_date)  # 使用原日期初始化
    date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=10)
    date_entry.bind("<Return>", lambda e: save_changes())
    
    def set_edit_date():
        def on_date_select():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, cal.get_date())
            top.grab_release()
            top.destroy()
        
        # 解析原始日期
        init_year, init_month, init_day = map(int, due_date.split('/'))
        
        top = tk.Toplevel(edit_window)
        top.title("选择日期")
        top.resizable(False, False)
        top.transient(root)
        top.grab_set()
        cal = Calendar(top, 
                      selectmode='day',
                      year=init_year,
                      month=init_month,
                      day=init_day,
                      date_pattern='y/mm/dd')
        cal.pack(padx=10, pady=10)
        ttk.Button(top, text="确定", command=on_date_select).pack(pady=10)
    
    # 添加日期选择按钮
    ttk.Button(info_frame, text="📅 选择", command=set_edit_date).grid(row=1, column=1, padx=120, pady=10)
    Tooltip(info_frame.winfo_children()[4], "在日历中选择日期")

    # ========== 任务状态部分 ==========
    status_frame = ttk.LabelFrame(main_frame, text="任务状态", padding=10, style="Large.TLabelframe")
    status_frame.pack(fill="x", pady=5)
    
    completed_var = tk.BooleanVar(value=(completed == "✅"))
    ttk.Checkbutton(
        status_frame,
        text="已完成",
        variable=completed_var,
        onvalue=True,
        offvalue=False
    ).pack(side="left", padx=5)

    # ========== 按钮部分 ==========
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=10)

    def save_changes():
        current_date = datetime.now().strftime("%Y/%m/%d")
        new_name = name_entry.get()
        new_status = "✅" if completed_var.get() else " "
        
        new_name = name_entry.get().strip()
        new_date = date_entry.get().strip()
        
        # 验证日期格式
        try:
            datetime.strptime(new_date, "%Y/%m/%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式无效，请使用YYYY/MM/DD格式")
            return
        
        # 计算新剩余天数
        current_date = datetime.now().date()
        due_date_obj = datetime.strptime(new_date, "%Y/%m/%d").date()
        new_rest_days = (due_date_obj - current_date).days

        # 获取原始状态
        c.execute("SELECT completed FROM tasks WHERE id=?", (task_id,))
        current_status = c.fetchone()[0].strip()
        
        if current_status.strip() == '' and new_status == "✅":
            conn.commit()  
            
            total = get_num(1)
            actual_completed = get_num(2)+1
            remaining = get_num(3)-1
            progress = round(actual_completed / total * 100, 2)
            print(total, actual_completed, remaining)

            if remaining == 0:
                sent_notice("完成了所有任务，真厉害！", f"已完成{progress}%，共计{total}个任务")
            else:
                sent_notice("搞定一个任务，太棒了！", f"已完成{progress}%，还有{remaining}个任务待完成")

        # 更新数据库
        try:
            c.execute(
            "UPDATE tasks SET name=?, due_date=?, rest_days=?, completed=? WHERE id=?",
            (new_name, new_date, new_rest_days, new_status, task_id)
            )
            
            conn.commit()
            update_task_list()
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            conn.rollback()

    ttk.Button(
        btn_frame,
        text="💾 保存",
        command=save_changes,
        width=15
    ).pack(side="left", padx=10)
    
    ttk.Button(
        btn_frame,
        text="↩️ 取消",
        command=edit_window.destroy,
        width=10
    ).pack(side="right", padx=10)

    edit_window.transient(root)
    edit_window.grab_set()

# 复制并粘贴任务
def copy_and_paste_task():
    selected = task_list.selection()
    if selected:
        task_id = task_list.item(selected[0], "values")[0]
        # 获取原始任务数据
        c.execute("SELECT name, due_date, rest_days, completed FROM tasks WHERE id=?", (task_id,))
        original = c.fetchone()
        
        if original:
            try:
                new_name = f"{original[0]}（副本）" 
                c.execute("INSERT INTO tasks (name, due_date, rest_days, completed) VALUES (?, ?, ?, ?)",
                        (new_name, original[1], original[2], original[3]))
                
                # 重新编号任务ID
                c.execute("SELECT id FROM tasks ORDER BY id")
                ids = [row[0] for row in c.fetchall()]
                for i, task_id in enumerate(ids):
                    c.execute("UPDATE tasks SET id=? WHERE id=?", (i + 1, task_id))
                conn.commit()

                update_task_list()
                sent_notice("您创建了一个任务副本", new_name)
            except Exception as e:
                messagebox.showerror("错误", f"复制失败\n错误信息：{str(e)}")

# 删除任务
def delete_task():
    selected = task_list.selection()
    if not selected:
        messagebox.showwarning("警告", "请选择一个任务进行删除。")
        return
    item = task_list.item(selected)
    task_id = item['values'][0]
    
    # 删除关联统计记录
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

    # 重新编号
    c.execute("SELECT id FROM tasks ORDER BY id")
    ids = [row[0] for row in c.fetchall()]
    for i, task_id in enumerate(ids):
        c.execute("UPDATE tasks SET id=? WHERE id=?", (i + 1, task_id))
    conn.commit()

    update_task_list()
    sent_notice("您删除了一个任务",f"目前还有{get_num(1)}个任务，{get_num(3)}个待完成")

# 确认清空任务列表的函数
def confirm_clear_tasks():
    if messagebox.askokcancel("确认", "确定要清空任务列表吗？此操作不可恢复"):
        c.execute("DELETE FROM tasks")
        conn.commit()
        update_task_list()
        sent_notice("您清空了任务列表","任务列表清空成功")

def pomodoro_set_tasks():
    # 获取选中的任务
    selected = task_list.selection()
    if not selected:
        messagebox.showwarning("提示", "请先选择一个任务", parent=root)
        return
    
    # 获取实际任务ID
    item = task_list.item(selected)
    task_id = item['values'][0]
    task_name = item['values'][1]
    task_due = item['values'][2]
    task_rest = item['values'][3]

    # 创建设置窗口
    setup_win = tk.Toplevel(root)
    setup_win.title("番茄钟设置")
    setup_win.geometry("600x700")  # 增加窗口高度
    setup_win.resizable(False, False)
    setup_win.transient(root)
    setup_win.grab_set()
    
    # ========== 主容器 ==========
    main_frame = ttk.Frame(setup_win)
    main_frame.pack(fill='both', expand=True, padx=20, pady=15)
    
    # ========== 设置区域 ==========
    setup_frame = ttk.Frame(main_frame)
    setup_frame.pack(fill='x', pady=10)
    
    # 标题和输入框
    header = ttk.Label(setup_frame, 
                      text="🍅 番茄钟设置",
                      font=('Microsoft YaHei', 16, 'bold'),
                      foreground='#4fb9fe')
    header.pack(pady=5)

    info_frame = ttk.LabelFrame(setup_frame, text="任务信息", style="Large.TLabelframe", padding=15)
    info_frame.pack(fill='both', expand=True, pady=10)

    ttk.Label(info_frame, 
             text=f"""当前任务：{task_name}
截止日期：{task_due}
剩余天数：{task_rest}""", 
             font=('Microsoft YaHei', 12),
             justify='left').grid(row=0, column=0, padx=5)

    input_frame = ttk.LabelFrame(setup_frame, text="时长设置", style="Large.TLabelframe", padding=15)
    input_frame.pack(fill='both', expand=True, pady=10)
    
    ttk.Label(input_frame, 
             text="专注时长:", 
             font=('Microsoft YaHei', 12)).grid(row=0, column=0, padx=5)
    
    time_var = tk.StringVar(value="25")
    duration_combo = ttk.Combobox(
        input_frame,
        textvariable=time_var,
        values=["5", "10", "15", "20", "25", "30", "45", "60", "90", "120", 
               "150", "180", "210", "240", "270", "300", "330", "360", "390", 
               "420", "450", "480", "510", "540", "570", "600"],
        state="readonly",
        font=('Microsoft YaHei', 11),
        width=8
    )
    duration_combo.grid(row=0, column=1, padx=10)

    ttk.Label(input_frame, 
             text="分钟", 
             font=('Microsoft YaHei', 12)).grid(row=0, column=2, padx=5)
    
    # ========== 说明区域 ==========
    desc_frame = ttk.LabelFrame(main_frame, 
                              text="方法说明", 
                              padding=15,
                              style="Large.TLabelframe")
    desc_frame.pack(fill='both', expand=True, pady=10)
    
    desc_text = """• 推荐使用方式：
  1、选择25分钟专注单元
  2、专注期间不处理其他事务
  3、完成后休息5分钟
  4、每完成4个番茄钟休息15-30分钟

• 注意事项：
  1、遇到打断需重新开始计时
  2、休息时间不要使用电子设备"""
    
    ttk.Label(desc_frame, 
             text=desc_text,
             font=('Microsoft YaHei', 10),
             foreground='#7f8c8d',
             justify='left').pack(anchor='w')
    
    # ========== 按钮区域 ==========
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=15)
    
    def start_pomodoro():
        setup_win.destroy()
        show_pomodoro_interface(int(time_var.get()), task_id)

    start_btn = ttk.Button(
        btn_frame,
        text="⌛️ 开始专注",
        command=lambda:start_pomodoro(),
        width=15,
        style="Accent.TButton"
    )
    start_btn.pack(pady=5)
    
    # 添加样式配置
    style = ttk.Style()
    style.configure("Accent.TButton", 
                   foreground='white',
                   background='#3498db',
                   font=('Microsoft YaHei', 12))

    setup_win.bind("<Return>", lambda e: start_pomodoro())

def show_pomodoro_interface(duration, task_id):
    # 获取任务详情
    c.execute("SELECT name, due_date, rest_days FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    
    # 创建主窗口
    pomo_win = tk.Toplevel(root)
    pomo_win.title(f"番茄钟 - {task[0]}")
    pomo_win.geometry("800x800")
    
    main_frame = ttk.Frame(pomo_win)
    main_frame.pack(fill='both', expand=True)

    # 一言显示区域
    try:
        yiyan = requests.get("https://v1.hitokoto.cn/?c=k").json()
        yiyan_text = f"『{yiyan['hitokoto']}』 —— {yiyan['from']}"
    except:
        yiyan_text = "『学如逆水行舟，不进则退』 —— 《增广贤文》"
    
    yiyan_label = ttk.Label(
        main_frame,
        text=yiyan_text,
        font=('华文魏体', 14, 'italic'),
        wraplength=1300,
        justify='left'
    )
    yiyan_label.pack(pady=20)

    # 分隔线
    ttk.Separator(main_frame).pack(fill='x', pady=10, padx=30)
    
    # 任务信息显示
    task_frame = ttk.Frame(main_frame)
    task_frame.pack(pady=10)
    
    task_label1 = ttk.Label(task_frame, text=f"您当前正在进行的任务是【{task[0]}】", font=('微软雅黑', 12), justify='center')
    task_label1.grid(row=0, column=0)
    task_label2 = ttk.Label(task_frame, text=f"任务将于 {task[1]} 截止，剩余{task[2]}天", font=('微软雅黑', 8), justify='center')
    task_label2.grid(row=1, column=0)
    
    # 计时器显示
    time_label = ttk.Label(
        main_frame,
        text="⏱正计时\n00:00:00",
        font=('Consolas', 40),
        anchor='center'  # 添加居中对齐
    )
    time_label.pack(pady=20, fill='both', expand=True)
    
    # 时间进度显示
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)
    time_info = ttk.Label(
        main_frame,
        text=f"{start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}",
        font=('微软雅黑', 8)
    )
    time_info.pack()
    
    # 计算字体增量
    add_size = 0
    def update_font_size(event=None):
        nonlocal add_size
        pomo_win.update_idletasks()
        win_height = pomo_win.winfo_height()
        
        add_size = int(win_height / 70)
        # 更新所有字体设置
        yiyan_label.config(font=('华文魏体', 13+add_size, 'italic'))
        task_label1.config(font=('微软雅黑', 10+add_size))
        task_label2.config(font=('微软雅黑', 8+add_size))
        time_label.config(font=('Consolas', 40+add_size))
        time_info.config(font=('微软雅黑', 10+add_size))

    # 初始化设置
    pomo_win.bind("<Configure>", update_font_size)
    update_font_size()

    # 分隔线
    ttk.Separator(main_frame).pack(fill='x', pady=10, padx=30)

    # 音频控制部分
    audio_frame = ttk.LabelFrame(main_frame, text="音频设置", style="Large.TLabelframe")
    audio_frame.pack(pady=15, padx=20, anchor='center', ipadx=5, ipady=5)
    
    # 白噪音选择
    pygame.mixer.init()
    sounds = {
        "散步时刻": "sound/relaxing_walk.mp3",
        "溪边蛙鸣": "sound/frogs.mp3",
        "星辰露营": "sound/camping.mp3",
        "营火柴声": "sound/campfire.mp3",
        "雨后天晴": "sound/after_rain.mp3",
        "大雨滂沱": "sound/heavy_rain.mp3",
        "自然水流": "sound/stream.mp3",
        "迷雾森林": "sound/foggy_forest.mp3"
    }
    
    sound_var = tk.StringVar()
    ttk.Label(audio_frame, text="选择环境音效：").grid(row=0, column=0, padx=5, pady=5)
    sound_combo = ttk.Combobox(
        audio_frame,
        textvariable=sound_var,
        values=list(sounds.keys()),
        state="readonly",
        width=18
    )
    sound_combo.grid(row=0, column=1, padx=5, pady=5)
    
    # 控制按钮
    def play_sound():
        if sound_var.get():
            pygame.mixer.music.load(resource_path(sounds[sound_var.get()]))
            pygame.mixer.music.play(-1)
    
    
    paused = [False]
    
    play_btn = ttk.Button(audio_frame, text="▶️ 播放", width=10)
    play_btn.grid(row=0, column=2, padx=5)
    
    # 修改后的播放控制逻辑
    def toggle_play():
        if not pygame.mixer.music.get_busy() or paused[0]:
            play_sound()
            play_btn.config(text="⏸ 暂停")
            paused[0] = False
        else:
            pygame.mixer.music.pause()
            play_btn.config(text="▶️ 继续")
            paused[0] = True
    
    play_btn.config(command=toggle_play)

    # 新增音量控制组件
    ttk.Label(audio_frame, text="系统音量:").grid(row=1, column=0, padx=5, pady=5)
    volume_scale = ttk.Scale(
        audio_frame,
        from_=0,
        to=100,
        value=get_current_volume(),
        command=lambda v: [  # 添加实时更新逻辑
            set_system_volume(v),
            volume_percent.config(text=f"{int(float(v))}%")
        ]
    )
    volume_scale.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
    
    # 新增实时百分比标签
    volume_percent = ttk.Label(audio_frame, text=f"{int(volume_scale.get())}%")
    volume_percent.grid(row=1, column=2, padx=2)
    
    ai_frame = ttk.LabelFrame(main_frame, text="学习辅助", style="Large.TLabelframe")
    ai_frame.pack(pady=15, padx=20, anchor='center', ipadx=10, ipady=5)
    ttk.Button(
        ai_frame,
        text="🤖 AI智答",
        command=lambda:open_ai_assistant(pomo_win)
    ).pack()
    Tooltip(ai_frame.winfo_children()[0], "专注期间的私人助手")
    
    # 控制面板
    ctrl_frame = ttk.Frame(main_frame)
    ctrl_frame.pack(side='bottom', fill='x', pady=10)
    
    def toggle_pause():
        running[0] = not running[0]
        if running[0]:
            pause_button.config(text="⏸ 暂停")
            update_timer()  # 恢复时重新启动计时
        else:
            pause_button.config(text="▶️ 继续")

    # 窗口置顶选项
    topmost_var = tk.IntVar(value=0)
    def toggle_topmost():
        pomo_win.attributes('-topmost', topmost_var.get())
    topmost_check = ttk.Checkbutton(
        ctrl_frame,
        text="窗口置顶",
        variable=topmost_var,
        command=toggle_topmost
    )
    topmost_check.pack(side='left', padx=20)
    
    # 初始化窗口置顶状态
    topmost_var.set(False)
    toggle_topmost()

    # 计时逻辑
    elapsed = [0]  # 使用列表实现闭包效果
    running = [True]
    
    def update_timer():
        # 先检查时间条件，再检查运行状态
        if elapsed[0] < duration * 60:
            if running[0]:  # 只有运行状态为True时才更新
                elapsed[0] += 1
                m, s = divmod(elapsed[0], 60)
                h, m = divmod(m, 60)
                time_label.config(text=f"⏱正计时\n{h:02d}:{m:02d}:{s:02d}")
                pomo_win.after(1000, update_timer)
            else:  # 运行状态被设为False时直接返回
                return
        else:
            finish_pomodoro(True)  # 仅当自然结束时触发
    
    def finish_pomodoro(natural_end):
        running[0] = False  # 立即停止计时器
        pygame.mixer.music.stop()

        should_proceed = True
        # 仅当非自然结束需要确认
        if not natural_end:
            should_proceed = messagebox.askyesno(
                "退出提示",
                "计时尚未完成，确定要提前结束吗？\n（建议坚持完成当前番茄钟）",
                icon='warning',
                parent=pomo_win
            )

        if should_proceed:
            if messagebox.askyesno(
                "计时结束", 
                f"是否已经完成任务【{task[0]}】？",
                parent=pomo_win
            ):
                # 获取原始状态
                c.execute("SELECT completed FROM tasks WHERE id=?", (task_id,))
                current_status = c.fetchone()[0].strip()
                
                if current_status.strip() == '':
                    conn.commit()  
                    
                    total = get_num(1)
                    actual_completed = get_num(2)+1
                    remaining = get_num(3)-1
                    progress = round(actual_completed / total * 100, 2)
                    print(total, actual_completed, remaining)

                    if remaining == 0:
                        sent_notice("完成了所有任务，真厉害！", f"已完成{progress}%，共计{total}个任务")
                    else:
                        sent_notice("搞定一个任务，太棒了！", f"已完成{progress}%，还有{remaining}个任务待完成")

                # 更新任务状态
                c.execute("UPDATE tasks SET completed='✅' WHERE id=?", (task_id,))
                conn.commit()
                update_task_list()

            # 更新番茄钟记录
            minutes = round(elapsed[0] / 60, 2)
            c.execute("UPDATE pomodoro_records SET total_sessions = total_sessions + ?, total_minutes = total_minutes + ?", 
                    (1, minutes,))
            conn.commit()
            
            pomo_win.destroy()
        else:
            running[0] = True
            update_timer()
    
    ttk.Button(
        ctrl_frame,
        text="退出专注",
        command=lambda: finish_pomodoro(False)
    ).pack(side='right', padx=20)

    pause_button = ttk.Button(
        ctrl_frame,
        text="⏸ 暂停",
        command=lambda: toggle_pause()
    )
    pause_button.pack(side='right', padx=5)

    pomo_win.protocol("WM_DELETE_WINDOW", lambda: finish_pomodoro(False))
    
    update_timer()

button_frame = ttk.Frame(root)
button_frame.grid(row=4, column=0, pady=10)

# 显示进度报告
def show_progress_report():
    progress_window = tk.Toplevel(root)
    progress_window.title("统计报告")
    progress_window.geometry("1200x700")# 
    progress_window.transient(root)
    progress_window.grab_set()

    # 设置全局字体
    style = ttk.Style()
    style.configure("Report.TLabelframe", font=("Microsoft YaHei", 12, "bold"))
    style.configure("Report.TLabel", font=("Microsoft YaHei", 11))
    
    # 主容器（左右分栏）
    main_frame = ttk.Frame(progress_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ========== 左侧区域 ==========
    left_frame = ttk.Frame(main_frame)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

    # 核心指标区
    metrics_frame = ttk.LabelFrame(left_frame, text="核心指标", style="Report.TLabelframe")
    metrics_frame.pack(fill="x", pady=10)

    # 获取统计数据
    c.execute("SELECT total_tasks FROM task_counter")
    result = c.fetchone()
    total_added = result[0] if result else 0
    c.execute("SELECT COUNT(*) FROM tasks WHERE rest_days=0")
    tomorrow_tasks = c.fetchone()[0]

    # 数值格式化函数
    def format_number(num):
        if num >= 10000:
            return f"{num/10000:.2f} 万"
        return str(num)

    # 指标卡片布局
    metrics_grid = ttk.Frame(metrics_frame)
    metrics_grid.pack(padx=10, pady=10, fill='both', expand=True)

    # 配置网格列权重
    for col in range(5):
        metrics_grid.columnconfigure(col, weight=1, uniform='metric_col')

    metrics_data = [
        ("📋 总任务数", format_number(get_num(1) or 0), "#4e73df"),
        ("✅ 已完成", format_number(get_num(2) or 0), "#1cc88a"),
        ("⏳ 待完成", format_number(get_num(3) or 0), "#f6c23e"),
        ("⏰ 明日过期", format_number(tomorrow_tasks or 0), "#e74a3b"),
        ("📈 累计添加", format_number(total_added or 0), "#36b9cc")
    ]

    for i, (title, value, color) in enumerate(metrics_data):
        card = ttk.Frame(metrics_grid, relief="groove", borderwidth=1)
        card.grid(row=0, column=i, padx=8, pady=8, sticky="nsew")
        
        # 配置卡片内部元素居中
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text=title, style="Report.TLabel").pack(pady=5, anchor='center')
        ttk.Label(card, text=str(value), 
                 font=("Microsoft YaHei", 20, "bold"), 
                 foreground=color).pack(pady=5, anchor='center')
    
    # 布局调整
    for i in range(5):
        card.columnconfigure(i, weight=1)

    # 图表区
    chart_frame = ttk.LabelFrame(left_frame, text="任务分布", style="Report.TLabelframe")
    chart_frame.pack(fill="both", expand=True, pady=10)

    # 配置中文字体（解决方格子问题）
    plt.rcParams['font.family'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.Figure(figsize=(10, 8))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    back_color = judge_theme(1)
    front_color = judge_theme(2)

    # 设置图表背景色
    fig.patch.set_facecolor(back_color)  # 图表整体背景色
    ax1.set_facecolor(back_color)  # 第一个子图背景色
    ax2.set_facecolor(back_color)  # 第二个子图背景色

    # 饼图数据
    pie_labels = ['已完成', '待完成']
    pie_sizes = [get_num(2), get_num(3)]
    pie_colors = ['#1cc88a', '#f6c23e']
    
    # 柱状图数据
    c.execute("SELECT rest_days, completed FROM tasks")
    all_tasks = c.fetchall()
    
    completed = 0
    pending = 0
    upcoming = 0
    expired = 0
    
    for task in all_tasks:
        rest_days, completed_status = task[0], task[1]
        if completed_status == '✅':
            completed += 1
        else:
            if rest_days >= 1:
                pending += 1
            elif rest_days == 0:
                upcoming += 1
            else:
                expired += 1

    status_labels = ['已完成', '进行中', '今日截止', '已过期']
    status_values = [completed, pending, upcoming, expired]
    colors = ['#1cc88a', '#4e73df', '#f6c23e', '#e74a3b']  # 绿、蓝、黄、红

    # 绘制图表
    ax1.pie(pie_sizes, labels=pie_labels, colors=pie_colors,
           autopct='%1.1f%%', startangle=140, textprops={'fontsize':10, 'color': front_color})  # 设置字体色
    ax1.set_title('任务完成比例', fontsize=12, color=front_color)  # 设置标题字体色

    bars = ax2.bar(status_labels, status_values, color=colors)
    ax2.set_title('任务状态分布', fontsize=12, color=front_color)  # 设置标题字体色
    ax2.set_ylabel('任务数量', fontsize=10, color=front_color)  # 设置坐标轴标签字体色
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom', fontsize=9, color=front_color)  # 设置数值标签字体色

    # 嵌入图表
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # ========== 右侧区域 ==========
    right_frame = ttk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

    # 详细数据区
    detail_frame = ttk.LabelFrame(right_frame, text="任务详情", style="Report.TLabelframe")
    detail_frame.pack(fill="both", expand=True)

    # 即将截止任务列表
    c.execute("SELECT name, due_date, rest_days FROM tasks WHERE completed != '✅' ORDER BY rest_days")
    urgent_tasks = c.fetchall()

    text_area = tk.Text(detail_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    
    # 添加带格式的内容
    text_area.tag_configure("header", font=("Microsoft YaHei", 11, "bold"))
    text_area.tag_configure("deadline_today", foreground="#f6c23e")
    text_area.tag_configure("deadline_overdue", foreground="#f8312f")
    text_area.insert(tk.END, "📌 待完成任务\n", "header")
    
    for task in urgent_tasks:
        if (task[2] > 0):
            text_area.insert(tk.END, 
                        f"  • {task[0]}\n"
                        f"     截止日期：{task[1]} （剩余{task[2]}天）\n\n")
        elif (task[2] == 0):
            text_area.insert(tk.END,
                        f"  • {task[0]}\n"
                        f"     截止日期：{task[1]} （今日截止）\n\n",
                        "deadline_today")
        else:
            text_area.insert(tk.END, 
                        f" • {task[0]}\n"
                        f"     截止日期：{task[1]} （过期{task[2]*-1}天）\n\n",
                        "deadline_overdue")
    
    text_area.configure(state="disabled")

    # 在右侧区域添加番茄钟统计
    pomodoro_frame = ttk.LabelFrame(right_frame, text="专注数据", style="Report.TLabelframe")
    pomodoro_frame.pack(fill="both", expand=True, pady=10)
    
    c.execute("SELECT * FROM pomodoro_records")
    pomo_data = c.fetchone()
    conn.commit()

    # 卡片式布局
    pomo_grid = ttk.Frame(pomodoro_frame)
    pomo_grid.pack(padx=10, pady=10, fill='both', expand=True)
    
    def format_duration(minutes):
        if minutes >= 60:
            return f"{minutes/60:.2f} 小时"
        return f"{minutes:.2f} 分钟"

    metrics = [
        ("🍅 专注次数", pomo_data[0] or 0, "#1cc88a"),
        ("⏳ 总时长", 
        format_duration(round(pomo_data[1], 2)) if pomo_data[1] else "0 分钟", 
        "#4e73df"),
        ("⏱️ 平均时长", 
        format_duration(round(pomo_data[1]/(pomo_data[0] or 1), 2)) if pomo_data[1] else "0 分钟", 
        "#f6c23e")
    ]
    
    for i, (title, value, color) in enumerate(metrics):
        card = ttk.Frame(pomo_grid, relief="groove", borderwidth=1)
        card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
        
        ttk.Label(card, text=title, style="Report.TLabel").pack(pady=5)
        ttk.Label(card, text=str(value), 
                 font=("Microsoft YaHei", 14, "bold"), 
                 foreground=color).pack(pady=5)
    
    # 布局调整
    for i in range(3):
        pomo_grid.columnconfigure(i, weight=1)

    # 布局权重配置
    main_frame.columnconfigure(0, weight=2)
    main_frame.columnconfigure(1, weight=2)
    main_frame.rowconfigure(0, weight=1)

    # 窗口关闭处理
    def close_window():
        plt.close('all')
        progress_window.destroy()
    
    progress_window.protocol("WM_DELETE_WINDOW", close_window)

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.geometry("1200x800")
    about_window.transient(root)
    about_window.grab_set()
    
    # ========== 主容器 ==========
    main_frame = ttk.Frame(about_window)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # ========== 标题区 ==========
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill='x', pady=10)
    
    # 应用标题居中
    ttk.Label(header_frame, 
             text="学翼 - TaskWing", 
             font=("Microsoft YaHei", 24, "bold"),
             foreground="#4fb9fe").pack(side='left', padx=25)
    
    # 当前版本移到左侧
    ttk.Label(header_frame, 
             text=Version,
             font=("Microsoft YaHei", 12),
             foreground="#666").pack(side='left', padx=10)
    
    # 检查更新按钮在右侧
    ttk.Button(header_frame,
              text="🔄 检查更新",
              command=lambda:version_judge(about_window),
              style='Accent.TButton').pack(side='right', padx=20)

    # ========== 核心内容区 ==========
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill='both', expand=True)

    pane = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
    pane.pack(fill='x', expand=True, padx=25, pady=10)

    # 功能列表
    features_frame = ttk.LabelFrame(pane, 
                                  text="核心功能", 
                                  padding=10,
                                  style="Large.TLabelframe")
    features_frame.pack(fill='x', padx=10, pady=5, side='left', expand=True)
    features = """✓ 任务管理与提醒
✓ 智能学习进度跟踪
✓ 番茄钟专注计时
✓ 数据可视化统计
✓ AI在线专业解答
✓ 多主题界面适配
✓ 系统托盘常驻运行
✓ 开机自启动设置"""
    ttk.Label(features_frame, 
             text=features,
             font=("Microsoft YaHei", 11),
             justify="left").pack(anchor='w')
    pane.add(features_frame)
    
    tips_frame = ttk.LabelFrame(pane,
                                  text="使用技巧 & 常见问题",
                                  padding=10,
                                  style="Large.TLabelframe")
    tips_frame.pack(fill='x', padx=10, pady=5, side='right', expand=True)
    tips = """【高级技巧】
· 在任务列表中双击任务可快速进入修改页面。
· 在任务列表中右键任务可唤出右键菜单。
· 在添加/修改任务页面，选中输入框，可按 Enter 快速提交。
· 【AI智答】输入框可使用 Enter 快速发送，Ctrl/Shift + Enter 换行，且支持撤销/恢复操作。
· 可同时开启多个【番茄钟】计时。
· 主页可在右上角选择是否置顶。
· 【番茄钟】计时窗口可在左下角选择是否置顶。


【常见问题 Q&A】
Q：为什么我的“AI智答”发送问题后会有错误弹窗？
A：这是因为服务商出现了问题，有时候是因为网络繁忙。推荐在“AI智答”的设置中按照教程配置自己的API。

Q：为什么有时候下载更新时会出现错误？
A：若不是手动关闭窗口的话，就是服务端的问题。由于本更新服务依赖GitHub，因此可能会出现网络问题。您也可以尝试在【关于】—【GitHub 项目页】手动下载更新包，然后手动安装。

Q：为什么我的“AI智答”发送问题后会有错误弹窗？
A：这是因为服务商出现了问题，有时候是因为网络繁忙。推荐在【AI智答】—【设置】中按照教程配置私有API，更加稳定。

Q：为什么“统计报告”显示不全？
A：这不是程序问题，是因为您当前没有其他数据可显示。

Q：为什么我的“统计报告”有些数据一直是0？
A：可能是您的数据库出现了问题。可在首页点击“设置”，并在“高级操作”中点击“删除所有数据”以重置数据库。

Q：为什么有的任务剩余天数是负数？
A：因为您那个任务过期了。

Q：为什么有时候专注后没有弹出任务完成的提示窗口？
A：因为您选择的任务已经完成了。"""
    # 滚动条容器
    scroll_container = ttk.Frame(tips_frame)
    scroll_container.pack(fill='both', expand=True)
    
    # 垂直滚动条
    scrollbar = ttk.Scrollbar(scroll_container)
    scrollbar.pack(side='right', fill='y')
    
    # 文本框配置
    tips_text = tk.Text(
        scroll_container,
        wrap=tk.WORD,
        yscrollcommand=scrollbar.set,
        font=("Microsoft YaHei", 11),
        padx=10,
        pady=10,
        height=9
    )
    tips_text.pack(fill='both', expand=True)
    scrollbar.config(command=tips_text.yview)

    # 插入带格式的内容
    tips_text.insert(tk.END, tips)  # 优化问题间距
    tips_text.configure(state="disabled")  # 设为只读

    pane.add(tips_frame)

    # ========== 信息区 ==========
    info_frame = ttk.Frame(content_frame)
    info_frame.pack(fill='x', expand=True, padx=20, pady=0)

    # 开发者信息
    dev_card = ttk.LabelFrame(info_frame, 
                            text="开发者信息", 
                            padding=15,
                            style="Large.TLabelframe")
    dev_card.pack(fill='x', padx=5, pady=5, side='left', expand=True)
    ttk.Label(dev_card,
             text="开发者：TiantianYZJ\nEmail：yzjtiantian@126.com",
             font=("Microsoft YaHei", 10),
             justify="left").pack(anchor='w')

    # ========== 底部信息区 ==========
    statement_frame = ttk.LabelFrame(info_frame, 
                            text="声明", 
                            padding=15,
                            style="Large.TLabelframe")
    statement_frame.pack(fill='x', padx=5, pady=5, side='right', expand=True)
    
    # 开源协议
    ttk.Label(statement_frame,
             text="学翼 遵循 GNU General Public License v3.0 开源协议",
             font=("Microsoft YaHei", 10),
             justify="left").pack(anchor='w')
    
    # 图标版权
    ttk.Label(statement_frame,
             text="部分图标来源于阿里巴巴矢量图标库，如有侵权请联系删除",
             font=("Microsoft YaHei", 10),
             justify="left").pack(anchor='w')

    # ========== 更新日志区 ==========
    changelog_frame = ttk.LabelFrame(main_frame, 
                                   text="更新日志", 
                                   padding=10,
                                   style="Large.TLabelframe")
    changelog_frame.pack(fill='both', expand=True, pady=5, padx=25)
    
    # 滚动条容器
    scroll_container = ttk.Frame(changelog_frame)
    scroll_container.pack(fill='both', expand=True)
    
    # 滚动条和文本框
    scrollbar = ttk.Scrollbar(scroll_container)
    scrollbar.pack(side='right', fill='y')
    
    changelog_text = tk.Text(
        scroll_container,
        wrap="word",
        yscrollcommand=scrollbar.set,
        font=("Microsoft YaHei", 10),
        height=8
    )
    changelog_text.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=changelog_text.yview)
    
    # 插入日志内容
    for entry in reversed(CHANGELOG):
        changelog_text.insert("end", f"• {entry}\n")
    changelog_text.configure(state="disabled")

    # ========== 操作按钮区 ==========
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=10)
    
    ttk.Button(btn_frame, 
              text="⭐ GitHub 项目页",
              command=lambda: webbrowser.open_new("https://github.com/TiantianYZJ/TaskWing")
              ).pack(side='left', padx=10)
    Tooltip(btn_frame.winfo_children()[0], "点击前往 GitHub 项目页（https://github.com/TiantianYZJ/TaskWing）")
    
    ttk.Button(btn_frame,
              text="关闭",
              style='Accent.TButton',
              command=about_window.destroy).pack(side='right', padx=10)

# ============== 设置界面 ==============
def open_settings():
    setting_window = tk.Toplevel(root)
    setting_window.title("设置")
    setting_window.geometry("500x500")
    setting_window.resizable(False, False)
    
    # ========== 主题设置 ==========
    theme_frame = ttk.LabelFrame(setting_window, text="界面设置", padding=10, style="Large.TLabelframe")
    theme_frame.pack(fill="x", padx=10, pady=5)
    
    c.execute("SELECT theme_choice FROM theme_settings")
    current_theme = c.fetchone()[0]
    
    theme_var = tk.StringVar(value=current_theme)
    ttk.Label(theme_frame, text="主题模式:").grid(row=0, column=0, sticky="w")
    theme_combobox = ttk.Combobox(
        theme_frame,
        textvariable=theme_var,
        values=["浅色模式", "深色模式", "跟随系统", "自动切换"],
        state="readonly",
        width=15
    )
    theme_combobox.grid(row=0, column=1, padx=5)

    # ========== 自启动设置 ==========
    autostart_frame = ttk.LabelFrame(setting_window, text="开机自启动", padding=10, style="Large.TLabelframe")
    autostart_frame.pack(fill="x", padx=10, pady=10)

    def get_startup_folder():
        """获取系统自启动文件夹路径"""
        startup_path = os.path.join(
            os.path.expanduser('~'),
            'AppData',
            'Roaming',
            'Microsoft',
            'Windows',
            'Start Menu',
            'Programs',
            'Startup'
        )
        return startup_path if os.path.exists(startup_path) else None

    def open_startup_folder():
        """打开自启动目录"""
        startup_path = get_startup_folder()
        if startup_path:
            os.startfile(startup_path)
        else:
            messagebox.showerror("错误", "找不到自启动目录", parent=setting_window)
    
    def create_autostart_shortcut():
        if getattr(sys, 'frozen', False):
            target_path = sys.executable
        else:
            target_path = os.path.abspath(sys.argv[0])
        
        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, "学翼.lnk")
        
        try:
            if os.path.exists(shortcut_path):
                if not messagebox.askyesno("确认", "已存在旧版本或已添加过的快捷方式，是否覆盖？", parent=setting_window):
                    return
                
            winshell.CreateShortcut(
                Path=shortcut_path,
                Target=target_path,
                Icon=(target_path, 0),
                Description="学翼"
            )
            messagebox.showinfo("成功", "开机自启动配置成功！", parent=setting_window)
        except Exception as e:
            messagebox.showerror("错误", f"配置失败：{str(e)}", parent=setting_window)

    # 删除
    def delete_autostart_shortcut():
        shortcut_path = os.path.join(winshell.startup(), "学翼.lnk")
        
        try:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                messagebox.showinfo("成功", "已取消开机自启动", parent=setting_window)
            else:
                messagebox.showinfo("提示", "您没有配置过开机自启动", parent=setting_window)
        except Exception as e:
            messagebox.showerror("错误", f"取消失败：{str(e)}", parent=setting_window)

    # 操作按钮
    ttk.Button(
        autostart_frame,
        text="⚡ 自动配置",
        command=create_autostart_shortcut,
        width=13
    ).grid(row=0, column=1, padx=5, pady=5)
    Tooltip(autostart_frame.winfo_children()[0], "设置开机自启动")

    ttk.Button(
        autostart_frame,
        text="❌ 取消配置",
        command=delete_autostart_shortcut,
        width=13
    ).grid(row=0, column=2, padx=5, pady=5)
    Tooltip(autostart_frame.winfo_children()[1], "取消开机自启动")
    
    # ========== 通知管理设置 ==========
    notify_frame = ttk.LabelFrame(setting_window, text="通知管理", padding=15, style="Large.TLabelframe")
    notify_frame.pack(pady=10, fill='x', padx=10)  # 放在显示设置之前

    # 获取当前通知设置
    c.execute("SELECT enable_notifications, check_updates FROM notice_settings")
    result = c.fetchone()
    notify_enabled, check_update = result if result else (1, 1)

    global notify_var, update_var
    notify_var = tk.IntVar(value=notify_enabled)
    update_var = tk.IntVar(value=check_update)

    # 通知开关
    ttk.Checkbutton(notify_frame,
                   text="开启系统通知",
                   variable=notify_var).pack(anchor="w")

    # 更新检查开关
    ttk.Checkbutton(notify_frame,
                   text="启动时自动检查更新",
                   variable=update_var).pack(anchor="w")


    danger_frame = ttk.LabelFrame(setting_window, text="高级选项", padding=10, style="Large.TLabelframe")
    danger_frame.pack(pady=10, fill='x', padx=10)
    
    def delete_all_data():
        # 二级确认
        if not messagebox.askokcancel(
            "警告", 
            "此操作将永久删除以下所有数据：\n"
            "• 所有任务数据\n• 累计任务数\n• 保存的主题设置\n• 保存的AI智答设置\n• 番茄钟统计记录\n"
            "请注意，该操作不可撤销！"
        ):
            return
            
        # 三级验证
        verification_code = ''.join(random.choices('ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz123456789', k=6))
        user_input = simpledialog.askstring(
            "最后确认", 
            f"请输入下方验证码（区分大小写）以确认删除\n验证码：{verification_code}\n"
            "这将清除所有数据且无法恢复，请三思！\n",
            parent=setting_window
        )
        
        if user_input == verification_code:
            # 执行删除操作
            tables = ['tasks', 'task_counter', 'theme_settings', 'ai_settings', 'pomodoro_records']
            for table in tables:
                c.execute(f"DELETE FROM {table}")
            
            # 重置默认设置
            c.execute("INSERT INTO theme_settings VALUES (1, '跟随系统')")
            c.execute("INSERT INTO task_counter (total_tasks) VALUES (0)")
            c.execute("INSERT INTO notice_settings (enable_notifications, check_updates) VALUES (1, 1)")
            c.execute("INSERT INTO ai_settings (api_key, default_model, provider, display_mode) VALUES ('', 'deepseek-chat', 'Deepseek', 'window')")
            conn.commit()
            
            # 更新界面
            update_task_list()
            theme_var.set('跟随系统')
            set_theme('跟随系统')
            messagebox.showinfo("完成", "所有数据已成功删除", parent=setting_window)
        else:
            messagebox.showwarning("取消", "验证码不匹配，删除操作已取消", parent=setting_window)

    # 打开数据库目录按钮
    ttk.Button(
        danger_frame,
        text="📂 查看数据库目录",
        command=lambda: os.startfile(user_data_dir)
    ).pack(side='left', pady=5, padx=5)
    Tooltip(danger_frame.winfo_children()[0], "打开数据库所在目录（⚠️程序运行时禁止删除或重命名数据库）")

    
    ttk.Button(
        danger_frame,
        text="📂 查看自启动目录",
        command=open_startup_folder,
    ).pack(side='left', pady=5, padx=5)
    Tooltip(danger_frame.winfo_children()[1], "打开自启动所在目录")

    ttk.Button(
        danger_frame,
        text="⚠️ 删除所有数据",
        command=delete_all_data,
        style="Danger.TButton"
    ).pack(side='left', pady=5, padx=5)
    Tooltip(danger_frame.winfo_children()[2], "⚠️删除您保存的所有数据⚠️")

    # 定义危险按钮样式
    style.configure("Danger.TButton", foreground="orange", background="#dc3545", font=("Microsoft YaHei", 10, "bold"))

    # ========== 保存按钮 ==========
    btn_frame = ttk.Frame(setting_window)
    btn_frame.pack(pady=10)

    def save_settings():
        set_theme(theme_var.get())
        c.execute("UPDATE notice_settings SET enable_notifications=?, check_updates=?",
            (notify_var.get(), update_var.get()))
        conn.commit()
        setting_window.destroy()

    ttk.Button(btn_frame, text="💾 保存", command=save_settings, width=12).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="↩️ 关闭", command=setting_window.destroy, width=12).grid(row=0, column=1, padx=5)

    setting_window.transient(root)
    setting_window.grab_set()
    
# ============== AI智答界面 ==============
def open_ai_assistant(parent):
    ai_window = tk.Toplevel(parent)
    ai_window.title("AI智答")
    ai_window.geometry("1100x800")
    
    # 获取当前主题颜色
    text_bg = judge_theme(1)
    text_fg = judge_theme(2)

    # 配置样式
    style = ttk.Style()
    style.configure("AIT.TFrame", background=text_bg)
    style.configure("Model.TButton", font=("Microsoft YaHei", 10), padding=5, width=18)
    style.configure("TFrame", bordercolor="#ced4da", lightcolor="#e9ecef", darkcolor="#dee2e6")
    
    main_frame = ttk.Frame(ai_window, padding=10)
    main_frame.pack(fill="both", expand=True)
    
    # 响应显示区域
    response_frame = ttk.LabelFrame(main_frame, 
                                  text="AI 回复",
                                  padding=5,
                                  style="Large.TLabelframe")
    response_frame.pack(fill="both", expand=True, pady=10)

    # 使用现代滚动条和边框
    response_container = ttk.Frame(response_frame, borderwidth=1, relief="solid")
    response_container.pack(fill="both", expand=True, padx=5, pady=5)

    # 配置滚动条
    response_scroll = ttk.Scrollbar(response_container)
    response_scroll.pack(side="right", fill="y")

    # 现代HTML显示区域
    html_label = HTMLLabel(
        response_container,
        background=text_bg,
        html='<div style="padding: 12px"></div>',  # 添加初始内边距
        borderwidth=0,
        highlightthickness=0
    )
    html_label.pack(fill="both", expand=True, padx=2)
    response_scroll.config(command=html_label.yview)

    # 添加阴影效果（需要先在样式配置中添加）
    style.configure("Response.TFrame", 
                   bordercolor="#e9ecef",
                   lightcolor="#f8f9fa",
                   darkcolor="#dee2e6")

    # 输入区域
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill="x", pady=10)

    # 使用ttk风格滚动条
    input_scroll = ttk.Scrollbar(input_frame)
    input_scroll.pack(side="right", fill="y")

    # 使用ttk风格输入框（需要配合Frame模拟现代输入框）
    input_container = ttk.Frame(input_frame, borderwidth=1, relief="solid")
    input_container.pack(fill="x", expand=True)

    input_text = tk.Text(
        input_container, 
        height=6,  # 增加高度
        wrap="word",
        font=("Microsoft YaHei", 12),
        yscrollcommand=input_scroll.set,
        bg=text_bg,
        fg=text_fg,
        insertbackground=text_fg,
        padx=8,  # 增加内边距
        pady=8,
        relief="flat",  # 去除默认边框
        highlightthickness=0,  # 隐藏高亮边框
        undo=True,  # 启用撤销功能
        autoseparators=True,  # 自动插入撤销分隔符
        maxundo=-1  # 无限撤销步骤
    )
    input_text.pack(fill="both", expand=True)

    # 键盘事件绑定
    def handle_keypress(event):
        # 撤销/恢复操作
        if event.state & 0x0004:  # Ctrl 键
            if event.keysym == 'z':
                input_text.edit_undo()
                return "break"
            elif event.keysym == 'y':
                input_text.edit_redo()
                return "break"

        # Enter发送，Ctrl/Shift+Enter换行
        if event.keysym == 'Return' and not (event.state & 0x0005):  # 0x0004(Ctrl) | 0x0001(Shift)
            send_message()
            return "break"
        elif event.keysym == 'Return' and (event.state & 0x0005):
            input_text.insert(tk.INSERT, '\n')
            return "break"
    
    input_text.bind("<KeyPress>", handle_keypress)

    # 配置滚动条命令
    input_scroll.config(command=input_text.yview)
    
    # 底部控制栏
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill="x", pady=5)
    
    # 模型切换按钮（固定宽度）
    model_var = tk.StringVar(value="deepseek-chat")
    
    def toggle_model():
        current = model_var.get()
        new_model = "deepseek-reasoner" if current == "deepseek-chat" else "deepseek-chat"
        model_var.set(new_model)
        btn_text = "✅ 深度思考已开启" if new_model == "deepseek-reasoner" else "❌ 深度思考已关闭"
        model_btn.config(text=btn_text)  # 保持按钮文本长度一致

    model_btn = ttk.Button(
        control_frame,
        text="❌ 深度思考已关闭",
        command=toggle_model,
        style="Model.TButton",
        width=18
    )
    model_btn.pack(side="left", padx=5)
    
    # 设置按钮
    ttk.Button(
        control_frame,
        text="⚙ 设置",
        command=lambda: open_ai_settings(ai_window),
        width=10
    ).pack(side="left", padx=5)

    ttk.Label(control_frame, 
             text="""（Enter 发送，Ctrl/Shift+Enter 换行）
本服务由Deepseek提供支持 · 不支持连续对话 · 本应用不对回答结果负责
默认使用共享API · 由作者自费 · 可在【设置】更改
有大量使用需求的用户请配置私有API，谢谢理解！""",
             font=("Microsoft YaHei", 9),
             foreground="#666666").pack(side="left", padx=5)
    
    # 新增附件相关组件
    attachments = {}  # 存储附件 {文件名: 内容}
    
    def add_attachments():
        nonlocal attachments
        if len(attachments) >= 5:
            messagebox.showwarning("提示", "最多添加5个附件", parent=ai_window)
            return
            
        files = filedialog.askopenfilenames(
            parent=ai_window,
            title="选择附件",
            filetypes=[
                ("文本文件", "*.txt*;.docx;*.doc;*.md;*.py;*.js;*.html;*.css"),
            ]
        )
        
        for file in files:
            if len(attachments) >=5: break
            try:
                # 处理Word文档
                # 处理Word文档（同时支持.doc和.docx）
                if file.lower().endswith(('.doc', '.docx')):
                    try:
                        # 新版.docx处理
                        if file.lower().endswith('.docx'):
                            doc = Document(file)
                            content = '\n'.join([para.text for para in doc.paragraphs])
                        # 旧版.doc处理
                        else:
                            
                            word = Dispatch('Word.Application')
                            word.visible = False  # 后台运行
                            doc = word.Documents.Open(file)
                            content = doc.Range().Text
                            doc.Close()
                            word.Quit()
                        
                        attachments[os.path.basename(file)] = content
                        
                    except Exception as e:
                        messagebox.showerror("文件读取错误", 
                            f"无法读取Word文档：{str(e)}\n"
                            "请确认：\n"
                            "1. 文件未被其他程序占用\n"
                            "2. 已安装Microsoft Word\n"
                            "3. 文件内容未被加密", 
                            parent=ai_window)
                        continue
                    
                # 处理其他文本文件    
                else:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        attachments[os.path.basename(file)] = f.read()
                        
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败：{str(e)}", parent=ai_window)
        
        # 更新附件显示（优化长文件名显示）
        file_names = []
        for name in attachments.keys():
            if len(name) > 100:
                shortened = f"{name[:10]}...{name[-7:]}"
                file_names.append(shortened)
            else:
                file_names.append(name)
        attachments_label.config(text=f"附件：{', '.join(file_names)}")

    def send_message():
        c.execute("SELECT provider, api_key FROM ai_settings")
        provider, api_key = c.fetchone()

        # 新增次数检查逻辑
        if not api_key:  # 使用共享API的情况
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 查询使用记录
            c.execute("SELECT date, count FROM api_usage LIMIT 1")
            record = c.fetchone()
            
            if record:
                record_date, remaining = record
                if record_date != today:  # 跨天重置
                    c.execute("UPDATE api_usage SET date=?, count=4", (today,))
                else:
                    if remaining <= 0:
                        messagebox.showwarning("次数已用尽", "今日免费次数已用尽，请配置私有API或明日再来", parent=ai_window)
                        return
                    c.execute("UPDATE api_usage SET count=count-1")
                c.execute("SELECT date, count FROM api_usage LIMIT 1")
            else:  # 首次使用
                c.execute("INSERT INTO api_usage VALUES (?, 4)", (today,))
            record = c.fetchone()
            sent_notice("您正在使用免费次数", f"今日剩余次数：{record}次\n（共享API每日免费次数5次，你可前往【设置】配置私有API）")
            conn.commit()

        question = input_text.get("1.0", "end").strip()
        global users_question

        # 拼接附件内容（优化格式）
        attachments_content = ""
        if attachments:
            attachments_content = "\n\n*（注意！以下是用户上传的附件，上文提到的文件也许在这里，请综合所有内容回答）"
            for name, content in attachments.items():
                attachments_content += f"\n\n【文件名：{name}】\n{content}"
        users_question = question
        
        if not question and not attachments:
            messagebox.showwarning("提示", "问题和附件不能同时为空", parent=ai_window)
            return
            
        # 显示提示
        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>思考中，请稍后（因需等待AI回答，所以程序未响应属正常现象）</p></div>'
        html_label.set_html(html_text)
        ai_window.update()
        

        if provider == "Deepseek":
            try:
                client = OpenAI(
                    api_key=api_key if api_key else "sk-6fa677012558401e88b54cde791f9822",  # 替换为默认API
                    base_url="https://api.deepseek.com"
                )
                
                response = client.chat.completions.create(
                    model=model_var.get(),
                    messages=[{"role": "user", "content": question + attachments_content}],
                    stream=False
                )
                
                c.execute("SELECT display_mode FROM ai_settings")
                display_mode = c.fetchone()[0] or "window"

                completion_tokens = response.usage.completion_tokens
                prompt_tokens = response.usage.prompt_tokens
                total_tokens = response.usage.total_tokens
                # 生成Markdown内容
                markdown = mistune.create_markdown(plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'math'])
                thinking_text = "<p>❌深度思考未开启，不进行深度思考</p>\n"
                if model_var.get() == "deepseek-reasoner":
                    thinking_text = f"<p>✅深度思考已完成</p><blockquote>{markdown(response.choices[0].message.reasoning_content)}</blockquote>\n"
                html_content = markdown(f"{response.choices[0].message.content}\n***\nToken用量统计：用户提问：{prompt_tokens} Tokens，AI回答：{completion_tokens} Tokens，共计：{total_tokens} Tokens")
                print(thinking_text + html_content)

                # 根据模式处理显示
                if display_mode == "window":
                    # 原有窗口显示逻辑
                    html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;">{thinking_text + "<p>（以上内容为AI思考过程，下文为正式回答）</p>" + html_content + "\n\n（AI回答乱码/格式不正确？在AI智答【设置】中将【AI回答显示方式】改为【在浏览器显示】即可！）"}</div>'
                    html_label.set_html(html_text)
                else:
                    global current_response_html
                    current_response_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/mhchem.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/copy-tex.min.js"></script>
                        <script>
                            document.addEventListener("DOMContentLoaded", function() {{
                                renderMathInElement(document.querySelector('.markdown-body'), {{
                                    delimiters: [
                                        {{left: '$$', right: '$$', display: true}},
                                        {{left: '$', right: '$', display: false}},
                                        {{left: '\\(', right: '\\)', display: false}},
                                        {{left: '\\[', right: '\\]', display: true}},
                                        {{left: '\\begin{{equation}}', right: '\\end{{equation}}', display: true}}, // 新增方程环境
                                        {{left: '\\begin{{align}}', right: '\\end{{align}}', display: true}} // 新增对齐环境
                                    ],
                                    ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option'],
                                    macros: {{
                                        "\\RR": "\\mathbb{{R}}",
                                        "\\abs": ["\\left|#1\\right|", 1]
                                    }},
                                    throwOnError: false,
                                    strict: 'ignore', // 忽略无法解析的内容
                                    trust: true, // 启用信任模式
                                    fleqn: true // 左对齐公式
                                }});
                            }});
                        </script>
                    </head>
                    <body>
                        <div class="markdown-body">
                        {thinking_text + html_content}
                        </div>
                    </body>
                    </html>
                    """

                    webbrowser.open("http://localhost:5000/ai-response")

                    # 显示提示
                    html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>回复已在浏览器显示</p></div>'
                    html_label.set_html(html_text)
                    ai_window.update()
                
            except Exception as e:
                messagebox.showerror("错误", f"请求失败：{str(e)}", parent=ai_window)
            finally:
                input_text.delete("1.0", "end")
                attachments.clear()
                attachments_label.config(text="")
                c.execute("UPDATE api_usage SET count=count+1")
                sent_notice("遇到错误", "已返还1次免费次数")
                conn.commit()
        elif provider == "硅基流动":
            api_key=api_key if api_key else "sk-dgxkvpdrkaxvnzhflxeiagetenlhvxsydybqncqwqurejvvf"  # 替换为默认API
            url = "https://api.siliconflow.cn/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type":"application/json"
            }
            payload = {
                "model": "deepseek-ai/DeepSeek-V3" if model_var.get() == "deepseek-chat" 
                        else "deepseek-ai/DeepSeek-R1",
                "messages": [{"role": "user", "content": question + attachments_content}],
            }
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    c.execute("SELECT display_mode FROM ai_settings")

                    display_mode = c.fetchone()[0] or "window"

                    completion_tokens = response.json()['usage']['completion_tokens']
                    prompt_tokens = response.json()['usage']['prompt_tokens']
                    total_tokens = response.json()['usage']['total_tokens']
                    # 生成Markdown内容
                    markdown = mistune.create_markdown(plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'math'])
                    thinking_text = "<p>❌深度思考未开启，不进行深度思考</p>\n"
                    if model_var.get() == "deepseek-reasoner":
                        thinking_text = f"<p>✅深度思考已完成</p><blockquote>{markdown(response.json()['choices'][0]['message']['reasoning_content'])}</blockquote>\n"
                    html_content = markdown(f"{response.json()['choices'][0]['message']['content']}\n***\nToken用量统计：用户提问：{prompt_tokens} Tokens，AI回答：{completion_tokens} Tokens，共计：{total_tokens} Tokens")
                    print(thinking_text + html_content)

                    # 根据模式处理显示
                    if display_mode == "window":
                        # 原有窗口显示逻辑
                        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;">{thinking_text + "<p>（以上内容为AI思考过程，下文为正式回答）</p>" + html_content + "\n\n（AI回答乱码/格式不正确？在AI智答【设置】中将【AI回答显示方式】改为【在浏览器显示】即可！）"}</div>'
                        html_label.set_html(html_text)
                    else:
                        current_response_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/mhchem.min.js"></script>
                        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/copy-tex.min.js"></script>
                        <script>
                            document.addEventListener("DOMContentLoaded", function() {{
                                renderMathInElement(document.querySelector('.markdown-body'), {{
                                    delimiters: [
                                        {{left: '$$', right: '$$', display: true}},
                                        {{left: '$', right: '$', display: false}},
                                        {{left: '\\(', right: '\\)', display: false}},
                                        {{left: '\\[', right: '\\]', display: true}},
                                        {{left: '\\begin{{equation}}', right: '\\end{{equation}}', display: true}}, // 新增方程环境
                                        {{left: '\\begin{{align}}', right: '\\end{{align}}', display: true}} // 新增对齐环境
                                    ],
                                    ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option'],
                                    macros: {{
                                        "\\RR": "\\mathbb{{R}}",
                                        "\\abs": ["\\left|#1\\right|", 1]
                                    }},
                                    throwOnError: false,
                                    strict: 'ignore', // 忽略无法解析的内容
                                    trust: true, // 启用信任模式
                                    fleqn: true // 左对齐公式
                                }});
                            }});
                        </script>
                    </head>
                    <body>
                        <div class="markdown-body">
                        {thinking_text + html_content}
                        </div>
                    </body>
                    </html>
                    """

                        webbrowser.open("http://localhost:5000/ai-response")

                        # 显示提示
                        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>回复已在浏览器显示</p></div>'
                        html_label.set_html(html_text)
                        ai_window.update()
                else:
                    messagebox.showerror("错误", f"请求失败：{response.text}", parent=ai_window)
            except Exception as e:
                messagebox.showerror("错误", f"请求异常：{str(e)}", parent=ai_window)
            finally:
                input_text.delete("1.0", "end")
                attachments.clear()
                attachments_label.config(text="")
                c.execute("UPDATE api_usage SET count=count+1")
                sent_notice("遇到错误", "已返还1次免费次数")
                conn.commit()

    ttk.Button(
        control_frame,
        text="⬆️ 发送",
        command=send_message,
        style="Accent.TButton"
    ).pack(side="right", padx=5)

    # 新增清空附件按钮
    ttk.Button(
        control_frame,
        text="清空附件",
        command=lambda: [attachments.clear(), attachments_label.config(text="")],
        style="Model.TButton",
        width=8
    ).pack(side="right", padx=2)
    Tooltip(control_frame.winfo_children()[4], "清除已添加的所有附件")

    # 附件标签和按钮（新增）
    attachments_label = ttk.Label(main_frame, text="", foreground="#666")
    attachments_label.pack(side="right", padx=2)
    ttk.Button(
        control_frame,
        text="📎 添加附件",
        command=add_attachments,
        style="Model.TButton",
        width=10
    ).pack(side="right", padx=5)
    Tooltip(control_frame.winfo_children()[5], "支持文件格式：.docx、.doc、.txt、.md、.py、.js、.html、.css")

    
    ai_window.transient(parent)
    ai_window.grab_set()

# ============== AI设置窗口 ==============
def open_ai_settings(parent):
    settings_window = tk.Toplevel(parent)
    settings_window.title("AI智答设置")
    settings_window.geometry("900x550")
    
    # 主容器使用pack布局
    main_frame = ttk.Frame(settings_window, padding=20)
    main_frame.pack(fill="both", expand=True)
    
    # API设置框架
    api_frame = ttk.LabelFrame(main_frame, text="API设置", padding=15, style="Large.TLabelframe")
    api_frame.pack(fill="x", pady=10)

    # 服务商选择框架
    provider_frame = ttk.LabelFrame(api_frame, text="服务提供商", padding=10, style="Large.TLabelframe")
    provider_frame.pack(fill="x", pady=5)
    
    # 获取当前设置
    c.execute("SELECT api_key, provider FROM ai_settings")
    api_key, current_provider = c.fetchone()
    
    # 服务商选择控件
    provider_var = tk.StringVar(value=current_provider)
    ttk.Label(provider_frame, text="选择服务商:").pack(side="left", padx=5)
    provider_combobox = ttk.Combobox(
        provider_frame,
        textvariable=provider_var,
        values=["Deepseek", "硅基流动"],
        state="readonly",
        width=15
    )
    provider_combobox.pack(side="left", padx=5)
    
    # API Key输入
    ttk.Label(api_frame, text="API Key:").pack(anchor="w")
    api_entry = ttk.Entry(api_frame)
    api_entry.insert(0, api_key)
    api_entry.pack(fill="x", pady=5, padx=0)
    
    ttk.Label(api_frame, 
             text="留空将使用作者自费的共享API\n推荐配置私有API，谢谢理解！",# 因近期Deepseek官方API关闭充值入口，【AI智答】暂停提供Deepseek渠道的共享API，单独配置该渠道私有API或使用硅基流动共享API不受影响\n
             font=("Microsoft YaHei", 9),
             foreground="#666666").pack(anchor="w")
    
    # ========== 新增配置教程按钮和内容 ==========
    def show_api_tutorial():
        webbrowser.open("http://localhost:5000/tutorial")
    
    ttk.Button(
        api_frame,
        text="📘 私有API配置教程",
        command=show_api_tutorial,
        width=20
    ).pack(pady=10)

    # ========== 新增回答设置部分 ==========
    display_frame = ttk.LabelFrame(main_frame, text="回答设置", padding=15, style="Large.TLabelframe")
    display_frame.pack(fill="x", pady=10)

    # 获取当前显示模式
    c.execute("SELECT display_mode FROM ai_settings")
    current_mode = c.fetchone()[0] or "window"

    # 显示方式下拉框
    ttk.Label(display_frame, text="AI回答显示方式:").pack(side="left", padx=5)
    mode_var = tk.StringVar(value=current_mode)
    mode_combobox = ttk.Combobox(
        display_frame,
        textvariable=mode_var,
        values=["window", "browser"],
        state="readonly",
        width=20
    )
    mode_combobox.pack(side="left", padx=5)
    
    # 设置下拉框显示文本
    mode_combobox.set("在原窗口显示" if current_mode == "window" else "在浏览器显示")
    mode_combobox.configure(
        values=["在原窗口显示", "在浏览器显示"],
        validate="key",
        validatecommand=lambda: False
    )

    ttk.Label(display_frame, 
             text="在原窗口显示：方便快捷。但仅支持IE4内核，因此无法渲染部分Markdown语法（表格、代码块等）\n在浏览器显示：将调用系统浏览器。但可渲染所有Markdown语法，更加现代化，可一键复制（推荐）",
             font=("Microsoft YaHei", 9),
             foreground="#666666").pack(anchor="w")
    
    save_btn = ttk.Button(
        main_frame,
        text="💾 保存设置",
        command=lambda: save_settings(api_entry.get(), provider_var.get()),
        style="Accent.TButton"
    )
    save_btn.pack(pady=15)
    
    def save_settings(key, provider):
        display_mode = "window" if mode_var.get() == "在原窗口显示" else "browser"
        c.execute("UPDATE ai_settings SET api_key=?, provider=?, display_mode=?", 
                (key, provider, display_mode))
        conn.commit()
        settings_window.destroy()
    
    settings_window.transient(parent)
    settings_window.grab_set()

# ============== 主窗口布局 ==============
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# 顶部功能区
top_frame = ttk.Frame(root)
top_frame.grid_rowconfigure(0, weight=1)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid(row=0, column=0, sticky="nsew")

# ntVar对象，用于追踪Checkbutton的状态
topmost_var = tk.IntVar(value=0)
# Checkbutton控件，用于切换窗口置顶状态
toggle_button = ttk.Checkbutton(top_frame, text="窗口置顶", variable=topmost_var, onvalue=1, offvalue=0, command=toggle_topmost)
toggle_button.grid(row=0, column=1, sticky="ne")

# 任务列表区域
task_frame = ttk.Frame(root)
task_frame.grid_rowconfigure(0, weight=1)
task_frame.grid_columnconfigure(0, weight=1)
task_frame.grid(row=1, column=0, sticky="nsew", padx=20)

style = ttk.Style(task_frame)
style.configure("Treeview.Heading", font=('Microsoft YaHei', 14))
style.configure("Treeview", font=('Microsoft YaHei', 12))
task_list = ttk.Treeview(task_frame, columns=("ID", "任务名称", "截止日期", "剩余天数", "状态"), show="headings")
task_list.grid_rowconfigure(0, weight=1)
task_list.grid_columnconfigure(0, weight=1)
task_list.grid(row=0, column=0, sticky="nsew")
task_list.column("ID", width=30, anchor='center')
task_list.heading("ID", text="ID")
task_list.column("任务名称", width=600, anchor='w')
task_list.heading("任务名称", text="任务名称")
task_list.column("截止日期", width=100, anchor='center')
task_list.heading("截止日期", text="截止日期")
task_list.column("剩余天数", width=80, anchor='center')
task_list.heading("剩余天数", text="剩余天数")
task_list.column("状态", width=50, anchor='center')
task_list.heading("状态", text="状态")

# 绑定双击事件
def on_double_click(event):
    if task_list.selection():
        edit_task()
task_list.bind("<Double-1>", on_double_click)

# 创建右键菜单
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="修改", command=edit_task)
context_menu.add_command(label="删除", command=delete_task)
context_menu.add_command(label="复制并粘贴", command=copy_and_paste_task)
context_menu.add_command(label="番茄钟", command=pomodoro_set_tasks)

def on_right_click(event):
    item = task_list.identify_row(event.y)
    if item:
        task_list.selection_set(item)
        context_menu.post(event.x_root, event.y_root)
        
task_list.bind("<Button-3>", on_right_click)

# 操作按钮组
edit_button = ttk.Frame(task_frame)
edit_button.grid(row=1, column=0, pady=10, sticky="nsew")

ttk.Button(edit_button, text="📝 修改", command=edit_task, width=10).grid(row=0, column=0, padx=3)
Tooltip(edit_button.winfo_children()[0], "修改选定任务的详细信息")
ttk.Button(edit_button, text="🗑️ 删除", command=delete_task, width=10).grid(row=0, column=1, padx=3)
Tooltip(edit_button.winfo_children()[1], "永久移除选定的任务")
ttk.Button(edit_button, text="🧹 清空", command=confirm_clear_tasks, width=10).grid(row=0, column=2, padx=3)
Tooltip(edit_button.winfo_children()[2], "清空当前任务列表")
ttk.Button(edit_button, text="🍅 番茄钟", command=pomodoro_set_tasks, width=10).grid(row=0, column=3, padx=3)
Tooltip(edit_button.winfo_children()[3], "启动番茄钟专注计时器")

# 底部功能区
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.grid(row=2, column=0, sticky="nsew")

# 添加任务模块
add_task_frame = ttk.LabelFrame(bottom_frame, text="新建任务", style="Large.TLabelframe", padding=10)
add_task_frame.pack(side="left", padx=10, fill="x", expand=True)

name_frame = ttk.Frame(add_task_frame)
name_frame.grid(row=0, column=0, sticky="w", pady=10)
ttk.Label(name_frame, text="任务名称:").grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(name_frame, width=40)
name_entry.grid(row=0, column=1, padx=5)
name_entry.bind("<Return>", lambda e: add_task())

# 创建一个新的 Frame 来放置日期选择的 Combobox
date_frame = ttk.Frame(add_task_frame)
date_frame.grid(row=1, column=0, sticky="w", pady=10)

ttk.Label(date_frame, text="截止日期:").grid(row=0, column=0, sticky="w")
date_entry = ttk.Entry(date_frame, width=12, font=('Microsoft YaHei', 9))
date_entry.insert(0, datetime.now().strftime("%Y/%m/%d"))  # 默认当前日期
date_entry.grid(row=0, column=1, padx=5)
date_entry.bind("<Return>", lambda e: add_task())

def set_add_date():
    def on_date_select():
        date_entry.delete(0, tk.END)
        date_entry.insert(0, cal.get_date())
        top.grab_release()
        top.destroy()
    
    top = tk.Toplevel(root)
    top.title("选择日期")
    top.resizable(False, False)
    top.transient(root)
    top.grab_set()
    cal = Calendar(top, 
                 selectmode='day',
                 year=datetime.now().year,
                 month=datetime.now().month,
                 day=datetime.now().day,
                 date_pattern='y/mm/dd')
    cal.pack(padx=10, pady=10)
    ttk.Button(top, text="确定", command=on_date_select).pack(pady=5)

ttk.Button(date_frame, text="📅 选择", command=set_add_date).grid(row=0, column=2, padx=5)
Tooltip(date_frame.winfo_children()[2], "在日历中选择日期")
ttk.Button(date_frame, text="➕ 确认添加", command=add_task, width=12).grid(row=0, column=3, padx=5)

# 右侧功能按钮
func_btn_frame = ttk.Frame(bottom_frame)
func_btn_frame.pack(side="right", padx=10)

ttk.Button(func_btn_frame, text="🤖 AI智答", command=lambda:open_ai_assistant(root), width=12).grid(row=0, column=0, pady=2)
Tooltip(func_btn_frame.winfo_children()[0], "使用AI解答疑惑")
ttk.Button(func_btn_frame, text="📈 统计报告", command=show_progress_report, width=12).grid(row=1, column=0, pady=2)
Tooltip(func_btn_frame.winfo_children()[1], "查看学习数据可视化报告")
ttk.Button(func_btn_frame, text="⚙️ 设置", command=open_settings, width=12).grid(row=2, column=0, pady=2)
Tooltip(func_btn_frame.winfo_children()[2], "修改应用设置")
ttk.Button(func_btn_frame, text="ℹ️ 关于应用", command=open_about, width=12).grid(row=3, column=0, pady=2)
Tooltip(func_btn_frame.winfo_children()[3], "查看应用信息和检查更新")

# 创建托盘
def on_closing(icon, item):
    icon.stop()
    if (get_num(1) == 0):
        sent_notice("学翼已退出", f"你没有任何任务哦")
    else:
        if (get_num(3) > 0):
            sent_notice("学翼已退出", f"记得完成剩下的{get_num(3)}个任务")
        elif (get_num(3) == 0):
            sent_notice("学翼已退出", f"厉害！你完成了所有共计{get_num(1)}个任务！")
    root.destroy()
    return 0

def on_show():
    root.withdraw()
    icon = create_tray_icon()
    sent_notice("已最小化到任务栏托盘", "右键托盘图标并选择【显示】可恢复")
    icon.run()
    return 0

root.protocol("WM_DELETE_WINDOW", on_show)
def on_showing(icon, item):
    icon.stop()
    root.deiconify()
    sent_notice("任务栏托盘已隐藏", "关闭所有窗口将再次出现")
    return 0

def open_ai_assistant_window(icon, item):
    icon.stop()
    root.deiconify()
    open_ai_assistant(root)
    sent_notice("任务栏托盘已隐藏", "关闭所有窗口将再次出现")
    return 0

def open_settings_window(icon, item):
    icon.stop()
    root.deiconify()
    open_settings()
    sent_notice("任务栏托盘已隐藏", "关闭所有窗口将再次出现")
    return 0

def open_about_window(icon, item):
    icon.stop()
    root.deiconify()
    open_about()
    sent_notice("任务栏托盘已隐藏", "关闭所有窗口将再次出现")
    return 0

def open_progress_window(icon, item):
    icon.stop()
    root.deiconify()
    show_progress_report()
    sent_notice("任务栏托盘已隐藏", "关闭所有窗口将再次出现")
    return 0

# 更新任务列表
update_task_list()

# 更新时间
update_time()

# 更新剩余天数
update_rest_days()

version_judge(root)

# 运行主循环
root.mainloop()

# 关闭数据库连接
conn.close()