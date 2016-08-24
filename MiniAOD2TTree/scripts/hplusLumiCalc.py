#!/usr/bin/env python

import os
import re
import sys
import glob
import subprocess
import json
from optparse import OptionParser
import ROOT
from HiggsAnalysis.NtupleAnalysis.tools.aux import execute

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

# lumiCalc.py usage taken from
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc

# PileUp calc according to https://indico.cern.ch/event/459797/contribution/3/attachments/1181542/1711291/PPD_PileUp.pdf
PileUpJSON = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt"

dataVersion_re = re.compile("dataVersion=(?P<dataVersion>[^: ]+)")
pu_re = re.compile("\|\s+\S+\s+\|\s+\S+\s+\|\s+.*\s+\|\s+.*\s+\|\s+\S+\s+\|\s+\S+\s+\|\s+(?P<lumi>\d+(\.\d*)?|\.\d+)\s+\|\s+(?P<pu>\d+(\.\d*)?|\.\d+)\s+\|\s+\S+\s+\|")

def isMCTask(taskdir):
    crabCfg = "crabConfig_"+taskdir+".py"
    if not os.path.exists(crabCfg):
        print "crab.cfg at %s doesn't exist, assuming task is MC" % crabCfg
        return True

    f = open(crabCfg)
    isData = False
    for line in f:
        if "pyCfgParams" in line:
            m = dataVersion_re.search(line)
            if not m:
                print "Unable to find dataVersion, assuming task %s is MC" % taskdir
                return True
            if "data" in m.group("dataVersion"):
                isData = True
            break
    f.close()
    return not isData

def isEmpty(taskdir):
    path = os.path.join(taskdir, "results")
    files = execute("ls %s"%path)
    return len(files)==0

# Convert luminosity to pb^-1
def convertLumi(lumi, unit):
    if unit == "ub":
        return lumi/1e6
    elif unit == "nb":
        return lumi/1e3
    elif unit == "pb":
        return lumi
    elif unit == "fb":
        return lumi*1e3
    else:
        raise Exception("Unsupported luminosity unit %s"%unit)

def main(opts, args):
    cell = "\|\s+(?P<%s>\S+)\s+"

#    lumi_re = re.compile((cell % "deliveredls")+
#                         (cell % "delivered")+
#                         (cell % "selectedls")+
#                         (cell % "recorded")+"\|")
    #lumi_re = re.compile("\|\s(?P<recorded>\S+)\s")
    lumi_re = re.compile("\|\s+(?P<recorded>\d+\.*\d*)\s+\|\s*$")
#Summary:  
#+-------+------+------+------+-------------------+------------------+
#| nfill | nrun | nls  | ncms | totdelivered(/pb) | totrecorded(/pb) |
#+-------+------+------+------+-------------------+------------------+
#|   1   |  1   | 1585 | 1585 |       25.515      |      25.028      |
#+-------+------+------+------+-------------------+------------------+
    unit_re = re.compile("totrecorded\(/(?P<unit>.*)\)")

    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    files = []
    # only if no explicit files, or some directories explicitly given
    if len(opts.files) == 0 or len(opts.dirs) > 0:
        crabdirs = multicrab.getTaskDirectories(opts)
        for d in crabdirs:
            if isMCTask(d):
                print "  Ignoring task directory '%s', it looks like MC" % d
                continue
            if isEmpty(d):
                print "  Ignoring task directory '%s', it looks empty" % d
                continue
    
            if opts.report:
                multicrab.checkCrabInPath()
                cmd = ["crab", "report", d]
                if opts.verbose:
                    print " ".join(cmd)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    print "Call to 'crab -report -d %s' failed with return value %d" % (d, ret)
                    print output
                    return 1
                if opts.verbose:
                    print output
        
            files.append((d, os.path.join(d, "results", "processedLumis.json")))
    files.extend([(None, f) for f in opts.files])
    
    data = {}
    for task, jsonfile in files:
        lumicalc = opts.lumicalc

        #print
        #print "================================================================================"
        #print "Dataset %s:" % d
