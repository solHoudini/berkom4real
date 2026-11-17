import sys
import time

timestamp = time.perf_counter()

def get_key():
    """Reads a single keypress without waiting for Enter."""
    # Windows System
    if sys.platform == "win32":
        import msvcrt
        # Double lookups handle special keys like arrows
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            return ch + msvcrt.getch()
        return ch.decode('utf-8', errors='ignore')
        
    # Unix Systems (Linux / macOS)
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# --- Main Game/App Loop ---
print("Press any key to test (Press 'q' to exit)...")
while True:
    new_time = time.perf_counter()
    print(int(new_time - timestamp))
    timestamp = new_time
    key = get_key()
    print('ra')
    if key == 'q':
        print("\nExiting...")
        break
    elif key == 'w':
        print("\nMoved Up!")
    else:
        print(f"\nYou pressed: {key}")
