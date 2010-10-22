import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
from PhysicsTools.PatAlgos.tools.tauTools import addTauCollection, classicTauIDSources, classicPFTauIDSources, tancTauIDSources
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching, restrictInputToAOD, removeSpecificPATObjects
import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChPFTauDiscriminatorsCont
import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTaus_cfi as HChTaus
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausCont_cfi as HChTausCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausTest_cfi as HChTausTest
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination_cfi as PFTauTestDiscrimination

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doPatMET=True):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    # Tau Discriminators
    process.hplusPatTauSequence = cms.Sequence()
    if doPatTaus:
        process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process)
	PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process)

        HChCaloTauDiscriminators.addCaloTauDiscriminationSequenceForChargedHiggs(process)
        HChCaloTauDiscriminatorsCont.addCaloTauDiscriminationSequenceForChargedHiggsCont(process)

        # These are already in 36X AOD, se remove them from the tautagging
        # sequence
        if not dataVersion.is35X():
            process.tautagging.remove(process.jptRecoTauProducer)
            process.tautagging.remove(process.caloRecoTauProducer)
            process.tautagging.remove(process.caloRecoTauDiscriminationAgainstElectron)
            process.tautagging.remove(process.caloRecoTauDiscriminationByIsolation)
            process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackFinding)
            process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackPtCut)
        
        process.load("RecoTauTag.Configuration.HPSPFTaus_cfi")

        process.hplusPatTauSequence = cms.Sequence(
            process.tautagging *
            process.PFTauDiscriminationSequenceForChargedHiggs *
            process.PFTauDiscriminationSequenceForChargedHiggsCont *
	    process.PFTauTestDiscriminationSequence *
            process.produceAndDiscriminateHPSPFTaus *
            process.CaloTauDiscriminationSequenceForChargedHiggs *
            process.CaloTauDiscriminationSequenceForChargedHiggsCont
        )

    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    # Count the number of primary vertices, and put into event
    #process.primaryVertexNumber = cms.EDProducer("HPlusVertexCountProducer",
    #    src = cms.InputTag('offlinePrimaryVertices'),
    #    alias = cms.string("primaryVertexNumber")
    #)
    #if dataVersion.isData():
    #    # See HChDataSelection
    #    process.primaryVertexNumber.src = "selectedPrimaryVertices"
    #if out != None:
    #    out.outputCommands.append("keep int_primaryVertexNumber_*_*")

    process.hplusPatSequence = cms.Sequence(
        process.hplusPatTauSequence *
        process.patDefaultSequence *
        process.primaryVertexNumber
    )

    # Restrict input to AOD
    restrictInputToAOD(process, ["All"])

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    if dataVersion.isData():
        removeMCMatching(process, ["All"])

    # Jets
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    process.patJets.addJetID = False
    if dataVersion.is38X():
        process.patJets.addTagInfos = False

    addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                     'AK5', 'JPT',
                     doJTA        = True,
                     doBTagging   = True,
                     jetCorrLabel = ('AK5','JPT'),
                     doType1MET   = False,
                     doL1Cleaning = False,
                     doL1Counters = True,
                     genJetCollection = cms.InputTag("ak5GenJets"),
                     doJetID      = False
                     )
    if out != None:
        out.outputCommands.append("keep *_selectedPatJetsAK5JPT_*_*")

    #### needed for CMSSW35x data
    if dataVersion.is35X():
        process.load("RecoJets.Configuration.GenJetParticles_cff")
        process.load("RecoJets.Configuration.RecoGenJets_cff")
        ## creating JPT jets
        process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
        process.load('RecoJets.Configuration.RecoJPTJets_cff')

        run36xOn35xInput(process)


    # Taus

    # Set default PATTauProducer options here, they should be
    # replicated to all added tau collections (and the first call to
    # addTauCollection should replace the default producer modified
    # here)
    process.patTaus.embedLeadTrack = True

    # For some reason, embedding these for 35X data does NOT work for
    # calotaus (output module complains about trying to persist
    # transient Ref/Ptr, so I'd guess there's transient RefVector of
    # tracks somewhere in the calotau reconstruction process

    # Update: Apparently it doesn't work on 36X collision data
    # either...

    #if not dataVersion.is35X():
    #    process.patTaus.embedSignalTracks = True
    #    process.patTaus.embedIsolationTracks = True

    # There's probably a bug in pat::Tau which in practice prevents
    # the emedding of PFCands. Therefore we keep the PFCandidates
    # collection in the event so that the PFCands can be accessed via
    # edm::Refs. (note: PFCand embedding works, so it is just the
    # collection embedding which doesn't. The PFCand embedding is
    # disabled for consistenty and saving even some disk space.

    process.patTaus.embedLeadPFCand = True
    process.patTaus.embedLeadPFChargedHadrCand = True
    process.patTaus.embedLeadPFNeutralCand = True
    # process.patTaus.embedSignalPFCands = True
    # process.patTaus.embedSignalPFChargedHadrCands = True
    # process.patTaus.embedSignalPFNeutralHadrCands = True
    # process.patTaus.embedSignalPFGammaCands = True
    # process.patTaus.embedIsolationPFCands = True
    # process.patTaus.embedIsolationPFChargedHadrCands = True
    # process.patTaus.embedIsolationPFNeutralHadrCands = True
    # process.patTaus.embedIsolationPFGammaCands = True

    if doPatTaus:
        classicTauIDSources.extend( HChTaus.HChTauIDSources )
        classicTauIDSources.extend( HChTausCont.HChTauIDSourcesCont )
	classicPFTauIDSources.extend( HChTausTest.TestTauIDSources )

        addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
                         algoLabel = "caloReco",
                         typeLabel = "Tau")
        process.patTausCaloRecoTau.embedLeadPFCand = False
        process.patTausCaloRecoTau.embedLeadPFChargedHadrCand = False
        process.patTausCaloRecoTau.embedLeadPFNeutralCand = False

        addTauCollection(process,cms.InputTag('shrinkingConePFTauProducer'),
                         algoLabel = "shrinkingCone",
                         typeLabel = "PFTau")
        # Disable isoDeposits like this untilthe problem with doPFIsoDeposits is fixed 
        process.patTausShrinkingConePFTau.isoDeposits = cms.PSet()

