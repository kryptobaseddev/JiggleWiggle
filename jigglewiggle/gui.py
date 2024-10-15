import tkinter as tk
import time
from threading import Thread
from jigglewiggle.jiggler import MouseJiggler
from jigglewiggle.utils import StopEvent

class JigglerApp:
    def __init__(self, app_version, latest_version=None):
        self.app_version = app_version
        self.latest_version = latest_version
        self.state = "Disabled"
        self.IDLE_TIME_SECONDS = 15
        self.idle_time = 0
        self.stop_event = StopEvent()

    def run(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("JiggleWiggle")
        self.window.resizable(False, False)

        # Set the custom icon
        self.set_window_icon()

        # Display the current app version
        self.add_version_label()

        # Add a status indicator
        self.add_status_indicator()

        # Add idle time label and timeout settings
        self.add_idle_and_timeout_widgets()

        # Add toggle button to start/stop jiggling and close button
        self.add_control_buttons()

        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a MouseJiggler instance
        self.jiggler = MouseJiggler()

        # Start the GUI main loop
        self.window.mainloop()

    def set_window_icon(self):
        """Set the custom icon for the window."""
        try:
            icon_path = self.resource_path('assets/icon.ico')
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error loading icon: {e}")

    def add_version_label(self):
        """Display the current app version."""
        self.version_label = tk.Label(self.window, text=f"Version: {self.app_version}")
        self.version_label.grid(row=0, column=0, padx=20, pady=10)

    def add_status_indicator(self):
        """Add a label to indicate current status."""
        self.indicator = tk.Label(self.window, text=f"Status: {self.state}", bg='red', width=20, relief=tk.RAISED)
        self.indicator.grid(row=1, column=0, padx=20, pady=10)

    def add_idle_and_timeout_widgets(self):
        """Add widgets for idle time and timeout setting."""
        self.idle_time_label = tk.Label(self.window, text=f"Idle Time: {self.idle_time} seconds")
        self.idle_time_label.grid(row=1, column=1, padx=20, pady=10)

        self.timeout_label = tk.Label(self.window, text=f"Timeout: {self.IDLE_TIME_SECONDS} seconds")
        self.timeout_label.grid(row=2, column=0, padx=20, pady=10)

        self.timeout_entry = tk.Entry(self.window, width=10)
        self.timeout_entry.grid(row=2, column=1, padx=20, pady=10)

        self.timeout_button = tk.Button(self.window, text="Set Timeout", command=self.set_timeout)
        self.timeout_button.grid(row=2, column=2, padx=20, pady=10)

    def add_control_buttons(self):
        """Add control buttons to start/stop the jiggler and close the application."""
        self.toggle_button = tk.Button(self.window, text="Turn On", command=self.toggle_jiggle)
        self.toggle_button.grid(row=3, column=0, padx=20, pady=10)

        self.close_button = tk.Button(self.window, text="Close", command=self.on_closing)
        self.close_button.grid(row=3, column=1, padx=20, pady=10)

    def toggle_jiggle(self):
        """Toggle the mouse jiggling process."""
        if self.state == "Disabled":
            self.state = "Idle"
            self.toggle_button.config(text="Turn Off")
            self.stop_event.clear()  # Reset the stop event
            Thread(target=self.jiggle_mouse).start()
        else:
            self.state = "Disabled"
            self.stop_event.set()  # Stop the thread
            self.toggle_button.config(text="Turn On")
            self.update_indicator()

    def set_timeout(self):
        """Set the idle time before the mouse starts to jiggle."""
        try:
            self.IDLE_TIME_SECONDS = int(self.timeout_entry.get())
            self.timeout_label.config(text=f"Timeout: {self.IDLE_TIME_SECONDS} seconds")
        except ValueError:
            self.timeout_label.config(text="Please enter a valid number.")

    def jiggle_mouse(self):
        """Jiggle the mouse if idle time exceeds the threshold."""
        while not self.stop_event.is_set():
            self.idle_time = self.jiggler.get_idle_time()
            self.idle_time_label.config(text=f"Idle Time: {self.idle_time} seconds")

            if self.idle_time > self.IDLE_TIME_SECONDS:
                self.state = "Active"
                self.update_indicator()
                self.jiggler.jiggle_mouse()
            else:
                self.state = "Idle"
                self.update_indicator()

            time.sleep(1)

    def update_indicator(self):
        """Update the state indicator."""
        self.indicator.config(text=f"Status: {self.state}")

        if self.state == "Disabled":
            self.indicator.config(bg='red')
        elif self.state == "Idle":
            self.indicator.config(bg='yellow', fg='black')
        else:
            self.indicator.config(bg='green', fg='white')

    def on_closing(self):
        """Handle the window close event."""
        self.stop_event.set()  # Ensure the jiggle thread is stopped
        self.window.destroy()
