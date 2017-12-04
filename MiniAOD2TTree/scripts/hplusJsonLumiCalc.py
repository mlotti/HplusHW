#!/usr/bin/env python
'''
PREREQUISITES:
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

DESCRIPTION:
Calculate the luminosity of a JSON file using the official brilcalc tool. 
It is important to use the correct normtag with brilcalc which can be found here
in https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM. The normtag 
contains the latest official calibrations for the appropriate run period. 
In general, the script runs a command of the form:
brilcalc lumi --normtag [normtag file] -i [your json]

BRIL tools analyse data in the database server at CERN which is closed to the outside.
Therefore the most convienient way is to run the toolkit on hosts (private or public) at CERN. 
If you must use the software installed outside the CERN intranet, a ssh tunnel to the database 
server at CERN has to be established first. Since the tunneling procedure requires a valid CERN
computer account, a complete unregistered person will not be able to access the BRIL data in 
any case. 
The following instruction assumes the easiest setup: 
you have two open sessions on the SAME off-site host, e.g. cmslpc32.fnal.gov, one for the ssh tunnel
and another for execution. It is also assumed that all the software are installed and the $PATH
variable set correctly on the execution shell.

USAGE (LXPLUS):
hplusJsonLumicalc.py <json_file>

USAGE (LPC (r outside LXPLUS in general):
open two terminals
for both terminals, ssh to the same machine (e.g. ssh -YK aattikis@cmslpc37.fnal.gov)
setup CMSSW and CRAB environments
terminal 1: (ssh tunneling session)
ssh -N -L 10121:itrac5212-v.cern.ch:10121 <username>@lxplus.cern.ch

terminal 2 (while terminal 1 is open):
hplusJsonLumiCalc.py <json_file>

COMMENTS:
brilcalc usage taken from
https://twiki.cern.ch/twiki/bin/view/CMS/CertificationTools#Lumi_calculation
PileUp calc according to
https://indico.cern.ch/event/459797/contribution/3/attachments/1181542/1711291/PPD_PileUp.pdf

LINKS:
https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM
http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html

INSTALL BRIL:
bash
bash-4.1$ export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-3.1.1/bin:$PATH
bash-4.1$ pip uninstall brilws
bash-4.1$ pip install --install-option="--prefix=$HOME/.local" brilws
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
import getpass
import socket
from optparse import OptionParser
from collections import OrderedDict
import ROOT
from HiggsAnalysis.NtupleAnalysis.tools.aux import execute

import HiggsAnalysis.NtupleAnalysis.tools.multicrab as multicrab

#================================================================================================
# Function Definition
#================================================================================================
def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)
    Verbose("Executing command: %s" % (cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)

    stdin  = p.stdin
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))
    stdout.close()
    Verbose("Command %s returned:\n\t%s" % (cmd, "\n\t".join(ret)))
    return ret


def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question. 
    Returns true if keystroke is \"y\", false otherwise.
    '''
    Verbose("AskUser()", printHeader)
    
    fName = __file__.split("/")[-1]
    if printHeader==True:
        fullmsg = "=== " + fName
        fullmsg += "\n\t" + msg + " (y/n): "
    else:
        fullmsg = "\t" + msg + " (y/n): "

    keystroke = raw_input(fullmsg)
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


def GetLumiAndUnits(output):
    '''
    Reads output of "brilcalc" command 
    and finds and returns the lumi and units
    '''
    Verbose("GetLumiAndUnits()", True)

    # Definitions
    lumi = -1.0
    unit = None

    # Regular expressions
    unit_re = re.compile("totrecorded\(/(?P<unit>.*)\)") 
    lumi_re = re.compile("\|\s+(?P<recorded>\d+\.*\d*)\s+\|\s*$")

    Verbose("Looping over all lines out brilcalc command output")
    #For-loop: All lines in "crab report <task>" output
    for line in output:
        m = unit_re.search(line)
        if m:
            unit = m.group("unit")
            
        m = lumi_re.search(line)
        if m:
            lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1

    if unit == None:
        raise Exception("Didn't find unit information from lumiCalc output:\n\t%s" % "".join(output))
    lumi = convertLumi(lumi, unit)
    return lumi, unit

        
def CallBrilcalc(BeamStatus, CorrectionTag, LumiUnit, InputFile, printOutput=True):
    '''
    Executes brilcalc and returns the execuble exit code and the output
    in the form of a list of strings.

    The original version of the code did not work for tcsh (built for "bash" I assume)
    p      = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    ret    = p.returncode

    For more help type in the terminal:
    brilcalc lumi --help        
    '''
    Verbose("CallBrilcalc()", True)

    # brilcalc lumi -u /pb -i JSON-file
    home = os.environ['HOME']
    path = os.path.join(home, ".local/bin")
    exe  = os.path.join(path, "brilcalc")

    # Ensure brilcal executable exists
    if not os.path.exists(exe):
        Print("brilcalc not found, have you installed it?", True)
        Print("http://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html")
        sys.exit()

    # Execute the command (e.g. brilcalc lumi -b "STABLE BEAMS" --normtag opts.normTag -u /pb -i opts.jsonFile)
    cmd     = [exe, "lumi", "-b", BeamStatus, "--normtag", CorrectionTag, "-u", LumiUnit, "-i", InputFile]
    cmd_ssh = ["-c", "offsite"]
    if opts.offsite:
        cmd.extend(cmd_ssh)

    sys_cmd = " ".join(cmd) + " > %s "  % (opts.logFile)
    Print(sys_cmd, True)

    # Execute the command
    ret    = os.system(sys_cmd)
    output = [i for i in open(opts.logFile, 'r').readlines()]
    
    # If return value is not zero print failure
    if ret != 0:
        Print("Call to %s failed with return value %d with command" % (cmd[0], ret ), True)
        Print(" ".join(cmd) )
        Print(output)
        sys.exit()

    if printOutput:
        Print("Printing program execution output:", True)
        for o in output:
            print o.replace('\n', "")
    Print("Output saved in file \"%s\"" % (opts.logFile), True)
    return ret, output


