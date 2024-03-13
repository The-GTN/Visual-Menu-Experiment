#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time

from src.Methods.Menu import Menu

TIMEPRESS = 0.5
PLACES = [(-1,0),(1,0),(0,-1),(0,1)]
SQUARESIZE = 75
BLABLAPOS = (270,270)

class BlablaMenu:

    #construit le menu avec sa fenêtre, widget et manager de reference, ainsi qu'avec le menu conceptuel qu'il représente et le mot à trouver
    def __init__(self,window,widget,manager,menu,goodWord):
        self.window = window
        self.widget = widget
        self.knownKey = []
        self.menu = menu
        self.currentmenu = [(menu,False)]
        self.manager = manager
        self.goodWord = goodWord
        self.writing = False
        self.currentword = ""
        self.time = 0

    # retourne le type du menu
    def getType(self):
        return "blabla"

    # active le menu
    def active(self):
        pass

    # desactive le menu
    def desactive(self):
        pass

    # dessin de la technique de menu
    def draw(self,painter,x,y):
        painter.drawEllipse(x-15,y-15,30,30)
        
        painter.setFont(QFont("times",15))
        rect = QRect(10,20, 350,100)
        painter.drawRect(rect)
        painter.drawText(rect, Qt.AlignCenter, self.currentword)
        
        painter.setFont(QFont("times",8))
        rect = QRect(BLABLAPOS[0], BLABLAPOS[1], SQUARESIZE,SQUARESIZE)
        painter.drawRect(rect)
        
        painter.drawText(rect, Qt.AlignCenter, self.currentmenu[-1][0].word)
        if not(self.currentmenu[-1][0].isItem()):
            words = ["","","",""]
            for i in range(len(self.currentmenu[-1][0].subFiles)):
                words[i%len(words)] += self.currentmenu[-1][0].subFiles[i].word + "\n"
                
            for i in range(len(words)):
                if words[i] != "":
                    rect = QRect(BLABLAPOS[0]+SQUARESIZE*PLACES[i][0], BLABLAPOS[1]+SQUARESIZE*PLACES[i][1], SQUARESIZE,SQUARESIZE)
                    painter.drawRect(rect)
                    painter.drawText(rect, Qt.AlignCenter, words[i])
                
            
            
        

    # réaction au click
    def callOnClick(self):
        pass

    # réaction au relâchement du click
    def callReleaseClick(self):
        pass
    
    # réaction à la réception de la pression d'une touche clavier
    def receivePress(self,event):
        if event.key() == Qt.Key_Shift:
            self.writing = True
    
    # réaction à la réception de la relache d'une touche clavier
    def receiveRelease(self,event):
        k = event.key()
        if k == Qt.Key_Shift:
            self.writing = False
            if self.currentmenu[-1][0].isItem():
                if self.currentmenu[-1][0].word == self.goodWord:
                    self.manager.goodItem(True)
                else:
                    self.manager.wrongItem(True)
            self.currentword = ""
            self.currentmenu = [(self.menu,False)]
        if self.writing:
            t = event.text().lower()
            if k == Qt.Key_Backspace:
                if len(self.currentmenu) > 1:
                    if self.currentmenu[-1][1]:
                        self.currentword = self.currentword[:-1]
                    self.currentmenu.pop()
            elif k == Qt.Key_Left:
                self.get_arrow_submenu(0)
            elif k == Qt.Key_Up:
                self.get_arrow_submenu(2)
            elif k == Qt.Key_Right:
                self.get_arrow_submenu(1)
            elif k == Qt.Key_Down:
                self.get_arrow_submenu(3)
            elif len(self.currentword) != 0:
                if t != self.currentword[-1] or (time.time() - self.time) > TIMEPRESS:
                    self.time = time.time()
                    self.currentword += t
                    self.currentmenu.append((self.currentmenu[-1][0].filter(self.currentword),True))
            elif k not in [Qt.Key_Backspace,Qt.Key_Left,Qt.Key_Up,Qt.Key_Right,Qt.Key_Down]:
                self.currentword += t
                self.currentmenu.append((self.currentmenu[-1][0].filter(self.currentword),True))
                        
        self.widget.update()
        
        
    def get_arrow_submenu(self,i):
        if not(self.currentmenu[-1][0].isItem()):
            m = []
            j = i
            while j < len(self.currentmenu[-1][0].subFiles):
                m.append(self.currentmenu[-1][0].subFiles[j].copy())
                j += 4
            if len(m) > 1:
                self.currentmenu.append((Menu(self.currentmenu[-1][0].word,m),False))
            else:
                self.currentmenu.append((m[0],False))
        
