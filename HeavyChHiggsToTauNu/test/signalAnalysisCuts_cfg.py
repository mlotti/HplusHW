import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import copy

#dataVersion = "35X"
dataVersion = "36X"
#dataVersion = "37X"

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
options = VarParsing.VarParsing()
options.register("crossSection",
                 0., # default value
                 options.multiplicity.singleton, # singleton or list
                 options.varType.float,          # string, int, or float
                 "Cross section of the dataset (stored to histograms ROOT file)")
options.parseArguments()

process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All
if dataVersion == "37X":
    process.GlobalTag.globaltag = cms.string("START37_V6::All")
else:
    process.GlobalTag.globaltag = cms.string("START36_V10::All")

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#    skipEvents = cms.untracked.uint32(500),
    fileNames = cms.untracked.vstring(
        "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/FA6E6683-C844-DF11-A2D8-0018F3D0961E.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/D0E1C289-C744-DF11-B84C-00261894389F.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/A24BB684-C544-DF11-81ED-00261894391D.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/284100C7-4E45-DF11-9AF9-0018F3D09710.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/06A4E187-C644-DF11-BC3E-0018F3D096AA.root'
  )
)

process.source.fileNames = cms.untracked.vstring("file:pattuple-1000.root")

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.TFileService.fileName = "histograms.root"

# Set up event counter stuff and the analysis sequence
process.countAll = cms.EDProducer("EventCountProducer")
process.analysis = cms.Sequence(process.countAll)
process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counters = cms.untracked.VInputTag(
        cms.InputTag("countAll")
    )
)
process.counterPath = cms.Path(process.counters)

# Add generator infor to the TFileService file
process.genRunInfo = cms.EDAnalyzer("HPlusGenRunInfoAnalyzer",
    src = cms.untracked.InputTag("generator")
)
process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer",
    crossSection = cms.untracked.double(options.crossSection)
)
print "Dataset cross section has been set to %g pb" % options.crossSection
process.analysis *= process.genRunInfo

# Module for miscellaneous debugging
# process.debug = cms.EDAnalyzer("HPlusDebugAnalyzer",
#     jetSrc = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
#     trigSrc = cms.untracked.InputTag("TriggerResults", "", "REDIGI36X")
# )
# process.analysis *= process.debug

# Import cut and histogrammint tools
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *

# selected* will hold the name of the product of the selected objects
# (i.e. which has passed the previous cut)
fixedConeTaus = cms.InputTag("selectedPatTaus")
selectedTaus = fixedConeTaus

calo_jets = cms.InputTag("selectedPatJets")
jpt_jets = cms.InputTag("selectedPatJetsAK5JPT")
selectedJets = jpt_jets

calo_met = cms.InputTag("patMETs")
pf_met = cms.InputTag("patMETsPF")
tc_met = cms.InputTag("patMETsTC")
selectedMet = pf_met

# List of histograms for each object type
tauHistos = [
    Histo("pt", "pt()", min=0., max=100., nbins=100, description="tau pt (GeV/c)"),
    Histo("eta", "eta()", min=-3, max=3, nbins=60, description="tau eta"),
    Histo("ldgtrkpt", "? leadTrack().isNonnull() ? leadTrack().pt() : -1", min=0., max=100., nbins=100, description="tau leading track pt (GeV/c)")
    ]
jetHistos = [
    Histo("pt", "pt()", min=0., max=100., nbins=100, description="jet pt (GeV/c)"),
    Histo("eta", "eta()", min=-3., max=3., nbins=60, description="jet eta"),
    Histo("trackCountingHighPurBJetTags", "bDiscriminator('trackCountingHighPurBJetTags')", min=-20, max=40, nbins=60, description="b discriminator"),
    Histo("trackCountingHighEffBJetTags", "bDiscriminator('trackCountingHighEffBJetTags')", min=-20, max=40, nbins=60, description="b discriminator"),
    ]
metHistos = [Histo("et", "et()", min=0., max=100., nbins=100, description="met et (GeV/c)")]

#### Beginning, book the first MultiHistoAnalyzer with all histograms
hi = 0
histoAnalyzer = addMultiHistoAnalyzer(process, process.analysis, "h%02d_beginning"%hi, [
    ("tau_", selectedTaus, tauHistos),
    ("jet_", selectedJets, jetHistos),
    ("calojet_", calo_jets, jetHistos),
    ("jptjet_", jpt_jets, jetHistos),
    ("met_", selectedMet, metHistos),
    ("calomet_", calo_met, metHistos),
    ("pfmet_", pf_met, metHistos),
    ("tcmet_", tc_met, metHistos)])


def cloneHisto(histo, cuttype, minObjects=None):
    h = copy.deepcopy(histo)
    h.setCuttype(cuttype)
    if minObjects != None:
        h.setMinObjects(minObjects)
    return h

