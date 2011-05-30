import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "311Xredigi"
#dataVersion = "41Xdata"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("TauEmbeddingAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_pattuple_v11b/8f83bb72c10133f1e52d950030b925c8/pattuple_134_1_0lc.root"
  )
)
################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.FwkReport.reportEvery = 1


process.TFileService.fileName = "histograms.root"

process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer")
if options.crossSection >= 0.:
    process.configInfo.crossSection = cms.untracked.double(options.crossSection)
    print "Dataset cross section has been set to %g pb" % options.crossSection
if options.luminosity >= 0:
    process.configInfo.luminosity = cms.untracked.double(options.luminosity)
    print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity

process.commonSequence = cms.Sequence(
    process.configInfo
)

debug=False
if debug:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
    process.wGenParticles = cms.EDProducer("GenParticlePruner",
        src = cms.InputTag("genParticles"),
        select = cms.vstring(
            "drop  *  ", # this is the default
            "keep++ pdgId = {W+} | pdgId = {W-}",
        )
    )
    process.commonSequence *= process.wGenParticles
    process.commonSequence *= process.printGenParticles
    process.printGenList.src = cms.InputTag("wGenParticles")

################################################################################

# Nu MET                  
process.genMetNu = cms.EDProducer("HPlusGenMETFromNuProducer",
    src = cms.InputTag("genParticles")
)

process.commonSequence *= process.genMetNu


################################################################################


from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *

# Pileup weighting
weight = None
# weighting not possible with tauAnalysis (necessary collection missing from tauAnalysis)
# if dataVersion.isMC():
#     import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as params
#     params.setPileupWeightFor2010()
#     params.setPileupWeightFor2011()
#     params.setPileupWeightFor2010and2011()
#     process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
#         alias = cms.string("pileupWeight")
#     )
#     insertPSetContentsTo(params.vertexWeight, process.pileupWeight)
#     process.commonSequence *= process.pileupWeight
#     weight = "pileupWeight"


#taus = "selectedPatTausShrinkingConePFTau"
taus = "selectedPatTausHpsPFTau"
#pfMET = "pfMet"
pfMET = "patMETsPF"
jets = "selectedPatJetsAK5PF"

process.LooseTauId = cms.EDFilter("PATTauSelector",
    src = cms.InputTag(taus),
    cut = cms.string("abs(eta) < 2.1 "
                     "&& leadPFChargedHadrCand().isNonnull() "
                     "&& tauID('againstMuonTight') > 0.5 && tauID('againstElectronMedium') > 0.5"
                     "&& tauID('byVLooseIsolation')"
#                     "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                     )
)
process.commonSequence *= process.LooseTauId

process.LooseTauPtId = cms.EDFilter("PATTauSelector",
    src = cms.InputTag(taus),
    cut = cms.string("pt > 40 "
                     "&& abs(eta) < 2.1 "
                     "&& leadPFChargedHadrCand().isNonnull() "
                     "&& tauID('againstMuonTight') > 0.5 && tauID('againstElectronMedium') > 0.5"
                     "&& tauID('byVLooseIsolation')"
#                     "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                     )
)
process.commonSequence *= process.LooseTauPtId
                     

EmbeddingAnalyzer = cms.EDAnalyzer("HPlusTauEmbeddingTauAnalyzer",
    tauSrc = cms.untracked.InputTag(taus),
    genParticleSrc = cms.untracked.InputTag("genParticles"),
    mets = cms.untracked.PSet(
        Met = cms.untracked.InputTag(pfMET),
#        GenMetTrue = cms.untracked.InputTag("genMetTrue"),
#        GenMetCalo = cms.untracked.InputTag("genMetCalo"),
#        GenMetCaloAndNonPrompt = cms.untracked.InputTag("genMetCaloAndNonPrompt"),
        GenMetNuSum = cms.untracked.InputTag("genMetNu"),
    ),
    genTauMatchingCone = cms.untracked.double(0.5),
    genTauPtCut = cms.untracked.double(-1),
    genTauEtaCut = cms.untracked.double(-1)
)
if weight != None:
    EmbeddingAnalyzer.prescaleSource = cms.untracked.InputTag(weight)

def addPath(prefix, **kwargs):
    path = cms.Path(process.commonSequence)
    setattr(process, prefix+"Path", path)

    if "preSequence" in kwargs:
        path *= kwargs["preSequence"]

    for name, tag in [("", taus),
                      ("tauId", "LooseTauId"),
                      ("tauPtId", "LooseTauPtId")]:
        for ptcut, etacut in [(-1, -1), (30, -1), (30, 2.1)]:
            pteta = ""
            if ptcut > 0 or etacut > 0:
                pteta += "Gen"
            if ptcut > 0:
                pteta += "Pt%d" % ptcut
            if etacut > 0:
                pteta += ("Eta%.1f" % etacut).replace(".", "")
    
            m = EmbeddingAnalyzer.clone(
                tauSrc = cms.untracked.InputTag(tag),
                genTauPtCut = cms.untracked.double(ptcut),
                genTauEtaCut = cms.untracked.double(etacut)
            )
            setattr(process, prefix+pteta+name+"TauAnalyzer", m)
            path *= m

addPath("")

process.goodJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag(jets),
    cut = cms.string(
        "pt() > 30 && abs(eta()) < 2.4"
        "&& numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99 && neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99 && chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0"
   )
)
process.goodJetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodJets"),
    minNumber = cms.uint32(3)
)


process.goodJetSequence = cms.Sequence(
    process.goodJets *
    process.goodJetFilter
)


process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.goodJetSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
process.muonVeto = cms.EDFilter("HPlusGlobalMuonVetoFilter",
    vertexSrc = cms.InputTag("firstPrimaryVertex"),
    GlobalMuonVeto = param.GlobalMuonVeto
)
process.electronVeto = cms.EDFilter("HPlusGlobalElectronVetoFilter",
    GlobalElectronVeto = param.GlobalElectronVeto
)
process.goodJetSequence *= (process.muonVeto*process.electronVeto)


addPath("Jets3", preSequence=process.goodJetSequence)
