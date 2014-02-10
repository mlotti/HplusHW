import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

configInfo = cms.PSet(
    pileupReweightType = cms.string("UNWEIGHTED"),
    topPtReweightType = cms.string("UNWEIGHTED"),
)

# Blind analysis - do not fill final counter and histogram for data if true
blindAnalysisStatus = cms.untracked.bool(False)

# Ambient level for filling histograms (options: Vital, Informative, Debug)
histogramAmbientLevel = cms.untracked.string("Debug")

singleTauMetTriggerPaths = [
# 2010
#    "HLT_SingleLooseIsoTau20",
#    "HLT_SingleLooseIsoTau20_Trk5",
#    "HLT_SingleIsoTau20_Trk5",
#    "HLT_SingleIsoTau20_Trk15_MET20",
#    "HLT_SingleIsoTau20_Trk15_MET25_v3",
#    "HLT_SingleIsoTau20_Trk15_MET25_v4",
# 2011
    "HLT_IsoPFTau35_Trk20_MET45_v1",
    "HLT_IsoPFTau35_Trk20_MET45_v2",
    "HLT_IsoPFTau35_Trk20_MET45_v4",
    "HLT_IsoPFTau35_Trk20_MET45_v6",
    "HLT_IsoPFTau35_Trk20_MET60_v2",
    "HLT_IsoPFTau35_Trk20_MET60_v3",
    "HLT_IsoPFTau35_Trk20_MET60_v4",
    "HLT_IsoPFTau35_Trk20_MET60_v6",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v5",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v6",
# 2012
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9",
#    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10",
]
# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    triggerSrc = cms.untracked.InputTag("TriggerResults", "", "INSERT_HLT_PROCESS_HERE"),
    patSrc = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring(singleTauMetTriggerPaths),
    hltMetCut = cms.untracked.double(60.0),
    throwIfNoMet = cms.untracked.bool(False), # to prevent jobs from failing, FIXME: must be investigated later
    selectionType = cms.untracked.string("byTriggerBit"), # Default byTriggerBit, other options , disabled
    caloMetSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("met"), # Calo MET
        metEmulationCut = cms.untracked.double(-1), # disabled by default
    )
)

from HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEmulationEfficiency_cfi import *

metFilters = cms.untracked.PSet(
    beamHaloSrc = cms.untracked.InputTag("BeamHaloSummary"),
    beamHaloEnabled = cms.untracked.bool(True),
    HBHENoiseFilterSrc = cms.untracked.InputTag("HBHENoiseFilterResultProducer", "HBHENoiseFilterResult"),
    HBHENoiseFilterEnabled = cms.untracked.bool(True),
    HBHENoiseFilterMETWGSrc = cms.untracked.InputTag("HBHENoiseFilterResultProducerMETWG", "HBHENoiseFilterResult"),
    HBHENoiseFilterMETWGEnabled = cms.untracked.bool(False), # Optional
    trackingFailureFilterSrc = cms.untracked.InputTag("trackingFailureFilter"),
    trackingFailureFilterEnabled = cms.untracked.bool(True),
    EcalDeadCellEventFilterSrc = cms.untracked.InputTag("EcalDeadCellEventFilter"),
    EcalDeadCellEventFilterEnabled = cms.untracked.bool(True),
    EcalDeadCellTPFilterSrc = cms.untracked.InputTag("ecalDeadCellTPfilter"),
    EcalDeadCellTPFilterEnabled = cms.untracked.bool(True),
    triggerResultsSrc = cms.untracked.InputTag("TriggerResults", "", "HChPatTuple"),
)

primaryVertexSelection = cms.untracked.PSet(
    selectedSrc = cms.untracked.InputTag("selectedPrimaryVertex"),
    allSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
    sumPtSrc = cms.untracked.InputTag("offlinePrimaryVerticesSumPt", "sumPt"),
    enabled = cms.untracked.bool(True)
)

# Default tau selection
tauSelectionBase = cms.untracked.PSet(
    # Operating mode options: 'standard'
    operatingMode = cms.untracked.string("standard"), # Standard tau ID (Tau candidate selection + tau ID applied)
    src = cms.untracked.InputTag("selectedPatTausHpsPFTau"),
    selection = cms.untracked.string(""),
#    ptCut = cms.untracked.double(50), # jet pt > value for heavy charged Higgs
    ptCut = cms.untracked.double(41), # jet pt > value
    etaCut = cms.untracked.double(2.1), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(20.0), # ldg. track > value
    againstElectronDiscriminator = cms.untracked.string("againstElectronTightMVA3"), # discriminator against electrons
    againstMuonDiscriminator = cms.untracked.string("againstMuonTight2"), # discriminator for against muons
    applyVetoForDeadECALCells = cms.untracked.bool(False), # set to true to exclude taus that are pointing to a dead ECAL cell
    deadECALCellsDeltaR = cms.untracked.double(0.01), # min allowed DeltaR to a dead ECAL cell
    isolationDiscriminator = cms.untracked.string("byMediumCombinedIsolationDeltaBetaCorr3Hits"), # discriminator for isolation
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1.0), # cut point for continuous isolation discriminator, applied only if it is non-zero
    rtauCut = cms.untracked.double(0.7), # rtau > value
    nprongs = cms.untracked.uint32(1), # number of prongs (options: 1, 3, or 13 == 1 || 3)
    analyseFakeTauComposition = cms.untracked.bool(False),
)

# Only HPS should be used (ignore TCTau, plain PF, TaNC, and Combined HPS+TaNC)

tauSelectionHPSTightTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byTightCombinedIsolationDeltaBetaCorr3Hits",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

tauSelectionHPSMediumTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byMediumCombinedIsolationDeltaBetaCorr3Hits",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

tauSelectionHPSLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

# Very loose working point is no longer supported
#tauSelectionHPSVeryLooseTauBased = tauSelectionBase.clone(
    #src = "selectedPatTausHpsPFTau",
    #selection = "HPSTauBased",
    #isolationDiscriminator = "byVLooseCombinedIsolationDeltaBetaCorr",
    #isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
#)

vetoTauBase = tauSelectionHPSLooseTauBased.clone(
    src = "selectedPatTausHpsPFTau",
#    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau"),
    ptCut = cms.untracked.double(20), # jet pt > value
    etaCut = cms.untracked.double(2.4), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(5.0), # ldg. track > value
#    leadingObjectPtCut = cms.untracked.double(5.0), # ldg. track > value
#    isolationDiscriminator = "byVLooseIsolation",
#    isolationDiscriminator = "byIsolation05",
    rtauCut = cms.untracked.double(0.0), # rtau > value
    nprongs = cms.untracked.uint32(13) # number of prongs (options: 1, 3, or 13 == 1 || 3)
)

