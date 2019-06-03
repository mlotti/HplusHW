#!/usr/bin/env python
'''
DESCRIPTION:
Script to combine datacards of two or more analyses into one


INSTRUCTIONS:


USAGE:
./dcardCombineAnalyses.py [options]


EXAMPLES:


LAST USED:
./dcardCombineAnalyses.py -d datacards_Hplus2tb_13TeV_TopMassLE400_BDT0p40_Binning4Eta5Pt_BinScheme18_Syst_01Aug2018_autoMCStats,datacards_HIG-18-014_Final_Sep2018 -v


'''

#================================================================================================
# Import modules
#================================================================================================
import os
import re
import time
import getpass
import sys
import datetime
import string
from optparse import OptionParser

import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================
# Variable definition
#================================================================================================
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
ls = ShellStyles.HighlightStyle()
es = ShellStyles.ErrorStyle()
cs = ShellStyles.CaptionStyle()

#================================================================================================
# Function definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def IntersectOfSets(myLists): 
     
    # Converting the arrays into sets 
    mySets = []
    for l in myLists:
        mySets.append(set(l))
      
    # Calculates intersection of all sets 
    for i, s in enumerate(mySets, 1):
        if i==len(mySets):
            break
        mySet = mySets[i-1].intersection(mySets[i])
    print mySet
      
    # Converts resulting set to a list & return
    final_list = list(mySet) 
    return final_list

