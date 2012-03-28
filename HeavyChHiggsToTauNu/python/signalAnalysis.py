import FWCore.ParameterSet.Config as cms

# Build the signal analysis EDFilter here so that the definition can
# be shared between configuration files. Customisations should be done
# in the configuration files. _cfi.py solution might not work, because
# HChSignalAnalysisParameters module is typically modified before
# creating the EDFilter.
def createEDFilter(param):
    return cms.EDFilter("HPlusSignalAnalysisFilter",
        blindAnalysisStatus = param.blindAnalysisStatus,
        trigger = param.trigger,
        triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor,
        primaryVertexSelection = param.primaryVertexSelection,
        GlobalElectronVeto = param.GlobalElectronVeto,
        GlobalMuonVeto = param.GlobalMuonVeto,
#    GlobalMuonVeto = param.NonIsolatedMuonVeto,
    # Change default tau algorithm here as needed
        tauSelection = param.tauSelectionHPSMediumTauBased,
        vetoTauSelection = param.vetoTauSelection,
        jetSelection = param.jetSelection,
        MET = param.MET,
        bTagging = param.bTagging,
        fakeMETVeto = param.fakeMETVeto,
        jetTauInvMass = param.jetTauInvMass,
        topSelection = param.topSelection,
        bjetSelection = param.bjetSelection,                                      
        topChiSelection = param.topChiSelection,                                  
        topWithBSelection = param.topWithBSelection,
        forwardJetVeto = param.forwardJetVeto,
        transverseMassCut = param.transverseMassCut,
        EvtTopology = param.EvtTopology,
        vertexWeight = param.vertexWeight,
        GenParticleAnalysis = param.GenParticleAnalysis,
        Tree = param.tree,
    )
