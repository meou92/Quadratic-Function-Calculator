import sys
from PyQt6 import QtWidgets,QtGui,QtCore,sip

def positive(num, text="",change=True):
    if num == 0:
        return ""
    elif num % 1 == 0.0:
        num=int(num)
    if change:
        return f"+{0-num}{text}" if num < 0 else f"-{num}{text}"
    else:
        return f"+{num}{text}" if num > 0 else f"-{0-num}{text}"

def pos(num, text=""):
    if num == 0:
        return ""
    elif num % 1 == 0.0:
        num=int(num)
    return f"+{num}{text}" if num > 0 else f"-{0-num}{text}"

def stript(text:str):
    t=text
    for ai in '+-=()':
        t=t.replace(ai,f",{ai}")
    return t.split(",")

def calculator():
    func=input0.text()
    if (
        (inputed := box.currentText()) in li
            and (output := box2.currentText()) in li
            and func[:2] == "y="
            and (
                ("x^2" in func and "x" in func[func.index("x^2") + 3 :])
                or (")^2" in func)
                or (
                    func.count("x") == 2
                    and func.count("(") == 2
                    and func.count(")") == 2
                )
            )
    ):
        if (t:=func)[2]not in'+-':
            t=t[:2]+'+'+t[2:]
        if t[3]in'x(':
            t=t[:3]+'1'+t[3:]
        ans=stript(t)
        a=float(ans[2][:-3]) if ans[2][-3:]=='x^2' else float(ans[2])
        f=float(ans[4]) if ans[4]!='' else 1
        if inputed=='一般式':
            b=float(ans[3][:-1]) if ans[2][:-1]!='' else 1
            c=float(ans[4]) if len(ans)>4 else 0
        elif inputed=='頂點式':
            b=f*2*a
            c=f**2*a
            if len(ans)==7:
                c+=float(ans[6])
        else:
            g=float(ans[7]) if ans[7]!='' else 0
            b=a*(f+g)
            c=a*f*g
        x1=b/(2*a)
        x2=c-(b**2)/(4*a)
        if inputed=="頂點式":
            vertex=func
        else:
            te=f"(x{pos(x1)})^2"
            vertex=f"y={positive(a,te,False)}{pos(x2)}"
        if output=='一般式':
            texts=f"y={pos(a,'x^2')[1:]}{pos(b,'x')}{pos(c)}"
        elif output=='頂點式':
            texts=vertex
        else:
            if (delta:=[d:=b**2-4*a*c, pow(d, 1/2)])[0]>=0:
                te=f"(x{positive((0-b+delta[1])/(2*a))})(x{positive((0-b-delta[1])/(2*a))})"
                texts=f"y={positive(a,te,False)[1:]}"
            else:
                texts='error'
        texts+=f"\n頂點在({0-x1},{x2}), {'開口朝上' if a>0 else '開口朝下'}"
        try:
            get=float(input1.text())
        except:
            ...
        else:
            if parameter.currentText() == "x":
                if get % 1 == 0:
                    get = int(get)
                text = t[2:]
                if inputed == "一般式":
                    text = text.replace("x", "*x")
                text = text.replace("^2", "**2")
                text = text.replace("(", "*(")
                texts += f"\n當x={get}時, y={eval(text,{'x':get})}"
            elif parameter.currentText() == "y":
                if inputed == "頂點式":
                    list_vertex = ans
                else:
                    list_vertex = stript(vertex)
                get0 = get
                if len(list_vertex) == 7:
                    get0 -= float(list_vertex[6])
                get1 = pow(get0 / float(list_vertex[2]), 1 / 2)
                m = float(list_vertex[4])
                texts += f"\n當y={get}時, x={get1-m}or{-get1-m}"
        output1.setPlainText(texts)
    else:
        output1.setPlainText(func)

