import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    src = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring("HLT_SingleLooseIsoTau20",
                                     "HLT_SingleLooseIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk15_MET20",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v3",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v4",
                                     "HLT_IsoPFTau35_Trk20_MET45_v1",
                                     "HLT_IsoPFTau35_Trk20_MET45_v2",
                                     "HLT_IsoPFTau35_Trk20_MET45_v4",
    ),
    hltMetCut = cms.untracked.double(45.0),
)
from HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEmulationEfficiency_cfi import *

primaryVertexSelection = cms.untracked.PSet(
    src = cms.untracked.InputTag("selectedPrimaryVertex"),
    enabled = cms.untracked.bool(True)
)

# Tau ID factorization map
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauIDFactorization_cfi as factorizationParams

# Default tau selection
tauSelectionBase = cms.untracked.PSet(
    # Operating mode options: 'standard', 'factorized', 'antitautag', 'antiisolatedtau'
    operatingMode = cms.untracked.string("standard"), # Standard tau ID (Tau candidate selection + tau ID applied)
#    operatingMode = cms.untracked.string("factorized"), # Tau candidate selection applied, tau ID factorized
#    operatingMode = cms.untracked.string("antitautag"), # Tau candidate selection applied, required prong cut, anti-isolation, and anti-rtau
#    operatingMode = cms.untracked.string("antiisolatedtau"), # Tau candidate selection applied, required prong cut and anti-isolation
    src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTauTauTriggerMatched"),
    selection = cms.untracked.string(""),
    ptCut = cms.untracked.double(40), # jet pt > value
    etaCut = cms.untracked.double(2.3), # jet |eta| < value
    leadingTrackPtCut = cms.untracked.double(20), # ldg. track > value
    rtauCut = cms.untracked.double(0.8), # rtau > value
    antiRtauCut = cms.untracked.double(0.4), # rtau < value
    invMassCut = cms.untracked.double(999.), # m(vis.tau) < value; FIXME has no effect in TauSelection.cc 
    nprongs = cms.untracked.uint32(1), # not used at the moment FIXME: has no effect in TauSelection.cc
    factorization = factorizationParams.tauIDFactorizationParameters
)

tauSelectionCaloTauCutBased = tauSelectionBase.clone(
    src = "selectedPatTausCaloRecoTauTauTriggerMatched",
    selection = "CaloTauCutBased"
)

tauSelectionShrinkingConeCutBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTauTauTriggerMatched",
    selection = "ShrinkingConePFTauCutBased"
)

tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTauTauTriggerMatched",
    selection = "ShrinkingConePFTauTaNCBased"
)

tauSelectionHPSTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTauTauTriggerMatched",
    selection = "HPSTauBased"
)

tauSelectionHPSMediumTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTauTauTriggerMatched",
    selection = "HPSMediumTauBased"
)

tauSelectionHPSLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTauTauTriggerMatched",
    selection = "HPSLooseTauBased"
)

tauSelectionCombinedHPSTaNCTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsTancPFTauTauTriggerMatched",
    selection = "CombinedHPSTaNCTauBased"
)


tauSelections = [tauSelectionCaloTauCutBased,
                 tauSelectionShrinkingConeCutBased,
                 tauSelectionShrinkingConeTaNCBased,
                 tauSelectionHPSTauBased,
                 tauSelectionHPSMediumTauBased,
                 tauSelectionHPSLooseTauBased,
                 tauSelectionCombinedHPSTaNCTauBased]
tauSelectionNames = ["TauSelectionCaloTauCutBased",
                     "TauSelectionShrinkingConeCutBased",
                     "TauSelectionShrinkingConeTaNCBased",
                     "TauSelectionHPSTightTauBased",
                     "TauSelectionHPSMediumTauBased",
                     "TauSelectionHPSLooseTauBased",
                     "TauSelectionCombinedHPSTaNCBased"]

#tauSelection = tauSelectionShrinkingConeCutBased
#tauSelection = tauSelectionShrinkingConeTaNCBased
#tauSelection = tauSelectionCaloTauCutBased
tauSelection = tauSelectionHPSTauBased
#tauSelection = tauSelectionHPSMediumTauBased
#tauSelection = tauSelectionCombinedHPSTaNCTauBased

jetSelection = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    src_met = cms.untracked.InputTag("patMETsPF"), # calo MET 
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3),
    METCut = cms.untracked.double(60.0)
)

MET = cms.untracked.PSet(
    # src = cms.untracked.InputTag("patMETs"), # calo MET
    src = cms.untracked.InputTag("patMETsPF"), # PF MET
    #src = cms.untracked.InputTag("patMETsTC"), # tc MET
    METCut = cms.untracked.double(70.0)
)

bTagging = cms.untracked.PSet(
    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminatorCut = cms.untracked.double(2.0),
    ptCut = cms.untracked.double(30),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1)
)

transverseMassCut = cms.untracked.double(100)

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

