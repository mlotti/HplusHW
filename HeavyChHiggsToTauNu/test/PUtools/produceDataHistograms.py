#!/usr/bin/env python

# Obtain files from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/
# as instructed in https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

import os
import subprocess

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi as certifiedLumi
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTools as multicrabWorkflowsTools


minBiasXsec = 69300
options = [
    "--calcMode",      "true",
    "--maxPileupBin",  "60",
    "--numPileupBins", "1200"
]
outputFileName = "PileupHistogramData"

jsonPath = ".."
runsJson = [
    (["2012A"], 190456, 190738, certifiedLumi.files["13Jul2012ReReco"]),
    (["2012A"], 190782, 190949, certifiedLumi.files["06Aug2012ReReco"]),
    (["2012A"], 191043, 193621, certifiedLumi.files["13Jul2012ReReco"]),
    (["2012B"], 193834, 196531, certifiedLumi.files["13Jul2012ReReco"]),
    (["2012C"], 198022, 198523, certifiedLumi.files["24Aug2012ReReco"]),
    (["2012C"], 198941, 200601, certifiedLumi.files["PromptReco12"]),
    (["2012C"], 202792, 203742, certifiedLumi.files["PromptReco12"]),
    ]
for tpl in runsJson:
    tpl[0].append("2012ABC")
eraPUJson = {
    "2012A": "pileup_JSON_DCSONLY_190389-200041_pixelcorr.txt",
    "2012B": "pileup_JSON_DCSONLY_190389-200041_pixelcorr.txt",
    "2012C": "pileup_JSON_DCSONLY_190389-204506_corr.txt",

    "2012AB": "pileup_JSON_DCSONLY_190389-200041_pixelcorr.txt",
    "2012ABC": "pileup_JSON_DCSONLY_190389-200041_pixelcorr_upto196531_190389-204506_corr.txt",
}

processEras = [
#    "2012A",
#    "2012B",
#    "2012C",
    "2012ABC",
]


def main():
    if not os.path.exists(eraPUJson["2012ABC"]):
        print "Creating PU json", eraPUJson["2012ABC"]
        cmd = ["filterJSON.py", "--max", "196531", "--output", "tmp1.txt", eraPUJson["2012A"]]
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))

        cmd = ["filterJSON.py", "--min", "198022", "--output", "tmp2.txt", eraPUJson["2012C"]]
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))

        cmd = ["mergeJSON.py", "--output", eraPUJson["2012ABC"], "tmp1.txt", "tmp2.txt"]
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))
        os.remove("tmp1.txt")
        os.remove("tmp2.txt")

    print "Filtering run/lumi JSON files according to eras and our run ranges"
    eraJsons = {}
    for eras, firstRun, lastRun, jsonfile in runsJson:
        filteredJson = jsonfile.replace(".txt", "_%d-%d.txt" % (firstRun, lastRun))
        cmd = ["filterJSON.py", "--min", str(firstRun), "--max", str(lastRun),
               "--output", filteredJson,
               os.path.join(jsonPath, jsonfile)]
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))
        for era in eras:
            multicrabWorkflowsTools._addToDictList(eraJsons, era, filteredJson)

    print "Merging run/lumi JSON files according to era"
    eraFinalJsons = {}
    for era, jsonFiles in eraJsons.iteritems():
        mergedJson = "Cert_%s.txt" % era
        cmd = ["mergeJSON.py", "--output", mergedJson] + jsonFiles
        ret = subprocess.call(cmd)
        if ret != 0:
            raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))
        eraFinalJsons[era] = mergedJson

    print "Running pileupCalc.py"
    outputFiles = []
    for era in processEras:
        jsonFile = eraFinalJsons[era]
        print "Processing era", era
        for scenario, xsecValue in [
            ("", minBiasXsec),
            ("up", int(minBiasXsec*1.05)),
            ("down", int(minBiasXsec*0.95)),
            ]:

            print "  Processing systematics scenario", {"": "Nominal"}.get(scenario, scenario)

            rootFile = outputFileName+era+scenario+".root"
            cmd = ["pileupCalc.py", "-i", jsonFile, "--inputLumiJSON", eraPUJson[era],
                   "--minBiasXsec", str(xsecValue)] + options
            cmd.append(rootFile)
            ret = subprocess.call(cmd)
            if ret != 0:
                raise Exception("Command '%s' failed with exit code %d" % (" ".join(cmd), ret))

            outputFiles.append(rootFile)

            # Put some metadata inside the ROOT file
            f = ROOT.TFile.Open(rootFile, "UPDATE")
            f.cd()
            tmp = ROOT.TNamed("pileupCalc", " ".join(cmd))
            tmp.Write()
            tmp = ROOT.TNamed("originalJsonFiles", " ".join(eraJsons[era]))
            tmp.Write()
            f.Close()

            print "  Done"
        print "Done"

    print
    print "Created data PU distributions to files"
    print "\n".join(outputFiles)


if __name__ == "__main__":
    main()
