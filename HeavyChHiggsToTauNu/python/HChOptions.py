import FWCore.ParameterSet.VarParsing as VarParsing
import sys

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
def getOptions():
    options = VarParsing.VarParsing()
    options.register("crossSection",
                     0., # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.float,          # string, int, or float
                     "Cross section of the dataset (stored to histograms ROOT file)")
    options.register("dataVersion",
                     "", # default value
                     options.multiplicity.singleton, # singleton or list
                     options.varType.string,          # string, int, or float
                     "Data version")

    # Protection in case sys.argv is missing due to various edm tools
    if not hasattr(sys, "argv"):
        return options

    # Hack to be able to pass multiple arguments from multicrab.cfg
    if len(sys.argv) > 0:
        last = sys.argv.pop()
        sys.argv.extend(last.split(":"))

    options.parseArguments()

    return options
