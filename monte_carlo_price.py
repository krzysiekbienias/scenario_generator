import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
sys.path.append('../CalendarHandling')
from calendar_kb import CashflowsCalendar,ScenariosCalendar



class MonteCarloPrice(Calendar_kb):
    def __init__(self, today, maturity_date, day_convention, strike, risk_free_rate):
        Calendar_kb.__init__(self, today, maturity_date, day_convention)
        self.strike = strike
        self.risk_free_rate = risk_free_rate

    def monte_carlo_price_fun(self, option_type):
        realizations = object_brownian_motion.geometric_brownian_motion_scenario_fun()
        S_T = realizations[:, -1]
        if option_type == 'call':
            payoff = np.fmax(S_T - self.strike, 0)
        else:
            payoff = np.fmax(self.strike - S_T, 0)
        price = np.exp(self.year_fraction_two_dates_fun() * self.risk_free_rate) * np.average(payoff)
        return price
