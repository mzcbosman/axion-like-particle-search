from TreeWrapper import TreeWrapper
from TreeMaker import TreeMaker
from array import array
from ROOT import TFile, TMVA, TCanvas, TCut

bdt_treemaker = TreeMaker(
    'blind_data_withBDT.root',  # output file name
    'DecayTree',  # output tree name
    ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'diphoton_with_constraint_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
     'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
     'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
     'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi', 'kClass', 'BDT']  # list of branches
)

band_treemaker = TreeMaker(
    'blind_data_afterBDT.root',  # output file name
    'DecayTree',  # output tree name
    ['B_M', 'Kst_M', 'gamma0_P', 'gamma1_P', 'diphoton_M', 'diphoton_with_constraint_M', 'B_FD_OWNPV', 'B_P', 'B_PT', 'B_DIRA_OWNPV', 'B_ENDVERTEX_CHI2',
     'B_CONEP_100', 'B_CONEMULT_100', 'B_NC_IT_100', 'B_NEWVTXISODCHI2MASS', 'B_VTXISODCHI2MASSONETRACK',
     'B_VTXISODCHI2MASSTWOTRACK', 'Kst_P', 'Kst_PT', 'K_P', 'K_PT', 'pi_P', 'pi_PT', 'Kst_IPCHI2_OWNPV',
     'K_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV', 'K_ProbNNk', 'pi_ProbNNpi', 'kClass', 'BDT']  # list of branches
)