GlobalMuonVeto = cms.untracked.PSet(
    MuonCollectionName = cms.untracked.InputTag("selectedPatMuons"),
    MuonSelection = cms.untracked.string("GlobalMuonPromptTight"),
    MuonPtCut = cms.untracked.double(15.0),
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
  src = MET.src,
  minDeltaPhi = cms.untracked.double(10.) # in degrees
)

jetTauInvMass = cms.untracked.PSet(
  ZmassResolution = cms.untracked.double(5.0),
)

TauEmbeddingAnalysis = cms.untracked.PSet(
  embeddingMetSrc = MET.src,
  embeddingMode = cms.untracked.bool(False)
)

forwardJetVeto = cms.untracked.PSet(
  src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
  src_met = MET.src,
  ptCut = cms.untracked.double(30),
  etaCut = cms.untracked.double(2.4),
  ForwJetEtCut = cms.untracked.double(10.0),
  ForwJetEtaCut = cms.untracked.double(2.5),
  EtSumRatioCut = cms.untracked.double(0.2)
 )

GenParticleAnalysis = cms.untracked.PSet(
  ptCut = cms.untracked.double(40),
  etaCut = cms.untracked.double(2.3)
)
topSelection = cms.untracked.PSet(
  TopMassLow = cms.untracked.double(100.0),
  TopMassHigh = cms.untracked.double(300.0)
)

vertexWeight = cms.untracked.PSet(
    vertexSrc = cms.InputTag("goodPrimaryVertices10"),
    pileupSrc = cms.InputTag("PileupSummaryInfos"),
    useSimulatedPileup = cms.bool(False), # reweight by PileupSummaryInfo (True) or vertices (False)
    weights = cms.vdouble(1.0),
    enabled = cms.bool(False),
)

triggerEfficiency = cms.untracked.PSet(
    # The selected triggers for the efficiency. If one trigger is
    # given, the parametrization of it is used as it is (i.e.
    # luminosity below is ignored). If multiple triggers are given,
    # their parametrizations are used weighted by the luminosities
    # given below.
    selectTriggers = cms.VPSet(
        cms.PSet(
            trigger = cms.string("HLT_SingleIsoTau20_Trk15_MET25_v4"),
            luminosity = cms.double(2.270373344)
        ),
    ),
    # The parameters of the trigger efficiency parametrizations,
    # looked dynamically from TriggerEfficiency_cff.py
    parameters = cms.PSet()
)
# Look up dynamically the triggers for which the parameters exist
import HiggsAnalysis.HeavyChHiggsToTauNu.TriggerEfficiency_cff as trigEff
for triggerName in filter(lambda n: len(n) > 4 and n[0:4] == "HLT_", dir(trigEff)):
    setattr(triggerEfficiency.parameters, triggerName, getattr(trigEff, triggerName))

# Functions
def overrideTriggerFromOptions(options):
    if options.trigger != "":
        trigger.triggers = [options.trigger]


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

def setTriggerVertexFor2010(**kwargs):
    (effargs, vargs) = _getTriggerVertexArgs(kwargs)
    setEfficiencyTriggersFor2010(**effargs)
    setVertexWeightFor2010(**vargs)

def setTriggerVertexFor2011(**kwargs):
    (effargs, vargs) = _getTriggerVertexArgs(kwargs)
    setEfficiencyTriggersFor2011(**effargs)
    setVertexWeightFor2011(**vargs)

# One trigger
def setEfficiencyTrigger(trigger, pset=triggerEfficiency):
    pset.selectTriggers = [cms.PSet(trigger = cms.string(trigger), luminosity = cms.double(-1))]

# Many triggers in  (trigger, lumi) pairs
def setEfficiencyTriggers(triggers, pset=triggerEfficiency):
    pset.selectTriggers = [cms.PSet(trigger=cms.string(t), luminosity=cms.double(l)) for t,l in triggers]

# Triggers and lumis from task names
def setEfficiencyTriggersFromMulticrabDatasets(tasknames, datasetType="pattuple_v10", **kwargs):
    from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabDatasets import datasets
    triggers = []
    for name in tasknames:
        if not name in datasets:
            raise Exception("No configuration fragment for datasets '%s' in multicrabDatasets.py" % name)
        conf = datasets[name]
        if not "trigger" in conf:
            raise Exception("No trigger field in configuration fragment of dataset '%s'" % name)

        if not datasetType in conf["data"]:
            raise Exception("No definition for datasetType '%s' for dataset '%s', required to deduce the integrated luminosity" % (datasetType, name))
        data = conf["data"][datasetType]
        while "fallback" in data:
            data = conf["data"][ data["fallback"] ]

        if not "luminosity" in data:
            raise Exception("No luminosity for dataset '%s' with datasetType '%s'" % (name, datasetType))

        triggers.append( (
                conf["trigger"],
                data["luminosity"]
            ) )
    setEfficiencyTriggers(triggers, **kwargs)

def setEfficiencyTriggersFor2010(datasetType="pattuple_v10", **kwargs):
    setEfficiencyTriggersFromMulticrabDatasets([
            "BTau_146428-148058_Dec22",
            "BTau_148822-149182_Dec22",
            "BTau_149291-149294_Dec22",
            ], datasetType, **kwargs)
