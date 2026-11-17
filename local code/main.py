# سْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
from datetime import date
import shutil
import os
import subprocess
import time
import sys
import ast


# global variables:
class GlobalFrame:
    size = [40, 40]
    screen = []  # globalFrame.text[X][Y]


MAX_FPS = 120
FRAMELENGTH = 40
GOALLENGT = 20
DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]
MONTH = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

Goal = 10000
DEFAULTGOAL = Goal

# Color codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"

# Custom Retro Orange Hex/RGB Palettes
BURNT_ORANGE = "\033[38;2;204;85;0m"  # Classic 70s earthy orange
VINTAGE_AMBER = "\033[38;2;255;176;0m"  # Old CRT terminal phosphor amber
TERRACOTTA = "\033[38;2;224;108;117m"  # Muted clay orange
RETRO_BRIGHT = "\033[38;2;255;110;0m"  # Arcade cabinet style neon orange

# Background variations (Notice the '48' instead of '38')
BG_BURNT = "\033[48;2;204;85;0m"
BG_AMBER = "\033[48;2;255;176;0m"
BG_TERRA = "\033[48;2;224;108;117m"
BG_BRIGHT = "\033[48;2;255;110;0m"
BG_BLACK = "\033[48;2;0;0;0m"

# Style codes
BOLD = "\033[1m"
BOLD_OFF = "\033[22m"
RESET = "\033[0m"


# Calculations -- BUDI
# Counting Total Steps
class calculation:
    def totalSteps(steps):
        total = 0
        for i in range(len(steps)):
            total += steps[i]
        return total

    # Counting Average Steps / Day
    def avgSteps(steps):
        return calculation.totalSteps(steps) / len(steps)

    # Finding Patterns -- ALBERT
    # Finding days that reached the goal
    def daysGoal(steps):
        result = []

        for i in range(len(steps)):
            if steps[i] >= Goal:
                result.append(DAYS[i])

        return result

    def notDaysGoal(steps):
        result = []

        for i in range(len(steps)):
            if steps[i] < Goal:
                result.append(DAYS[i])

        return result

    # Finding Step Trend -- BUDI
    def trend(steps):
        # Average of Halves
        AvgFirstHalf = 0
        for i in range(0, 3):
            AvgFirstHalf += steps[i]
        AvgFirstHalf = AvgFirstHalf / 3

        AvgSecondHalf = 0
        for i in range(4, 7):
            AvgSecondHalf += steps[i]
        AvgSecondHalf = AvgSecondHalf / 3

        if AvgSecondHalf > AvgFirstHalf:
            return "Step trend is going up ↑"
        elif AvgFirstHalf == AvgSecondHalf:
            return "Step trend is static ←→"
        else:
            return "Step trend is going down ↓"


class history:
    log = []

    # format:
    # log = [{
    #     'weekN':1,
    #     'month':0,
    #     'steps':[0,0,0,0,0,0,0],
    #     'goal': ''
    # }]
    def report():
        Frame.clear()
        print(history.log)
        time.sleep(5)

    def load():
        with open("log.txt", "r", encoding="utf-8") as file:
            content = file.read()
            history.log = ast.literal_eval(content)

    def save():
        with open("log.txt", "w", encoding="utf-8") as file:
            file.write(str(history.log))


class input:
    currentKey = None

    class key:
        def up():
            return input.currentKey in (b"\xe0H", "\x1b[A")

        def down():
            return input.currentKey in (b"\xe0P", "\x1b[B")

        def right():
            return input.currentKey in (b"\xe0M", "\x1b[C")

        def left():
            return input.currentKey in (b"\xe0K", "\x1b[D")

        def select():
            return input.currentKey in ("\r", "\n", b"\r", " ")

        def backspace():
            return input.currentKey in (b"\x08", "\x7f", "\x08")

        def pgup():
            return input.currentKey in (b"\xe0I", "\x1b[5~")

        def pgdown():
            return input.currentKey in (b"\xe0Q", "\x1b[6~")

        # def right():
        #     return input.currentKey in

    def inputBound(inputBox, maxVal, sensitivity, minVal=0):
        inputBox.update()
        if input.key.pgup():
            inputBox.content = str(int(inputBox.content) + sensitivity)
        if input.key.pgdown():
            inputBox.content = str(int(inputBox.content) - sensitivity)
        inputBox.content = str(min(int(inputBox.content), maxVal))
        inputBox.content = str(max(int(inputBox.content), minVal))

    def getKey():
        input.currentKey = input.getKey_()

    def getKey_():
        """Returns the pressed key immediately, or None if no key was pressed."""
        # --- Windows Implementation ---
        if sys.platform == "win32":
            import msvcrt

            if msvcrt.kbhit():  # Check if a keypress is waiting in the buffer
                ch = msvcrt.getch()
                if ch in (b"\x00", b"\xe0"):
                    return ch + msvcrt.getch()
                return ch.decode("utf-8", errors="ignore")
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
                    if ch == "\x1b":
                        # Grab the rest of the arrow key sequence characters
                        rlist_seq, _, _ = select.select([sys.stdin], [], [], 0.02)
                        if rlist_seq:
                            ch += sys.stdin.read(3)
                    return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return None


