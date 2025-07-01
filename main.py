import sys
from start_screen import create_start_screen
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget

## TODO: UNIT TESTING!

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Battleship")
        self.setFixedSize(QSize(500, 900))

        self.instructions = QWidget()
        self.playerBoard = QWidget()
        self.pixmaps = {}
        self.playerBoardArray =  [["_" for i in range(10)] for j in range(10)]
        self.oppBoardArray = [["_" for i in range(10)] for j in range(10)]
        self.placingRotation = True
        self.placingIndex = 0
        self.oppBoard = QWidget()
        self.moreText = QLabel()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    create_start_screen(w)
    w.show()
    app.exec()
    
if __name__ == '__main__':
    main()