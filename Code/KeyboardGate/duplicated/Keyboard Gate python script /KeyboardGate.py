import sys
import platform

OS_TYPE = platform.system()

if OS_TYPE == "Windows":
    import msvcrt
else:
    import termios

class KeyboardGate:
    def __init__(self):
        self.os_type = OS_TYPE
        self.old_settings = None

    def KeyboardGateDisable(self):
        if self.os_type == "Windows":
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            try:
                fd = sys.stdin.fileno()
                self.old_settings = termios.tcgetattr(fd)
                new_settings = termios.tcgetattr(fd)
                new_settings[3] = new_settings[3] & ~termios.ECHO
                termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
            except Exception:
                pass

    def KeyboardGateEnable(self):
        if self.os_type == "Windows":
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            if self.old_settings:
                try:
                    fd = sys.stdin.fileno()
                    termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
                except Exception:
                    pass

    def __enter__(self):
        self.KeyboardGateDisable()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.KeyboardGateEnable()