vetoTauSelection = cms.untracked.PSet(
    tauSelection = vetoTauBase,
    src = cms.untracked.InputTag("genParticles"),
    oneProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"),
    oneAndThreeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng"),
    threeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauThreeProng"),
    Zmass = cms.untracked.double(90), # Z mass value in GeV
    ZmassWindow = cms.untracked.double(10), # window around Z mass in GeV for vetoing events
)

tauSelections = [tauSelectionHPSTightTauBased,
                 tauSelectionHPSMediumTauBased,
                 tauSelectionHPSLooseTauBased]
tauSelectionNames = ["TauSelectionHPSTightTauBasedTauTriggerMatched",
                     "TauSelectionHPSMediumTauBasedTauTriggerMatched",
                     "TauSelectionHPSLooseTauBasedTauTriggerMatched"]

#tauSelection = tauSelectionHPSTightTauBased
#tauSelection = tauSelectionHPSLooseTauBased
tauSelection = tauSelectionHPSMediumTauBased

# The fake tau SF and systematics numbers apply for 2011 data
# Source: https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation
fakeTauSFandSystematicsBase = cms.untracked.PSet(
    visibleMCTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng"), # All MC visible taus
    visibleMCTauOneProngSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"), # MC visible 1-prong taus
    matchingConditionDeltaR = cms.untracked.double(0.1), # Matching cone size
    scalefactorGenuineTauBarrel = cms.untracked.double(1.0),
    scalefactorGenuineTauEndcap = cms.untracked.double(1.0),
    scalefactorFakeTauBarrelElectron = cms.untracked.double(2.0),
    scalefactorFakeTauEndcapElectron = cms.untracked.double(1.2),
    scalefactorFakeTauBarrelMuon = cms.untracked.double(1.0),
    scalefactorFakeTauEndcapMuon = cms.untracked.double(1.0),
    scalefactorFakeTauBarrelJet = cms.untracked.double(1.0),
    scalefactorFakeTauEndcapJet = cms.untracked.double(1.0),
    # The following numbers are to be understood as SF +- the indicated number
    systematicsGenuineTauBarrel = cms.untracked.double(0.06),
    systematicsGenuineTauEndcap = cms.untracked.double(0.06),
    systematicsFakeTauBarrelElectron = cms.untracked.double(0.4),
    systematicsFakeTauEndcapElectron = cms.untracked.double(0.4),
    systematicsFakeTauBarrelMuon = cms.untracked.double(0.3),
    systematicsFakeTauEndcapMuon = cms.untracked.double(0.3),
    systematicsFakeTauBarrelJet = cms.untracked.double(0.2),
    systematicsFakeTauEndcapJet = cms.untracked.double(0.2)
)

fakeTauSFandSystematicsAgainstElectronMedium = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 0.95,
    scalefactorFakeTauEndcapElectron = 0.75,
    systematicsFakeTauBarrelElectron = 0.95*0.10,
    systematicsFakeTauEndcapElectron = 0.75*0.15,
)
fakeTauSFandSystematicsAgainstElectronMVA = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 0.85,
    scalefactorFakeTauEndcapElectron = 0.65,
    systematicsFakeTauBarrelElectron = 0.85*0.2,
    systematicsFakeTauEndcapElectron = 0.65*0.2,
)
fakeTauSFandSystematicsAgainstElectronLooseMVA3 = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 1.4,
    scalefactorFakeTauEndcapElectron = 0.8,
    systematicsFakeTauBarrelElectron = 0.3,
    systematicsFakeTauEndcapElectron = 0.3,
)
fakeTauSFandSystematicsAgainstElectronMediumMVA3 = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 1.6,
    scalefactorFakeTauEndcapElectron = 0.8,
    systematicsFakeTauBarrelElectron = 0.3,
    systematicsFakeTauEndcapElectron = 0.3,
)
fakeTauSFandSystematicsAgainstElectronTightMVA3 = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 2.0,
    scalefactorFakeTauEndcapElectron = 1.2,
    systematicsFakeTauBarrelElectron = 0.4,
    systematicsFakeTauEndcapElectron = 0.4,
)
fakeTauSFandSystematicsAgainstElectronVTightMVA3 = fakeTauSFandSystematicsBase.clone(
    scalefactorFakeTauBarrelElectron = 2.4,
    scalefactorFakeTauEndcapElectron = 1.2,
    systematicsFakeTauBarrelElectron = 0.5,
    systematicsFakeTauEndcapElectron = 0.5,
)
# Obtain genuine and fake tau systematics automatically based on tau against electron discriminator
def setFakeTauSFAndSystematics(fakeTauPSet, tausele, mod="HChSignalAnalysisParameters_cff"):
    source = "fakeTauSFandSystematics"+tausele.againstElectronDiscriminator.value().replace("against","Against")
    try:
        pset = globals()[source].clone()
    except KeyError:
        myOptionList = filter(lambda item: "fakeTauSFandSystematics" in item, globals().keys())
        raise Exception("Error: Could not find fakeTauSFandSystematics for against electron discriminator %s! Options are: %s"%(tauSelection.againstElectronDiscriminator.value(), ", ".join(map(str, myOptionList))))

    HChTools.insertPSetContentsTo(pset, fakeTauPSet)
    # Update scale factor values for systematics variations
    myList = []
    if "GenuineTau" in mod or "FakeTau" in mod:
        if "GenuineTau" in mod:
            myList = ["GenuineTauBarrel","GenuineTauEndcap"]
        elif "FakeTauBarrelElectron" in mod:
            myList = ["FakeTauBarrelElectron"]
        elif "FakeTauEndcapElectron" in mod:
            myList = ["FakeTauEndcapElectron"]
        elif "FakeTauMuon" in mod:
            myList = ["FakeTauBarrelMuon","FakeTauEndcapMuon"]
        elif "FakeTauJet" in mod:
            myList = ["FakeTauBarrelJet","FakeTauEndcapJet"]
        for item in myList:
            sfValue = getattr(fakeTauPSet, "scalefactor"+item)
            systValue = getattr(fakeTauPSet, "systematics"+item)
            newSfValue = float(sfValue.value()) + float(systValue.value())
            if "Minus" in mod:
                newSfValue = float(sfValue.value()) - float(systValue.value())
            setattr(fakeTauPSet, "scalefactor"+item, newSfValue)
    # Print info
    if len(myList):
        print "fakeTauSFandSystematics set to %s for %s; SF variatated for %s" % (source, mod, ", ".join(map(str,myList)))
    else:
        print "fakeTauSFandSystematics set to %s for %s" % (source, mod)
