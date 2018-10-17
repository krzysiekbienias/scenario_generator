import numpy as np
import pandas as pd
import bdateutil as bd
import datetime as dt
import calendar
from pandas.tseries.offsets import *
import sys

sys.path.append('../CalendarHandling')
from calendar_kb import ScenariosCalendar

from gen_fun import Scenario_Generator

o_scenario_calendar = ScenariosCalendar(today='2018-08-20', day_convention='Actual/365', maturity_date='2018-11-20')

o_scenario_generator=Scenario_Generator(today='2018-08-20', day_convention='Actual/365',
                                                maturity_date='2018-11-20',runs=10**4)


class Vasicek_Model(Scenario_Generator,ScenariosCalendar):
    def __init__(self, today, day_convention,r0, theta, k, volatility, runs,maturity_date=None):
        Scenario_Generator.__init__(self, today, day_convention, runs, maturity_date)
        ScenariosCalendar.__init__ (self, today, day_convention,maturity_date)
        self.r0 = r0
        self.theta = theta
        self.k = k
        self.volatility = volatility

    def vasicek_scenario_fun(self):
        dt=self.get_increments()
        vas_model = np.zeros((o_scenario_generator._runs, len(dt)))  # create empty array
        vas_model[:, 0] = self.r0  # current price
        for t in range(1, len(vas_model[0])):
            z = np.random.standard_normal(o_scenario_generator._runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            vas_model[:, t] = vas_model[:, t - 1] + (
                        self.theta - self.k * vas_model[:, t - 1]) * dt[t] + self.volatility * z
        return vas_model


if __name__ == '__main__':




    o_vasicek = Vasicek_Model(today='2018-08-20',
                               maturity_date='2018-11-20',
                               day_convention='Actual/365',
                               r0=0.03,
                               theta=0.05,
                               k=0.04,
                               volatility=0.01,
                              runs=10**4
                               )

    ar__vasicek_scenarios=o_vasicek.vasicek_scenario_fun()




    print("THE END")
