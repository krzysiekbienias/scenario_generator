import numpy as np
import pandas as pd
import bdateutil as bd
import datetime as dt
import calendar
from pandas.tseries.offsets import *
import matplotlib.pyplot as plt

import sys
sys.path.append('../CalendarHandling')
from calendar_kb import ScenariosCalendar

o_scenario_calendar = ScenariosCalendar(today='2018-08-20', day_convention='Actual/365',
                                        maturity_date='2018-11-20',lag=0)

class Scenario_Generator(ScenariosCalendar):
    def __init__(self, today, day_convention,runs,lag, maturity_date=None):
        ScenariosCalendar.__init__(self, today, day_convention,lag,maturity_date)
        self._runs = runs

    def plot_scenarios(self, scenarios, x_label, y_label):
        df_scenarios=pd.DataFrame(scenarios,index=o_scenario_calendar.get_date_series())


        for k in range(10):
            plt.plot(df_scenarios[k])
        plt.grid(True)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()


if __name__ == '__main__':
    o_scenario_calendar = ScenariosCalendar(today='2018-08-20', day_convention='Actual/365',
                                                maturity_date='2018-11-20',lag=0)

    o_scenario_generator=Scenario_Generator(today='2018-08-20', day_convention='Actual/365',
                                                maturity_date='2018-11-20',runs=10**4,lag=0)

    u=o_scenario_calendar.get_date_series()

    print("The END")
