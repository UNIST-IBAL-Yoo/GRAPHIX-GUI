import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pressure_plot_ch1 import *
from pressure_plot_ch2 import *
from connect_ioc import *

main_ui_class = uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, main_ui_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.versionOutput.setText(get_version_CMD())
        self.snOutput.setText(get_sn_CMD())
        self.pnOutput.setText(get_pn_CMD())
        self.ch1Press.clicked.connect(self.subPlotch1)
        self.ch2Press.clicked.connect(self.subPlotch2)
        self.sendButton.clicked.connect(self.send_CMD)
        self.receiveButton.clicked.connect(self.get_CMD)

    def subPlotch1(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = SubPlotCh1()
        self.ui.setupPlot()
    
    def subPlotch2(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = SubPlotCh2()
        self.ui.setupPlot()
        
    def send_CMD(self):
        if self.readSelButton.isChecked():
            pGr = self.pGroup.value()
            pNo = self.pNumber.value()
            send_read_CMD(pGr, pNo)
        elif self.writeSelButton.isChecked():
            pGr = self.pGroup.value()
            pNo = self.pNumber.value()
            inpVal = self.inputValue.text()
            send_write_CMD(pGr, pNo, inpVal)
        
    def get_CMD(self):
        if self.readSelButton.isChecked():
            self.outputValue.clear()
            gotVal = get_read_CMD()
            self.outputValue.setText(gotVal)
        elif self.writeSelButton.isChecked():
            self.outputValue.clear()
            gotVal = get_write_CMD()
            self.outputValue.setText(gotVal)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
