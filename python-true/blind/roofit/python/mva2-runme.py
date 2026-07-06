##############################################################################
#                                                                            #
#                          Simple RooFit Example                             #
#                                                                            #
##############################################################################

from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooCBShape, RooExponential, RooAddPdf, RooArgSet, RooArgList, kRed, kGreen, kDashed, TCanvas


# Before we can do any fitting we must put the data into a format that RooFtit
# can use. This is a RooDataSet

# Let's start with the data in data/example.root again. We'll open it, convert
# the data to RooFit's format, then save that to a file so we don't need to do
# it again

# first of all check whether it exists already

import os
if not os.path.exists('myData.root'):

    # now to create a RooDataSet
    # create the variable to hold the data (name, title, range)
    mass = RooRealVar('mass', 'm_{B}', 4800, 6800, 'MeV')
    dataset = RooDataSet('mydata', 'mydata', RooArgSet(mass))

    # going to use the tree wrapper to reading the existing file
    from TreeWrapper import TreeWrapper
    tree = TreeWrapper('../mva/blind_data_afterBDT.root', 'DecayTree')
    for i in tree.entry():
        if mass.getMin() <= tree.B_M < mass.getMax():
            mass.setVal(tree.B_M)
            dataset.addFast(RooArgSet(mass))

    # now let's save the file
    file = TFile('myData.root', 'recreate')
    file.WriteTObject(dataset)
    file.Close()


# Read in the data
file = TFile('myData.root')
dataset = file.Get('mydata')


# our fit variable
mass = dataset.get().find('mass')

##############################################################################
#                                                                            #
#                            Build a PDF to fit                              #
#                                                                            #
##############################################################################

# We need to define a PDF to fit to the data, and all the parameters that PDF
# depends on


# signal PDF, we'll use a gaussian
mean = RooRealVar('mean',  'm_{B}',  5289)
sigma = RooRealVar('sigma', '#sigma',   90.93)
alpha = RooRealVar('alpha', '#alpha',   -1.369)
n = RooRealVar('n', '#n',   3.043)

signalPDF = RooCBShape('signalpdf', 'signalpdf', mass, mean, sigma, alpha, n)

# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', -0.001, -1e-1, -1e-6)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)


# now we need to add them together, with the different yields
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 1000, 0, 10000)
Nbackground = RooRealVar('Nbackground', 'N_{Bkg}', 5000, 0, 10000)

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    signalPDF, backgroundPDF), RooArgList(Nsignal, Nbackground))

##############################################################################
#                                                                            #
#                               Run the fit                                  #
#                                                                            #
##############################################################################
result = totalPDF.fitTo(dataset, RooFit.Strategy(
    2), RooFit.Extended(True), RooFit.Save(True))

# check for convergence and the quality of the covariance matrix
if result.status() == 0:
    print('Migrad converged')
else:
    print('Migrad did not converge')

if result.covQual() == 3:
    print('Errors accurate')
else:
    print('Errors not accurate')


##############################################################################
#                                                                            #
#                        Plot the result and pulls                           #
#                                                                            #
##############################################################################

frame = mass.frame(RooFit.Title(' '), RooFit.Bins(105))
dataset.plotOn(frame)
totalPDF.plotOn(frame)
totalPDF.plotOn(frame, RooFit.Components("signalpdf"),
                RooFit.LineColor(kRed), RooFit.LineStyle(kDashed))
totalPDF.plotOn(frame, RooFit.Components("bkgpdf"),
                RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed))

pullframe = mass.frame(RooFit.Title(' '))
# make a pull histogram for the dataset vs the totalpdf
pulls = frame.getObject(0).makeResidHist(frame.getObject(1), True)
pullframe.addPlotable(pulls, 'P')


canvas = TCanvas()
canvas.Divide(1, 2)
canvas.cd(1)
frame.Draw()

canvas.cd(2)
pullframe.Draw()
canvas.Modified()
canvas.Update()
input("Press ENTER to exit")
