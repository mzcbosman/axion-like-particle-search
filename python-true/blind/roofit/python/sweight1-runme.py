##############################################################################
#                                                                            #
#                          Simple RooFit Example                             #
#                                                                            #
##############################################################################

from TreeMaker import TreeMaker
from TreeWrapper import TreeWrapper
from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooCBShape, RooExponential, RooAddPdf, RooArgSet, RooArgList, RooStats, kRed, kGreen, kDashed, TCanvas


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
mean = RooRealVar('mean',  'm_{B}',  5297)
sigma1 = RooRealVar('sigma1', '#sigma1',   82.33)
sigma2 = RooRealVar('sigma2', '#sigma2',   261.4)

signalPDF = RooGaussian('signalpdf', 'signalpdf', mass, mean, sigma1)
partrecoPDF = RooGaussian('partrecopdf', 'partrecopdf', mass, mean, sigma2)

# background PDF, we'll use an exponential
exponent = RooRealVar('exponent', '#tau_{Bkg}', -0.001, -1e-1, -1e-6)
backgroundPDF = RooExponential('bkgpdf', 'bkgpdf', mass, exponent)


# now we need to add them together, with the different yields
Nsignal = RooRealVar('Nsignal', 'N_{Sig}', 1000, 0, 10000)
Npartreco = RooRealVar('Npartreco', 'N_{pr}', 1000, 0, 10000)
Nbackground = RooRealVar('Nbackground', 'N_{Bkg}', 5000, 0, 10000)

totalPDF = RooAddPdf('totalpdf', 'totalpdf', RooArgList(
    signalPDF, partrecoPDF, backgroundPDF), RooArgList(Nsignal, Npartreco, Nbackground))

##############################################################################
#                                                                            #
#                               Run the fit                                  #
#                                                                            #
##############################################################################
result = totalPDF.fitTo(dataset, RooFit.Strategy(
    2), RooFit.Extended(True), RooFit.Save(True))

# check for convergence and the quality of the covariance matrix

if result.status() != 0 or result.covQual() != 3:
    print('Something has gone wrong with the fix')
    exit

##############################################################################
#                                                                            #
#                   Do the SPlot stage and save weights                      #
#                                                                            #
##############################################################################


splot = RooStats.SPlot('splot', 'splot', dataset, totalPDF,
                       RooArgList(Nsignal, Npartreco, Nbackground))

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
