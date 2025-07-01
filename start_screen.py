from ship_placing import create_placing_screen
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QLabel, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QVBoxLayout, QWidget

## TODO: tidy up code, reduce repetitiveness

def create_start_screen(mainWindow : QMainWindow):
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    title = QLabel("BATTLESHIP")
    font = title.font()
    font.setPointSize(50)
    title.setFont(font)
    title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    title.setFixedHeight(80)
    layout.addWidget(title)

    header = QLabel("Graphics Key")
    font2 = header.font()
    font2.setPointSize(20)
    header.setFont(font2)
    header.setFixedHeight(50)
    layout.addWidget(header)
    keyLayout = QGridLayout()
    keyLayout.setSpacing(0)
    keyLayout.setContentsMargins(0, 0, 0, 0)

    unknownText = QLabel("Unknown Location")
    unknownText.setFixedSize(QSize(200, 20))
    keyLayout.addWidget(unknownText, 0, 0)
    unknown = QLabel()
    unknownPixmap = QPixmap('C:/mandy/myPython/battleship/unknown.png')
    unknown.setPixmap(unknownPixmap)
    keyLayout.addWidget(unknown, 0, 1)

    hitText = QLabel("Hit")
    hitText.setFixedSize(QSize(200, 20))
    keyLayout.addWidget(hitText, 1, 0)
    hit = QLabel()
    hitPixmap = QPixmap('C:/mandy/myPython/battleship/hit.png')
    hit.setPixmap(hitPixmap)
    keyLayout.addWidget(hit, 1, 1)

    missText = QLabel("Miss")
    missText.setFixedSize(QSize(200, 20))
    keyLayout.addWidget(missText, 2, 0)
    miss = QLabel()
    missPixmap = QPixmap('C:/mandy/myPython/battleship/miss.png')
    miss.setPixmap(missPixmap)
    keyLayout.addWidget(miss, 2, 1)

    shipText = QLabel("Ship")
    shipText.setFixedSize(QSize(200, 20))
    keyLayout.addWidget(shipText, 3, 0)

    shipLayout = QHBoxLayout()
    shipLayout.setSpacing(0)
    shipLayout.setContentsMargins(0, 0, 0, 0)
    ship1 = QLabel()
    ship1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    shipEndPixmap = QPixmap('C:/mandy/myPython/battleship/ship_end.png')
    ship1.setPixmap(shipEndPixmap)
    ship1.setFixedSize(shipEndPixmap.size())
    ship1.setScaledContents(False)
    shipLayout.addWidget(ship1)

    ship2 = QLabel()
    ship2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    shipMiddlePixmap = QPixmap('C:/mandy/myPython/battleship/ship_middle.png')
    ship2.setPixmap(shipMiddlePixmap)
    ship2.setFixedSize(shipMiddlePixmap.size())
    ship2.setScaledContents(False)
    shipLayout.addWidget(ship2)

    ship3 = QLabel()
    ship3.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    transform = QTransform()
    transform.rotate(180)
    ship3Pixmap = shipEndPixmap.transformed(transform)
    ship3.setPixmap(ship3Pixmap)
    ship3.setFixedSize(ship3Pixmap.size())
    ship3.setScaledContents(False)
    shipLayout.addWidget(ship3)

    ship = QWidget()
    ship.setLayout(shipLayout)
    ship.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    ship.setFixedSize(shipLayout.sizeHint())
    keyLayout.addWidget(ship, 3, 1)

    graphicsKey = QWidget()
    graphicsKey.setLayout(keyLayout)
    layout.addWidget(graphicsKey)

    start = QPushButton("START")
    start.setFixedSize(QSize(200, 50))
    start.clicked.connect(lambda: game_started(mainWindow))
    layout.addWidget(start, alignment=Qt.AlignmentFlag.AlignHCenter)

    widget = QWidget()
    widget.setLayout(layout)
    mainWindow.setCentralWidget(widget)

def game_started(mainWindow):
    create_placing_screen(mainWindow)
    return
