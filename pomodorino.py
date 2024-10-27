import tkinter as tk
from time import sleep
from threading import Thread
from pathlib import Path

POMODORO_DURATION = 25  # 25 minutes

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.is_running = False
        self.pomodoros = 0
        self.create_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Map>", lambda e: self.set_topmost(True) if not self.is_running else None)

    def create_window(self):
        self.width = 300
        self.height = 180
        self.root.geometry(f"{self.width}x{self.height}+%d+%d" % (
            (self.root.winfo_screenwidth() - self.width) // 2,
            (self.root.winfo_screenheight() - self.height) // 2
        ))

        icon_path = Path('pomodoro_77K_1.ico')
        if icon_path.exists():
            self.root.iconbitmap(icon_path)

        self.root.configure(bg="black")
        self.root.title("Pomodoro Timer")
        self.set_topmost(True)

        # Start Button
        self.start_button = tk.Button(
            self.root,
            text="Start",
            font=("Arial", 30),
            command=self.start_pomodoro,
            bg="white",
            fg="black"
        )
        self.start_button.pack(expand=True, fill="both", padx=30, pady=(20, 20))

        # Pomodoros Counter Label
        self.pomodoro_label = tk.Label(
            self.root,
            text=f"Previous pomodoros: {self.pomodoros}",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )
        self.pomodoro_label.pack(pady=(0, 20))

    def set_topmost(self, state):
        self.root.attributes('-topmost', state)
        if state:
            self.root.focus_set()

    def start_pomodoro(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED, text="Running...")
            self.set_topmost(False)
            self.root.iconify()
            Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        
        for remaining in range(POMODORO_DURATION, 0, -1):
            self.root.title(f"{remaining:02}' left")
            sleep(60)

        self.is_running = False
        self.pomodoros += 1  # Increment the pomodoros count
        self.root.deiconify()
        self.set_topmost(True)
        self.start_button.config(state=tk.NORMAL, text="Start")
        self.pomodoro_label.config(text=f"Previous pomodoros: {self.pomodoros}")  # Update label
        self.root.title("Pomodoro Timer")

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    PomodoroTimer().run()