fakeTauSFandSystematics = fakeTauSFandSystematicsBase.clone()
setFakeTauSFAndSystematics(fakeTauSFandSystematics, tauSelection)

jetSelectionBase = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPatJets"),  # PF jets
    cleanTauDR = cms.untracked.double(0.5), # cone for rejecting jets around tau jet
    ptCut = cms.untracked.double(30.0),
    etaCut = cms.untracked.double(2.4),
    jetNumber = cms.untracked.uint32(3), # minimum number of selected jets
    jetNumberCutDirection = cms.untracked.string("GEQ"), # direction of jet number cut direction, options: NEQ, EQ, GT, GEQ, LT, LEQ
    # Jet ID cuts
    jetIdMaxNeutralHadronEnergyFraction = cms.untracked.double(0.99),
    jetIdMaxNeutralEMEnergyFraction = cms.untracked.double(0.99),
    jetIdMinNumberOfDaughters = cms.untracked.uint32(1),
    jetIdMinChargedHadronEnergyFraction = cms.untracked.double(0.0),
    jetIdMinChargedMultiplicity = cms.untracked.uint32(0),
    jetIdMaxChargedEMEnergyFraction = cms.untracked.double(0.99),
    # Pileup cleaning
    jetPileUpJetCollectionPrefix = cms.untracked.string("puJetMva"),
    jetPileUpType = cms.untracked.string("full"), # options: 'full' (BDT based), 'cutbased', 'philv1', 'simple'
    jetPileUpWorkingPoint = cms.untracked.string("tight"), # options: tight, medium, loose
    jetPileUpMVAValues = cms.untracked.InputTag("","",""), # will be set by the function setJetPUIdSrc from AnalysisConfiguration
    jetPileUpIdFlag = cms.untracked.InputTag("","",""), # will be set by the function setJetPUIdSrc from AnalysisConfiguration
    # Veto event if jet hits dead ECAL cell - experimental, do not use for latest greatest results!
    applyVetoForDeadECALCells = cms.untracked.bool(False),
    deadECALCellsVetoDeltaR = cms.untracked.double(0.07),
    # Experimental
    EMfractionCut = cms.untracked.double(999), # large number to effectively disable the cut
)

jetSelectionLoose = jetSelectionBase.clone()

jetSelectionMedium = jetSelectionBase.clone(
    jetIdMaxNeutralHadronEnergyFraction = cms.untracked.double(0.95),
    jetIdMaxNeutralEMEnergyFraction = cms.untracked.double(0.95),
)

jetSelectionTight = jetSelectionBase.clone(
    jetIdMaxNeutralHadronEnergyFraction = cms.untracked.double(0.90),
    jetIdMaxNeutralEMEnergyFraction = cms.untracked.double(0.90),
)

jetSelection = jetSelectionTight # set default jet selection

MET = cms.untracked.PSet(
    rawSrc = cms.untracked.InputTag("patPFMet"), # PF MET
    type1Src = cms.untracked.InputTag("patType1CorrectedPFMet"),
    type2Src = cms.untracked.InputTag("patType1p2CorrectedPFMet"),
    caloSrc = cms.untracked.InputTag("metNoHF"),
    tcSrc = cms.untracked.InputTag("patMETsTC"),
    select = cms.untracked.string("type1"), # raw, type1, type2
    METCut = cms.untracked.double(60.0),
    preMETCut = cms.untracked.double(0.0), # Pre-cut is important for background measurements
#    METCut = cms.untracked.double(80.0), # MET cut for heavy charged Higgs
    # For type I/II correction
    doTypeICorrectionForPossiblyIsolatedTaus = cms.untracked.string("disabled"), # This flag affects only to METSelection::(silent)analyzeWithPossiblyIsolatedTaus(), valid values are: disabled, never, always, forIsolatedOnly
    tauJetMatchingCone = cms.untracked.double(0.5),
    jetType1Threshold = cms.untracked.double(10),
    jetOffsetCorrLabel = cms.untracked.string("L1FastJet"),
    #type2ScaleFactor = cms.untracked.double(1.4),

    # For phi oscillation correction - very preliminary parameters
    phiCorrectionSlopeXForData = cms.untracked.double(0.6224), # +- 0.0286
    phiCorrectionOffsetXForData = cms.untracked.double(-0.3173), # +- 0.597
    phiCorrectionSlopeYForData = cms.untracked.double(-0.4129), # +- 0.0285
    phiCorrectionOffsetYForData = cms.untracked.double(1.14), # +- 0.59
    phiCorrectionSlopeXForMC = cms.untracked.double(-0.02390), # taken from Christian
    phiCorrectionOffsetXForMC = cms.untracked.double(0.11438), # taken from Christian
    phiCorrectionSlopeYForMC = cms.untracked.double(-0.27637), # taken from Christian
    phiCorrectionOffsetYForMC = cms.untracked.double(2.1351), # taken from Christian
)

bTagging = cms.untracked.PSet(
    # jetBProbabilityBJetTags,jetProbabilityBJetTags,trackCountingHighPurBJetTags,trackCountingHighEffBJetTags,simpleSecondaryVertexHighEffBJetTags,simpleSecondaryVertexHighPurBJetTags,combinedSecondaryVertexBJetTags,combinedSecondaryVertexMVABJetTags,softMuonBJetTags,softMuonByPtBJetTags,softMuonByIP3dBJetTags
#   OP: JPL = 0.275, JPM = 0.545, JPT = 0.790, CSVL = 0.244, CSVM = 0.679, CSVT = 0.898
#    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminator = cms.untracked.string("combinedSecondaryVertexBJetTags"),
#    discriminator = cms.untracked.string("jetProbabilityBJetTags"),   
    leadingDiscriminatorCut = cms.untracked.double(0.898), # used for best bjet candidates (best discriminator)
    subleadingDiscriminatorCut = cms.untracked.double(0.898), # disabled, use leading discriminator cut only (was used for other bjet candidates)
    ptCut = cms.untracked.double(30.0), # No effect, change value in jet selection, if necessary!
#    ptCut = cms.untracked.double(30.0), # for heavy charged Higgs
    etaCut = cms.untracked.double(2.4), # No effect, change value in jet selection, if necessary!
    jetNumber = cms.untracked.uint32(1),
    jetNumberCutDirection = cms.untracked.string("GEQ"), # direction of jet number cut direction, options: NEQ, EQ, GT, GEQ, LT, LEQ
    variationEnabled = cms.untracked.bool(False),
    variationShiftBy = cms.untracked.double(0),
)

oneProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng")
 
#deltaPhiTauMET = cms.untracked.double(160.0) # less than this value in degrees
deltaPhiTauMET = cms.untracked.double(180.0) # less than this value in degrees, for heavy charged Higgs

def QCDTailKillerBin(cutShape, cutX, cutY):
    validShapes = ["noCut", "rectangular", "triangular", "circular"]
    if cutShape not in validShapes:
        raise Exception("QCDTailKiller config for cut shape '%s' is not valid! (options: %s)"%(cutShape,", ".join(map(str, validShapes))))
    return cms.untracked.PSet(
        CutShape = cms.untracked.string(cutShape), # options: noCut, rectangular, triangular, circular
        CutX = cms.untracked.double(cutX),
        CutY = cms.untracked.double(cutY) # for circular this value is not considered
        )

QCDTailKiller = cms.untracked.PSet(
    scenarioLabel = cms.untracked.string("NoCuts"),
    maxJetsToConsider = cms.untracked.uint32(4),
    # Back to back (bottom right corner of 2D plane tau,MET vs. jet,MET)
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 1
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 2
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    ),
    # Collinear topology (top left corner of 2D plane tau,MET vs. jet,MET)
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 1
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 2
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 3
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 4
    ),
    disableCollinearCuts = cms.untracked.bool(False),
)

QCDTailKillerNoCuts = QCDTailKiller.clone()

QCDTailKillerZeroPlus = QCDTailKiller.clone(
    scenarioLabel = cms.untracked.string("ZeroPlus"),
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 1
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 2
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 3
        QCDTailKillerBin("noCut", 0.0, 0.0), # jet 4
    ),
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    )
)

QCDTailKillerLoosePlus = QCDTailKiller.clone(
    scenarioLabel = cms.untracked.string("LoosePlus"),
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    ),
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    )
)

QCDTailKillerMediumPlus = QCDTailKiller.clone(
    scenarioLabel = cms.untracked.string("MediumPlus"),
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 60.0, 60.0), # jet 1
        QCDTailKillerBin("circular", 60.0, 60.0), # jet 2
        QCDTailKillerBin("circular", 60.0, 60.0), # jet 3
        QCDTailKillerBin("noCut", 60.0, 60.0), # jet 4
    ),
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    )
)

QCDTailKillerTightPlus = QCDTailKiller.clone(
    scenarioLabel = cms.untracked.string("TightPlus"),
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 80.0, 80.0), # jet 1
        QCDTailKillerBin("circular", 80.0, 80.0), # jet 2
        QCDTailKillerBin("circular", 80.0, 80.0), # jet 3
        QCDTailKillerBin("noCut", 80.0, 80.0), # jet 4
    ),
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    )
)

QCDTailKillerVeryTightPlus = QCDTailKiller.clone(
    scenarioLabel = cms.untracked.string("VeryTightPlus"),
    backToBack = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 100.0, 100.0), # jet 1
        QCDTailKillerBin("circular", 100.0, 100.0), # jet 2
        QCDTailKillerBin("circular", 100.0, 100.0), # jet 3
        QCDTailKillerBin("noCut", 100.0, 100.0), # jet 4
    ),
    collinear = cms.untracked.VPSet(
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 1
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 2
        QCDTailKillerBin("circular", 40.0, 40.0), # jet 3
        QCDTailKillerBin("noCut", 40.0, 40.0), # jet 4
    )
)

# Define here QCD tail killer scenarios (note that the nominal module will be produced in addition to these)
QCDTailKillerScenarios = ["QCDTailKillerZeroPlus",
                          "QCDTailKillerLoosePlus",
                          "QCDTailKillerMediumPlus",
                          "QCDTailKillerTightPlus",
                          "QCDTailKillerVeryTightPlus"]

# Define H+ Invariant Mass Reco options
invMassReco = cms.untracked.PSet(
    #topInvMassCutName = cms.untracked.string("None")
    topInvMassLowerCut = cms.untracked.double(-1.0), # Negative value means no cut. This is currently the default.
    topInvMassUpperCut = cms.untracked.double(-1.0),  # Negative value means no cut. This is currently the default.
    pzSelectionMethod  = cms.untracked.string("DeltaEtaMin"), # Method of selecting the pZ of neutrino for real solutions
    metSelectionMethod = cms.untracked.string("SmallestMagnitude"), #Method of selecting MET for complex solutions
    reApplyMetCut      = MET.METCut, #Re-apply the MET cut after invariant mass reconstruction calculations (only for complex solutions). Set value as <0 to disable.
    #reApplyMetCut      = cms.untracked.double(0.0)
    )

topReconstruction = cms.untracked.string("None") # Options: None, chi, std, Bselection, Wselection

transverseMassCut = cms.untracked.double(100) # Not used

EvtTopology = cms.untracked.PSet(
    #discriminator = cms.untracked.string("test"),
    #discriminatorCut = cms.untracked.double(0.0),
    #alphaT = cms.untracked.double(-5.00)
    alphaT = cms.untracked.double(-5.0), #cut on values >=0 to enable
    sphericity = cms.untracked.double(-5.0), #cut on values =>0 (<= 1) to enable
    aplanarity = cms.untracked.double(-5.0), #cut on values =>0 (<= 0.5) to enable
    planarity = cms.untracked.double(-5.0),  #cut on values =>0 (<= 0.5) to enable
    circularity = cms.untracked.double(-5.0),#cut on values =>0 (<= 1) to enable
    Cparameter = cms.untracked.double(-5.0), #cut on values =>0 (<= 1) to enable
    Dparameter = cms.untracked.double(-5.0), #cut on values =>0 (<= 1) to enable
    jetThrust = cms.untracked.double(-5.0),  #cut on values =>0 (<= 1)to enable
)

