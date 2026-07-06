##############################################################################
#                                                                            #
#                             SPlotting Example                              #
#                                                                            #
##############################################################################

from TreeMaker import TreeMaker
from TreeWrapper import TreeWrapper
from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooExponential, RooAddPdf, RooArgSet, RooArgList, RooStats, TCanvas


# SPlotting is a method for background subtraction. First a fit to the data
# needs to be done, then the weights must be computed. Then the weights must
# be associated with the original data again.

# We'll set up the fit pretty much as it was in the simple fit tutorial

import os
if not os.path.exists('myData.root'):

    mass = RooRealVar('mass',  'm_{B}', 4800, 6800, 'MeV')
    dataset = RooDataSet('mydata', 'mydata', RooArgSet(mass))

    from TreeWrapper import TreeWrapper
    tree = TreeWrapper('../mva/blind_data_afterBDT.root', 'DecayTree')
    for i in tree.entry():
        # if mass.getMin() <= tree.B_M < mass.getMax():
        mass.setVal(tree.B_M)
        dataset.addFast(RooArgSet(mass))

    file = TFile('myData.root', 'recreate')
    file.WriteTObject(dataset)
    file.Close()


file = TFile('myData.root')
dataset = file.Get('mydata')


# our fit variable
mass = dataset.get().find('mass')

##############################################################################
#                                                                            #
#                          Do the fitting stage                              #
#                                                                            #
##############################################################################

# mean.SetConstant

# signal PDF, we'll use a gaussian
mean = RooRealVar('mean',  'm_{B}',  5250, 4800, 6800)
sigma = RooRealVar('sigma', '#sigma',   100,    5,  150)
signalPDF = RooGaussian('signalpdf', 'signalpdf', mass, mean, sigma)

# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', -0.003, -1e-1, -1e-6)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)

# total PDF
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 1000, 0, 20000)
Nbackground = RooRealVar('Nbackground', 'N_{Bkg}', 1000, 0, 20000)
totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    signalPDF, backgroundPDF), RooArgList(Nsignal, Nbackground))

# Ok, time to do the fit
result = totalPDF.fitTo(dataset, RooFit.Strategy(
    2), RooFit.Extended(True), RooFit.Save(True))

if result.status() != 0 or result.covQual() != 3:
    print('Something has gone wrong with the fix')
    exit

##############################################################################
#                                                                            #
#                   Do the SPlot stage and save weights                      #
#                                                                            #
##############################################################################


splot = RooStats.SPlot('splot', 'splot', dataset, totalPDF,
                       RooArgList(Nsignal, Nbackground))

tree = TreeWrapper('../mva/blind_data_afterBDT.root', 'DecayTree')

with TreeMaker('blind_data_sweighted.root', 'DecayTree', ['B_M', 'diphoton_M', 'sweight']) as outtree:
    for entry in tree.entry():
        outtree.Fill({
            'B_M': tree.B_M,
            'diphoton_M': tree.diphoton_M,
            'sweight': dataset.get(entry).getRealValue('Nsignal_sw')
        })


##############################################################################
#                                                                            #
#                             Use the result                                 #
#                                                                            #
##############################################################################

tree = TreeWrapper('blind_data_sweighted.root', 'DecayTree')
canvas = TCanvas()
tree.Draw('diphoton_M')
tree.Draw('diphoton_M', 'sweight', 'same hist')
canvas.Modified()
canvas.Update()

canvas2 = TCanvas()
tree.Draw('B_M')
tree.Draw('B_M', 'sweight', 'same hist')
canvas2.Modified()
canvas2.Update()
input("Press ENTER to exit")
