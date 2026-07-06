from TreeWrapper import TreeWrapper
from TreeMaker import TreeMaker
from array import array
from ROOT import TFile, TMVA, TCanvas

# Make an output file for the diagnostic information/plots
outfile = TFile('diagnostic.root', 'recreate')

# this does the bulk of the work
factory = TMVA.Factory('classifier', outfile,
                       'Transformations=I;D;P;G,D:AnalysisType=Classification')

# Make a class to manage the data and add the variables we want to use
dataloader = TMVA.DataLoader('classifier_trainingset')
dataloader.AddVariable('B_FD_OWNPV',       'B_FD_OWNPV',       '', 'F')
dataloader.AddVariable('B_P',              'B_P',              '', 'F')
dataloader.AddVariable('B_PT',             'B_PT',             '', 'F')
dataloader.AddVariable('B_DIRA_OWNPV',     'B_DIRA_OWNPV',     '', 'F')
dataloader.AddVariable('B_ENDVERTEX_CHI2', 'B_ENDVERTEX_CHI2', '', 'F')
dataloader.AddVariable('B_CONEP_100',      'B_CONEP_100',      '', 'F')
dataloader.AddVariable('B_CONEMULT_100',      'B_CONEMULT_100',      '', 'F')
dataloader.AddVariable('B_NC_IT_100',      'B_NC_IT_100',      '', 'F')
dataloader.AddVariable('B_NEWVTXISODCHI2MASS',
                       'B_NEWVTXISODCHI2MASS',      '', 'F')
dataloader.AddVariable('B_VTXISODCHI2MASSONETRACK',
                       'B_VTXISODCHI2MASSONETRACK',      '', 'F')
dataloader.AddVariable('B_VTXISODCHI2MASSTWOTRACK',
                       'B_VTXISODCHI2MASSTWOTRACK',      '', 'F')
dataloader.AddVariable('Kst_P',      'Kst_P',      '', 'F')
dataloader.AddVariable('Kst_PT',      'Kst_PT',      '', 'F')
dataloader.AddVariable('K_P',      'K_P',      '', 'F')
dataloader.AddVariable('K_PT',             'K_PT',             '', 'F')
dataloader.AddVariable('pi_P',      'pi_P',      '', 'F')
dataloader.AddVariable('pi_PT',            'pi_PT',            '', 'F')
dataloader.AddVariable('Kst_IPCHI2_OWNPV',
                       'Kst_IPCHI2_OWNPV',      '', 'F')
dataloader.AddVariable('K_IPCHI2_OWNPV',      'K_IPCHI2_OWNPV',      '', 'F')
dataloader.AddVariable('pi_IPCHI2_OWNPV',      'pi_IPCHI2_OWNPV',      '', 'F')
dataloader.AddVariable('K_ProbNNk',      'K_ProbNNk',      '', 'F')
dataloader.AddVariable('pi_ProbNNpi',      'pi_ProbNNpi',      '', 'F')


# Add a signal and background sample
# MC as a signal proxy
sigfile = TFile('../mc-reduced-creator/MC-reduced.root')
# upper mass sideband as background proxy
bkgfile = TFile('../data-reduced-creator/data-reduced-sideband.root')

sigtree = sigfile.Get('DecayTree')
bkgtree = bkgfile.Get('DecayTree')

dataloader.AddSignalTree(sigtree)
dataloader.AddBackgroundTree(bkgtree)


# add the BDT method with an AdaBoost algorithm
bdtmethod = factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT',
                               "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")

# Do the training
factory.OptimizeAllMethods("ROCIntegral", "FitGA")
# factory.OptimizeAllMethods("ROCIntegral","Minuit")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

outfile.Close()

input("Press Enter to continue...")
