# PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# calcul d'angles
import math
# calcul d'angles
import numpy as np
# passage du mode facile/difficile
import time

# distance de l'algorithme de la corde
STEP = 100
# taille des menus
MENUSIZE = 100
# à partir de quel distance du point central du menu on considère un retour en arrière
BACKGAP = 10

# délai activation du mode visuel
TIMETICK = 0.3

class MarkingMenu:

    #construit le menu avec sa fenêtre, widget et manager de reference, ainsi qu'avec le menu conceptuel qu'il représente et le mot à trouver
    def __init__(self,window,widget,manager,menu,goodWord):
        self.window = window
        self.widget = widget
        self.knownKey = []
        self.menu = menu
        self.manager = manager
        self.goodWord = goodWord
        
        self.memory = []
        self.saveMemory = []

        self.showMenu = False
        self.time = -1
        self.current = None

        self.toSelect = -1
        self.currentWord = None

    # retourne le type de menu
    def getType(self):
        return "marking"

    # active le menu
    def active(self):
        pass

    # desactive le menu
    def desactive(self):
        pass

    # dessin de la technique de menu
    def draw(self,painter,x,y):

        if self.widget.isClicked:

            # if no move, set the easy mode with 
            self.setMode(x,y)

            # remember the actual point
            self.memory += [[x,y]]

            # simplify the curve
            red = reduit(self.memory,STEP)
            self.memory = red

            # save the old steps (to not clear )
            if len(self.memory) > 2:
                self.saveMemory += self.memory[:1]
                self.memory = self.memory[1:]

            # if the last stick is too long, create a point and consider a selection
            elif len(self.memory) == 2:
                n = normDist(self.memory[0],self.memory[1])
                if n > MENUSIZE * (4/3):
                    x = (self.memory[1][0] - self.memory[0][0])/n
                    y = (self.memory[1][1] - self.memory[0][1])/n
                    x = self.memory[0][0] + (x * MENUSIZE * (4/3))
                    y = self.memory[0][1] + (y * MENUSIZE * (4/3))
                    pt = [x,y]
                    self.saveMemory += self.memory[:1]
                    self.memory = [pt] + self.memory[1:]

            # accept a turn back selection
            if len(self.saveMemory) >= 1:
                if len(self.memory) >= 2:
                    if notSoFar(self.memory[-2],self.memory[-1]):
                        self.memory = self.memory[:-2] + [self.saveMemory[-1]]
                        self.saveMemory = self.saveMemory[:-1]
                        self.currentWord = None

            # draw the curve of selection
            temp = self.saveMemory + self.memory
            for p in range(len(temp)-1):
                painter.drawLine(temp[p][0],temp[p][1],
                                 temp[p+1][0],temp[p+1][1])

            
            c = self.menu
            i = 0
            while i < len(temp)-1:
                self.drawMenu(painter,c,i,MENUSIZE)
                if c.subFiles[self.toSelect].isItem():
                    self.currentWord = c.subFiles[self.toSelect].word
                else:
                    self.currentWord = None
                if len(c.subFiles[self.toSelect].subFiles) > 0:
                    c = c.subFiles[self.toSelect]
                    i += 1
                else:
                    i = len(temp) -1
            
        else:
            self.reset()


    # dessine le menu
    def drawMenu(self,painter,menu,i,size):
        
        temp = self.saveMemory + self.memory
        x = temp[i][0]
        y = temp[i][1]

        x1 = temp[i+1][0]
        y1 = temp[i+1][1]
        repere = [x,y1]
        angle = getAngle([x,y],repere,[x1,y1])

        points = []
        n = len(menu.subFiles)
        w = 360/n          
                                        
        for i in range(n):
            polygon = QPolygonF()                                            
            t = w*i
            xx = size*math.cos(math.radians(t))
            yy = size*math.sin(math.radians(t))
            points += [(xx+x,yy+y)]
            polygon.append(QPointF(xx+x, yy + y)) 

            t1 = w*(i+1)
            xx1 = size*math.cos(math.radians(t1))
            yy1 = size*math.sin(math.radians(t1))
            polygon.append(QPointF(xx1+x, yy1 + y)) 

            polygon.append(QPointF(x, y))

            if w*i  <= (angle-90)%360 <= w*(i+1):
                painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
                painter.setBrush(QBrush(QColor(255, 0, 0)))
                sizeText = 12
                self.toSelect = i
            else:
                painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                painter.setBrush(QBrush(QColor(0, 0, 255)))
                sizeText = 8

            if self.showMenu:
                painter.drawPolygon(polygon)

                xText = x+(xx+(xx1 - xx)/2)/(4/3)
                yText = y+(yy+(yy1 - yy)/2)/(4/3)
                painter.setFont(QFont("times",sizeText))
                painter.drawText(xText,yText,menu.subFiles[i].word)

        if self.showMenu:
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            for p in points:
                painter.drawLine(x,y,p[0],p[1])

    # affecte le mode facile/difficile
    def setMode(self,x,y):
        if self.time == -1:
            self.time = time.time()
        if self.current == None:
            self.current = [x,y]
        else:
            if not(notSoFar(self.current,[x,y],3)):
                self.time = time.time()
                self.current = [x,y]
            else:
                t = time.time()
                if t - self.time > TIMETICK:
                    self.showMenu = True

    # remet à zero les attributs
    def reset(self):
        self.toSelect = -1
        self.currentWord = None
        self.memory = []
        self.saveMemory = []
        self.showMenu = False
        self.time = -1
        self.current = None

    # réaction à la réception de la pression d'une touche clavier
    def receivePress(self,event):
        pass
    
    # réaction à la réception de la relache d'une touche clavier
    def receiveRelease(self,event):
        pass

    # réaction au click
    def callOnClick(self):
        pass

    # réaction au relâchement du click
    def callReleaseClick(self):
        if self.currentWord != None:
            if self.goodWord == self.currentWord:
                self.manager.goodItem(True)
            else:
                self.manager.wrongItem(True)
        self.reset()



