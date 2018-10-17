import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
sys.path.append('../CalendarHandling')
from calendar_kb import ScenariosCalendar

from gen_fun import Scenario_Generator

o_scenario_calendar = ScenariosCalendar(today='2018-08-20', day_convention='Actual/365', maturity_date='2018-11-20',lag=0)

o_scenario_generator=Scenario_Generator(today='2018-08-20', day_convention='Actual/365',
                                                maturity_date='2018-11-20',runs=10**4,lag=0)

class Brownian_Motion(Scenario_Generator):
    def __init__(self, today, maturity_date, day_convention,lag, runs, gbm_s0,
                 gbm_drift, gbm_volatility,bm_x0=None,bm_drift=None,bm_volatility=None):
        Scenario_Generator.__init__(self, today, day_convention,lag, runs, maturity_date)
        ScenariosCalendar.__init__(self, today, day_convention,lag, maturity_date)
        self._bm_x0 = bm_x0
        self._bm_drift = bm_drift
        self._bm_volatility = bm_volatility
        self._gbm_s0 = gbm_s0
        self._gbm_drift = gbm_drift
        self._gbm_volatility = gbm_volatility
        self._runs = runs

    def geometric_brownian_motion_scenario_fun(self):
        dt = self.get_increments()
        gbm_model = np.zeros((self._runs, len(o_scenario_calendar.get_date_series())))  # create empty array
        gbm_model[:, 0] = self._gbm_s0  # current price
        for t in range(1, len(gbm_model[0])):
            z = np.random.standard_normal(self._runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self._gbm_drift - 0.5 * self._gbm_volatility ** 2) * dt[t-1] +
                self._gbm_volatility * np.sqrt(dt[t-1]) * z)
        return np.transpose(gbm_model)

    def brownian_motion_scenario_fun(self):
        dt = self.get_increments()
        bm_model = np.zeros((self._runs, len(o_scenario_calendar.get_date_series())))  # create empty array
        bm_model[:, 0] = self._bm_x0  # current price
        for t in range(1, len(bm_model[0])):
            z = np.random.standard_normal(self._runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            bm_model[:, t] = bm_model[:, t - 1] + self._bm_drift * dt[t] + self._bm_volatility * bm_model[:,
                                                                                            t - 1] * np.sqrt(dt) * z


    def input_brownian_motion_fun(self):
        print('State at the beginning = ', self._bm_x0)
        print('Brownian motion drift = ', self._bm_drift)
        print('Brownian Motion volatility = ', self._bm_volatility)
        print('State at the beginning = ', self._bm_x0)
        print('time step in scenario = ', self._dt)

    def input_geometric_brownian_motion_info_fun(self):
        print('State at the beginning = ', self._gbm_s0)
        print('Geometric Brownian motion drift = ', self._gbm_drift)
        print('Gemetric Brownian Motion volatility = ', self._gbm_volatility)


o_gbm_scenarios=Brownian_Motion(today='2018-08-20',
                                maturity_date='2018-11-20',
                                day_convention='Actual/365',
                                gbm_drift=0.03,
                                gbm_s0=90,
                                gbm_volatility=0.35,
                                runs=10**4,
                                lag=0
                                )
u=o_scenario_calendar.get_date_series()
ar_gbm=o_gbm_scenarios.geometric_brownian_motion_scenario_fun()
o_gbm_scenarios.plot_scenarios(scenarios=ar_gbm,x_label='x',y_label='y')

print('END')