# loop over kfolds and give bdt for only the one that hasn't been trained on
for ii in range(10):

    # Make an output file for the diagnostic information/plots
    outfile = TFile('diagnostic.root', 'recreate')

    # this does the bulk of the work
    factory = TMVA.Factory('classifier', outfile,
                           '!V:!Silent:Color:DrawProgressBar')

    # Make a class to manage the data and add the variables we want to use
    dataloader = TMVA.DataLoader('classifier_trainingset')
    dataloader.AddVariable('B_FD_OWNPV',       'B_FD_OWNPV',       '', 'F')
    dataloader.AddVariable('B_P',              'B_P',              '', 'F')
    dataloader.AddVariable('B_PT',             'B_PT',             '', 'F')
    dataloader.AddVariable('B_DIRA_OWNPV',     'B_DIRA_OWNPV',     '', 'F')
    dataloader.AddVariable('B_ENDVERTEX_CHI2', 'B_ENDVERTEX_CHI2', '', 'F')
    # dataloader.AddVariable('B_CONEP_100',      'B_CONEP_100',      '', 'F')
    # dataloader.AddVariable('B_CONEMULT_100',
    #                        'B_CONEMULT_100',      '', 'F')
    # dataloader.AddVariable('B_NC_IT_100',      'B_NC_IT_100',      '', 'F')
    dataloader.AddVariable('B_NEWVTXISODCHI2MASS',
                           'B_NEWVTXISODCHI2MASS',      '', 'F')
    # dataloader.AddVariable('B_VTXISODCHI2MASSONETRACK',
    #                        'B_VTXISODCHI2MASSONETRACK',      '', 'F')
    # dataloader.AddVariable('B_VTXISODCHI2MASSTWOTRACK',
    #                        'B_VTXISODCHI2MASSTWOTRACK',      '', 'F')
    dataloader.AddVariable('Kst_P',      'Kst_P',      '', 'F')
    dataloader.AddVariable('Kst_PT',      'Kst_PT',      '', 'F')
    dataloader.AddVariable('K_P',      'K_P',      '', 'F')
    dataloader.AddVariable('K_PT',             'K_PT',             '', 'F')
    dataloader.AddVariable('pi_P',      'pi_P',      '', 'F')
    dataloader.AddVariable('pi_PT',            'pi_PT',            '', 'F')
    dataloader.AddVariable('Kst_IPCHI2_OWNPV',
                           'Kst_IPCHI2_OWNPV',      '', 'F')
    dataloader.AddVariable('K_IPCHI2_OWNPV',
                           'K_IPCHI2_OWNPV',      '', 'F')
    dataloader.AddVariable('pi_IPCHI2_OWNPV',
                           'pi_IPCHI2_OWNPV',      '', 'F')
    dataloader.AddVariable('K_ProbNNk',      'K_ProbNNk',      '', 'F')
    dataloader.AddVariable('pi_ProbNNpi',      'pi_ProbNNpi',      '', 'F')

    # Add a signal and background sample
    # MC as a signal proxy
    sigfile = TFile('../mc-creator/MC-blind.root')
    # upper mass sideband as background proxy
    bkgfile = TFile('../data-creator/data-blind-sideband.root')

    sigtree = sigfile.Get('DecayTree')
    bkgtree = bkgfile.Get('DecayTree')

    traincut = TCut('kClass != '+str(ii))
    testcut = TCut('kClass == '+str(ii))

    dataloader.AddTree(sigtree, 'Signal', 1, traincut, 0)
    dataloader.AddTree(sigtree, 'Signal', 1, testcut, 1)
    dataloader.AddTree(bkgtree, 'Background', 1, traincut, 0)
    dataloader.AddTree(bkgtree, 'Background', 1, testcut, 1)

    # add the BDT method with an AdaBoost algorithm
    bdtmethod = factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT',
                                   "!H:!V:NTrees=800:MinNodeSize=0.5%:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=200")

    # Do the training
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    outfile.Close()

    ###############################################################################
    #                                                                             #
    #                  Apply the trained BDT to a data sample                     #
    #                                                                             #
    ###############################################################################

    # create the reader for the BDT weights
    reader = TMVA.Reader('!Color:Silent')

    # Add the variables to the reader
    B_FD_OWNPV = array('f', [0.])
    B_P = array('f', [0.])
    B_PT = array('f', [0.])
    B_DIRA_OWNPV = array('f', [0.])
    B_ENDVERTEX_CHI2 = array('f', [0.])
    # B_CONEP_100 = array('f', [0.])
    # B_CONEMULT_100 = array('f', [0.])
    # B_NC_IT_100 = array('f', [0.])
    B_NEWVTXISODCHI2MASS = array('f', [0.])
    # B_VTXISODCHI2MASSONETRACK = array('f', [0.])
    # B_VTXISODCHI2MASSTWOTRACK = array('f', [0.])
    Kst_P = array('f', [0.])
    Kst_PT = array('f', [0.])
    K_P = array('f', [0.])
    K_PT = array('f', [0.])
    pi_P = array('f', [0.])
    pi_PT = array('f', [0.])
    Kst_IPCHI2_OWNPV = array('f', [0.])
    K_IPCHI2_OWNPV = array('f', [0.])
    pi_IPCHI2_OWNPV = array('f', [0.])
    K_ProbNNk = array('f', [0.])
    pi_ProbNNpi = array('f', [0.])

    reader.AddVariable('B_FD_OWNPV',       B_FD_OWNPV)
    reader.AddVariable('B_P',              B_P)
    reader.AddVariable('B_PT',             B_PT)
    reader.AddVariable('B_DIRA_OWNPV',     B_DIRA_OWNPV)
    reader.AddVariable('B_ENDVERTEX_CHI2', B_ENDVERTEX_CHI2)
    # reader.AddVariable('B_CONEP_100',     B_CONEP_100)
    # reader.AddVariable('B_CONEMULT_100',      B_CONEMULT_100)
    # reader.AddVariable('B_NC_IT_100',      B_NC_IT_100)
    reader.AddVariable('B_NEWVTXISODCHI2MASS',      B_NEWVTXISODCHI2MASS)
    # reader.AddVariable('B_VTXISODCHI2MASSONETRACK',
    #                    B_VTXISODCHI2MASSONETRACK)
    # reader.AddVariable('B_VTXISODCHI2MASSTWOTRACK',
    #                    B_VTXISODCHI2MASSTWOTRACK)
    reader.AddVariable('Kst_P',      Kst_P)
    reader.AddVariable('Kst_PT',      Kst_PT)
    reader.AddVariable('K_P',      K_P)
    reader.AddVariable('K_PT',             K_PT)
    reader.AddVariable('pi_P',      pi_P)
    reader.AddVariable('pi_PT',           pi_PT)
    reader.AddVariable('Kst_IPCHI2_OWNPV',      Kst_IPCHI2_OWNPV)
    reader.AddVariable('K_IPCHI2_OWNPV',      K_IPCHI2_OWNPV)
    reader.AddVariable('pi_IPCHI2_OWNPV',      pi_IPCHI2_OWNPV)
    reader.AddVariable('K_ProbNNk',      K_ProbNNk)
    reader.AddVariable('pi_ProbNNpi',      pi_ProbNNpi)

    # Tell the reader where to find the weights
    reader.BookMVA(
        'classifier', 'classifier_trainingset/weights/classifier_BDT.weights.xml')

    # now we can apply the BDT to the data

    bdt_treewrapper = TreeWrapper(
        "../data-creator/data-blind-full.root", "DecayTree")
    for entry in bdt_treewrapper.entry():
        if bdt_treewrapper.kClass == ii:
            # give the reader the data it needs
            B_FD_OWNPV[0] = bdt_treewrapper.B_FD_OWNPV
            B_P[0] = bdt_treewrapper.B_P
            B_PT[0] = bdt_treewrapper.B_PT
            B_DIRA_OWNPV[0] = bdt_treewrapper.B_DIRA_OWNPV
            B_ENDVERTEX_CHI2[0] = bdt_treewrapper.B_ENDVERTEX_CHI2
            # B_CONEP_100[0] = bdt_treewrapper.B_CONEP_100
            # B_CONEMULT_100[0] = bdt_treewrapper.B_CONEMULT_100
            # B_NC_IT_100[0] = bdt_treewrapper.B_NC_IT_100
            B_NEWVTXISODCHI2MASS[0] = bdt_treewrapper.B_NEWVTXISODCHI2MASS
            # B_VTXISODCHI2MASSONETRACK[0] = bdt_treewrapper.B_VTXISODCHI2MASSONETRACK
            # B_VTXISODCHI2MASSTWOTRACK[0] = bdt_treewrapper.B_VTXISODCHI2MASSTWOTRACK
            Kst_P[0] = bdt_treewrapper.Kst_P
            Kst_PT[0] = bdt_treewrapper.Kst_PT
            K_P[0] = bdt_treewrapper.K_P
            K_PT[0] = bdt_treewrapper.K_PT
            pi_P[0] = bdt_treewrapper.pi_P
            pi_PT[0] = bdt_treewrapper.pi_PT
            Kst_IPCHI2_OWNPV[0] = bdt_treewrapper.Kst_IPCHI2_OWNPV
            K_IPCHI2_OWNPV[0] = bdt_treewrapper.K_IPCHI2_OWNPV
            pi_IPCHI2_OWNPV[0] = bdt_treewrapper.pi_IPCHI2_OWNPV
            K_ProbNNk[0] = bdt_treewrapper.K_ProbNNk
            pi_ProbNNpi[0] = bdt_treewrapper.pi_ProbNNpi

            bdt_treemaker.Fill({
                "B_M": bdt_treewrapper.B_M,
                "Kst_M": bdt_treewrapper.Kst_M,
                "gamma0_P": bdt_treewrapper.gamma0_P,
                "gamma1_P": bdt_treewrapper.gamma1_P,
                "diphoton_M": bdt_treewrapper.diphoton_M,
                "diphoton_with_constraint_M": bdt_treewrapper.diphoton_with_constraint_M,
                "B_FD_OWNPV": bdt_treewrapper.B_FD_OWNPV,
                "B_P": bdt_treewrapper.B_P,
                "B_PT": bdt_treewrapper.B_PT,
                "B_DIRA_OWNPV": bdt_treewrapper.B_DIRA_OWNPV,
                "B_ENDVERTEX_CHI2": bdt_treewrapper.B_ENDVERTEX_CHI2,
                "B_CONEP_100": bdt_treewrapper.B_CONEP_100,
                "B_CONEMULT_100": bdt_treewrapper.B_CONEMULT_100,
                "B_NC_IT_100": bdt_treewrapper.B_NC_IT_100,
                "B_NEWVTXISODCHI2MASS": bdt_treewrapper.B_NEWVTXISODCHI2MASS,
                "B_VTXISODCHI2MASSONETRACK": bdt_treewrapper.B_VTXISODCHI2MASSONETRACK,
                "B_VTXISODCHI2MASSTWOTRACK": bdt_treewrapper.B_VTXISODCHI2MASSTWOTRACK,
                "Kst_P": bdt_treewrapper.Kst_P,
                "Kst_PT": bdt_treewrapper.Kst_PT,
                "K_P": bdt_treewrapper.K_P,
                "K_PT": bdt_treewrapper.K_PT,
                "pi_P": bdt_treewrapper.pi_P,
                "pi_PT": bdt_treewrapper.pi_PT,
                "Kst_IPCHI2_OWNPV": bdt_treewrapper.Kst_IPCHI2_OWNPV,
                "K_IPCHI2_OWNPV": bdt_treewrapper.K_IPCHI2_OWNPV,
                "pi_IPCHI2_OWNPV": bdt_treewrapper.pi_IPCHI2_OWNPV,
                "K_ProbNNk": bdt_treewrapper.K_ProbNNk,
                "pi_ProbNNpi": bdt_treewrapper.pi_ProbNNpi,
                # the output of the classifier
                "BDT": reader.EvaluateMVA('classifier')
            })