class Draw:
    # 空
    def barReport(sizeY, barWidth, barSpaces, goalHeight, stepsArray):
        xmultiplier = barSpaces + barWidth
        sizeX = 7 * xmultiplier
        # matrix = [[' ' for _ in range(y)] for _ in range(x)]
        frame = [[" " for _ in range(sizeY)] for _ in range(sizeX)]
        barHeights = []
        for day in stepsArray:
            barHeights.append(int(day / Goal * goalHeight))
        goalHeight -= 1
        for y in range(sizeY - 1, -1, -1):
            for x in range(sizeX):
                isFilled = barHeights[int(x / xmultiplier)] > y and (
                    x % xmultiplier < barWidth
                )
                isGoalBar = goalHeight == y
                if isFilled and (not isGoalBar):
                    frame[x][y] = "█"
                elif (not isFilled) and isGoalBar:
                    frame[x][y] = "╌"
                elif isFilled and isGoalBar:
                    frame[x][y] = "▓"
                else:
                    frame[x][y] = " "
                    # frame[x][y] = '□'
                # these are for debugging:
                # frame[x][y] = ("1" if isFilled else '0')
                # frame[x][y] = str(int(x/3))
                # frame[x][y] = str(barHeights[int(x / 3)])
                # frame[x][y] = str(y)
                # frame[x][y] = ("1" if isGoalBar else '0')
            # frame[x][y] = "\n"

        return frame

    def stringify(aFrame):
        psFrame = []
        sizeX, sizeY = len(aFrame), len(aFrame[0])

        for y in reversed(range(sizeY)):
            for x in range(sizeX):
                psFrame.append(aFrame[x][y])
            psFrame.append("\n")
        return "".join(psFrame)

    def listify(sFrame):  # first line must be '\n'
        aFrame_ = [list(line) for line in sFrame.splitlines()]
        del aFrame_[0]
        sizeX, sizeY = len(aFrame_[0]), len(aFrame_)
        aFrame = [[" " for y_ in range(sizeY)] for x_ in range(sizeX)]
        # we need to rotate it tho
        for y in range(sizeY):
            for x in range(sizeX):
                aFrame[x][sizeY - y - 1] = aFrame_[y][x]
        return aFrame

    def insert(posX, posY, inFrame, targetFrame):
        if len(inFrame) == 0:
            return
        sizeXi, sizeYi = len(inFrame), len(inFrame[0])
        sizeXt, sizeYt = len(targetFrame), len(targetFrame[0])
        for y in range(sizeYi):
            for x in range(sizeXi):
                targetFrame[posX + x][posY + y] = inFrame[x][y]

    def getSize(inFrame):
        return [len(inFrame), len(inFrame[0])]

    def box(sizeX, sizeY, Type):
        buffer = [[" " for y_ in range(sizeY)] for x_ in range(sizeX)]

        ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = "┌", "┐", "└", "┘", "─", "│"

        match Type:
            case "light":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "┌",
                    "┐",
                    "└",
                    "┘",
                    "─",
                    "│",
                )
            case "heavy":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "┏",
                    "┓",
                    "┗",
                    "┛",
                    "━",
                    "┃",
                )
            case "double":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "╔",
                    "╗",
                    "╚",
                    "╝",
                    "═",
                    "║",
                )
            case "rounded":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "╭",
                    "╮",
                    "╰",
                    "╯",
                    "─",
                    "│",
                )
            case "dashed":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "┌",
                    "┐",
                    "└",
                    "┘",
                    "╌",
                    "┆",
                )
            case "dotted":
                ltcorn, rtcorn, lbcorn, rbcorn, horizo, vertic = (
                    "┌",
                    "┐",
                    "└",
                    "┘",
                    "┄",
                    "┊",
                )

        for y in range(sizeY):
            buffer[0][y] = vertic
            buffer[sizeX - 1][y] = vertic
        for x in range(sizeX):
            buffer[x][0] = horizo
            buffer[x][sizeY - 1] = horizo
        buffer[0][sizeY - 1] = ltcorn
        buffer[sizeX - 1][0] = rbcorn
        buffer[0][0] = lbcorn
        buffer[sizeX - 1][sizeY - 1] = rtcorn
        return buffer

    class selHorArrow:
        arrChar = ">"
        interval = 1

        def __init__(self, interval=1, arr=">", half=False):
            self.arrChar = arr
            self.interval = interval
            self.half = half

        def getState(self):
            return (time.perf_counter() % self.interval) >= (self.interval / 2)

        def print(self):
            if self.getState() != self.half:
                return f" {self.arrChar}"
            else:
                return f"{self.arrChar} "

    class selVerArrow:

        def __init__(self, interval=1, arr="▲", half=False):
            self.arrChar = arr
            self.interval = interval
            self.half = half

        def getState(self):
            return (time.perf_counter() % self.interval) >= (self.interval / 2)

        def print(self):
            if self.getState() != self.half:
                return f"\n{self.arrChar}\n "
            else:
                return f"\n \n{self.arrChar}"

    class inputBox:
        content = ""
        numbersOnly = True
        limit = 0

        def __init__(self, limit=5, numbersOnly=True, init=""):
            self.numbersOnly = numbersOnly
            self.content = ("0" if numbersOnly else "") if init == "" else init
            self.qwerty = list("qwertyuiopasdfghjklzxcvbnm")
            self.numbers = list("1234567890")
            self.limit = limit

        def update(self):
            if input.currentKey != None:

                if len(self.content) < self.limit:
                    if self.numbersOnly:
                        if input.currentKey in self.numbers:
                            self.content += input.currentKey

                if input.key.backspace():
                    self.content = self.content[: len(self.content) - 1]
                    if self.numbersOnly and self.content == "":
                        self.content = "0"

            return self.content

    class common:
        def pageFrame():
            Draw.insert(
                5,
                0,
                Draw.box(GlobalFrame.size[0] - 9, GlobalFrame.size[1], "heavy"),
                GlobalFrame.screen,
            )

        def date():
            today = f"Date: {str(date.today())}"
            Draw.insert(
                int((GlobalFrame.size[0] - len(today)) - 10),
                int((GlobalFrame.size[1]) - 3),
                list(today),
                GlobalFrame.screen,
            )

        def backButton():
            text = "go back"
            Draw.insert(
                int(13),
                int((GlobalFrame.size[1]) - 3),
                list(text),
                GlobalFrame.screen,
            )

