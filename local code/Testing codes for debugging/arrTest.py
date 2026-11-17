import time

class selHorArrow:
    arrChar = '>'
    interval = 1
    def __init__(self,arr = '>', interval = 1):
        self.arrChar = arr
        self.interval = interval
    def getState(self):
        return (time.perf_counter() % self.interval) >= (self.interval/2)
    def print(self):
        if self.getState():
            return f' {self.arrChar}'
        else:
            return f'{self.arrChar} '
        
        
arr = selHorArrow()
while True:
    print("\033[H", end="")  # move this to the appropriate function later
    print(arr.print())