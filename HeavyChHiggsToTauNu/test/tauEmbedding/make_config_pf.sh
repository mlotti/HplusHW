#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,HLT:GRun
#NEVENTS=-1
NEVENTS=2
SKIMFILE=file:skim.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10/b3c16f1ee121445edb6d9b12e0772d8e/skim_108_1_LI4.root

#HLTFILE=file:embedded_HLT.root
HLTFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_generation_v10_pt40/407f41e7ada5cc209b7b3dca1b2a4528/embedded_HLT_14_1_NXY.root

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