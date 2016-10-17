#!/usr/bin/env python
'''
Description:
Once all the jobs have been successfully retrieved from a multicrab job two scripts must then be run:
1) hplusLumiCalc.py:
Calculates luminosity with LumiCalc and the pile-up with pileupCalc for collision dataset samples. There
is no need to run this if only MC samples were processed. 

2) hplusMergeHistograms.py:
Merges ROOT files into one (or more) files. It also reads TopPt.root and adds a "top-pt-correction-weigh" histogram in miniaod2tree.root files. 
The maximum allowable size for a single ROOT file is limited to 2 GB (but can be overwritten).


Usage: (from inside a multicrab_AnalysisType_vXYZ_TimeStamp directory)
hplusLumicalc.py


Comments:
brilcalc usage taken from
https://twiki.cern.ch/twiki/bin/view/CMS/CertificationTools#Lumi_calculation

PileUp calc according to
https://indico.cern.ch/event/459797/contribution/3/attachments/1181542/1711291/PPD_PileUp.pdf


Useful Links:
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
'''

#================================================================================================
# Import Modules
#================================================================================================
import os
import re
import sys
import glob
import subprocess
import json
from optparse import OptionParser
from collections import OrderedDict
import ROOT
from HiggsAnalysis.NtupleAnalysis.tools.aux import execute

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

#================================================================================================
# Global Definitions
#================================================================================================
PBARLENGTH  = 10

# JSON files
NormTagJSON = "/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json"
PileUpJSON  = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt"

# Regular Expression
dataVersion_re = re.compile("dataVersion=(?P<dataVersion>[^: ]+)")
pu_re = re.compile("\|\s+\S+\s+\|\s+\S+\s+\|\s+.*\s+\|\s+.*\s+\|\s+\S+\s+\|\s+\S+\s+\|\s+(?P<lumi>\d+(\.\d*)?|\.\d+)\s+\|\s+(?P<pu>\d+(\.\d*)?|\.\d+)\s+\|\s+\S+\s+\|")


#================================================================================================
# Function Definition
#================================================================================================
def FinishProgressBar():
    Verbose("FinishProgressBar()")
    sys.stdout.write('\n')
    return


def PrintProgressBar(taskName, iteration, total, suffix = ""):
    '''
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    barLength   - Optional  : character length of bar (Int)
    '''
    Verbose("PrintProgressBar()")

    iteration      += 1 # since what is passed is the index of the file (starts from zero)
    prefix          = "\t" + taskName
    decimals        = 1
    barLength       = PBARLENGTH
    txtSize         = 60
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '=' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s: |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    return


def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)
    
    keystroke = raw_input("\t" +  msg + " (y/n): ")
    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)


def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=False):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def GetRegularExpression(arg):
    Verbose("GetRegularExpression()", True)
    if isinstance(arg, basestring):
        arg = [arg]
    return [re.compile(a) for a in arg]


def GetIncludeExcludeDatasets(datasets, opts):
    '''
    Does nothing by default, unless the user specifies a dataset to include (--includeTasks <datasetNames>) or
    to exclude (--excludeTasks <datasetNames>) when executing the script. This function filters for the inlcude/exclude
    datasets and returns the lists of datasets and baseNames to be used further in the program.
    '''
    Verbose("GetIncludeExcludeDatasets()", True)

    # Initialise lists
    newDatasets = []
 
    # Include datasets
    if opts.includeTasks != "":
        tmp = []
        include = GetRegularExpression(opts.includeTasks)

        Verbose("Will include the following tasks (using re): %s" % (opts.includeTasks) )
        # For-loop: All datasets/tasks
        for d in datasets:
            task  = d #GetBasename(d)
            found = False

            # For-loop: All datasets to be included
            for i_re in include:
                if i_re.search(task):
                    found = True
                    break
            if found:
                newDatasets.append(d)
        return newDatasets

    return datasets


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
    Verbose("isEmpty()", True)
    path  = os.path.join(taskdir, "results")
    files = execute("ls %s"%path)
    return len(files)==0


def convertLumi(lumi, unit):
    '''
    Convert luminosity to pb^-1
    '''
    Verbose("convertLumi()")
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


