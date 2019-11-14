"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
import math
import statsmodels.api as sm
from statsmodels.formula.api import ols
np.random.seed(0)

def create_sample_dists(cleaned_data, y_var=None, categories=[]):
    """
    Each hypothesis test will require you to create a sample distribution from your data
    Best make a repeatable function

    :param cleaned_data:
    :param y_var: The numeric variable you are comparing
    :param categories: the categories whose means you are comparing
    :return: a list of sample distributions to be used in subsequent t-tests

    """
    htest_dfs = []

    # Main chunk of code using t-tests or z-tests
    return htest_dfs

def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(alpha = None, cleaned_data=None):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    # Get data for tests
    comparison_groups = create_sample_dists(cleaned_data=None, y_var=None, categories=[])

    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###

    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        # calculations for effect size, power, etc here as well

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between NONE')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_two():
    pass

def hypothesis_test_three():
    pass

def hypothesis_test_four():
    pass



def anova_table(aov):
    ''' Takes as input the OLS Anova table and calucalte the eta queared and omega squared values and appends them to the table
    '''
    
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])
    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov

def anova(frame, x, y, year = None):
    ''' Carries out the Anova test using the stats model OLS method on one or more columns of interest
        
        required parameters:
        frame: dataframe containing the data with columns of interest
        x : column name of the dependent variable as a string
        y : column name of the independent variable in a list
    '''
    
    if len(y) > 1:
        dFrames = []
        for i in y:
            formula = '{} ~ C({})'.format(i,x)
            lm = ols(formula, frame).fit()
            table = sm.stats.anova_lm(lm, typ=2)
            allVal = anova_table(table)
            result = allVal.iloc[:1,:]
            result.index = ['ANOVA of {} against {}'.format(i.title(),x.title())]
            dFrames.append(result)
        df = pd.concat(dFrames)
        return df
    else:
        formula = '{} ~ C({})'.format(y[0],x)
        lm = ols(formula, frame).fit()
        table = sm.stats.anova_lm(lm, typ=2)
        allVal = anova_table(table)
        result = allVal.iloc[:1,:]
        result.index = ['ANOVA of {} against {}'.format(y[0].title(),x.title())]
        return result
    
def anova_loop(frame, x, y, yearcol, yearlst):
    ''' Carries out the Anova test using the stats model OLS method containing just one IV and DV
        required a list of years for which the test has to be carried out.
        
        Parameters:
        frame: dataframe containing the column with data of interest
        x : column name of the dependent variable as a string eg. 'colname'
        y : one column name of the independent variable in a list eg. ['colname']
        yearcol: column of the dataframe containg years as values
        yearlst: list of years for which the test has to be carried out.
        
    '''
    
    dfframe = []
    for year in yearlst:
        data = frame[frame['year']== year].sample(500)
        test = anova(data, x, y)
        test.index = ['ANOVA of {} against {} for {}'.format(y[0].title(),x.title(), year)]
        dfframe.append(test)
    df = pd.concat(dfframe)
    df = df.style.set_properties(**{'background-color': 'white',
                           'color': 'black',
                           'border-color': 'white'})
    return df
