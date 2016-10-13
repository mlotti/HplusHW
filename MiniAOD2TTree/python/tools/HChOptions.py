import FWCore.ParameterSet.VarParsing as VarParsing
from HiggsAnalysis.MiniAOD2TTree.tools.HChDataVersion import DataVersion
import sys

validSampleValues = [
    "WJets",
    "W1Jets",
    "W2Jets",
    "W3Jets",
    "W4Jets",
    "TTJets",
]

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
def getOptions(options=None):
    if options == None:
        options = VarParsing.VarParsing()
    options.register("crossSection",
                     -1., # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.float,          # string, int, or float
                     "Cross section of the dataset (stored to histograms ROOT file)")
    options.register("luminosity",
                     -1., # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.float,          # string, int, or float
                     "Integrated luminosity of the dataset (stored to histograms ROOT file)")
    options.register("dataVersion",
                     "", # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.string,          # string, int, or float
                     "Data version")
    options.register("doPat",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Run PAT on the fly (needed for RECO/AOD samples)")
    options.register("trigger",
                     [],
                     options.multiplicity.list, options.varType.string,
                     "Triggers to use (logical OR if multiple given")
    options.register("doTauHLTMatching",
                     1,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Do tau trigger matching? (default: 1)")
    options.register("doTauHLTMatchingInAnalysis",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Do tau trigger mathching with the InAnalysis method? (default: 0")
    options.register("triggerThrow",
                     1,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Should the TriggerFilter for data throw if trigger path is not found? (default: 1)")
    options.register("triggerMC",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Should MC be triggered? (default: 0) If MC is to be triggered, the default trigger is taken from HChDataVersion (called signalTrigger in there). This can be overridden with the 'trigger' command line argument.")
    options.register("triggerMCInAnalysis",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Should MC be triggered in analysis job, if triggerMC=0? (default: 0)")
    options.register("skimConfig",
                     [],
                     options.multiplicity.list,
                     options.varType.string,
                     "Configuration fragment for a skim to be done during pattuplization (if multiple are given, an OR of skims is taken)")
    options.register("pvSelectionConfig",
                     "",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "Configuration fragment for a primary vertex selection (default is to use offlinePrimaryVertices as it is")
    options.register("customizeConfig",
                     [],
                     options.multiplicity.list,
                     options.varType.string,
                     "Configuration fragment for a generic customization")
    options.register("tauEmbeddingInput",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Input is from tau embedding (default: 0)")
    options.register("tauEmbeddingCaloMet",
#                     "caloMetNoHFSum", no-HF in first part of 2011A, after that HF is included
                     "caloMetSum",
                     options.multiplicity.singleton, options.varType.string,
                     "What calo MET object to use in signal analysis of tau embedded samples")
    options.register("tauEmbeddingTauTrigger",
                     "",
                     options.multiplicity.singleton, options.varType.string,
                     "What tau trigger efficiency to use for tau embedding normalisation")
    options.register("doTauEmbeddingLikePreselection",
                     0,
                     options.multiplicity.singleton, options.varType.int,
                     "Run 'tau embedding'-like preselection for normal MC")
    options.register("runOnCrab",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Set to 1 if job will be run with crab. Typically you don't have to set it by yourself, since it is set in crab.cfg/multicrab.cfg")
    options.register("puWeightEra",
                     "",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "DEPRECATED (should be removed soon) Select specific PU reweighting era (Default: use the one in configuration)")
    options.register("hasMCBJetsFilter",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "If set to 1, chooses only events that have MC b jets; if set to -1, chooses only events that have no MC b jets")
    options.register("energy",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int, # Use integer for now, if we later need e.g. 12.5 TeV, let's use string then
                     "Centre-of-mass energy in TeV")
    options.register("wjetsWeighting",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Set to 1 WJets inclusive+exclusive weighting should be enabled")
    options.register("sample",
                     "",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "Sample name for specific weighting schemes (valid values are: "+", ".join(validSampleValues))
    options.register("bquarkNumFilter",
                     -1,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "b-quark filtering option (-1=disabled, 0=0b, 1=1b, 2=2b, 3=at least 3b)")
    options.register("trgAnalysis",
                     "",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "Giving TTEffAnalyzer info about whether it is TauLeg, MetLeg or QuadJet in question")
    

    # Protection in case sys.argv is missing due to various edm tools
    if not hasattr(sys, "argv"):
        return options

    # Hack to be able to pass multiple arguments from multicrab.cfg
    if len(sys.argv) > 0:
        last = sys.argv.pop()
        sys.argv.extend(last.split(":"))

    options.parseArguments()

    if options.doPat != 0 and options.doTauHLTMatchingInAnalysis != 0:
        raise Exception("doTauHLTMatchingInAnalysis may not be used with doPat=1 (use PAT trigger matching instead)")
    if options.sample != "" and options.sample not in validSampleValues:
        raise Exception("Invalid value '%s' of 'sample' command line parameter, valid values are %s" % (options.sample, ", ".join(validSampleValues)))

    return options


def getOptionsDataVersion(dataVersion, options=None, useDefaultSignalTrigger=True):
    options = getOptions(options)
    if options.dataVersion != "":
        dataVersion = options.dataVersion
    #print "Data version is", dataVersion

    dataVersion = DataVersion(dataVersion)
    if useDefaultSignalTrigger and len(options.trigger) == 0 and dataVersion.isMC() and options.tauEmbeddingInput == 0:
        options.trigger = [dataVersion.getDefaultSignalTrigger()]

    return (options, dataVersion)