bdt_treemaker.close()


band_treewrapper = TreeWrapper(
    "blind_data_withBDT.root", "DecayTree")
for entry in band_treewrapper.entry():
    if band_treewrapper.BDT > 0 and 5000 <= band_treewrapper.B_M < 6500:
        band_treemaker.Fill({
            "B_M": band_treewrapper.B_M,
            "Kst_M": band_treewrapper.Kst_M,
            "gamma0_P": band_treewrapper.gamma0_P,
            "gamma1_P": band_treewrapper.gamma1_P,
            "diphoton_M": band_treewrapper.diphoton_M,
            "diphoton_with_constraint_M": band_treewrapper.diphoton_with_constraint_M,
            "B_FD_OWNPV": band_treewrapper.B_FD_OWNPV,
            "B_P": band_treewrapper.B_P,
            "B_PT": band_treewrapper.B_PT,
            "B_DIRA_OWNPV": band_treewrapper.B_DIRA_OWNPV,
            "B_ENDVERTEX_CHI2": band_treewrapper.B_ENDVERTEX_CHI2,
            "B_CONEP_100": band_treewrapper.B_CONEP_100,
            "B_CONEMULT_100": band_treewrapper.B_CONEMULT_100,
            "B_NC_IT_100": band_treewrapper.B_NC_IT_100,
            "B_NEWVTXISODCHI2MASS": band_treewrapper.B_NEWVTXISODCHI2MASS,
            "B_VTXISODCHI2MASSONETRACK": band_treewrapper.B_VTXISODCHI2MASSONETRACK,
            "B_VTXISODCHI2MASSTWOTRACK": band_treewrapper.B_VTXISODCHI2MASSTWOTRACK,
            "Kst_P": band_treewrapper.Kst_P,
            "Kst_PT": band_treewrapper.Kst_PT,
            "K_P": band_treewrapper.K_P,
            "K_PT": band_treewrapper.K_PT,
            "pi_P": band_treewrapper.pi_P,
            "pi_PT": band_treewrapper.pi_PT,
            "Kst_IPCHI2_OWNPV": band_treewrapper.Kst_IPCHI2_OWNPV,
            "K_IPCHI2_OWNPV": band_treewrapper.K_IPCHI2_OWNPV,
            "pi_IPCHI2_OWNPV": band_treewrapper.pi_IPCHI2_OWNPV,
            "K_ProbNNk": band_treewrapper.K_ProbNNk,
            "pi_ProbNNpi": band_treewrapper.pi_ProbNNpi,
            "BDT": band_treewrapper.BDT
        })

band_treemaker.close()

canvas = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "abs(B_M - 5300) < 300",  "")  # no BDT cut
tree.Draw("B_M", "abs(B_M - 5300) < 300 && BDT >  0",
          "same")  # A loose BDT cut
tree.Draw("B_M", "abs(B_M - 5300) < 300 && BDT > 0.2",
          "same")  # A tight BDT cut
canvas.Modified()
canvas.Update()

canvas2 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "",  "")  # no BDT cut
canvas2.Modified()
canvas2.Update()

canvas3 = TCanvas()
tree = TreeWrapper("blind_data_withBDT.root", "DecayTree")
tree.Draw("B_M", "BDT >  0",
          "")  # A loose BDT cut
canvas3.Modified()
canvas3.Update()

###############################################################################
#                                                                             #
#                        Open the diagnostics file                            #
#                                                                             #
###############################################################################

TMVA.TMVAGui('diagnostic.root')

input("Press ENTER to exit")