def Execute(cmd):
    '''
    Executes a given command and return the output.
    '''
    Verbose("Execute()", True)

    Verbose("Executing command: %s" % (cmd))
    p = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = p.communicate()[0]
    ret    = p.returncode
    return output, ret


def PrintSummary(data, lumiUnit):
    '''
    Prints a table summarising the task and the recorded luminosity.
    Also prints the total integrated luminosity.
    '''
    Verbose("PrintSummary()", True)
    table   = []
    table.append("")
    align   = "{:<3} {:<50} {:>20} {:<7}"
    hLine   = "="*80
    header  = align.format("#", "Task", "Luminosity", "")
    data    = OrderedDict(sorted(data.items(), key=lambda t: t[0]))
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    index   = 0
    intLumi = 0
    # For-loop: All task-lumi pairs
    for task, lumi in data.items():
        index+=1
        table.append( align.format(index, task, "%.3f"%lumi, lumiUnit ) )
        intLumi+= lumi
    table.append(hLine)
    table.append( align.format("", "", "%.3f"%intLumi, lumiUnit) )
    table.append("")
    for row in table:
        Print(row)
    return


def IsSSHReady(opts):
    '''
    Ensures user confirms ssh tunnel is open
    '''
    Verbose("IsSSHReady()", True)

    if not opts.offsite:
        return
    cmd_ssh   = "ssh -N -L 10121:itrac5212-v.cern.ch:10121 <username>@lxplus.cern.ch\n\tPress "
    ssh_ready = AskUser("Script executed outside LXPLUS (--offsite enabled). Is the ssh tunneling session ready?\n\t%s" % (cmd_ssh), True)
    if not ssh_ready:
        sys.exit()
    else:
        return


def main(opts, args):
    
    cell = "\|\s+(?P<%s>\S+)\s+"

    # Ensure user has the ssh tunnel session ready (if required)
    IsSSHReady(opts)

    # if lumi.joson already exists, load
    if os.path.exists(opts.logFile):
        raise Exception("Destination file \"%s\% already exists. USe --overwrite/-o option to overwrite" % (opts.logFile) )

    # Execute the command
    ret, output =  CallBrilcalc(BeamStatus='"STABLE BEAMS"', CorrectionTag=opts.normTag, LumiUnit=opts.lumiUnit, InputFile=opts.jsonFile)
    
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
    JSONFILE      = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    NORMTAG       = "/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json"
    #NORMTAG       = "/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json"
    LUMIUNIT      = "/pb"
    LOGFILE       = "brilcalc.log"
    VERBOSE       = False
    OFFSITE       = False

    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")

    multicrab.addOptions(parser)

    parser.add_option("-j", "--jsonFile", dest="jsonFile", type="string", default=JSONFILE,
                      help="JSON file to calculate the luminosity for [default: %s]" % (JSONFILE) )

    parser.add_option("-n", "--normTag", dest="normTag", type="string", default=NORMTAG,
                      help="The \"normtag\" contains the latest official (Luminosity POG) calibrations for the appropriate run period [default: %s]" % (NORMTAG) )

    parser.add_option("-u", "--lumiUnit", dest="lumiUnit", type="string", default=LUMIUNIT,
                      help="Show luminosity in the specified unit and scale the output value accordingly [default: %s]" % (LUMIUNIT) )

    parser.add_option("-l", "--logFile", dest="logFile", type="string", default=LOGFILE,
                      help="Name of log file to write the output of program execution [default: %s]" % (LOGFILE) )

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print outputs of the commands which are executed [default: %s]" % (VERBOSE) )

    parser.add_option("--offsite", dest="offsite" , action="store_true", default=OFFSITE, 
                      help="Run bril tools as usual with connection string -c offsite. [default: %s]" % (OFFSITE) )

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)
    
    lumiUnits = ["/kb", "/b", "/mb", "/ub", "/nb", "/pb", "/fb", "/ab"]
    if opts.lumiUnit not in lumiUnits:
        Print("Must choose one of the following supported luminosity units:%s" % ("".join(lumiUnits)), True)
        sys.exit()
        

    if "lxplus" not in socket.gethostname() and not opts.offsite:
        Print("Must enable the --offsite option when working outside LXPLUS. Read docstrings. Exit", True)
        #print __doc__
        sys.exit()

    # Inform user
    sys.exit(main(opts, args))
