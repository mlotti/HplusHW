#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,RECO
#SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,HLT:GRun,RAW2DIGI,RECO
#NEVENTS=-1
NEVENTS=20
#SKIMFILE=file:skim.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_skim_v44_4_2/80448358a193f69c52fb3eaa57e02bff/skim_3984_1_ZFm.root

cmsDriver.py HiggsAnalysis/HeavyChHiggsToTauNu/python/tauEmbedding/PFEmbeddingSource_cff.py \
    -s $SEQUENCE \
    --no_exec \
    -n $NEVENTS \
    --conditions=$CONDITIONS \
    --process=EMBEDDING \
    --filein=$SKIMFILE \
    --fileout=embedded.root  \
    --python_filename=embed.py \
    --customise=HiggsAnalysis/HeavyChHiggsToTauNu/tauEmbedding/pf_customize.py
python embed.py

