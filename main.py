#load libraries 
import yfinance as yf  #access historical market data
import pandas as pd  #data manipulation 
import warnings
warnings.filterwarnings("ignore")


class Trading:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.df = None

    #Data Acquisition
    def load_data(self):
        try:
            self.df = yf.download(
                tickers=self.symbol, 
                start=self.start_date, 
                end=self.end_date,
                progress= False,
                threads=False
                )
            if isinstance(self.df, pd.DataFrame) and self.df.empty:
                print(f"Please write the correct ticker. No data found for ticker '{self.symbol}'.")
                return False
            else:
                print(f"Data successfully loaded for '{self.symbol}'.")
                return True

        except Exception:
            print(f"Error occurred while fetching data for '{self.symbol}'. ")
            return False

    #Data Cleanup
    def clean_data(self):
        self.df = self.df.drop_duplicates(keep='first')
        self.df = self.df.ffill()
        print("Data cleanup Completed!")

    # Analytical Insights
    def insights(self):
        print("Analytical Insights")



    
    # execute  
    def run(self):
        self.load_data()
        self.clean_data()
        self.insights()

# Example Run
strategy = Trading("AAPL", "2018-01-01", "2023-12-31")
strategy.run()
