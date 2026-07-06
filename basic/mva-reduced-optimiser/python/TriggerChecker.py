from TreeMaker import TreeMaker
from array import array
from TreeWrapper import TreeWrapper
import numpy as np
from ROOT import TTree, TFile, TBrowser, TCanvas, gRandom, TH1F

# Load datasets
data_tree_up = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/Data/Data2018Kstgg_MagUp.root', 'DecayTree')
mc_tree_up = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/MC/MC2018Ksteta_11102452_MagUp.root', 'DecayTree')
data_tree_down = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/Data/Data2018Kstgg_MagDown.root', 'DecayTree')
mc_tree_down = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/MC/MC2018Ksteta_11102452_MagDown.root', 'DecayTree')

Ne = 25000  # amount of entries searched

for ii in ['B_L0HadronDecision_TIS', 'B_L0HadronDecision_TOS', 'B_L0PhotonDecision_TIS', 'B_L0PhotonDecision_TOS', 'B_L0ElectronDecision_TIS', 'B_L0ElectronDecision_TOS', 'B_L0MuonDecision_TIS', 'B_L0MuonDecision_TOS', 'B_Hlt1TrackMVADecision_TIS', 'B_Hlt1TrackMVADecision_TOS', 'B_Hlt1TwoTrackMVADecision_TIS', 'B_Hlt1TwoTrackMVADecision_TOS', 'B_Hlt2Topo2BodyDecision_TIS', 'B_Hlt2Topo2BodyDecision_TOS']:
    mc_array = []
    data_array = []

    mc_up_loc = 'mc_tree_up.'+ii
    data_up_loc = 'data_tree_up.'+ii
    mc_down_loc = 'mc_tree_down.'+ii
    data_down_loc = 'data_tree_down.'+ii

    for entry in mc_tree_up.entry(quiet=True, Nentries=Ne):
        mc_array.append(eval(mc_up_loc))

    for entry in data_tree_up.entry(quiet=True, Nentries=Ne):
        if data_tree_up.B_M > 5800:
            data_array.append(eval(data_up_loc))

    for entry in mc_tree_down.entry(quiet=True, Nentries=Ne):
        mc_array.append(eval(mc_down_loc))

    for entry in data_tree_down.entry(quiet=True, Nentries=Ne):
        if data_tree_down.B_M > 5800:
            data_array.append(eval(data_down_loc))

    print('for', ii, 'the MC value is\t', round(np.mean(mc_array), 4), 'the background value is\t', round(np.mean(data_array), 4), 'and the difference is\t',
          round(np.mean(mc_array)-np.mean(data_array), 4), '\t(', round((np.mean(mc_array)-np.mean(data_array))*100/min(np.mean(mc_array), np.mean(data_array)), 4), '%)')

input("Press Enter to continue...")
