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
from scipy.stats import ttest_ind
np.random.seed(0)
import data_cleaning as dc
import visualizations as vz

def get_sample(data, n):
    sample = []
    while len(sample) != n:
        x = np.random.choice(data)
        sample.append(x)
    
    return sample

def get_sample_mean(sample):
    return sum(sample) / len(sample)


def create_sample_distribution(data, dist_size=1000, n=1000):
    sample_dist = []
    while len(sample_dist) != dist_size:
        sample = get_sample(data, n)
        sample_mean = get_sample_mean(sample)
        sample_dist.append(sample_mean)
    
    return sample_dist

def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(alpha = 0.05, verbose=False):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    
    tracks_df = pd.read_csv('tracks_csv.csv')
    tracks2009=tracks_df[tracks_df['year']==2009]

    sample_2009 = create_sample_distribution(tracks2009['energy'], dist_size=100, n=40)
    sample_population = create_sample_distribution(tracks_df['energy'], dist_size=100, n=40)
    
    sample_2009_mean = np.mean(sample_2009)
    sample_pop_mean = np.mean(sample_population)
    if verbose:
        print('Means: ')
        print("2009 mean value:",sample_2009_mean)
        print("Population mean value:",sample_pop_mean)
    sample_2009_std = np.std(sample_2009)
    sample_pop_std = np.std(sample_population)

    if verbose:
        print('Standard Deviations')
        print("2009 std value:",sample_2009_std)
        print("pop std value:",sample_pop_std)
    ttest,pval = ttest_ind(sample_2009,sample_population)
    
    if verbose:
        print("p-value",pval)
    
    viz = vz.overlapping_density(sample_2009, sample_population)
    
    if pval < alpha:
        status = "we reject null hypothesis"
    else:
        status = "we accept null hypothesis"
        
    if verbose:
        print(status)
    
    return status, viz



def hypothesis_test_four():
    
    twenty_years = pd.read_csv('20 year songs.csv')
    twenty_years['year'] = twenty_years.release_date.str[0:4]
    tracks_1999 = twenty_years[twenty_years['year']=='1999']
    tracks_2018 = twenty_years[twenty_years['year']=='2018']
    
    dist1999  =  create_sample_distribution(tracks_1999['danceability'])
    dist2018_n1000 =  create_sample_distribution(tracks_2018['danceability'])
    
    x = pd.DataFrame(dist1999)
    x['year']=1999
    y= pd.DataFrame(dist2018_n1000)
    y['year']=2018
    
    
    
    dof = (x[0].var()/x[0].size + y[0].var()/y[0].size)**2 / ((x[0].var()/x[0].size)**2 / (x[0].size-1) +      (y[0].var()/y[0].size)**2 / (y[0].size-1))
   
    t, p = stats.ttest_ind(x[0], y[0], equal_var = False)
    print("\n",
        f"Welch's t-test= {t:.4f}", "\n",
        f"p-value = {p:.4f}", "\n",
        f"Welch-Satterthwaite Degrees of Freedom= {dof:.4f}")
    
    dist_concat = pd.concat([x, y])

    viz = vz.raincloud('year', 0, dist_concat)

    return viz

def seasons_stratifier(dataframe, sampleSize=1000):
    data = dataframe
    spring = data[data.seasons == 'spring'].sample(1000)
    summer = data[data.seasons == 'summer'].sample(1000)
    winter = data[data.seasons == 'winter'].sample(1000)
    fall = data[data.seasons == 'fall'].sample(1000)
    frames = [spring, summer, winter, fall]
    df = pd.concat(frames)
    return df

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

def anova_loop(frame, x, y, yearcol, yearlst, compact=False):
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
        data = frame[yearcol == year]
        testData = seasons_stratifier(data)
        test = anova(testData, x, y)
        test.index = ['ANOVA of {} against {} for {}'.format(y[0].title(),x.title(), year)]
        dfframe.append(test)
    df = pd.concat(dfframe)
    if compact:
        df = df[['F', 'PR(>F)', 'eta_sq']]
        df = df.style.set_properties(**{'background-color': 'white',
                           'color': 'black',
                           'border-color': 'white'})
        return df
    df = df.style.set_properties(**{'background-color': 'white',
                           'color': 'black',
                           'border-color': 'white'})
    
    return df
