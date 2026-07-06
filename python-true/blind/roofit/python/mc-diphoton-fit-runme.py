from ROOT import TFile, TTree, TCanvas, TH1D, TF1, kBlue, kRed, kGreen, kCyan

# first lets get a histogram from the example data
# file = TFile('../mc-creator/MC-blind.root')
file = TFile(
    '~/python-scripts/s-optimiser-blind/4-Hlt2TopoTOS/mc-creator/MC-blind.root')
tree = file.Get('DecayTree')

# make a histogram with 100 bins in the range [4900:7000] to store our data
hist_BM = TH1D('hist_diphotonM', ';m_{#gamma#gamma}', 100, 450, 650)
# ask the tree to draw the specified data into our histogram
tree.Draw('diphoton_M >> hist_diphotonM', '', 'goff')

canvas = TCanvas()
hist_BM.Draw()
canvas.Modified()
canvas.Update()
print('''We're going to fit various functions to this data''')


###############################################################################
#                                                                             #
#                            Fit only a signal shape                          #
#                                                                             #
###############################################################################
# So we're assuming in the signal region we're going to be gaussian
input("Press ENTER to fit an gaussian to the signal region")
fitshape_gaus = TF1('myfit2', 'gausn', 450, 650)
fitshape_gaus.SetLineColor(kBlue)
# fit in the range, and add it to the list of fits, i.e. don't replace the previous fit
hist_BM.Fit(fitshape_gaus, 'R')
canvas.Modified()
canvas.Update()
print('''\n\nYou should notice we've got a nice blue line describing the signal region''')


###############################################################################
#                                                                             #
#                     Setting the parameter starting values                   #
#                                                                             #
###############################################################################

# Now we need to start from a more reasonable place
input("Press ENTER to fit using the pre-fit values")
fitshape_full2 = TF1('myfit4', '[4]*gausn+[3]')
fitshape_full2.SetLineColor(kCyan)
# Set the names of the "physics" parameters
fitshape_full2.SetParName(0, 'NSignal')
fitshape_full2.SetParName(1, 'm_{diphoton}')       #
fitshape_full2.SetParName(2, '#sigma_{diphoton}')  #
fitshape_full2.SetParName(3, 'background')  #
# set the starting values from the result of the previous small range fits
fitshape_full2.SetParameter(0, fitshape_gaus.GetParameter(0))
fitshape_full2.SetParameter(1, fitshape_gaus.GetParameter(1))
fitshape_full2.SetParameter(2, fitshape_gaus.GetParameter(2))
fitshape_full2.SetParameter(4, hist_BM.GetBinWidth(1))
# Tell the fit to use our values rather than the defaults for the built-in functions with 'B' option
# Now we're going to save the result of the fit with the 'S' option
result = hist_BM.Fit(fitshape_full2, 'SB+')
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
