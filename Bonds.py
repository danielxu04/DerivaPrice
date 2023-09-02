import matplotlib.pyplot as plt
from computations.YieldCurves import *
import datetime as dt

class Bond:
    def __init__(self, rates=[], times=[], face=None):
        self.coupon_rates = rates
        self.times = times.sort()
        self.face_value = face

    def construct_bond(self, rates, times):
        if len(rates) == 0:
            print('Warning: empty coupon rate')
            return
        if len(rates) != len(times):
            print('Warning: coupon rate and time mismatch')
            return
        
        self.coupon_rates = rates
        self.times = times

    # GETTER METHODS
    def get_coupons(self):
        return self.coupon_rates
    
    def get_times(self):
        return self.times
    
    def get_maturity(self):
        return self.times[-1]
    
    def get_face_value(self):
        if self.face_value == None:
            print('Warning: face value not available')
            return
        return self.face_value
    
    # SETTER METHODS
    def set_face_value(self, price: float):
        self.face_value = price

    def plot_bond_payments(self):
        fig, ax = plt.subplots()
        ax.bar(self.times, self.coupon_rates, width=0.1)
        ax.set_xlabel('Time')
        ax.set_ylabel('Coupon Rate')
        ax.set_title('Bond Payments')
        ax.set_xlim(0, self.times[-1])
        plt.show(block=False)

# Class for absolute bonds
class Absolute(Bond):
    def bond_pricer(self, surve, date=0):
        pass

# Class for relative bonds
class Relative(Bond):
    def bond_pricer(self, ycurve, time=0):
        present_value = 0
        for i in range(len(self.times)):
            if self.times[i] < time:
                continue
            present_value += ycurve.discount_factor(self.times[i] - time) * self.coupon_rates[i]
        return present_value
    
    def yield_to_maturity(self, price=None):
        if price == None:
            price = self.face_value

        if self.face_value == None:
            print('No price info')
        
        if self.length == 1:
            return -100 * math.log(price / self.coupon_rates[0]) / self.times[0]
        
        freq = round(1 / (self.times[1] - self.times[0]))
        tolerance = 0.000001

        def f(y):
            sigma = self.coupon_rates[0] / (1 + y / freq) ** (freq * self.times[0])
            for i in range(1, self.length):
                sigma += self.coupon_rates[i] / (1 + y / freq) ** (freq * self.times[i])
            return sigma - price
        
        def f_prime(y):
            sigma = self.times[0] * self.coupon_rates[0] / (1 + y / freq) ** (freq * self.times[0] + 1)
            for i in range(1, self.length):
                sigma += self.times[i] * self.coupon_rates[i] / (1 + y / freq) ** (freq * self.times[i] + 1)
            return -sigma
        
        prev_y = 0
        curr_y = prev_y - f(prev_y) / f_prime(prev_y)

        while abs(curr_y - prev_y) > tolerance:
            prev_y = curr_y
            curr_y = prev_y - f(prev_y) / f_prime(prev_y)
        

def construct_bond(dates: list, coupon_rates: list):
    if len(dates) != len(coupon_rates):
        print('Warning: dates and rates mismatch')
        return

    if all([(type(date) == float) for date in dates]):
        bond = Relative(rates=coupon_rates, times=dates)
        return bond
    
    if all([(type(date) == dt.date) for date in dates]):
        pass

    print('Warning: date type not supported')
    return

def construct_coupon_bond(maturity: float, face_value: float, rate: float, freq: int):
    if freq < 0:
        print('Warning: negative frequency')
        return
    
    if freq == 0:
        payment = [float(face_value)]
        paydate = [float(maturity)]
        bond = construct_bond(paydate, payment)
        return bond
    
    
    payments = []
    paydates = []
    period = 1/freq
    date = float(maturity)
    while date > 0:
        paydates.append(date)
        date -= period

    paydates.sort()

    coupon = (rate / 100) * face_value / freq

    for c in range(len(paydates)):
        payments.append(coupon)

    payments[-1] += face_value
    bond = construct_bond(paydates, payments)
    
    return bond

    

    

    

    
