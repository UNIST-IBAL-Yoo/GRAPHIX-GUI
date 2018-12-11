# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 13:30:03 2018
@author: Kyounghun Yoo
Plot Pressure Data in Ch. 2
"""

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import time
from connect_ioc import *
from utils import *


class SubPlotCh2(QtWidgets.QWidget):
    def setupPlot(self):
        vbox = QtWidgets.QVBoxLayout()
        self.pw1 = pg.PlotWidget(
                        title="Pressure Data", 
                        labels={'left':'Pressure (mbar)'},
                        axisItems = {'bottom':TimeAxisItem(orientation='bottom')}
                        )

        self.le1 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.le1.setFont(font)

        vbox.addWidget(self.pw1)
        vbox.addWidget(self.le1)
        self.setLayout(vbox)

        self.setWindowTitle("Pressure Data")

        self.x = []
        self.y = []
        self.pl = self.pw1.plot(pen='w')

        self.mytimer = QtCore.QTimer()
        self.mytimer.start(1000)  
        self.mytimer.timeout.connect(self.get_data)

        self.draw_chart(self.x, self.y)
        self.show()

    def draw_chart(self, x, y):
        self.pl.setData(x=x, y=y)  # line chart 그리기

    @QtCore.pyqtSlot()
    def get_data(self):
        currentTime = timestamp()
        currentTimeStr = time.ctime()
        self.x.append(currentTime)
        pressData = get_press2_CMD()
        pressUnit = get_unit_CMD()
        self.y.append(float(pressData))

        self.le1.setText("Current Pressure\t :\t" 
                       + pressData + "\t" + pressUnit)
        
        logFile = open("Pressure_Data.csv", "a")
        logFile.write("\n")
        logFile.write("{timestamp},{time},{pressure},{unit}".
                                          format(timestamp=currentTime,
                                                 time=currentTimeStr,
                                                 pressure=pressData
                                                 unit=pressUnit
                                                ))
        logFile.close()

        self.draw_chart(self.x, self.y)
