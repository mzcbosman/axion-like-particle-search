from TreeWrapper import TreeWrapper
from TreeMaker import TreeMaker
from array import array
from ROOT import TFile, TMVA, TCanvas

canvas = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "abs(B_M - 5280) < 1000",  "")  # no BDT cut
tree.Draw("B_M", "abs(B_M - 5280) < 1000 && BDT >  0",
          "same")  # A loose BDT cut
tree.Draw("B_M", "abs(B_M - 5280) < 1000 && BDT > 0.2",
          "same")  # A tight BDT cut
canvas.Modified()
canvas.Update()

canvas2 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("diphoton_M", "abs(B_M - 5280) < 150",  "")  # no BDT cut
canvas2.Modified()
canvas2.Update()

canvas3 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("diphoton_M", "abs(B_M - 5280) < 150 && BDT > 0", "")  # loose BDT cut
canvas3.Modified()
canvas3.Update()

canvas4 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "",  "")  # no BDT cut
canvas4.Modified()
canvas4.Update()

canvas5 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "BDT >  0",
          "")  # A loose BDT cut
canvas5.Modified()
canvas5.Update()

canvas6 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "abs(B_M - 5280)<300",  "")  # no BDT cut
canvas6.Modified()
canvas6.Update()

canvas7 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "B_M > 5800 && BDT >  0",
          "")  # A loose BDT cut
canvas7.Modified()
canvas7.Update()

input("Press Enter to continue...")
