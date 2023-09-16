from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtChart import QLineSeries, QBarSeries, QChartView, QChart
from PyQt5.QtCore import QMargins, Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
import math
import numpy as np
import pandas as pd
import sys
from datetime import datetime
from Indicators import Indicators
from stockFile import stockFile
import yfinance as yf

St =  "^SPX"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, stock, name, start_date, end_date, Avg1, Avg2, Avg3,
                 parent=None):
        super().__init__(parent)

        self.d = stock[0]
        self.o = stock[1]
        self.h = stock[2]
        self.l = stock[3]
        self.z = stock[4]
        self.v = stock[5]
        self.name = name
        self.stock = stock
        self.Avg1 = Avg1
        self.Avg2 = Avg2
        self.Avg3 = Avg3
        self.start_date = start_date
        self.end_date = end_date

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
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QVBoxLayout(central_widget)
        lay.addWidget(view1, stretch=3)
        lay.addWidget(view2, stretch=1)
        lay.addWidget(view3, stretch=1)
        lay.addWidget(self.scrollbar)
        lay.addWidget(self.slider)

        self.resize(640, 480)

        self.adjust_axes(100, 200)
        min_x, max_x = 0, len(self.z)
        self.lims = np.array([min_x, max_x])

        self.onAxisSliderMoved(self.scrollbar.value())
        

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
        self._line0_serie.count = 100

        y1 = self.z[0]
        self._line0_serie.append(0, y1)
        k1 = 2.0 / (self.Avg1 +1.0)
        k2 = 2.0 / 51
        y2 = y1
        for i in range(1, len(self.z)):
            c = self.z[i]
            c1 = c
            c = c * k1 + y1 * (1-k1)
            y1 = c
            c1 = c1*k2 + y2 * (1-k2)
            y2 = c1
            self._line0_serie.append(i, c)
            self._line01_serie.append(i, c1)
        self._line0_serie.setColor(QtGui.QColor(QtCore.Qt.blue))
        self._line01_serie.setColor(QtGui.QColor(QtCore.Qt.green))
        self._chart.addSeries(self._line0_serie)
        self._chart.addSeries(self._line01_serie)

        self._chart.createDefaultAxes()
        self._chart.legend().hide()
        self._chart.axisX(self._candlestick_serie).setCategories(tm)
        self._chart.axisX(self._candlestick_serie).setVisible(False)
        self._chart.setMargins(QMargins(0,0,50,0))

        self._chart_view = QtChart.QChartView()
        self._chart.axisX(self._line0_serie).setVisible(False)
        self._chart.axisX(self._line01_serie).setVisible(False)
        self._chart.setTitle(self.name);

        font=QtGui.QFont()
        font.setPixelSize(20)
        font.setPointSize(20)
        self._chart.setTitleFont(font)
        
        self._chart_view = QChartView(self._chart)       
        
        return self._chart_view        


    def creat_volumechart(self):
        self._volume_serie = QLineSeries()
        self._volume1_serie = QLineSeries()
        self._volume1_serie.count = 100

        c1 = 10.0/np.max(self.v)
        list = []
        for i in range(0, len(self.v)):
            c = self.v[i]*c1
            self._volume_serie.append(i, c)
            list.append(c)

        r = Indicators(list).EMA(self.Avg2)
        for i in range(1, len(self.v)):
            c = r[i]
            self._volume1_serie.append(i, c)

        self._volume1_serie.setColor(QtGui.QColor(QtCore.Qt.red))

        Pen= QtGui.QPen()
        Pen.setWidth(2);
        self._volume_serie.setPen(Pen);

        self._volume = QChart()
        self._volume.addSeries(self._volume_serie)
        self._volume.addSeries(self._volume1_serie)
        self._volume.createDefaultAxes()
        self._volume.legend().hide()

        self._volume_view = QtChart.QChartView()
        self._volume.setMargins(QMargins(15,0,50,0))

        self._volume.setTitle("Volume (with its 50 days EMA)");

        self._volume_view = QChartView(self._volume)
        self._volume.axisX(self._volume_serie).setVisible(False)
        self._volume.axisX(self._volume1_serie).setVisible(False)
        