#        if lumicalc == "lumiCalc1":
#            cmd = ["lumiCalc.py", "-i", jsonfile, "--with-correction", "--nowarning", "overview", "-b", "stable"]
#        if lumicalc == "lumiCalc2":
#            cmd = ["lumiCalc2.py", "-i", jsonfile, "--nowarning", "overview", "-b", "stable"]
#        if lumicalc == "pixelLumiCalc":
#            cmd = ["pixelLumiCalc.py", "-i", jsonfile, "--nowarning", "overview"]
        #cmd = ["lumiCalc.py", "-c", "frontier://LumiCalc/CMS_LUMI_PROD", "-r", "132440", "--nowarning", "overview"]
        #ret = subprocess.call(cmd)

	# brilcalc lumi -u /pb -i JSON-file
        home = os.environ['HOME']
        path = os.path.join(home,".local/bin")
        exe  = os.path.join(path,"brilcalc")
        if not os.path.exists(exe):
            print " brilcalc not found, have you installed it?"
            print " http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html"
            sys.exit()

	cmd = [exe,"lumi","--byls", "-u/pb","-i", jsonfile]
        if opts.verbose:
            print " ".join(cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        ret = p.returncode
        if ret != 0:
            print "Call to",cmd[0],"failed with return value %d with command" % ret
            print " ".join(cmd)
            print output
            return 1
        if opts.verbose:
            print output


        lines = output.split("\n")
        lumi = -1.0
        unit = None
        for line in lines:
            m = unit_re.search(line)
            if m:
                unit = m.group("unit")
#                break

            m = lumi_re.search(line)
            if m:
                lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1

        if unit == None:
            raise Exception("Didn't find unit information from lumiCalc output, command was %s" % " ".join(cmd))
        lumi = convertLumi(lumi, unit)

        # PileUp
        fOUT = os.path.join(task, "results", "PileUp.root")
        minBiasXsec = 63000
#        pucmd = ["pileupCalc.py","-i",jsonfile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","80000","--maxPileupBin","50","--numPileupBins","50",fOUT] # 2015 xsec 80000
#        pucmd = ["pileupCalc.py","-i",jsonfile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","63000","--maxPileupBin","50","--numPileupBins","50",fOUT] # 2016 xsec 63000
        pucmd = ["pileupCalc.py","-i",jsonfile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","%s"%minBiasXsec,"--maxPileupBin","50","--numPileupBins","50",fOUT]

        pu = subprocess.Popen(pucmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        puoutput = pu.communicate()[0]
        puret = pu.returncode
        if puret != 0:
            print "Call to",pucmd[0],"failed with return value %d with command" % puret
            print " ".join(pucmd)
            print puoutput
            return puret

        if task == None:
            print "File %s recorded luminosity %f pb^-1" % (jsonfile, lumi)
        else:
            print "Task %s recorded luminosity %f pb^-1" % (task, lumi)
            data[task] = lumi

        # Save the json file after each data task in case of future errors
        if len(data) > 0:
            f = open(opts.output, "wb")
            json.dump(data, f, sort_keys=True, indent=2)
            f.close()

        # https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
        # change the --minBiasXsec value in the pileupCalc.py command by +/-5% around the chosen central value.
	puUncert = 0.05

	minBiasXsec = minBiasXsec*(1+puUncert)
	pucmd = ["pileupCalc.py","-i",jsonfile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","%s"%minBiasXsec,"--maxPileupBin","50","--numPileupBins","50",fOUT.replace(".root","_up.root"),"--pileupHistName","pileup_up"]
        pu = subprocess.Popen(pucmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	puoutput = pu.communicate()[0]

        minBiasXsec = minBiasXsec*(1-puUncert)
        pucmd = ["pileupCalc.py","-i",jsonfile,"--inputLumiJSON",PileUpJSON,"--calcMode","true","--minBiasXsec","%s"%minBiasXsec,"--maxPileupBin","50","--numPileupBins","50",fOUT.replace(".root","_down.root"),"--pileupHistName","pileup_down"]
        pu = subprocess.Popen(pucmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        puoutput = pu.communicate()[0]

	fPU = ROOT.TFile.Open(fOUT,"UPDATE")
	fPUup = ROOT.TFile.Open(fOUT.replace(".root","_up.root"),"r")
	h_pu = fPUup.Get("pileup_up")
	fPU.cd()
	h_pu.Write()
	fPUup.Close()

        fPUdown = ROOT.TFile.Open(fOUT.replace(".root","_down.root"),"r")                                                                                                                                                                                               
        h_pu = fPUdown.Get("pileup_down")                                                                                                                                                                                                                           
        fPU.cd()                                                                                                                                                                                                                                                
        h_pu.Write()                                                                                                                                                                                                                                            
        fPUdown.Close()

	fPU.Close()

    if len(data) > 0:
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="JSON files to calculate the luminosity for (this or -d is required)")
    parser.add_option("--output", "-o", dest="output", type="string", default="lumi.json",
                      help="Output file to write the dataset integrated luminosities")
    parser.add_option("--truncate", dest="truncate", default=False, action="store_true",
                      help="Truncate the output file before writing")
    parser.add_option("--noreport", dest="report", action="store_false", default=True,
                      help="Do not run 'crab -report', i.e. you guarantee that the processedLumis.json contains already all jobs.")
    parser.add_option("--verbose", dest="verbose", action="store_true", default=False,
                      help="Print outputs of the commands which are executed")
    parser.add_option("--lumiCalc1", dest="lumicalc", action="store_const", const="lumiCalc1",
                      help="Use lumiCalc.py instead of lumiCalc2.py")
    parser.add_option("--lumiCalc2", dest="lumicalc", action="store_const", const="lumiCalc2",
                      help="Use lumiCalc2.py (default is to use pixelLumiCalc.py)")
    parser.add_option("--pixelLumiCalc", dest="lumicalc", action="store_const", const="pixelLumiCalc",
                      help="Use pixelLumiCalc.py instead of lumiCalc2.py (default)")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    
    if opts.lumicalc == None:
        opts.lumicalc = "brilcalc"
    print "Calculating luminosity with %s" % opts.lumicalc
    print "Calculating pileup with pileupCalc"

    sys.exit(main(opts, args))
