from multiprocessing.connection import Listener
import subprocess
import sys
import time


class logger:
    port = None
    listener = None
    conn = None
    def init():
# 1. Start listener on port 0 (OS assigns a guaranteed free port)
        logger.listener = Listener(('localhost', 0), authkey=b'secret')
        logger.port = logger.listener.address[1]
    # 2. Launch Script B in a new console window, passing the port
        subprocess.Popen(
            [sys.executable, "logger.py", str(logger.port)],
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Windows pop-out terminal
        )
        logger.conn = logger.listener.accept()
    def send(msg):
        try:
            logger.conn.send(msg)
        except ConnectionResetError:
            logger.init()
            logger.send(msg)
        

logger.init()
# 3. Wait for Script B to connect

# 4. Stream data directly into the pop-out window
# conn.send({"angle": 45, "grid": [[1, 2], [3, 4]]})
# conn.send({"angle": 90, "grid": [[5, 6], [7, 8]]})
while True:
    logger.send(input())


conn.close()
listener.close()