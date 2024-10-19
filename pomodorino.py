import tkinter as tk
import ctypes
import time
import threading
import sys, os.path

# Timer settings
POMODORO_DURATION = 25 * 60  # For testing purposes

# Function to make the window stay on top across all desktops (Windows-specific)
def set_always_on_top(hwnd):
    HWND_TOPMOST = -1
    SWP_NOSIZE = 0x0001
    SWP_NOMOVE = 0x0002
    SWP_SHOWWINDOW = 0x0040
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                      SWP_NOSIZE | SWP_NOMOVE | SWP_SHOWWINDOW)
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.is_running = False
        self.create_window()  # Create the initial window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close gracefully

    def center_window(self):
        window_width = 300  # Set the window width
        window_height = 100  # Set the window height

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the window's position
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_window(self):
        """Create the Pomodoro window"""
        self.center_window()
        self.root.iconbitmap(resource_path('pomodoro_77K_1.ico'))
        self.root.configure(bg="black")  # Set the background color of the window
        self.root.title("Pomodoro Timer")

        # Ensure the window stays on top until the timer starts
        self.root.attributes('-topmost', True)

        # Create a large button that fills the window
        self.start_button = tk.Button(self.root, text="Start", font=("Arial", 30), command=self.start_pomodoro)
        self.start_button.config(bg="white", fg="black")  # Set button background and text color
        self.start_button.pack(expand=True, fill="both", padx=20, pady=20)

    def minimize_window(self):
        """Minimize the window to the taskbar"""
        self.root.iconify()

    def show_window(self):
        """Show the window and bring it to the top"""
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        # Ensure the window stays on top across all virtual desktops
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        set_always_on_top(hwnd)

    def start_pomodoro(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED, text="Running...")  # Disable button during the Pomodoro
            self.minimize_window()  # Minimize when Pomodoro starts
            threading.Thread(target=self.run_timer, args=(POMODORO_DURATION,)).start()

    def run_timer(self, duration):
        remaining_time = duration
        while remaining_time > 0:
            mins, secs = divmod(remaining_time, 60)
            time_format = f"{mins:02}:{secs:02}"
            
            # Update the window title with time left
            self.root.title(f"Time Left: {time_format}")
            
            # Sleep for 1 second
            time.sleep(1)
            remaining_time -= 1

        # When time is up, bring the window back to the front
        self.is_running = False
        self.show_window()  # Show the window
        self.start_button.config(state=tk.NORMAL, text="Start")  # Reset button text

        # Reset the title to its default
        self.root.title("Pomodoro Timer")

    def on_closing(self):
        """Handle window close event gracefully"""
        if self.is_running:
            self.is_running = False  # Stop the timer if it's running
        self.root.destroy()  # Close the window gracefully

# Main application loop
root = tk.Tk()
timer_app = PomodoroTimer(root)
root.mainloop()


# // <a href="https://www.flaticon.com/free-icons/pomodoro" title="pomodoro icons">Pomodoro icons created by andinur - Flaticon</a>