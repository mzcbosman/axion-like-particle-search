from ROOT import TFile, RooFit, TTree, kRed, kGreen, TPaveLabel, kFullCircle, kFullTriangleUp, kDashed, TCanvas, TH1D, TF1, gStyle, gPad
from TreeMaker import TreeMaker
from TreeWrapper import TreeWrapper

tree1 = TreeWrapper('blind_data_sweighted.root', 'DecayTree')
tree2 = TreeWrapper('../mva/blind_mc_withBDT.root', 'DecayTree')

var = 'BDT'
begin = -0.2
end = 0.6

sum1abs = 0
sum2abs = 0

hist_1 = TH1D('hist_1', 'sWeighted normalisation channel', 100, begin, end)
tree1.Draw(var+' >> hist_1', 'sweight', 'goff')

hist_2 = TH1D('hist_2', 'Simulated B->K*eta events', 100, begin, end)
tree2.Draw(var+' >> hist_2', '', 'goff')

for i in range(100):
    sum1abs += abs(hist_1.GetBinContent(i+1))
    sum2abs += abs(hist_2.GetBinContent(i+1))

sum1 = hist_1.Integral()
sum2 = hist_2.Integral()
# hist_1.Scale(1/sum1)
# hist_2.Scale(1/sum2)
hist_1.Scale(1/sum1abs)
hist_2.Scale(1/sum2abs)

gStyle.SetPalette(104)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
# hist_1.SetMarkerStyle(kFullCircle)
# hist_2.SetMarkerStyle(kFullTriangleUp)

canvas = TCanvas()
hist_2.Draw('PMC PLC')
hist_1.Draw('same PMC PLC')
gPad.BuildLegend(0.6, 0.69, 0.9, 0.9)
canvas.Modified()
canvas.Update()

input('Press enter to quit')
