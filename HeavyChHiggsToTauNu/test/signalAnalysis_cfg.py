import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

#dataVersion = "35X"
dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"


process.genRunInfo = cms.EDAnalyzer("HPlusGenRunInfoAnalyzer",
    src = cms.untracked.InputTag("generator")
)
process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer",
    crossSection = cms.untracked.double(options.crossSection)
)
process.infoPath = cms.Path(
    process.genRunInfo +
    process.configInfo
)
print "Dataset cross section has been set to %g pb" % options.crossSection


# Signal analysis module
process.signalAnalysis = cms.EDProducer("HPlusSignalAnalysisProducer",
    trigger = cms.untracked.PSet(
        src = cms.untracked.InputTag("patTriggerEvent"),
        trigger = cms.untracked.string("HLT_SingleLooseIsoTau20")
    ),
    tauSelection = cms.untracked.PSet(
        #src = cms.untracked.InputTag("patPFTauProducerFixedCone"),
        #src = cms.untracked.InputTag("selectedPatTausCaloRecoTau"),
        src = cms.untracked.InputTag("selectedPatTausFixedConePFTau"),
        #src = cms.untracked.InputTag("selectedPatTausShrinkingConePFTau"),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        leadingTrackPtCut = cms.untracked.double(10)
    ),
    jetSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("selectedPatJets"),
#        src = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
        cleanTauDR = cms.untracked.double(0.5),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        minNumber = cms.untracked.uint32(3)
    ),
    bTagging = cms.untracked.PSet(
        discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
        discriminatorCut = cms.untracked.double(1.5),
        minNumber = cms.untracked.uint32(1)
    ),
    MET = cms.untracked.PSet(
        src = cms.untracked.InputTag("patMETs"), # calo MET
#        src = cms.untracked.InputTag("patMETsPF"), # PF MET
#        src = cms.untracked.InputTag("patMETsTC"), # tc MET
        METCut = cms.untracked.double(40)
    )
)
# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.signalAnalysisCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("signalAnalysis", "counterNames"),
    counterInstances = cms.untracked.InputTag("signalAnalysis", "counterInstances"),
    verbose = cms.untracked.bool(True)
)
process.signalAnalysisPath = cms.Path(
    process.signalAnalysis *
    process.signalAnalysisCounters
)

# An example how to create an array of analyzers to do the same
# analysis by varying a single parameter. It is significantly more
# efficienct to run many analyzers in single crab job than to run many
# crab jobs with a single analyzer.
#
#
# def setTauPt(m, val):
#     m.tauSelection.ptCut = val
# from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
# addAnalysisArray(process, "signalAnalysisTauPt", process.signalAnalysis, setTauPt,
#                  [10, 20, 30, 40, 50])


# Print tau discriminators from one tau from one event
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.signalAnalysis.tauSelection.src
)
#process.tauDiscriminatorPrintPath = cms.Path(process.tauDiscriminatorPrint)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *_*_*_HChSignalAnalysis",
        "drop *_*_counterNames_*",
        "drop *_*_counterInstances_*"
#	"drop *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
#process.outpath = cms.EndPath(process.out)

