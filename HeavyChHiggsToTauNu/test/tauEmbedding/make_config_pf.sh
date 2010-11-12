#!/bin/sh

CONDITIONS=auto:startup
SEQUENCE=GEN:ProductionFilterSequence,SIM,DIGI,L1,DIGI2RAW,HLT:GRun
#SEQUENCE=GEN:ProductionFilterSequence
#NEVENTS=-1
NEVENTS=50
SKIMFILE=file:skim.root
SKIMFILE=/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2/52e54222a22093cabccf53a197393901/skim_11_1_Ip8.root


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
    --filein=file:embedded_HLT.root \
    --fileout=embedded_RECO.root \
    --python_filename=embed_RECO.py \
    --customise=HiggsAnalysis/HeavyChHiggsToTauNu/tauEmbedding/pf_02_customize_Simulation.py
python embed_RECO.py