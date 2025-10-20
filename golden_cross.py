#load libraries 
import yfinance as yf  #access historical market data
import pandas as pd  #data manipulation
import sys # error occurs
import warnings 
warnings.filterwarnings("ignore") # ignore warning


class Trading:
    def __init__(self, symbol, from_date, to_date):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.df = None
        self.budget = 5000
        self.position = False
        self.share = 0
        self.profit = 0
        self.total = self.budget
        

    #Data Acquisition
    def load_data(self):
        try:
            self.df = yf.download(
                tickers=self.symbol, 
                start=self.from_date, 
                end=self.to_date,
                progress= False,
                threads=False
                )
            if isinstance(self.df, pd.DataFrame) and self.df.empty:
                sys.exit(f"Please write the correct ticker. No data found for ticker '{self.symbol}'.")
            elif 'Close' not in self.df.columns:
                sys.exit("Data does not contain 'Close' prices.")
            else:
                print(f"Data successfully loaded for '{self.symbol}'.")


        except Exception:
            sys.exit(f"Error occurred while fetching data for '{self.symbol}'. ")

    #Data Cleanup
    def clean_data(self):
        self.df = self.df.drop_duplicates(keep='first')
        self.df = self.df.ffill()
        print("Data cleanup Completed!")

    # Analytical Insights
    def insights(self):
        self.df['MA_50'] = self.df['Close'].rolling(window=50 , min_periods=50).mean()
        self.df['MA_200'] = self.df['Close'].rolling(window=200 , min_periods=200).mean()
        print('Calculated moving averages moving averages for 50 and 200 days.')

    # Golden Opportunity # Investment Strategy:
    def opportunity(self):

        for i in range(1, len(self.df)):
            today_50 = self.df['MA_50'].iloc[i]
            yesterday_50 = self.df['MA_50'].iloc[i-1]
            today_200 = self.df['MA_200'].iloc[i]
            yesterday_200 = self.df['MA_200'].iloc[i-1]
            today_close = self.df['Close'].iloc[i]

            # Golden Opportunity
            if (today_50 > today_200) and (yesterday_50 <= yesterday_200):
                #Investment Strategy
                if not self.position:
                    self.share = int(self.total // today_close)
                    if self.share > 0:
                        buy = int(self.share * today_close)
                        self.total -= buy
                        self.position = True
                        print(f'Number of {self.share} shares bought at {buy} USD')
        
            # Timely Actions
            elif (today_50 < today_200) and (yesterday_50 >= yesterday_200):
                if self.position:
                    sell = int(self.share * today_close)
                    self.total += sell
                    self.position = False
                    self.share = 0
                    print(f'All shares sold  at {sell} USD')


        # Final Touches
        if self.position:
            close_price = self.df['Close'].iloc[-1]
            self.total += int(self.share * close_price)
            self.position = False
            self.share = 0
    
    # Evaluation:
    def evaluation(self):
        self.profit = self.total - self.budget
        if self.profit > 0:
            print(f'Congrats! Your total profit "{self.profit}" USD')
        else:
            print(f'Bad Luck! Your total losses "{self.profit}" USD')


    # Execute  
    def run(self):
        try:
            self.load_data()
            self.clean_data()
            self.insights()
            self.opportunity()
            self.evaluation()
        except Exception as e:
            print(f"Something went wrong at: {e}")

# Example Run
if __name__ == "__main__":
    strategy = Trading("GOOG", "2018-01-01", "2023-12-31")
    strategy.run()