def GetCrabDirectories(opts):
    '''
    Return an alphabetically sorted list of datasets found under
    the multicrab dir used (opts.dirName)
    '''
    Verbose("GetCrabDirectories()", True)

    crabdirs = multicrab.getTaskDirectories(opts)
    crabdirs = filter(lambda x: "multicrab_" not in x, crabdirs) # Remove "multicrab_" directory from list 
    crabdirs = filter(lambda x: "2016B_" not in x, crabdirs) #tmp fixme iro
    crabdirs = filter(lambda x: "2016C_" not in x, crabdirs) #tmp fixme iro
    crabdirs = filter(lambda x: "2016D_" not in x, crabdirs) #tmp fixme iro

    crabdirs = GetIncludeExcludeDatasets(crabdirs, opts)
    # Return list (alphabetically ordered)
    return sorted(crabdirs)


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)

    Verbose("Executing command: %s" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.communicate()[0]
    ret    = p.returncode

    #stdin  = p.stdout
    #stdout = p.stdout
    #ret    = []
    #for line in stdout:
    #    ret.append(line.replace("\n", ""))
    #
    #stdout.close()
    return output, ret


def main(opts, args):
    '''
    Calculates luminosity with LumiCalc and the pile-up with pileupCalc for collision dataset samples. 

    Summary:  
    +-------+------+------+------+-------------------+------------------+
    | nfill | nrun | nls  | ncms | totdelivered(/pb) | totrecorded(/pb) |
    +-------+------+------+------+-------------------+------------------+
    |   1   |  1   | 1585 | 1585 |       25.515      |      25.028      |
    +-------+------+------+------+-------------------+------------------+
    '''
    Verbose("main()", True)
    
    cell = "\|\s+(?P<%s>\S+)\s+"
    lumi_re = re.compile("\|\s+(?P<recorded>\d+\.*\d*)\s+\|\s*$")
    unit_re = re.compile("totrecorded\(/(?P<unit>.*)\)") 

    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    files = []
    # only if no explicit files, or some directories explicitly given
    if len(opts.files) == 0 or len(opts.dirs) > 0:

        crabdirs = GetCrabDirectories(opts)
        
        # For-loop: All tasks
        for index, d in enumerate(crabdirs):

            if isMCTask(d):
                Print("%s, ignoring, it looks like MC" % d)
                continue

            if isEmpty(d):
                Print("%s, ignoring, it looks empty" % d)
                continue
    
            if opts.report:
                multicrab.checkCrabInPath()
                cmd = ["crab", "report", d]
                Verbose(" ".join(cmd) )
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = p.communicate()[0]
                ret = p.returncode
                if ret != 0:
                    print "Call to 'crab -report -d %s' failed with return value %d" % (d, ret)
                    print output
                    return 1
                Verbose(output)

            # Append tuple (task, json) to files list
            files.append((d, os.path.join(d, "results", "processedLumis.json")))

            # Update progress bar
            PrintProgressBar(d + ", Crab", index, len(crabdirs) )

    # Flush stdout
    FinishProgressBar()

    # Extend the list
    files.extend([(None, f) for f in opts.files])

    data  = {}
    index = -1
    # For-loop: All json files
    for task, jsonfile in files:
        index += 1
        
        Verbose("%s, %s" % (task, os.path.basename(jsonfile) ) )
        lumicalc = opts.lumicalc

	# brilcalc lumi -u /pb -i JSON-file
        home = os.environ['HOME']
        path = os.path.join(home, ".local/bin")
        exe  = os.path.join(path, "brilcalc")

        # Ensure brilcal executable exists
        if not os.path.exists(exe):
            Print("brilcalc not found, have you installed it?", True)
            Print("http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html")
            sys.exit()
        else:
            pass

        # Run the steps to get the Pileup histo
        PrintProgressBar(task + ", Lumi", index, len(files), "[" + os.path.basename(jsonfile) + "]")
        cmd = [exe,"lumi","-b", "STABLE BEAMS", "--normtag", NormTagJSON, "-u /pb", "-i", jsonfile]
        output, ret = Execute(cmd) #iro
        #Verbose(" ".join(cmd) )
        #p      = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #output = p.communicate()[0]
        #ret    = p.returncode


        # If return value is not zero print failure
        if ret != 0:
            Print("Call to %s failed with return value %d with command" % (cmd[0], ret ), True)
            Print(" ".join(cmd) )
            Print(output)
            return 1
        Verbose(output)

        lines = output.split("\n")
        lumi = -1.0
        unit = None

        #For-loop: All lines in "crab report <task>" output
        for line in lines:
            m = unit_re.search(line)
            if m:
                unit = m.group("unit")
            
            m = lumi_re.search(line)
            if m:
                lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1

        if unit == None:
            raise Exception("Didn't find unit information from lumiCalc output, command was %s" % " ".join(cmd))
        lumi = convertLumi(lumi, unit)

        print

        # PileUp
        fOUT = os.path.join(task, "results", "PileUp.root")
        minBiasXsec = 63000
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

        # Update progress bar
        #PrintProgressBar(task + ", Lumi", index, len(files) ) #iro
        
    # Flush stdout
    FinishProgressBar()

    if len(data) > 0:
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()

    return 0

if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html

    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default Values
    FILES    = []
    OUTPUT   = "lumi.json"
    TRUNCATE = False
    REPORT   = True
    VERBOSE  = False

    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")

    multicrab.addOptions(parser)

    parser.add_option("-f", dest="files", type="string", action="append", default=FILES,
                      help="JSON files to calculate the luminosity for (this or -d is required) [default: %s]" % (FILES) )

    parser.add_option("--output", "-o", dest="output", type="string", default=OUTPUT,
                      help="Output file to write the dataset integrated luminosities [default: %s]" % (OUTPUT) )

    parser.add_option("--truncate", dest="truncate", default=TRUNCATE, action="store_true",
                      help="Truncate the output file before writing [default: %s]" % (TRUNCATE) )

    parser.add_option("--noreport", dest="report", action="store_false", default=REPORT,
                      help="Do not run 'crab report', i.e. you guarantee that the processedLumis.json contains already all jobs. [default: %s]" % (REPORT) ) 

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print outputs of the commands which are executed [default: %s]" % (VERBOSE) )

    parser.add_option("--lumiCalc1", dest="lumicalc", action="store_const", const="lumiCalc1",
                      help="Use lumiCalc.py instead of lumiCalc2.py")

    parser.add_option("--lumiCalc2", dest="lumicalc", action="store_const", const="lumiCalc2",
                      help="Use lumiCalc2.py (default is to use pixelLumiCalc.py)")

    parser.add_option("--pixelLumiCalc", dest="lumicalc", action="store_const", const="pixelLumiCalc",
                      help="Use pixelLumiCalc.py instead of lumiCalc2.py (default)")

    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string", 
                      help="Only perform action for this dataset(s) [default: '']")

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    
    if opts.lumicalc == None:
        opts.lumicalc = "brilcalc"

    Print("Calculating luminosity with %s" % opts.lumicalc, True)
    Print("Calculating pileup with pileupCalc")

    sys.exit(main(opts, args))
