#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters
# 19.1.2012 M.Kortelainen CMSSW_4_4_2_patch9 Added tag for GenFilters
# 17.9.2012 M.Kortelainen CMSSW_4_4_4 Added tag for electron MVA ID
# 12.10.2012 M.Kortelainen CMSSW_5_3_5 MET filters
# 5.4.2013 M.Kortelainen CMSSW_5_3_9_patch2 Removed PileupJetID tag (it has been moved to ../checkoutTags.sh)
# 18.4.2013 M.Kortelainen CMSSW_5_3_9_patch2 Updated MET filters

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#A_Central_Filter_Package_RecoMET
cvs co -r V00-00-13 RecoMET/METFilters
cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V00-11-17 DPGAnalysis/SiStripTools


# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification
#
# The tag is checked out in the analysis checkoutTags (because of
# cut-based ID), but we can do the downloading of the xmls here.
#
# Downloads ~50 MB of xml, which compresses to ~8.5 MB with 'tar zcf'
if [ ! -e EGamma/EGammaAnalysisTools ]; then
    echo "ERROR: You should run HiggsAnalysis/HeavyChHiggsToTauNu/test/checkoutTags.sh first !"
    exit 1
fi
cd EGamma/EGammaAnalysisTools/data
rm -f *.xml # In case there are old files
cat download.url | xargs wget
cd ../../..

