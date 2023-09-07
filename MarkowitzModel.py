import matplotlib.pyplot as plt
import scipy.optimize as optimization
import numpy as np
import yfinance as yf
import pandas as pd

TRADING_DAYS = 252
PORTFOLIOS = 100000

# Download yfinance data for selected stocks, from start_date - end_date
def download_data(start_date, end_date, stocks):
    close_data = {}
    for s in stocks:
        ticker = yf.Ticker(s)
        close_data[s] = ticker.history(start=start_date, end=end_date)['Close']
    return pd.DataFrame(close_data)

# Compute noralized log returns for each stock
def compute_returns(data):
    # Normalize with logs
    log_return = np.log(data / data.shift(1))
    return log_return[1:]

# Compute mean and covariance of returns
def compute_statistics(returns):
    # Mean of annual return
    print('ANNUAL MEAN: \n' + str(returns.mean() * TRADING_DAYS))
    print('\nCOVARIANCE MATRIX: \n' + str(returns.cov() * TRADING_DAYS))

# Compute mean and volatility of portfolio
def compute_mean_variance(returns, weights):
    ret = np.sum(returns.mean() * weights) * TRADING_DAYS
    vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * TRADING_DAYS, weights)))
    print('Expected portfolio mean: '+ str(ret))
    print('Expected portfolio volatility: '+ str(vol))

# Generate random portfolios
def generate_portfolios(returns, stocks):
    means = []
    risks = []
    weights = []

    for _ in range(PORTFOLIOS):
        weight = np.random.random(len(stocks))
        weight /= np.sum(weight)
        mean = np.sum(returns.mean() * weight) * TRADING_DAYS
        risk = np.sqrt(np.dot(weight.T, np.dot(returns.cov() * TRADING_DAYS, weight)))
        weights.append(weight)
        means.append(mean)
        risks.append(risk)

    return np.array(weights), np.array(means), np.array(risks)

# Portfolio statistics, containing returns, volatility and sharpe ratio
def portfolio_statistics(weights, returns):
    ret = np.sum(returns.mean() * weights) * TRADING_DAYS
    vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * TRADING_DAYS, weights)))
    return np.array([ret, vol, ret/vol])

def minimize_sharpe_ratio(weights, returns):
    return -portfolio_statistics(weights, returns)[2]

# Minimize f(x) = 0, where sum of weights equivalent to 1
def optimize_portfolio(weights, returns, stocks):
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(stocks)))
    optimum = optimization.minimize(fun=minimize_sharpe_ratio, x0=weights[0], args=returns,
                                    method='SLSQP', bounds=bounds, constraints=constraints)
    print('Optimal portfolio: ' + str(optimum['x'].round(3)))
    print('Expected return, volatility and Sharpe ratio: ' + str(portfolio_statistics(optimum['x'].round(3), returns)))
    return optimum

# Plot data
def plot_data(data):
    data.plot(figsize=(10, 6))
    plt.show()

# Plot portfolios
def plot_portfolios(returns, vol):
    plt.figure(figsize=(10, 6))
    plt.grid(True)
    plt.scatter(vol, returns, c=returns/vol, marker='o')
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.show()

# Plot optimal portfolio
def plot_optimal_portfolio(opt, returns, portfolio_returns, vol):
    plt.figure(figsize=(10, 6))
    plt.grid(True)
    plt.scatter(vol, portfolio_returns, c=portfolio_returns/vol, marker='o')
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(portfolio_statistics(opt['x'], returns)[1], portfolio_statistics(opt['x'], returns)[0], 'g*', markersize=20.0)
    plt.show()



