import FWCore.ParameterSet.Config as cms

from CondCore.DBCommon.CondDBCommon_cfi import *

#PoolDBESSource = cms.ESSource("PoolDBESSource",
#                              CondDBCommon,
#                              toGet = cms.VPSet(
#    #
#    # working points
#    #
#    cms.PSet(
#    record = cms.string('PerformancePayloadRecord'),
#    tag = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_T'),
#    label = cms.untracked.string('BTAGTCHEL_hplusBtagDB_TTJets_T')
#    ),
#    cms.PSet(
#    record = cms.string('PerformanceWPRecord'),
#    tag = cms.string('BTAGTCHEL_hplusBtagDB_TTJets_WP'),
#    label = cms.untracked.string('BTAGTCHEL_hplusBtagDB_TTJets_WP')
#    ),
#))

                              
PoolDBESSourcebtagMuJetsWp = cms.ESSource("PoolDBESSource",
                                              CondDBCommon,
                                              toGet = cms.VPSet( cms.PSet( record = cms.string('PerformancePayloadRecord'),
    									   tag = cms.string('PerformancePayloadFromBinnedTFormula_MUJETSWPBTAGCSVL_v9_offline'),
     								           label = cms.untracked.string('MUJETSWPBTAGCSVL_T')
                                                                         ),
    								 cms.PSet( record = cms.string('PerformanceWPRecord'),
    									   tag = cms.string('PerformanceWorkingPoint_MUJETSWPBTAGCSVL_v9_offline'),
           								   label = cms.untracked.string('MUJETSWPBTAGCSVL_WP')
                                                                         ),
    								 cms.PSet( record = cms.string('PerformancePayloadRecord'),
    									   tag = cms.string('PerformancePayloadFromBinnedTFormula_MUJETSWPBTAGCSVM_v9_offline'),
    									   label = cms.untracked.string('MUJETSWPBTAGCSVM_T')
    									 ),
    								 cms.PSet( record = cms.string('PerformanceWPRecord'),
    									   tag = cms.string('PerformanceWorkingPoint_MUJETSWPBTAGCSVM_v9_offline'),
    									   label = cms.untracked.string('MUJETSWPBTAGCSVM_WP')
    									 ), 
    								 cms.PSet( record = cms.string('PerformancePayloadRecord'),
    									   tag = cms.string('PerformancePayloadFromBinnedTFormula_MUJETSWPBTAGCSVT_v9_offline'),
   									   label = cms.untracked.string('MUJETSWPBTAGCSVT_T')
   									 ),
    								 cms.PSet( record = cms.string('PerformanceWPRecord'),
    									   tag = cms.string('PerformanceWorkingPoint_MUJETSWPBTAGCSVT_v9_offline'),
    									   label = cms.untracked.string('MUJETSWPBTAGCSVT_WP')
    									 ),
                           
 								 )
 					 )                            
PoolDBESSourcebtagMuJetsWp.connect = 'frontier://FrontierProd/CMS_COND_PAT_000'
