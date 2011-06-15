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
    selectionType = cms.untracked.string("byTriggerBit"), # Default byTriggerBit, other options byParametrisation, disabled
    triggerTauSelection = cms.untracked.PSet(),
    triggerMETSelection = cms.untracked.PSet(),
    triggerEfficiency = cms.untracked.PSet(),
    caloMetSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("patMETs"), # Calo MET
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
    rtauCut = cms.untracked.double(0.0), # rtau > value
    antiRtauCut = cms.untracked.double(0.0), # rtau < value
    invMassCut = cms.untracked.double(999.), # m(vis.tau) < value; FIXME has no effect in TauSelection.cc 
    nprongs = cms.untracked.uint32(1) # not used at the moment FIXME: has no effect in TauSelection.cc
)

#for QCD control plots
tauSelectionHPSTightTauBasedNoLdgPtOrRtauCut = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTightTauBased",
    leadingTrackPtCut = cms.untracked.double(0.0),
    rtauCut = cms.untracked.double(0.0)
    )

tauSelectionCaloTauCutBased = tauSelectionBase.clone(
    src = "selectedPatTausCaloRecoTau",
    selection = "CaloTauCutBased"
)

tauSelectionShrinkingConeCutBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTau",
    selection = "ShrinkingConePFTauCutBased"
)

tauSelectionShrinkingConeTaNCBased = tauSelectionBase.clone(
    src = "selectedPatTausShrinkingConePFTau",
    selection = "ShrinkingConePFTauTaNCBased"
)

tauSelectionHPSTightTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSTightTauBased"
)

tauSelectionHPSMediumTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSMediumTauBased"
)

tauSelectionHPSLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSLooseTauBased"
)

tauSelectionHPSVeryLooseTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsPFTau",
    selection = "HPSVeryLooseTauBased"
)

tauSelectionCombinedHPSTaNCTauBased = tauSelectionBase.clone(
    src = "selectedPatTausHpsTancPFTau",
    selection = "CombinedHPSTaNCTauBased"
)


tauSelections = [tauSelectionCaloTauCutBased,
                 tauSelectionShrinkingConeCutBased,
                 tauSelectionShrinkingConeTaNCBased,
                 tauSelectionHPSTightTauBased,
                 tauSelectionHPSTightTauBasedNoLdgPtOrRtauCut, #for QCD control plots
                 tauSelectionHPSMediumTauBased,
                 tauSelectionHPSLooseTauBased,
                 tauSelectionCombinedHPSTaNCTauBased]
tauSelectionNames = ["TauSelectionCaloTauCutBasedTauTriggerMatched",
                     "TauSelectionShrinkingConeCutBasedTauTriggerMatched",
                     "TauSelectionShrinkingConeTaNCBasedTauTriggerMatched",
                     "TauSelectionHPSTightTauBasedTauTriggerMatched",
                     "TauSelectionHPSTightTauBasedNoLdgPtOrRtauCutTauTriggerMatched",
                     "TauSelectionHPSMediumTauBasedTauTriggerMatched",
                     "TauSelectionHPSLooseTauBasedTauTriggerMatched",
                     "TauSelectionCombinedHPSTaNCBasedTauTriggerMatched"]

#tauSelection = tauSelectionShrinkingConeCutBased
#tauSelection = tauSelectionShrinkingConeTaNCBased
#tauSelection = tauSelectionCaloTauCutBased
tauSelection = tauSelectionHPSTightTauBased
#tauSelection = tauSelectionHPSMediumTauBased
#tauSelection = tauSelectionCombinedHPSTaNCTauBased

jetSelection = cms.untracked.PSet(
    #src = cms.untracked.InputTag("selectedPatJets"),       # Calo jets
    #src = cms.untracked.InputTag("selectedPatJetsAK5JPT"), # JPT jets 
    src = cms.untracked.InputTag("selectedPatJetsAK5PF"),  # PF jets
    src_met = cms.untracked.InputTag("patMETsPF"), # calo MET 
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30.0),
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
    discriminatorCut = cms.untracked.double(1.7),
    ptCut = cms.untracked.double(30.0),
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
    pileupSrc = cms.InputTag("addPileupInfo"),
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
trigger.triggerEfficiency = triggerEfficiency

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


# Weighting by instantaneous luminosity, and the number of true
# simulated pile up interactions
def setPileupWeightFor2010(pset=vertexWeight):
    # From Apr21 JSON
    pset.weights = cms.vdouble(2.17905734, 3.57481462, 3.45593082, 2.45853780, 1.42664179, 0.71282896, 0.31676356, 0.12779020, 0.04743868, 0.01635333, 0.00526898, 0.00176643, 0.00060303, 0.00021282, 0.00007491, 0.00002750, 0.00001017, 0.00000382, 0.00000146, 0.00000059, 0.00000022, 0.00000010, 0.00000004, 0.00000001, 0.00000001, 0.00000000)
    pset.enabled = True
    pset.useSimulatedPileup = True

