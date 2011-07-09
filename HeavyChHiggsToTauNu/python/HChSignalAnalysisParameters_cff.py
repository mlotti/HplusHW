import FWCore.ParameterSet.Config as cms

# WARNING: the trigger path is modified in signalAnalysis_cfg.py depending on
# the data version
trigger = cms.untracked.PSet(
    triggerSrc = cms.untracked.InputTag("TriggerResults", "", "INSERT_HLT_PROCESS_HERE"),
    patSrc = cms.untracked.InputTag("patTriggerEvent"),
    triggers = cms.untracked.vstring("HLT_SingleLooseIsoTau20",
                                     "HLT_SingleLooseIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk5",
                                     "HLT_SingleIsoTau20_Trk15_MET20",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v3",
                                     "HLT_SingleIsoTau20_Trk15_MET25_v4",
                                     "HLT_IsoPFTau35_Trk20_MET45_v1",
                                     "HLT_IsoPFTau35_Trk20_MET45_v2",
                                     "HLT_IsoPFTau35_Trk20_MET45_v4",
                                     "HLT_IsoPFTau35_Trk20_MET45_v6",
                                     "HLT_IsoPFTau35_Trk20_MET60_v2",
    ),
    hltMetCut = cms.untracked.double(60.0),
    throwIfNoMet = cms.untracked.bool(False), # to prevent jobs from failing, FIXME: must be investigated later
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
#tauSelection = tauSelectionHPSLooseTauBased
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
    minNumber = cms.untracked.uint32(1),
    scaleFactorBFlavorValue = cms.untracked.double(0.95), # from BTV-11-001, flat in pT
    scaleFactorBFlavorUncertainty = cms.untracked.double(0.06), # from BTV-11-001, flat in pT
    scaleFactorLightFlavorValue = cms.untracked.double(1.11), # from BTV-11-001, flat in pT
    scaleFactorLightFlavorUncertainty = cms.untracked.double(0.11), # from BTV-11-001, flat in pT
    variationMode = cms.untracked.string("normal")
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
    useSimulatedPileup = cms.bool(False), # reweight by PileupSummaryInfo (True) or vertices (False)
    weights = cms.vdouble(0.0),
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

def setTriggerPileupFor2010(**kwargs):
    (effargs, vargs) = _getTriggerVertexArgs(kwargs)
    setEfficiencyTriggersFor2010(**effargs)
    setPileupWeightFor2010(**vargs)

def setTriggerPileupFor2011(**kwargs):
    (effargs, vargs) = _getTriggerVertexArgs(kwargs)
    setEfficiencyTriggersFor2011(**effargs)
    setPileupWeightFor2011All(**vargs)

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

# Summer11
# SimGeneral/MixingModule/python/mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT.py rev 1.2
mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT = cms.vdouble(0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0630151648,0.0526654164,0.0402754482,0.0292988928,0.0194384503,0.0122016783,0.007207042,0.004003637,0.0020278322,0.0010739954,0.0004595759,0.0002229748,0.0001028162,4.58337152809607E-05)

def setPileupWeightFor2010(pset=vertexWeight):
    # From Apr21 JSON
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble()
    pset.enabled = True
    pset.useSimulatedPileup = True
    raise Exception("Data PU distribution for 2010 is not yet available")

def setPileupWeightFor2011May10(pset=vertexWeight):
    # From May10 JSON
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble(3920760.80629436, 6081805.28281331, 13810357.99011321, 22505758.94021218, 28864043.83552697, 30917427.86233390, 28721324.56001887, 23746403.90406303, 17803439.77098848, 12274902.61013811, 7868110.47066589, 4729915.39947807, 2686011.14199905, 1449831.55635479, 747892.02788490, 370496.37848078, 177039.18864957, 81929.34806527, 36852.77647303, 16164.44620983, 6932.97050646, 2914.39317056, 1202.91639412, 488.15400922, 194.93432620)
    pset.enabled = True
    pset.useSimulatedPileup = True

def setPileupWeightFor2011Prompt(pset=vertexWeight):
    # From PromptReco JSON, excluding May10
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble(3364411.22646056, 6507536.11599253, 15783688.78330901, 27546803.40290805, 37805440.04499011, 43130651.44049883, 42413959.59334268, 36886700.45408770, 28916975.43342970, 20735332.44659095, 13757174.49119082, 8522971.03806628, 4967396.75218076, 2740323.71571966, 1438216.13654605, 721205.63553246, 346808.38911421, 160424.48638762, 71576.36381337, 30874.28861973, 12901.20200799, 5231.57827249, 2061.90603311, 790.88902422, 295.57795295)
    pset.enabled = True
    pset.useSimulatedPileup = True

def setPileupWeightFor2011All(pset=vertexWeight):
    # From May10+PromptReco JSON
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble(7285172.03275537, 12589341.39881099, 29594046.77342086, 50052562.34239509, 66669483.87818073, 74048079.30104686, 71135284.15336381, 60633104.35815605, 46720415.20442367, 33010235.05672242, 21625284.96185776, 13252886.43754622, 7653407.89417986, 4190155.27207472, 2186108.16443100, 1091702.01401312, 523847.57776371, 242353.83445289, 108429.14028640, 47038.73482953, 19834.17251443, 8145.97144305, 3264.82242723, 1279.04303343, 490.51227915)
    pset.enabled = True
    pset.useSimulatedPileup = True

def setPileupWeightFor2010and2011(pset=vertexWeight):
    # From Apr21 (2010) and May10+PromptReco (2011) JSONs
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble()
    pset.enabled = True
    pset.useSimulatedPileup = True
    raise Exception("Data PU distribution for 2010 and 2011 is not yet available")

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