#        if not dataVersion.is38X():
#            addTauCollection(process,cms.InputTag('fixedConePFTauProducer'),
#                             algoLabel = "fixedCone",
#                             typeLabel = "PFTau")
#            process.patTausFixedConePFTau.isoDeposits = cms.PSet()

        addTauCollection(process,cms.InputTag('hpsPFTauProducer'),
                         algoLabel = "hps",
                         typeLabel = "PFTau")
        process.patTausHpsPFTau.isoDeposits = cms.PSet()
    else:
        removeSpecificPATObjects(process, ["Taus"], outputInProcess= out != None)
    

    # Add PAT default event content
    if out != None:
        out.outputCommands.extend(patEventContentNoCleaning)
	out.outputCommands.extend(["drop *_selectedPatTaus_*_*",
                                   #"keep *_cleanPatTaus_*_*",
                                   #"drop *_cleanPatTaus_*_*",
                                   #"keep *_patTaus*_*_*",
                                   #"keep *_patPFTauProducerFixedCone_*_*",
                                   # keep these until the embedding problem with pat::Tau is fixed
                                   #"keep recoPFCandidates_particleFlow_*_*",
                                   #"keep recoTracks_generalTracks_*_*"
                                   ])

    # MET
    if doPatMET:
        addTcMET(process, 'TC')
        addPfMET(process, 'PF')
        if out != None:
            out.outputCommands.extend(["keep *_patMETsPF_*_*", "keep *_patMETsTC_*_*"])
    else:
        removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)


    # Muons

    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    #process.patMuons.usePV = False


    # Trigger
    if doPatTrigger:
        outMod= ''
        if out != None:
            outMod  = 'out'
        switchOnTrigger(process)
        #, hltProcess=dataVersion.getTriggerProcess(), outputModule=outMod)

    # Build sequence
    seq = cms.Sequence()
    if dataVersion.is35X():
        process.hplusJptSequence = cms.Sequence(
            process.genJetParticles *
            process.ak5GenJets *
            process.recoJPTJets
        )
        seq *= process.hplusJptSequence

    seq *= process.hplusPatSequence

    return seq
    