# retourne l'angle entre [origin v1] et [origin v2] 
def getAngle(origin,v1,v2):
    n1 = normDist(v1,origin)
    if n1 == 0:
        n1 = 1
    n2 = normDist(v2,origin)
    if n2 == 0:
        n2 = 1
    unit_vector_1 = [(v1[0] - origin[0])/n1, (v1[1]-origin[1])/n1]
    unit_vector_2 = [(v2[0] - origin[0])/n2, (v2[1] - origin[1])/n2]
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    angle = math.degrees(angle)

    if v2[1] > origin[1]:
        angle = 90 + (90 - angle)
    if v2[0] < origin[0]:
        angle = 180 + (180 - angle)

    return angle

# indique si deux points sont proches de gap ou non
def notSoFar(pt1,pt2,gap=BACKGAP): 
    x = pt1[0] - gap < pt2[0] <  pt1[0] + gap      
    y = pt1[1] - gap < pt2[1] <  pt1[1] + gap 
    return x and y 


# algorithme de la corde
def reduit( cont, dmax ):
    # Calcul des distances entre les points et la corde
    d = distancesEspace(cont)
    # Si la distance maximale est inferieure au seuil, retourner les extremites
    if max(d) <= dmax:
      return [cont[0], cont[-1]]
    else:
      # Indice du point le plus eloigne de la corde
      loin = d.index(max(d))
      # Reduire les deux sous-chaines de contour
      cont1 = reduit( cont[:(loin+1)], dmax )
      cont2 = reduit( cont[loin:], dmax )
      # Enlever un point et concatener
      return cont1 + cont2[1:]

# distance entre 2 points
def normDist(pt1,pt2):
    x = pt2[0] - pt1[0]
    y = pt2[1] - pt1[1]
    return math.sqrt(x**2+y**2)

# retourne les distances des points et la corde
def distancesEspace(cont):
    d = []
    b = [cont[0][0], cont[0][1]]
    c = [cont[-1][0], cont[-1][1]]
    u = [c[0]-b[0],c[1]-b[1]]

    for i in range(len(cont)):
        a=[cont[i][0], cont[i][1]]
        ba=[a[0]-b[0],a[1]-b[1]]
        bau = np.cross(ba,u).item(0)
        normeBau = math.sqrt(bau**2)
        normeU = math.sqrt(u[0]**2+u[1]**2)
        if(normeU == 0):
            normeU = 1
        d.append(normeBau/normeU)

    return d
