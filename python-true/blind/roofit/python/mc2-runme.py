from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooExponential, RooAddPdf, RooArgSet, RooArgList, kRed, kGreen, kDashed, TCanvas

import os
if not os.path.exists('myData.root'):

    # now to create a RooDataSet
    # create the variable to hold the data (name, title, range)
    mass = RooRealVar('mass', 'm_{B}', 4800, 5800, 'MeV')
    dataset = RooDataSet('mydata', 'mydata', RooArgSet(mass))

    # going to use the tree wrapper to reading the existing file
    from TreeWrapper import TreeWrapper
    tree = TreeWrapper('../mc-creator/MC-blind.root', 'DecayTree')
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
mean = RooRealVar('mean',  'm_{B}',  5250, 4800, 5800)
sigma1 = RooRealVar('sigma1', '#sigma1',   80,    5,  150)

signalPDF = RooGaussian('signalpdf', 'signalpdf', mass, mean, sigma1)

# background PDF, we'll use an exponential
sigma2 = RooRealVar('sigma2', '#sigma2', 250, 100, 500)
sig2PDF = RooGaussian('sig2pdf', 'sig2pdf', mass, mean, sigma2)


# now we need to add them together, with the different yields
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 30000, 0, 50000)

Nsig2 = RooRealVar('Nsig2', 'N_{S2}',  0.1, 0.001, 0.9)


sigPDF = RooAddPdf('sigpdf', 'sigpdf', RooArgList(
    signalPDF, sig2PDF), RooArgList(Nsig2))

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    sigPDF), RooArgList(Nsignal))

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

print(Nsig2.getValV())
input("Press ENTER to exit")
