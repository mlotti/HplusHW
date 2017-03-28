import FWCore.ParameterSet.Config as cms

# How to use:
# - Import this module
# - Call produceCustomisations just before cms.Path
# - Add process.CustomisationsSequence to the cms.Path

def produceCustomisations(process,isData):
    process.CustomisationsSequence = cms.Sequence()
#    reproduceJEC(process)
#    reproduceElectronID(process)
    reproduceMETNoiseFilters(process)
    reproduceMET(process,isData)
    reproduceJEC(process)
    print "=== Customisations done"

# ===== Reproduce jet collections with the latest JEC =====
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrPatJets
def reproduceJEC(process):
    print "=== Customisation: reproducing jet collections with latest JEC"
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process,
#        jetSource = cms.InputTag('slimmedJets'),
        jetSource = cms.InputTag('cleanedPatJets'),
        labelName = 'UpdatedJEC',
        jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')  # Do not forget 'L2L3Residual' on data!
    )
#    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
#    # PF AK4CHS jets
#    if not hasattr(process, "JECpayloadAK4PFchs"):
#        raise Exception("Error: Could not access process.JECpayloadAK4PFchs! Please load Jet_cfi.py before calling customizations")
#    process.patJetCorrFactorsReapplyJECAK4CHS = patJetCorrFactorsUpdated.clone(
#      src = cms.InputTag("slimmedJets"),
#      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
#      payload = process.JECpayloadAK4PFchs.payload,  # Set in Jet_cfi.py
#    ) 
#    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
#    process.patJetsReapplyJECAK4CHS = patJetsUpdated.clone(
#      jetSource = cms.InputTag("slimmedJets"),
#      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4CHS"))
#    )
#    # PUPPI jets
#    updateJetCollection(
#        process,
#        jetSource = cms.InputTag('slimmedJetsPuppi'),
#        labelName = 'UpdatedJECPuppi',
#        jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None')  # Do not$
#    )
#    if not hasattr(process, "JECpayloadAK4PFPuppi"):
#        raise Exception("Error: Could not access process.JECpayloadAK4PFPuppi! Please load Jet_cfi.py before calling customizations")
#    process.patJetCorrFactorsReapplyJECPuppi = patJetCorrFactorsUpdated.clone(
#      src = cms.InputTag("slimmedJetsPuppi"),
#      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
#      payload = process.JECpayloadAK4PFPuppi.payload,  # Set in Jet_cfi.py
#    )
#    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
#    process.patJetsReapplyJECPuppi = patJetsUpdated.clone(
#      jetSource = cms.InputTag("slimmedJetsPuppi"), 
#      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECPuppi"))
#    )
    #process.reapplyJEC = cms.Sequence(process.patJetCorrFactorsReapplyJECAK4CHS +
    #                                  process.patJetsReapplyJECAK4CHS +
    #                                  process.patJetCorrFactorsReapplyJECPuppi +
    #                                  process.patJetsReapplyJECPuppi)
#    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECAK4CHS
#    process.CustomisationsSequence += process.patJetsReapplyJECAK4CHS
#    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECPuppi
#    process.CustomisationsSequence += process.patJetsReapplyJECPuppi
    process.CustomisationsSequence += process.patJetCorrFactorsUpdatedJEC
    process.CustomisationsSequence += process.updatedPatJetsUpdatedJEC
#    process.CustomisationsSequence += process.patJetCorrFactorsUpdatedJECPuppi
#    process.CustomisationsSequence += process.updatedPatJetsUpdatedJECPuppi


# ===== Set up electron ID (VID framework) =====
# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
def reproduceElectronID(process):
    print "=== Customisation: reproducing electron ID discriminators"
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    # define which IDs we want to produce and add them to the VID producer
    for idmod in ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff']:
        setupAllVIDIdsInModule(process, idmod, setupVIDElectronSelection)
    process.CustomisationsSequence += process.egmGsfElectronIDSequence

# ===== Set up HBHE noise filter =====
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
def reproduceMETNoiseFilters(process):
    print "=== Customisation: reproducing HBHE noise filter"
    process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
    process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)
    process.HBHENoiseFilterResultProducer.IgnoreTS4TS5ifJetInLowBVRegion=cms.bool(False)
    process.HBHENoiseFilterResultProducer.defaultDecision = cms.string("HBHENoiseFilterResultRun2Loose")

    process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
    process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
    process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadPFMuonFilter.taggingMode   = cms.bool(True)

    process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
    process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
    process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
    process.BadChargedCandidateFilter.taggingMode   = cms.bool(True)

    # Do not apply EDfilters for HBHE noise, the discriminators for them are saved into the ttree
    process.CustomisationsSequence += process.HBHENoiseFilterResultProducer
    process.CustomisationsSequence += process.BadPFMuonFilter
    process.CustomisationsSequence += process.BadChargedCandidateFilter

# ===== Set up MET uncertainties =====
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#A_tool_to_help_you_calculate_MET
def reproduceMET(process,isdata):

    from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup
    import os

    # https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
    if isdata:
#      era="Spring16_25nsV6_DATA"
       era="Summer16_23Sep2016AllV4_DATA"
    else:
#      era="Spring16_25nsV6_MC"
      era="Summer16_23Sep2016V4_MC"

    # https://github.com/cms-jet/JRDatabase/tree/master/SQLiteFiles
#    jerera="Spring16_25nsV6"
    jerera="Spring16_25nsV10"

