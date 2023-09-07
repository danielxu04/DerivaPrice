# Monte Carlo Simulation Black Scholes

import numpy as np

class MonteCarloSimulation:
    def __init__(self, iterations, stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):
        self.iterations = iterations
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility

    # Monte-Carlo simulation for put option
    def simulate_put_option(self):
        # 1st column 0-filled, 2nd column payoff
        # Payoff function: max(0, E-S) for call option, where E = strike price, S = stock price
        data = np.zeros([self.iterations, 2])
        # 1D array w/ n items, where n = iterations
        random = np.random.normal(0, 1, [1, self.iterations])
        # S(t) price
        price = self.stock_price * np.exp(self.time_to_maturity * (self.risk_free_rate - 0.5 * self.volatility **2) + self.volatility * np.sqrt(self.time_to_maturity) * random)
        # E-S, E = strike price, S = stock price
        data[:,1] = self.strike_price - price
        # Average for Monte-Carlo, where amax(data, axis=1) returns max(0, E-S)
        avg = np.sum(np.amax(data, axis=1)) / float(self.iterations)
        # Use exp(-rT) discount factor, where r = risk-free rate, T = time to maturity
        return np.exp(-1 * self.risk_free_rate * self.time_to_maturity) * avg
    
    # Monte-Carlo simulation for call option
    def simulate_call_option(self):
        # 1st column 0-filled, 2nd column payoff
        # Payoff function: max(0, S-E) for call option, where S = stock price, E = strike price
        data = np.zeros([self.iterations, 2])
        # 1D array w/ n items, where n = iterations
        random = np.random.normal(0, 1, [1, self.iterations])
        # S(t) price
        price = self.stock_price * np.exp(self.time_to_maturity * (self.risk_free_rate - 0.5 * self.volatility ** 2) + self.volatility * np.sqrt(self.time_to_maturity) * random)
        # S-E, S = stock price, E = strike price
        data[:,1] = price - self.strike_price
        # Average for Monte-Carlo, where amax(data, axis=1) returns max(0, S-E)
        avg = np.sum(np.amax(data, axis=1)) / float(self.iterations)
        # Use exp(-rT) discount factor, where r = risk-free rate, T = time to maturity
        return np.exp(-1 * self.risk_free_rate * self.time_to_maturity) * avg
