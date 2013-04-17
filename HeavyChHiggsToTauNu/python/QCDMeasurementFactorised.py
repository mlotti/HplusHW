import FWCore.ParameterSet.Config as cms

# Build the QCD factorised EDFilter here so that the definition can
# be shared between configuration files. Customisations should be done
# in the configuration files. _cfi.py solution might not work, because
# HChSignalAnalysisParameters module is typically modified before
# creating the EDFilter.
def createEDFilter(param):
    return cms.EDFilter("HPlusQCDMeasurementFactorisedFilter",
        blindAnalysisStatus = param.blindAnalysisStatus,
        histogramAmbientLevel = param.histogramAmbientLevel,
        trigger = param.trigger.clone(),
        tauTriggerEfficiencyScaleFactor = param.tauTriggerEfficiencyScaleFactor.clone(),
        metTriggerEfficiencyScaleFactor = param.metTriggerEfficiencyScaleFactor.clone(),
        primaryVertexSelection = param.primaryVertexSelection.clone(),
        ElectronSelection= param.ElectronSelection.clone(),
        MuonSelection = param.MuonSelection.clone(),
        #GlobalMuonVeto = param.NonIsolatedMuonVeto.clone(),
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
        GenParticleAnalysis = param.GenParticleAnalysis.clone(),
        QCDTailKiller = param.QCDTailKiller.clone(),
        Tree = param.tree.clone(),
        eventCounter = param.eventCounter.clone(),
        tauEmbeddingStatus = cms.untracked.bool(False),
        factorisationTauPtBinLowEdges = cms.untracked.vdouble(50., 60., 70., 80., 100., 120., 150., 200., 300.),
        factorisationTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, 1.5), # probably need to constrain to -1.5, 1.5, i.e. endcap-, barrel, endcap+
        factorisationNVerticesBinLowEdges = cms.untracked.vint32(10, 20),
        factorisationTransverseMassRange = cms.untracked.vdouble(40., 0., 400.),
        factorisationFullMassRange = cms.untracked.vdouble(50., 0., 500.),
    )
