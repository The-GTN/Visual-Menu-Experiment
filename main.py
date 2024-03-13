# utilisation PyQt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# utilisation sys.argv
import sys
# usage fenêtre principale
from src.mainWindow import MainWindow

def main(args):
    ### Afficher les arguments
    # print(args)

    ### Nom par défaut
    name = None

    ### Dimensions par défaut
    w = 1024
    h = 600

    ### Paramétrages : soit name, soit name largeur hauteur, soit largeur hauteur, soit pas de paramètres
    if len(args) not in [1,2,3,4]:
        usage()
        return
        
    elif len(args) == 2:
        name = args[1]
        
    elif len(args) == 3:
        w = int(args[1])
        h = int(args[2])
        
    elif len(args) == 4:
        name = args[1]
        w = int(args[2])
        h = int(args[3])

    ### Application Principale
    app = QApplication(args)

    ### Utilisation de notre Window
    if name != None:
        win = MainWindow(name)
    else:
        win = MainWindow()

    ### Execution de l'application
    
    if not win.err:
        win.resize(w,h)
        win.show()
        app.exec_()
    return

# message d'erreur indiquant la bonne utilisation
def usage():
    print("There is 4 ways to use this program : \n\t - no parameter : default use \n\t - 1 parameter : choose the name \n\t - 2 parameters : choose the width and height of the widget \n\t - 3 parameters : choose the name and the width and height of the widget")

# fonction main
if __name__ == "__main__":
    main(sys.argv)