def main(opts):

    # Make a new directory for combined datacards
    Verbose("Creating new datacards directory %s" % (hs + opts.saveDir + ns), True)
    os.system("mkdir %s" % opts.saveDir)

    # Declarations
    alphabet    =  list(string.ascii_uppercase) #list(string.ascii_lowercase)
    mass_points = {}
    files       = {}
    formats     = ["txt", "root"]
    
    # For-loop: All file formats
    for i, d in enumerate(opts.dirs, 0):

        # Variables
        mass_points_tmp = [] 
        files_tmp       = []

        # Convert number to alphabet letter
        letter  = alphabet[i]
        aux.PrintFlushed("%sProcessing analysis \"%s\" (%d/%d)%s" % (hs, letter, i+1, len(opts.dirs), ns), i==0)

        # For-loop: All file formats
        for j, ext in enumerate(formats, 1):
            cmd = "cp %s/*.%s %s" % (opts.dirs[i], ext, opts.saveDir)
            Verbose("Copying all %s files to new directory %s" % (ls + ext + ns, hs + opts.saveDir + ns), i==0) #fixme
            os.system(cmd)

        # For-loop: All files 
        for k, fName in enumerate(os.listdir(d), 1):
            ext     = fName.split(".")[-1] 
            if ext not in formats:
                Verbose("Skipping file (or dir) %s" % (ls + fName + ns), False)
                continue

            # Rename the files
            oldPath = os.path.join(opts.saveDir, fName)            
            # newPath = os.path.join(opts.saveDir, fName.replace("." + ext, "_%s.%s" % (letter, ext) ) )
            newPath = os.path.join(opts.saveDir, fName.replace("." + ext, "_%s.%s" % (letter, ext) ) )
            mass    = int(filter(str.isdigit, os.path.basename(newPath)))
            Verbose("Renaming file: %s -> %s" % (ls + oldPath + ns, hs + newPath + ns), k==1)
            os.rename(oldPath, newPath)

            # Store all files copied for this analysis
            files_tmp.append(newPath) #path.basename(newPath)

            if ext == "txt":
                mass_points_tmp.append(mass)

        # Store files/mass-point list to dictionary
        files[letter]       = files_tmp
        mass_points[letter] = mass_points_tmp


    # Update references to root files in txt datacards
    firstline = "" 

    # For-loop: All analyses
    for i, key in enumerate(files.keys(), 1):
        # print "\nfiles[%s] = %s" % ( key, files[key])
        
        # For-loop: All files for given analysis
        for j, fileName in enumerate(files[key], 1):
            
            # Only consider datacards (.txt files)
            if ".txt" not in fileName:
                continue

            with open(fileName, "r+") as f:
                firstline = f.readline()
                f.seek(0)
                s = f.read()
                s = s.replace(".root", "_%s.root" % letter)#.replace("CMS_Hptn_mu_RF_Hptn_heavy","CMS_Hptn_mu_RF_Hptn      ")
                f.seek(0)
                f.write(s)
                f.truncate()
                continue

    # Run combineCards.py for mass points available in all categories considered
    lumi = re.findall(r'luminosity=\d+\.\d+', firstline)

    # Make a list of mass-point lists
    massList = []
    for l in mass_points.values():
        massList.append(l)

    # For-loop: All (common) mass points
    massPoints = IntersectOfSets(massList)
    for i, m in enumerate(massPoints, 1):
        aux.PrintFlushed("Creating datacard for mass point %d (%d/%d)" % (m, i, len(massPoints)), i==1)

        # Definitions
        dcard = "combine_datacard_hplushadronic_m%d" % m
        text = ""
        cmd  = "combineCards.py"
        
        # For-loop: All analyses
        for letter in mass_points.keys():
            datacard = ""
            for f in files[letter]:
                if ".txt" not in f:
                    continue

                if "m%s" % m in f or "mH%s" % m in f:
                    datacard = f
                    break
                else:
                    pass
            cmd += " taunuhadr_%s=%s" % (letter, datacard)
            text += "Description: Combine datacard (combined from two categories) mass=%d, %s 1/pb\n"%(m, lumi) #[0])

        # Finalise commands and datacards
        cmd += " > %s.txt" % ( os.path.join(opts.saveDir,dcard) )
        aux.PrintFlushed("%s" % (ls + cmd + ns), i==1)
        os.system(cmd)
        sys.exit()
        # Add mass, lumi and other information to the new datacard as first line
        text += "Date: %s\n" % time.ctime()
        filePath = os.path.join( opts.saveDir, dcard + ".txt") # dcard + ".txt"

        # with file(filePath, 'r') as old: data = old.read()
        # data = data[data.find('\n')+1:-1] # remove the default description by combineCards.py
        # 
        # with file(filePath, 'w') as modified: modified.write(text+data)

    # Inform user
    print
    Print("New datacards saved to directory %s" % (ss + opts.saveDir + ns), True)

    # remove original, category-specific datacards
    for filename in os.listdir("."):
        if "a.txt" in filename or "b.txt" in filename or "c.txt" in filename:
            os.system("rm %s"%filename)

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

    # Default Values
    VERBOSE     = False
    SAVEDIR     = None #"/afs/cern.ch/user/%s/%s/public/html/Datacards" % (getpass.getuser()[0], getpass.getuser())
    POSTFIX     = None
    DIRS        = None

    parser = OptionParser(usage="Usage: %prog [options]")
    
    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    #parser.add_option("-a", "--a", action="store", type="string", dest="dir1",
    #                  help="Datacard directories for analysises")
    
    #parser.add_option("-b", "--b", action="store", type="string", dest="dir2",
    #                  help="datacard directory for category B")

    #parser.add_option("-c", "--c", action="store", type="string", dest="dir3",
    #                  help="datacard directory for category C", default = None)

    parser.add_option("-d", "--dirs", dest="dirs", action="store", 
                      help="Path to the multicrab directories for input")

    parser.add_option("--postfix", dest="postfix", type="string", default = POSTFIX,
                      help="Postfix for output name [default: %s]" % (POSTFIX) )

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory for saving output [default: %s]" % SAVEDIR)

    (opts, args) = parser.parse_args()


    # Sanity checks
    if opts.saveDir == None:
        opts.date = datetime.date.today().strftime("%d%h%Y")      # datetime.date.today().strftime('%y%m%d') 
        opts.time = datetime.datetime.now().strftime('%Hh%Mm%Ss') # datetime.datetime.now().strftime('%H%M%S')
        if opts.postfix != None:
            opts.saveDir = "datacards_combine_multianalysis_%s_%s_%s" % (opts.postfix, opts.date, opts.time)
        else:
            opts.saveDir = "datacards_combine_multianalysis_%s_%s" % (opts.date, opts.time)

    if isinstance(opts.dirs, str):
        pass
    else:
        msg =  "Datacard directories must be provided as a comma-separated string"
        raise Exception(es + msg + ns)

    if "," in opts.dirs:
        opts.dirs = opts.dirs.split(",")    
        aux.Print("Will use the following datacard %d directories:" % (len(opts.dirs)), True)
        for i, d in enumerate(opts.dirs, 1):
            bIsDir = os.path.isdir(d)
            if not bIsDir:
                msg = "The provided path \"%s\" is not a directory!" % d
                raise Exception(es + msg + ns)
            else:
                msg = "%d) %s" % (i, hs + d + ns)
                Print(msg, False)
    else:
        msg = "The datacards directories must be provided in a single argument seperated with a comma (\",\")"
        raise Exception(es + msg + ns)
        
    main(opts)
