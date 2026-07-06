from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooExponential, RooCBShape, RooAddPdf, RooArgSet, RooArgList, kRed, kGreen, kOrange, kYellow, kDashed, TCanvas


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
    mass = RooRealVar('mass', 'm_{B}', 5000, 6500, 'MeV')
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
mean = RooRealVar('mean',  'm_{B}',  5296)
sigma1 = RooRealVar('sigma1', '#sigma1',   81.99)
sigma2 = RooRealVar('sigma2', '#sigma2',   246.8)

k1mean = RooRealVar('k1mean',  'm_{K1}',  5018)
alpha = RooRealVar('alpha', 'alpha', -1.621)
n = RooRealVar('n', 'n', 0.9935)
k1sigma = RooRealVar('k1sigma', 'k1sigma', 150.2)

signalPDF = RooGaussian('signalpdf', 'signalpdf', mass, mean, sigma1)
sig2PDF = RooGaussian('sig2pdf', 'sig2pdf', mass, mean, sigma2)
k1PDF = RooCBShape('k1pdf', 'k1pdf', mass, k1mean, k1sigma, alpha, n)

# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', -0.001, -1e-1, -1e-8)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)


# now we need to add them together, with the different yields
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 5000, 0, 100000)
Nsig2 = RooRealVar('Nsig2', 'N_{S2}', 0.8369038858694966)

sigPDF = RooAddPdf('sigpdf', 'sigpdf', RooArgList(
    signalPDF, sig2PDF), RooArgList(Nsig2))

Nk1 = RooRealVar('Nk1', 'N_{k1}', 15000, 0, 100000)
Nbackground = RooRealVar('Nbackground', 'N_{Bkg}', 45000, 1000, 100000)

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    sigPDF, backgroundPDF, k1PDF), RooArgList(Nsignal, Nbackground, Nk1))

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
totalPDF.plotOn(frame, RooFit.Components("sigpdf"),
                RooFit.LineColor(kRed), RooFit.LineStyle(kDashed))
totalPDF.plotOn(frame, RooFit.Components("k1pdf"),
                RooFit.LineColor(kOrange), RooFit.LineStyle(kDashed))
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