#        self._line.axisX(self._line_serie).setGridLineVisible(True)
#        self._line.axisX(self._line_serie).setShadesVisible(False)


        return self._volume_view        

    def creat_lndicatorchart(self):
        self._line3_serie = QLineSeries()
        list = self.stock[4]
        r = Indicators(list).RSI(self.Avg3)
        
        for i in range(len(r)):
            self._line3_serie.append(i, r[i])

        self._line3 = QChart()
        self._line3.addSeries(self._line3_serie)
        self._line3.createDefaultAxes()
        self._line3.legend().hide()

        self._line3_view = QtChart.QChartView()
        self._line3.setMargins(QMargins(15,0,15,0))
        self._line3.setTitle("RSI");

        self._line3_view = QChartView(self._line3)
        self._line3.axisX(self._line3_serie).setVisible(False)
        TimeaxisX = self.setTimeAxis()
        self._line3_serie.attachAxis(TimeaxisX)
        self._line3.addAxis(TimeaxisX, Qt.AlignBottom)
        axisPen= QtGui.QPen()
        axisPen.setWidth(2);
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
           
    def creat_barchart(self):
        self._bar_serie = QBarSeries()
        c1 = 10.0/np.max(self.stock[5])
        
        for i in range(0, len(z)):
            barset = QBarSet(str(i))
            c = self.stock[5][i]*c1
            barset.append(c)
            self._bar_serie.append(barset)

        self._bar = QChart()
        self._bar.addSeries(self._bar_serie)
        self._bar.createDefaultAxes()
        self._bar.legend().hide()
        self._bar_serie.count = 100

        self.axisX2 = QBarCategoryAxis()
        time1 = []
        for i in range(len(v)):
            c = pd.to_datetime(self.d[i],format='%m/%d/%Y %H:%M')
            c1 = str(c.month) + "-" + str(c.day) + "-" + str(c.year)
            time1.append(c1)
        self.axisX2.append(time1)
        
        self._bar.addAxis(self.axisX2, Qt.AlignBottom)
        
        self._bar_view = QtChart.QChartView()

        self._bar_view = QChartView(self._bar)

        return self._bar_view        

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
        
        self._volume.axisX(self._volume_serie).setRange(
            value_min, value1
        )

        self._volume.axisX(self._volume1_serie).setRange(
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
            self._volume.axisY(self._volume_serie).setRange(0, 10)
            self._volume.axisY(self._volume1_serie).setRange(0, 10)
            self._line3.axisY(self._line3_serie).setRange(10, 90)
            self.y1 = ymin
            self.y2 = ymax

        s0 = pd.to_datetime(self.d[value_min],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMin(s0)
        s0 = pd.to_datetime(self.d[value1],format='%m/%d/%Y %H:%M')
        self.TimeAxisX.setMax(s0)
        
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

    start_date = "2016-1-1"
    dt = datetime.now()
    end_date = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
    print(end_date)

#    St =  ["^RUT", "SOXL", "UAL", "AAPL", "JPM", "CAT", "MSFT", "AMZN"]
    x1 = "./stock.csv"
        
    x = stockFile(x1, St, start_date, end_date)
    x.yahooData()

    stock2 = []
    stock2.append(x.stock.Date)
    stock2.append(x.stock.Open)
    stock2.append(x.stock.High)
    stock2.append(x.stock.Low)
    stock2.append(x.stock.Close)
    stock2.append(x.stock.Volume)    
        
    app = QtWidgets.QApplication(sys.argv)
        
    w = MainWindow(stock2, St, start_date, end_date, 14, 50, 14)
    w.show()

    sys.exit(app.exec_())
