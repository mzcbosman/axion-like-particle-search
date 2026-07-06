from ROOT import TTree, TH1D, TF1, kBlue, kCyan
from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooExponential, RooAddPdf, RooArgSet, RooArgList, kRed, kGreen, kDashed, TCanvas

import os
if not os.path.exists('myData.root'):

    # now to create a RooDataSet
    # create the variable to hold the data (name, title, range)
    mass = RooRealVar('mass', 'm_{gg}', 450, 650, 'MeV')
    weight = RooRealVar('weight', 'weight', 0, -10, 10)
    dataset = RooDataSet('mydata', 'mydata', RooArgSet(mass, weight), 'weight')

    # going to use the tree wrapper to reading the existing file
    from TreeWrapper import TreeWrapper
    tree = TreeWrapper('../roofit/blind_data_sweighted.root', 'DecayTree')
    for i in tree.entry():
        if mass.getMin() <= tree.diphoton_M < mass.getMax():
            mass.setVal(tree.diphoton_M)
            dataset.addFast(RooArgSet(mass), tree.sweight)

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
#                            Build a PDF to fit  sig                         #
#                                                                            #
##############################################################################

# We need to define a PDF to fit to the data, and all the parameters that PDF
# depends on


# signal PDF, we'll use a gaussian
mean = RooRealVar('mean',  'm_{B}',  550, 450, 650)
sigma = RooRealVar('sigma', '#sigma',   20,    5,  50)

signalPDF = RooGaussian('signalpdf', 'signalpdf', mass, mean, sigma)

# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', 0)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)

# now we need to add them together, with the different yields
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 1000, 0, 50000)
Nbackground = RooRealVar('Nbackground', 'N_{bkg}', 1000, 0, 50000)

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    signalPDF, backgroundPDF), RooArgList(Nsignal, Nbackground))

##############################################################################
#                                                                            #
#                               Run the fit                                  #
#                                                                            #
##############################################################################
sigresult = totalPDF.fitTo(dataset, RooFit.Strategy(
    2), RooFit.Extended(True), RooFit.Save(True))

# check for convergence and the quality of the covariance matrix
if sigresult.status() == 0:
    print('Migrad converged')
else:
    print('Migrad did not converge')

if sigresult.covQual() == 3:
    print('Errors accurate')
else:
    print('Errors not accurate')


##############################################################################
#                                                                            #
#                        Plot the sigresult and pulls                        #
#                                                                            #
##############################################################################

sigframe = mass.frame(RooFit.Title(' '), RooFit.Bins(105))
dataset.plotOn(sigframe)
totalPDF.plotOn(sigframe)
totalPDF.plotOn(sigframe, RooFit.Components("signalpdf"),
                RooFit.LineColor(kRed), RooFit.LineStyle(kDashed))
totalPDF.plotOn(sigframe, RooFit.Components("backgroundpdf"),
                RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed))

pullsigframe = mass.frame(RooFit.Title(' '))
# make a pull histogram for the dataset vs the totalpdf
pulls = sigframe.getObject(0).makeResidHist(sigframe.getObject(1), True)
pullsigframe.addPlotable(pulls, 'P')


canvas = TCanvas()
canvas.Divide(1, 2)
canvas.cd(1)
sigframe.Draw()

canvas.cd(2)
pullsigframe.Draw()
canvas.Modified()
canvas.Update()

##############################################################################
#                                                                            #
#                            Build a PDF to fit bkg                          #
#                                                                            #
##############################################################################

# We need to define a PDF to fit to the data, and all the parameters that PDF
# depends on


# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', 0)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)

# now we need to add them together, with the different yields
Nbackground = RooRealVar('Nbackground', 'N_{bkg}', 1000, 0, 50000)

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    backgroundPDF), RooArgList(Nbackground))

##############################################################################
#                                                                            #
#                               Run the fit                                  #
#                                                                            #
##############################################################################
bkgresult = totalPDF.fitTo(dataset, RooFit.Strategy(
    2), RooFit.Extended(True), RooFit.Save(True))

# check for convergence and the quality of the covariance matrix
if bkgresult.status() == 0:
    print('Migrad converged')
else:
    print('Migrad did not converge')

if bkgresult.covQual() == 3:
    print('Errors accurate')
else:
    print('Errors not accurate')


##############################################################################
#                                                                            #
#                        Plot the bkgresult and pulls                        #
#                                                                            #
##############################################################################

bkgframe = mass.frame(RooFit.Title(' '), RooFit.Bins(105))
dataset.plotOn(bkgframe)
totalPDF.plotOn(bkgframe)
totalPDF.plotOn(bkgframe, RooFit.Components("backgroundpdf"),
                RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed))

pullbkgframe = mass.frame(RooFit.Title(' '))
# make a pull histogram for the dataset vs the totalpdf
pulls = bkgframe.getObject(0).makeResidHist(bkgframe.getObject(1), True)
pullbkgframe.addPlotable(pulls, 'P')


canvas2 = TCanvas()
canvas2.Divide(1, 2)
canvas2.cd(1)
bkgframe.Draw()

canvas2.cd(2)
pullbkgframe.Draw()
canvas2.Modified()
canvas2.Update()

print('Your sig NLL is ' + str(sigresult.minNll()))
print('Your bkg NLL is ' + str(bkgresult.minNll()))
print('Your test statistic is ' +
      str(abs(sigresult.minNll()-bkgresult.minNll()) ** 0.5))

input("Press ENTER to exit")
