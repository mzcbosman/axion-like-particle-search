from TreeWrapper import TreeWrapper
from TreeMaker import TreeMaker
from array import array
from ROOT import TFile, TMVA, TCanvas, TCut

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
# dataloader.AddVariable('B_CONEP_100',      'B_CONEP_100',      '', 'F')
# dataloader.AddVariable('B_CONEMULT_100',      'B_CONEMULT_100',      '', 'F')
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
dataloader.AddVariable('K_IPCHI2_OWNPV',      'K_IPCHI2_OWNPV',      '', 'F')
dataloader.AddVariable('pi_IPCHI2_OWNPV',      'pi_IPCHI2_OWNPV',      '', 'F')
dataloader.AddVariable('K_ProbNNk',      'K_ProbNNk',      '', 'F')
dataloader.AddVariable('pi_ProbNNpi',      'pi_ProbNNpi',      '', 'F')


# Add a signal and background sample
# MC as a signal proxy
sigfile = TFile('../mc-creator/MC-blind.root')
# upper mass sideband as background proxy
bkgfile = TFile('../data-creator/data-blind-sideband.root')
bkg2file = TFile('../data-creator/data-blind-full.root')

sigtree = sigfile.Get('DecayTree')
bkgtree = bkgfile.Get('DecayTree')
bkg2tree = bkg2file.Get('DecayTree')

# k fold 4 had the highest results
ii = 4

traincut = TCut('kClass != '+str(ii))
sigtestcut = TCut('kClass == '+str(ii))
bkgtestcut = TCut('B_M < 5800 && B_M > 5500')

dataloader.AddTree(sigtree, 'Signal', 1, traincut, 0)
dataloader.AddTree(sigtree, 'Signal', 1, sigtestcut, 1)
dataloader.AddTree(bkgtree, 'Background', 1, traincut, 0)
dataloader.AddTree(bkg2tree, 'Background', 1, bkgtestcut, 1)


# add the BDT method with an AdaBoost algorithm
bdtmethod = factory.BookMethod(dataloader, TMVA.Types.kBDT, 'BDT',
                               "!H:!V:NTrees=1000:MinNodeSize=1%:MaxDepth=4:BoostType=AdaBoost:AdaBoostBeta=0.6:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")

# Do the training
factory.OptimizeAllMethods("ROCIntegral", "FitGA")
# factory.OptimizeAllMethods("ROCIntegral","Minuit")

outfile.Close()

input("Press Enter to continue...")
