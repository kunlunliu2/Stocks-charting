from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtChart import QLineSeries, QBarSeries, QChartView, QChart
from PyQt5.QtCore import QMargins, Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import *
import math
import numpy as np
import pandas as pd
import sys
from datetime import datetime
from Indicators import Indicators
from stockFile import stockFile
import yfinance as yf

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 300))    
        self.setWindowTitle("Stock charting, by Kunlun Liu") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Input a stock: (^SPX)')
        self.nameLabel.resize(160, 20)
        self.line = QLineEdit(self)

        self.line.move(200, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 25)

        self.nameLabel1 = QLabel(self)
        self.nameLabel1.setText('Start day (YYYY-MM-DD):')
        self.nameLabel1.resize(160, 20)
        self.line1 = QLineEdit(self)
        self.line1.move(200, 60)
        self.line1.resize(200, 32)
        self.nameLabel1.move(20, 65)

        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('End day  (YYYY-MM-DD):')
        self.nameLabel2.resize(160, 20)
        self.line2 = QLineEdit(self)
        self.line2.move(200, 100)
        self.line2.resize(200, 32)
        self.nameLabel2.move(20, 105)

        self.nameLabel3 = QLabel(self)
        self.nameLabel3.setText('Compare to a stock \nfor relavent strength')
        self.nameLabel3.resize(160, 40)
        self.line3 = QLineEdit(self)
        self.line3.move(200, 140)
        self.line3.resize(200, 32)
        self.nameLabel3.move(20, 140)
        
        pybutton = QPushButton('Page A', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(160,32)
        pybutton.move(40, 250)        

        pybutton1 = QPushButton('Page B', self)
        pybutton1.clicked.connect(self.clickMethod1)
        pybutton1.resize(160,32)
        pybutton1.move(240, 250)        

    def clickMethod(self, checked):
        St = self.line.text()

        start_date = self.line1.text()
        dt = datetime.now()
        end_date = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
        x1 = "./stock.csv"
        
        pag = 1
        x = stockFile(x1, St, start_date, end_date)
        x.yahooData()

        stock2 = []
        stock2.append(x.stock.Date)
        stock2.append(x.stock.Open)
        stock2.append(x.stock.High)
        stock2.append(x.stock.Low)
        stock2.append(x.stock.Close)
        stock2.append(x.stock.Volume)
        self.w = AnotherWindow(stock2, St, start_date, end_date, 14, 50, 14, pag)
        self.w.show()

    def clickMethod1(self, checked):
        St = self.line.text()

        start_date = self.line1.text()
        dt = datetime.now()
        end_date = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
        x1 = "./stock.csv"
        
        pag = 2
        x = stockFile(x1, St, start_date, end_date)
        x.yahooData()

        St1 = self.line3.text()
        x2 = stockFile(x1, St1, start_date, end_date)
        x2.yahooData()

        stock2 = []
        stock2.append(x.stock.Date)
        stock2.append(x.stock.Open)
        stock2.append(x.stock.High)
        stock2.append(x.stock.Low)
        stock2.append(x.stock.Close)
        stock2.append(x.stock.Volume)
        stock2.append(x2.stock.Close)
        self.w = AnotherWindow(stock2, St, start_date, end_date, 14, 50, 14, pag)
        self.w.show()
        
class AnotherWindow(QtWidgets.QWidget):    
    def __init__(self, stock, name, start_date, end_date, Avg1, Avg2, Avg3, pag,
                 parent=None):
        super(AnotherWindow, self).__init__()
        win = QWidget()
        
        self.d = stock[0]
        self.o = stock[1]
        self.h = stock[2]
        self.l = stock[3]
        self.z = stock[4]
        self.v = stock[5]
        self.ind0 = []
        self.ind1 = []
        self.ind2 = []
        self.name = name
        self.stock = stock
        self.Avg1 = Avg1
        self.Avg2 = Avg2
        self.Avg3 = Avg3
        self.start_date = start_date
        self.end_date = end_date
        self.pag = pag
        self.TimeAxisX1 = []
        self.TimeAxisX2 = []

        if self.pag == 2:
            self.z1 = stock[6]

        self.step = 0.1
        self.x1 = 100
        self.y1 = 100
        self.y2 = 200
        view1 = self.creat_candelstick()
        view2 = self.creat_volumechart()
        view3 = self.creat_lndicatorchart()
        
        self.scrollbar = QtWidgets.QScrollBar(
            QtCore.Qt.Horizontal,
            sliderMoved=self.onAxisSliderMoved,
            pageStep=self.step * 100,
        )
        self.slider = QtWidgets.QSlider(
            QtCore.Qt.Horizontal, sliderMoved=self.onZoomSliderMoved
        )

        central_widget = QtWidgets.QWidget()

#        self.setCentralWidget(central_widget)

        lay = QtWidgets.QVBoxLayout(central_widget)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(view1, stretch=3)
        lay.addWidget(view2, stretch=1)
        lay.addWidget(view3, stretch=1)
        lay.addWidget(self.scrollbar)       
        lay.addWidget(self.slider)
        self.setLayout(lay)

        self.resize(1200, 800)

        self.adjust_axes(100, 200)
        min_x, max_x = 0, len(self.z)
        self.lims = np.array([min_x, max_x])

        self.onAxisSliderMoved(self.scrollbar.value())
        win.show()
        

    def creat_candelstick(self):
        self._candlestick_serie = QtChart.QCandlestickSeries()
        self._candlestick_serie.setDecreasingColor(QtGui.QColor(QtCore.Qt.red))
        self._candlestick_serie.setIncreasingColor(QtGui.QColor(QtCore.Qt.green))
        
        self._candlestick_serie.count = 100
        self._chart = QtChart.QChart()

        tm = []
        for i in range(0, len(self.z)):
            o_ = self.o[i]
            h_ = self.h[i]
            l_ = self.l[i]
            c_ = self.z[i]

            self._candlestick_serie.append(QtChart.QCandlestickSet(o_, h_, l_, c_))
            tm.append(str(i))
        min_x, max_x = 0, len(self.z)-1

        self._chart.addSeries(self._candlestick_serie)

        self._line0_serie = QLineSeries()
        self._line01_serie = QLineSeries()
        self._line02_serie = QLineSeries()
        self._line03_serie = QLineSeries()
        self._line0_serie.count = 100
        
        r = Indicators(self.z).EMA(self.Avg1)
        r1 = Indicators(self.z).EMA(self.Avg2)
        for i in range(len(r)):
            self._line0_serie.append(i, r[i])
            self._line01_serie.append(i, r1[i])
            self._line02_serie.append(i, r[i]*1.025)
            self._line03_serie.append(i, r[i]*0.975)
            
            
        self._line0_serie.setColor(QtGui.QColor(QtCore.Qt.blue))
        self._line01_serie.setColor(QtGui.QColor(QtCore.Qt.red))
        self._chart.addSeries(self._line0_serie)
        self._chart.addSeries(self._line01_serie)

        Pen1= QtGui.QPen()
        Pen1.setWidth(2);
        Pen1.setBrush(Qt.blue)
        self._line0_serie.setPen(Pen1)

        pen2 = QtGui.QPen()
        pen2 = QPen(Qt.red, 2, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        self._line01_serie.setPen(pen2)

        pen=QtGui.QPen()
        pen.setWidth(2)
        pen.setStyle(Qt.DashDotLine)
        pen.setBrush(Qt.green)
        self._line02_serie.setPen(pen)
        self._line03_serie.setPen(pen)
        self._chart.addSeries(self._line02_serie)
        self._chart.addSeries(self._line03_serie)

        self._chart.createDefaultAxes()
        self._chart.legend().hide()
        self._chart.axisX(self._candlestick_serie).setCategories(tm)
        self._chart.axisX(self._candlestick_serie).setVisible(False)

        d1 = 0
        if self.z[1] < 100:
            d1 = 20
        elif self.z[1] < 1000:
            d1 = 10
        self._chart.setMargins(QMargins(d1,0,0,0))

        self._chart_view = QtChart.QChartView()
        self._chart.axisX(self._line0_serie).setVisible(False)
        self._chart.axisX(self._line01_serie).setVisible(False)
        self._chart.axisX(self._line02_serie).setVisible(False)
        self._chart.axisX(self._line03_serie).setVisible(False)
        self._chart.setTitle(self.name);

        self.TimeAxisX1 = self.setTimeAxis()
        self._line03_serie.attachAxis(self.TimeAxisX1)
        self._chart.addAxis(self.TimeAxisX1, Qt.AlignBottom)

        font=QtGui.QFont()
        font.setPixelSize(20)
        font.setPointSize(20)
        self._chart.setTitleFont(font)


        self._chart_view = QChartView(self._chart)       
        
        return self._chart_view        


    def creat_volumechart(self):
        self._volume1_serie = QLineSeries()
        self._volume1_serie.count = 100

        if self.pag == 1:

            self._volume_serie = QtChart.QCandlestickSeries()
            self._volume_serie.setDecreasingColor(QtGui.QColor(QtCore.Qt.red))
            self._volume_serie.setIncreasingColor(QtGui.QColor(QtCore.Qt.green))
            
            self._volume_serie.count = 100
            c1 = 0.0
            for i in range(len(self.z)):
                c1 = max(c1, (self.z[i]+self.o[i])*self.v[i])
            c1 = 10.0 / c1
            list = []
            tm = []
            for i in range(0, len(self.z)):
                c = self.v[i]*(self.z[i]+self.o[i])*c1
                list.append(c)
                if self.o[i] > self.z[i]:
                    o_ = c
                    h_ = c
                    l_ = 0
                    c_ = 0
                else:
                    o_ = 0
                    h_ = c
                    l_ = 0
                    c_ = c

                self._volume_serie.append(QtChart.QCandlestickSet(o_, h_, l_, c_))
                tm.append(str(i))

            r = Indicators(list).EMA(self.Avg2)
            for i in range(1, len(self.v)):
                c = r[i]
                self._volume1_serie.append(i, c)

        else:

            self._volume_serie = QLineSeries()            
            self._volume_serie.count = 100

            c = self.z1[0] / self.z[0]
            a = 2.0 / (self.Avg1+1.0)
            c2 = 1.0
        
            for i in range(0, len(self.z)):
                c1 = self.z[i] / self.z1[i] * c
                self._volume_serie.append(i, c1)
                self.ind0.append(c1)
                
                c2 = c1 * a + c2 *(1.0-a)
                self._volume1_serie.append(i, c2)


        Pen= QtGui.QPen()
        Pen.setWidth(3);
        Pen.setBrush(Qt.black)
        self._volume1_serie.setPen(Pen)

        self._volume = QChart()

        self._volume.addSeries(self._volume_serie)
        self._volume.addSeries(self._volume1_serie)
        self._volume.createDefaultAxes()
        self._volume.legend().hide()
        if self.pag == 1:
            self._volume.axisX(self._volume_serie).setCategories(tm)
            self._volume.setTitle("Money flow: Volume*(Close+Open) (with its 50 days EMA)");
        else:
            st = "relavent strength and its 20-days EMA ( "+self.name+" performs better, when relavent strength >1 )" 
            self._volume.setTitle(st);

        self._volume.axisX(self._volume_serie).setVisible(False)
        self._volume.axisX(self._volume1_serie).setVisible(False)

        self._volume_view = QtChart.QChartView()
        self._volume.setMargins(QMargins(20,0,0,0))

        self.TimeAxisX2 = self.setTimeAxis()
        self._volume1_serie.attachAxis(self.TimeAxisX2)
        self._volume.addAxis(self.TimeAxisX2, Qt.AlignBottom)

        self._volume_view = QChartView(self._volume)
        
#        self._line.axisX(self._line_serie).setGridLineVisible(True)
#        self._line.axisX(self._line_serie).setShadesVisible(False)


        return self._volume_view        

    def creat_lndicatorchart(self):
        self._line3_serie = QLineSeries()
        self._line2_serie = QLineSeries()

        list = self.z


        if self.pag == 1:
            self.ind1 = Indicators(list).RSI(self.Avg3)

            list1 = []
            list1.append(self.o)
            list1.append(self.z)
            list1.append(self.v)
            self.ind2 = Indicators(list1).Volatility()
            
        else:
            self.ind1, self.ind2 = Indicators(list).MACD(5, 25, 10)
        
        for i in range(len(self.ind1)):
            self._line2_serie.append(i, self.ind1[i])
            self._line3_serie.append(i, self.ind2[i])

        Pen= QtGui.QPen()
        Pen.setWidth(2);
        Pen.setBrush(Qt.blue)
        self._line2_serie.setPen(Pen)

        Pen1= QtGui.QPen()
        Pen1.setWidth(2);
        Pen1.setBrush(Qt.red)
        self._line3_serie.setPen(Pen1)

        self._line3 = QChart()
        self._line3.addSeries(self._line2_serie)
        self._line3.addSeries(self._line3_serie)
        self._line3.createDefaultAxes()
        self._line3.legend().hide()

        print("3")

        self._line3_view = QtChart.QChartView()
        self._line3.setMargins(QMargins(20,0,0,0))

        if self.pag == 1:
            self._line3.setTitle("RSI (blue) and Volatility (red) (bullish when >50)");
        else:
            self._line3.setTitle("MACD (14,26,9)");
            
        self._line3_view = QChartView(self._line3)
        self._line3.axisX(self._line2_serie).setVisible(False)
        self._line3.axisX(self._line3_serie).setVisible(False)
        TimeaxisX = self.setTimeAxis()
        self._line3_serie.attachAxis(TimeaxisX)
        self._line3.addAxis(TimeaxisX, Qt.AlignBottom)
        axisPen= QtGui.QPen()
        axisPen.setWidth(3);
        TimeaxisX.setLinePen(axisPen);

        return self._line3_view
    
    def setTimeAxis(self):
        self.TimeAxisX = QtChart.QDateTimeAxis()
        self.TimeAxisX.setFormat("MM-dd-yyyy")
        s0 = pd.to_datetime(self.d[0],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMin(s0)
        leng = len(self.d)-1
        s0 = pd.to_datetime(self.d[leng],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMax(s0)
                
        self.TimeAxisX.setTickCount(20);
        self.TimeAxisX.setLabelsAngle(0)
        self.TimeAxisX.tickInterval = 20

        return self.TimeAxisX    

    def adjust_axes(self, value_min, value_max):
        value1 = value_max - 1
        self._chart.axisX(self._candlestick_serie).setRange(
            str(value_min), str(value1)
        )

        self._chart.axisX(self._line0_serie).setRange(
            value_min, value1
        )
        
        self._chart.axisX(self._line01_serie).setRange(
            value_min, value1
        )

        self._chart.axisX(self._line02_serie).setRange(
            value_min, value1
        )

        self._chart.axisX(self._line03_serie).setRange(
            value_min, value1
        )

        if self.pag == 1:
            self._volume.axisX(self._volume_serie).setRange(
                str(value_min), str(value1)
            )
        else:
            self._volume.axisX(self._volume1_serie).setRange(
                value_min, value1
            )

        self._volume.axisX(self._volume1_serie).setRange(
            value_min, value1
        )

        self._line3.axisX(self._line2_serie).setRange(
            value_min, value1
        )
        
        self._line3.axisX(self._line3_serie).setRange(
            value_min, value1
        )
                
        if value_min > 0 and value_max > 0 and value_max < 10000:
            ymin = np.amin(self.l[int(value_min): int(value1)])*0.95
            ymax = np.amax(self.h[int(value_min): int(value1)])*1.05
            self._chart.axisY(self._candlestick_serie).setRange(ymin, ymax)
            self._chart.axisY(self._line0_serie).setRange(ymin, ymax)
            self._chart.axisY(self._line01_serie).setRange(ymin, ymax)
            self._chart.axisY(self._line02_serie).setRange(ymin, ymax)
            self._chart.axisY(self._line03_serie).setRange(ymin, ymax)
            if self.pag == 1:
                self._volume.axisY(self._volume_serie).setRange(0, 10)
                self._volume.axisY(self._volume1_serie).setRange(0, 10)

                self._line3.axisY(self._line2_serie).setRange(10, 90)
                self._line3.axisY(self._line3_serie).setRange(10, 90)
            else:
                ymin1 = np.amin(self.ind0[int(value_min): int(value1)])*0.9
                ymax1 = np.amax(self.ind0[int(value_min): int(value1)])*1.1
                self._volume.axisY(self._volume_serie).setRange(ymin1, ymax1)
                self._volume.axisY(self._volume1_serie).setRange(ymin1, ymax1)
                
                ymin2 = np.amin(self.ind1[int(value_min): int(value1)])*0.9
                ymax2 = np.amax(self.ind1[int(value_min): int(value1)])*1.1
                ymax2 = max(ymax2, abs(ymin2))
                ymin2 = - ymax2
                    
                self._line3.axisY(self._line2_serie).setRange(ymin2, ymax2)
                self._line3.axisY(self._line3_serie).setRange(ymin2, ymax2)
                
            self.y1 = ymin
            self.y2 = ymax


        s0 = pd.to_datetime(self.d[value_min],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMin(s0)
        self.TimeAxisX1.setMin(s0)
        self.TimeAxisX2.setMin(s0)
        s0 = pd.to_datetime(self.d[value1],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMax(s0)
        self.TimeAxisX1.setMax(s0)
        self.TimeAxisX2.setMax(s0)
        
    @QtCore.pyqtSlot(int)
    def onAxisSliderMoved(self, value):
        r = value / ((1 + self.step) * 100)
        l1 = self.lims[0] + r * np.diff(self.lims)
        l2 = l1 + np.diff(self.lims) * self.step
        self.adjust_axes(math.floor(l1), math.ceil(l2))

    @QtCore.pyqtSlot(int)
    def onZoomSliderMoved(self, value):
        self.step=value/100
        self.onAxisSliderMoved(self.scrollbar.value())
        print(value)


        
if __name__ == "__main__":

        
    app = QtWidgets.QApplication(sys.argv)
        
    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
