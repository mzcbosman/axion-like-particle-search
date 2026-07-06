from TreeMaker import TreeMaker
from array import array
from TreeWrapper import TreeWrapper
from ROOT import TTree, TFile, TBrowser, TCanvas, gRandom

# open tree in wrapper
data_treewrapper_up = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/Data/Data2018Kstgg_MagUp.root', 'DecayTree')

data_treewrapper_down = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/Data/Data2018Kstgg_MagDown.root', 'DecayTree')

sideband_treemaker = TreeMaker(
    'data-unblind-sideband.root',  # output file name
    'DecayTree',  # output tree name
    ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'diphoton_with_constraint_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
     'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
     'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
     'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi']  # list of branches
)

for entry in data_treewrapper_up.entry():
    # make sure we get high mass sideband and selection is unblind (diphoton mass within 200 MeV of eta)
    # and the K prob is high (this is a strongly discriminating factor)
    if data_treewrapper_up.B_M > 5800 and data_treewrapper_up.K_ProbNNk > 0.1 and data_treewrapper_up.B_L0PhotonDecision_TOS == 1 and data_treewrapper_up.B_Hlt1TrackMVADecision_TOS == 1 and data_treewrapper_up.B_Hlt2Topo2BodyDecision_TOS == 1:
        sideband_treemaker.Fill({  # wants a dictionary of values
            'B_M': data_treewrapper_up.B_M,
            'Kst_M': data_treewrapper_up.Kst_M,
            'gamma0_P': data_treewrapper_up.gamma0_P,
            'gamma1_P': data_treewrapper_up.gamma1_P,
            'diphoton_M': data_treewrapper_up.diphoton_M,
            'diphoton_with_constraint_M': data_treewrapper_up.diphoton_with_constraint_M,
            'B_FD_OWNPV': data_treewrapper_up.B_FD_OWNPV,
            'B_P': data_treewrapper_up.B_P,
            'B_PT': data_treewrapper_up.B_PT,
            'B_DIRA_OWNPV': data_treewrapper_up.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': data_treewrapper_up.B_ENDVERTEX_CHI2,
            'B_CONEP_100': data_treewrapper_up.B_CONEP_100,
            'B_CONEMULT_100': data_treewrapper_up.B_CONEMULT_100,
            'B_NC_IT_100': data_treewrapper_up.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': data_treewrapper_up.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': data_treewrapper_up.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': data_treewrapper_up.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': data_treewrapper_up.Kst_P,
            'Kst_PT': data_treewrapper_up.Kst_PT,
            'K_P': data_treewrapper_up.K_P,
            'K_PT': data_treewrapper_up.K_PT,
            'pi_P': data_treewrapper_up.pi_P,
            'pi_PT': data_treewrapper_up.pi_PT,
            'Kst_IPCHI2_OWNPV': data_treewrapper_up.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': data_treewrapper_up.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': data_treewrapper_up.pi_IPCHI2_OWNPV,
            'K_ProbNNk': data_treewrapper_up.K_ProbNNk,
            'pi_ProbNNpi': data_treewrapper_up.pi_ProbNNpi
        })

for entry in data_treewrapper_down.entry():
    # make sure we get high mass sideband and selection is unblind (diphoton mass within 200 MeV of eta)
    # and the K prob is high (this is a strongly discriminating factor)
    if data_treewrapper_down.B_M > 5800 and data_treewrapper_down.K_ProbNNk > 0.1 and data_treewrapper_down.B_L0PhotonDecision_TOS == 1 and data_treewrapper_down.B_Hlt1TrackMVADecision_TOS == 1 and data_treewrapper_down.B_Hlt2Topo2BodyDecision_TOS == 1:
        sideband_treemaker.Fill({  # wants a dictionary of values
            'B_M': data_treewrapper_down.B_M,
            'Kst_M': data_treewrapper_down.Kst_M,
            'gamma0_P': data_treewrapper_down.gamma0_P,
            'gamma1_P': data_treewrapper_down.gamma1_P,
            'diphoton_M': data_treewrapper_down.diphoton_M,
            'diphoton_with_constraint_M': data_treewrapper_down.diphoton_with_constraint_M,
            'B_FD_OWNPV': data_treewrapper_down.B_FD_OWNPV,
            'B_P': data_treewrapper_down.B_P,
            'B_PT': data_treewrapper_down.B_PT,
            'B_DIRA_OWNPV': data_treewrapper_down.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': data_treewrapper_down.B_ENDVERTEX_CHI2,
            'B_CONEP_100': data_treewrapper_down.B_CONEP_100,
            'B_CONEMULT_100': data_treewrapper_down.B_CONEMULT_100,
            'B_NC_IT_100': data_treewrapper_down.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': data_treewrapper_down.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': data_treewrapper_down.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': data_treewrapper_down.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': data_treewrapper_down.Kst_P,
            'Kst_PT': data_treewrapper_down.Kst_PT,
            'K_P': data_treewrapper_down.K_P,
            'K_PT': data_treewrapper_down.K_PT,
            'pi_P': data_treewrapper_down.pi_P,
            'pi_PT': data_treewrapper_down.pi_PT,
            'Kst_IPCHI2_OWNPV': data_treewrapper_down.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': data_treewrapper_down.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': data_treewrapper_down.pi_IPCHI2_OWNPV,
            'K_ProbNNk': data_treewrapper_down.K_ProbNNk,
            'pi_ProbNNpi': data_treewrapper_down.pi_ProbNNpi
        })
sideband_treemaker.close()

data_treemaker = TreeMaker(
    'data-unblind-full.root',  # output file name
    'DecayTree',  # output tree name
    ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'diphoton_with_constraint_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
     'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
     'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
     'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi']  # list of branches
)

