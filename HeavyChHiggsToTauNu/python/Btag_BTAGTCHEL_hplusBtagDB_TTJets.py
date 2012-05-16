import FWCore.ParameterSet.Config as cms
BtagPerformanceESProducer_BTAGTCHEL_hplusBtagDB_TTJets = cms.ESProducer("BtagPerformanceESProducer",
# this is what it makes available
    ComponentName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets'),
# this is where it gets the payload from                                                
    PayloadName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_T'),
    WorkingPointName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_WP')
)
