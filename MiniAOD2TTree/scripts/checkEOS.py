#!/usr/bin/env python
'''
Usage:
./checkEOS.py
or
./checkEOS.py --skipVerify --cleanAll
or
./checkEOS.py --skipVerify --verbose --cleanAll

Description:
This script is used to check quota and delete files/directories on EOS.

Links:
https://cern.service-now.com/service-portal/article.do?n=KB0001998
https://twiki.cern.ch/twiki/bin/view/EOS/UserHowTo
'''


#================================================================================================
# Import Modules
#================================================================================================
import os
import sys
import subprocess
import socket

from optparse import OptionParser

#================================================================================================
# Function Definitions
#================================================================================================
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return

    if printHeader:
        print "=== checkEOS.py:"
    print "\t", msg
    return


def Print(msg, printHeader=False):
    if printHeader:
        print "=== checkEOS.py:"
    print "\t", msg
    return


def GetHost():
    return socket.gethostname()


def GetEosContentsList(opts):
    '''
    '''
    pathPrefix = "/store/user/"
    userName   = os.getenv("USER")
    eosPath    = os.path.join(pathPrefix, userName, opts.dir)

    # Construct & Execute command
    if "lxplus" in GetHost():
        cmd = "eos ls"
    elif "cmslpc" in GetHost():
        cmd = "eosls"
    else:
        raise Exception("Unsupported hostname \"%s\"." % (GetHost()) )
    csh_cmd = cmd + " " + eosPath
    Verbose(csh_cmd, True)

    # Execute shell command
    p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)

    # Use Popen with the communicate() method when you need pipes
    cmd_out, cmd_err = p.communicate()

    # Convert string result to a list (of strings)
    fileList = cmd_out.split("\n")
    fileList.remove('')
    return fileList, eosPath


def GetEosQuota(opts):
    '''
    '''
    if "lxplus" in GetHost():
        csh_cmd = "eos quota | grep ^user -A1 -B2"
    elif "cmslpc" in GetHost():
        csh_cmd = "eosquota"
    else:
        raise Exception("Unsupported hostname \"%s\"." % (GetHost()) )

    Verbose(csh_cmd, True)
    p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)

    # Use Popen with the communicate() method when you need pipes
    cmd_out, cmd_err = p.communicate()
    return cmd_out, cmd_err


def DeleteEosContents(fileList, eosPath, opts):
    '''
    '''
    if len(fileList) < 1:
        Print("Nothing to delete!")
        return     

    # Define the delete command
    if "lxplus" in GetHost():
        cmd = "eos rm -r"
    elif "cmslpc" in GetHost():
        cmd = "eosrm -r"
    else:
        raise Exception("Unsupported hostname \"%s\"." % (GetHost()) )

    # Foor-loop: All files on EOS
    printHeader = True
    for f in fileList:
        # Append the path to the command to be executed
        path    = os.path.join(eosPath, f)
        csh_cmd = cmd + " " + path
        Verbose(csh_cmd, True)

        # Execute the deletion command
        if not opts.skipVerify:
            if UserConfirm(path):
                p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)
                #Print(csh_cmd, printHeader)
            else:
                pass
        else:
            p = subprocess.Popen(['/bin/csh', '-c', csh_cmd], stdout=subprocess.PIPE)
            Print(csh_cmd, printHeader)

        # Disable header
        printHeader = False
    return


def UserConfirm(fileOrDir):
    '''
    Prompts user for keystroke. Returns True if keystroke is "y", False otherwise
    '''
    message   = "=== checkEOS.py:\n\tDelete \"%s\" ? " % (fileOrDir)
    keystroke = raw_input(message)
    if (keystroke) == "y":
        return True
    elif (keystroke) == "n":
        return False
    else:
        UserConfirm(fileOrDir)
    return


#================================================================================================
# Main Program
#================================================================================================
def main(opts, args):
    
    # Get the list of files/dirs on EOS
    fileList, eosPath = GetEosContentsList(opts)

    # Print the files/dirs found on EOS    
    Print("Found %s items under %s:" % (len(fileList), eosPath + "/"), True)
    for f in fileList:
        Print(f, False)

    # Get the EOS quota
    quota_out, quota_err = GetEosQuota(opts)

    # If user does not was to delete the contents return
    if not opts.cleanAll:
        Print(quota_out, True)
        return
    else:
        DeleteEosContents(fileList, eosPath, opts)
        Print(quota_out, True)

    return


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

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", "--verbose"   , dest="verbose"   , default=False, action="store_true", help="Verbose mode (for debugging)")
    parser.add_option("-s", "--skipVerify", dest="skipVerify", default=False, action="store_true", help="Skip confirmation when deleting files/dirs. Used with --cleanAll")
    parser.add_option("-c", "--cleanAll"  , dest="cleanAll"  , default=False, action="store_true", help="Delete all file/dir found on EOS")
    parser.add_option("-d", "--dir"       , dest="dir"       , default="CRAB3_TransferData", action="store", help="Dir to probe in EOS (default: CRAB3_TransferData")

    (opts, args) = parser.parse_args()

    if opts.skipVerify and not opts.cleanAll:
        Print("WARNING! The option --skipVerify can only if the option --cleanAll is also enabled. EXIT", True)
        sys.exit()

    sys.exit( main(opts, args) )