ElectronSelection = cms.untracked.PSet(
    genParticleSrc = cms.untracked.InputTag("genParticles"),
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    conversionSrc = cms.untracked.InputTag("allConversions"),
    beamspotSrc = cms.untracked.InputTag("offlineBeamSpot"),
    rhoSrc = cms.untracked.InputTag("kt6PFJetsForEleIso", "rho"),
    ElectronSelectionVeto = cms.untracked.string("VETO"),
    ElectronSelectionTight = cms.untracked.string("TIGHT"),
    ElectronSelectionMedium = cms.untracked.string("MEDIUM"),
    ElectronPtCut = cms.untracked.double(15.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)

MuonSelection = cms.untracked.PSet(
    genParticleSrc = cms.untracked.InputTag("genParticles"),
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    applyMuonIsolation = cms.untracked.bool(True),
    MuonPtCut = cms.untracked.double(10.0),
    MuonEtaCut = cms.untracked.double(2.5),
)

InvMassVetoOnJets = cms.untracked.PSet(
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    #setTrueToUseModule = cms.untracked.bool(False)
    setTrueToUseModule = cms.untracked.bool(True)
)

fakeMETVeto = cms.untracked.PSet(
  minDeltaPhi = cms.untracked.double(10.) # in degrees
)

jetTauInvMass = cms.untracked.PSet(
  ZmassResolution = cms.untracked.double(5.0),
)

forwardJetVeto = cms.untracked.PSet(
  src = cms.untracked.InputTag("selectedPatJets"),  # PF jets
  ptCut = cms.untracked.double(30),
  etaCut = cms.untracked.double(2.4),
  ForwJetEtCut = cms.untracked.double(10.0),
  ForwJetEtaCut = cms.untracked.double(2.5),
  EtSumRatioCut = cms.untracked.double(0.2)
 )

GenParticleAnalysis = cms.untracked.PSet(
  src = cms.untracked.InputTag("genParticles"),
  metSrc = cms.untracked.InputTag("genMetTrue"),
  oneProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"),
  oneAndThreeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng"),
  threeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauThreeProng"),
  enabled = cms.untracked.bool(True),
)


topSelection = cms.untracked.PSet(
  TopMassLow = cms.untracked.double(120.0),
  TopMassHigh = cms.untracked.double(300.0),
  src = cms.untracked.InputTag("genParticles")
)

bjetSelection = cms.untracked.PSet(
  src = cms.untracked.InputTag("genParticles"),
  oneProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"),
  oneAndThreeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng") 
)

MCAnalysisOfSelectedEvents = cms.untracked.PSet(
  src = cms.untracked.InputTag("genParticles"),
  oneProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"),
  oneAndThreeProngTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng") 
)


topChiSelection = cms.untracked.PSet(
    TopMassLow = cms.untracked.double(120.0),
    TopMassHigh = cms.untracked.double(300.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)

topWithBSelection = cms.untracked.PSet(
    TopMassLow = cms.untracked.double(120.0),
    TopMassHigh = cms.untracked.double(300.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)

topWithWSelection = cms.untracked.PSet(
    TopMassLow = cms.untracked.double(120.0),
    TopMassHigh = cms.untracked.double(300.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)

topWithMHSelection = cms.untracked.PSet(
    TopMassLow = cms.untracked.double(120.0),
    TopMassHigh = cms.untracked.double(300.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)


topWithMHSelection = cms.untracked.PSet(
        TopMassLow = cms.untracked.double(120.0),
        TopMassHigh = cms.untracked.double(300.0),
        Chi2Cut = cms.untracked.double(5.0),
        src = cms.untracked.InputTag("genParticles"),
        enabled = cms.untracked.bool(False)
)

def SetHistogramBinSettings(nbins, axismin, axismax):
    return cms.untracked.PSet(
        nBins = cms.untracked.uint32(nbins), # Number of bins for axis
        axisMin = cms.untracked.double(axismin), # Minimum value in axis
        axisMax = cms.untracked.double(axismax) # Maximum value in axis
        )

commonPlotsSettings = cms.untracked.PSet(
    enableTauFakeRateAnalysis = cms.untracked.bool(True),
    enableNormalisationAnalysis = cms.untracked.bool(True),
    enableMETOscillationAnalysis = cms.untracked.bool(True),
    # Histogram splitting (useful for QCD measurements and detailed studies)
    histogramSplitting = cms.untracked.PSet(
        #splitHistogramByTauPtBinLowEdges = cms.untracked.vdouble(41., 50., 60., 70., 80., 100., 120., 150., 200., 300.)
        #splitHistogramByTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, 1.5) # probably need to constrain to -1.5, 1.5, i.e. endcap-, barrel, endcap+
        #splitHistogramByNVerticesBinLowEdges = cms.untracked.vint32(10)
        #splitHistogramByDeltaPhiTauMetInDegrees = cms.untracked.vdouble(90.)
    ),
    # Histogram dimension definitions for control plots and shapes (input for datacard generator)
    ptBins = SetHistogramBinSettings(50, 0., 500.),
    etaBins = SetHistogramBinSettings(60, -3., 3.),
    phiBins = SetHistogramBinSettings(72, -3.1415926, 3.1415926),
    rtauBins = SetHistogramBinSettings(55, 0., 1.1),
    njetsBins = SetHistogramBinSettings(20, 0., 20.),
    metBins = SetHistogramBinSettings(50, 0., 500.),
    tailKiller1DBins = SetHistogramBinSettings(52, 0., 260.),
    topMassBins = SetHistogramBinSettings(50, 0., 500.),
    WMassBins = SetHistogramBinSettings(60, 0., 300.),
    mtBins = SetHistogramBinSettings(50, 0., 500.),
    invmassBins = SetHistogramBinSettings(50, 0., 500.),
)

tree = cms.untracked.PSet(
    fill = cms.untracked.bool(True),
    fillJetEnergyFractions = cms.untracked.bool(False), # Disabled by LAW on 25.4.2013 (not very useful anymore because jets are smeared)
    fillNonIsoLeptonVars = cms.untracked.bool(False),
    tauIDs = cms.untracked.vstring(
        "byTightCombinedIsolationDeltaBetaCorr",
        "byMediumCombinedIsolationDeltaBetaCorr",
        "byLooseCombinedIsolationDeltaBetaCorr",
        "byTightCombinedIsolationDeltaBetaCorr3Hits",
        "byMediumCombinedIsolationDeltaBetaCorr3Hits",
        "byLooseCombinedIsolationDeltaBetaCorr3Hits",
        "againstElectronMVA",
        "againstElectronTightMVA3",
        "againstElectronLoose",
        "againstElectronMedium",
        "againstElectronTight",
        "againstMuonLoose",
        "againstMuonTight",
        "againstMuonTight2",

    ),
    genParticleSrc = cms.untracked.InputTag("genParticles")
)

eventCounter = cms.untracked.PSet(
    counters = cms.untracked.VInputTag()
)

prescaleWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("hplusPrescaleWeightProducer"),
    enabled = cms.bool(False),
)

wjetsWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("wjetsWeight"),
    enabled = cms.bool(False),
)

embeddingGeneratorWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("generator", "weight"),
    enabled = cms.bool(False),
)

embeddingWTauMuWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("wtaumuWeight"),
    enabled = cms.bool(False)
)

vertexWeight = cms.untracked.PSet(
    vertexSrc = cms.InputTag("goodPrimaryVertices"),
#    vertexSrc = cms.InputTag("goodPrimaryVertices10"),
    puSummarySrc = cms.InputTag("addPileupInfo"),
    dataPUdistribution = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData2011.root"),
    dataPUdistributionLabel = cms.string("pileup"),
    mcPUdistribution = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramMCFall11.root"),
    mcPUdistributionLabel = cms.string("pileup"),
    weightDistribution = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/weights_2011AB.root"),
    weightDistributionLabel = cms.string("weights"),
    weightDistributionEnable = cms.bool(False),
    enabled = cms.bool(False),
)

pileupWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("PUVertexWeightNominal"),
    enabled = cms.bool(False),
)

