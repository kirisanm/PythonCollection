#Problem 5

import numpy as np
import numpy_financial as npf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import scipy.stats as ss

Nsim = 10000 #Number of samples 
initial_cost = -100000 #$ Water separator
useful_life = 6 #useful life of 6 years
cf_in = np.random.normal(25000, 7500, Nsim) #Draw random samples from a normal distribution
salvage_value = np.random.uniform(5000, 15000, Nsim) #Draw random samples from an uniform distribution
depreciation_sl_3years = (-initial_cost)/3 #Straigt-line depreciation to 0
#depreciation_sl_3years = (-initial_cost-salvage_value)/3. We tax the difference between BV and MV
MARR = 0.10 #After-TAX MARR (10%)
tax_rate = 0.17 #Corporate tax rate (17%)



#Problem 5A:

#BTCF (Before-Tax Cashflow)
BTCF0 = initial_cost
BTCF1 = cf_in
BTCF2 = cf_in
BTCF3 = cf_in
BTCF4 = cf_in
BTCF5 = cf_in
BTCF6 = cf_in + salvage_value 
#The salvage value is added in the BTCF as we depreciate the asset to $0 
#and need to tax for the difference between the MV and the BV.

#Depreciation (d)
d1 = depreciation_sl_3years
d2 = depreciation_sl_3years
d3 = depreciation_sl_3years

#TI || NIBT (Taxable Income or Net Income Before-Tax)
TI1 = BTCF1 - d1
TI2 = BTCF2 - d2
TI3 = BTCF3 - d3
TI4 = BTCF4
TI5 = BTCF5
TI6 = BTCF6

#TAX (Income Tax Cashflow)
T1 = -tax_rate*TI1
T2 = -tax_rate*TI2
T3 = -tax_rate*TI3
T4 = -tax_rate*TI4
T5 = -tax_rate*TI5
T6 = -tax_rate*TI6

#ATCF (After-Tax CashFlow)
ATCF0 = BTCF0
ATCF1 = BTCF1 + T1
ATCF2 = BTCF2 + T2
ATCF3 = BTCF3 + T3
ATCF4 = BTCF4 + T4
ATCF5 = BTCF5 + T5
ATCF6 = BTCF6 + T6

#Present Worth at ATCF
PW0 = ATCF0 / (1+MARR)**0
PW1 = ATCF1 / (1+MARR)**1
PW2 = ATCF2 / (1+MARR)**2
PW3 = ATCF3 / (1+MARR)**3
PW4 = ATCF4 / (1+MARR)**4
PW5 = ATCF5 / (1+MARR)**5
PW6 = ATCF6 / (1+MARR)**6 

#Sum of PW at ATCF
PW_tot = PW0 + PW1 + PW2 + PW3 + PW4 + PW5 + PW6 

#The after-tax mean
mean_PW = sum(PW_tot)/len(PW_tot)
print("The after-tax mean of the PW will be: ", mean_PW)

#The after-tax standard deviation
sd_PW = np.std(PW_tot)
print("The after-tax standard deviation of the PW will be: ", sd_PW)




#Problem 5B

#Array length of the ATCFs
array_length = ATCF6.shape[0]
#Empty array to input the calculated IRRs from the for-loop
irr_array = np.zeros(ATCF6.shape)

#Each iteration of the loop calculates the IRR of the ATCFs for each index by using numpy-financial.irr 
for idx in range(array_length):
    ATCF0_indexed = ATCF0
    ATCF1_indexed = ATCF1[idx]
    ATCF2_indexed = ATCF2[idx]
    ATCF3_indexed = ATCF3[idx]
    ATCF4_indexed = ATCF4[idx]
    ATCF5_indexed = ATCF5[idx]
    ATCF6_indexed = ATCF6[idx]
    
    irr = npf.irr([ATCF0_indexed, ATCF1_indexed, ATCF2_indexed, ATCF3_indexed, ATCF4_indexed, ATCF5_indexed, ATCF6_indexed])
    irr_array[idx] = irr 

#Calculate the after-tax mean of the IRR by using numpy.nansum which sets non-numbers to 0.    
mean_irr = np.nansum(irr_array)/len(irr_array)
print("The after-tax mean of the IRR will be: ", mean_irr)

#Calculate the after-tax SD of the IRR by using numpy.nanstd which sets non-numbers to 0.
sd_irr = np.nanstd(irr_array)
print("The after-tax standard deviation of the IRR will be: ", sd_irr)




#Problem 5C

#Cumulative Histogram: The ATCF PW (after-tax CashFlow present worth calculation)
hist_PW = px.histogram(x=PW_tot, cumulative=True, nbins = 10000, histnorm='probability')
hist_PW.update_layout(xaxis_title="Present Worth", yaxis_title="Probability", title={'text':"Cumulative Histogram of Present Worth (k $)",'x':0.5,'y':0.95})
hist_PW.show()

#Histogram: Normal distribution of the ATCF PWs (after-tax CashFlow present worths)
hist_PW2 = px.histogram(x=PW_tot, cumulative=False, nbins = 10000, histnorm='probability')
hist_PW2.update_layout(xaxis_title="Present Worth", yaxis_title="Probability", title={'text':"Histogram of Present Worth (k $)",'x':0.5,'y':0.95})
hist_PW2.show()



#Problem 5D

pw_negative_prct = len([num for num in PW_tot if num < 0])/Nsim
print('The probability of losing money on the investment is {:.2%}'.format(pw_negative_prct), '.')



#Problem 5E

pw_o_20000 = len([num for num in PW_tot if num >= 20000])/Nsim
print('The probability of an after-tax PW > $20,000 is {:.2%}'.format(pw_o_20000), '.')