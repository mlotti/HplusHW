import FWCore.ParameterSet.Config as cms

from CondCore.DBCommon.CondDBCommon_cfi import *

PoolDBESSource = cms.ESSource("PoolDBESSource",
                              CondDBCommon,
                              toGet = cms.VPSet(
    #
    # working points
    #
    cms.PSet(
    record = cms.string('PerformancePayloadRecord'),
    tag = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_T'),
    label = cms.untracked.string('BTAGTCHEL_hplusBtagDB_TTJets_T')
    ),
    cms.PSet(
    record = cms.string('PerformanceWPRecord'),
    tag = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_WP'),
    label = cms.untracked.string('BTAGTCHEL_hplusBtagDB_TTJets_WP')
    ),
))

                              
                              
                              