def setPileupWeightFor2011(pset=vertexWeight):
    # From May10 JSON
    pset.weights = cms.vdouble(0.35702197, 0.39872966, 0.93383097, 1.57574239, 2.06786668, 2.23237405, 2.05856116, 1.66571901, 1.20680394, 0.79514625, 0.48238646, 0.30154678, 0.19093225, 0.12479613, 0.08150170, 0.05577673, 0.03874763, 0.02759475, 0.02023368, 0.01580798, 0.01150307, 0.01010894, 0.00765439, 0.00596082, 0.00469376, 0.00000000)
    pset.enabled = True
    pset.useSimulatedPileup = True

def setPileupWeightFor2010and2011(pset=vertexWeight):
    # From Apr21 (2010) and May10 (2011) JSONs
    pset.weights = cms.vdouble(0.55669307, 0.89223000, 1.33000619, 1.69326210, 1.91344756, 1.92774735, 1.73919965, 1.41792615, 1.05583012, 0.72551064, 0.46426616, 0.30894711, 0.20983226, 0.14807083, 0.10498652, 0.07838662, 0.05967027, 0.04674974, 0.03785193, 0.03277864, 0.02654201, 0.02607185, 0.02217936, 0.01951763, 0.01748345, 0.00000000)
    pset.enabled = True
    pset.useSimulatedPileup = True

# Weighting by number of reconstructed vertices
def setVertexWeightFor2010(pset=vertexWeight):
    # From runs 136035-149294 single tau trigger and W+jet
    #vertexWeight.weights = cms.vdouble(0.00000, 3.66926, 3.00360, 1.39912, 0.50035, 0.15271, 0.04164, 0.01124, 0.00293, 0.00083, 0.00022, 0.00006, 0.00000)
    # From runs 136035-149294 single tau trigger and QCD, vertex sumpt > 10
    pset.weights = cms.vdouble(0.09267533, 2.24385810, 1.55092120, 0.59239078, 0.17919108, 0.04978977, 0.01336043, 0.00359282, 0.00072334, 0.00017415, 0.00000000)
    pset.enabled = True
    pset.useSimulatedPileup = False

def setVertexWeightFor2011(pset=vertexWeight):
    # From runs 160431-162828 single tau trigger and W+jets
    #vertexWeight.weights = cms.vdouble(0.00000, 0.24846, 0.88677, 1.52082, 1.79081, 1.53684, 1.08603, 0.71142, 0.45012, 0.27843, 0.17420, 0.13067, 0.08622, 0.04736, 0.03079, 0.14548, 0.00000)
    # From runs 160431-162828 single tau trigger and W+jets, vertex sumpt > 10
    pset.weights = cms.vdouble(0.03445398, 0.76995593, 1.36990047, 1.32346773, 0.96835577, 0.63931763, 0.41220802, 0.25240105, 0.15958929, 0.11445294, 0.07332379, 0.10596101, 0.00000000)
    pset.enabled = True
    pset.useSimulatedPileup = False


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
    tauSelectionHPSTightTauBased.src        = "selectedPatTausHpsPFTau"
    tauSelectionHPSTightTauBasedNoLdgPtOrRtauCut.src = "selectedPatTausHpsPFTau" #for QCD control plots
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTau"
    tauSelectionHPSLooseTauBased.src        = "selectedPatTausHpsPFTau"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTau"

def setAllTauSelectionSrcSelectedPatTausTriggerMatched():
    tauSelectionCaloTauCutBased.src         = "selectedPatTausCaloRecoTauTauTriggerMatched"
    tauSelectionShrinkingConeTaNCBased.src  = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionShrinkingConeCutBased.src   = "selectedPatTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionHPSTightTauBased.src        = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSTightTauBasedNoLdgPtOrRtauCut.src = "selectedPatTausHpsPFTauTauTriggerMatched"#for QCD control plots
    tauSelectionHPSMediumTauBased.src       = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSLooseTauBased.src        = "selectedPatTausHpsPFTauTauTriggerMatched"
    tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTauTauTriggerMatched"
    
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
def setTauSelection(module, val):
    module.tauSelection = val
def addTauIdAnalyses(process, prefix, module, commonSequence, additionalCounters):
    selections = tauSelections[:]
    names = tauSelectionNames[:]
    # Remove TCTau from list
    tctauIndex = selections.index(tauSelectionCaloTauCutBased)
    del selections[tctauIndex]
    del names[tctauIndex]
    # Remove PF shrinking cone from list
    pfShrinkingConeIndex = selections.index(tauSelectionShrinkingConeCutBased)
    del selections[pfShrinkingConeIndex]
    del names[pfShrinkingConeIndex]
    # Remove TaNC from list
    tancIndex = selections.index(tauSelectionShrinkingConeTaNCBased)
    del selections[tancIndex]
    del names[tancIndex]
    # HPS loose
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
    # Remove combined HPS TaNC from list
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
    _changeCollection([
            jetSelection.src_met,
            MET.src,
            fakeMETVeto.src,
            TauEmbeddingAnalysis.embeddingMetSrc,
            forwardJetVeto.src_met
            ], **kwargs)
