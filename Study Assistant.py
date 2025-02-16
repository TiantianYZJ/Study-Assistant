# 更新日志
CHANGELOG = [
    "V0.0.1-2024.01.19 1、“学习助手”正式诞生，具备代办管理功能",
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
    "V1.0.0-2024.02.16 1、“学习助手”1.0.0正式版发布！欢迎体验交流",
]

import threading
import tkinter as tk
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

# Flask配置
flask_app = Flask(__name__, template_folder='templates', static_folder='static')
flask_app.config['TEMPLATES_AUTO_RELOAD'] = True
current_response_html = ""  # 用于存储当前要显示的HTML内容
users_question = ""  # 用于存储用户的问题

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
    toaster = ToastNotifier()
    toaster.show_toast(
        title=t,
        msg=m,
        duration=1,
        icon_path=icon_path,
        threaded=True
    )

# 切换窗口置顶状态
def toggle_topmost():
    is_topmost = topmost_var.get()
    root.attributes('-topmost', is_topmost)

# 设置默认编码为 utf-8
locale.setlocale(locale.LC_CTYPE, 'zh_CN.UTF-8')
importlib.reload(sys)

# 获取用户数据目录
user_data_dir = Path(os.getenv('APPDATA')) / "Study Assistant"
user_data_dir.mkdir(exist_ok=True)

# 修改数据库连接路径
db_path = user_data_dir / "Study Assistant_tasks.db"
conn = sqlite3.connect(str(db_path))
c = conn.cursor()