class MoveLabel(QtWidgets.QLabel):
    def __init__(self,type=11,shape=0,last_time=5,color="1x2"):
        super().__init__(label)
        width=min(label.width(),label.height())//2
        self.setGeometry(0,0,width,width)
        self.setStyleSheet("background-color: #00000000;")
        self.side_width=width
        self.shape=shape
        self.color=colors[color][len(items)%7]
        if type//10==1:
            t0=(0, 0)
            t1=(label.width() - width, label.height() - width)
        elif type//10==2:
            t0=((label.width()-width)//2,0)
            t1=((label.width()-width)//2,label.height()-width)
        elif type//10==3:
            t0=(label.width()-width,0)
            t1=(0,label.height()-width)
        elif type//10==4:
            t0=(label.width()-width,label.height()-width)
            t1=(0,label.height()-width)
        self.animation1 = QtCore.QPropertyAnimation(self, b'geometry')
        self.animation1.finished.connect(self.toggleAnimation)
        if type%10==1:
            self.animation1.setStartValue(QtCore.QRectF(*t0,width, width))
            self.animation1.setEndValue(QtCore.QRectF(*t1,width, width))
        else:
            self.animation1.setStartValue(QtCore.QRectF(*t1,width, width))
            self.animation1.setEndValue(QtCore.QRectF(*t0,width, width))
        self.animation1.setDuration(last_time*500)
        self.animation1.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animation1.start()
        self.show()
    def toggleAnimation(self):
        a=self.animation1.startValue()
        self.animation1.setStartValue(self.animation1.endValue())
        self.animation1.setEndValue(a)
        self.animation1.start()
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        if self.shape==1:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
            painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1))
        elif self.shape==2:
            painter.fillRect(0, 0, self.side_width, self.side_width, QtGui.QColor(self.color))
        elif self.shape==3:
            p1 = QtCore.QPointF(self.width() / 2, (self.height() - self.side_width * 0.866) / 2)  # 0.866 为 sqrt(3)/2，即等边三角形的高度
            p2 = QtCore.QPointF((self.width() - self.side_width) / 2, (self.height() + self.side_width * 0.866) / 2)
            p3 = QtCore.QPointF((self.width() + self.side_width) / 2, (self.height() + self.side_width * 0.866) / 2)
            painter.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
            painter.drawPolygon(QtGui.QPolygonF([p1, p2, p3]))

def change_color():
    global items
    if (inputed:=box.currentText()) in li and (output:=box2.currentText()) in li and inputed!=output:
        key=f"{li.index(inputed)+1}x{li.index(output)+1}"
        for i in items:
            sip.delete(i)
        items = []
        for item in shapes:
            items+=[MoveLabel(item['type'],item['shape'],item['last_time'],key)]
        label.setStyleSheet(f"background:{bgcolor[key]};")
        label1.setStyleSheet(f"color:{bgcolor[key]};")
        output1.setStyleSheet(f"border:1px solid #fff;background:transparent;color:{bgcolor[key]};")

app=QtWidgets.QApplication(sys.argv)
main_window=QtWidgets.QMainWindow()
main_window.setGeometry(300,100,670,520)
main_window.setWindowIcon(QtGui.QIcon('logo.png'))
main_window.setWindowTitle('二次函數計算機')
central_widget = QtWidgets.QWidget(main_window)
li = ['一般式','頂點式','交點式']
bgcolor = {"1x2":"#7b040d","1x3":"#800076","2x1":"#7c8000","2x3":"#008013","3x1":"#2d0080","3x2":"#006080"}
colors={
    "1x2":["#fcc2c6","#fba4aa","#fa858d","#f96671","#f84754","#f72838","#f7091b"],
    "1x3":["#ffbffb","#ff9ff8","#ff80f5","#ff60f3","#ff40f1","#ff20ee","#ff00ec"],
    "2x1":["#feffbf","#fdff9f","#fcff80","#fbff60","#fbff40","#faff20","#f9ff00"],
    "2x3":["#bfffc9","#9fffae","#80ff93","#60ff78","#40ff5c","#20ff42","#00ff26"],
    "3x1":["#d6bfff","#c19fff","#ac80ff","#9860ff","#8340ff","#6f20ff","#5900ff"],
    "3x2":["#bfefff","#9fe8ff","#80dfff","#60d8ff","#2bcaff","#0bc2ff","#00afea"]
}
shapes=[
    {'type':22,'shape':3,'last_time':6},
    {'type':42,'shape':3,'last_time':2},
    {'type':41,'shape':1,'last_time':8},
    {'type':32,'shape':3,'last_time':2},
    {'type':32,'shape':1,'last_time':3},
    {'type':31,'shape':2,'last_time':5},
    {'type':42,'shape':2,'last_time':8},
    {'type':32,'shape':2,'last_time':4},
    {'type':11,'shape':1,'last_time':7},
    {'type':31,'shape':1,'last_time':3},
    {'type':22,'shape':2,'last_time':1},
    {'type':42,'shape':3,'last_time':4},
    {'type':42,'shape':2,'last_time':6},
    {'type':11,'shape':3,'last_time':2},
]
label = QtWidgets.QLabel(main_window)
label.setStyleSheet("background:#7b040d;")
label.setGeometry(0,0,670,520)
items = []
for item in shapes:
    items+=[MoveLabel(item['type'],item['shape'],item['last_time'])]
