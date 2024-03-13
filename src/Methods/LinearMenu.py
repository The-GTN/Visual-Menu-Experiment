from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from random import randint

keys = ["a","z","e","r","t","y","u","i","o","p","q","s","d","f","g","h","j","k","l","m","w","x",
        "c","v","b","n"]

class LinearMenu:

    #construit le menu avec sa fenêtre, widget et manager de reference, ainsi qu'avec le menu conceptuel qu'il représente et le mot à trouver
    def __init__(self,window,widget,manager,menu,goodWord):
        self.window = window
        self.widget = widget
        self.knownKey = []
        self.menu = menu
        self.manager = manager
        self.goodWord = goodWord
        self.bar = None

    # retourne le type de menu
    def getType(self):
        return "linear"

    # active le menu
    def active(self):
        self.menuBar()

    # desactive le menu
    def desactive(self):
        if(self.bar != None):
            self.bar.clear()

    # fait apparaître le menu lineaire
    def menuBar(self):
        self.window.statusBar()
        self.bar = self.window.menuBar()
        a = self.menu
        self.affectActions(a)
        
    # affecte les actions du menu conceptuel au menu lineaire
    def affectActions(self,menus,mainMenu=None):
        if mainMenu == None:
            mainMenu = self.bar

        for item in menus.subFiles:
            if not(item.isItem()):
                temp = mainMenu.addMenu(item.word)
                self.affectActions(item,temp)
            else:
                if item.word == self.goodWord:
                    mainMenu.addAction(self.act(item.word,self.manager.goodItem))
                else:
                    mainMenu.addAction(self.act(item.word,self.manager.wrongItem))

    # affecte une action nommée name avec raccourci clavier aléatoire
    def act(self,name,action):
        theAct = QAction(name+"...", self.widget )
        key = self.getFreeKey()
        theAct.setShortcut( QKeySequence("Ctrl+"+key[0]+", Ctrl+"+key[1]))
        theAct.setToolTip(name)
        theAct.setStatusTip(name)
        theAct.triggered.connect( action )
        return theAct

    # retourne un raccourci clavier libre
    def getFreeKey(self):
        key = keys[randint(0,len(keys)-1)] + keys[randint(0,len(keys)-1)]
        while key in self.knownKey:
            key = keys[randint(0,len(keys)-1)] + keys[randint(0,len(keys)-1)]
        self.knownKey += [key]
        return key

    # dessin de la technique de menu
    def draw(self,painter,x,y):
        painter.drawEllipse(\
            x-5,\
            y-5,10,10)

    # réaction au click
    def callOnClick(self):
        pass

    # réaction au relâchement du click
    def callReleaseClick(self):
        pass
    
    # réaction à la réception de la pression d'une touche clavier
    def receivePress(self,event):
        pass
    
    # réaction à la réception de la relache d'une touche clavier
    def receiveRelease(self,event):
        pass