topPtWeightReader = cms.untracked.PSet(
    weightSrc = cms.InputTag("topPtWeightNominal"),
    enabled = cms.bool(False),
)

# Default parameters for heavy H+ analysis
def cloneForHeavyAnalysis(lightModule):
    heavyModule = lightModule.clone()
    # Insert here all parameter updates heavy H+ needs on top of the light H+ analysis
    # 'lightModule' is essentially process.signalAnalysis (or equivalent)
    return heavyModule

# Set trigger efficiency / scale factor depending on tau selection params
triggerEffPrototype = cms.untracked.PSet(
    data = cms.FileInPath("NOT_YET_SET"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("NOT_YET_SET"),
    mode = cms.untracked.string("disabled"), # mcEfficiency, dataEfficiency, scaleFactor, disabled
    variationEnabled = cms.bool(False),
    useMaxUncertainty = cms.bool(True),
)

import HiggsAnalysis.HeavyChHiggsToTauNu.tauLegTriggerEfficiency2011_cff as tauTriggerEfficiency
def setTriggerEfficiencyScaleFactorBasedOnTau(scaleFactorPSet, tausele, mod="HChSignalAnalysisParameters_cff"):
    print "Trigger efficiency / scalefactor set according to tau isolation '%s' and tau against electron discr. '%s' for %s" % (tausele.isolationDiscriminator.value(), tausele.againstElectronDiscriminator.value(), mod)
    tauTriggerEfficiency.setEfficiency(scaleFactorPSet, "byMediumCombinedIsolationDeltaBetaCorr", "againstElectronMedium") # FIXME changed default to best so far
    return
    # FIXME
    tauTriggerEfficiency.setEfficiency(scaleFactorPSet, tausele.isolationDiscriminator.value(), tausele.againstElectronDiscriminator.value())
    raise Exception("Tau trigger efficencies/scale factors are only available for:\n  tau isolation: 'byLooseCombinedIsolationDeltaBetaCorr3Hits', 'byMediumCombinedIsolationDeltaBetaCorr3Hits'\n  against electron discr.: 'againstElectronMedium', 'againstElectronMVA' (MVA not available for VLoose isol.)")
# Set trigger efficiency / scale factor for low purity depending on tau selection params
def setTriggerEfficiencyLowPurityScaleFactorBasedOnTau(scaleFactorPSet, tausele, mod="HChSignalAnalysisParameters_cff"):
    import HiggsAnalysis.HeavyChHiggsToTauNu.tauLegTriggerEfficiency2011_cff as tauTriggerEfficiency # FIXME
    print "Trigger efficiency / scalefactor set according to tau isolation '%s' and tau against electron discr. '%s' for %s" % (tausele.isolationDiscriminator.value(), tausele.againstElectronDiscriminator.value(), mod)
    tauTriggerEfficiency.setEfficiency(scaleFactorPSet, "byMediumCombinedIsolationDeltaBetaCorr", "againstElectronMedium") # FIXME changed default to best so far

#triggerEfficiencyScaleFactor = TriggerEfficiency.tauLegEfficiency
tauTriggerEfficiencyScaleFactor = triggerEffPrototype.clone()
setTriggerEfficiencyScaleFactorBasedOnTau(tauTriggerEfficiencyScaleFactor, tauSelection)

import HiggsAnalysis.HeavyChHiggsToTauNu.metLegTriggerEfficiency2011_cff as metTriggerEfficiency
metTriggerEfficiencyScaleFactor = triggerEffPrototype.clone()
metTriggerEfficiency.setEfficiency(metTriggerEfficiencyScaleFactor)

# Muon trigger+ID efficiencies, for embedding normalization
import HiggsAnalysis.HeavyChHiggsToTauNu.muonTriggerIDEfficiency_cff as muonTriggerIDEfficiency
#embeddingMuonEfficiency = muonTriggerIDEfficiency.efficiency
#embeddingMuonEfficiency.variationEnabled = cms.bool(False)
#embeddingMuonEfficiency.variationShiftBy = cms.double(0)

embeddingMuonIdEfficiency = muonTriggerIDEfficiency.efficiency_ID
embeddingMuonIdEfficiency.variationEnabled = cms.bool(False)
embeddingMuonIdEfficiency.useMaxUncertainty = cms.bool(True)

embeddingMuonTriggerEfficiency = muonTriggerIDEfficiency.efficiency_trigger
embeddingMuonTriggerEfficiency.variationEnabled = cms.bool(False)
embeddingMuonTriggerEfficiency.useMaxUncertainty = cms.bool(True)

# Look up dynamically the triggers for which the parameters exist
#import HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEfficiency_cff as trigEff
#for triggerName in filter(lambda n: len(n) > 4 and n[0:4] == "HLT_", dir(trigEff)):
#    setattr(triggerEfficiency.parameters, triggerName, getattr(trigEff, triggerName))

# Functions
def overrideTriggerFromOptions(options):
    if isinstance(options.trigger, basestring) and options.trigger != "":
        trigger.triggers = [options.trigger]
    elif len(options.trigger) > 0:
        trigger.triggers = options.trigger

def _getTriggerVertexArgs(kwargs):
    effargs = {}
    vargs = {}
    effargs.update(kwargs)
    if "module" in effargs:
        module = effargs["module"]
        del effargs["module"]
        effargs["pset"] = module.triggerEfficiency
        vargs["pset"] = module.vertexWeight
    return (effargs, vargs)

def _setTriggerEfficiencyForEraMC(dataVersion, era, pset):
    if dataVersion.isS4():
        pset.mcSelect = "Summer11"
    elif dataVersion.isS6():
        if era == "Run2011A":
            pset.mcSelect = "Fall11_PU_2011A"
        if era == "Run2011B":
            pset.mcSelect = "Fall11_PU_2011B"
        if era == "Run2011AB":
            pset.mcSelect = "Fall11_PU_2011AB"
    elif dataVersion.isHighPU():
        pset.mode = "disabled"
    else:
        raise Exception("MC trigger efficencies are available only for Summer11 and Fall11")

def setTauTriggerEfficiencyForEra(dataVersion, era, pset):
    if dataVersion.isMC():
        _setTriggerEfficiencyForEraMC(dataVersion, era, pset)
    pset.dataSelect = tauTriggerEfficiency.getRunsForEra(era)

def setMetTriggerEfficiencyForEra(dataVersion, era, pset):
    if dataVersion.isMC():
        _setTriggerEfficiencyForEraMC(dataVersion, era, pset)
    pset.dataSelect = metTriggerEfficiency.getRunsForEra(era)

# Weighting by instantaneous luminosity, and the number of true
# simulated pile up interactions
# See test/PUtools for tools to generate distributions and links to twiki
# 

def setPileupWeight(dataVersion, process, commonSequence, pset=vertexWeight, psetReader=pileupWeightReader, era="Run2011A", suffix="", histogramAmbientLevel="Informative"):
    if dataVersion.isData():
        return
    if dataVersion.isS6():
        # Fall11
        pset.mcPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramMCFall11.root"
        pset.mcPUdistributionLabel = "pileup"
    elif dataVersion.isHighPU():
	# High PU - disable vertex reweighting
        pset.enabled = False
        psetReader.enabled = False
        return
    else:
        raise Exception("No PU reweighting support for anything else than Fall11 S6 scenario at the moment")
    pset.enabled = True
    psetReader.enabled = True

    if era == "Run2011A" or era == "Run2011B":
        pset.dataPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData"+era.replace("Run","")+suffix+".root"
        pset.weightDistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/weights_"+era.replace("Run","")+".root"
    elif era == "Run2011AB":
        pset.dataPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData2011"+suffix+".root"
    else:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are 'Run2011A', 'Run2011B', 'Run2011AB'" % era)
    pset.dataPUdistributionLabel = "pileup"
    # Make procuder for weights and add it to common sequence
    tmp = pset.clone()
    PUWeightProducer = cms.EDProducer("HPlusVertexWeightProducer",
                                      vertexSrc = tmp.vertexSrc,
                                      puSummarySrc = tmp.puSummarySrc,
                                      enabled = tmp.enabled,
                                      histogramAmbientLevel = cms.untracked.string(histogramAmbientLevel),
                                      dataPUdistribution = tmp.dataPUdistribution,
                                      dataPUdistributionLabel = tmp.dataPUdistributionLabel,
                                      mcPUdistribution = tmp.mcPUdistribution,
                                      mcPUdistributionLabel = tmp.mcPUdistributionLabel,
                                      weightDistribution = tmp.weightDistribution,
                                      weightDistributionLabel = tmp.weightDistributionLabel,
                                      weightDistributionEnable = tmp.weightDistributionEnable,
                                      alias = cms.string("PUVertexWeight"+era+suffix)
    )
    name = "PUWeightProducer"+era+suffix
    setattr(process, name, PUWeightProducer)
    commonSequence *= PUWeightProducer
    psetReader.weightSrc = name
    return name

def setPileupWeightForVariation(dataVersion, process, commonSequence, pset, psetReader, suffix, histogramAmbientLevel="Informative"):
    if dataVersion.isData():
        return
    if dataVersion.isS6():
        # Fall11
        pset.mcPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramMCFall11.root"
        pset.mcPUdistributionLabel = "pileup"
    elif dataVersion.isHighPU():
	# High PU - disable vertex reweighting
        pset.enabled = False
        psetReader.enabled = False
        return
    else:
        raise Exception("No PU reweighting support for anything else than Fall11 S6 scenario at the moment")
    pset.enabled = True
    psetReader.enabled = True

    # None means to use the existing, just replace the suffix
    pset.dataPUdistribution = pset.dataPUdistribution.value().replace(".root", suffix+".root")
    pset.dataPUdistributionLabel = "pileup"
    # Make procuder for weights and add it to common sequence
    PUWeightProducer = cms.EDProducer("HPlusVertexWeightProducer",
                                      vertexSrc = pset.vertexSrc,
                                      puSummarySrc = pset.puSummarySrc,
                                      enabled = pset.enabled,
                                      histogramAmbientLevel = cms.untracked.string(histogramAmbientLevel),
                                      dataPUdistribution = pset.dataPUdistribution,
                                      dataPUdistributionLabel = pset.dataPUdistributionLabel,
                                      mcPUdistribution = pset.mcPUdistribution,
                                      mcPUdistributionLabel = pset.mcPUdistributionLabel,
                                      weightDistribution = pset.weightDistribution,
                                      weightDistributionLabel = pset.weightDistributionLabel,
                                      weightDistributionEnable = pset.weightDistributionEnable,
                                      alias = cms.string("PUVertexWeight"+suffix)
    )
    name = psetReader.weightSrc.value()+suffix
    setattr(process, name, PUWeightProducer)
    commonSequence *= PUWeightProducer
    psetReader.weightSrc = name
    return name

# Tau selection
def forEachTauSelection(function):
    for selection in tauSelections:
        function(selection)

def setAllTauSelectionOperatingMode(mode):
    forEachTauSelection(lambda x: x.operatingMode.setValue(mode))

def setAllTauSelectionSrcSelectedPatTaus():
    tauSelectionHPSTightTauBased.src        = "selectedPatTausHpsPFTau"
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTau"
    tauSelectionHPSLooseTauBased.src        = "selectedPatTausHpsPFTau"

def setAllTauSelectionSrcSelectedPatTausTriggerMatched():
    tauSelectionHPSTightTauBased.src        = "patTausHpsPFTauTriggerMatched"
    tauSelectionHPSMediumTauBased.src       = "patTausHpsPFTauTriggerMatched"
    tauSelectionHPSLooseTauBased.src        = "patTausHpsPFTauTriggerMatched"
    
def addTauIdAnalyses(process, dataVersion, prefix, prototype, commonSequence, additionalCounters):
    from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection

    selections = tauSelections[:]
    names = tauSelectionNames[:]
    # HPS loose
    hpsLoose = selections.index(tauSelectionHPSLooseTauBased)
    #del selections[hpsLoose]
    #del names[hpsLoose]

    for selection, name in zip(selections, names):
        module = prototype.clone()
        module.tauSelection = selection.clone()

        # Calculate type 1 MET
        raise Exception("This needs further adjustment")
        type1Sequence = MetCorrection.addCorrectedMet(process, dataVersion, module, postfix=name)

        seq = cms.Sequence(
            commonSequence *
            type1Sequence
        )
        setattr(process, "commonSequence"+name, seq)

        addAnalysis(process, prefix+name, module,
                    preSequence=seq,
                    additionalCounters=additionalCounters)

def setJetPUIdSrc(jetSelectionPSet, moduleName):
    # Check PUID type validity
    myPUIDType = jetSelectionPSet.jetPileUpType.value()
    myValidPUIDTypes = ["full", "cutbased", "philv1", "simple", "none"]
    if not (myPUIDType in myValidPUIDTypes):
        raise Exception("jet PU ID type '%s' is not valid! (options: %s)"%(myPUIDType,", ".join(myValidPUIDTypes)))
    # Check PUID working point validity
    myPUIDWP = jetSelectionPSet.jetPileUpWorkingPoint.value()
    myValidPUIDWPs = ["tight", "medium", "loose"]
    if not (myPUIDWP in myValidPUIDWPs):
        raise Exception("jet PU ID working point '%s' is not valid! (options: %s)"%(myPUIDWP,", ".join(myValidPUIDWPs)))
    # Set jet PU ID src
    mySrc = jetSelectionPSet.src.value()
    mySrc.replace("Chs","") # Take out the suffix to reduce if sentences
    try:
        myPileUpSrc = jetSelectionPSet.jetPileUpJetCollectionPrefix.value() + {
            "selectedPatJets":                "",
            "smearedPatJets":                 "ForsmearedPatJets",
            "shiftedPatJetsEnDownForCorrMEt": "ForshiftedPatJetsEnDownForCorrMEt",
            "shiftedPatJetsEnUpForCorrMEt":   "ForshiftedPatJetsEnUpForCorrMEt",
            "smearedPatJetsResDown":          "ForsmearedPatJetsResDown",
            "smearedPatJetsResUp":            "ForsmearedPatJetsResUp",
            }[mySrc]
    except KeyError:
        raise Exception("Cannot set jet PU ID src for unknown jet src '%s' in module '%s'"%(jetSelection.src.value(),moduleName))
    # Add suffix
    if "Chs" in jetSelection.src.value():
        myPileUpSrc += "Chs"
    if myPUIDType != "none":
        jetSelectionPSet.jetPileUpMVAValues = cms.untracked.InputTag(myPileUpSrc, myPUIDType+"Discriminant")
        jetSelectionPSet.jetPileUpIdFlag = cms.untracked.InputTag(myPileUpSrc, myPUIDType+"Id")
    else:
        jetSelectionPSet.jetPileUpMVAValues = cms.untracked.InputTag("None")
        jetSelectionPSet.jetPileUpIdFlag = cms.untracked.InputTag("None")
    print "Jet PU Id src set to '%s' based on jet source '%s' in module '%s'"%(myPileUpSrc,jetSelection.src.value(),moduleName)

def _changeCollection(inputTags, moduleLabel=None, instanceLabel=None, processName=None):
    for tag in inputTags:
        if moduleLabel != None:
            tag.setModuleLabel(moduleLabel)
        if instanceLabel != None:
            tag.setProductInstanceLabel(instanceLabel)
        if processName != None:
            tag.setProcessName(processName)

def changeJetCollection(**kwargs):
    _changeCollection([jetSelection.src, forwardJetVeto.src], **kwargs)

def setJERSmearedJets(dataVersion):
    if dataVersion.isMC():
        if jetSelection.src.value() == "selectedPatJets":
            print "Using JER-smeared jets"
            changeJetCollection(moduleLabel="smearedPatJets")
        elif jetSelection.src.value() == "selectedPatJetsChs":
            print "Using JER-smeared CHS jets"
            changeJetCollection(moduleLabel="smearedPatJetsChs")
        else:
            raise Exception("Unsupported value for jet src %s, expected 'selectedPatJets' or 'selectedPatJetsChs'" % jetSelection.src.value())

def changeCollectionsToPF2PAT(dataVersion, postfix="PFlow", useGSFElectrons=True):
    # Taus
    hps = "selectedPatTaus"+postfix
    if "TriggerMatched" in tauSelectionHPSTightTauBased.src.value():
        hps = "patTaus%sTriggerMatched%s" % (postfix, postfix)

    tauSelectionHPSTightTauBased.src = hps
    tauSelectionHPSMediumTauBased.src = hps
    tauSelectionHPSLooseTauBased.src = hps
    tauSelectionHPSVeryLooseTauBased.src = hps
    vetoTauSelection.tauSelection.src = "selectedPatTaus"+postfix


    # Muons
    GlobalMuonVeto.MuonCollectionName = "selectedPatMuons"+postfix
    NonIsolatedMuonVeto.MuonCollectionName = "selectedPatMuons"+postfix

    # Electrons
    if useGSFElectrons:
        print "Using GSF electrons despite of PF2PAT"
    else:
        GlobalElectronVeto.ElectronCollectionName = "selectedPatElectrons"+postfix
        NonIsolatedElectronVeto.ElectronCollectionName = "selectedPatElectrons"+postfix

    # Jets
    if dataVersion.isData():
        changeJetCollection(moduleLabel="selectedPatJets"+postfix)
    else:
        changeJetCollection(moduleLabel="smearedPatJets"+postfix)

    # MET
    MET.caloSrc = "Nonexistent"
    MET.tcSrc = "Nonexistent"
    MET.rawSrc = "patPFMet"
    MET.type1Src = "patType1CorrectedPFMet"
    MET.type2Src = "patType1p2CorrectedPFMet"
