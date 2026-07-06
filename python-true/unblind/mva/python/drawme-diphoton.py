from TreeWrapper import TreeWrapper
from TreeMaker import TreeMaker
from array import array
from ROOT import TFile, TMVA, TCanvas, TH1D, TF1
from ctypes import *

tree = TreeWrapper('unblind_data_sweighted.root', 'DecayTree')

sigma = 24.4
meta = 547.9
mpion = 134.0
momega = 782.7
metap = 957.8

errfull = c_double()
erreta = c_double()
errpion = c_double()
erromega = c_double()
erretap = c_double()


canvas = TCanvas()
tree.Draw('diphoton_with_constraint_M')
tree.Draw('diphoton_with_constraint_M', 'sweight', 'same hist')
canvas.Modified()
canvas.Update()

#canvas3 = TCanvas()
#tree.Draw('diphoton_with_constraint_M', 'sweight', '')
# canvas3.Modified()
# canvas3.Update()

#canvas4 = TCanvas()
#tree.Draw('diphoton_with_constraint_M', 'diphoton_with_constraint_M < 450', '')
# canvas4.Modified()
# canvas4.Update()

hist_BM = TH1D('hist_diphotonM', ';m_{#gamma#gamma}', 100, 0, 3500)
tree.Draw('diphoton_with_constraint_M >> hist_diphotonM', 'sweight', '')
fullamount = hist_BM.IntegralAndError(1, 100, errfull)

hist_eta = TH1D('hist_diphotonM2',
                ';m_{#gamma#gamma}', 10, meta - 2*sigma, meta + 2*sigma)
tree.Draw('diphoton_with_constraint_M >> hist_diphotonM2', 'sweight', '')
etaamount = hist_eta.IntegralAndError(1, 10, erreta)

hist_pion = TH1D('hist_diphotonM3',
                 ';m_{#gamma#gamma}', 10, mpion - 2*sigma, mpion + 2*sigma)
tree.Draw('diphoton_with_constraint_M >> hist_diphotonM3', 'sweight', '')
pionamount = hist_pion.IntegralAndError(1, 10, errpion)

hist_omega = TH1D('hist_diphotonM4',
                  ';m_{#gamma#gamma}', 10, momega - 2*sigma, momega + 2*sigma)
tree.Draw('diphoton_with_constraint_M >> hist_diphotonM4', 'sweight', '')
omegaamount = hist_omega.IntegralAndError(1, 10, erromega)

hist_etap = TH1D('hist_diphotonM5',
                 ';m_{#gamma#gamma}', 10, metap - 2*sigma, metap + 2*sigma)
tree.Draw('diphoton_with_constraint_M >> hist_diphotonM5', 'sweight', '')
etapamount = hist_etap.IntegralAndError(1, 10, erretap)

amount = fullamount - etaamount - pionamount - omegaamount - etapamount
err = (errfull.value**2 - erreta.value**2 - erretap.value **
       2 - errpion.value**2 - erretap.value**2)**0.5

print(amount)
print(err)
print(fullamount)
print(errfull)

input("Press Enter to continue...")
