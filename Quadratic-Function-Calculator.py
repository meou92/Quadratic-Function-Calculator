import sys
from PyQt6 import QtWidgets,QtGui,QtCore,sip

def calculator():
    if "x^2" in (func:=input0.text()) and "x" in func[func.index("x^2")+3:] and (inputed:=box.currentText()) in li and (output:=box2.currentText()) in li:
        ans = []
        if (t:=func)[2]not in'+-':
            t=t[:2]+'+'+t[2:]
        if t[3]in'x(':
            t=t[:3]+'1'+t[3:]
        AnsListNum=[0]
        for ai in range(len(t)):
            if t[ai] in "0123456789.":
                pass
            elif t[ai]=='(':
                if t[AnsListNum[-1]:ai]!=''and t[AnsListNum[-1]:ai]!='y=' :
                    ans+=[t[AnsListNum[-1]:ai]]
                if t[ai:t.index(')')+1]!='':
                    ans+=[t[ai:t.index(')')+1]]
                AnsListNum+=[t.index(')')]
            elif t[ai] in '+-*/' and t[AnsListNum[-1]:ai]!='':
                ans+=[t[AnsListNum[-1]:ai]]
                AnsListNum+=[ai]
            elif t[ai]=='=' and t[AnsListNum[-1]:ai]!='':
                AnsListNum+=[ai+1]
                ans+=[t[AnsListNum[-2]:ai],'=']
        ans+=[t[AnsListNum[-1]:]]
        a=float(ans[2][:-3]) if ans[2][-3:]=='x^2' else float(ans[2])
        f=float(ans[3][3:-1]) if ans[3][3:-1]!='' else 1
        if inputed=='一般式':
            b=float(ans[3][:-1]) if ans[2][:-1]!='' else 1
            c=float(ans[4]) if len(ans)>4 else 0
        elif inputed=='頂點式':
            b=f*2*a
            c=f**2*a
            if len(ans)==6:
                c+=float(ans[5])
        else:
            g=0
            if len(ans)>6:
                g=float(ans[6][:-1]) if ans[6][:-1]!='' else 0
            elif len(ans)==6:
                g=float(ans[5][:-1]) if ans[5][:-1]!='' else 0
            b=a*(f+g)
            c=a*f*g
        x1=b/(2*a)
        x2=c-(b**2)/(4*a)
        if output=='一般式':
            Return=f"y={a}x^2+{b}x+{c}"
        elif output=='頂點式':
            Return=f"y={a}(x+{x1})^2+{x2}"
        else:
            if (delta:=[d:=b**2-4*a*c, pow(d, 1/2)])[0]>=0:
                Return=f"y={a}(x{positive((0-b+delta[1])/(2*a))})(x{positive((0-b-delta[1])/(2*a))})"
            else:
                Return='error'
        input1.setPlainText(f"{Return}\n頂點在({0-x1},{x2}), {'開口朝上' if a>0 else '開口朝下'}")
    else:
        input1.setPlainText(func)

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
            r0=QtCore.QRectF(0, 0, self.width(), self.height())
            r1=QtCore.QRectF(label.width() - width, label.height() - width, width, width)
        elif type//10==2:
            r0=QtCore.QRectF((label.width()-width)//2,0,width, width)
            r1=QtCore.QRectF((label.width()-width)//2,label.height()-width,width, width)
        elif type//10==3:
            r0=QtCore.QRectF(label.width()-width,0,width, width)
            r1=QtCore.QRectF(0,label.height()-width,width, width)
        elif type//10==4:
            r0=QtCore.QRectF(label.width()-width,(label.height()-width)//2,width, width)
            r1=QtCore.QRectF(0,(label.height()-width)//2,width, width)
        self.animation = QtCore.QPropertyAnimation(self, b'geometry')
        self.animation.finished.connect(self.toggleAnimation)
        if type%10==1:
            self.animation.setStartValue(r0)
            self.animation.setEndValue(r1)
        else:
            self.animation.setStartValue(r1)
            self.animation.setEndValue(r0)
        self.animation.setDuration(last_time*1000)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animation.start()
    def toggleAnimation(self):
        a=self.animation.startValue()
        self.animation.setStartValue(self.animation.endValue())
        self.animation.setEndValue(a)
        self.animation.start()
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
            i=MoveLabel(item['type'],item['shape'],item['last_time'],key)
            i.show()
            items+=[i]
        label.setStyleSheet(f"background:{bgcolor[key]};")

positive = lambda num : "" if num == 0.0 else f"+{0-num}" if num < 0 else f"-{num}"
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
    {'type':11,'shape':3,'last_time':8},
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
op0.setOpacity(0.5)
op1 = QtWidgets.QGraphicsOpacityEffect()
op1.setOpacity(0.5)
op2 = QtWidgets.QGraphicsOpacityEffect()
op2.setOpacity(0.5)
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
btn = QtWidgets.QPushButton(window)
btn.setText('確認')
btn.setGeometry(20, 180, 70, 40)
btn.setStyleSheet("""
    QPushButton {background:#5379FF;color:#FFAEC9;}
    QPushButton:hover {background:#5379FF;color:#FFAEC9;}
""")
btn.clicked.connect(calculator)
form.addWidget(btn,4,0)
label1 = QtWidgets.QLabel("一般式 y=ax^2+bx+c\n頂點式 y=a(x+b/2a)^2+(4ac-b^2)/4a\n交點式 y=a(x-a)(x-b)\n\n就算該項係數為零也要寫\n不然它只會把輸入的二次函數原封不動的傳回來",window)
form.addWidget(label1,15,0,1,10)
input1 = QtWidgets.QPlainTextEdit(window)
input1.setStyleSheet("""
    QPlainTextEdit {
        border:1px solid #fff;
        background-color:transparent;
        color:#f00;
    }
""")
input1.setGeometry(340, 70, 300, 400)
input1.setReadOnly(True)
form.addWidget(input1,0,10,40,1)
for i in [input0, input1, btn, box, box2]:
    i.setFont(f)
    i.show()
main_window.show()
sys.exit(app.exec())