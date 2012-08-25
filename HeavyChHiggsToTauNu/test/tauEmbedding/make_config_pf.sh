#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,RECO
#SEQUENCE=GEN,SIM,DIGI,L1,DIGI2RAW,HLT:GRun,RAW2DIGI,RECO
#NEVENTS=-1
NEVENTS=10
#SKIMFILE=file:skim.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_skim_v44_1_TTJets_TuneZ2_Fall11//2f6341f5a210122b891e378fe7516bcf/skim_1007_1_IiS.root

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

