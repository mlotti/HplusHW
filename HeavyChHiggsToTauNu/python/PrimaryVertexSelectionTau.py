import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.tauTools as tauTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching

# The sequence built by the buildSequence() function is ran after
# pat::Trigger has been produced, but before the PF2PAT seuqence(s).
# The function is expected to build a Sequence, but not insert it to
# the process (this is done by the caller). The sequence should
# produce an int for the index of the selected primary verte with the
# name "selectedPrimaryVertexIndex".
def buildSequence(process, patArgs):
    sequence = cms.Sequence()

    # Produce HPS taus from AK5 PF jets already in AOD
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    sequence *= process.PFTau
    # Produce pat taus, assuming patDefaultSequence is already included to the process
    if not hasattr(process, "patTausHpsPFTau"):
        tauTools.addTauCollection(process, cms.InputTag('hpsPFTauProducer'),
                                  algoLabel = "hps",
                                  typeLabel = "PFTau")

    process.patTausHpsPFTauForPV = process.patTausHpsPFTau.clone(
        addGenJetMatch = False,
        embedGenJetMatch = False,
        addGenMatch = False,
        embedGenMatch = False,
        userIsolation = cms.PSet(),
        isoDeposits = cms.PSet(),
    )
    process.patTausHpsPFTauForPV.tauIDSources.byRawCombinedIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr")

    sequence *= process.patTausHpsPFTauForPV

    # Trigger matching
    sequence *= HChTriggerMatching.addTauHLTMatching(process, patArgs["matchingTauTrigger"], collections=["patTausHpsPFTauForPV"], postfix="ForPV")

    # Require decay mode finding
    process.selectedPatTausHpsPFTauForPV = cms.EDFilter("PATTauSelector",
        src = cms.InputTag("patTausHpsPFTauForPVTriggerMatchedForPV"),
        cut = cms.string("tauID('decayModeFinding')")
    )
    sequence *= process.selectedPatTausHpsPFTauForPV

    # Obtain the index of the vertex of most isolated tau
    process.selectedPrimaryVertexIndex = cms.EDProducer("HPlusVertexIndexTauMostIsolatedProducer",
        vertexSrc = cms.InputTag("offlinePrimaryVertices"),
        tauSrc = cms.InputTag("selectedPatTausHpsPFTauForPV"),
        tauDiscriminator = cms.string("byRawCombinedIsolationDeltaBetaCorr"),
        dz = cms.double(0.2),
    )
    sequence *= process.selectedPrimaryVertexIndex

    return sequence