# 创建任务表
# c.execute('DROP TABLE ai_settings')
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             due_date TEXT,
             rest_days INTEGER,
             completed TEXT NOT NULL DEFAULT ' ')''')
conn.commit()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()

# 创建任务计数器表
c.execute('''CREATE TABLE IF NOT EXISTS task_counter (
             total_tasks INTEGER DEFAULT 0)''')
conn.commit()
# 初始化计数器
c.execute("SELECT COUNT(*) FROM task_counter")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO task_counter (total_tasks) VALUES (0)")
    conn.commit()
c.execute("SELECT * FROM task_counter")
task_counter = c.fetchall()

# 主题设置
c.execute('''CREATE TABLE IF NOT EXISTS theme_settings (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             theme_choice TEXT NOT NULL)''')
conn.commit()
c.execute("SELECT * FROM theme_settings")
theme_settings = c.fetchall()

# AI配置
c.execute('''CREATE TABLE IF NOT EXISTS ai_settings (
             api_key TEXT,
             default_model TEXT,
             provider TEXT,
             display_mode TEXT)''')
conn.commit()
# 更新初始化数据
c.execute("SELECT COUNT(*) FROM ai_settings")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO ai_settings (api_key, default_model, provider, display_mode) VALUES ('', 'deepseek-chat', 'Deepseek', 'window')")
    conn.commit()
ai_settings = c.fetchall()

# 检查读取的数据
print(tasks, task_counter, theme_settings, ai_settings)

def get_num(mode):
    # 获取任务总量、已完成数量和待完成数量
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
    sent_notice(f"{judge_time()}好！", f"你没有待完成的任务，快去添加吧！")

# 主窗口
root = tk.Tk()
root.title("学习助手")
width = 1000
height = 600
root.geometry(f"{width}x{height}")

# 创建一个Frame作为容器
frame = tk.Frame(root)
frame.grid(row=0, column=1, sticky="nsew")

# 设置网格的行和列权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# 创建并启动Flask线程（添加到主窗口初始化之后）
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

# 获取当前主题设置
c.execute("SELECT theme_choice FROM theme_settings")
current_theme = c.fetchone()[0]

# 设置主题
def set_theme(theme_choice):
    global theme
    if theme_choice == "浅色模式":
        root.tk.call("set_theme", "light")
        theme = "light"
    elif theme_choice == "深色模式":
        root.tk.call("set_theme", "dark")
        theme = "dark"
    elif theme_choice == "跟随系统":
        clock = int(strftime("%H"))
        if ((clock >= 0 and clock <= 4) or (clock >= 21 and clock <= 24)):
            root.tk.call("set_theme", "dark")
            theme = "dark"
        else:
            root.tk.call("set_theme", "light")
            theme = "light"

    # 重新应用表格样式
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Microsoft YaHei', 14))
    style.configure("Treeview",font=('Microsoft YaHei', 12))

    # 更新数据库中的主题设置
    c.execute("UPDATE theme_settings SET theme_choice=? WHERE id=1", (theme_choice,))
    conn.commit()

# 应用默认主题设置
set_theme(current_theme)
print(theme)

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
        width = event.width
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

# 显示托盘图标
def create_tray_icon():
    image = Image.open(resource_path('LOGO.png'))

    menu = (pystray.MenuItem('显示', on_showing), 
            pystray.MenuItem('AI智答', open_ai_assistant_window),
            pystray.MenuItem('设置', open_settings_window),
            pystray.MenuItem('关于', open_about_window),
            pystray.MenuItem('退出', on_closing))

    icon = pystray.Icon("LOGO", image, f"学习助手（{get_num(3)}个任务待完成）", menu)
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
    name = name_entry.get()
    year = year_combobox.get()
    month = month_combobox.get()
    day = day_combobox.get()
    due_date = f"{year}/{month}/{day}"
    completed = " "
    
    # 计算剩余天数
    due_date_obj = datetime.strptime(due_date, "%Y/%m/%d")
    rest_days = (due_date_obj - datetime.strptime(current_date, "%Y/%m/%d")).days

    if name and year and month and day:
        # 插入任务并更新计数器
        c.execute(
        "INSERT INTO tasks (name, due_date, rest_days, completed) VALUES (?, ?, ?, ?)",
        (name, due_date, rest_days, completed)
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
    else:
        messagebox.showwarning("警告", "请填写所有任务信息。")

# 编辑任务
def edit_task():
    selected = task_list.selection()
    if not selected:
        messagebox.showwarning("警告", "请选择一个任务进行编辑。")
        return
    item = task_list.item(selected)
    task_id, name, due_date, rest_days, completed, *extra_values = item['values']
    
    edit_window = tk.Toplevel(root)
    edit_window.title("编辑任务")
    edit_window.geometry("500x300")
    edit_window.resizable(False, False)
    
    # 主容器框架
    main_frame = ttk.Frame(edit_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # ========== 任务信息部分 ==========
    info_frame = ttk.LabelFrame(main_frame, text="任务详情", padding=10)
    info_frame.pack(fill="x", pady=5)
    
    # 任务名称
    ttk.Label(info_frame, text="任务名称:").grid(row=0, column=0, sticky="w", padx=5)
    name_entry = ttk.Entry(info_frame, width=40)
    name_entry.insert(0, name)
    name_entry.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)  # 水平扩展

    # ========== 截止日期部分 ==========
    ttk.Label(info_frame, text="截止日期:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    due_date_parts = due_date.split('/')
    
    year_var = tk.StringVar(value=due_date_parts[0])
    month_var = tk.StringVar(value=due_date_parts[1])
    day_var = tk.StringVar(value=due_date_parts[2])
    
    # 年份选择
    year_combo = ttk.Combobox(
        info_frame, 
        textvariable=year_var,
        values=[str(y) for y in range(2023, 2051)],
        width=7
    )
    year_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)  # 调整列位置
    ttk.Label(info_frame, text="年").grid(row=1, column=1, sticky="w", padx=75, pady=5)
    
    # 月份选择
    month_combo = ttk.Combobox(
        info_frame,
        textvariable=month_var,
        values=[str(m).zfill(2) for m in range(1, 13)],
        width=5
    )
    month_combo.grid(row=1, column=1, sticky="w", padx=100, pady=5)
    ttk.Label(info_frame, text="月").grid(row=1, column=1, sticky="w", padx=160, pady=5)
    
    # 日期选择
    day_combo = ttk.Combobox(
        info_frame,
        textvariable=day_var,
        values=[str(d).zfill(2) for d in range(1, 32)],
        width=5
    )
    day_combo.grid(row=1, column=1, sticky="w", padx=185, pady=5)
    ttk.Label(info_frame, text="日").grid(row=1, column=1, sticky="w", padx=245, pady=5)

    # ========== 任务状态部分 ==========
    status_frame = ttk.LabelFrame(main_frame, text="任务状态", padding=10)
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
        new_name = name_entry.get()
        new_date = f"{year_var.get()}/{month_var.get()}/{day_var.get()}"
        new_status = "✅" if completed_var.get() else " "
        
        # 计算剩余天数
        new_due_date_obj = datetime.strptime(new_date, "%Y/%m/%d")
        new_rest_days = (new_due_date_obj - datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")).days

        # 获取原始状态
        c.execute("SELECT completed FROM tasks WHERE id=?", (task_id,))
        current_status = c.fetchone()[0].strip()
        
        if current_status.strip() == '' and new_status == "✅":
            conn.commit()  
            
            total = get_num(1)
            actual_completed = get_num(2)+1
            remaining = get_num(3)-1
            progress = actual_completed / total * 100
            print(total, actual_completed, remaining)

            if remaining == 0:
                sent_notice("完成了所有任务，真厉害！", f"已完成{progress}%，共计{get_num(1)}个任务")
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
    if messagebox.askokcancel("确认", """确定要清空任务列表吗？
此操作将同时重置统计数据（【累计添加】等归零）"""):
        c.execute("DELETE FROM tasks")
        c.execute("UPDATE task_counter SET total_tasks=0")
        conn.commit()
        update_task_list()
        sent_notice("您清空了任务列表","任务列表清空成功")

button_frame = ttk.Frame(root)
button_frame.grid(row=4, column=0, pady=10)

# 显示进度报告
def show_progress_report():
    progress_window = tk.Toplevel(root)
    progress_window.title("学习数据统计")
    progress_window.geometry("1200x700")
    
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

    # 指标卡片布局
    metrics_grid = ttk.Frame(metrics_frame)
    metrics_grid.pack(padx=10, pady=10)

    metrics_data = [
        ("📋 总任务数", get_num(1), "#4e73df"),
        ("✅ 已完成", get_num(2), "#1cc88a"),
        ("⏳ 待完成", get_num(3), "#f6c23e"),
        ("⏰ 明日过期", tomorrow_tasks, "#e74a3b"),
        ("📈 累计添加", total_added, "#36b9cc")
    ]

    for i, (title, value, color) in enumerate(metrics_data):
        card = ttk.Frame(metrics_grid, relief="groove", borderwidth=1)
        card.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")
        
        ttk.Label(card, text=title, style="Report.TLabel").pack(pady=5)
        ttk.Label(card, text=str(value), 
                 font=("Microsoft YaHei", 20, "bold"), 
                 foreground=color).pack(pady=5)

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
            if rest_days > 1:
                pending += 1
            elif rest_days >= 0:
                upcoming += 1
            else:
                expired += 1

    status_labels = ['已完成', '待完成', '待完成-即将截止', '待完成-已截止']
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
    c.execute("SELECT name, due_date, rest_days FROM tasks WHERE rest_days <= 3 ORDER BY rest_days")
    urgent_tasks = c.fetchall()

    text_area = tk.Text(detail_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10))
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    
    # 添加带格式的内容
    text_area.tag_configure("header", font=("Microsoft YaHei", 11, "bold"))
    text_area.insert(tk.END, "📌 即将截止（剩余3天以内）\n", "header")
    
    for task in urgent_tasks:
        if (task[2] > 0):
            text_area.insert(tk.END, 
                        f"  • {task[0]}\n"
                        f"     截止日期：{task[1]} （剩余{task[2]}天）\n\n")
        elif (task[2] == 0):
            text_area.insert(tk.END,
                        f"  • {task[0]}\n"
                        f"     截止日期：{task[1]} （今日截止）\n\n")
        else:
            text_area.insert(tk.END, 
                        f"  • {task[0]}\n"
                        f"     截止日期：{task[1]} （过期{task[2]*-1}天）\n\n")
    
    text_area.configure(state="disabled")

    # 布局权重配置
    main_frame.columnconfigure(0, weight=3)  # 左侧占3/4
    main_frame.columnconfigure(1, weight=1)  # 右侧占1/4
    main_frame.rowconfigure(0, weight=1)

    # 窗口关闭处理
    def close_window():
        plt.close('all')
        progress_window.destroy()
    
    progress_window.protocol("WM_DELETE_WINDOW", close_window)

def open_about():
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.geometry("1000x860")
    about_window.resizable(False, False)
    
    # 使用Frame容器
    content_frame = ttk.Frame(about_window)
    content_frame.pack(pady=20, padx=30, fill='both', expand=True)

    # 标题部分
    ttk.Label(content_frame, 
             text="学习助手\nStudy Assistant", 
             font=("Microsoft YaHei", 18, "bold"),
             foreground="#2c3e50",
             justify="center").pack(pady=10)

    # 版本信息
    ttk.Label(content_frame,
             text="V1.0.0",
             font=("Microsoft YaHei", 10),
             foreground="#7f8c8d").pack(pady=5)

    # 分隔线
    ttk.Separator(content_frame).pack(fill='x', pady=10)

    # 功能列表
    features = """
亮点功能：
✓ 任务管理与提醒
✓ 智能学习进度跟踪
✓ 数据可视化统计
✓ 接入Deepseek-V3&R1模型，AI在线专业解答
✓ 多主题界面适配
✓ 响应式窗口布局
✓ 系统托盘常驻运行
✓ 可设置开机自启动
"""
    ttk.Label(content_frame, 
             text=features,
             font=("Microsoft YaHei", 11),
             justify="left").pack(pady=5, anchor='w')

    # 开发信息
    ttk.Label(content_frame,
             text="开发者：TiantianYZJ\n"
                  "Email：yzjtiantian@126.com\n",
             font=("Microsoft YaHei", 10),
             justify="left",
             foreground="#34495e").pack(pady=10, anchor='w')

    # 版权信息
    ttk.Label(content_frame,
             text="所有图标均来源于阿里巴巴矢量图标库 · 如有侵权请联系删除",
             font=("Microsoft YaHei", 9),
             foreground="#95a5a6",
             justify="center").pack(pady=10)
    
    # 许可证信息
    ttk.Label(content_frame,
             text="本应用遵循 GNU General Public License v3.0 开源协议",
             font=("Microsoft YaHei", 9),
             foreground="#95a5a6",
             justify="center").pack(pady=0)
    
    # 添加超链接提示
    link_label = ttk.Label(content_frame,
                           text="查看GitHub项目页",
                           font=("Microsoft YaHei", 9, "underline"),
                           foreground="#3498db",
                           cursor="hand2")
    link_label.pack(pady=3)
    link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/TiantianYZJ/Study-Assistant"))
    
    # ========== 新增更新日志部分 ==========
    changelog_frame = ttk.LabelFrame(content_frame, text="更新日志", padding=10)
    changelog_frame.pack(fill="both", expand=True, pady=10)
    
    # 滚动条容器
    scroll_container = ttk.Frame(changelog_frame)
    scroll_container.pack(fill="both", expand=True)
    
    # 滚动条
    scrollbar = ttk.Scrollbar(scroll_container)
    scrollbar.pack(side="right", fill="y")
    
    # 文本框显示日志
    changelog_text = tk.Text(
        scroll_container,
        wrap="word",
        yscrollcommand=scrollbar.set,
        font=("Microsoft YaHei", 10),
        height=8
    )
    changelog_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=changelog_text.yview)
    
    # 插入日志内容
    for entry in reversed(CHANGELOG):
        changelog_text.insert("end", f"• {entry}\n")
    changelog_text.configure(state="disabled")

    # 关闭按钮
    ttk.Button(content_frame, 
              text="确定", 
              command=about_window.destroy,
              style='Accent.TButton').pack(pady=15)

# ============== 设置界面 ==============
def open_settings():
    setting_window = tk.Toplevel(root)
    setting_window.title("程序设置")
    setting_window.geometry("450x300")
    setting_window.resizable(False, False)
    
    # ========== 主题设置 ==========
    theme_frame = ttk.LabelFrame(setting_window, text="界面设置", padding=10)
    theme_frame.pack(fill="x", padx=10, pady=5)
    
    c.execute("SELECT theme_choice FROM theme_settings")
    current_theme = c.fetchone()[0]
    
    theme_var = tk.StringVar(value=current_theme)
    ttk.Label(theme_frame, text="主题模式:").grid(row=0, column=0, sticky="w")
    theme_combobox = ttk.Combobox(
        theme_frame,
        textvariable=theme_var,
        values=["浅色模式", "深色模式", "跟随系统"],
        state="readonly",
        width=15
    )
    theme_combobox.grid(row=0, column=1, padx=5)

    # ========== 自启动设置 ==========
    autostart_frame = ttk.LabelFrame(setting_window, text="开机自启动", padding=10)
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
            messagebox.showinfo("操作指南",
                "1. 在打开的文件夹中选中\"Study Assistant\"，右键呼出菜单\n"
                "2. 选择【删除】\n"
                "单击【确定】以打开系统自启动目录",
                parent=setting_window)
            os.startfile(startup_path)
        else:
            messagebox.showerror("错误", "找不到自启动目录", parent=setting_window)
    
    def create_autostart_shortcut():
        if getattr(sys, 'frozen', False):
            target_path = sys.executable
        else:
            target_path = os.path.abspath(sys.argv[0])
        
        startup_folder = winshell.startup()
        shortcut_path = os.path.join(startup_folder, "Study Assistant.lnk")
        
        try:
            if os.path.exists(shortcut_path):
                if not messagebox.askyesno("确认", "已存在旧版本的快捷方式，是否覆盖？", parent=setting_window):
                    return
                
            winshell.CreateShortcut(
                Path=shortcut_path,
                Target=target_path,
                Icon=(target_path, 0),
                Description="学习助手"
            )
            messagebox.showinfo("成功", "开机自启动配置成功！重启设备生效", parent=setting_window)
        except Exception as e:
            messagebox.showerror("错误", f"配置失败：{str(e)}", parent=setting_window)

    # 操作按钮
    ttk.Button(
        autostart_frame,
        text="⚡ 自动配置",
        command=create_autostart_shortcut,
        width=18
    ).grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(
        autostart_frame,
        text="❌ 取消配置",
        command=open_startup_folder,
        width=18
    ).grid(row=0, column=2, padx=5, pady=5)

    # 说明文字
    ttk.Label(autostart_frame, 
             text="将本程序添加到开机启动项", 
             foreground="#666666",
             font=("Microsoft YaHei", 9)
             ).grid(row=1, column=0, columnspan=2)

    # ========== 保存按钮 ==========
    btn_frame = ttk.Frame(setting_window)
    btn_frame.pack(pady=10)

    def save_settings():
        set_theme(theme_var.get())
        setting_window.destroy()

    ttk.Button(btn_frame, text="💾 保存", command=save_settings, width=12).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="↩️ 关闭", command=setting_window.destroy, width=12).grid(row=0, column=1, padx=5)

    setting_window.transient(root)
    setting_window.grab_set()
    
# ============== AI智答界面 ==============
def open_ai_assistant():
    ai_window = tk.Toplevel(root)
    ai_window.title("AI智答")
    ai_window.geometry("1000x800")
    
    # 获取当前主题颜色
    text_bg = judge_theme(1)
    text_fg = judge_theme(2)

    # 配置样式
    style = ttk.Style()
    style.configure("AIT.TFrame", background=text_bg)
    style.configure("Model.TButton", font=("Microsoft YaHei", 10), padding=5, width=18)
    
    main_frame = ttk.Frame(ai_window, padding=10)
    main_frame.pack(fill="both", expand=True)
    
    # 响应显示区域
    response_frame = ttk.Frame(main_frame)
    response_frame.pack(fill="both", expand=True, pady=5)
    
    response_scroll = tk.Scrollbar(response_frame)
    response_scroll.pack(side="right", fill="y")
    
    # 使用 HTMLLabel 替代原有的 Text 组件
    html_label = HTMLLabel(response_frame, background=text_bg)
    html_label.pack(fill="both", expand=True)
    response_scroll.config(command=html_label.yview)

    # 输入区域
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill="x", pady=10)
    
    input_scroll = tk.Scrollbar(input_frame)
    input_scroll.pack(side="right", fill="y")
    
    input_text = tk.Text(
        input_frame, 
        height=6,
        wrap="word",
        font=("Microsoft YaHei", 12),
        yscrollcommand=input_scroll.set,
        bg=text_bg,
        fg=text_fg,
        insertbackground=text_fg
    )
    input_text.pack(fill="x", expand=True)
    input_scroll.config(command=input_text.yview)
    
    # 底部控制栏
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill="x", pady=5)
    
    # 模型切换按钮（固定宽度）
    model_var = tk.StringVar(value="deepseek-chat")
    
    def toggle_model():
        current = model_var.get()
        new_model = "deepseek-r1" if current == "deepseek-chat" else "deepseek-chat"
        model_var.set(new_model)
        btn_text = "✅深度思考已开启" if new_model == "deepseek-r1" else "❌深度思考已关闭"
        model_btn.config(text=btn_text)  # 保持按钮文本长度一致

    model_btn = ttk.Button(
        control_frame,
        text="❌深度思考已关闭",
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
             text="""本服务由Deepseek提供支持 · 不支持连续对话
默认使用共享API · 由作者自费 · 可在【设置】更改
有大量使用需求的用户请配置自己的API，谢谢理解！""",
             font=("Microsoft YaHei", 9),
             foreground="#666666").pack(side="left", padx=5)
    
    def send_message():
        question = input_text.get("1.0", "end").strip()
        global users_question
        users_question = question
        c.execute("SELECT provider, api_key FROM ai_settings")
        provider, api_key = c.fetchone()
        
        if not question:
            messagebox.showwarning("提示", "请输入问题内容")
            return
            
        # 显示提示
        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>思考中，请稍后（未响应属正常现象）</p></div>'
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
                    messages=[{"role": "user", "content": question}],
                    stream=False
                )
                
                c.execute("SELECT display_mode FROM ai_settings")
                display_mode = c.fetchone()[0] or "window"

                # 生成Markdown内容
                markdown = mistune.create_markdown(plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'math'])
                html_content = markdown(response.choices[0].message.content)
                
                # 根据模式处理显示
                if display_mode == "window":
                    # 原有窗口显示逻辑
                    html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;">{html_content}</div>'
                    html_label.set_html(html_text)
                else:
                    global current_response_html
                    current_response_html = f"""
                    <div class="markdown-body">
                    {html_content}
                    </div>
                    """

                    # 改成更简单的结构，CSS通过模板加载
                    webbrowser.open("http://localhost:5000/ai-response")

                    # 显示提示
                    html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>回复已在浏览器显示</p></div>'
                    html_label.set_html(html_text)
                    ai_window.update()
                
            except Exception as e:
                messagebox.showerror("错误", f"请求失败：{str(e)}")
            finally:
                input_text.delete("1.0", "end")
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
                "messages": [{"role": "user", "content": question}],
            }
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    c.execute("SELECT display_mode FROM ai_settings")
                    display_mode = c.fetchone()[0] or "window"

                    # 生成Markdown内容
                    markdown = mistune.create_markdown(plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'math'])
                    html_content = markdown(response.json()['choices'][0]['message']['content'])
                    
                    # 根据模式处理显示
                    if display_mode == "window":
                        # 原有窗口显示逻辑
                        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;">{html_content}</div>'
                        html_label.set_html(html_text)
                    else:
                        current_response_html = f"""
                        <div class="markdown-body">
                        {html_content}
                        </div>
                        """

                        webbrowser.open("http://localhost:5000/ai-response")

                        # 显示提示
                        html_text = f'<div style="background-color: {judge_theme(1)}; color: {judge_theme(2)}; font-family: Microsoft YaHei;"><p>回复已在浏览器显示</p></div>'
                        html_label.set_html(html_text)
                        ai_window.update()
                else:
                    messagebox.showerror("错误", f"请求失败：{response.text}")
            except Exception as e:
                messagebox.showerror("错误", f"网络请求异常：{str(e)}")

    ttk.Button(
        control_frame,
        text="⬆️ 发送",
        command=send_message,
        style="Accent.TButton"
    ).pack(side="right", padx=5)
    
    ai_window.transient(root)
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
    api_frame = ttk.LabelFrame(main_frame, text="API设置", padding=15)
    api_frame.pack(fill="x", pady=10)

    # 服务商选择框架
    provider_frame = ttk.LabelFrame(api_frame, text="服务提供商", padding=10)
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
    api_entry.pack(fill="x", pady=5, padx=5)
    
    ttk.Label(api_frame, 
             text="留空将使用作者自费默认API\n推荐配置私有API Key，谢谢理解！",
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
    display_frame = ttk.LabelFrame(main_frame, text="回答设置", padding=15)
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
             text="在原窗口显示：方便快捷。但仅支持IE4内核，因此无法渲染部分Markdown语法\n在浏览器显示：将调用系统，浏览器。但可渲染所有Markdown语法，更加现代化，可一键复制（推荐）",
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

# 操作按钮组
edit_button = ttk.Frame(task_frame)
edit_button.grid(row=1, column=0, pady=10, sticky="nsew")

ttk.Button(edit_button, text="📝 编辑", command=edit_task, width=10).grid(row=0, column=0, padx=3)
ttk.Button(edit_button, text="🗑️ 删除", command=delete_task, width=10).grid(row=0, column=1, padx=3)
ttk.Button(edit_button, text="🧹 清空", command=confirm_clear_tasks, width=10).grid(row=0, column=2, padx=3)

# 底部功能区
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.grid(row=2, column=0, sticky="nsew")

# 添加任务模块
add_task_frame = ttk.LabelFrame(bottom_frame, text="新建任务", padding=10)
add_task_frame.pack(side="left", padx=10, fill="x", expand=True)

name_frame = ttk.Frame(add_task_frame)
name_frame.grid(row=0, column=0, sticky="w", pady=10)
ttk.Label(name_frame, text="任务名称:").grid(row=0, column=0, sticky="w")
name_entry = ttk.Entry(name_frame, width=40)
name_entry.grid(row=0, column=1, padx=5)

# 创建一个新的 Frame 来放置日期选择的 Combobox
date_frame = ttk.Frame(add_task_frame)
date_frame.grid(row=1, column=0, sticky="w", pady=10)

ttk.Label(date_frame, text="截止日期:").grid(row=0, column=0, sticky="w")
year_combobox = ttk.Combobox(date_frame, values=[str(y) for y in range(2025,2051)], width=7)
year_combobox.set(strftime("%Y"))
year_combobox.grid(row=0, column=1, padx=2)
ttk.Label(date_frame, text="年").grid(row=0, column=2, sticky="w")
month_combobox = ttk.Combobox(date_frame, values=[str(m).zfill(2) for m in range(1,13)], width=5)
month_combobox.set(strftime("%m"))
month_combobox.grid(row=0, column=3, padx=2)
ttk.Label(date_frame, text="月").grid(row=0, column=4, sticky="w")
day_combobox = ttk.Combobox(date_frame, values=[str(d).zfill(2) for d in range(1,32)], width=5)
day_combobox.set(strftime("%d"))
day_combobox.grid(row=0, column=5, padx=2)
ttk.Label(date_frame, text="日").grid(row=0, column=6, sticky="w")
ttk.Button(date_frame, text="➕ 添加", command=add_task, width=8).grid(row=0, column=7, padx=5)

# 右侧功能按钮
func_btn_frame = ttk.Frame(bottom_frame)
func_btn_frame.pack(side="right", padx=10)

ttk.Button(func_btn_frame, text="🤖 AI智答", command=open_ai_assistant, width=12).grid(row=0, column=0, pady=2)
ttk.Button(func_btn_frame, text="📈 统计报告", command=show_progress_report, width=12).grid(row=1, column=0, pady=2)
ttk.Button(func_btn_frame, text="⚙️ 设置", command=open_settings, width=12).grid(row=2, column=0, pady=2)
ttk.Button(func_btn_frame, text="ℹ️ 关于应用", command=open_about, width=12).grid(row=3, column=0, pady=2)

# 创建托盘
def on_closing(icon, item):
    icon.stop()
    if (get_num(3) > 0):
        sent_notice("学习助手已退出", f"记得完成剩下的{get_num(3)}个任务")
    elif (get_num(3) == 0):
        sent_notice("学习助手已退出", f"厉害！你完成了所有共计{get_num(1)}个任务！")
    root.destroy()
    return 0

def on_show():
    root.withdraw()
    icon = create_tray_icon()
    sent_notice("已最小化到任务栏托盘", "右击托盘图标并选择【显示】可恢复")
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
    open_ai_assistant()
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

# 更新任务列表
update_task_list()

# 更新时间
update_time()

# 更新剩余天数
update_rest_days()

# 运行主循环
root.mainloop()

# 关闭数据库连接
conn.close()