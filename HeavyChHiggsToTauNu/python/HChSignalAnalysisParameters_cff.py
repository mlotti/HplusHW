import FWCore.ParameterSet.Config as cms

# Blind analysis - do not fill final counter and histogram for data if true
blindAnalysisStatus = cms.untracked.bool(False);

singleTauMetTriggerPaths = [
#    "HLT_SingleLooseIsoTau20",
#    "HLT_SingleLooseIsoTau20_Trk5",
#    "HLT_SingleIsoTau20_Trk5",
#    "HLT_SingleIsoTau20_Trk15_MET20",
#    "HLT_SingleIsoTau20_Trk15_MET25_v3",
#    "HLT_SingleIsoTau20_Trk15_MET25_v4",
    "HLT_IsoPFTau35_Trk20_MET45_v1",
    "HLT_IsoPFTau35_Trk20_MET45_v2",
    "HLT_IsoPFTau35_Trk20_MET45_v4",
    "HLT_IsoPFTau35_Trk20_MET45_v6",
    "HLT_IsoPFTau35_Trk20_MET60_v2",
    "HLT_IsoPFTau35_Trk20_MET60_v3",
    "HLT_IsoPFTau35_Trk20_MET60_v4",
    "HLT_IsoPFTau35_Trk20_MET60_v6",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
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

primaryVertexSelection = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPrimaryVertex"),
    enabled = cms.untracked.bool(True)
)

# Default tau selection
tauSelectionBase = cms.untracked.PSet(
    # Operating mode options: 'standard'
    operatingMode = cms.untracked.string("standard"), # Standard tau ID (Tau candidate selection + tau ID applied)
    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(40), # jet pt > value
    etaCut = cms.untracked.double(2.1), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(20.0), # ldg. track > value
    againstElectronDiscriminator = cms.untracked.string("againstElectronMedium"), # discriminator against electrons
    againstMuonDiscriminator = cms.untracked.string("againstMuonTight"), # discriminator for against muons
    isolationDiscriminator = cms.untracked.string("byMediumCombinedIsolationDeltaBetaCorr"), # discriminator for isolation
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1.0), # cut point for continuous isolation discriminator, applied only if it is non-zero
    rtauCut = cms.untracked.double(0.7), # rtau > value
    nprongs = cms.untracked.uint32(1) # number of prongs (options: 1, 3, or 13 == 1 || 3)
)

# Only HPS should be used (ignore TCTau, plain PF, TaNC, and Combined HPS+TaNC)

tauSelectionHPSTightTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byTightCombinedIsolationDeltaBetaCorr",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

tauSelectionHPSMediumTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byMediumCombinedIsolationDeltaBetaCorr",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

tauSelectionHPSLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byLooseCombinedIsolationDeltaBetaCorr",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

tauSelectionHPSVeryLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTauBased",
    isolationDiscriminator = "byVLooseCombinedIsolationDeltaBetaCorr",
    isolationDiscriminatorContinuousCutPoint = cms.untracked.double(-1)
)

vetoTauBase = tauSelectionHPSVeryLooseTauBased.clone(
    ptCut = cms.untracked.double(15), # jet pt > value
    etaCut = cms.untracked.double(2.5), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(5.0), # ldg. track > value
#    isolationDiscriminator = "byVLooseIsolation",
    rtauCut = cms.untracked.double(0.0), # rtau > value
    nprongs = cms.untracked.uint32(1) # number of prongs (options: 1, 3, or 13 == 1 || 3)
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

jetSelectionBase = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    cleanTauDR = cms.untracked.double(0.5), # cone for rejecting jets around tau jet
    ptCut = cms.untracked.double(20.0),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3), # minimum number of selected jets # FIXME rename minNumber to jetNumber
    jetNumber = cms.untracked.uint32(3), # minimum number of selected jets # FIXME rename minNumber to jetNumber
    jetNumberCutDirection = cms.untracked.string("GEQ"), # direction of jet number cut direction, options: NEQ, EQ, GT, GEQ, LT, LEQ
    # Jet ID cuts
    jetIdMaxNeutralHadronEnergyFraction = cms.untracked.double(0.99),
    jetIdMaxNeutralEMEnergyFraction = cms.untracked.double(0.99),
    jetIdMinNumberOfDaughters = cms.untracked.uint32(2),
    jetIdMinChargedHadronEnergyFraction = cms.untracked.double(0.0),
    jetIdMinChargedMultiplicity = cms.untracked.uint32(0),
    jetIdMaxChargedEMEnergyFraction = cms.untracked.double(0.99),
    # Pileup cleaning
    betaCut = cms.untracked.double(0.0), # disabled
    betaCutSource = cms.untracked.string("beta"), # tag name in user floats
    betaCutDirection = cms.untracked.string("GT"), # direction of beta cut direction, options: NEQ, EQ, GT, GEQ, LT, LEQ
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

jetSelection = jetSelectionLoose # set default jet selection

