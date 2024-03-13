# PyQt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Widget de l'expérience
from src.MenuXP.MenuWidget import MenuWidget

# Il s'agit de la fenêtre de dialogue pour le questionnaire d'expérience
class ExpSetup(QDialog):

    # construction de la fenêtre de dialogue, initialisation des options et du visuel
    def __init__(self,window):
        super().__init__()
        self.setWindowTitle("Setup Experience")
        self.setWindowIcon(QIcon('media/images/logo.png'))
        self.setWindowModality(Qt.ApplicationModal)
        self.window = window
        self.finish = False
        self.opts = {"user":self.getUserId(),"repetition":3,"niveau":"Debutant","age":22}
        self.initLayout()
        self.exec_()

    # Fonction qui ferme la fenêtre de questionnaire et qui lance l'expérience avec les options du questionnaire
    def startXP(self):
        self.window.setWidget(MenuWidget,self.opts)
        self.finish = True
        self.close()

    # Visuel de la fenêtre
    def initLayout(self):
        self.resize(250,180)
        
        user, label = self.SliderInput("age","Age de l'utilisateur",1,99,1)
        items = ["Debutant","Intermediaire", "Expert"]
        tech, techlab = self.ChoiceInput("niveau","Niveau de l'utilisateur",items) 
        rep, replab = self.SliderInput("repetition","Nombre de répétitions",1,10,1,True)
        b = QPushButton("Valider",self)
        b.clicked.connect(self.startXP)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(label)
        vbox.addWidget(user)
        vbox.addWidget(techlab)
        vbox.addWidget(tech)
        vbox.addWidget(replab)
        vbox.addWidget(rep)
        vbox.addWidget(b)

        self.setLayout(vbox)

    # ajoute un input à entrée de texte, qui changera l'attribut att des options et qui aura un label à name
    def LineInput(self,att,name):
        label = self.createLabel(name,str(self.opts[att]))
        user = QLineEdit(self)
        user.setText("0")
        user.textChanged[str].connect(lambda v : self.updateLabel(label,att,name,v))
        return (user,label)

    # ajoute un input à choix parmis les items, qui changera l'attribut att des options et qui aura un label à name
    def ChoiceInput(self,att,name,items=[]):
        cb = QComboBox()
        cb.addItems(items)
        label = self.createLabel(name,cb.currentText())
        cb.currentIndexChanged.connect(lambda _ : self.updateLabel(label,att,name,cb.currentText()))
        return (cb,label)


    # ajoute un input slider allant de min à max avec des pas de step, changera la valeur att des options, avec un label
    def SliderInput(self,att,name,min,max,step,special=False):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(min, max)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setPageStep(5)
        slider.setValue(self.opts[att])
        slider.setTickInterval(step)
        slider.setSingleStep(step)

        label = self.createLabel(name,str(self.opts[att]),special)

        slider.valueChanged.connect(lambda v : self.updateLabel(label,att,name,v,True,special))

        return (slider,label)

    # crée un label avec un nom name et une valeur value
    def createLabel(self,name,value,special=False):
        if special:
            label = QLabel(name+' : '+value+" ("+str(27*int(value))+" selections)", self)
        else:
            label = QLabel(name+' : '+value, self)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label.setMinimumWidth(80)
        return label

    # change le texte courant d'un label. si setValue, l'attribut att des options est affecté à value
    def updateLabel(self,label,att,text,value,setValue=True,special=False):
        if setValue:
            self.opts[att] = value
        if special:
            label.setText(text+" : "+str(value)+" ("+str(27*value)+" selections)")
        else:
            label.setText(text+" : "+str(value))

    # événement de fermeture de fenêtre
    def closeEvent(self, event):
        if self.finish:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Stop Setup', 'Are you sure you want to stop the experiment setup ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.window.error()
                event.accept()
            else:
                event.ignore()

    # modifie l'événement "?" pour ouvrir une fenêtre de dialogue d'informations 
    def event(self, event): 
        if event.type() == QEvent.EnterWhatsThisMode:
            error = QDialog(None,Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
            error.setWindowTitle("Help")
            error.setWindowIcon(QIcon('media/images/logo.png'))
            error.setWindowModality(Qt.ApplicationModal)
            vbox = QVBoxLayout()
            b = QPushButton("Okay",self)
            b.clicked.connect(error.close)
            label = QLabel("Level and Age are for data analysis and Repetition is for the duration of the XP", error)
            label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            label.setMinimumWidth(80)
            vbox.addWidget(label)
            vbox.addWidget(b)
            error.setLayout(vbox)
            error.exec_()
            QWhatsThis.leaveWhatsThisMode()
            return True
        return QDialog.event(self, event)


    # récupère le numéro utilisateur en fonction des lignes déjà présentes dans le fichier de log
    def getUserId(self):
        try:
            with open("./media/data/logs.csv", newline='\n') as csvfile:
                read = csvfile.readlines()
                if len(read) <= 1:
                    return "0"
                else:
                    try:
                        s = read[-1].split(",")
                        return str(int(s[0])+1)
                    except:
                        return "0"
        except:
            return "0"