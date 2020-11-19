#Problem 5, alternative solution without using numpy.financial
#Run in Jupyter

import numpy as np
import plotly.express as px
import pandas as pd
import scipy.stats as ss
import scipy.optimize as opt

#--------------------------------------------------------------------------------------------------------------------------------------

#Problem 5A

def fun_pw(inv, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6, salvage, tax_rate, marr, life):
    btcf = np.array([0, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6 + salvage])   # (A) Before-TAX CashFlow
    dep = np.array([0, (-inv)/3, (-inv)/3, (-inv)/3, 0, 0, 0])     # (B) straight line depreciation over 3 years
    nibt = btcf - dep        # (C) = (A) - (B) Taxable income / Net Income Before Tax
    tax_cf = -tax_rate * nibt    # (D) = -t * (C)
    atcf = btcf + tax_cf       # (E) = (A) + (D) After TAX CashFlow
    years = np.arange(life + 1)                                                                                          
    disc_factor = 1/((1+marr)**years)  #discount factors
    pw_project = inv + sum(atcf * disc_factor)  #PW
    return pw_project

#--------------------------------------------------------------------------------------------------------------------------------------

tax_rate = 0.17
marr = 0.1
inv = -100000
revenue_1 = 25000
revenue_2 = 25000
revenue_3 = 25000
revenue_4 = 25000
revenue_5 = 25000
revenue_6 = 25000
salvage = 10000
life = 6
base = fun_pw(inv, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6 , salvage, tax_rate, marr, life)

print('The PW of the base case is ${:,.2f}'.format(base), '.')

#--------------------------------------------------------------------------------------------------------------------------------------

n_samples = 1000
salvage_rnd = ss.uniform.rvs(loc=5000,scale=(15000-5000),size=n_samples) 
revenue_1_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)
revenue_2_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)
revenue_3_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)
revenue_4_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)
revenue_5_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)
revenue_6_rnd = ss.norm.rvs(loc=25000,scale=7500,size=n_samples)

#--------------------------------------------------------------------------------------------------------------------------------------

pw_rnd = fun_pw(inv, revenue_1_rnd, revenue_2_rnd, revenue_3_rnd, revenue_4_rnd, revenue_5_rnd, revenue_6_rnd, salvage_rnd, tax_rate, marr, life)

df_trials = pd.DataFrame(data={'Revenue year 1':revenue_1_rnd, 'Revenue year 2':revenue_2_rnd, 'Revenue year 3':revenue_3_rnd, 'Revenue year 4':revenue_4_rnd, 'Revenue year 5':revenue_5_rnd, 'Revenue year 6':revenue_6_rnd, 'Salvage Value':salvage_rnd, 'PW':pw_rnd})
df_trials

#--------------------------------------------------------------------------------------------------------------------------------------

pw_mean = np.mean(pw_rnd)
pw_sd = np.std(pw_rnd)
print('The after-tax mean of the PW is ${:,.2f}'.format(pw_mean), '.')
print('The after-tax sd of the PW is ${:,.2f}'.format(pw_sd), '.')

#--------------------------------------------------------------------------------------------------------------------------------------

#Problem 5B
pw_target = 0
squared_error = lambda marr: (fun_pw(inv, revenue_1, revenue_2, revenue_3, revenue_4, revenue_5, revenue_6, salvage, tax_rate, marr, life)-pw_target)**2
irr = opt.minimize(fun=squared_error, x0=0.5, method='L-BFGS-B', bounds=((0, 1),))
print('The IRR of the base case is {:.2%}'.format(irr.x[0]), '.')
#URL: https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html

#--------------------------------------------------------------------------------------------------------------------------------------

def fun_irr_rnd(row):
    pw_target = 0
    squared_error_rnd = lambda marr: (fun_pw(inv, row['Revenue year 1'], row['Revenue year 2'], row['Revenue year 3'], row['Revenue year 4'], row['Revenue year 5'], row['Revenue year 6'], row['Salvage Value'], tax_rate, marr, life)-pw_target)**2
    irr_rnd = opt.minimize(fun=squared_error_rnd, x0=0.5, method='L-BFGS-B', bounds=((0, 1),))
    return irr_rnd.x[0]

df_irr_rnd = df_trials.apply(fun_irr_rnd, axis=1)   #DataFrame
df_irr_rnd

#--------------------------------------------------------------------------------------------------------------------------------------

irr_mean = np.mean(df_irr_rnd)
irr_sd = np.std(df_irr_rnd)
print('The after-tax mean of the IRR is {:.2%}'.format(irr_mean), '.')
print('The after-tax sd of the IRR is {:.2%}'.format(irr_sd), '.')

#--------------------------------------------------------------------------------------------------------------------------------------

#Problem 5C
pw_rnd_sort = np.sort(pw_rnd)
df_sort = pd.DataFrame(data={'PW of Project A':pw_rnd_sort,  'Cumulated probability':(np.arange(n_samples)+1)/n_samples})

fig_cum = px.line(df_sort, x='PW of Project A', y='Cumulated probability')
fig_cum.show()

#--------------------------------------------------------------------------------------------------------------------------------------

#Problem 5D
pw_negative_prct = len([num for num in pw_rnd if num < 0])/n_samples
print('The probability of losing money on the investment is {:.2%}'.format(pw_negative_prct), '.')

#--------------------------------------------------------------------------------------------------------------------------------------

#Problem 5E
pw_o_20000 = len([num for num in pw_rnd if num >= 20000])/n_samples
print('The probability of an after-tax PW > $20,000 is {:.2%}'.format(pw_o_20000), '.')













