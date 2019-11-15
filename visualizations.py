"""
This module is for your final visualization code.
One visualization per hypothesis question is required.
A framework for each type of visualization is provided.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt

# Set specific parameters for the visualizations
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def overlapping_density(sample1, sample2):
    """
    Set the characteristics of your overlapping density plot
    All arguments are set to None purely as a filler right now

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    Should be able to call this function in later visualization code.

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """

    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    # Starter code for figuring out which package to use
    sns.distplot(sample1, label = "2009" )
    sns.distplot(sample2, label = 'Population')
    plt.title('Energy of a sample of top 100 songs of 2009 in comparison to a sample of the population ')
    plt.xlabel('Energy')

    return fig



def raincloud(par1, par2, df):
    """
    Same specifications and requirements as overlapping density plot

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """
    dx = par1; dy = par2; ort = "h"; pal = "Set2"; sigma = .2
    fig, ax = plt.subplots(figsize=(16, 10))

    pt.RainCloud(x = dx, y = dy, data = df, palette = pal, bw = sigma,
                 width_viol = .6, ax = ax, orient = ort, move = 0)
    plt.xlabel('Danceability')
    plt.title('20 year Comparison of Songs Danceability')
    
    return fig


def visualization_one(target_var = None, input_vars= None, output_image_name=None):
    """
    The visualization functions are what is used to create each individual image.
    The function should be repeatable if not generalizable
    The function will call either the boxplot or density plot functions you wrote above

    :param target_var:
    :param input_vars:
    :param output_image_name: the desired name for the image saved
    :return: outputs a saved png file and returns a fig object for testing
    """
    ###
    # Main chunk of code here
    ###

    # Starter code for labeling the image
    plt.xlabel(None, figure = fig)
    plt.ylabel(None, figure = fig)
    plt.title(None, figure= fig)
    plt.legend()

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)
    return fig


# please fully flesh out this function to meet same specifications of visualization one

def box_subplots(row, col, data, xseries , columns, yticks=[]):
    sns.set(style="white", palette="muted", color_codes=True)
    sns.set_context("paper", font_scale=2.0)
    f, axes = plt.subplots(row,col, figsize=(25, 20))
    sns.despine(left=True)
    i = 0
    for col in range(0,3):
        for row in range(0,4):
            name = columns[i]
            sns.boxplot(x=xseries,y = data[name], ax=axes[row, col])
            ax = axes[row,col]
            ax.tick_params(labelrotation=45)
            i += 1     
    plt.setp(axes, yticks=[])
    plt.tight_layout()


def sub_violinplots(x, y, group, data, ylabel, xlabel, pal="pastel"):
    sns.set(style="white", palette= pal, color_codes=True)
    f, ax = plt.subplots(1,1, figsize=(19, 10))
    sns.set_context("paper", font_scale = 2)
    sns.despine(left=True)
    ax = sns.violinplot(x=x, y=y, hue=group, data=data, 
                        split=True, scale="width", inner="quartile", font_scale = 2)
    ax.tick_params(labelrotation=45, labelsize= 15)
    ax.set_ylabel('{}'.format(ylabel), fontsize = 20) # Y label
    ax.set_xlabel('{}'.format(xlabel), fontsize = 20) 
    plt.setp(ax, yticks=[])
    plt.tight_layout()
    
    
def visualization_three(output_image_name):
    pass

def visualization_four(output_image_name):
    pass