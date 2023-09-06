# Black Scholes pricer
from scipy import stats
import numpy as np

def put_option_pricer(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + volatility * volatility / 2.0) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    print('Probability factor D1:', d1)
    print('Probability factor D2:', d2)
    # N(x) to calculate option price
    price = -stock_price * stats.norm.cdf(-d1) + strike_price * np.exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(-d2)
    return price

def call_option_pricer(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):
    d1 = (np.log(stock_price / strike_price) + (risk_free_rate + volatility * volatility / 2.0) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    print('Probability factor D1:', d1)
    print('Probability factor D2:', d2)
    # N(x) to calculate option price
    price = stock_price * stats.norm.cdf(d1) - strike_price * np.exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(d2)
    return price

