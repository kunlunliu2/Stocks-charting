import yfinance as yf

class stockFile:
    def __init__(self, NameOfFile, StockNames, start_date, end_date):

        self.file = NameOfFile
        self.N = 0
        self.Name = StockNames
        self.stockAna1 = []
        self.stock = []
        self.stockAna2 = []
        self.macd1 = []
        self.macd2 = []
        self.rsi = []
        self.vforce = []

        self.start_date = start_date
        self.end_date = end_date
        
    def yahooData(self):
        print(self.Name)
        self.stock = yf.download(tickers = self.Name,
                  start = self.start_date,
                  end = self.end_date)
        self.stock.reset_index(inplace=True)

    def readData(self):
        with open(self.file, 'r') as fp2:
            self.stock = pd.read_csv(self.file)
        
        fp2.close()

            
    def writefile(self):
        with open(self.file, 'w') as fp2:
            for i in range(len(self.stock)):
                for j in range(len(self.stock[i])):
                    fp2.write(str(self.stock[j][i])+ ",")
                fp2.write("\n")
        fp2.close()

