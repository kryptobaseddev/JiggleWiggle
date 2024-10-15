import pyautogui
import time
import ctypes

class MouseJiggler:
    def __init__(self, idle_time_seconds=15):
        self.idle_time_seconds = idle_time_seconds

    def get_idle_time(self):
        """Get the idle time in seconds."""
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

        last_input_info = LASTINPUTINFO()
        last_input_info.cbSize = ctypes.sizeof(last_input_info)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))

        millis = ctypes.windll.kernel32.GetTickCount() - last_input_info.dwTime
        return int(millis / 1000.0)

    def jiggle_mouse(self):
        """Jiggle the mouse."""
        current_mouse_x, current_mouse_y = pyautogui.position()
        pyautogui.moveTo(current_mouse_x + 5, current_mouse_y + 5)
        time.sleep(1)
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