def setEfficiencyTriggersFor2011(datasetType="pattuple_v10", **kwargs):
    setEfficiencyTriggersFromMulticrabDatasets([
            "Tau_160431-161016_Prompt",
            "Tau_162803-163261_Prompt",
            "Tau_163270-163369_Prompt",
            ], **kwargs)

def formatEfficiencyTrigger(pset):
    if pset.luminosity.value() < 0:
        return pset.trigger.value()
    else:
        return "%s (%f)" % (pset.trigger.value(), pset.luminosity.value())

# Vertex weighting
def setVertexWeightFor2010(pset=vertexWeight):
    # From runs 136035-149294 single tau trigger and W+jet
    #vertexWeight.weights = cms.vdouble(0.00000, 3.66926, 3.00360, 1.39912, 0.50035, 0.15271, 0.04164, 0.01124, 0.00293, 0.00083, 0.00022, 0.00006, 0.00000)
    # From runs 136035-149294 single tau trigger and QCD, vertex sumpt > 10
    pset.weights = cms.vdouble(0.01959606, 0.47446048, 0.32793999, 0.12526016, 0.03788969, 0.01052797, 0.00282504, 0.00075970, 0.00015295, 0.00003682, 0.00000000, 0.00055113, 0.00000000)
    pset.enabled = True

def setVertexWeightFor2011(pset=vertexWeight):
    # From runs 160431-162828 single tau trigger and W+jets
    #vertexWeight.weights = cms.vdouble(0.00000, 0.24846, 0.88677, 1.52082, 1.79081, 1.53684, 1.08603, 0.71142, 0.45012, 0.27843, 0.17420, 0.13067, 0.08622, 0.04736, 0.03079, 0.14548, 0.00000)
    # From runs 160431-162828 single tau trigger and W+jets, vertex sumpt > 10
    pset.weights = cms.vdouble(0.00553621, 0.12371974, 0.22012135, 0.21266034, 0.15559946, 0.10272823, 0.06623531, 0.04055686, 0.02564348, 0.01839078, 0.01178197, 0.01702626, 0.00000000)
    pset.enabled = True


# Tau selection
def forEachTauSelection(function):
    for selection in tauSelections:
        function(selection)

def setAllTauSelectionOperatingMode(mode):
    forEachTauSelection(lambda x: x.operatingMode.setValue(mode))

def setAllTauSelectionSrcSelectedPatTaus():
    tauSelectionCaloTauCutBased.src         = "selectedPatTausCaloRecoTau"
    tauSelectionShrinkingConeTaNCBased.src  = "selectedPatTausShrinkingConePFTau"
    tauSelectionShrinkingConeCutBased.src   = "selectedPatTausShrinkingConePFTau"
    tauSelectionHPSTauBased.src             = "selectedPatTausHpsPFTau"
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTau"
    tauSelectionHPSLooseTauBased.src        = "selectedPatTausHpsPFTau"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTau"

def setAllTauSelectionSrcSelectedPatTausTriggerMatched():
    tauSelectionCaloTauCutBased.src         = "selectedPatTausCaloRecoTauTauTriggerMatched"
    tauSelectionShrinkingConeTaNCBased.src  = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionShrinkingConeCutBased.src   = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionHPSTauBased.src             = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSLooseTauBased.src        = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTauTauTriggerMatched"
    
def setTauIDFactorizationMap(options):
    from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getTauIDFactorizationMap
    myFactorizationFilename = getTauIDFactorizationMap(options)
    tauIDCoefficients = __import__(myFactorizationFilename, fromlist=['dummy'])
    tauSelectionCaloTauCutBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionShrinkingConeTaNCBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionShrinkingConeCutBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionHPSTauBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients
    tauSelectionCombinedHPSTaNCTauBased.factorization.factorizationTables = tauIDCoefficients.tauIDFactorizationCoefficients

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
def setTauSelection(module, val):
    module.tauSelection = val
def addTauIdAnalyses(process, prefix, module, commonSequence, additionalCounters):
    selections = tauSelections[:]
    names = tauSelectionNames[:]
    hpsLoose = selections.index(tauSelectionHPSLooseTauBased)
    #del selections[hpsLoose]
    #del names[hpsLoose]
    # TCTau can be missing in tau embedding case
    try: 
        caloTauIndex = selections.index(tauSelectionCaloTauCutBased)
        del selections[caloTauIndex]
        del names[caloTauIndex]
    except ValueError:
        pass
    combinedHPSTaNCIndex = selections.index(tauSelectionCombinedHPSTaNCTauBased)
    del selections[combinedHPSTaNCIndex]
    del names[combinedHPSTaNCIndex]

    addAnalysisArray(process, prefix, module, setTauSelection,
                     values = selections, names = names,
                     preSequence = commonSequence,
                     additionalCounters = additionalCounters)


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

def changeMetCollection(**kwargs):
    _changeCollection([jetSelection.src_met, MET.src, fakeMETVeto.src, forwardJetVeto.src_met], **kwargs)
