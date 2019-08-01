import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql

sys.path.append('../CalendarAlgorithm')
from calendar_ql_supported import SetUpSchedule


class EquityModels(SetUpSchedule):

    def __init__(self, valuation_date, termination_date, calendar, convention, schedule_freq, business_convention,
                 termination_business_convention,
                 date_generation, end_of_month, type_option, current_price, strike, ann_risk_free_rate,
                 ann_volatility, ann_dividend, runs):
        SetUpSchedule.__init__(self, valuation_date, termination_date, calendar, business_convention,
                               termination_business_convention,
                               date_generation, end_of_month, convention, schedule_freq)
        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._drift = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend
        self._runs = runs
        self.m_ar_equity_price = self.geometric_brownian_motion_scenario_fun()
        self.mlt_payoffandST = self.calculate_payoffs()  # lt list of tuples ST and tuples and payoff sorted
        self.mf_monte_carlo_price = self.monte_carlo_price()

    def geometric_brownian_motion_scenario_fun(self):
        dt = self.ml_yf
        gbm_model = np.zeros((self._runs, len(
            self.ml_yf)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        gbm_model[:, 0] = self._S0  # current price
        for t in range(1, len(gbm_model[0])):
            z = np.random.standard_normal(self._runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self._drift - 0.5 * self._sigma ** 2) * dt[t - 1] +
                self._sigma * np.sqrt(dt[t - 1]) * z)
        return np.transpose(gbm_model)

    def calculate_payoffs(self):  # delivery_data random or given
        ST = self.m_ar_equity_price[-1]

        vpayoff = np.zeros(len(ST))
        for i in range(len(ST)):#
            if (self._type_option == 'call'):
                vpayoff[i] = max(ST[i] - self._K, 0)
            else:
                vpayoff[i] = max(self._K - ST[i], 0)
        zipped = list((zip(ST, vpayoff)))
        sorted_zip = sorted(zipped, key=lambda x: x[0])  # without sorting there is a problem with ploting
        return sorted_zip

    def monte_carlo_price(self):
        take_payoff = lambda x: x[1] #get second coordinates from tuple
        payoff = list(map(take_payoff, self.mlt_payoffandST))
        return np.mean(payoff)*np.exp(-self._drift*self.mf_yf_between_valu_date_and_maturity)


if __name__ == '__main__':
    o_black_scholes_test = EquityModels(valuation_date='2019-06-20',
                                        termination_date='2019-08-20',
                                        schedule_freq='Daily',
                                        convention='ActualActual',  # Daily,Monthly,Quarterly
                                        calendar=ql.Poland(),
                                        business_convention=ql.Following,
                                        # TODO Find out what does it mean. It is int =0
                                        termination_business_convention=ql.Following,
                                        date_generation=ql.DateGeneration.Forward,
                                        end_of_month=False,
                                        ##################################
                                        type_option='call',
                                        current_price=90,
                                        strike=91,
                                        ann_risk_free_rate=0.03,
                                        ann_volatility=0.25,
                                        ann_dividend=0,
                                        runs=100)
    print('The end')