# the pages:
class Page:
    # pages system:
    # currentPage = "ScreenSizeTest"
    # currentPage = "InsertPage"
    currentPage = "HomePage"

    def update():
        # insert the code for drawing here
        # draw pages based on which page it is currently
        match Page.currentPage:
            case "HomePage":
                Page.homePage()
            case "ScreenSizeTest":
                Page.screenSizeTest()
            case "InsertPage":
                Page.insertPage()
            case "HistoryPage":
                Page.historyPage()
            case _:
                Page.notFound()

    def initVar(key, val):  # only run if its not initiated yet
        if not key in Page.variables:
            Page.variables[key] = val

    def pageInitVar(page, key, val):  # only run if its not initiated yet
        Page.initVar(page, {})
        if not key in Page.variables[page]:
            Page.variables[page][key] = val

    variables = {}

    def notFound():
        Draw.common.pageFrame()
        Draw.insert(
            int((GlobalFrame.size[0] - 2) / 2),
            int((GlobalFrame.size[1]) / 2),
            list("404"),
            GlobalFrame.screen,
        )

    def historyPage():
        global Goal
        Draw.common.pageFrame()
        Draw.common.date()
        Draw.common.backButton()
        Page.initVar("historyPage", {})
        Locals = Page.variables["historyPage"]

        historyDict_ = [[] for _ in range(12)]
        historyDict = []  # list of months

        for log in history.log:
            historyDict_[log["month"]].append(log)
        for dict in historyDict_:
            if dict != []:
                historyDict.append(dict)

        elWidth = 6 + 4  # 5 + arrow lenth+ space
        dictSizeX = len(historyDict) * elWidth
        dictSizeY = 12
        dictPosX = int((GlobalFrame.size[0] - dictSizeX) / 2)
        dictPosY = int(GlobalFrame.size[1] * 0.1)
        monthY = dictPosY + dictSizeY - 1

        Page.pageInitVar("historyPage", "steps", [0, 0, 0, 0, 0, 0, 0])
        Page.pageInitVar("historyPage", "goal", 0)

        for monthI in range(len(historyDict)):
            month = historyDict[monthI]
            monthX = dictPosX + (monthI * elWidth)
            Draw.insert(
                monthX,
                monthY,
                list(f'[{"".join(list(MONTH[month[0]["month"]])[:3])}]'),
                GlobalFrame.screen,
            )
            for weekI in range(len(month)):
                week = month[weekI]
                weekN = week["weekN"]
                prefix = "0" if weekN < 10 else ""
                elY = dictPosY + dictSizeY - 4 - (3 * weekI)
                Draw.insert(monthX, elY, Draw.box(6, 3, "light"), GlobalFrame.screen)
                Draw.insert(
                    monthX + 2, elY + 1, list(f"{prefix}{weekN}"), GlobalFrame.screen
                )
        navGuide = "Record of past report, organized by [x]th week of month [n]:"
        Draw.insert(
            int((GlobalFrame.size[0] - len(navGuide)) / 2),
            monthY + 2,
            list(navGuide),
            GlobalFrame.screen,
        )
        Page.pageInitVar("historyPage", "recordCur", [0, 1])
        Page.pageInitVar("historyPage", "maxY", 1)
        maxMonth = len(historyDict)
        maxWeeks = [len(month) for month in historyDict]

        if input.key.down():
            Locals["recordCur"][1] += 1
        if input.key.up():
            Locals["recordCur"][1] -= 1
        Locals["maxY"] = maxWeeks[Locals["recordCur"][0]]
        Locals["recordCur"][1] = max(0, Locals["recordCur"][1])
        Locals["recordCur"][1] = min(Locals["maxY"], Locals["recordCur"][1])


        if Locals["recordCur"][1] == 0:
            Page.pageInitVar("historyPage", "backArr", Draw.selHorArrow(1, "<", False))
            Draw.insert(
                int(10),
                int((GlobalFrame.size[1]) - 3),
                list(Locals["backArr"].print()),
                GlobalFrame.screen,
            )
            if input.key.select():
                Page.currentPage = "HomePage"
        elif Locals["recordCur"][1] != Locals["maxY"] + 1:
            Page.pageInitVar("historyPage", "backArr", Draw.selHorArrow(1, "<", False))
            if input.key.right():
                Locals["recordCur"][0] += 1
            if input.key.left():
                Locals["recordCur"][0] -= 1
            Locals["recordCur"][0] = max(0, Locals["recordCur"][0])
            Locals["recordCur"][0] = min(maxMonth - 1, Locals["recordCur"][0])
            Locals["maxY"] = maxWeeks[Locals["recordCur"][0]]
            Locals["recordCur"][1] = max(0, Locals["recordCur"][1])
            Locals["recordCur"][1] = min(Locals["maxY"], Locals["recordCur"][1])


            Locals["steps"] = historyDict[Locals['recordCur'][0]][Locals['recordCur'][1]-1]["steps"]
            Locals["goal"] = historyDict[Locals['recordCur'][0]][Locals['recordCur'][1]-1]["goal"]
            Locals["weekN"] = historyDict[Locals['recordCur'][0]][Locals['recordCur'][1]-1]["weekN"]
            Locals["monthN"] = historyDict[Locals['recordCur'][0]][Locals['recordCur'][1]-1]["month"]
            Goal = Locals["goal"]
            
            Draw.insert(
                dictPosX + (elWidth * Locals["recordCur"][0]) + 6,
                dictPosY + dictSizeY - 3 - (3 * (Locals["recordCur"][1] - 1)),
                Locals["backArr"].print(),
                GlobalFrame.screen,
            )
            
        # graph
        goalHeight = 15
        graph = Draw.barReport(20, 9, 4, goalHeight, Locals["steps"])
        graphSize = Draw.getSize(graph)
        graphPos = [
            int((GlobalFrame.size[0] - graphSize[0]) / 2),
            monthY + 6,
        ]

        Draw.insert(
            graphPos[0],
            graphPos[1],
            graph,
            GlobalFrame.screen,
        )
        Draw.insert(
            graphPos[0] - 3,
            graphPos[1] - 1,
            ["■" for _ in range(graphSize[0] + 3)],
            GlobalFrame.screen,
        )
        Draw.insert(
            graphPos[0] + graphSize[0] - 3,
            graphPos[1] + goalHeight - 1,
            list(":Goal"),
            GlobalFrame.screen,
        )
        suffix = ""
        match Locals['weekN']:
            case 1:
                suffix = "st"
            case 2:
                suffix = "nd"
            case _:
                suffix = "rd"
        subTitle = f"Step tracking report for {Locals['weekN']}{suffix} week of {MONTH[Locals['monthN']]}"
        Draw.insert(
            int((GlobalFrame.size[0] - len(subTitle)) / 2),
            graphPos[1] + graphSize[1]+1,
            list(subTitle),
            GlobalFrame.screen,
        )
        goalInfo = f'Goal: {Goal}'
        Draw.insert(
            int((GlobalFrame.size[0] - len(goalInfo)) / 2),
            graphPos[1] + graphSize[1],
            list(goalInfo),
            GlobalFrame.screen,
        )

    def insertPage():
        global Goal
        # titleSizeX, titleSizeY = len(title), len(title[0])
        Page.initVar("insertPage", {})
        Locals = Page.variables["insertPage"]

        Draw.common.pageFrame()
        Draw.common.date()
        Draw.common.backButton()
        # Page.pageInitVar(
        #     "insertPage", "steps", [10000, 5000, 15000, 2000, 3000, 5000, 9000]
        # )
        Page.pageInitVar("insertPage", "steps", [0, 0, 0, 0, 0, 0, 0])
        goalHeight = 15
        # barWidth
        graph = Draw.barReport(20, 9, 4, goalHeight, Locals["steps"])
        graphSize = Draw.getSize(graph)
        graphPos = [
            int((GlobalFrame.size[0] - graphSize[0]) / 2),
            int((GlobalFrame.size[1] - graphSize[1]) * 0.7),
        ]

        Draw.insert(
            graphPos[0],
            graphPos[1],
            graph,
            GlobalFrame.screen,
        )
        Draw.insert(
            graphPos[0] + graphSize[0] - 3,
            graphPos[1] + goalHeight - 1,
            list(":Goal"),
            GlobalFrame.screen,
        )
        Draw.insert(
            graphPos[0] - 3,
            graphPos[1] - 1,
            ["■" for _ in range(graphSize[0] + 3)],
            GlobalFrame.screen,
        )
        Draw.insert(
            graphPos[0],
            graphPos[1] - 3,
            list("".join("[       ]    " for _ in range(7))),
            GlobalFrame.screen,
        )

        Page.pageInitVar("insertPage", "selectTab", 1)

        if input.key.down():
            Locals["selectTab"] += 1
            Locals["selectTab"] = min(2, Locals["selectTab"])
        if input.key.up():
            Locals["selectTab"] -= 1
            Locals["selectTab"] = max(0, Locals["selectTab"])

        Page.pageInitVar("insertPage", "textBox", [Draw.inputBox() for _ in range(7)])
        Page.pageInitVar("insertPage", "arrPos", 0)

        textBox = [Locals["textBox"][i].content for i in range(7)]
        marginConstant = 13
        arrPosMargin = marginConstant * Locals["arrPos"]

        for i in range(7):
            Locals["steps"][i] = int(Locals["textBox"][i].content)
            Draw.insert(
                graphPos[0] + 2 + (marginConstant * i),
                graphPos[1] - 3,
                list(textBox[i]),
                GlobalFrame.screen,
            )
            Draw.insert(
                graphPos[0] + 3 + (marginConstant * i),
                graphPos[1] - 2,
                list("".join(list(DAYS[i])[:3])),
                GlobalFrame.screen,
            )

        # Analysis box
        # calculation:
        Steps = Locals["steps"]
        totalSteps = calculation.totalSteps(Steps)
        averageSteps = calculation.avgSteps(Steps)
        goalDays = calculation.daysGoal(Steps)
        notGoalDays = calculation.notDaysGoal(Steps)
        trend = calculation.trend(Steps)

        AnalBoxSize = [81, 12]
        AnalBoxPos = [int((GlobalFrame.size[0] - AnalBoxSize[0]) / 2), graphPos[1] - 6]
        Draw.insert(
            AnalBoxPos[0],
            AnalBoxPos[1] - AnalBoxSize[1],
            Draw.box(AnalBoxSize[0], AnalBoxSize[1], "heavy"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 5, AnalBoxPos[1] - 1, list("Analysis:"), GlobalFrame.screen
        )
        Draw.insert(
            AnalBoxPos[0] + 5,
            AnalBoxPos[1] - 3,
            list(f"Total step: {totalSteps} steps"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 5,
            AnalBoxPos[1] - 6,
            list(f"Average step: {round(averageSteps)} steps"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 5,
            AnalBoxPos[1] - 9,
            list("Trend across the week:"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 5,
            AnalBoxPos[1] - 10,
            list(f"● {trend}"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 40,
            AnalBoxPos[1] - 3,
            Draw.listify("\nDay(s) that   \npass the goal:"),
            GlobalFrame.screen,
        )
        for i in range(len(goalDays)):
            Draw.insert(
                AnalBoxPos[0] + 40,
                AnalBoxPos[1] - 4 - i,
                list(f"{i+1}. {goalDays[i]}"),
                GlobalFrame.screen,
            )

        Draw.insert(
            AnalBoxPos[0] + 60,
            AnalBoxPos[1] - 3,
            Draw.listify("\nDay(s) that  \ndid not pass:"),
            GlobalFrame.screen,
        )
        for i in range(len(notGoalDays)):
            Draw.insert(
                AnalBoxPos[0] + 60,
                AnalBoxPos[1] - 4 - i,
                list(f"{i+1}. {notGoalDays[i]}"),
                GlobalFrame.screen,
            )

        Page.pageInitVar("insertPage", "GoalBoxStyle", "light")
        Page.pageInitVar("insertPage", "DateBoxStyle", "light")
        Page.pageInitVar("insertPage", "SaveBoxStyle", "light")

        # Bottom tabs
        # Goal setting
        BottomSizeY = 5
        BottomYpos = AnalBoxPos[1] - AnalBoxSize[1] - 3
        Draw.insert(
            AnalBoxPos[0],
            BottomYpos - 2,
            Draw.box(24, BottomSizeY, Locals["GoalBoxStyle"]),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 3,
            BottomYpos + BottomSizeY - 3,
            list("Goal:"),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + 3,
            BottomYpos + 0,
            list("Week goal: [     ]"),
            GlobalFrame.screen,
        )
        Page.pageInitVar("insertPage", "GoalTextBox", Draw.inputBox(5, True, str(Goal)))
        Draw.insert(
            AnalBoxPos[0] + 15,
            BottomYpos + 0,
            list(Locals["GoalTextBox"].content),
            GlobalFrame.screen,
        )

        # Date setting
        DatePosX = AnalBoxPos[0] + 31
        Draw.insert(
            DatePosX,
            BottomYpos - 2,
            Draw.box(29, BottomSizeY, Locals["DateBoxStyle"]),
            GlobalFrame.screen,
        )
        Draw.insert(
            DatePosX + 3,
            BottomYpos + BottomSizeY - 3,
            list("Date:"),
            GlobalFrame.screen,
        )
        Page.pageInitVar("insertPage", "weekN", Draw.inputBox(1, True, "1"))
        weekN = int(Locals["weekN"].content)
        suffix = ""
        match weekN:
            case 1:
                suffix = "st"
            case 2:
                suffix = "nd"
            case _:
                suffix = "rd"
        Page.pageInitVar(
            "insertPage", "month", Draw.inputBox(0, True, str(date.today().month - 1))
        )
        monthN = int(Locals["month"].content)
        Draw.insert(
            DatePosX + 2,
            BottomYpos + 0,
            list(f"[{weekN}{suffix}] week of [{MONTH[monthN]}]"),
            GlobalFrame.screen,
        )

        # Save
        Draw.insert(
            AnalBoxPos[0] + AnalBoxSize[0] - 15,
            BottomYpos + BottomSizeY - 6,
            Draw.box(15, 4, Locals["SaveBoxStyle"]),
            GlobalFrame.screen,
        )
        Draw.insert(
            AnalBoxPos[0] + AnalBoxSize[0] - 13,
            BottomYpos + BottomSizeY - 5,
            Draw.listify(
                f"\nSave as {weekN}{suffix}\nweek of {"".join(list(MONTH[monthN])[:3])}"
            ),
            GlobalFrame.screen,
        )
        # highlight the box selected
        Locals["GoalBoxStyle"] = "light"
        Locals["DateBoxStyle"] = "light"
        Locals["SaveBoxStyle"] = "light"

        match Locals["selectTab"]:
            case 0:
                Page.pageInitVar(
                    "insertPage", "backArr", Draw.selHorArrow(1, "<", False)
                )
                Draw.insert(
                    int(10),
                    int((GlobalFrame.size[1]) - 3),
                    list(Locals["backArr"].print()),
                    GlobalFrame.screen,
                )
                if input.key.select():
                    Page.currentPage = "HomePage"
            case 1:
                Page.pageInitVar("insertPage", "arr1", Draw.selHorArrow(1, "◄", False))
                Page.pageInitVar("insertPage", "arr2", Draw.selHorArrow(1, "►", True))
                arr1 = Locals["arr1"].print()
                arr2 = Locals["arr2"].print()
                if input.key.right():
                    Locals["arrPos"] += 1
                if input.key.left():
                    Locals["arrPos"] -= 1
                Locals["arrPos"] %= 7

                arrPos1 = [
                    graphPos[0] - 2,
                    graphPos[1] - 3,
                ]
                arrPos2 = [
                    graphPos[0] + 9,
                    graphPos[1] - 3,
                ]

                Draw.insert(
                    arrPos1[0] + arrPosMargin,
                    arrPos1[1],
                    list(arr1),
                    GlobalFrame.screen,
                )
                Draw.insert(
                    arrPos2[0] + arrPosMargin,
                    arrPos2[1],
                    list(arr2),
                    GlobalFrame.screen,
                )
                # up and down interaction
                sensitivity = 500
                maxSteps = int(Goal * (5 / 4))
                input.inputBound(
                    Locals["textBox"][Locals["arrPos"]], maxSteps, sensitivity
                )
                guideText = "<Increase and Decrease each value with Pgup and PgDown or type them directly>"
                Draw.insert(
                    int((GlobalFrame.size[0] - len(guideText)) / 2),
                    graphPos[1] - 5,
                    list(guideText),
                    GlobalFrame.screen,
                )
            case 2:
                Page.pageInitVar("insertPage", "horTabSel", 0)
                if input.key.right():
                    Locals["horTabSel"] += 1
                if input.key.left():
                    Locals["horTabSel"] -= 1
                Locals["horTabSel"] = max(0, Locals["horTabSel"])
                Locals["horTabSel"] = min(3, Locals["horTabSel"])

                def dateGuideText():
                    guideText = "<PgUp or PgDown>"
                    Draw.insert(
                        DatePosX + 7,
                        BottomYpos - 3,
                        list(guideText),
                        GlobalFrame.screen,
                    )

                match Locals["horTabSel"]:
                    # Goal box
                    case 0:
                        Locals["GoalBoxStyle"] = "double"
                        guideText = "<PgUp or PgDown or type>"
                        input.inputBound(Locals["GoalTextBox"], 20000, 1000, 1)
                        Goal = int(Locals["GoalTextBox"].content)
                        Draw.insert(
                            AnalBoxPos[0] + 1,
                            BottomYpos - 3,
                            list(guideText),
                            GlobalFrame.screen,
                        )
                        xMargin = 17
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos + 1,
                            list("▲"),
                            GlobalFrame.screen,
                        )
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos - 1,
                            list("▼"),
                            GlobalFrame.screen,
                        )
                    # Date box style
                    case 1:
                        Locals["DateBoxStyle"] = "double"
                        input.inputBound(Locals["weekN"], 4, 1, 1)
                        dateGuideText()
                        xMargin = 35
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos + 1,
                            list("▲"),
                            GlobalFrame.screen,
                        )
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos - 1,
                            list("▼"),
                            GlobalFrame.screen,
                        )
                    # Date 2
                    case 2:
                        Locals["DateBoxStyle"] = "double"
                        input.inputBound(Locals["month"], 11, 1, 0)
                        dateGuideText()
                        xMargin = 48 + int(len(MONTH[monthN]) / 2)
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos + 1,
                            list("▲"),
                            GlobalFrame.screen,
                        )
                        Draw.insert(
                            AnalBoxPos[0] + xMargin,
                            BottomYpos - 1,
                            list("▼"),
                            GlobalFrame.screen,
                        )
                    # save box style
                    case 3:
                        Locals["SaveBoxStyle"] = "double"
                        guideText = "<Enter to confirm>"
                        Draw.insert(
                            AnalBoxPos[0] + AnalBoxSize[0] - 16,
                            BottomYpos - 2,
                            list(guideText),
                            GlobalFrame.screen,
                        )
                        if input.key.select():
                            history.log.append(
                                {
                                    "id": monthN * 4 + weekN,
                                    "weekN": weekN,
                                    "month": monthN,
                                    "steps": Locals["steps"],
                                    "goal": Goal,
                                }
                            )
                            history.log.sort(key=lambda x: x["id"])
                            # reset memory
                            Locals["weekN"].content = "1"
                            Locals["month"].content = str(date.today().month - 1)
                            # Locals["steps"] = [0, 0, 0, 0, 0, 0, 0]
                            for i in range(7):
                                Locals["textBox"][i].content = "0"
                            Locals["GoalTextBox"].content = str(DEFAULTGOAL)
                            history.save()
                            history.load()
        title = "( Insert log new data )"
        Draw.insert(
            int((GlobalFrame.size[0] - len(title)) / 2),
            GlobalFrame.size[1] - 3,
            list(title),
            GlobalFrame.screen,
        )
        subTitle = f"Step tracking report for {weekN}{suffix} week of {MONTH[monthN]}"
        Draw.insert(
            int((GlobalFrame.size[0] - len(subTitle)) / 2),
            graphPos[1] + graphSize[1],
            list(subTitle),
            GlobalFrame.screen,
        )

    def homePage():
        Page.initVar("homePage", {})
        Locals = Page.variables["homePage"]
        Draw.common.pageFrame()
        Draw.common.date()

        boxSizeX, boxSizeY = 40, 9
        SelectBoxPos = [
            int((GlobalFrame.size[0] - boxSizeX) / 2),
            int((GlobalFrame.size[1] - boxSizeY) / 5),
        ]
        # Select box
        Draw.insert(
            SelectBoxPos[0],
            SelectBoxPos[1],
            Draw.box(boxSizeX, boxSizeY, "light"),
            GlobalFrame.screen,
        )
        Draw.insert(
            SelectBoxPos[0] + 4,
            SelectBoxPos[1] + boxSizeY - 1,
            list("Menu:"),
            GlobalFrame.screen,
        )
        # Select text
        SelectTextPos = [
            [  # "Open history"
                SelectBoxPos[0] + 8,
                SelectBoxPos[1] + boxSizeY - 3,
            ],
            [  # "Insert new data"
                SelectBoxPos[0] + 8,
                SelectBoxPos[1] + boxSizeY - 5,
            ],
            [  # "exit"
                SelectBoxPos[0] + 8,
                SelectBoxPos[1] + boxSizeY - 7,
            ],
        ]
        Draw.insert(
            SelectTextPos[0][0],
            SelectTextPos[0][1],
            list("Open history"),
            GlobalFrame.screen,
        )
        Draw.insert(
            SelectTextPos[1][0],
            SelectTextPos[1][1],
            list("Insert new data"),
            GlobalFrame.screen,
        )
        Draw.insert(
            SelectTextPos[2][0],
            SelectTextPos[2][1],
            list("Exit"),
            GlobalFrame.screen,
        )
        # Select arrow
        # input system:
        Page.pageInitVar("homePage", "arrPos", 0)
        if input.key.down():
            Locals["arrPos"] += 1
        if input.key.up():
            Locals["arrPos"] -= 1
        Locals["arrPos"] %= 3

        Page.pageInitVar("homePage", "arr1", Draw.selHorArrow())
        arr = Locals["arr1"].print()
        Draw.insert(
            SelectTextPos[Locals["arrPos"]][0] - 3,
            SelectTextPos[Locals["arrPos"]][1],
            list(arr),
            GlobalFrame.screen,
        )
        # selecting one of them:
        if input.key.select():
            match Locals["arrPos"]:
                case 0:
                    Page.currentPage = "HistoryPage"
                case 1:
                    Page.currentPage = "InsertPage"
                case 2:
                    exit()

        title = Draw.listify(
            """
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
███████╗██╔████╔██║███████║██████╔╝   ██║   ██║ █╗ ██║███████║   ██║   ██║     ███████║
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝"""
        )
        titleSize = Draw.getSize(title)
        Draw.insert(
            int((GlobalFrame.size[0] - titleSize[0]) / 2),
            (GlobalFrame.size[1] - 10),
            title,
            GlobalFrame.screen,
        )
        subtitle = Draw.listify("""
┏┓ ╻ ╻   ┏━╸┏━┓┏━┓╻ ╻┏━┓   ╻ ╻
┣┻┓┗┳┛   ┃╺┓┣┳┛┃ ┃┃ ┃┣━┛   ┗━┫
┗━┛ ╹    ┗━┛╹┗╸┗━┛┗━┛╹       ╹""")
        subtitleSize = Draw.getSize(subtitle)
        Draw.insert(
            int((GlobalFrame.size[0] - subtitleSize[0]) / 2),
            (GlobalFrame.size[1] - 14),
            subtitle,
            GlobalFrame.screen,
        )

    def screenSizeTest():
        text = list(str(GlobalFrame.size[0]) + ", " + str(GlobalFrame.size[1]))
        Draw.insert(
            5,
            0,
            Draw.box(GlobalFrame.size[0] - 9, GlobalFrame.size[1], "light"),
            GlobalFrame.screen,
        )
        Draw.insert(
            int((GlobalFrame.size[0] - len(text)) / 2),
            int(GlobalFrame.size[1] / 2),
            (text),
            GlobalFrame.screen,
        )


