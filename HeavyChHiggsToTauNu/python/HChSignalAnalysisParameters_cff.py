import FWCore.ParameterSet.Config as cms

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
    rtauCut = cms.untracked.double(0.7), # rtau > value
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
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30.0),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3),
    METCut = cms.untracked.double(60.0),
    EMfractionCut = cms.untracked.double(0.6)
#    EMfractionCut = cms.untracked.double(999), # large number to effectively disable the cut
)

MET = cms.untracked.PSet(
    # src = cms.untracked.InputTag("patMETs"), # calo MET
    #src = cms.untracked.InputTag("patMETsTC"), # tc MET
    rawSrc = cms.untracked.InputTag("patMETsPF"), # PF MET
    type1Src = cms.untracked.InputTag("dummy"),
    type2Src = cms.untracked.InputTag("dummy"),
    caloSrc = cms.untracked.InputTag("patMETs"),
    tcSrc = cms.untracked.InputTag("patMETsTC"),
    select = cms.untracked.string("raw"), # raw, type1, type2
    METCut = cms.untracked.double(70.0)
)

bTagging = cms.untracked.PSet(
    discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
    discriminatorCut = cms.untracked.double(1.7),
    ptCut = cms.untracked.double(30.0),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(1),
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
  TopMassHigh = cms.untracked.double(300.0)
)

tree = cms.untracked.PSet(
    fill = cms.untracked.bool(True),
    tauIDs = cms.untracked.vstring(
        "byTightIsolation",
        "byMediumIsolation",
        "byLooseIsolation"
    )
)

vertexWeight = cms.untracked.PSet(
    vertexSrc = cms.InputTag("goodPrimaryVertices"),
#    vertexSrc = cms.InputTag("goodPrimaryVertices10"),
    puSummarySrc = cms.InputTag("addPileupInfo"),
    useSimulatedPileup = cms.bool(False), # reweight by PileupSummaryInfo (True) or vertices (False)
    summer11S4Mode = cms.bool(False),
    weights = cms.vdouble(0.0),
    enabled = cms.bool(False),
    shiftMean = cms.bool(False),
    shiftMeanAmount = cms.double(0),    
)


