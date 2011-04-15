#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,HLT:GRun
#NEVENTS=-1
NEVENTS=2
SKIMFILE=file:skim.root
#SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2/52e54222a22093cabccf53a197393901/skim_11_1_Ip8.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/Mu_146240-147116/Mu/Run2010B_PromptReco_v2_AOD_tauembedding_skim_v2/df8d5a0675762f7704edd4730bf7a6a7/skim_9_1_GGa.root

HLTFILE=file:embedded_HLT.root
#HLTFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/local_Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2_52e54222a22093cabccf53a197393901_USER_tauembedding_generation_v2/30de4d1810b82a43ef34b86cea04d93e/embedded_HLT_9_1_Q1C.root
#HLTFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/Mu_146240-147116/Mu/local-Run2010B_PromptReco_v2_AOD_tauembedding_generation_v2/82f01f8276126324da0436a1c37f3326/embedded_HLT_1_1_Djg.root

cmsDriver.py HiggsAnalysis/HeavyChHiggsToTauNu/python/tauEmbedding/PFEmbeddingSource_cff.py \
    -s $SEQUENCE \
    --no_exec \
    -n $NEVENTS \
    --conditions=$CONDITIONS \
    --process=EMBEDDINGHLT \
    --filein=$SKIMFILE \
    --fileout=embedded_HLT.root  \
    --python_filename=embed_HLT.py \
    --customise=HiggsAnalysis/HeavyChHiggsToTauNu/tauEmbedding/pf_01_customize_HLT.py
python embed_HLT.py

cmsDriver.py \
    -s RAW2DIGI,RECO \
    --no_exec \
    -n $NEVENTS \
    --conditions=${CONDITIONS} \
    --process=EMBEDDINGRECO \
    --filein=$HLTFILE \
    --fileout=embedded_RECO.root \
    --python_filename=embed_RECO.py \
    --customise=HiggsAnalysis/HeavyChHiggsToTauNu/tauEmbedding/pf_02_customize_Simulation.py
python embed_RECO.py