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
    cleanTauDR = cms.untracked.double(0.5), #no change
    ptCut = cms.untracked.double(30.0),
    etaCut = cms.untracked.double(2.4),
    minNumber = cms.untracked.uint32(3),
    EMfractionCut = cms.untracked.double(999), # large number to effectively disable the cut
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
    method = cms.string("intime"), # intime, 3D
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
# The following two distributions for Summer11 are from
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
Summer11_PU_S4_3D = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
Summer11_PU_S4_intime = cms.vdouble(1.45346E-01, 6.42802E-02, 6.95255E-02, 6.96747E-02, 6.92955E-02, 6.84997E-02, 6.69528E-02, 6.45515E-02, 6.09865E-02, 5.63323E-02, 5.07322E-02, 4.44681E-02, 3.79205E-02, 3.15131E-02, 2.54220E-02, 2.00184E-02, 1.53776E-02, 1.15387E-02, 8.47608E-03, 6.08715E-03, 4.28255E-03, 2.97185E-03, 2.01918E-03, 1.34490E-03, 8.81587E-04, 5.69954E-04, 3.61493E-04, 2.28692E-04, 1.40791E-04, 8.44606E-05, 5.10204E-05, 3.07802E-05, 1.81401E-05, 1.00201E-05, 5.80004E-06)
Summer11_PU_S4_ave = cms.vdouble(0.104109, 0.0703573, 0.0698445, 0.0698254, 0.0697054, 0.0697907, 0.0696751, 0.0694486, 0.0680332, 0.0651044, 0.0598036, 0.0527395, 0.0439513, 0.0352202, 0.0266714, 0.019411, 0.0133974, 0.00898536, 0.0057516, 0.00351493, 0.00212087, 0.00122891, 0.00070592, 0.000384744, 0.000219377)


def setPileupWeightFor2010(pset=vertexWeight):
    # From Apr21 JSON
    pset.mcDist = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT
    pset.dataDist = cms.vdouble()
    pset.enabled = True
    pset.useSimulatedPileup = True
    raise Exception("Data PU distribution for 2010 is not yet available")

