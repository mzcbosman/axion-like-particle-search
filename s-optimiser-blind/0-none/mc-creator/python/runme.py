from TreeMaker import TreeMaker
from array import array
from TreeWrapper import TreeWrapper
from ROOT import TTree, TFile, TBrowser, TCanvas, gRandom

# open tree in wrapper
mc_treewrapper_up = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/MC/MC2018Ksteta_11102452_MagUp.root', 'DecayTree')

mc_treewrapper_down = TreeWrapper(
    '/vols/lhcb/mmccann/analysis/kstgg/tuples/MC/MC2018Ksteta_11102452_MagDown.root', 'DecayTree')

treemaker = TreeMaker(
    'MC-blind.root',  # output file name
    'DecayTree',  # output tree name
    ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
     'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
     'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
     'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi']  # list of branches
)

for entry in mc_treewrapper_up.entry():
    # make sure the B is a B and the K is a K and that the selection is blind (200 MeV window around eta mass)
    # and the K prob is high (this is a strongly discriminating factor)
    if abs(mc_treewrapper_up.B_BKGCAT) == 30 and abs(mc_treewrapper_up.K_TRUEID) == 321 and abs(mc_treewrapper_up.diphoton_M - 550) < 100:
        treemaker.Fill({  # wants a dictionary of values
            'B_M': mc_treewrapper_up.B_M,
            'Kst_M': mc_treewrapper_up.Kst_M,
            'gamma0_P': mc_treewrapper_up.gamma0_P,
            'gamma1_P': mc_treewrapper_up.gamma1_P,
            'diphoton_M': mc_treewrapper_up.diphoton_M,
            'B_FD_OWNPV': mc_treewrapper_up.B_FD_OWNPV,
            'B_P': mc_treewrapper_up.B_P,
            'B_PT': mc_treewrapper_up.B_PT,
            'B_DIRA_OWNPV': mc_treewrapper_up.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': mc_treewrapper_up.B_ENDVERTEX_CHI2,
            'B_CONEP_100': mc_treewrapper_up.B_CONEP_100,
            'B_CONEMULT_100': mc_treewrapper_up.B_CONEMULT_100,
            'B_NC_IT_100': mc_treewrapper_up.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': mc_treewrapper_up.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': mc_treewrapper_up.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': mc_treewrapper_up.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': mc_treewrapper_up.Kst_P,
            'Kst_PT': mc_treewrapper_up.Kst_PT,
            'K_P': mc_treewrapper_up.K_P,
            'K_PT': mc_treewrapper_up.K_PT,
            'pi_P': mc_treewrapper_up.pi_P,
            'pi_PT': mc_treewrapper_up.pi_PT,
            'Kst_IPCHI2_OWNPV': mc_treewrapper_up.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': mc_treewrapper_up.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': mc_treewrapper_up.pi_IPCHI2_OWNPV,
            'K_ProbNNk': mc_treewrapper_up.K_ProbNNk,
            'pi_ProbNNpi': mc_treewrapper_up.pi_ProbNNpi
        })

for entry in mc_treewrapper_down.entry():
    # make sure the B is a B and the K is a K and that the selection is blind (200 MeV window around eta mass)
    # and the K prob is high (this is a strongly discriminating factor)
    if abs(mc_treewrapper_down.B_BKGCAT) == 30 and abs(mc_treewrapper_down.K_TRUEID) == 321 and abs(mc_treewrapper_up.diphoton_M - 550) < 100:
        treemaker.Fill({  # wants a dictionary of values
            'B_M': mc_treewrapper_down.B_M,
            'Kst_M': mc_treewrapper_down.Kst_M,
            'gamma0_P': mc_treewrapper_down.gamma0_P,
            'gamma1_P': mc_treewrapper_down.gamma1_P,
            'diphoton_M': mc_treewrapper_up.diphoton_M,
            'B_FD_OWNPV': mc_treewrapper_down.B_FD_OWNPV,
            'B_P': mc_treewrapper_down.B_P,
            'B_PT': mc_treewrapper_down.B_PT,
            'B_DIRA_OWNPV': mc_treewrapper_down.B_DIRA_OWNPV,
            'B_ENDVERTEX_CHI2': mc_treewrapper_down.B_ENDVERTEX_CHI2,
            'B_CONEP_100': mc_treewrapper_down.B_CONEP_100,
            'B_CONEMULT_100': mc_treewrapper_down.B_CONEMULT_100,
            'B_NC_IT_100': mc_treewrapper_down.B_NC_IT_100,
            'B_NEWVTXISODCHI2MASS': mc_treewrapper_down.B_NEWVTXISODCHI2MASS,
            'B_VTXISODCHI2MASSONETRACK': mc_treewrapper_down.B_VTXISODCHI2MASSONETRACK,
            'B_VTXISODCHI2MASSTWOTRACK': mc_treewrapper_down.B_VTXISODCHI2MASSTWOTRACK,
            'Kst_P': mc_treewrapper_down.Kst_P,
            'Kst_PT': mc_treewrapper_down.Kst_PT,
            'K_P': mc_treewrapper_down.K_P,
            'K_PT': mc_treewrapper_down.K_PT,
            'pi_P': mc_treewrapper_down.pi_P,
            'pi_PT': mc_treewrapper_down.pi_PT,
            'Kst_IPCHI2_OWNPV': mc_treewrapper_down.Kst_IPCHI2_OWNPV,
            'K_IPCHI2_OWNPV': mc_treewrapper_down.K_IPCHI2_OWNPV,
            'pi_IPCHI2_OWNPV': mc_treewrapper_down.pi_IPCHI2_OWNPV,
            'K_ProbNNk': mc_treewrapper_down.K_ProbNNk,
            'pi_ProbNNpi': mc_treewrapper_down.pi_ProbNNpi
        })
treemaker.close()

canvas3 = TCanvas()
that_tree = TreeWrapper('MC-blind.root', 'DecayTree')
# Draw the original B mass around its peak
that_tree.Draw('B_M', 'abs(B_M - 5280) < 1000')
canvas3.Modified()
canvas3.Update()

input("Press Enter to Exit...")
