def listify(sFrame): #first line must be '\n'
    aFrame_ = [list(line) for line in sFrame.splitlines()]
    del aFrame_[0]
    sizeX, sizeY = len(aFrame_[0]), len(aFrame_)
    aFrame = [
        [" " for y_ in range(sizeY)]
        for x_ in range(sizeX)
    ]
    # we need to rotate it tho
    for y in range(sizeY):
        for x in range(sizeX):
            aFrame[x][y] = aFrame_[y][x]
    return aFrame
            
title = """
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
███████╗██╔████╔██║███████║██████╔╝   ██║   ██║ █╗ ██║███████║   ██║   ██║     ███████║
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝"""

print(listify('''
123
456
'''))