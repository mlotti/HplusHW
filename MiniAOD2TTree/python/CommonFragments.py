import FWCore.ParameterSet.Config as cms

# How to use:
# - Import this module
# - Call produceCustomisations just before cms.Path
# - Add process.CustomisationsSequence to the cms.Path

def produceCustomisations(process):
    process.CustomisationsSequence = cms.Sequence()
    reproduceJEC(process)
#    reproduceElectronID(process)
    reproduceMETNoiseFilters(process)
    print "=== Customisations done"

# ===== Reproduce jet collections with the latest JEC =====
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrPatJets
def reproduceJEC(process):
    print "=== Customisation: reproducing jet collections with latest JEC"
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    # PF AK4CHS jets
    if not hasattr(process, "JECpayloadAK4PFchs"):
        raise Exception("Error: Could not access process.JECpayloadAK4PFchs! Please load Jet_cfi.py before calling customizations")
    process.patJetCorrFactorsReapplyJECAK4CHS = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJets"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = process.JECpayloadAK4PFchs.payload,  # Set in Jet_cfi.py
    ) 
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJECAK4CHS = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECAK4CHS"))
    )
    # PUPPI jets
    if not hasattr(process, "JECpayloadAK4PFPuppi"):
        raise Exception("Error: Could not access process.JECpayloadAK4PFPuppi! Please load Jet_cfi.py before calling customizations")
    process.patJetCorrFactorsReapplyJECPuppi = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJetsPuppi"),
      levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
      payload = process.JECpayloadAK4PFPuppi.payload,  # Set in Jet_cfi.py
    )
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJECPuppi = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJetsPuppi"), 
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJECPuppi"))
    )
    #process.reapplyJEC = cms.Sequence(process.patJetCorrFactorsReapplyJECAK4CHS +
    #                                  process.patJetsReapplyJECAK4CHS +
    #                                  process.patJetCorrFactorsReapplyJECPuppi +
    #                                  process.patJetsReapplyJECPuppi)
    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECAK4CHS
    process.CustomisationsSequence += process.patJetsReapplyJECAK4CHS
    process.CustomisationsSequence += process.patJetCorrFactorsReapplyJECPuppi
    process.CustomisationsSequence += process.patJetsReapplyJECPuppi

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
    # Do not apply EDfilters for HBHE noise, the discriminators for them are saved into the ttree
    process.CustomisationsSequence += process.HBHENoiseFilterResultProducer

# ===== Set up MET uncertainties - FIXME: does not work at the moment =====
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATTools#MET_Systematics_Tools
#def reproduceMET(process):
    #import PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties as metUncertaintyTools
    #metUncertaintyTools.runMETCorrectionsAndUncertainties(process=process,
                                                      #metType="PF",
                                                      #correctionLevel=["T0","T1","Txy"], # additional options: Smear
                                                      #computeUncertainties=True,
                                                      #produceIntermediateCorrections=False,
                                                      #addToPatDefaultSequence=True,
                                                      #jetCollection=cms.InputTag("slimmedJets"),
                                                      #jetCollectionUnskimmed=cms.InputTag("slimmedJets"),
                                                      #electronCollection="",
                                                      #muonCollection="",
                                                      #tauCollection="",
                                                      #pfCandCollection=cms.InputTag("packedPFCandidates"),
                                                      #onMiniAOD=True,
                                                      #postfix="Type01xy")