class Frame:
    # frame system:
    def update():
        Page.update()

    def clear():
        # Determine the correct command based on OS ('cls' for Windows, 'clear' for Linux/macOS)
        command = "cls" if os.name == "nt" else "clear"
        # Run the command safely without a manual shell wrapper
        subprocess.run([command], shell=True)
        Frame.removeCursor()

    def removeCursor():
        sys.stdout.write("\033[?25l")

    def updateGlobalFrame(x, y):
        global GlobalFrame
        GlobalFrame.size = [x, y]
        # matrix = [[' ' for _ in range(y)] for _ in range(x)]
        GlobalFrame.screen = [
            [" " for y_ in range(GlobalFrame.size[1])]
            for x_ in range(GlobalFrame.size[0])
        ]
        Frame.update()
        Frame.removeCursor()

    def checkGlobalFrameSize():
        size = shutil.get_terminal_size()
        x, y = (
            size.columns,
            size.lines - 3,
        )  # this margin of -2 is quite important to avoid overflow
        if not (x == GlobalFrame.size[0] and y == GlobalFrame.size[1]):
            Frame.updateGlobalFrame(x, y)


def main():
    0
    # clear_terminal()
    input.getKey()
    print("\033[H", end="")  # move this to the appropriate function later
    print(RETRO_BRIGHT)
    Frame.checkGlobalFrameSize()
    Frame.update()
    print(Draw.stringify(GlobalFrame.screen))
    # page.screenTest()

    time.sleep(1 / MAX_FPS)


Frame.clear()
history.load()

while True:
    main()