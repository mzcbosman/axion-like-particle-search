from TreeMaker import TreeMaker
from array import array
from TreeWrapper import TreeWrapper
from ROOT import TTree, TFile, TBrowser, TCanvas, gRandom

canvas2 = TCanvas()
that_tree = TreeWrapper('data-blind-sideband.root', 'DecayTree')
# Draw the original B mass distribution
that_tree.Draw('B_M')
canvas2.Modified()
canvas2.Update()

canvas3 = TCanvas()
that_tree = TreeWrapper('data-blind-full.root', 'DecayTree')
# Draw the original B mass around its peak
that_tree.Draw('B_M', 'abs(B_M - 5280) < 1000')
canvas3.Modified()
canvas3.Update()

canvas4 = TCanvas()
that_tree = TreeWrapper('data-blind-full.root', 'DecayTree')
# Draw the original B mass in a 100 MeV window around the peak
that_tree.Draw('diphoton_M')
canvas4.Modified()
canvas4.Update()

input("Press Enter to Exit...")