efficiencyPlots = [
    ("tau_", selectedTaus, [cloneHisto(tauHistos[0], ">"),
                            Histo("eta", "abs(eta())", min=0, max=3, nbins=30, description="tau eta", cuttype="<"),
                            cloneHisto(tauHistos[2], ">")]),
    ("jet_", selectedJets, [cloneHisto(jetHistos[0], ">", minObjects=3)],
     "met_", selectedMet, [cloneHisto(metHistos[0], ">")])]
addMultiEfficiencyPerObjectAnalyzer(process, process.analysis, "h%02d_beginning_passes_object"%hi, efficiencyPlots)
addMultiEfficiencyPerEventAnalyzer(process, process.analysis, "h%02d_beginning_passes_event"%hi, efficiencyPlots)

# process.taupteff = cms.EDAnalyzer("HPlusCandViewMultiEfficiencyPerObjectAnalyzer",
#     tau_ = cms.untracked.PSet(
#         src = cms.InputTag(selectedTaus),
#         histograms = cms.VPSet(
#             cms.PSet(
#                 nbins = cms.untracked.int32(100),
#                 description = cms.untracked.string('tau pt (GeV/c)'),
#                 plotquantity = cms.untracked.string('pt()'),
#                 min = cms.untracked.double(0.0),
#                 max = cms.untracked.double(100.0),
#                 cuttype = cms.untracked.string(">"),
#                 lazyParsing = cms.untracked.bool(True),
#                 name = cms.untracked.string('pt')
#             )
#         )
#     )
# )
# process.taupteffevent = cms.EDAnalyzer("HPlusCandViewMultiEfficiencyPerEventAnalyzer",
#     tau_ = cms.untracked.PSet(
#         src = cms.InputTag(selectedTaus),
#         histograms = cms.VPSet(
#             cms.PSet(
#                 nbins = cms.untracked.int32(100),
#                 description = cms.untracked.string('tau pt (GeV/c)'),
#                 plotquantity = cms.untracked.string('pt()'),
#                 min = cms.untracked.double(0.0),
#                 max = cms.untracked.double(100.0),
#                 cuttype = cms.untracked.string(">"),
#                 lazyParsing = cms.untracked.bool(True),
#                 name = cms.untracked.string('pt')
#             )
#         )
#     )
# )
# process.analysis *= process.taupteff
# process.analysis *= process.taupteffevent

#### Trigger
# from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
# process.TriggerFilter = triggerResultsFilter.clone()
# process.TriggerFilter.hltResults = cms.InputTag("TriggerResults", "", "REDIGI36X")
# process.TriggerFilter.l1tResults = cms.InputTag("")
# #process.TriggerFilter.throw = cms.bool(False) # Should it throw an exception if the trigger product is not found
# process.TriggerFilter.triggerConditions = cms.vstring("HLT_Mu9")
# process.countTrigger = cms.EDProducer("EventCountProducer")
# process.analysis *= process.TriggerFilter
# process.analysis *= process.countTrigger
# process.counters.counters.append(cms.InputTag("countTrigger"))

# hi+=1
# histoAnalyzer = cloneModule(process, process.analysis, "h%02d_trigger"%hi, histoAnalyzer)


#### Tau Pt cut
hi+=1
selectedTaus = addCut(process, process.analysis, "TauPtCut", selectedTaus, "pt() > 20.", counter=process.counters)
# Clone the set of histograms to plot after the cut and update the collection of selected taus
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_tauptcut"%hi, histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Tau Eta cut
hi+=1 
selectedTaus = addCut(process, process.analysis, "TauEtaCut", selectedTaus, "abs(eta()) < 2.4", counter=process.counters)
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_tauetacut"%hi, histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

# #### Tau leading track pt cut
hi+=1
selectedTaus = addCut(process, process.analysis, "TauLeadTrkPtCut", selectedTaus, "leadTrack().isNonnull() && leadTrack().pt() > 20.", counter=process.counters)
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_tauldgtrkptcut"%hi, histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Demand exactly one tau jet
process.TauNumberFilter = cms.EDFilter("PATCandViewCountFilter",
    src = selectedTaus,
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1)
)
process.countTauNumber = cms.EDProducer("EventCountProducer")
process.analysis *= process.TauNumberFilter
process.analysis *= process.countTauNumber
process.counters.counters.append(cms.InputTag("countTauNumber"))

histoAnalyzer = cloneModule(process, process.analysis, "h%02d_taunumbercut"%hi, histoAnalyzer)
hi+=1

#### Clean jet collection from tau jet
process.cleanedPatJets = cms.EDProducer("PATJetCleaner",
    src = selectedJets,
    preselection = cms.string(""),
    checkOverlaps = cms.PSet(
        taus = cms.PSet(
            src = selectedTaus,
            algorithm = cms.string("byDeltaR"),
            preselection = cms.string(""),
            deltaR = cms.double(0.5),
            checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
            pairCut = cms.string(""),
            requireNoOverlaps = cms.bool(True), # overlaps causes the jet to be discarded
        )
    ),
    finalCut = cms.string("")
)
process.analysis *= process.cleanedPatJets
selectedJets = cms.InputTag("cleanedPatJets")


