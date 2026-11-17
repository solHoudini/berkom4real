import sys
import time
import select

def getKey():
    """Returns the pressed key immediately, or None if no key was pressed."""
    # --- Windows Implementation ---
    if sys.platform == "win32":
        import msvcrt
        if msvcrt.kbhit():  # Check if a keypress is waiting in the buffer
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                return ch + msvcrt.getch()
            return ch.decode('utf-8', errors='ignore')
        return None  # No key pressed, instantly keep going

    # --- Linux / macOS Implementation ---
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # Use select with a 0-second timeout to check for input instantly
            rlist, _, _ = select.select([sys.stdin], [], [], 0.0)
            if rlist:
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    # Grab the rest of the arrow key sequence characters
                    rlist_seq, _, _ = select.select([sys.stdin], [], [], 0.02)
                    if rlist_seq:
                        ch += sys.stdin.read(2)
                return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
# Setup your grid tracking variables
x_index = 0
y_index = 0

print("Live TUI Engine Started. Press Arrow Keys to move. Press 'q' to quit.")

while True:
    # 1. Grab any instant input (will NOT freeze the loop)
    key = getKey()

    if key == 'q':
        print("\r\nExiting live loop...")
        break

    # 2. Process Input Actions
    if key in (b'\xe0H', '\x1b[A'):
        y_index -= 1
        print(f"\rMove Up! Pos: ({x_index}, {y_index})    ", end="")
    elif key in (b'\xe0P', '\x1b[B'):
        y_index += 1
        print(f"\rMove Down! Pos: ({x_index}, {y_index})  ", end="")
    elif key in (b'\xe0K', '\x1b[D'):
        x_index -= 1
        print(f"\rMove Left! Pos: ({x_index}, {y_index})  ", end="")
    elif key in (b'\xe0M', '\x1b[C'):
        x_index += 1
        print(f"\rMove Right! Pos: ({x_index}, {y_index}) ", end="")
    # print("\033[H", end="")  # move this to the appropriate function later
    # print(x_index,y_index)
    if key != None:
        print(key)
    if key in ('\r', '\n', b'\r', ' '):
        print("\r\n[ENTER KEY PRESSED! Triggering action...]")
        
    # 3. Live Background Process (Proof that the loop never blocks!)
    # This keeps ticking constantly even when you leave the keyboard completely untouched
    current_time = time.strftime("%H:%M:%S")
    # Print the time at the edge of the terminal frame
    # (Using \r and end="" lets us overwrite the same line like a live HUD)
    # print(f"\r[Live Clock: {current_time}] Position: ({x_index}, {y_index})   ", end="")

    # 4. Cap the game loop speed (e.g., ~60 frames per second)
    time.sleep(1 / 60)
