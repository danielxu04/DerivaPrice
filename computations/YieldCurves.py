import math
import matplotlib.pyplot as plt
import numpy as np
from Interpolation import *

def newton_solver(interpolator, bond):
    TOLERANCE = 0.000001
    coupons = bond.get_coupons()
    times = bond.get_times()
    maturity = bond.get_maturity()
    face_value = bond.get_face_value()

    def f(x):
        temp = interpolator.copy()
        temp.extend(maturity, x)
        sigma = -face_value
        for i in range(len(times)):
            sigma += math.exp(-temp.eval(times[i]) * times[i]) * coupons[i]
        return sigma
    
    def f_prime(x):
        temp = interpolator.copy()
        temp.extend(maturity, x)
        max_index = len(temp) - 1
        sigma = 0
        for i in range(len(times)):
            sigma += temp.delta(times[i], max_index) * times[i] * math.exp(-temp.eval(times[i]) * times[i]) * coupons[i]
        return -sigma
    
    prev_x = 0
    curr_x = prev_x - f(prev_x) / f_prime(prev_x)
    while abs(curr_x - prev_x) > TOLERANCE:
        prev_x = curr_x
        curr_x = prev_x - f(prev_x) / f_prime(prev_x)

    return curr_x


# Yield Curves
class YCurve:
    def __init__(self):
        self.tenors = []
        self.rates = []
        self.length = 0
        self.interpolator = None

    def rates_constructor(self, tenors, rates, interpolator=None):
        if self.length > 0:
            print('Warning: curve already constructed')
            return
        if len(tenors) != len(rates):
            print('Warning: tenors and rates mismatch')
            return
        self.tenors = tenors.copy()
        self.rates = rates.copy()
        self.length = len(tenors)

        if interpolator == 'pwl':
            self.interpolator = PWL(self.tenors, self.rates)
        elif interpolator == 'catmull-rom':
            self.interpolator = CATMULL_ROM(self.tenors, self.rates)
        elif interpolator == 'natural-spline':
            self.interpolator = NATURAL_SPLINE(self.tenors, self.rates)
        else:
            print('Warning: invalid interpolator, using PWL')
            self.interpolator = PWL(self.tenors, self.rates)

# For Bonds, only pwl interpolator is available
    def bonds_constructor(self, bonds):
        self.interpolator = PWL()

        if self.length > 0:
            print('Warning: curve already constructed')
            return
        
        def get_maturity(bond):
            return bond.get_maturity()
        bonds.sort(key=get_maturity)

        for i in range(len(bonds)):
            self.interpolator.extend(bonds[i].get_maturity(), newton_solver(self.interpolator, bonds[i]))
            self.tenors.append(bonds[i].get_maturity())
            self.rates.append(newton_solver(self.interpolator, bonds[i]))
            self.length += 1

    def copy(self):
        new = YCurve()
        new.rates_constructor(tenors=self.tenors, rates=self.rates, interpolator=self.interpolator.copy())
        return new
    
    def get_rates(self):
        return self.rates.copy()
    
    def get_tenors(self):
        return self.tenors
    
    # Returns continuously compounded spot rate for a given tenor
    def get_yield(self, tenor):
        return self.interpolator.eval(tenor)
    
    def discount_factor(self, tenor):
        return math.exp(-self.interpolator.eval(tenor) * tenor)
    
    def spot_rate(self, time, compounding=0):
        # Simple
        if compounding == 0:
            return 100 * (1 / self.discount_factor(time) - 1) / time
        elif compounding > 0:
            return 100 * (self.discount_factor(time) ** (-1 / compounding / time) - 1) * compounding
        else:
            print('Warning: invalid compounding')
            return
        
    # PLOTTING
    def plot_yield_curve(self, max_tenor=0):
        if max_tenor <= 0:
            max_tenor = max(self.tenors)

        fig, ax = plt.subplots()
        tenor = np.arrange(0, max_tenor, 0.1)
        yield_curve = []

        for t in tenor:
            y = self.get_yield(t)
            yield_curve.append(y)

        yield_curve = np.array(yield_curve)
        
        ax.plot(tenor, yield_curve)
        ax.set(xlabel='Tenor', ylabel='Yield', title='Yield Curve')
        plt.show(block=False)

    def plot_discount_curve(self, max_tenor=0):
        if max_tenor <= 0:
            max_tenor = max(self.tenors)

        fig, ax = plt.subplots()
        tenor = np.arrange(0, max_tenor, 0.1)
        discount_curve = []

        for t in tenor:
            d = self.discount_factor(t)
            discount_curve.append(d)

        discount_curve = np.array(discount_curve)
        
        ax.plot(tenor, discount_curve)
        ax.set(xlabel='Tenor', ylabel='Discount Factor', title='Discount Curve')
        plt.show(block=False)

    def shift_rates(self, delta: float):
        delta /= 100
        shifted = []
        for i in range(self.length):
            shifted.append(self.rates[i] + delta)
        curve = YCurve()
        curve.rates_constructor(rates=shifted, tenors=self.tenors, interpolator=self.interpolator.copy())
        return curve
    
    def shift_rate(self, delta: float, index: int):
        delta /= 100
        shifted = self.rates.copy()
        shifted[index] += delta
        curve = YCurve()
        curve.rates_constructor(rates=shifted, tenors=self.tenors, interpolator=self.interpolator.copy())
        return curve
    