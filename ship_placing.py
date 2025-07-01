from game import create_screen

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QTransform
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QWidget, QVBoxLayout

def create_placing_screen(mainWindow : QMainWindow):
    ships = [5, 4, 3, 3, 2]
    shipNames = ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"]
    mainWindow.pixmaps = getPixmaps() ## expand as needed, integrate hit and unknown graphics as needed

    layout = QVBoxLayout()

    mainWindow.instructions = QLabel("You are about to place your Carrier, it is 5 units long.")
    mainWindow.instructions.setFixedHeight(50)
    layout.addWidget(mainWindow.instructions)

    rotationLayout = QHBoxLayout()
    rotationLayout.addWidget(QLabel("Pick a rotation: "))
    horizontal = QPushButton("Horizontal")
    horizontal.clicked.connect(lambda: rotation_selected(False, mainWindow))
    rotationLayout.addWidget(horizontal)
    vertical = QPushButton("Vertical")
    vertical.clicked.connect(lambda: rotation_selected(True, mainWindow))
    rotationLayout.addWidget(vertical)
    rotation = QWidget()
    rotation.setFixedHeight(50)
    rotation.setLayout(rotationLayout)
    layout.addWidget(rotation)

    display = QGridLayout()
    for i in range(10):
        for j in range(10):
            button = QPushButton()
            button.setIcon(QIcon(QPixmap('C:/mandy/myPython/battleship/miss.png')))
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.setIconSize(QSize(40, 40))
            button.setFixedSize(QSize(40, 40))
            button.setContentsMargins(0, 0, 0, 0)
            button.setStyleSheet("margin: 0px; padding: 0px; border: none;")
            button.setObjectName(str(i) + str(j))
            button.clicked.connect(lambda  _, b=button: grid_clicked(mainWindow, b, ships, shipNames))
            display.addWidget(button, i, j, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) 
    display.setSpacing(0)
    display.setContentsMargins(0, 0, 0, 0)
    mainWindow.playerBoard = QWidget()
    mainWindow.playerBoard.setFixedSize(QSize(400, 400))
    mainWindow.playerBoard.setLayout(display)
    layout.addWidget(mainWindow.playerBoard, alignment = Qt.AlignmentFlag.AlignHCenter)

    widget = QWidget()
    widget.setLayout(layout)
    mainWindow.setCentralWidget(widget) 

def rotation_selected(isVertical, mainWindow : QMainWindow):
    mainWindow.placingRotation = isVertical
    if (isVertical): 
        mainWindow.instructions.setText("Click a grid spot to place the top of the ship.")
    else: 
        mainWindow.instructions.setText("Click a grid spot to place the left end of the ship.")

def grid_clicked(mainWindow, button : QPushButton, ships, shipNames):
    coordstr = button.objectName()
    y = int(coordstr[0:1])
    x = int(coordstr[1:2])
    place_ship(mainWindow, x, y, ships)
    if (mainWindow.placingIndex > 4):
        create_screen(mainWindow)
        return
    mainWindow.instructions.setText("You are about to place your " + shipNames[mainWindow.placingIndex] + ", it is " + str(ships[mainWindow.placingIndex]) + " units long.")

def place_ship(mainWindow : QMainWindow, x, y, ships):
    if (mainWindow.placingRotation):
        if (y + ships[mainWindow.placingIndex] - 1 > 9):
            show_popup(mainWindow, "Bottom Out Of Bounds", "You attempted to place this ship out of bounds.")
            return
        else: 
            mainWindow.playerBoardArray[y][x] = "T"
            for i in range(1, ships[mainWindow.placingIndex] - 1):
                if (mainWindow.playerBoardArray[y + i][x] != "_"):
                    mainWindow.playerBoardArray[y][x] = "_"
                    show_popup(mainWindow, "Overlaps With Existing Ship - Vertical", "You attempted to place this ship on top of a previously placed ship.")
                    return
            if (mainWindow.playerBoardArray[y + ships[mainWindow.placingIndex] - 1][x] != "_"): 
                mainWindow.playerBoardArray[y][x] = "_"
                show_popup(mainWindow, "Overlaps With Existing Ship - Vertical Final", "You attempted to place this ship on top of a previously placed ship.") 
                return
            for i in range(1, ships[mainWindow.placingIndex] - 1):
                mainWindow.playerBoardArray[y + i][x] = "V"
            mainWindow.playerBoardArray[y + ships[mainWindow.placingIndex] - 1][x] = "B"
    else:
        if (x + ships[mainWindow.placingIndex] - 1 > 9):
            show_popup(mainWindow, "Right Side Out Of Bounds", "You attempted to place this ship out of bounds.")
            return
        else:
            mainWindow.playerBoardArray[y][x] = "L"
            for i in range(1, ships[mainWindow.placingIndex] - 1): 
                if (mainWindow.playerBoardArray[y][x + i] != "_"):
                    mainWindow.playerBoardArray[y][x] = "_"
                    show_popup(mainWindow, "Overlaps With Existing Ship - Horizontal", "You attempted to place this ship on top of a previously placed ship.")
                    return
            if (mainWindow.playerBoardArray[y][x + ships[mainWindow.placingIndex] - 1] != "_"):
                mainWindow.playerBoardArray[y][x] = "_"
                show_popup(mainWindow, "Overlaps With Existing Ship - Horizontal Final", "You attempted to place this ship on top of a previously placed ship.") 
                return
            for i in range(1, ships[mainWindow.placingIndex] - 1):
                mainWindow.playerBoardArray[y][x + i] = "H"
            mainWindow.playerBoardArray[y][x + ships[mainWindow.placingIndex] - 1] = "R"
    mainWindow.placingIndex += 1
    update_display(mainWindow)

def update_display(mainWindow : QMainWindow):
    layout = mainWindow.playerBoard.layout()
    for i in range(10):
        for j in range(10):
            if (mainWindow.playerBoardArray[i][j] != "_"):
                image = QLabel()
                image.setPixmap(mainWindow.pixmaps[mainWindow.playerBoardArray[i][j]])
                image.setFixedSize(QSize(40, 40))
                image.setContentsMargins(0, 0, 0, 0)
                oldWidget = layout.itemAtPosition(i, j)
                oldWidget = oldWidget.widget()
                layout.removeWidget(oldWidget)
                oldWidget.deleteLater()
                layout.addWidget(image, i, j, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft) 
    mainWindow.playerBoard.setLayout(layout)

def getPixmaps():
    pixmaps = {}
    shipEndPixmap = QPixmap('C:/mandy/myPython/battleship/ship_end.png')
    pixmaps["L"] = shipEndPixmap

    rotate90 = QTransform()
    rotate90.rotate(90)
    endT = shipEndPixmap.transformed(rotate90)
    pixmaps["T"] = endT

    endR = endT.transformed(rotate90)
    pixmaps["R"] = endR

    endB = endR.transformed(rotate90)
    pixmaps["B"] = endB

    shipMiddlePixmap = QPixmap('C:/mandy/myPython/battleship/ship_middle.png')
    pixmaps["H"] = shipMiddlePixmap

    middleV = shipMiddlePixmap.transformed(rotate90)
    pixmaps["V"] = middleV

    pixmaps["_"] = QPixmap('C:/mandy/myPython/battleship/miss.png')

    pixmaps["X"] = QPixmap('C:/mandy/myPython/battleship/hit.png')
    return pixmaps

def show_popup(parent, e, message):
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setWindowTitle("Error: " + e)
    msg_box.setText(message + " Try again.")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()  