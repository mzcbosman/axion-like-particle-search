###############################################################################
#                                                                             #
#                 A simple example of ROOT's histogram fitting                #
#                                                                             #
###############################################################################


# ROOT has an internal fitting infrastructure designed for basic fits to graphs
# and histograms. For more complicated fits see the RooFit example. In this
# example some simple fits are performed on an example dataset.


from ROOT import TFile, TTree, TCanvas, TH1D, TF1, kBlue, kRed, kGreen, kCyan

# first lets get a histogram from the example data
file = TFile('../mc-creator/MC-blind.root')
tree = file.Get('DecayTree')

# make a histogram with 100 bins in the range [4900:7000] to store our data
hist_BM = TH1D('hist_BM', ';m_{K#pi#mu#mu}', 100, 4800, 5800)
# ask the tree to draw the specified data into our histogram
tree.Draw('B_M >> hist_BM', '', 'goff')

canvas = TCanvas()
hist_BM.Draw()
canvas.Modified()
canvas.Update()
print('''We're going to fit various functions to this data''')

###############################################################################
#                                                                             #
#                          Fit only a gaussian shape                          #
#                                                                             #
###############################################################################

# We're assuming the background is going to be exponential
input("Press ENTER to fit a gaussian")
# Create a new 1D fit fuction, using a built in function (expo) in the range [5500:7000]
fitshape_gaus = TF1('myfit1', 'gaus', 5280-100, 5280 + 100)
fitshape_gaus.SetLineColor(kRed)
# Fit the shape, specifying to use the range set by the function
hist_BM.Fit(fitshape_gaus, 'R')
canvas.Modified()
canvas.Update()
print('''\n\nYou should notice we've got a nice red line describing the background at high mass''')

###############################################################################
#                                                                             #
#                            Fit second gaussian shape                        #
#                                                                             #
###############################################################################
# So we're assuming in the signal region we're going to be gaussian
input("Press ENTER to fit two gaussians to the signal region")
fitshape_gaus2 = TF1('myfit2', 'gaus', 5100-100, 5100+100)
fitshape_gaus2.SetLineColor(kBlue)
hist_BM.Fit(fitshape_gaus2, 'R+')
canvas.Modified()
canvas.Update()
print('''\n\nYou should notice we've got a nice blue line describing the signal region''')


###############################################################################
#                                                                             #
#                Fit the sum of a signal and background shape                 #
#                                                                             #
###############################################################################

# Now we're going to make our own function, which should be the sum of a gaussian and exponential
input("Press ENTER to fit the full function")
# you can make your own function, by combining built-in functions (or writing from scratch), here we have to offset the parameter numbers, so the expo starts at 3, rather than 0
fitshape_full = TF1('myfit3', 'gaus+gaus(3)')
fitshape_full.SetLineColor(kGreen)
# NB we've removed the range requirement, so the full histogram can be set
hist_BM.Fit(fitshape_full, '+')
canvas.Modified()
canvas.Update()

print('''\n\nYou should notice this hasn't done a good job (green line)''')
print('''This is because the default starting values are too far from the best values''')


###############################################################################
#                                                                             #
#                     Setting the parameter starting values                   #
#                                                                             #
###############################################################################

# Now we need to start from a more reasonable place
input("Press ENTER to fit using the pre-fit values")
fitshape_full2 = TF1('myfit4', 'gaus+gaus(3)')
fitshape_full2.SetLineColor(kCyan)
# Set the names of the "physics" parameters
fitshape_full2.SetParName(0, 'NSignal')
fitshape_full2.SetParName(1, 'm_{B}')       #
fitshape_full2.SetParName(2, '#sigma_{B}')  #
# set the starting values from the result of the previous small range fits
fitshape_full2.SetParameter(0, fitshape_gaus2.GetParameter(0))
fitshape_full2.SetParameter(1, fitshape_gaus2.GetParameter(1))
fitshape_full2.SetParameter(2, fitshape_gaus2.GetParameter(2))
fitshape_full2.SetParameter(3, fitshape_gaus.GetParameter(0))
fitshape_full2.SetParameter(4, fitshape_gaus.GetParameter(1))
fitshape_full2.SetParameter(5, fitshape_gaus.GetParameter(2))
# Tell the fit to use our values rather than the defaults for the built-in functions with 'B' option
hist_BM.Fit(fitshape_full2, 'B+')
canvas.Modified()
canvas.Update()


