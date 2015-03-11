#!/usr/bin/env python

# Obtain files from /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/
# as instructed in https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData

import os
import json
import subprocess

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi as certifiedLumi
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux


minBiasXsec = 69400
options = [
    "--calcMode",      "true",
    "--maxPileupBin",  "60",
#    "--maxPileupBin",  "80",
    "--numPileupBins", "1200"
]
outputFileName = "PileupHistogramData"

jsonPath = ".."
runsJson = [
    (["2012A"], 190456, 193621, certifiedLumi.files["22Jan2013ReReco"]),
    (["2012B"], 193834, 196531, certifiedLumi.files["22Jan2013ReReco"]),
    (["2012C"], 198022, 203742, certifiedLumi.files["22Jan2013ReReco"]),
    (["2012D"], 203777, 208686, certifiedLumi.files["22Jan2013ReReco"]),
    ]
for tpl in runsJson:
    if tpl[0][0] in ["2012A", "2012B"]:
        tpl[0].append("2012AB")
        tpl[0].append("2012ABC")
        tpl[0].append("2012ABCD")
    elif tpl[0][0] in ["2012C"]:
        tpl[0].append("2012ABC")
        tpl[0].append("2012ABCD")
    elif tpl[0][0] in ["2012CD"]:
        tpl[0].append("2012ABCD")
eraPUJson = {
    "2012A": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
    "2012B": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
    "2012C": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
    "2012D": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",

    "2012AB": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
    "2012ABC": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
    "2012ABCD": "pileup_JSON_DCSONLY_190389-208686_All_2012_pixelcorr.txt",
}

processEras = [
    "2012A",
    "2012B",
    "2012C",
    "2012D",
    "2012AB",
    "2012ABC",
    "2012ABCD",
]

def main():
    # Code to mix HF and pixel JSON files (in case necessary in the future)
    # if not os.path.exists(eraPUJson["2012ABC"]):
    #     print "Creating PU json", eraPUJson["2012ABC"]

    #     f = open(eraPUJson["2012A"])
    #     pixelPU = json.load(f)
    #     f.close()

    #     f = open(eraPUJson["2012C"])
    #     hfPU = json.load(f)
    #     f.close()

    #     for run in pixelPU.keys():
    #         if int(run) > 196531:
    #             del pixelPU[run]

    #     for run in hfPU.keys():
    #         if int(run) < 198022:
    #             del hfPU[run]

    #     pixelPU.update(hfPU)

    #     f = open(eraPUJson["2012ABC"], "w")
    #     json.dump(pixelPU, f, sort_keys=True)
    #     f.close()

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
            aux.addToDictList(eraJsons, era, filteredJson)

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