def setPileupWeightFor2011(dataVersion, pset=vertexWeight, era="EPS", method="intime"):
    if dataVersion.isData():
        return

    if dataVersion.isS4():
        pset.mcDistIntime = Summer11_PU_S4_intime
        pset.mcDist3D = Summer11_PU_S4_3D
        pset.weightFile3D = cms.string("")
        pset.method = method
        if method != "intime":
            raise Exception("For the moment only 'intime' PU weighting is supported (it gives the best data/MC matching)")
    else:
        raise Exception("No PU reweighting support for anything else than Summer11 S4 scenario at the moment")
    pset.enabled = True
    pset.useSimulatedPileup = True

    # /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp
    if era == "EPS":
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileup_v2.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileup_v2.root
        pset.dataDistIntime = cms.vdouble(8116477.00000000, 35321928.00000000, 81685392.00000000, 132385592.00000000, 168089600.00000000, 177634496.00000000, 162288416.00000000, 131549432.00000000, 96403088.00000000, 64783048.00000000, 40367300.00000000, 23533640.00000000, 12931737.00000000, 6739807.00000000, 3349574.00000000, 1594808.00000000, 730430.43750000, 322976.00000000, 138316.20312500, 57534.10156250, 23303.56054688, 9211.73242188, 3560.76806641, 1348.30310059, 500.88070679, 182.78894043, 65.60128021, 23.17440987, 8.06377983, 2.76517296, 0.93474805, 0.31154540, 0.10237330, 0.03316922, 0.01539941)
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileupTruth_v2.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileupTruth_v2.root
        pset.dataDist3D = cms.vdouble(0.00000000, 179221.81250000, 3814551.00000000, 25772300.00000000, 172987680.00000000, 356233824.00000000, 353649024.00000000, 175073792.00000000, 47863632.00000000, 10613712.00000000, 1599420.50000000, 243314.20312500, 26479.34960938, 4621.37011719, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000)
        pset.weightFile3D = "HiggsAnalysis/HeavyChHiggsToTauNu/data/Weight3D_160404-167913.root"

    elif era == "Run2011A":
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileup_v2.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileup_v2.root
        # Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileup_v2.root
        # Cert_172620-173692_PromptReco_JSON.pileup_v2.root
        pset.dataDistIntime = cms.vdouble(12965370.00000000, 55851368.00000000, 129329360.00000000, 212133600.00000000, 276137728.00000000, 303603552.00000000, 293257504.00000000, 255632864.00000000, 204970016.00000000, 153263664.00000000, 107935616.00000000, 72100608.00000000, 45912988.00000000, 27970044.00000000, 16342576.00000000, 9175983.00000000, 4958610.00000000, 2582392.75000000, 1297695.75000000, 629975.06250000, 295784.25000000, 134469.67187500, 59260.07031250, 25343.86718750, 10530.08984375, 4255.04833984, 1673.94946289, 641.77648926, 240.02249146, 87.65042877, 31.28098488, 10.91952801, 3.73145652, 1.24922824, 0.60236752)
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileupTruth_v2.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileupTruth_v2.root
        # Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileupTruth_v2.root
        # Cert_172620-173692_PromptReco_JSON.pileupTruth_v2.root
        pset.dataDist3D = cms.vdouble(0.00000000, 252573.03125000, 5738606.50000000, 50564120.00000000, 268197264.00000000, 512976800.00000000, 521465600.00000000, 375661280.00000000, 241466880.00000000, 143150480.00000000, 53831752.00000000, 11812459.00000000, 1290734.00000000, 111569.03125000, 6537.93310547, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000)

    elif era == "Run2011B":
        # Cert_175832-177515_PromptReco_JSON.pileup_v2.root
        # Cert_177718_178078_7TeV_PromptReco_Collisons11_JSON.pileup_v2.root
        pset.dataDistIntime = cms.vdouble(288839.53915556, 1944213.26515934, 7048893.23414854, 17866609.95292950, 35426386.30411588, 58569220.47460749, 84109732.81887844, 107913437.32744664, 126207015.92123026, 136532056.99027678, 138111301.86270767, 131696668.90145068, 119102716.65215862, 102637515.42847806, 84591412.32094480, 66875650.26462977, 50838721.28147475, 37240033.46912239, 26333217.71488850, 18004589.36255783, 11920512.70239508, 7653181.43074327, 4770835.32761546, 2891324.00292016, 1705583.78483189, 980459.54751395, 549865.64067858, 301180.84548916, 161286.57232955, 84529.11170115, 43397.75678300, 21846.03128374, 10791.61205329, 5235.31386353, 4645.12031734)
        # Cert_175832-177515_PromptReco_JSON.pileupTruth_v2.root
        # Cert_177718_178078_7TeV_PromptReco_Collisons11_JSON.pileupTruth_v2.root
        pset.dataDist3D = ms.vdouble(0.00000000, 27267.43951180, 35590.01162089, 74493.32615900, 574589.87278601, 2906478.58801937, 33631126.33142464, 93666084.68744215, 138283180.67404377, 187623897.42037976, 215647291.26482403, 211729949.14499977, 187001951.98512825, 146693123.78931406, 94437211.96536994, 46031697.28833491, 16923096.85784976, 5181606.42557313, 1428052.42465751, 437008.14233306, 102694.05116599, 6516.19593707, 0.00000000, 0.00000000, 0.00000000)

    elif era == "all":
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileup_v2.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileup_v2.root
        # Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileup_v2.root
        # Cert_172620-173692_PromptReco_JSON.pileup_v2.root
        # Cert_175832-177515_PromptReco_JSON.pileup_v2.root
        # Cert_177718_178078_7TeV_PromptReco_Collisons11_JSON.pileup_v2.root
        pset.dataDistIntime = cms.vdouble(13254210.00000000, 57795580.00000000, 136378256.00000000, 230000208.00000000, 311564128.00000000, 362172768.00000000, 377367232.00000000, 363546304.00000000, 331177056.00000000, 289795712.00000000, 246046912.00000000, 203797264.00000000, 165015696.00000000, 130607568.00000000, 100933984.00000000, 76051632.00000000, 55797336.00000000, 39822424.00000000, 27630914.00000000, 18634564.00000000, 12216297.00000000, 7787651.00000000, 4830095.00000000, 2916667.75000000, 1716113.87500000, 984714.62500000, 551539.56250000, 301822.62500000, 161526.59375000, 84616.76562500, 43429.03906250, 21856.95117188, 10795.34375000, 5236.56347656, 4645.72265625)
        # Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileupTruth.root
        # Cert_165088-167913_7TeV_PromptReco_JSON.pileupTruth.root
        # Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileupTruth.root
        # Cert_172620-173692_PromptReco_JSON.pileupTruth.root
        pset.dataDist3D = cms.vdouble(0.00000000, 279840.46875000, 5774196.50000000, 50638612.00000000, 268771872.00000000, 515883296.00000000, 555096704.00000000, 469327360.00000000, 379750048.00000000, 330774368.00000000, 269479040.00000000, 223542416.00000000, 188292688.00000000, 146804688.00000000, 94443744.00000000, 46031696.00000000, 16923096.00000000, 5181606.50000000, 1428052.50000000, 437008.12500000, 102694.04687500, 6516.19580078, 0.00000000, 0.00000000, 0.00000000)

    else:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are 'EPS', 'Run2011A', 'Run2011B', 'all'" % era)

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
