# Value at Risk Monte Carlo Simulation

import pandas as pd
import yfinance as yf
import numpy as np


def download_adj_close_data(ticker, start_date, end_date):
    data = {}
    ticker_data = yf.download(ticker, start_date, end_date)
    data['Adj Close'] = ticker_data['Adj Close']
    return pd.DataFrame(data)

class MonteCarloSimulation:
    def __init__(self, iterations, investment, mean, std, confidence, days):
        self.iterations = iterations
        self.investment = investment
        self.mean = mean
        self.std = std
        self.confidence = confidence
        self.days = days

    def simulate(self):
        random = np.random.normal(0, 1, [1, self.iterations])
        # S(t) asset price
        asset_price = self.investment * np.exp(self.days * (self.mean - 0.5 * self.std ** 2) + self.std * np.sqrt(self.days) * random)
        # Sort asset prices to determine percentile
        asset_price = np.sort(asset_price)
        # Confidence levels: 95% -> 5, 99% -> 1
        percentile = np.percentile(asset_price, (1 - self.confidence) * 100)
        return self.investment - percentile

