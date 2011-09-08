import FWCore.ParameterSet.VarParsing as VarParsing
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import sys

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
                     "Trigger to use")
    options.register("tauEmbeddingInput",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Input is from tau embedding (default: 0)")
    options.register("tauIDFactorizationMap",
                     "FactorizationMap_NoFactorization_cfi",
                     options.multiplicity.singleton,
                     options.varType.string,
                     "Factorization map config file")
    options.register("runOnCrab",
                     0,
                     options.multiplicity.singleton,
                     options.varType.int,
                     "Set to 1 if job will be run with crab. Typically you don't have to set it by yourself, since it is set in crab.cfg/multicrab.cfg")

    # Protection in case sys.argv is missing due to various edm tools
    if not hasattr(sys, "argv"):
        return options

    # Hack to be able to pass multiple arguments from multicrab.cfg
    if len(sys.argv) > 0:
        last = sys.argv.pop()
        sys.argv.extend(last.split(":"))

    options.parseArguments()

    return options


def getOptionsDataVersion(dataVersion, options=None, useDefaultSignalTrigger=True):
    options = getOptions(options)

    if options.dataVersion != "":
        dataVersion = options.dataVersion
    print "Data version is", dataVersion

    dataVersion = DataVersion(dataVersion)

    if useDefaultSignalTrigger and options.trigger == "" and dataVersion.isMC():
        options.trigger = dataVersion.getDefaultSignalTrigger()

    return (options, dataVersion)


def getTauIDFactorizationMap(options):
    if options.tauIDFactorizationMap != "":
        myFactorizationMapName = "HiggsAnalysis.HeavyChHiggsToTauNu."+options.tauIDFactorizationMap
    else:
        raise RuntimeError, "HChOptions::getTauIDFactorizationMap: Check default parameter value!"
    print "tauID factorization map is:", myFactorizationMapName
    return myFactorizationMapName
