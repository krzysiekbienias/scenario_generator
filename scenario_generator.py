import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys

sys.path.append('../BlackScholesModel')
from calendar_kb import Calendar_kb


class Scenario_Generator(Calendar_kb):
    def __init__(self, today, maturity_date, day_convention, dt, runs):
        Calendar_kb.__init__(self, today, maturity_date, day_convention)
        self.dt = dt
        self.runs = runs

    def get_year_fraction_fun(self):
        return self.year_fraction_two_dates_fun()

    def get_spot_date(self):
        return self.year_fraction_fun(shift=0, period='days')

    def get_path_len_fun(self):
        return self.days_difference_fun()