print('''\n\nYou'll notice that the signal yield, NSignal, is the maximum of the Gaussian, not the number of signal events (which should be ~10k)''')
print('''We can improve this by using a normalised gaussian''')


###############################################################################
#                                                                             #
#                          Using a normalised gaussian                        #
#                                                                             #
###############################################################################

# Same thing, but using a normalised gaussian
input("Press ENTER to fit using the normalised gaussian")
fitshape_full3 = TF1('myfit5', 'gausn+gaus(3)')
fitshape_full3.SetLineColor(kCyan)
fitshape_full3.SetParName(0, 'NSignal')
fitshape_full3.SetParName(1, 'm_{B}')
fitshape_full3.SetParName(2, '#sigma_{B}')
fitshape_full3.SetParameter(0, fitshape_gaus2.GetParameter(0))
fitshape_full3.SetParameter(1, fitshape_gaus2.GetParameter(1))
fitshape_full3.SetParameter(2, fitshape_gaus2.GetParameter(2))
fitshape_full3.SetParameter(3, fitshape_gaus.GetParameter(0))
fitshape_full3.SetParameter(4, fitshape_gaus.GetParameter(1))
fitshape_full3.SetParameter(5, fitshape_gaus.GetParameter(2))
hist_BM.Fit(fitshape_full3, 'B+')
canvas.Modified()
canvas.Update()


print('''\n\nThis is better, but still not 10k it should be??''')
print('''This is because we've binned the data, so the values we're fitting are the integral over each bin''')
print('''We can compensate for this by including the integration region (bin width) in the function''')

###############################################################################
#                                                                             #
#                         Adding more parameters (fixed)                      #
#                                                                             #
###############################################################################
# Now we add another parameter to the fit to hold the scaling necessary to get
# the yield correctly, i.e. undoing the integration the binning does

# This is an important thing when dealing with binned data, shape parameters
# are fine, but yields need some thought. The function is a PDF that assumes
# it is dN/dm, where as we're fitting to binned data, where each bin is
# N = int_{m_{min}}^{m_{max}}(dN/dm dm), i.e it's the integral of the PDF over
# the bin. So the normalisation is different between the values of the bins
# and the values of the PDF. They are different by the integral region
# m_max - m_min, which is the bin width

input("Press ENTER to fit including a factor with the bin width")
# We're now multiplying our gaussian by a new parameter
fitshape_full4 = TF1('myfit6', '[6]*gausn+gaus(3)')
fitshape_full4.SetLineColor(kCyan)
fitshape_full4.SetParName(0, 'NSignal')
fitshape_full4.SetParName(1, 'm_{B}')
fitshape_full4.SetParName(2, '#sigma_{B}')
fitshape_full4.SetParameter(0, fitshape_gaus2.GetParameter(0))
fitshape_full4.SetParameter(1, fitshape_gaus2.GetParameter(1))
fitshape_full4.SetParameter(2, fitshape_gaus2.GetParameter(2))
fitshape_full4.SetParameter(3, fitshape_gaus.GetParameter(0))
fitshape_full4.SetParameter(4, fitshape_gaus.GetParameter(1))
fitshape_full4.SetParameter(5, fitshape_gaus.GetParameter(2))
# Here we our new parameter (and fix it in the fit) to the bin width
fitshape_full4.FixParameter(6, hist_BM.GetBinWidth(1))
# Now we're going to save the result of the fit with the 'S' option
result = hist_BM.Fit(fitshape_full4, 'SB+')
canvas.Modified()
canvas.Update()

###############################################################################
#                                                                             #
#                             Accessing the values                            #
#                                                                             #
###############################################################################

print('''\n\nYay, now we have something that tells us we have {} +/- {} signal events'''.format(
    result.Parameter(0), result.ParError(0)))
print('''The fit Chi2 is {}, with D.o.F {}, so a p-value {}'''.format(result.Chi2(),
      result.Ndf(), result.Prob()))

input("Press ENTER to exit")
