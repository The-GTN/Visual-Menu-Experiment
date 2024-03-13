# PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Widget de la fenêtre d'expérience
class MenuWidget(QWidget):
    
    # construction du widget, a une position de curseur suivi, un attribut start qui indique si l'xp a commencé et un attribut isClicked qui indique si on est en train de cliquer
    def __init__(self,window):
        super().__init__()
        self.window = window
        self.setMouseTracking(True) # on active le mouseTracking
        self.cursorPos = None

        self.start = False
        self.isClicked = False
        self.setFocusPolicy(Qt.StrongFocus)
        self.canPress = False
    
    def keyPressEvent(self,event):
        super(MenuWidget, self).keyPressEvent(event)
        if self.cursorPos != None:
            if self.window.manager != None:
                if self.window.manager.menu != None:
                    self.window.manager.menu.receivePress(event)
                    
    def keyReleaseEvent(self,event):
        super(MenuWidget, self).keyReleaseEvent(event)
        if self.cursorPos != None:
            if self.window.manager != None:
                if self.window.manager.menu != None:
                    self.window.manager.menu.receiveRelease(event)

    def mouseMoveEvent(self, event): # evenement mouseMove
        self.cursorPos = event.pos() # on stocke la position du curseur
        self.update() # on met à jour l'affichage

    # événement click de souris
    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.accept()
        if not(self.start):
            self.window.manager.setNextMenu()
            self.start = True
        self.isClicked = True
        self.window.manager.menu.callOnClick()

    # événement de relachement du click de souris
    def mouseReleaseEvent(self, event):
        self.isClicked = False
        self.window.manager.menu.callReleaseClick()

    
    #evenement QPaintEvent
    def paintEvent(self, event):
        painter = QPainter(self)

        # on affiche le dessin de l'expérience contrôlé, avec mot à trouvé et technique utilisée
        if self.start:
            painter.setFont(QFont("times",15))
            rect = QRect(600,50, 350,100)
            painter.drawRect(rect)
            if self.window.manager != None:
                painter.drawText(rect, Qt.AlignCenter, "Methode utilisee : Menu "+self.window.manager.type)
            painter.setFont(QFont("times",20))
            rect = QRect(600,300, 350,250)
            painter.drawRect(rect)
            if self.window.manager != None:
                painter.drawText(rect, Qt.AlignCenter, "Mot à trouver : "+self.window.manager.goodWord)
        
        # pas de click initial, on attend avec l'écran d'attente que l'utilisateur clique 
        else:
            painter.setFont(QFont("times",22))
            rect = QRect(300,150, 500,250)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter, "Click Screen To Begin the XP")

        # on affiche le visuel de la technique utilisée
        if self.cursorPos != None:
            if self.window.manager != None:
                if self.window.manager.menu != None:
                    self.window.manager.menu.draw(painter,self.cursorPos.x(),self.cursorPos.y())
    

    # fenêtre de dialogue d'erreur de sélection
    def errorDialog(self):
        error = QDialog(None,Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        error.setWindowTitle("Error")
        error.setWindowIcon(QIcon('media/images/logo.png'))
        error.setWindowModality(Qt.ApplicationModal)
        vbox = QVBoxLayout()
        b = QPushButton("Sorry",self)
        b.clicked.connect(error.close)
        label = QLabel("Oops ! You made a mistake !", error)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setMinimumWidth(80)
        vbox.addWidget(label)
        vbox.addWidget(b)
        error.setLayout(vbox)
        error.exec_()


    # fenêtre de dialogue de fin d'expérience
    def finishDialog(self):
        error = QDialog(None,Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        error.setWindowTitle("End of the Experience")
        error.setWindowIcon(QIcon('media/images/logo.png'))
        error.setWindowModality(Qt.ApplicationModal)
        vbox = QVBoxLayout()
        b = QPushButton("Finish",self)
        b.clicked.connect(error.close)
        label = QLabel("Thanks for doing the experiment !", error)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setMinimumWidth(80)
        vbox.addWidget(label)
        vbox.addWidget(b)
        error.setLayout(vbox)
        error.exec_()

        self.window.error()



    
