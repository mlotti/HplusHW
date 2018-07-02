#!/usr/bin/env python
'''

  DESCRIPTION:
  Simple script to merge the uncertainties JSONs into one JSON file.
  
  USAGE:
  ./mergeJSONs.py
   
'''

# ================
# Imports
# ================
import os
import re
import sys

import copy
from optparse import OptionParser


#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    aux.Print(msg, printHeader)
    return


# ==========================
# Main
# ==========================
def main(opts):
    
    merged = open("uncertainties_GenuineTT.json", "w")
    
    myList = [opts.mtop, opts.showerScales, opts.highPtRadiation, opts.partonShower, opts.evtGen, opts.matching]
    myLines= []
    
    for k, json in enumerate(myList):
        myfile = open(json, "r")
        count = len(myfile.readlines())
        myLines.append(count)
        myfile.close()

    merged.write("{\n")
    
    for k, myfile in enumerate(myList):
        
        i = open(myfile, "r")
        line = i.readline()
        cnt = 1
        while line:
            
            if opts.verbose:
                print("Line {}: {}".format(cnt, line.strip()))
                
            line = i.readline()
            
            if k == 0:
                if cnt < myLines[k]-2:
                    merged.write(line)
                elif cnt == myLines[k]-1:
                    merged.write("      },\n")
                else:
                    pass
            else:
                
                if cnt > 2:
                    if cnt < myLines[k]-2:
                        merged.write(line)
                    elif cnt == myLines[k]-2:
                        if k == len(myList)-1:
                            merged.write("      } \n")
                        else:
                            merged.write("      }, \n")
                    else:
                        pass
                else:
                    pass
            
            cnt += 1

        i.close()

    merged.write("}")
    merged.close()
            
    return

           

#================================================================================================ 
# Main                                                                                          
#================================================================================================  
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
    # Default Settings
    VERBOSE         = False
    MTOP            = "uncertainties_mTop.json"
    SHOWERSCALES    = "uncertainties_showerScales.json"
    HIGHPTRADIATION = "uncertainties_highPtRadiation.json"
    PARTONSHOWER    = "uncertainties_partonShower.json"
    EVTGEN          = "uncertainties_evtGen.json"
    MATCHING        = "uncertainties_matching.json"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)
    parser.add_option("--mtop", dest="mtop", action="store", help="Path to the mtop JSON file", default=MTOP)
    parser.add_option("--showerScales", dest="showerScales", action="store", help="Path to the showerScales JSON file", default=SHOWERSCALES)
    parser.add_option("--highPtRadiation", dest="highPtRadiation", action="store", help="Path to the highPtRadiation JSON file", default=HIGHPTRADIATION)
    parser.add_option("--partonShower", dest="partonShower", action="store", help="Path to the partonShower JSON file", default=PARTONSHOWER)
    parser.add_option("--evtGen", dest="evtGen", action="store", help="Path to the evtGen JSON file", default=EVTGEN)
    parser.add_option("--matching", dest="matching", action="store", help="Path to the matching JSON file", default=MATCHING)
    
    (opts, parseArgs) = parser.parse_args()

    if opts.mtop == None or opts.showerScales == None or opts.highPtRadiation == None or opts.partonShower == None or opts.evtGen == None or opts.matching == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        parser.print_help()
        sys.exit(1)
        
    # Call the main function
    main(opts)
