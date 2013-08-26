import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions

#dataVersion = "35X"
dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "37X"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion

process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
#    skipEvents = cms.untracked.uint32(500),
    fileNames = cms.untracked.vstring(
    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTbar_Htaunu_M80/TTbar_Htaunu_M80/Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_test5/744fc999107787b3f27dc1fe1e804784/pattuple_4_1_pCt.root"
    #"dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTbar_Htaunu_M80/TTbar_Htaunu_M80/Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_test5/744fc999107787b3f27dc1fe1e804784/pattuple_4_1_pCt.root"
#        "file:pattuple-1000.root"
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.TFileService.fileName = "histograms.root"

# Import cut and histogrammint tools
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *

# Create the Analysis object, which helps to build the proper
# configuration
analysis = Analysis(process, "analysis", options)

# Module for miscellaneous debugging
process.debug = cms.EDAnalyzer("HPlusDebugAnalyzer",
    jetSrc = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
    tauSrc = cms.untracked.InputTag("selectedPatTaus"),
    trigSrc = cms.untracked.InputTag("TriggerResults", "", "REDIGI36X")
)
#analysis.appendToSequence(process.debug)

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

# keep the previous histogram analyzer in the histoAnalyzer variable
histoAnalyzer = analysis.addMultiHistoAnalyzer("beginning", [
    ("tau_", selectedTaus, tauHistos),
    ("jet_", selectedJets, jetHistos),
    ("calojet_", calo_jets, jetHistos),
    ("jptjet_", jpt_jets, jetHistos),
    ("met_", selectedMet, metHistos),
    ("calomet_", calo_met, metHistos),
    ("pfmet_", pf_met, metHistos),
    ("tcmet_", tc_met, metHistos)])

#### Trigger
analysis.addTriggerCut(dataVersion, "HLT_SingleLooseIsoTau20")
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("trigger", histoAnalyzer)

#### Tau Pt cut
selectedTaus = analysis.addCut("TauPtCut", selectedTaus, "pt() > 20.")
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("tauptcut", histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Tau Eta cut
selectedTaus = analysis.addCut("TauEtaCut", selectedTaus, "abs(eta()) < 2.4")
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("tauetacut", histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Tau leading track Pt cut
selectedTaus = analysis.addCut("TauLeadTrkPtPtCut", selectedTaus, "leadTrack().isNonnull() && leadTrack().pt() > 10.")
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("tauleadtrkptptcut", histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Tau ID
tauIDs = [
    "againstElectron",
    "againstMuon",
    "byIsolation",
    "HChTauIDcharge"
]
selectedTaus = analysis.addCut("TauIdCuts", selectedTaus, " && ".join(["tauID('%s')"%x for x in tauIDs]))
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("tauidcut", histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus

#### Demand exactly one tau jet
analysis.addNumberCut("TauNumber", selectedTaus, minNumber=1, maxNumber=1)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("taunumbercut", histoAnalyzer)
histoAnalyzer.tau_.src = selectedTaus


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
analysis.appendToSequence(process.cleanedPatJets)
selectedJets = cms.InputTag("cleanedPatJets")

#### Jet Pt cut
selectedJets = analysis.addCut("JetPtCut", selectedJets, "pt() > 30.", minNumber=3)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("jetptcut", histoAnalyzer)
histoAnalyzer.jet_.src = selectedJets

#### Jet Eta cut
selectedJets = analysis.addCut("JetEtaCut", selectedJets, "abs(eta()) < 2.4", minNumber=3)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("jetetacut", histoAnalyzer)
histoAnalyzer.jet_.src = selectedJets

#### B-tagging
selectedBjets = analysis.addCut("Btagging", selectedJets, "bDiscriminator('trackCountingHighEffBJetTags') > 1.5", minNumber=1)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("btagging", histoAnalyzer)
histoAnalyzer.bjet_ = cms.untracked.PSet(
    src = selectedBjets,
    histograms = cms.VPSet([h.pset() for h in jetHistos])
)


#### MET cut
selectedMet = analysis.addCut("METCut", selectedMet, "et() > 40.")

# calculate transverse mass
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusTransverseMassProducer_cfi")
process.transverseMass.tauSrc = selectedTaus
process.transverseMass.metSrc = selectedMet
analysis.appendToSequence(process.transverseMass)

# add transverse mass plot to the MultiHistoAnalyzer which is run after the MET cut
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("metcut", histoAnalyzer)
histoAnalyzer.met_.src = selectedMet
histoAnalyzer.transverseMass_ = cms.untracked.PSet(
    src = cms.InputTag("transverseMass"),
    histograms = cms.VPSet(Histo("mt", "mass()", min=0, max=200, nbins=100, description="m_T").pset())
)

process.analysisPath = cms.Path(analysis.getSequence())

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
            cutvalue = cms.untracked.double(10.)
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
            cutvalue = cms.untracked.double(30.)
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
        "keep *_*_*_HChSignalAnalysis"
#	"drop *",
#        "keep edmMergeableCounter_*_*_*"
    )
)
#process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.analysisPath,
    process.fullEffPath,
    analysis.getCountPath()
#    ,process.outpath
)


