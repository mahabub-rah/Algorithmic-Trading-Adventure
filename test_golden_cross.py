import pytest
from golden_cross import Trading
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOG"]
from_date = "2022-01-01"
to_date = "2022-12-31"

#Test Data Acquisition
@pytest.mark.parametrize("ticker", tickers)
def test_load_data(ticker):
    strategy = Trading(ticker, from_date, to_date)
    strategy.load_data()
    assert isinstance(strategy.df, pd.DataFrame)
    assert not strategy.df.empty
    assert 'Close' in strategy.df.columns


@pytest.mark.parametrize("ticker", tickers)
def test_clean_data(ticker):
    strategy = Trading(ticker, from_date, to_date)
    strategy.load_data()
    strategy.clean_data()
    assert not strategy.df.index.duplicated().any()

# Test Analytical Insights
@pytest.mark.parametrize("ticker", tickers)
def test_insights(ticker):
    strategy = Trading(ticker, from_date, to_date)
    strategy.load_data()
    strategy.clean_data()
    strategy.insights()
    assert 'MA_50' in strategy.df.columns
    assert 'MA_200' in strategy.df.columns

# Test Execute
@pytest.mark.parametrize("ticker", tickers)
def test_run(ticker):
    strategy = Trading(ticker, from_date, to_date)
    strategy.run()
    assert isinstance(strategy.profit, (int, float))


# Test Invalid
def test_invalid_ticker(): 
    strategy = Trading("INVALID123", from_date, to_date) 
    with pytest.raises(SystemExit): 
        strategy.load_data()