import FWCore.ParameterSet.Config as cms

Electrons = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Electrons"),
        src = cms.InputTag("slimmedElectrons"),
        rhoSource = cms.InputTag("fixedGridRhoFastjetAll"), # for PU mitigation in isolation
#        IDprefix = cms.string("egmGsfElectronIDs"),
#        discriminators = cms.vstring()
	discriminators = cms.vstring("cutBasedElectronID-Spring15-25ns-V1-standalone-veto",
                                     "cutBasedElectronID-Spring15-25ns-V1-standalone-loose",
                                     "cutBasedElectronID-Spring15-25ns-V1-standalone-medium",
                                     "cutBasedElectronID-Spring15-25ns-V1-standalone-tight",
                                     )
#        discriminators = cms.vstring("mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80",
#                                     "mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90")
    )
)

# 8X
# egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto
# egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose
# egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium
# egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight
#
# heepElectronID-HEEPV60 
# mvaEleID-Spring15-25ns-nonTrig-V1-wp80 
# mvaEleID-Spring15-25ns-nonTrig-V1-wp90 
# cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose 
# cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium 
# cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight 
# cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto 
# cutBasedElectronID-Spring15-25ns-V1-standalone-loose 
# cutBasedElectronID-Spring15-25ns-V1-standalone-medium 
# cutBasedElectronID-Spring15-25ns-V1-standalone-tight 
# cutBasedElectronID-Spring15-25ns-V1-standalone-veto 
# cutBasedElectronID-Spring15-50ns-V1-standalone-loose 
# cutBasedElectronID-Spring15-50ns-V1-standalone-medium 
# cutBasedElectronID-Spring15-50ns-V1-standalone-tight 
# cutBasedElectronID-Spring15-50ns-V1-standalone-veto 
# eidLoose 
# eidRobustHighEnergy 
# eidRobustLoose 
# eidRobustTight 
# eidTight
