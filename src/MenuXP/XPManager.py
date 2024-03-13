# PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# ecriture dans logs.csv
import csv
# indice de début de lecture de la séquence
import random
# analyse du temps de sélection dans l'expérience
import time

# constrution menu via fichier
from src.Methods.Menu import Menu
# utilisation du LinearMenu
from src.Methods.LinearMenu import LinearMenu
# utilisation du BlablaMenu
from src.Methods.BlablaMenu import BlablaMenu
# utilisation du MarkingMenu
from src.Methods.MarkingMenu import MarkingMenu


class XPManager:

    # construit le gestionnaire d'xp, récupère la séquence et la lit à un indice aléatoire
    def __init__(self,window,opts):
        self.opts = opts
        self.window = window

        self.time = time.time()
        self.nbErrors = 0
        self.count = 0
        
        self.goodWord = ""
        self.type = ""
        self.menu = None

        s = "./media/data/sequences/"+str(self.opts["repetition"])+".csv"
        self.sequence = self.getSequence(s)

        self.index = random.randint(0,len(self.sequence)-1)


    # passe à la prochaine sélection à faire
    def setNextMenu(self):
        if self.count < len(self.sequence):
            menu, soluce = self.sequence[self.index]
            self.goodWord = soluce

            if menu[0] == "B":
                self.type = "blabla"
                const = BlablaMenu
            elif menu[0] == "L":
                self.type = "linear"
                const = LinearMenu
            else:
                self.type = "marking"
                const = MarkingMenu

            m = Menu.fromFile("./media/data/menus/"+self.type+"/D"+menu[1]+"S"+menu[2]+"-"+menu[3]+".csv")
            
            if self.menu == None:
                self.menu = const(self.window,self.window.widget,self,m,soluce)
                self.menu.active()

            self.menu.desactive()

            self.menu = const(self.window,self.window.widget,self,m,soluce)
            self.menu.active()

            self.count += 1
            self.index = (self.index + 1)%len(self.sequence)
            self.window.setWindowTitle("Expérience contrôlée : "+str(self.count)+"/"+str(27*int(self.opts["repetition"])))
            self.window.widget.update()

        else:
            self.finish()

    # récupère la séquence selon le nombre de répétitions à faire
    def getSequence(self,file):
        res = []
        with open(file, newline='\n') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            for data in read:
                res += [(data[0],data[1])]
        return res

    # écriture des résultats dans le fichier de logs
    def notifyResult(self,t,errors):
        t = float("{:.2f}".format(t))
        filename = './media/data/logs.csv'
        if self.index-1 < 0:
            format = self.sequence[-1][0]
        else:
            format = self.sequence[self.index-1][0]
        # userId,age,niveau,nbRepetition,format,time,errors
        with open(filename, 'a') as f:
            s = ""
            s += self.opts["user"]
            s += ","+str(self.opts["age"])
            s += ","+str(self.opts["niveau"])
            s += ","+str(self.opts["repetition"])
            s += ","+format
            s += ","+str(t)
            s += ","+str(errors)
            f.write(s)
            f.write('\n')
        
    # réaction à une bonne sélection
    def goodItem(self,value):
        t = time.time()
        save_t = t-self.time
        self.notifyResult(save_t,self.nbErrors)
        self.time = t
        self.nbErrors = 0
        self.setNextMenu()

    # réaction à une mauvaise sélection
    def wrongItem(self,value):
        self.nbErrors += 1
        self.window.widget.errorDialog()

    # fin de l'expérience
    def finish(self):
        self.window.widget.finishDialog()

