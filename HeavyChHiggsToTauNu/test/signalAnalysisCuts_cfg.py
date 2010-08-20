import FWCore.ParameterSet.Config as cms

#dataVersion = "35X"
dataVersion = "36X"
#dataVersion = "37X"

process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All
if dataVersion == "37X":
    process.GlobalTag.globaltag = cms.string("START37_V6::All")
else:
    process.GlobalTag.globaltag = cms.string("START36_V10::All")

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/FA6E6683-C844-DF11-A2D8-0018F3D0961E.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/D0E1C289-C744-DF11-B84C-00261894389F.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/A24BB684-C544-DF11-81ED-00261894391D.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/284100C7-4E45-DF11-9AF9-0018F3D09710.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/06A4E187-C644-DF11-BC3E-0018F3D096AA.root'
  )
)

process.source.fileNames = cms.untracked.vstring("file:pattuple.root")

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.TFileService.fileName = "histograms.root"

process.countAll = cms.EDProducer("EventCountProducer")
process.analysis = cms.Sequence(process.countAll)

taus = "selectedPatTaus"

calo_jets = "selectedPatJets"
jpt_jets = "selectedPatJetsAK5JPT"
jets = jpt_jets

calo_met = "patMETs"
pf_met = "patMETsPF"
tc_met = "patMETsTC"
met = pf_met

def addCut(process, sequence, name, src, cut, min=1, selector="CandViewSelector"):
    cutname = name
    filtername = name+"Filter"
    countname = "count"+name

    m1 = cms.EDFilter(selector,
                      src = cms.InputTag(src),
                      cut = cms.string(cut))
    m2 = cms.EDFilter("CandViewCountFilter",
                      src = cms.InputTag(name),
                      minNumber = cms.uint32(min))
    m3 = cms.EDProducer("EventCountProducer")
    process.__setattr__(cutname, m1)
    process.__setattr__(filtername, m2)
    process.__setattr__(countname, m3)

    for n in [m1, m2, m3]:
        sequence *= n

    return cutname

def addHisto(process, sequence, name, m):
    process.__setattr__(name, m)
    sequence *= m

def addHistoAnalyzer(process, sequence, name, src, lst):
    histos = cms.VPSet()
    for histo in lst:
        histos.append(histo.pset())
    addHisto(process, sequence, name, cms.EDAnalyzer("CandViewHistoAnalyzer", src=cms.InputTag(src), histograms=histos))

class Histo:
    def __init__(self, name, expr, min, max, nbins, description=None, lazy=True):
        self.min = min
        self.max = max
        self.nbins = nbins
        self.name = name
        self.expr = expr
        self.lazy = lazy
        if description == None:
            self.descr = name
        else:
            self.descr = description

    def pset(self):
        return cms.PSet(min = cms.untracked.double(self.min),
                        max = cms.untracked.double(self.max),
                        nbins = cms.untracked.int32(self.nbins),
                        name = cms.untracked.string(self.name),
                        plotquantity = cms.untracked.string(self.expr),
                        description = cms.untracked.string(self.descr),
                        lazyParsing = cms.untracked.bool(self.lazy))

tauHistos = [
    Histo("taupt", "pt()", min=0., max=100., nbins=100, description="tau pt (GeV/c)"),
    Histo("taueta", "eta()", min=-3, max=3, nbins=60, description="tau eta"),
    Histo("tauldgtrkpt", "? leadTrack().isNonnull() ? leadTrack().pt() : -1", min=0., max=100., nbins=100, description="tau leading track pt (GeV/c)")
    ]
jetHistos = [Histo("jetpt", "pt()", min=0., max=100., nbins=100, description="jet pt (GeV/c)")]
metHistos = [Histo("metet", "et()", min=0., max=100., nbins=100, description="met et (GeV/c)")]

def addHistoAnalyzers(process, sequence, prefix, lst):
    for t in lst:
        addHistoAnalyzer(process, sequence, prefix+"_"+t[0], t[1], t[2])

#### Beginning
addHistoAnalyzers(process, process.analysis, "00_beginning", [
    ("tau", taus, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])
                  
#### Tau Pt cut
prevtaucut = addCut(process, process.analysis, "TauPtCut", taus, "pt() > 30.", selector="PATTauSelector")
addHistoAnalyzers(process, process.analysis, "01_tauptcut", [
    ("tau", prevtaucut, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])

#### Tau Eta cut
prevtaucut = addCut(process, process.analysis, "TauEtaCut", prevtaucut, "abs(eta()) < 2.4", selector="PATTauSelector")
addHistoAnalyzers(process, process.analysis, "02_tauetacut", [
    ("tau", prevtaucut, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])

#### Tau leading track pt cut
#prevcut = addCut(process, process.analysis, "TauLeadTrkPtCut", prevcut, "? isPFTau ? (leadPFChargedHadrCand().isNonnull() && leadPFChargedHardCand().pt() > 30.) : (leadTrack().isNonnull() && leadTrack().pt() > 30.)", selector="PATTauSelector")
prevtaucut = addCut(process, process.analysis, "TauLeadTrkPtCut", prevtaucut, "leadTrack().isNonnull() && leadTrack().pt() > 30.", selector="PATTauSelector")
addHistoAnalyzers(process, process.analysis, "03_tauldgtrkptcut", [
    ("tau", prevtaucut, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])

#### Jet pt cut
prevjetcut = addCut(process, process.analysis, "JetPtCut", jets, "pt() > 30.", min=3)
addHistoAnalyzers(process, process.analysis, "02_jetptcut", [
    ("tau", prevtaucut, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])

# MET cut
prevmetcut = addCut(process, process.analysis, "METCut", met, "et() > 40.")
addHistoAnalyzers(process, process.analysis, "02_metcut", [
    ("tau", prevtaucut, tauHistos),
    ("calojet", calo_jets, jetHistos),
    ("jptjet", jpt_jets, jetHistos),
    ("calomet", calo_met, metHistos),
    ("pfmet", pf_met, metHistos),
    ("tcmet", tc_met, metHistos)])
                                                    

process.path    = cms.Path(process.analysis)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
#    SelectEvents = cms.untracked.PSet(
#        SelectEvents = cms.vstring("path")
#    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
	"drop *",
        "keep edmMergeableCounter_*_*_*"
    )
)

process.outpath = cms.EndPath(process.out)

