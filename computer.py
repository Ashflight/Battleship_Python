import random

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QLabel, QMainWindow

checked = [[False for i in range(10)] for j in range(10)]
## TODO: reduce code complexity, reduce if/else
def generate_board(): 
    ships = [5, 4, 3, 3, 2]
    oppBoard = [["_" for i in range(10)] for j in range(10)]
    for i in range(5):
        rotation = random.randint(1, 2)
        checker = True
        if (rotation == 1):
            while (checker):
                y = random.randint(0, 10 - ships[i])
                x = random.randint(0, 9)
                for j in range(0, ships[i]):
                    if (oppBoard[y + j][x] != "_"):
                        checker = False
                checker = not checker
            oppBoard[y][x] = "T"
            for k in range(1, ships[i] - 1):
                oppBoard[y + k][x] = "V"
            oppBoard[y + ships[i] - 1][x] = "B"
        else:
            while (checker):
                y = random.randint(0, 9)
                x = random.randint(0, 10 - ships[i])
                for j in range(0, ships[i]):
                    if (oppBoard[y][x + j] != "_"):
                        checker = False
                checker = not checker
            oppBoard[y][x] = "L"
            for k in range(1, ships[i] - 1):
                oppBoard[y][x + k] = "H"
            oppBoard[y][x + ships[i] - 1] = "R"
    return oppBoard

def computer_random_shot(mainWindow : QMainWindow):
    global checked
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    if (checked[y][x]):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
    checked[y][x] = True
    return shoot_player_board(mainWindow, y, x)

trackingOn =  False
trackingHit = (0, 0)
prevShot = (0, 0)
prevHit = False
directionsChecked = [False for i in range(4)]
currentDirection = 0
currentHit = False

## TODO: FIX THIS
def computer_tracking_shot(mainWindow : QMainWindow):
    global trackingOn, trackingHit, prevShot, prevHit, directionsChecked, currentDirection, currentHit
    if (trackingOn): ## targeting turning off early?
        prevHit = currentHit
        if (currentDirection == 0): 
            prevShot = (prevShot[0] + 1, prevShot[1])
            currentHit = shoot_player_board(mainWindow, prevShot[0], prevShot[1])
        elif (currentDirection == 1):
            prevShot = (prevShot[0] - 1, prevShot[1])
            currentHit = shoot_player_board(mainWindow, prevShot[0], prevShot[1])
        elif (currentDirection == 2):
            prevShot = (prevShot[0], prevShot[1] + 1)
            currentHit = shoot_player_board(mainWindow, prevShot[0], prevShot[1])
        else: 
            prevShot = (prevShot[0], prevShot[1] - 1)
            currentHit = shoot_player_board(mainWindow, prevShot[0], prevShot[1])
        if (currentHit[0] == 10):
            directionsChecked[currentDirection] = True
            if (all(directionsChecked) or (prevHit and directionsChecked[0] and directionsChecked[2]) or (prevHit and directionsChecked[1] and directionsChecked[3])):
                trackingOn = False
                directionsChecked = [False for i in range(4)]
                return
            elif (prevHit):
                currentDirection = (currentDirection + 2) % 4
            else:
                while (directionsChecked[currentDirection]):
                    currentDirection = (currentDirection + random.randint(1, 3)) % 4
            prevShot = (trackingHit[0], trackingHit[1])
    else: 
        hit = computer_random_shot(mainWindow)
        if (hit[0] != 10):
            trackingOn = True
            currentDirection = random.randint(0, 3)
            trackingHit = (hit[0], hit[1])
            prevShot = (hit[0], hit[1])
            prevHit = False
            currentHit = True

def shoot_player_board(mainWindow : QMainWindow, y, x):
    mainWindow.moreText.setText("This is your board. The opponent's most recent shot: R: " + str(y) + " C: " + str(x))
    if (mainWindow.playerBoardArray[y][x] != "_"):
        mainWindow.playerBoardArray[y][x] = "X"
        layout = mainWindow.playerBoard.layout()
        image = QLabel()
        image.setPixmap(mainWindow.pixmaps["X"])
        image.setFixedSize(QSize(40, 40))
        image.setContentsMargins(0, 0, 0, 0)
        oldWidget = layout.itemAtPosition(y, x)
        oldWidget = oldWidget.widget()
        layout.removeWidget(oldWidget)
        oldWidget.deleteLater()
        layout.addWidget(image, y, x, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return (y, x)
    return (10, 10)