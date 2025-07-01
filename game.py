from computer import computer_random_shot, computer_tracking_shot, generate_board

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QGridLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QWidget, QVBoxLayout

def create_screen(mainWindow : QMainWindow,):
    layout = QVBoxLayout()

    mainWindow.oppBoardArray = generate_board()

    mainWindow.instructions.setText("This is the opponent's board. Click to shoot.")
    layout.addWidget(mainWindow.instructions)
    oppBoardLayout = QGridLayout()
    for i in range(10):
        for j in range(10):
            button = QPushButton()
            button.setIcon(QIcon(QPixmap('C:/mandy/myPython/battleship/unknown.png')))
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.setIconSize(QSize(40, 40))
            button.setFixedSize(QSize(40, 40))
            button.setContentsMargins(0, 0, 0, 0)
            button.setStyleSheet("margin: 0px; padding: 0px; border: none;")
            button.setObjectName(str(i) + str(j))
            button.clicked.connect(lambda _, b=button: player_shoots(b, mainWindow))
            oppBoardLayout.addWidget(button, i, j, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    oppBoardLayout.setSpacing(0)
    oppBoardLayout.setContentsMargins(0, 0, 0, 0)
    mainWindow.oppBoard.setFixedSize(QSize(400, 400))
    mainWindow.oppBoard.setLayout(oppBoardLayout)
    layout.addWidget(mainWindow.oppBoard, alignment = Qt.AlignmentFlag.AlignHCenter)
    mainWindow.moreText.setText("This is your board.")
    layout.addWidget(mainWindow.moreText)
    playerBoardLayout = QGridLayout()
    for i in range(10):
        for j in range(10):
            image = QLabel()
            image.setPixmap(mainWindow.pixmaps[mainWindow.playerBoardArray[i][j]])
            image.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            image.setFixedSize(QSize(40, 40))
            image.setContentsMargins(0, 0, 0, 0)
            image.setStyleSheet("margin: 0px; padding: 0px; border: none;")
            image.setObjectName(str(i) + str(j))
            playerBoardLayout.addWidget(image, i, j)
    playerBoardLayout.setSpacing(0)
    playerBoardLayout.setContentsMargins(0, 0, 0, 0)
    mainWindow.playerBoard = QWidget()
    mainWindow.playerBoard.setFixedSize(QSize(400, 400))
    mainWindow.playerBoard.setLayout(playerBoardLayout)
    layout.addWidget(mainWindow.playerBoard, alignment = Qt.AlignmentFlag.AlignHCenter)
    widget = QWidget()
    widget.setLayout(layout)
    mainWindow.setCentralWidget(widget)

def player_shoots(button : QPushButton, mainWindow : QMainWindow):
    oppBoardLayout = mainWindow.oppBoard.layout()
    coordstr = button.objectName()
    y = int(coordstr[0:1])
    x = int(coordstr[1:2])
    if (mainWindow.oppBoardArray[y][x] != "_"):
        mainWindow.oppBoardArray[y][x] = "X"
    image = QLabel()
    image.setPixmap(mainWindow.pixmaps[mainWindow.oppBoardArray[y][x]])
    image.setFixedSize(QSize(40, 40))
    image.setContentsMargins(0, 0, 0, 0)
    oldWidget = oppBoardLayout.itemAtPosition(y, x)
    oldWidget = oldWidget.widget()
    oppBoardLayout.removeWidget(oldWidget)
    oldWidget.deleteLater()
    oppBoardLayout.addWidget(image, y, x, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    if (checkWin(mainWindow.oppBoardArray)):
        mainWindow.instructions.setText("You win! Your opponent's board: ")
        mainWindow.moreText.setText("Your Board: ")
        freezeOppBoard(mainWindow)
        return
    
    ## computer_random_shot(mainWindow)
    computer_tracking_shot(mainWindow)
    
    if (checkWin(mainWindow.playerBoardArray)):
        mainWindow.instructions.setText("You lost. Your opponent's board: ")
        mainWindow.moreText.setText("Your Board: ")
        freezeOppBoard(mainWindow)
        return
 
def checkWin(board):
    counter = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == "X"):
                counter += 1
    return (counter == 17)

def freezeOppBoard(mainWindow : QMainWindow):
    oppBoardLayout = mainWindow.oppBoard.layout()
    for i in range(10):
        for j in range(10):
            oldWidget = oppBoardLayout.itemAtPosition(i, j)
            oldWidget = oldWidget.widget()
            if (isinstance(oldWidget, QPushButton)):
                image = QLabel()
                image.setPixmap(mainWindow.pixmaps[mainWindow.oppBoardArray[i][j]])
                image.setFixedSize(QSize(40, 40))
                image.setContentsMargins(0, 0, 0, 0)
                oppBoardLayout.removeWidget(oldWidget)
                oldWidget.deleteLater()
                oppBoardLayout.addWidget(image, i, j, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    mainWindow.oppBoard.setLayout(oppBoardLayout)