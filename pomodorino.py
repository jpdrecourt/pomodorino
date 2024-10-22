import tkinter as tk
import time
import threading
import sys, os.path

POMODORO_DURATION = 5  # For testing purposes

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.is_running = False
        self.create_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.keep_on_top()

    def create_window(self):
        window_width = 300
        window_height = 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        self.root.iconbitmap(resource_path('pomodoro_77K_1.ico'))
        self.root.configure(bg="black")
        self.root.title("Pomodoro Timer")

        self.start_button = tk.Button(self.root, text="Start", font=("Arial", 30), command=self.start_pomodoro)
        self.start_button.config(bg="white", fg="black")
        self.start_button.pack(expand=True, fill="both", padx=20, pady=20)

    def keep_on_top(self):
        if not self.is_running:
            self.root.attributes('-topmost', True)
            self.root.after(100, self.keep_on_top)

    def start_pomodoro(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED, text="Running...")
            self.root.attributes('-topmost', False)
            self.root.iconify()
            threading.Thread(target=self.run_timer, args=(POMODORO_DURATION,)).start()

    def run_timer(self, duration):
        for remaining in range(duration, 0, -1):
            mins, secs = divmod(remaining, 60)
            self.root.title(f"Time Left: {mins:02}:{secs:02}")
            time.sleep(1)

        self.is_running = False
        self.root.deiconify()
        self.start_button.config(state=tk.NORMAL, text="Start")
        self.root.title("Pomodoro Timer")
        self.keep_on_top()

    def on_closing(self):
        self.is_running = False
        self.root.destroy()

root = tk.Tk()
timer_app = PomodoroTimer(root)
root.mainloop()