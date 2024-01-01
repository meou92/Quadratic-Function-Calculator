from PyQt6 import QtWidgets, QtGui, QtCore
import sys

def int_all(*arg:float):
    Return=[]
    for i in arg:
        Return += [int(i) if i % 1==0.0 else i]
    return Return

def general_expression(a:float|int,b:float|int,c:float|int):
    """一般式"""
    a,b,c,=int_all(a,b,c)
    return f"y={a}x^2+{b}x+{c}"

def intersection_formula(a:float|int,b:float|int,c:float|int):
    """交點式"""
    if (delta:=[d:=b**2-4*a*c, pow(d, 1/2)])[0]>=0:
        a1,x1,x2,=int_all(a,(0-b+delta[1])/(2*a),(0-b-delta[1])/(2*a))
        return f"y={a1}(x+{0-x1})(x+{0-x2})"
    else:
        return 'error'

def Vertex_type(a:float|int,b:float|int,c:float|int):
    """頂點式"""
    a,x1,x2,=int_all(a,b/(2*a),(4*a*c-b**2)/(4*a))
    return f"y={a}(x+{x1})^2+{x2}"

class equation(QtWidgets.QLineEdit):
    def __init__(self) -> None:
        super().__init__(window)
        self.select=''
        self.target=''
        self.Return=''
    def check(self):
        ans = []
        self.select=box.currentText()[:3]
        self.target=box2.currentText()[:3]
        a=1
        if (t:=self.text())[2]not in'+-':
            t=t[:2]+'+'+t[2:]
        if t[3]in'x(':
            t=t[:3]+'1'+t[3:]
        AnsListNum=[0]
        for ai in range(len(t)):
            try:
                int(t[ai])
            except:
                if t[ai]=='(':
                    if t[AnsListNum[-1]:ai]!=''and t[AnsListNum[-1]:ai]!='y=' :ans+=[t[AnsListNum[-1]:ai]]
                    if t[ai:t.index(')')+1]!='':ans+=[t[ai:t.index(')')+1]]
                    AnsListNum+=[t.index(')')]
                    continue
                elif t[ai] in '+-*/' and t[AnsListNum[-1]:ai]!='':
                    ans+=[t[AnsListNum[-1]:ai]]
                    AnsListNum+=[ai]
                elif t[ai]=='=' and t[AnsListNum[-1]:ai]!='':
                    AnsListNum+=[ai+1]
                    ans+=[t[AnsListNum[-2]:ai],'=']
        ans+=[t[AnsListNum[-1]:]]
        ans+=['-next\n']
        if ans[2][-3:]=='x^2':
            a=int(ans[2][:-3])
        else:
            a=int(ans[2])
        b=0
        c=0
        f=float(ans[3][3:-1]) if ans[3][3:-1]!='' else 1
        if self.select=='一般式':
            b=int(ans[3][:-1]) if ans[2][:-1]!='' else 1
            try:
                c=int(ans[4]) if ans[4] not in ['','\n'] else 0
            except:...
        elif self.select=='頂點式':
            b=f*2*a
            c=f**2*a
            if len(ans)==7:
                c+=float(ans[5])
        else:
            g=0
            if len(ans)>7:
                g=float(ans[6][:-1]) if ans[6][:-1]!='' else 0
            elif len(ans)==7:
                g=float(ans[5][:-1]) if ans[5][:-1]!='' else 0
            b=a*(f+g)
            c=a*f*g
        if self.target=='一般式':
            self.Return=general_expression(a,b,c)
        elif self.target=='頂點式':
            self.Return=Vertex_type(a,b,c)
        else:
            self.Return=intersection_formula(a,b,c)
        m,n,=int_all(0-(b/(2*a)),(4*a*c-b**2)/(4*a))
        self.Return+=f'\n頂點在({m},{n}), '
        self.Return+='開口朝上' if a>0 else '開口朝下'
        input1.setPlainText('')
        input1.insertPlainText(self.Return)

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setGeometry(200, 200, 650, 500)
window.setWindowTitle('二次函數計算機')
window.show()
f = QtGui.QFont()
f.setFamily('System')
f.setPointSize(30)
f.setBold(True)
l0 = QtWidgets.QLabel(window)
l0.setGeometry(20, 20, 300, 40)
l0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
l0.setStyleSheet('background:#5379FF;color:#FFAEC9;border: 3px solid #FFAEC9;text-align:center;')
l0.setText("Input")
l1 = QtWidgets.QLabel(window)
l1.setText("Output")
l1.setStyleSheet('background:#5379FF;color:#FFAEC9;border: 3px solid #FFAEC9;text-align:center;')
l1.setGeometry(340, 20, 300, 40)
l1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
input0 = equation()
input0.setGeometry(20, 70, 300, 40)
box = QtWidgets.QComboBox(window)
box.addItems(['一般式 y=ax^2+bx+c','頂點式 y=a(x+b/2a)^2+(4ac-b^2)/4a','交点式 y=a(x-a)(x-b)'])
box.setGeometry(20, 120, 300, 20)
box2 = QtWidgets.QComboBox(window)
box2.addItems(['一般式 y=ax^2+bx+c','頂點式 y=a(x+b/2a)^2+(4ac-b^2)/4a','交点式 y=a(x-a)(x-b)'])
box2.setGeometry(20, 150, 300, 20)
btn = QtWidgets.QPushButton(window)
btn.setText('確認')
btn.setGeometry(20, 180, 70, 40)
btn.setStyleSheet("""
    QPushButton {background:#5379FF;color:#FFAEC9;border: 3px solid #FFAEC9;}
    QPushButton:hover {color: #ff0;background: #f00;}
""")
btn.clicked.connect(input0.check)
input1 = QtWidgets.QPlainTextEdit(window)
input1.setGeometry(340, 70, 300, 400)
input1.setReadOnly(True)
for i in [l0, l1, input0, input1, btn, box, box2]:
    i.setFont(f)
    i.show()
sys.exit(app.exec())