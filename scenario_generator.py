import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
sys.path.append('../CalendarHandling')
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


class Brownian_Motion(Scenario_Generator):
    def __init__(self, today, maturity_date, day_convention, dt, runs, bm_x0, bm_drift, bm_volatility, gbm_s0,
                 gbm_drift, gbm_volatility):
        Scenario_Generator.__init__(self, today, maturity_date, day_convention, dt, runs)
        self.bm_x0 = bm_x0
        self.bm_drift = bm_drift
        self.bm_volatility = bm_volatility
        self.gbm_s0 = gbm_s0
        self.gbm_drift = gbm_drift
        self.gbm_volatility = gbm_volatility
        self.dt = dt
        self.runs = runs

    def geometric_brownian_motion_scenario_fun(self):
        len_of_scenario = self.get_path_len_fun()
        gbm_model = np.zeros((self.runs, len_of_scenario))  # create empty array
        gbm_model[:, 0] = self.gbm_s0  # current price
        for t in range(1, len(gbm_model[0])):
            z = np.random.standard_normal(self.runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self.gbm_drift - 0.5 * self.gbm_volatility ** 2) * self.dt +
                self.gbm_volatility * np.sqrt(self.dt) * z)
        return gbm_model

    def brownian_motion_scenario_fun(self, runs, graph):
        len_of_scenario = self.get_path_len_fun()
        bm_model = np.zeros((runs, len_of_scenario))  # create empty array
        bm_model[:, 0] = self.bm_x0  # current price
        for t in range(1, len(bm_model[0])):
            z = np.random.standard_normal(runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            bm_model[:, t] = bm_model[:, t - 1] + self.bm_drift * dt + self.bm_volatility * bm_model[:,
                                                                                            t - 1] * np.sqrt(dt) * z

    def plot_scenarios_fun(self, model, xlabel, ylabel):
        for k in range(10):
            plt.plot(model[k])
            plt.grid(True)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
        plt.show()

    def input_brownian_motion_fun(self):
        print('State at the beginning = ', self.bm_x0)
        print('Brownian motion drift = ', self.bm_drift)
        print('Brownian Motion volatility = ', self.bm_volatility)
        print('State at the beginning = ', self.bm_x0)
        print('time step in scenario = ', self.dt)
        print('Len of scenario in days = ', self.get_path_len_fun())
        print('Start date of scenario = ', self.get_spot_date())
        print('Maturity date of scenario = ', self.maturity_date)

    def input_geometric_brownian_motion_info_fun(self):
        print('State at the beginning = ', self.gbm_s0)
        print('Geometric Brownian motion drift = ', self.gbm_drift)
        print('Gemetric Brownian Motion volatility = ', self.gbm_volatility)
        print('time step in scenario = ', self.dt)
        print('Lenght of scenario in days = ', self.get_path_len_fun())


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



class Vasicek_Model(Scenario_Generator):
    def __init__(self, r0, theta, k, volatility, today, maturity_date, day_convention, dt, runs):
        Scenario_Generator.__init__(self, today, maturity_date, day_convention, dt, runs)
        self.r0 = r0
        self.theta = theta
        self.k = k
        self.volatility = volatility

    def vasicek_scenario_fun(self):
        len_of_scenario = self.get_path_len_fun()
        vas_model = np.zeros((self.runs, len_of_scenario))  # create empty array
        vas_model[:, 0] = self.r0  # current price
        for t in range(1, len(vas_model[0])):
            z = np.random.standard_normal(self.runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            vas_model[:, t] = vas_model[:, t - 1] + (
                        self.theta - self.k * vas_model[:, t - 1]) * self.dt + self.volatility * z
        return vas_model

    def plot_scenarios_fun(self, model, xlabel, ylabel):
        for k in range(10):
            plt.plot(model[k])
            plt.grid(True)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
        plt.show()


object_vasicek = Vasicek_Model(today=dt.date(2014, 9, 8),
                               maturity_date=dt.date(2014, 12, 18),
                               day_convention='Actual/365',
                               r0=0.03,
                               theta=0.05,
                               k=0.6,
                               volatility=0.02,
                               runs=10 ** 5,
                               dt=1 / 365)

object_mc_price = MonteCarloPrice(today=dt.date(2014, 9, 8),
                                  maturity_date=dt.date(2014, 12, 18),
                                  day_convention='Actual/365',
                                  strike=40,
                                  risk_free_rate=0.2)

if __name__ == '__main__':
    object_brownian_motion = Brownian_Motion(today=dt.date(2014, 9, 8),
                                         maturity_date=dt.date(2014, 12, 18),
                                         day_convention='Actual/365',
                                         dt=1 / 365,
                                         bm_x0=0,
                                         bm_drift=0.3,
                                         bm_volatility=0.1,
                                         gbm_s0=41,
                                         gbm_drift=0.2,
                                         gbm_volatility=0.25,
                                         runs=10 ** 5)

    gbm=object_brownian_motion.geometric_brownian_motion_scenario_fun()

    print("The END")