MET = cms.untracked.PSet(
    rawSrc = cms.untracked.InputTag("patMETsPF"), # PF MET
    type1Src = cms.untracked.InputTag("dummy"),
    type2Src = cms.untracked.InputTag("dummy"),
    caloSrc = cms.untracked.InputTag("patMETs"),
    tcSrc = cms.untracked.InputTag("patMETsTC"),
    select = cms.untracked.string("type1"), # raw, type1, type2
    METCut = cms.untracked.double(50.0),

    # For type I/II correction
    tauJetMatchingCone = cms.untracked.double(0.5),
    jetType1Threshold = cms.untracked.double(10),
    jetOffsetCorrLabel = cms.untracked.string("L1FastJet"),
    #type2ScaleFactor = cms.untracked.double(1.4),
)

bTagging = cms.untracked.PSet(
    # jetBProbabilityBJetTags,jetProbabilityBJetTags,trackCountingHighPurBJetTags,trackCountingHighEffBJetTags,simpleSecondaryVertexHighEffBJetTags,simpleSecondaryVertexHighPurBJetTags,combinedSecondaryVertexBJetTags,combinedSecondaryVertexMVABJetTags,softMuonBJetTags,softMuonByPtBJetTags,softMuonByIP3dBJetTags
#   OP: JPL = 0.275, LPM = 0.545, JPT = 0.790, CSVL = 0.244, CSVM = 0.679, CSVT = 0.898
#    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminator = cms.untracked.string("combinedSecondaryVertexBJetTags"),
    discriminatorCut = cms.untracked.double(0.679),
    ptCut = cms.untracked.double(30.0),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1), #FIXME change minNumber to jetNumber
    jetNumber = cms.untracked.uint32(1), #FIXME change minNumber to jetNumber
    jetNumberCutDirection = cms.untracked.string("GEQ") # direction of jet number cut direction, options: NEQ, EQ, GT, GEQ, LT, LEQ
)

deltaPhiTauMET = cms.untracked.double(160.0) # less than this value in degrees
topReconstruction = cms.untracked.string("None") # Options: None

transverseMassCut = cms.untracked.double(100) # Not used

EvtTopology = cms.untracked.PSet(
    #discriminator = cms.untracked.string("test"),
    #discriminatorCut = cms.untracked.double(0.0),
    #alphaT = cms.untracked.double(-5.00)
    alphaT = cms.untracked.double(-5.0)
)

GlobalElectronVeto = cms.untracked.PSet(
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    ElectronSelection = cms.untracked.string("simpleEleId95relIso"),
    ElectronPtCut = cms.untracked.double(15.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)

NonIsolatedElectronVeto = cms.untracked.PSet(
    ElectronCollectionName = cms.untracked.InputTag("selectedPatElectrons"),
    ElectronSelection = cms.untracked.string("simpleEleId60relIso"),
    ElectronPtCut = cms.untracked.double(10.0),
    ElectronEtaCut = cms.untracked.double(2.5)
)

GlobalMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("GlobalMuonPromptTight"),
    MuonPtCut = cms.untracked.double(15.0),
    MuonEtaCut = cms.untracked.double(2.5),  
    MuonApplyIpz = cms.untracked.bool(False) # Apply IP-z cut
)

NonIsolatedMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("AllGlobalMuons"),
    MuonPtCut = cms.untracked.double(5.0),
    MuonEtaCut = cms.untracked.double(2.5),  
    MuonApplyIpz = cms.untracked.bool(False) # Apply IP-z cut
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
  src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
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
)
topSelection = cms.untracked.PSet(
  TopMassLow = cms.untracked.double(100.0),
  TopMassHigh = cms.untracked.double(300.0),
  src = cms.untracked.InputTag("genParticles")
)

