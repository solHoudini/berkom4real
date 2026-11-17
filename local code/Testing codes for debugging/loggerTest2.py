from multiprocessing.connection import Client
import traceback
import sys
import subprocess
import time
subprocess.run("", shell=True)  # Enables ANSI colors in Windows pop-out console
RETRO_BRIGHT = "\033[38;2;255;110;0m"  # Arcade cabinet style neon orange

print(RETRO_BRIGHT)
try:
    # Grab the port passed by Script A
    port = int(sys.argv[1])

    with Client(('localhost', port), authkey=b'secret') as conn:
        while True:
            msg = conn.recv()
            if msg == "EXIT":
                break
            # Everything printed here shows up in the pop-out terminal!
            print(f'{time.strftime("%H:%M:%S")} -> {msg}')

    # input("Done! Press Enter to close window...")

except EOFError:
    print('ok im done')
except Exception:
    traceback.print_exc()
    input("Crashed! Press Enter to close...")
    