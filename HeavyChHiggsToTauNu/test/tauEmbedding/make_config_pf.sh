#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,HLT:GRun,RAW2DIGI,RECO
#NEVENTS=-1
NEVENTS=10
#SKIMFILE=file:skim.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_2_X/TTJets_TuneZ2_Summer11_1/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13_2/6ce8de2c5b6c0c9ed414998577b7e28d/skim_982_1_xgs.root

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