bjetSelection = cms.untracked.PSet(
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
    TopMassHigh = cms.untracked.double(250.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)

topWithWSelection = cms.untracked.PSet(
    TopMassLow = cms.untracked.double(120.0),
    TopMassHigh = cms.untracked.double(250.0),
    Chi2Cut = cms.untracked.double(5.0),
    src = cms.untracked.InputTag("genParticles"),
    enabled = cms.untracked.bool(False)
)

tree = cms.untracked.PSet(
    fill = cms.untracked.bool(True),
    fillJetEnergyFractions = cms.untracked.bool(True),
    tauIDs = cms.untracked.vstring(
        "byTightIsolation",
        "byMediumIsolation",
        "byLooseIsolation",
        "againstElectronLoose",
        "againstElectronMedium",
        "againstElectronTight",
        "againstMuonLoose",
        "againstMuonTight",
    ),
    genParticleSrc = cms.untracked.InputTag("genParticles")
)

vertexWeight = cms.untracked.PSet(
    vertexSrc = cms.InputTag("goodPrimaryVertices"),
#    vertexSrc = cms.InputTag("goodPrimaryVertices10"),
    puSummarySrc = cms.InputTag("addPileupInfo"),
    dataPUdistribution = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData2011.root"),
    dataPUdistributionLabel = cms.string("pileup"),
    mcPUdistribution = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramMCFall11.root"),
    mcPUdistributionLabel = cms.string("pileup"),
    enabled = cms.bool(False),
)

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )
triggerEfficiencyScaleFactor = cms.untracked.PSet(
    # The selected triggers for the efficiency. If one trigger is
    # given, the parametrization of it is used as it is (i.e.
    # luminosity below is ignored). If multiple triggers are given,
    # their parametrizations are used weighted by the luminosities
    # given below.
    # selectTriggers = cms.VPSet(
    #     cms.PSet(
    #         trigger = cms.string("HLT_IsoPFTau35_Trk20_EPS"),
    #         luminosity = cms.double(0)
    #     ),
    # ),
    # The parameters of the trigger efficiency parametrizations,
    # looked dynamically from TriggerEfficiency_cff.py
    dataParameters = cms.PSet(
        # L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20
        runs_160431_167913 = cms.PSet(
            firstRun = cms.uint32(160431),
            lastRun = cms.uint32(167913),
            luminosity = cms.double(1145.897000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.515873,  0.04844569),
                triggerBin(50, 0.8571429, 0.1583514),
                triggerBin(60, 0.8571429, 0.2572427),
                triggerBin(80, 0.8571429, 0.2572427)
            ),
        ),
        # L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(780.396000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.666667, 0.101509),
                triggerBin(50, 1,        0.369032),
                triggerBin(60, 1,        0.369032),
                triggerBin(80, 1,        0.8415)
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)
        runs_173236_173692 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(246.527000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.6, 0.204692),
                triggerBin(50, 1,   0.458818),
                triggerBin(60, 1,   0.369032),
                triggerBin(80, 1,   0.8415)
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175860_180252 = cms.PSet(
        ),
    ),
    mcParameters = cms.PSet(
        Summer11 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(40, 0.6168224, 0.03608822),
                triggerBin(50, 0.8809524, 0.07255525),
                triggerBin(60, 0.8125,    0.1494758),
                triggerBin(80, 1,         0.1682306)
            ),
        ),
        # Placeholder until efficiencies have been measured
        Fall11 = cms.PSet(
        ), 
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

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

def setDataTriggerEfficiency(dataVersion, era):
    if dataVersion.isMC():
        if dataVersion.isS4():
            triggerEfficiencyScaleFactor.mcSelect = "Summer11"
        elif dataVersion.isS6():
            triggerEfficiencyScaleFactor.mcSelect = "Fall11"
        elif dataVersion.isHighPU():
	    triggerEfficiencyScaleFactor.mode = "disabled"
        else:
            raise Exception("MC trigger efficencies are available only for Summer11 and Fall11")
    
    if era == "EPS":
        triggerEfficiencyScaleFactor.dataSelect = ["runs_160431_167913"]
    elif era == "Run2011A":
        triggerEfficiencyScaleFactor.dataSelect = ["runs_160431_167913", "runs_170722_173198", "runs_173236_173692"]
    elif era == "Run2011A-EPS":
        triggerEfficiencyScaleFactor.dataSelect = ["runs_170722_173198", "runs_173236_173692"]
    elif era == "Run2011B":
        raise Exception("Tau trigger efficiencies are not yet measured for Run2011B")
    elif era == "Run2011A+B":
        raise Exception("Tau trigger efficiencies are not yet measured for Run2011B")
    else:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are 'EPS, 'Run2011A-EPS', 'Run2011A', 'Run2011B', 'Run2011A+B'")


# Weighting by instantaneous luminosity, and the number of true
# simulated pile up interactions
# See test/PUtools for tools to generate distributions and links to twiki

def setPileupWeight(dataVersion, pset=vertexWeight, era="Run2011A", suffix=""):
    if dataVersion.isData():
        return
    if dataVersion.isS6():
        # Fall11
        pset.mcPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramMCFall11.root"
        pset.mcPUdistributionLabel = "pileup"
    elif dataVersion.isHighPU():
	# High PU - disable vertex reweighting
        pset.enabled = False
        return
    else:
        raise Exception("No PU reweighting support for anything else than Fall11 S6 scenario at the moment")
    pset.enabled = True

    if era == "Run2011A" or era == "Run2011B":
        dataPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData"+era+suffix+".root"
    elif era == "Run2011A+B":
        dataPUdistribution = "HiggsAnalysis/HeavyChHiggsToTauNu/data/PileupHistogramData2011"+suffix+".root"
    else:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are 'Run2011A', 'Run2011B', 'Run2011A+B'" % era)
    dataPUdistributionLabel = "pileup"

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
    tauSelectionHPSTightTauBased.src        = "patTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSMediumTauBased.src       = "patTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSLooseTauBased.src        = "patTausHpsPFTauTauTriggerMatched"
    
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

def changeCollectionsToPF2PAT(postfix="PFlow"):
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
    GlobalElectronVeto.ElectronCollectionName = "selectedPatElectrons"+postfix
    NonIsolatedElectronVeto.ElectronCollectionName = "selectedPatElectrons"+postfix

    # Jets
    changeJetCollection(moduleLabel="selectedPatJets"+postfix)

    # MET
    MET.rawSrc = "patMETsPFlow"
    MET.caloSrc = "Nonexistent"
    MET.tcSrc = "Nonexistent"