#### Jet pt cut
hi+=1
selectedJets = addCut(process, process.analysis, "JetPtCut", selectedJets, "pt() > 20.", min=2, counter=process.counters)
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_jetptcut"%hi, histoAnalyzer)
histoAnalyzer.jet_.src = selectedJets

#### Jet eta cut
hi+=1
selectedJets = addCut(process, process.analysis, "JetEtaCut", selectedJets, "abs(eta()) < 2.4", min=2, counter=process.counters)
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_jetetacut"%hi, histoAnalyzer)
histoAnalyzer.jet_.src = selectedJets

#### B-tagging
hi+=1
selectedBjets = addCut(process, process.analysis, "Btagging", selectedJets, "bDiscriminator('trackCountingHighEffBJetTags') > 1.5", min=1, counter=process.counters)
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_btagging"%hi, histoAnalyzer)
histoAnalyzer.bjet_ = cms.untracked.PSet(
    src = selectedBjets,
    histograms = cms.VPSet([h.pset() for h in jetHistos])
)

#### MET cut
hi+=1
selectedMet = addCut(process, process.analysis, "METCut", selectedMet, "et() > 40.", counter=process.counters)

# calculate transverse mass
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusTransverseMassProducer_cfi")
process.transverseMass.tauSrc = selectedTaus
process.transverseMass.metSrc = selectedMet
process.analysis *= process.transverseMass

# add transverse mass plot to the MultiHistoAnalyzer which is run after the MET cut
histoAnalyzer = cloneModule(process, process.analysis, "h%02d_metcut"%hi, histoAnalyzer)
histoAnalyzer.met_.src = selectedMet
histoAnalyzer.transverseMass_ = cms.untracked.PSet(
    src = cms.InputTag("transverseMass"),
    histograms = cms.VPSet(Histo("mt", "mass()", min=0, max=200, nbins=100, description="m_T").pset())
)


process.path    = cms.Path(process.analysis)

################################################################################
# Efficiency plots after full selection

process.fullEfficiencyPerEvent = cms.EDAnalyzer("HPlusCandViewFullEfficiencyPerEventAnalyzer",
    tau_ = cms.untracked.PSet(
        src = fixedConeTaus,
        histograms = cms.VPSet(cms.PSet(
            nbins = cms.untracked.int32(100),
            description = cms.untracked.string('tau pt (GeV/c)'),
            plotquantity = cms.untracked.string('pt()'),
            min = cms.untracked.double(0.5),
            max = cms.untracked.double(100.5),
            lazyParsing = cms.untracked.bool(True),
            name = cms.untracked.string('pt'),
            cuttype = cms.untracked.string('>'),
            cutvalue = cms.untracked.double(20.)
        ),
        cms.PSet(
            nbins = cms.untracked.int32(30),
            description = cms.untracked.string('tau eta'),
            plotquantity = cms.untracked.string('abs(eta())'),
            min = cms.untracked.double(0.05),
            max = cms.untracked.double(3.05),
            lazyParsing = cms.untracked.bool(True),
            name = cms.untracked.string('eta'),
            cuttype = cms.untracked.string('<'),
            cutvalue = cms.untracked.double(2.4),
        ),
        cms.PSet(
            nbins = cms.untracked.int32(100),
            description = cms.untracked.string('tau leading track pt (GeV/c)'),
            plotquantity = cms.untracked.string('? leadTrack().isNonnull() ? leadTrack().pt() : -1'),
            min = cms.untracked.double(0.5),
            max = cms.untracked.double(100.5),
            lazyParsing = cms.untracked.bool(True),
            name = cms.untracked.string('ldgtrkpt'),
            cuttype = cms.untracked.string('>'),
            cutvalue = cms.untracked.double(20.)
        ))
    ),
    jet_ = cms.untracked.PSet(
        src = jpt_jets,
        histograms = cms.VPSet(cms.PSet(
            nbins = cms.untracked.int32(100),
            description = cms.untracked.string('jet pt (GeV/c)'),
            plotquantity = cms.untracked.string('pt()'),
            min = cms.untracked.double(0.5),
            max = cms.untracked.double(100.5),
            lazyParsing = cms.untracked.bool(True),
            name = cms.untracked.string('pt'),
            minObjects = cms.untracked.uint32(3),
            cuttype = cms.untracked.string('>'),
            cutvalue = cms.untracked.double(20.)
        ))
    )
)
process.fullEffPath = cms.Path(process.fullEfficiencyPerEvent)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
#    SelectEvents = cms.untracked.PSet(
#        SelectEvents = cms.vstring("path")
#    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
#        "keep *_*_*_HChSignalAnalysis"
	"drop *",
        "keep edmMergeableCounter_*_*_*"
    )
)

process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.path,
    process.fullEffPath,
    process.counterPath,
    process.outpath
)
