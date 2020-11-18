#Problem 5, alternative solution without using numpy.financial

import numpy as np
import plotly.express as px
import pandas as pd
import scipy.stats as ss
import scipy.optimize as opt

#Problem 5A

def fun_pw(inv, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6, salvage, tax_rate, marr, life):
    btcf = np.array([0, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6 + salvage])   # (A) Before-TAX CashFlow
    dep = np.array([0, (-inv-salvage)/3, (-inv-salvage)/3, (-inv-salvage)/3, 0, 0, 0])     # (B) straight line depreciation over 3 years
    nibt = btcf - dep        # (C) = (A) - (B) Taxable income / Net Income Before Tax
    tax_cf = -tax_rate * nibt    # (D) = -t * (C)
    atcf = btcf + tax_cf       # (E) = (A) + (D) After TAX CashFlow
    years = np.arange(life + 1)                                                                                          
    disc_factors = 1/((1+marr)**years)  #discount factors
    pw_project = inv + sum(atcf * disc_factor)  #PW
    return pw_project


tax_rate = 0.17
marr = 0.10 
inv = -100000
revenue_1 = 25000
revenue_2 = 25000
revenue_3 = 25000
revenue_4 = 25000
revenue_5 = 25000
revenue_6 = 25000
salvage = 10000
life = 6
base = fun_pw(inv, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6, salvage, tax_rate, marr, life)
print('The PW of the base case is ${:,.2f}'.format(base))


n_samples = 1000
salvage_rnd = ss.uniform.rvs(loc = 5000, scale = (15000 - 5000), size = n_samples)
revenue_1_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)
revenue_2_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)
revenue_3_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)
revenue_4_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)
revenue_5_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)
revenue_6_rnd = ss.norm.rvs(loc = 25000, scale = 7500, size = n_samples)

pw_rnd = fun_pw(inv, revenue_1_rnd, revenue_2_rnd, revenue_3_rnd, revenue_4_rnd, revenue_5_rnd, revenue_6_rnd, salvage_rnd, tax_rate, marr, life)
df_trials = pd.DataFrame(data = {'Revenue year 1':revenue_1_rnd, 'Revenue year 2':revenue_2_rnd, 'Revenue year 3':revenue_3_rnd, 'Revenue year 4':revenue_4_rnd, 'Revenue year 5':revenue_5_rnd, 'Revenue year 6':revenue_6_rnd, 'Salvage value':salvage_rnd, 'PW':pw_rnd})
df_trials

pw_mean = np.mean(pw_rnd)
pw_sd = np.std(pw_rnd)
print('The after-TAX mean of the PW is ${:,.2f}'.format(pw_mean))
print('The after-TAX standard deviation of the PW is ${:,.2f}'.format(pw_sd))



#Problem 5B