for entry in data_treewrapper_up.entry():
    # make sure selection is unblind (diphoton mass within 200 MeV of eta)
    # and the K prob is high (this is a strongly discriminating factor)
    if data_treewrapper_up.K_ProbNNk > 0.1 and data_treewrapper_up.B_L0PhotonDecision_TOS == 1 and data_treewrapper_up.B_Hlt1TrackMVADecision_TOS == 1 and data_treewrapper_up.B_Hlt2Topo2BodyDecision_TOS == 1:
        data_treemaker.Fill({  # wants a dictionary of values
            'B_M': data_treewrapper_up.B_M,
            'Kst_M': data_treewrapper_up.Kst_M,
            'gamma0_P': data_treewrapper_up.gamma0_P,
            'gamma1_P': data_treewrapper_up.gamma1_P,
            'diphoton_M': data_treewrapper_up.diphoton_M,
            'diphoton_with_constraint_M': data_treewrapper_up.diphoton_with_constraint_M,
            'B_FD_OWNPV': data_treewrapper_up.B_FD_OWNPV,
            'B_P': data_treewrapper_up.B_P,
            'B_PT': data_treewrapper_up.B_PT,
            'B_DIRA_OWNPV': data_treewrapper_up.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': data_treewrapper_up.B_ENDVERTEX_CHI2,
            'B_CONEP_100': data_treewrapper_up.B_CONEP_100,
            'B_CONEMULT_100': data_treewrapper_up.B_CONEMULT_100,
            'B_NC_IT_100': data_treewrapper_up.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': data_treewrapper_up.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': data_treewrapper_up.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': data_treewrapper_up.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': data_treewrapper_up.Kst_P,
            'Kst_PT': data_treewrapper_up.Kst_PT,
            'K_P': data_treewrapper_up.K_P,
            'K_PT': data_treewrapper_up.K_PT,
            'pi_P': data_treewrapper_up.pi_P,
            'pi_PT': data_treewrapper_up.pi_PT,
            'Kst_IPCHI2_OWNPV': data_treewrapper_up.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': data_treewrapper_up.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': data_treewrapper_up.pi_IPCHI2_OWNPV,
            'K_ProbNNk': data_treewrapper_up.K_ProbNNk,
            'pi_ProbNNpi': data_treewrapper_up.pi_ProbNNpi
        })

for entry in data_treewrapper_down.entry():
    # make sure selection is unblind (diphoton mass within 200 MeV of eta)
    # and the K prob is high (this is a strongly discriminating factor)
    if data_treewrapper_down.K_ProbNNk > 0.1 and data_treewrapper_down.B_L0PhotonDecision_TOS == 1 and data_treewrapper_down.B_Hlt1TrackMVADecision_TOS == 1 and data_treewrapper_down.B_Hlt2Topo2BodyDecision_TOS == 1:
        data_treemaker.Fill({  # wants a dictionary of values
            'B_M': data_treewrapper_down.B_M,
            'Kst_M': data_treewrapper_down.Kst_M,
            'gamma0_P': data_treewrapper_down.gamma0_P,
            'gamma1_P': data_treewrapper_down.gamma1_P,
            'diphoton_M': data_treewrapper_down.diphoton_M,
            'diphoton_with_constraint_M': data_treewrapper_down.diphoton_with_constraint_M,
            'B_FD_OWNPV': data_treewrapper_down.B_FD_OWNPV,
            'B_P': data_treewrapper_down.B_P,
            'B_PT': data_treewrapper_down.B_PT,
            'B_DIRA_OWNPV': data_treewrapper_down.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': data_treewrapper_down.B_ENDVERTEX_CHI2,
            'B_CONEP_100': data_treewrapper_down.B_CONEP_100,
            'B_CONEMULT_100': data_treewrapper_down.B_CONEMULT_100,
            'B_NC_IT_100': data_treewrapper_down.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': data_treewrapper_down.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': data_treewrapper_down.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': data_treewrapper_down.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': data_treewrapper_down.Kst_P,
            'Kst_PT': data_treewrapper_down.Kst_PT,
            'K_P': data_treewrapper_down.K_P,
            'K_PT': data_treewrapper_down.K_PT,
            'pi_P': data_treewrapper_down.pi_P,
            'pi_PT': data_treewrapper_down.pi_PT,
            'Kst_IPCHI2_OWNPV': data_treewrapper_down.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': data_treewrapper_down.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': data_treewrapper_down.pi_IPCHI2_OWNPV,
            'K_ProbNNk': data_treewrapper_down.K_ProbNNk,
            'pi_ProbNNpi': data_treewrapper_down.pi_ProbNNpi
        })
data_treemaker.close()

canvas2 = TCanvas()
that_tree = TreeWrapper('data-unblind-sideband.root', 'DecayTree')
# Draw the original B mass distribution
that_tree.Draw('B_M')
canvas2.Modified()
canvas2.Update()

canvas3 = TCanvas()
that_tree = TreeWrapper('data-unblind-full.root', 'DecayTree')
# Draw the original B mass around its peak
that_tree.Draw('B_M', 'abs(B_M - 5280) < 1000')
canvas3.Modified()
canvas3.Update()

canvas4 = TCanvas()
that_tree = TreeWrapper('data-unblind-full.root', 'DecayTree')
# Draw the original B mass in a 100 MeV window around the peak
that_tree.Draw('diphoton_M')
canvas4.Modified()
canvas4.Update()

canvas5 = TCanvas()
that_tree = TreeWrapper('data-unblind-full.root', 'DecayTree')
# Draw the original B mass in a 100 MeV window around the peak
that_tree.Draw('diphoton_with_constraint_M')
canvas5.Modified()
canvas5.Update()

input("Press Enter to Exit...")
