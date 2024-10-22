import tkinter as tk
from time import sleep
from threading import Thread
from pathlib import Path

POMODORO_DURATION = 25 * 60  # 25 minutes

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.is_running = False
        self.create_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Map>", lambda e: self.set_topmost(True) if not self.is_running else None)

    def create_window(self):
        self.root.geometry('300x100+%d+%d' % (
            (self.root.winfo_screenwidth() - 300) // 2,
            (self.root.winfo_screenheight() - 100) // 2
        ))
        
        icon_path = Path('pomodoro_77K_1.ico')
        if icon_path.exists():
            self.root.iconbitmap(icon_path)
            
        self.root.configure(bg="black")
        self.root.title("Pomodoro Timer")
        self.set_topmost(True)

        self.start_button = tk.Button(
            self.root, 
            text="Start",
            font=("Arial", 30),
            command=self.start_pomodoro,
            bg="white",
            fg="black"
        )
        self.start_button.pack(expand=True, fill="both", padx=20, pady=20)

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
            mins, secs = divmod(remaining, 60)
            self.root.title(f"{mins:02}:{secs:02}")
            sleep(1)

        self.is_running = False
        self.root.deiconify()
        self.set_topmost(True)
        self.start_button.config(state=tk.NORMAL, text="Start")
        self.root.title("Pomodoro Timer")

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    PomodoroTimer().run()