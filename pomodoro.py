# -*- coding: utf-8 -*-
"""
桌面番茄钟 - 基于 Python + Tkinter
功能：25 分钟工作 / 5 分钟休息，支持 开始 / 暂停 / 重置
双击即可运行，无需安装任何依赖。
"""

import tkinter as tk
from tkinter import messagebox

# ---- 时间配置（分钟）----
WORK_MIN = 25   # 工作时长
BREAK_MIN = 5   # 休息时长

# ---- 配色 ----
COLOR_WORK = "#d95550"          # 工作-红
COLOR_WORK_ACTIVE = "#b84540"   # 工作按钮按下
COLOR_BREAK = "#4c9195"         # 休息-青
COLOR_BREAK_ACTIVE = "#3a7175"  # 休息按钮按下
COLOR_BG = "#2b2b2b"            # 背景
COLOR_TEXT = "#ffffff"


class Pomodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟")
        self.root.geometry("320x360")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

        # 状态
        self.is_work = True          # 当前是否处于工作阶段
        self.running = False         # 是否在倒计时
        self.remaining = WORK_MIN * 60   # 剩余秒数
        self.completed = 0           # 今日已完成番茄数
        self._after_id = None        # tkinter after 句柄

        self._build_ui()
        self._apply_phase_style()
        self._update_time()

    def _build_ui(self):
        # 阶段标题
        self.phase_label = tk.Label(
            self.root, text="工作", font=("Microsoft YaHei", 22, "bold"),
            bg=COLOR_BG, fg=COLOR_WORK)
        self.phase_label.pack(pady=(28, 6))

        # 倒计时显示
        self.time_label = tk.Label(
            self.root, text="25:00", font=("Consolas", 56, "bold"),
            bg=COLOR_BG, fg=COLOR_TEXT)
        self.time_label.pack(pady=10)

        # 完成番茄计数
        self.count_label = tk.Label(
            self.root, text="今日已完成 0 个番茄", font=("Microsoft YaHei", 11),
            bg=COLOR_BG, fg="#aaaaaa")
        self.count_label.pack(pady=(0, 18))

        # 按钮区
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, text="开始", width=8, font=("Microsoft YaHei", 12),
            command=self.toggle, bg=COLOR_WORK, fg="white",
            activebackground=COLOR_WORK_ACTIVE, relief="flat", cursor="hand2")
        self.start_btn.grid(row=0, column=0, padx=6)

        self.reset_btn = tk.Button(
            btn_frame, text="重置", width=8, font=("Microsoft YaHei", 12),
            command=self.reset, bg="#555555", fg="white",
            activebackground="#444444", relief="flat", cursor="hand2")
        self.reset_btn.grid(row=0, column=1, padx=6)

        # 跳过当前阶段
        self.skip_btn = tk.Button(
            self.root, text="跳过本阶段", font=("Microsoft YaHei", 10),
            command=self.skip, bg=COLOR_BG, fg="#888888",
            activebackground=COLOR_BG, activeforeground="#cccccc",
            relief="flat", cursor="hand2", bd=0)
        self.skip_btn.pack(pady=20)

    def _cancel_timer(self):
        """取消挂起的倒计时回调"""
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None

    def toggle(self):
        """开始 / 暂停 切换"""
        if self.running:
            self.running = False
            self.start_btn.config(text="继续")
            self._cancel_timer()
        else:
            self.running = True
            self.start_btn.config(text="暂停")
            self._tick()

    def _tick(self):
        """每秒倒计时一次"""
        if not self.running:
            return
        if self.remaining > 0:
            self.remaining -= 1
            self._update_time()
            self._after_id = self.root.after(1000, self._tick)
        else:
            self._phase_done()

    def _phase_done(self):
        """一个阶段结束"""
        self.running = False
        self.root.bell()  # 系统提示音
        if self.is_work:
            self.completed += 1
            self.count_label.config(text=f"今日已完成 {self.completed} 个番茄")
            messagebox.showinfo("番茄钟", "工作时间结束，休息一下吧！")
        else:
            messagebox.showinfo("番茄钟", "休息结束，开始下一个番茄！")
        self._switch_phase()

    def _switch_phase(self):
        """切换工作 / 休息"""
        self.is_work = not self.is_work
        self._reset_phase()

    def skip(self):
        """跳过当前阶段"""
        self._cancel_timer()
        self.running = False
        self._switch_phase()

    def reset(self):
        """重置到当前阶段开头"""
        self._cancel_timer()
        self.running = False
        self._reset_phase()

    def _reset_phase(self):
        """把当前阶段重置到开头并刷新界面"""
        self.remaining = (WORK_MIN if self.is_work else BREAK_MIN) * 60
        self.start_btn.config(text="开始")
        self._apply_phase_style()
        self._update_time()

    def _update_time(self):
        """刷新倒计时文本（每秒调用）"""
        m, s = divmod(self.remaining, 60)
        self.time_label.config(text=f"{m:02d}:{s:02d}")

    def _apply_phase_style(self):
        """根据当前阶段刷新标题与按钮配色（仅阶段切换时调用）"""
        if self.is_work:
            self.phase_label.config(text="工作", fg=COLOR_WORK)
            self.start_btn.config(bg=COLOR_WORK, activebackground=COLOR_WORK_ACTIVE)
        else:
            self.phase_label.config(text="休息", fg=COLOR_BREAK)
            self.start_btn.config(bg=COLOR_BREAK, activebackground=COLOR_BREAK_ACTIVE)


if __name__ == "__main__":
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()
