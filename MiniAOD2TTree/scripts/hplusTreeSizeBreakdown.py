#!/usr/bin/env python
'''
Description:
Very simple script that takes as input a ROOT file (-f or --rootFile)  with a TTree 
(-t or --treeName) and reads the size of each branch. It produces an output file (-o or 
--output) with a table breaking down the percentage of the total size occupied by each TBranch.
It also give an estimate of the size per event. 

Usage:
hplusTreeSizeBreakdown.py -f miniaod2tree.root
[creates the file "miniaod2tree_size.txt"]


Note:
A very preliminary stage of a large and more useful script!


Useful Links:
https://root.cern.ch/doc/master/classTTree.html
https://root.cern.ch/doc/master/classTBranch.html
'''

#================================================================================================
# Import Modules
#================================================================================================
import os
import sys
import numpy
import math

from optparse import OptionParser

import ROOT

#================================================================================================
# Function Definitions
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


def GetObjectByName(fileIn, objectName):
    '''
    '''
    # For-loop: Over all keys in file
    for key in fileIn.GetListOfKeys():    

        # Skip if object name is wrong
        keyName = key.GetName()
        if (keyName!= opts.treeName):
            continue
        else:
            o = fileIn.Get(keyName)
            return o
    raise Exception("Could not find object with name '%s' in input ROOT file with name '%s'." % ( objectName, fileIn.GetName() ) )


def OpenTFile(filePath, mode):
    '''
    '''
    return ROOT.TFile.Open(filePath, mode)
            

def CreateFile(filePath, fileName, fileMode, titleLines, ):
    '''
    '''
    if (filePath.endswith("/") == False):
        filePath = filePath + "/"

    # Create the file
    f = open(filePath + fileName , fileMode)

    # Write the title lines (if any)
    for l in titleLines:
        f.write(l)

    return f


def main(opts, args):

    filePath = opts.rootFile

    # For-loop: All datasets
    for dataset in datasets:

        # Open ROOT file
        Print("Opening ROOT file \"%s\"" % (filePath) )
        fileIn = OpenTFile(filePath, "READ")

        # Get the TTree    
        treeIn = GetObjectByName(fileIn, opts.treeName) #treeIn = fileIn.Get(treeName)
    
        # For-loop: All TBranches in the TTree
        treeBranches   = treeIn.GetListOfBranches()
        bName_to_bSize = {}
        bNames         = []
        bSizes         = []
        totalSize_MB   = 0
        basketSize_MB  = 0;
        nEntries       = treeIn.GetEntries()

        # For-loop: All TTree branches
        for b in treeBranches:
            totalSize_MB  += b.GetTotalSize() * 1e-06
            basketSize_MB += b.GetBasketSize() * 1e-06

        # For-loop: All TTree branches
        for b in treeBranches:

            # Get the values
            bName   = b.GetName()
            bSize   = b.GetTotalSize()
            
            # Savee the names/size
            bNames.append(bName)
            bSizes.append((bSize * 1e-06)/(totalSize_MB)*100)
            bName_to_bSize[bName] = (bSize * 1e-06)/(totalSize_MB)*100

        # Sort the two lists according to the bSizes list (descding order)
        from operator import itemgetter
        bSizes, bNames = [list(x) for x in zip(*sorted(zip(bSizes, bNames), key=itemgetter(0), reverse=True))]

        # Create a txt file
        title     = []
        hLine     = '='*90
        txtAlign  = '\n{:<65}  {:>10}  {:>5}'
        titleLine = txtAlign.format("TBranch", "Size", "Units")
        title.append(" "*30 + dataset)
        title.append("\n" + hLine)
        title.append(titleLine)
        title.append("\n" + hLine)
        fileOut = CreateFile(os.getcwd(), opts.output, "a", title)
        Print("Created output file %s" % (fileOut.name) )

        # For-loop: All dictionary keys/values
        for bName, bSize in zip(bNames, bSizes):
            bSize = bName_to_bSize[bName]
        
            # Convert to kilo-bytes before saving and Keep only two decimals
            bSize   = '%0.3f' % (bSize)
            newLine = txtAlign.format(bName, bSize, "%")

            # Write line to file
            fileOut.write(newLine)

        # Write final lines
        lastLine_1a = txtAlign.format("Total Size"         , '%0.2f' % (totalSize_MB) , "MB")
        lastLine_1b = txtAlign.format("Basket Size "       , '%0.2f' % (basketSize_MB), "MB")
        lastLine_2a = txtAlign.format("Total Size  / Event", '%0.2f' % ((totalSize_MB/nEntries)*1e+03), "kB")
        lastLine_2b = txtAlign.format("Basket Size / Event", '%0.2f' % ((basketSize_MB/nEntries)*1e+03), "kB")
        # 
        fileOut.write(lastLine_1a)
        fileOut.write(lastLine_1b)
        fileOut.write(lastLine_2a)
        fileOut.write(lastLine_2b)
        fileOut.write("\n" + hLine + "\n")
        fileOut.write("\n")
        
    # Close file
    fileOut.close()

###############################################################
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
    VERBOSE  = False
    datasets = ["test"]
    OUTPUT   = "miniaod2tree_size.txt"
    TREENAME = "Events"

    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-v", "--verbose", dest="verbose", default=VERBOSE, action="store_true",
                      help="Verbose mode for debugging purposes [default: %s]" % (VERBOSE))

    parser.add_option("-f", "--rootFile", dest="rootFile", default=None, 
                      help="The ROOT file (miniaod2tree.root) to be analyzed [default: None]")

    parser.add_option("-t", "--treeName", dest="treeName", default=TREENAME,
                      help="The TTree name to be analyzed [default: %s]" % (TREENAME))

    parser.add_option("-o", "--output", dest="output", default=OUTPUT, type="string", 
                      help="The name of the output file to be produced [default: %s]" % (OUTPUT))

    #parser.add_option("-r", "--dir", dest="dirName", default=DIRNAME, type="string",
    #help="Custom name for CRAB directory name [default: %s]" % (DIRNAME))

    (opts, args) = parser.parse_args()

    if opts.rootFile == None:
        raise Exception("Must provide a ROOT file (miniaod2tree.root) as argument!")
    else:
        if os.path.exists(opts.rootFile):
            sys.exit( main(opts, args) )
        else:
            raise Exception("The ROOT file provided (%s) does not exists!" % (opts.rootFile) )
