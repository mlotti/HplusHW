import FWCore.ParameterSet.Config as cms

# Build the signal analysis EDFilter here so that the definition can
# be shared between configuration files. Customisations should be done
# in the configuration files. _cfi.py solution might not work, because
# HChSignalAnalysisParameters module is typically modified before
# creating the EDFilter.
def createEDFilter(param):
    return cms.EDFilter("HPlusSignalAnalysisInvertedTauFilter",
        blindAnalysisStatus = param.blindAnalysisStatus,
	histogramAmbientLevel = param.histogramAmbientLevel,
        trigger = param.trigger.clone(),
        triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor.clone(),
        primaryVertexSelection = param.primaryVertexSelection.clone(),
        GlobalElectronVeto = param.GlobalElectronVeto.clone(),
        GlobalMuonVeto = param.GlobalMuonVeto.clone(),
#    GlobalMuonVeto = param.NonIsolatedMuonVeto.clone(),
    # Change default tau algorithm here as needed
        tauSelection = param.tauSelectionHPSMediumTauBased.clone(),
        fakeTauSFandSystematics = param.fakeTauSFandSystematics.clone(),
        vetoTauSelection = param.vetoTauSelection.clone(),
        jetSelection = param.jetSelection.clone(),
        MET = param.MET.clone(),
        bTagging = param.bTagging.clone(),
        fakeMETVeto = param.fakeMETVeto.clone(),
        jetTauInvMass = param.jetTauInvMass.clone(),
        deltaPhiTauMET = param.deltaPhiTauMET,
	topReconstruction = param.topReconstruction,
        topSelection = param.topSelection.clone(),
        bjetSelection = param.bjetSelection.clone(),                                      
        topChiSelection = param.topChiSelection.clone(),                                  
        topWithBSelection = param.topWithBSelection.clone(),
        topWithWSelection = param.topWithWSelection.clone(),
        forwardJetVeto = param.forwardJetVeto.clone(),
        transverseMassCut = param.transverseMassCut,
        EvtTopology = param.EvtTopology.clone(),
        prescaleWeightReader = param.prescaleWeightReader.clone(),
        vertexWeight = param.vertexWeight.clone(),
        pileupWeightReader = param.pileupWeightReader.clone(),
        wjetsWeightReader = param.wjetsWeightReader.clone(),                   
        GenParticleAnalysis = param.GenParticleAnalysis.clone(),
        Tree = param.tree.clone(),
        eventCounter = param.eventCounter.clone(),
        oneAndThreeProngTauSrc = cms.untracked.InputTag("VisibleTaus","HadronicTauOneAndThreeProng"),
        tauEmbeddingStatus = cms.untracked.bool(False),
        metFilters = param.metFilters.clone(),
    )
