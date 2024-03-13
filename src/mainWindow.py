# utilisation PyQt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Setup de l'expérience
from src.MenuXP.ExpSetup import ExpSetup
# Gestion de l'expérience
from src.MenuXP.XPManager import XPManager


# Classe fenêtre principale
class MainWindow(QMainWindow):

    # Construction de la fenêtre, on y instancie le Setup de l'Expérience
    def __init__(self,name="Expérience contrôlée : Bienvenue"):
        super().__init__()
        self.setWindowIcon(QIcon('media/images/logo.png'))
        self.setWindowTitle(name)
        self.setWidget(QWidget)
        self.err = False
        self.manager = None
        ExpSetup(self)

    # disposition d'une widget centrale à la fenêtre, si options, on initialise le XPManager
    def setWidget(self,widget,opts={}):
        if len(opts) == 0:
            self.widget = widget()
        else:
            self.manager = XPManager(self,opts)
            self.widget = widget(self)
        self.setCentralWidget(self.widget)

    # événement fermeture fenêtre principale
    def closeEvent(self, event):
        if self.err:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Stop Experience', 'Are you sure you want to stop the experiment ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    # déclenchement erreur dans la fenêtre, fermeture sans ouverture fenêtre dialogue
    def error(self):
        self.err = True
        self.close()

    # retourne la status bar de la fenêtre
    def statusBar(self) -> 'QStatusBar':
        return super().statusBar()

    # retourne le menu bar de la fenêtre
    def menuBar(self) -> 'QMenuBar':
        return super().menuBar()
    
        