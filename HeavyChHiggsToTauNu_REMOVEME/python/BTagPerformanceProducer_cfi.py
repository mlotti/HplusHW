import FWCore.ParameterSet.Config as cms
######################## for TTBar efficiency #####################################################################################
#BTagPerformanceESProducer_TTBARDISCRIMBTAGCSV = cms.ESProducer("BtagPerformanceESProducer",
                                                               # this is what it makes available
#                                                               ComponentName = cms.string('TTBARDISCRIMBTAGCSV'),
#                                                              # this is where it gets the payload from
#                                                               PayloadName = cms.string('BTagTTBARDISCRIMBTAGCSVtable_v8_offline'),
#                                                               WorkingPointName = cms.string('BTagTTBARDISCRIMBTAGCSVwp_v8_offline')
#
#)
######################## for MU+JETS btag SF WP #####################################################################################
BtagPerformanceESProducer_MUJETSWPBTAGCSVM = cms.ESProducer("BtagPerformanceESProducer",
                                                          # this is what it makes available
                                                          ComponentName = cms.string('MUJETSWPBTAGCSVM'),
                                                          # this is where it gets the payload from                                                
                                                          PayloadName = cms.string('BTagMUJETSWPBTAGCSVMtable_v8_offline'),
                                                          WorkingPointName = cms.string('BTagMUJETSWPBTAGCSVMwp_v8_offline')
                                                           )
######################## for MU+JETS mistag SF WP #####################################################################################
## BtagPerformanceESProducer_MISTAGCSVM = cms.ESProducer("BtagPerformanceESProducer",
##                                                        # this is what it makes availab
##                                                        ComponentName = cms.string('MISTAGCSVM'),
##                                                        # this is where it gets the payload from                                                
##                                                        PayloadName = cms.string('BTagMISTAGCSVMtable_v8_offline'),
##                                                        WorkingPointName = cms.string('BTagMISTAGCSVMwp_v8_offline')
##                                                        )
######################## for TTBar btag SF WP #####################################################################################
## BtagPerformanceESProducer_TTBARWPBTAGCSVM = cms.ESProducer("BtagPerformanceESProducer",
##                                                           # this is what it makes available
##                                                           ComponentName = cms.string('TTBARWPBTAGCSVM'),
##                                                           # this is where it gets the payload from                                                
##                                                           PayloadName = cms.string('BTagTTBARWPBTAGCSVMtable_v8_offline'),
##                                                           WorkingPointName = cms.string('BTagTTBARWPBTAGCSVMwp_v8_offline')
##                                                           )