blur_effect = QtWidgets.QGraphicsBlurEffect()
blur_effect.setBlurRadius(90)
label.setGraphicsEffect(blur_effect)
main_window.setCentralWidget(central_widget)
window = QtWidgets.QWidget(main_window)
window.setGeometry(10, 10, 650, 500)
f = QtGui.QFont()
f.setFamily('System')
f.setPointSize(30)
f.setBold(True)
op0 = QtWidgets.QGraphicsOpacityEffect()
op0.setOpacity(0.6)
op1 = QtWidgets.QGraphicsOpacityEffect()
op1.setOpacity(0.6)
op2 = QtWidgets.QGraphicsOpacityEffect()
op2.setOpacity(0.6)
op3 = QtWidgets.QGraphicsOpacityEffect()
op3.setOpacity(0.5)
form = QtWidgets.QGridLayout(window)
label0 = QtWidgets.QLabel("請輸入二次函數：",window)
form.addWidget(label0,0,0,1,10)
input0 = QtWidgets.QLineEdit(window)
input0.setGraphicsEffect(op0)
input0.setGeometry(20, 70, 300, 40)
form.addWidget(input0,1,0,1,10)
box = QtWidgets.QComboBox(window)
box.addItems(["請選擇輸入函式類型", *li])
box.setGraphicsEffect(op1)
box.currentTextChanged.connect(change_color)
box.setGeometry(20, 120, 300, 20)
form.addWidget(box,2,0,1,10)
box2 = QtWidgets.QComboBox(window)
box2.addItems(["請選擇目標函式類型", *li])
box2.setGraphicsEffect(op2)
box2.currentTextChanged.connect(change_color)
box2.setGeometry(20, 150, 300, 20)
form.addWidget(box2,3,0,1,10)
parameter=QtWidgets.QComboBox(window)
parameter.addItems(["請選擇輸入的是哪種未知數的值","x","y"])
parameter.setGeometry(20, 150, 300, 20)
form.addWidget(parameter,4,0,1,10)
input1 = QtWidgets.QLineEdit(window)
input1.setGeometry(20, 70, 300, 40)
form.addWidget(input1,5,0,1,10)
btn = QtWidgets.QPushButton(window)
btn.setText('確認')
btn.setGeometry(20, 180, 100, 70)
btn.setStyleSheet("background:#5379FF; color:#FFAEC9; border-radius: 10px; border: 2px groove gray;border-style: outset;")
btn.clicked.connect(calculator)
form.addWidget(btn,6,0,2,4)
label1_bg= QtWidgets.QLabel("",window)
label1_bg.setStyleSheet("background-color:#ffffff;")
label1_bg.setGraphicsEffect(op3)
form.addWidget(label1_bg,39,0,1,10)
label1 = QtWidgets.QLabel("一般式 y=ax^2+bx+c\n頂點式 y=a(x+b/2a)^2+(4ac-b^2)/4a\n交點式 y=a(x-a)(x-b)\n\n就算該項係數為零也要寫\n不然它只會把輸入的二次函數\n原封不動的傳回來",window)
label1.setStyleSheet("color:#7b040d;")
form.addWidget(label1,39,0,1,10)
output1 = QtWidgets.QPlainTextEdit(window)
output1.setStyleSheet("border:1px solid #fff;background-color:transparent;color:#7b040d;")
output1.setGeometry(340, 70, 300, 400)
output1.setReadOnly(True)
form.addWidget(output1,0,10,40,1)
for i in [input0, output1, btn, box, box2]:
    i.setFont(f)
    i.show()
main_window.show()
sys.exit(app.exec())
