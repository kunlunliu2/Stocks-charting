import pandas as pd

class Indicators:
    def __init__(self, stock):
        self.stock = stock
        self.avg0 = 14
        self.avg1 = 20
        self.rsi = []
        self.ema = []
        self.obv = []

    def RSI(self, avg0):
        a = 1.0 / avg0
        gain = 0
        loss = 0
        for i in range(1, len(self.stock)):
            e = (self.stock[i] - self.stock[i-1])
            if(i > self.avg0-1):
                if e > 0:
                    gain = (gain * (avg0-1) + e) * a
                    loss = loss * (avg0 - 1.0) * a
                else:
                    gain = gain * (avg0 - 1.0) * a
                    loss = (loss * (avg0-1) - e) * a
                c = 100.0 * gain / (gain + loss)

            else:
                if e > 0:
                    gain = gain + e * a
                else:
                    loss = loss - e * a
                c = 50.0
            self.rsi.append(c)

        return self.rsi
                
    def EMA(self, avg1):
        self.avg1 = avg1
        a = 2.0 / (self.avg1+1.0)
        c = self.stock[0]
        self.ema.append(c)
        for i in range(1, len(self.stock)):
            c = self.stock[i] * a + c * (1.0 - a)
            self.ema.append(c)

        return self.ema

    def OBV(self):
        a = 2.0 / (self.avg1+1.0)
        c = self.stock[1][0]
        self.obv.append(c)
        for i in range(1, len(self.stock[0])):
            e = (self.stock[0][i] - self.stock[0][i-1])
            if(e > 0):
                c = c + self.stock[1][0]
            elif (e < 0):
                c = c -  self.stock[1][0]
                
            self.obv.append(c)

        return self.obv


#df = pd.read_csv('result2.csv',
#                         index_col='DATE',
#                         parse_dates=True,
#                         infer_datetime_format=True)
#                         engine='python')

#stock = df.iloc[:, 0].values
#f = Indicators(stock)
#g = f.RSI1()
#print(g)
