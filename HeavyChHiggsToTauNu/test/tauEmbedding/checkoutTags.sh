#!/bin/sh

set -e

# Tag list modification history
# 10.11.2010/M.Kortelainen CMSSW_3_8_6
# 11.11.2010/M.Kortelainen the tag is needed to get the code to compile, moved one level up
# 12.11.2010/M.Kortelainen CMSSW_3_8_6 workaround added
# 17.11.2010/M.Kortelainen CMSSW_3_8_6 patch for OscarProducer
# 23.11.2010/M.Kortelainen CMSSW_3_8_6 updated MCEmbeddingTools tag
# 1.2.2011/M.Kortelainen CMSSW_3_9_7 Updated MCEmbeddingTools tag
# 22.3.2011/M.Kortelainen CMSSW_3_9_7 Added MuonAnalysis tag

cvs co -r V00-00-09 TauAnalysis/MCEmbeddingTools
cvs co -r V01-13-00 MuonAnalysis/MuonAssociators

# We have to add protection for multiple runs in OscarProducer
addpkg SimG4Core/Application
patch -p0 < HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/OscarProducer.patch