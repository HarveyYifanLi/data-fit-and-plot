# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 13:34:15 2015

@author: Yifan Li
"""
############################################################
#
# comments are explaining the following line of code
#
# AFTER a line of code, there can be multiple of the following lines that further explain the ABOVE line of code:
## <-- explains used function parameters. For additional information see the object inspector (help panel on the upper right)   
#### <-- this marks additional information that explain some of the inner workings of python
#
############################################################

# this boolean decides whether a fit is performed. The data itself is plotted in both cases.
make_fit = True
#make_fit = False

# import the usual libraries
import numpy as np
import matplotlib.pyplot as plt
# import the fitting functionality
from scipy.optimize import curve_fit
# import functionality to read out parameter names from a function
from inspect import getargspec
'''
# this section generates the test data on your computer -- please execute the script once and then delete or 'comment out' this section
#tmp = np.linspace(0.,3.,50)
#noise = 0.3*(np.random.random(50)-0.5)*2
#np.savetxt('testDataCurveFit.csv',np.column_stack((tmp,tmp*2.+1.+noise,np.ones(50)*0.2)),delimiter=',',fmt=' %.3f')
#del tmp
'''

# read in data - the file is assumed to be in csv format (separated by comma). Files need to be specified with a full path OR they have to be saved in the same folder as the script
data = np.loadtxt('squareWave.csv', delimiter=',', comments='#')
## alternative -- use skiprows=? : first ? rows are ignored during reading of data -- this can also be used to not read in the header information
# ----- a header is information at the beginning of a file, that identifies the following data, e.g., the column titles

# access the data columns and assign variables x,y,y_sigma. If you don't have error data, set "y_sigma = None"
x = data[:,0]
y = data[:,1]
#y_sigma = data[:,2]
#### data is not copied during this process - x,y,y_sigma are 'pointing' to the same memory as data

# the fit is only done if the flag make_fit=True
if make_fit :
    # "fit_function" is fitted to the data via least squares fit. A number of example functions are given below. Only have the function that you use uncommented and commet out all others.
    #def fit_function(x, y_intercept):
    #    """ constant function """
    #    return y_intercept*np.ones(x.shape)
    #def fit_function(x, slope, y_intercept):
        """ linear function """
        return slope*x + y_intercept
#    def fit_function(x, amplitude,frequency,phase,y_offset):
#        """ sine function """
#        return amplitude * np.sin( 2.*np.pi * frequency * x + phase ) + y_offset
    def fit_function(x, y_intercept,exponent,y_offset):
        """ exponential function """
#        NOTE: if the fit result is bad, then this is probably due to a bad initial guess for the fit parameters. Least square fit function "curve_fit" uses a default of 1. for each fit parameter, and the iterative optimization procedure usually fails, because one or more of the initial guesses have the wrong sign.
#        Two options:
#            1) Set an initial guess manually in the function "curve_fit" via the optional parameter "p0", which has to be specified as a list of values - one for each parameter. E.g. p0=[1.,-1,0.]
#            2) in a semi-log plot (y-axis is logarithmic), an exponential function appears as a straight line. You can use this fact to avoid the numerical issue. Fit x,ln(y) to a linear function. You then have to rescale the linear fit parameters to exponential fit parameters: y_intercept=exp(y_intercept) and exponent=slope. WARNING: This method assumes y_offset=0 !! There is no way around this. So, if you expect y_offset!=0, then you have to use method 1).  """
        return y_intercept * np.exp( x / exponent ) + y_offset
    
    # fit "fit_function" to the data
    fit_parameters_result,fit_covariance_matrix = curve_fit(fit_function,x,y,sigma=y_sigma,maxfev=10**5)
    ## sigma=y_sigma : the values y_sigma are used as weights. For an unweighted fit set 'sigma=None'
    ## maxfev=10**5 : set the maximum number of iterations of the least squares optimizer -- '**' is the power operator in python that usually has the symbol '^'

# plot data
plt.errorbar(x, y,yerr=y_sigma,marker='.',linestyle='',label="measured data")
## yerr=y_sigma : assign the data for the error bars in y-direction
## marker='o' : use markers to indicate each data point (x_1,y_1),(x_2,y_2)
## linestyle= '' : no line is drawn to connect the data points
## label=string : the string is shown in the legend

# add axis labels and title
plt.xlabel('Made up scale required')
plt.ylabel('Made up scale required')
plt.title(r'This is a title with latex $f(x)$')

# the fit is only done if the flag make_fit=True
if make_fit :
    # create fit data using the found fit parameters and plot the fit curve
    x_fit = np.linspace(min(x),max(x),2*len(x))
    y_fit = fit_function(x_fit,*fit_parameters_result)
    plt.plot(x_fit,y_fit,marker="",linestyle="-",linewidth=2,color="r",label="least squares fit")
    ## marker='' : data points are not indicated by markers
    ## linestyle= '-' : a continuous line is drawn
    ## linewidth=2 : the line thickness is set to 2
    ## color='r' : the color of the line is set to red
    ## label=string : the string is shown in the legend
    
    # show a legend
    plt.legend(loc=0,numpoints=1)
    ## loc=0 : show the legend where the least amount of data is obstructed
    
    # function that  calculates the chi square value of a fit
    def chi_square (fit_parameters, x, y, sigma):
        """ chi square value of a fit """
        if sigma is None : sigma = 1.
        return np.power((y-fit_function(x, *fit_parameters))/sigma,2).sum()
    # calculate and print chi square as well as the per degree-of-freedom value
    print "\nGoodness of fit - chi square measure:"
    chi2 = chi_square(fit_parameters_result,x,y,y_sigma)
    dof = len(x) - len(fit_parameters_result)
    print "Chi2 = {:.1f}, Chi2/dof = {:.3f}\n".format(chi2, chi2/dof)
    
    # the covariance matrix is rescaled to cancel the inverse scaling that is performed for numerical reasons during execution of curve_fit -- do not change this line!
    fit_covariance_matrix = fit_covariance_matrix*dof/chi2
    
    # read out fit parameter names
    parameter_names = getargspec(fit_function)[0][1:]
    
    # calculate the standard deviation as uncertainty of the fit parameters
    fit_parameters_error = np.sqrt(np.diag(fit_covariance_matrix))
    # print the found values for the fit parameters with their uncertainty
    print "Values of fit parameters:"
    for name,value,error in zip(parameter_names,fit_parameters_result,fit_parameters_error):
        print "{} = {:.3e} +/- {:.3e}".format(name, value, error)
    print "\n",
    
    # print the covariance between pairs of fit parameters
    print "Covariance between fit parameters:"
    for i,fit_covariance in enumerate(fit_covariance_matrix
    ) :
        for j in xrange(i+1,len(fit_covariance)) :
            print "{} and {} : {:.3e}".format(parameter_names[i],parameter_names[j],fit_covariance[j])
        
