import os
from TreeMaker import TreeMaker
from array import array
from TreeWrapper import TreeWrapper
from ROOT import TFile, RooFit, RooDataSet, RooRealVar, RooGaussian, RooExponential, RooCBShape, RooAddPdf, RooArgSet, RooArgList, kRed, kGreen, kYellow, kOrange, kDashed, TCanvas

with TreeMaker("blind_data_afterBDT01.root", "DecayTree", ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'diphoton_with_constraint_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
                                                           'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
                                                           'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
                                                           'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi', 'BDT']) as outtree:
    tree = TreeWrapper(
        "blind_data_withBDT.root", "DecayTree")
    for entry in tree.entry():
        if tree.BDT > 0.1 and 5000 <= tree.B_M < 6500:
            outtree.Fill({
                "B_M": tree.B_M,
                "Kst_M": tree.Kst_M,
                "gamma0_P": tree.gamma0_P,
                "gamma1_P": tree.gamma1_P,
                "diphoton_M": tree.diphoton_M,
                "diphoton_with_constraint_M": tree.diphoton_with_constraint_M,
                "B_FD_OWNPV": tree.B_FD_OWNPV,
                "B_P": tree.B_P,
                "B_PT": tree.B_PT,
                "B_DIRA_OWNPV": tree.B_DIRA_OWNPV,
                "B_ENDVERTEX_CHI2": tree.B_ENDVERTEX_CHI2,
                "B_CONEP_100": tree.B_CONEP_100,
                "B_CONEMULT_100": tree.B_CONEMULT_100,
                "B_NC_IT_100": tree.B_NC_IT_100,
                "B_NEWVTXISODCHI2MASS": tree.B_NEWVTXISODCHI2MASS,
                "B_VTXISODCHI2MASSONETRACK": tree.B_VTXISODCHI2MASSONETRACK,
                "B_VTXISODCHI2MASSTWOTRACK": tree.B_VTXISODCHI2MASSTWOTRACK,
                "Kst_P": tree.Kst_P,
                "Kst_PT": tree.Kst_PT,
                "K_P": tree.K_P,
                "K_PT": tree.K_PT,
                "pi_P": tree.pi_P,
                "pi_PT": tree.pi_PT,
                "Kst_IPCHI2_OWNPV": tree.Kst_IPCHI2_OWNPV,
                "K_IPCHI2_OWNPV": tree.K_IPCHI2_OWNPV,
                "pi_IPCHI2_OWNPV": tree.pi_IPCHI2_OWNPV,
                "K_ProbNNk": tree.K_ProbNNk,
                "pi_ProbNNpi": tree.pi_ProbNNpi,
                "BDT": tree.BDT
            })

with TreeMaker("blind_MC_afterBDT01.root", "DecayTree", ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
                                                         'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
                                                         'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
                                                         'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi', 'BDT']) as outtree:
    tree = TreeWrapper(
        "blind_mc_withBDT.root", "DecayTree")
    for entry in tree.entry():
        if tree.BDT > 0.1 and 5000 <= tree.B_M < 6500:
            outtree.Fill({
                "B_M": tree.B_M,
                "Kst_M": tree.Kst_M,
                "gamma0_P": tree.gamma0_P,
                "gamma1_P": tree.gamma1_P,
                "diphoton_M": tree.diphoton_M,
                "B_FD_OWNPV": tree.B_FD_OWNPV,
                "B_P": tree.B_P,
                "B_PT": tree.B_PT,
                "B_DIRA_OWNPV": tree.B_DIRA_OWNPV,
                "B_ENDVERTEX_CHI2": tree.B_ENDVERTEX_CHI2,
                "B_CONEP_100": tree.B_CONEP_100,
                "B_CONEMULT_100": tree.B_CONEMULT_100,
                "B_NC_IT_100": tree.B_NC_IT_100,
                "B_NEWVTXISODCHI2MASS": tree.B_NEWVTXISODCHI2MASS,
                "B_VTXISODCHI2MASSONETRACK": tree.B_VTXISODCHI2MASSONETRACK,
                "B_VTXISODCHI2MASSTWOTRACK": tree.B_VTXISODCHI2MASSTWOTRACK,
                "Kst_P": tree.Kst_P,
                "Kst_PT": tree.Kst_PT,
                "K_P": tree.K_P,
                "K_PT": tree.K_PT,
                "pi_P": tree.pi_P,
                "pi_PT": tree.pi_PT,
                "Kst_IPCHI2_OWNPV": tree.Kst_IPCHI2_OWNPV,
                "K_IPCHI2_OWNPV": tree.K_IPCHI2_OWNPV,
                "pi_IPCHI2_OWNPV": tree.pi_IPCHI2_OWNPV,
                "K_ProbNNk": tree.K_ProbNNk,
                "pi_ProbNNpi": tree.pi_ProbNNpi,
                "BDT": tree.BDT
            })

canvasx = TCanvas()
treewrapper_mc = TreeWrapper("blind_MC_afterBDT01.root", "DecayTree")
treewrapper_mc.Draw('B_M')
canvasx.Modified()
canvasx.Update()


if not os.path.exists('myData.root'):

    # now to create a RooDataSet
    # create the variable to hold the data (name, title, range)
    mass = RooRealVar('mass', 'm_{B}', 5000, 6500, 'MeV')
    dataset = RooDataSet('mydata', 'mydata', RooArgSet(mass))

    # going to use the tree wrapper to reading the existing file
    from TreeWrapper import TreeWrapper
    tree = TreeWrapper('../mva/blind_data_afterBDT01.root', 'DecayTree')
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

Nk1 = RooRealVar('Nk1', 'N_{k1}', 5000, 0, 100000)
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