def triggerBin(pt, dataEff, dataUnc, mcEff, mcUnc):
    return cms.PSet(
        pt = cms.double(pt),
        dataEff = cms.double(dataEff),
        dataUncertainty = cms.double(dataUnc),
        mcEff = cms.double(mcEff),
        mcUncertainty = cms.double(mcUnc)
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
    parameters = cms.untracked.VPSet(
        triggerBin(40, 0.4035088, 0.06502412, 0.406639,  0.02247143),
        triggerBin(50, 0.7857143, 0.1164651,  0.6967213, 0.04239523),
        triggerBin(60, 0.8,       0.1108131,  0.8235294, 0.04892095),
        triggerBin(80, 1,         0.2496484,  0.7916667, 0.08808045),
    ),
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

# def setTriggerPileupFor2010(**kwargs):
#     (effargs, vargs) = _getTriggerVertexArgs(kwargs)
#     setEfficiencyTriggersFor2010(**effargs)
#     setPileupWeightFor2010(**vargs)

# def setTriggerPileupFor2011(**kwargs):
#     (effargs, vargs) = _getTriggerVertexArgs(kwargs)
#     setEfficiencyTriggersFor2011(**effargs)
#     setPileupWeightFor2011All(**vargs)

# # One trigger
# def setEfficiencyTrigger(trigger, pset=triggerEfficiency):
#     pset.selectTriggers = [cms.PSet(trigger = cms.string(trigger), luminosity = cms.double(-1))]

# # Many triggers in  (trigger, lumi) pairs
# def setEfficiencyTriggers(triggers, pset=triggerEfficiency):
#     pset.selectTriggers = [cms.PSet(trigger=cms.string(t), luminosity=cms.double(l)) for t,l in triggers]

# # Triggers and lumis from task names
# def setEfficiencyTriggersFromMulticrabDatasets(tasknames, datasetType="pattuple_v10", **kwargs):
#     from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabDatasets import datasets
#     triggers = []
#     for name in tasknames:
#         if not name in datasets:
#             raise Exception("No configuration fragment for datasets '%s' in multicrabDatasets.py" % name)
#         conf = datasets[name]
#         if not "trigger" in conf:
#             raise Exception("No trigger field in configuration fragment of dataset '%s'" % name)

#         if not datasetType in conf["data"]:
#             raise Exception("No definition for datasetType '%s' for dataset '%s', required to deduce the integrated luminosity" % (datasetType, name))
#         data = conf["data"][datasetType]
#         while "fallback" in data:
#             data = conf["data"][ data["fallback"] ]

#         if not "luminosity" in data:
#             raise Exception("No luminosity for dataset '%s' with datasetType '%s'" % (name, datasetType))

#         triggers.append( (
#                 conf["trigger"],
#                 data["luminosity"]
#             ) )
#     setEfficiencyTriggers(triggers, **kwargs)

# def setEfficiencyTriggersFor2010(datasetType="pattuple_v10", **kwargs):
#     raise Exception("This function is not supported at the moment")
#     setEfficiencyTriggersFromMulticrabDatasets([
#             "BTau_146428-148058_Dec22",
#             "BTau_148822-149182_Dec22",
#             "BTau_149291-149294_Dec22",
#             ], datasetType, **kwargs)
# def setEfficiencyTriggersFor2011(datasetType="pattuple_v10", **kwargs):
#     raise Exception("This function is not supported at the moment")
#     setEfficiencyTriggersFromMulticrabDatasets([
#             "Tau_160431-161016_Prompt",
#             "Tau_162803-163261_Prompt",
#             "Tau_163270-163369_Prompt",
#             ], **kwargs)

# def formatEfficiencyTrigger(pset):
#     if pset.luminosity.value() < 0:
#         return pset.trigger.value()
#     else:
#         return "%s (%f)" % (pset.trigger.value(), pset.luminosity.value())


# Weighting by instantaneous luminosity, and the number of true
# simulated pile up interactions

# Summer11
# SimGeneral/MixingModule/python/mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT.py rev 1.2
mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT = cms.vdouble(0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0630151648,0.0526654164,0.0402754482,0.0292988928,0.0194384503,0.0122016783,0.007207042,0.004003637,0.0020278322,0.0010739954,0.0004595759,0.0002229748,0.0001028162,4.58337152809607E-05)
Summer11_PU_S4 = cms.vdouble(0.104109, 0.0703573, 0.0698445, 0.0698254, 0.0697054, 0.0697907, 0.0696751, 0.0694486, 0.0680332, 0.0651044, 0.0598036, 0.0527395, 0.0439513, 0.0352202, 0.0266714, 0.019411, 0.0133974, 0.00898536, 0.0057516, 0.00351493, 0.00212087, 0.00122891, 0.00070592, 0.000384744, 0.000219377)


def setPileupWeightFor2010(pset=vertexWeight):
    # From Apr21 JSON
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble()
    pset.enabled = True
    pset.useSimulatedPileup = True
    raise Exception("Data PU distribution for 2010 is not yet available")

def setPileupWeightFor2011(dataVersion, pset=vertexWeight, era="EPS"):
    # From May10 JSON
    if dataVersion.isS4():
        pset.mcDist = Summer11_PU_S4
        pset.summer11S4Mode = True
    else:
        pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
        pset.summer11S4Mode = False
    pset.enabled = True
    pset.useSimulatedPileup = True

    if era == "EPS":
        # from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp/Pileup_2011_EPS_8_jul.root
        pset.dataDist = cms.vdouble(14541678.75140152, 34774289.38286586, 78924690.82740858, 126467305.04758325, 159328519.15029529, 167603454.44535571, 152683760.94960380, 123793506.45609140, 90946208.64651683, 61397298.32203319, 38505025.66458631, 22628034.29716743, 12550315.25868838, 6610507.05491146, 3324027.56535537, 1602862.62059887, 743920.15564290, 333476.86203421, 144860.60591722, 61112.68817281, 25110.18359585, 10065.11629597, 3943.97900547, 1513.53535599, 896.16051321)
    elif era == "all":
        # from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp/Pileup_2011_to_172802_LP_LumiScale.root
        pset.dataDist = cms.vdouble(13577061.34960927, 36988195.79256942, 87784462.15955786, 148782145.82866752, 200194824.54279479, 227349906.22656760, 226472477.30015501, 203175245.93433914, 167317368.02201021, 128301353.72262345, 92616728.24257115, 63470211.62257222, 41558646.73644819, 26124508.46311678, 15821365.84873490, 9253707.52579752, 5235996.37046473, 2869480.81515694, 1524386.71200273, 785535.62462179, 392893.09321437, 190841.97559003, 90079.33573278, 41342.87414307, 32218.24625225)
    else:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are 'EPS' and 'all'" % era)


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
    tauSelectionCaloTauCutBased.src         = "patTausCaloRecoTauTauTriggerMatched"
    tauSelectionShrinkingConeTaNCBased.src  = "patTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionShrinkingConeCutBased.src   = "patTausShrinkingConePFTauTauTriggerMatched"
    tauSelectionHPSTightTauBased.src        = "patTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSTightTauBasedNoLdgPtOrRtauCut.src = "patTausHpsPFTauTauTriggerMatched"#for QCD control plots
    tauSelectionHPSMediumTauBased.src       = "patTausHpsPFTauTauTriggerMatched"
    tauSelectionHPSLooseTauBased.src        = "patTausHpsPFTauTauTriggerMatched"
    tauSelectionCombinedHPSTaNCTauBased.src = "patTausHpsTancPFTauTauTriggerMatched"
    
def addTauIdAnalyses(process, dataVersion, prefix, prototype, commonSequence, additionalCounters):
    from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection

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

    for selection, name in zip(selections, names):
        module = prototype.clone()
        module.tauSelection = selection.clone()

        # Calculate type 1 MET
        (type1Sequence, type1Met) = MetCorrection.addCorrectedMet(process, dataVersion, module.tauSelection, module.jetSelection, postfix=name)
        module.MET.type1Src = type1Met

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

def changeMetCollection(**kwargs):
    _changeCollection([
            MET.rawSrc,
            forwardJetVeto.src_met
            ], **kwargs)
