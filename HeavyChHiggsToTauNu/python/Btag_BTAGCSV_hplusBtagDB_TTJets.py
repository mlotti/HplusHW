##import FWCore.ParameterSet.Config as cms
## BtagPerformanceESProducer_BTAGTCHEL_hplusBtagDB_TTJets = cms.ESProducer("BtagPerformanceESProducer",
## # this is what it makes available
##     ComponentName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets'),
## # this is where it gets the payload from                                                
##     PayloadName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_T'),
##     WorkingPointName = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_WP')
## )
import FWCore.ParameterSet.Config as cms
from CondCore.DBCommon.CondDBCommon_cfi import *
######## for TTBar efficiency ##########################################################################################################################
#PoolDBESSourcebtagTtbarDiscrim0612 = cms.ESSource("PoolDBESSource",
#                                                  CondDBCommon,
#                                                  toGet = cms.VPSet( cms.PSet( record = cms.string('PerformancePayloadRecord'),
#                                                                               tag = cms.string('BTagTTBARDISCRIMBTAGCSVtable_v8_offline'),
#                                                                               label = cms.untracked.string('BTagTTBARDISCRIMBTAGCSVtable_v8_offline')
#                                                                               ),
#                                                                     cms.PSet( record = cms.string('PerformanceWPRecord'),
#                                                                               tag = cms.string('BTagTTBARDISCRIMBTAGCSVwp_v8_offline'),
#                                                                               label = cms.untracked.string('BTagTTBARDISCRIMBTAGCSVwp_v8_offline')
#                                                                               ),
#                                                                     )
#                                                  )
#PoolDBESSourcebtagTtbarDiscrim0612.connect = 'frontier://FrontierProd/CMS_COND_PAT_000'
######## for TTBar btag SF ##########################################################################################################################
#PoolDBESSourcebtagTtbarWp0612= cms.ESSource("PoolDBESSource",
#                                                  CondDBCommon,
#                                                  toGet = cms.VPSet( cms.PSet( record = cms.string('PerformancePayloadRecord'),
#                                                                               tag = cms.string('BTagTTBARWPBTAGCSVMtable_v8_offline'),
#                                                                               label = cms.untracked.string('BTagTTBARWPBTAGCSVMtable_v8_offline')
#                                                                               ),
#                                                                     cms.PSet( record = cms.string('PerformanceWPRecord'),
#                                                                               tag = cms.string('BTagTTBARWPBTAGCSVMwp_v8_offline'),
#                                                                               label = cms.untracked.string('BTagTTBARWPBTAGCSVMwp_v8_offline')
#                                                                               ),
#                                                                     )
#                                                  )
#PoolDBESSourcebtagTtbarWp0612.connect = 'frontier://FrontierProd/CMS_COND_PAT_000'
######## for MU+jets btag SF  ##########################################################################################################################
PoolDBESSourcebtagMuJetsWp0612 = cms.ESSource("PoolDBESSource",
                                                  CondDBCommon,
                                                  toGet = cms.VPSet( cms.PSet( record = cms.string('PerformancePayloadRecord'),
                                                                               tag = cms.string('BTagMUJETSWPBTAGCSVMtable_v8_offline'), 
                                                                               label = cms.untracked.string('BTagMUJETSWPBTAGCSVMtable_v8_offline')
                                                                               ),
                                                                     cms.PSet( record = cms.string('PerformanceWPRecord'),
                                                                               tag = cms.string('BTagMUJETSWPBTAGCSVMwp_v8_offline'),
                                                                               label = cms.untracked.string('BTagMUJETSWPBTAGCSVMwp_v8_offline')
                                                                               ),
                                                                     )
                                                  )
PoolDBESSourcebtagMuJetsWp0612.connect = 'frontier://FrontierProd/CMS_COND_PAT_000'
######## for MU+jets mistag SF  ##########################################################################################################################
## PoolDBESSourcebtagMistag0612 = cms.ESSource("PoolDBESSource",
##                                CondDBCommon,
##                                toGet = cms.VPSet( cms.PSet(record = cms.string('PerformancePayloadRecord'),
##                                                            tag = cms.string('BTagMISTAGCSVMtable_v8_offline'),
##                                                            label = cms.untracked.string('BTagMISTAGCSVMtable_v8_offline')
##                                                            ),
##                                                   cms.PSet(record = cms.string('PerformanceWPRecord'),
##                                                            tag = cms.string('BTagMISTAGCSVMwp_v8_offline'),
##                                                            label = cms.untracked.string('BTagMISTAGCSVMwp_v8_offline')
##                                                            ),
##                                                   )
##                                             )
#PoolDBESSourcebtagMistag0612.connect = 'frontier://FrontierProd/CMS_COND_PAT_000'
