# ecriture et lecture dans fichiers csv
import csv
# construction des menu
from random import shuffle, choice, randint

# taille des menus intermédiaires
N = 4
# tailles à tester
SIZES = [3,4,5]
# profondeurs à tester
DEPTHS = [0,1,2]
# techniques à tester
MENUS = ["linear","marking","blabla"]


class Menu():

    # un menu c'est un mot et une liste de sous menu
    def __init__(self,word,l):
        self.word = word
        self.subFiles = l

    # un menu est item s'il n'a pas de sous menus
    def isItem(self):
        return len(self.subFiles) == 0

    # ajout d'un item au menu
    def addItem(self,word):
        self.subFiles.append(word)

    # mélange du menu
    def shuffle(self):
        shuffle(self.subFiles)
        for i in self.subFiles:
            i.shuffle()

    # crée les fichiers pour l'expérience
    def createAllFiles(rep,fullMenuFile="./media/data/fullMenu.csv"):
        res = []
        menus = ["L","M","B"]
        for i in range(rep):
            for size in SIZES:
                for depth in DEPTHS:
                    for menu in range(len(MENUS)):
                        (m,a) = Menu.fromParams(fullMenuFile,depth,size,True)
                        m.toFile("./media/data/menus/"+MENUS[menu]+"/D"+str(depth)+"S"+str(size)+"-"+str(i)+".csv")
                        res += [(menus[menu]+str(depth)+str(size)+str(i),a)]

            shuffle(res)
            with open("./media/data/sequences/"+str(i+1)+".csv", 'w') as f:
                for name,answer in res:
                    f.write(name+","+answer)
                    f.write("\n")

    # crée un menu à partir d'un fullMenu decrit dans file, avec un element à trouver dans un menu de taille size et profondeur depth
    def fromParams(file,depth,size,showAnswer=False):
        base = Menu.fromFile(file)
        base.shuffle()

        answer = base.subFiles[0].setDepthSize(max(DEPTHS),depth,size,showAnswer)
        if depth == 0:
            while len(base.subFiles) > size:
                base.subFiles = base.subFiles[:-1]
        for i in range(1,len(base.subFiles)):
            base.subFiles[i].setDepthSize(max(DEPTHS),choice(DEPTHS),choice(SIZES))

        base.shuffle()

        return (base,answer)

    # ajuste les sous menus du menu principal
    def setDepthSize(self,maxDepth,depth,size,finalPrint=False):

        if depth == 0:
            self.subFiles = []
            if finalPrint:
                return self.word

        else:
            if depth == 1:
                theSize = size
            else:
                theSize = N

            while len(self.subFiles) > theSize:
                self.subFiles = self.subFiles[:-1]

            for i in range(1,len(self.subFiles)):
                if not(self.subFiles[i].isItem()):
                    self.subFiles[i].setDepthSize(maxDepth-1,randint(0,maxDepth-1),choice(SIZES))

            return self.subFiles[0].setDepthSize(maxDepth-1,depth-1,size,finalPrint)
        
        return ""

    # crée un menu depuis un fichier
    def fromFile(file):
        base = Menu("root",[])
        with open(file, newline='\n') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            current = base
            for data in read:
                level = int(data[0])
                for i in range(level):
                    name = data[i+1]
                    item = 0
                    founded = False
                    while item < len(current.subFiles) and not(founded):
                        if current.subFiles[item].word == name:
                            founded = True
                            current = current.subFiles[item]
                        item += 1
                    if not(founded):
                        current.addItem(Menu(name,[]))
                        current = current.subFiles[-1]
                for j in range(level+1,len(data)):
                    current.addItem(Menu(data[j],[]))
                current = base
        return base

    # convertie le menu en fichier
    def toFile(self,filename):
        with open(filename, 'w') as f:
            f.write(self.toFileContent())

    # renvoie le contenu du fichier correspondant au menu
    def toFileContent(self,level=0,hist=[]):
        s = str(level)

        for word in hist:
            s += ","+word

        for i in self.subFiles:
            s += ","+i.word

        s += "\n"

        level += 1
        oldHist = hist
        for i in self.subFiles:
            if not(i.isItem()):
                newHist = oldHist + [i.word]
                s += i.toFileContent(level,newHist)
        
        return s
        
    # print du menu
    def print(self,level=0):
        s = level*"\t"+"- "+self.word
        if not(self.isItem()):
            s += " : \n"
        else:
            s += "\n"
        level += 1

        for i in self.subFiles:
            s += i.print(level)

        return s

    # conversion en string du menu
    def __str__(self):
        return self.print()

    # representation du menu
    def __repr__(self):
        return self.print()
    
    def filter(self,s):
        if s == "":
            return self.copy()
        else:
            m = self.copy()
            for i in range(len(m.subFiles)-1,-1,-1):
                if m.subFiles[i].isItem():
                    if not(s in m.subFiles[i].word):
                        m.subFiles.pop(i)
                else:
                    m.subFiles[i] = m.subFiles[i].filter(s)
                    if m.subFiles[i].isItem():
                        if not(s in m.subFiles[i].word):
                            m.subFiles.pop(i)
            return m
        
    def copy(self):
        return Menu(self.word,self.subFiles.copy())
                        

# on appelle ce fichier pour recréer les fichiers d'expériences
if __name__ == "__main__":
    Menu.createAllFiles(10)