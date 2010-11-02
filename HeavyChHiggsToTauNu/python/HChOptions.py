import FWCore.ParameterSet.VarParsing as VarParsing
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
                     "",
                     options.multiplicity.singleton, options.varType.string,
                     "Trigger to use")

    # Protection in case sys.argv is missing due to various edm tools
    if not hasattr(sys, "argv"):
        return options

    # Hack to be able to pass multiple arguments from multicrab.cfg
    if len(sys.argv) > 0:
        last = sys.argv.pop()
        sys.argv.extend(last.split(":"))

    options.parseArguments()

    return options
