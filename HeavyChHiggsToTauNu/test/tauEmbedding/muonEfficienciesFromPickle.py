#!/usr/bin/env python

## Reads and prints muon ID efficiencies from a pickle format

import sys
import pickle

class EffValue:
    def __init__(self, name, firstRun=None, lastRun=None):
        self.name = name
        self.firstRun = firstRun
        self.lastRun = lastRun
        self.bins = []

    def addBin(self, eta, bin, uncertainty):
        self.bins.append( (eta, bin, uncertainty) )

    def content(self):
        ret = ["%s = cms.PSet(" % self.name]
        if self.firstRun is not None:
            ret.append("    firstRun = cms.uint32(%s)," % self.firstRun)
        if self.lastRun is not None:
            ret.append("    lastRun = cms.uint32(%s)," % self.lastRun)

        ret.append("    bins = cms.VPSet(")
        for b in self.bins:
            ret.append("         triggerBin(%s, %f, %f)," % b)
        ret.extend([
                "    ),",
                "),",
                ])

        return ret

def extract2011(data):
    dataParameters = []
    mcParameters = []

    numbers = "TIGHT_nL8"
    dataEras = [
        "2011A",
        "2011B"
    ]

    for era in dataEras2011:
        etaBinDict = data[numbers+"_"+era]["eta_pt>20"]
        etaBinNames = etaBinDict.keys()
        etaBins = [(n.split("_")[0], n) for n in etaBinNames]
        etaBins.sort(key=lambda x: float(x[0]))

        dataEff = EffValue("Run"+era)
        mcEff = EffValue("Run"+era)
        for bin, name in etaBins:
            mcEff.addBin(bin,
                         etaBinDict[name]["mc"]["efficiency"],
                         max(etaBinDict[name]["mc"]["err_low"], etaBinDict[name]["mc"]["err_hi"]))
            dataEff.addBin(bin,
                         etaBinDict[name]["data"]["efficiency"],
                         max(etaBinDict[name]["data"]["err_low"], etaBinDict[name]["data"]["err_hi"]))

        dataParameters.append(dataEff)
        mcParameters.append(mcEff)

    return (dataParameters, mcParameters)

def extract2012id(data):
    dataParameters = []
    mcParameters = []

    numbers = "Tight"

    etaBinDict = data[numbers]["etapt20-500"]
    etaBinNames = etaBinDict.keys()
    etaBins = [(n.split("_")[0], n) for n in etaBinNames]
    etaBins.sort(key=lambda x: float(x[0]))

    dataEff = EffValue("Run2012ABCD")
    mcEff = EffValue("Run2012ABCD")
    for bin, name in etaBins:
        mcEff.addBin(bin,
                     etaBinDict[name]["mc"]["efficiency"],
                     max(etaBinDict[name]["mc"]["err_low"], etaBinDict[name]["mc"]["err_hi"]))
        dataEff.addBin(bin,
                       etaBinDict[name]["data"]["efficiency"],
                       max(etaBinDict[name]["data"]["err_low"], etaBinDict[name]["data"]["err_hi"]))
    dataParameters.append(dataEff)
    mcParameters.append(mcEff)

    return (dataParameters, mcParameters)

def extract2012trigger(data):
    dataParameters = []
    mcParameters = []

    trigger = "Mu40"
    id = "TightID"

    etaBinDict = data[trigger][id]["ETA"]
    etaBinNames = etaBinDict.keys()
    etaBins = [(n.split("_")[0], n) for n in etaBinNames]
    etaBins.sort(key=lambda x: float(x[0]))

    dataEff = EffValue("Run2012ABCD")
    mcEff = EffValue("Run2012ABCD")
    for bin, name in etaBins:
        mcEff.addBin(bin,
                     etaBinDict[name]["mc"]["efficiency"],
                     max(etaBinDict[name]["mc"]["err_low"], etaBinDict[name]["mc"]["err_hi"]))
        dataEff.addBin(bin,
                       etaBinDict[name]["data"]["efficiency"],
                       max(etaBinDict[name]["data"]["err_low"], etaBinDict[name]["data"]["err_hi"]))
    dataParameters.append(dataEff)
    mcParameters.append(mcEff)

    return (dataParameters, mcParameters)

def main(args):
    if len(args) != 1:
        raise Exception("Expecting one pickle file")

    f = open(args[0])
    data = pickle.load(f)
    f.close()

    #(dataParameters, mcParameters) = extract2011(data)
    #(dataParameters, mcParameters) = extract2012id(data)
    (dataParameters, mcParameters) = extract2012trigger(data)
    

    res = [
        "def triggerBin(eta, eff, unc):",
        "    return cms.PSet(",
        "        eta = cms.double(eta),",
        "        efficiency = cms.double(eff),",
        "        uncertainty = cms.double(unc),",
        "    )",
        "",
        "# Taken from https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs",
        "# file %s" % args[0],
        "efficiency_pickle = cms.untracked.PSet(",
        "    dataParameters = cms.PSet("]
    for dp in dataParameters:
        res.extend(["        "+x for x in dp.content()])
    res.extend(["    ),",
                "    mcParameters = cms.PSet("])
    for mp in mcParameters:
        res.extend(["        "+x for x in mp.content()])
    res.extend(["    ),",
                "    dataSelect = cms.vstring("])
    for dp in dataParameters:
        res.append('        "%s",' % dp.name)
    res.extend(["    ),",
                '    mcSelect = cms.string("%s"),' % mcParameters[0].name,
                '    mode = cms.untracked.string("disabled"),',
                '    type = cms.untracked.string("binned"),',
                ")"])

    print "\n".join(res)

if __name__ == "__main__":
    main(sys.argv[1:])