##___________________________External JEC file________________________________||
 
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
#                               connect = cms.string("sqlite:PhysicsTools/PatUtils/data/"+era+".db"),
                               connect = cms.string("sqlite:"+era+"_JEC.db"),
                               toGet =  cms.VPSet(
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
                label= cms.untracked.string("AK4PF")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),  
                label= cms.untracked.string("AK4PFchs")
                ),
            cms.PSet(record  = cms.string("JetCorrectionsRecord"),
                tag     = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFPuppi"),
                label   = cms.untracked.string("AK4PFPuppi")
                ),
            )
                               )
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')

##___________________________External JER file________________________________||
    
    process.jer = cms.ESSource("PoolDBESSource",CondDBSetup,
#                               connect = cms.string("sqlite:PhysicsTools/PatUtils/data/JER/"+jerera+"_MC.db"),
                               connect = cms.string("sqlite:"+jerera+"_MC_JER.db"),
                               toGet =  cms.VPSet(
        #######
        ### read the PFchs  

        cms.PSet(
          record = cms.string('JetResolutionRcd'),
          tag    = cms.string('JR_'+jerera+'_MC_PtResolution_AK4PFchs'),
          label  = cms.untracked.string('AK4PFchs_pt')
          ),
        cms.PSet(
          record = cms.string("JetResolutionRcd"),
          tag    = cms.string('JR_'+jerera+'_MC_PhiResolution_AK4PFchs'),
          label  = cms.untracked.string("AK4PFchs_phi")
          ),
        cms.PSet( 
          record = cms.string('JetResolutionScaleFactorRcd'),
          tag    = cms.string('JR_'+jerera+'_MC_SF_AK4PFchs'),
          label  = cms.untracked.string('AK4PFchs')
          ),
                  
        #######
        ### read the Puppi JER

#        cms.PSet( 
#          record = cms.string('JetResolutionRcd'),
#          tag    = cms.string('JR_'+jerera+'_MC_PtResolution_AK4PFPuppi'),
#          label  = cms.untracked.string('AK4PFPuppi_pt')
#          ),
#        cms.PSet(
#          record = cms.string("JetResolutionRcd"),
#          tag = cms.string('JR_'+jerera+'_MC_PhiResolution_AK4PFPuppi'),
#          label= cms.untracked.string("AK4PFPuppi_phi")
#          ),
#        cms.PSet(
#          record = cms.string('JetResolutionScaleFactorRcd'),
#          tag    = cms.string('JR_'+jerera+'_MC_SF_AK4PFPuppi'),
#          label  = cms.untracked.string('AK4PFPuppi')
#          ),
        ) 
    )
          
    process.es_prefer_jer = cms.ESPrefer("PoolDBESSource",'jer')

    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    
    #default configuration for miniAOD reprocessing, change the isData flag to run on data
    #for a full met computation, remove the pfCandColl input
    runMetCorAndUncFromMiniAOD(process,
                           isData=isdata,
                           )

#    process.selectedPatJetsForMetT1T2Corr.src = cms.InputTag("cleanedPatJets")
#    process.patPFMetT1.src = cms.InputTag("slimmedMETs")
#
#    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJEC 
#    process.CustomisationsSequence += process.patJetsReapplyJEC
#    process.CustomisationsSequence += process.basicJetsForMet
#    process.CustomisationsSequence += process.jetSelectorForMet
#    process.CustomisationsSequence += process.cleanedPatJets
#    process.CustomisationsSequence += process.metrawCalo
#    process.CustomisationsSequence += process.selectedPatJetsForMetT1T2Corr   
#    process.CustomisationsSequence += process.patPFMetT1T2Corr
#    process.CustomisationsSequence += process.patPFMetT1

#    process.CustomisationsSequence += process.patMetCorrectionSequence

    if isdata:
        return

#    process.CustomisationsSequence += process.patMetUncertaintySequence #only for MC
#    process.CustomisationsSequence += process.patShiftedModuleSequence #only for MC


    """    
    # puppi jets and puppi met
    from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
    makePuppiesFromMiniAOD(process);

    runMetCorAndUncFromMiniAOD(process,
                             isData=isdata,
                             pfCandColl=cms.InputTag("puppiForMET"),
                             recoMetFromPFCs=True,
                             reclusterJets=True,
                             jetFlavor="AK4PFPuppi",
                             postfix="Puppi"
                             )
    process.patPFMetPuppi.addGenMET = cms.bool(False)
    process.basicJetsForMetPuppi.src = cms.InputTag("slimmedJetsPuppi")
    process.patPFMetT1Puppi.src = cms.InputTag("slimmedMETsPuppi")

    process.producePatPFMETCorrectionsPuppi.remove(process.patPFMetPuppi)
    process.CustomisationsSequence += process.producePatPFMETCorrectionsPuppi

#    process.CustomisationsSequence += process.pfNoLepPUPPI
#    process.CustomisationsSequence += process.puppiNoLep
#    process.CustomisationsSequence += process.pfLeptonsPUPPET
#    process.CustomisationsSequence += process.puppiMerged
#    process.CustomisationsSequence += process.puppiForMET
##    process.CustomisationsSequence += process.pfMetPuppi
##    process.CustomisationsSequence += process.patPFMetPuppi
#    process.CustomisationsSequence += process.ak4PFJetsPuppi
#    process.CustomisationsSequence += process.basicJetsForMetPuppi
#    process.CustomisationsSequence += process.jetSelectorForMetPuppi
#    process.CustomisationsSequence += process.cleanedPatJetsPuppi
#    process.CustomisationsSequence += process.pfMetPuppi
#    process.CustomisationsSequence += process.metrawCaloPuppi
#    process.CustomisationsSequence += process.patPFMetT1Puppi
#
#    process.CustomisationsSequence += process.patMetUncertaintySequencePuppi
#    process.CustomisationsSequence += process.patShiftedModuleSequencePuppi
#    process.CustomisationsSequence += process.patMetCorrectionSequencePuppi
    """
