#!/usr/bin/env python  
'''
DESCRIPTION:
Script to replace bin-by-bin uncertainties by Barlow-Beeston (autoMCStats) uncertainties
(see: https://cms-hcomb.gitbooks.io/combine/content/part2/bin-wise-stats.html)


USAGE:
 ./dcardCreateBarlowBeestonDatacards.py [path_to_datacard_directory]


EXAMPLE:
./dcardCreateBarlowBeestonDatacards.py datacards_Hplus2tb_13TeV_EraRun2016_Search80to1000_OptNominal_limits2016_DataDriven_mH180to500_StatOnly_180422_143959


NB: 
Remember to the option --X-rtd MINIMIZER_analytic to Combine command line!


AUTHOR:
S. Laurila


LAST UPDATED:
7.2.2018

'''
#================================================================================================       
# Imports
#================================================================================================       
import os
import sys
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================       
# Function definition
#================================================================================================       
def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg   = "\r\t" + msg
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
        sys.stdout.write(msg)
    sys.stdout.flush()
    return

def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if 1:
        return
    Print(msg, printHeader)
    return

#================================================================================================       
# Main
#================================================================================================       
if len (sys.argv) != 2 :
    print "You must give exactly one path to datacard directory as an input!"
    sys.exit(1)

# Make a copy of the input directory
input_path  = sys.argv[1]
input_directory = input_path.rstrip('\\').rsplit('/', 1)[-1]
output_directory_name = input_directory+"_autoMCstats"

Verbose("Copying directory %s into %s" % (input_directory, output_directory_name), True)
os.system("mkdir "+ output_directory_name)
os.system("cp -r %s/combine* %s" % (input_path, output_directory_name) )
Verbose("Copying done", True)

# list all the datacard files
filenames = os.listdir(output_directory_name)
datacard_names = []
os.chdir(output_directory_name)
for filename in filenames:
    if "datacard" in filename and ".txt" in filename:
        datacard_names.append(filename)
if len(datacard_names)==0:
    Print("No datacards found in input directory", True)
    sys.exit(1)

# remove old Combine output and limits from copied directory
#os.system("rm -rf CombineResults*")
    
Verbose("Looping over datacards:", True)
# For-loop: All  datacards (replace bin-by-bin uncertainties with Barlow-Beeston command)
for i, dcard_name in enumerate(datacard_names, 1):
    Print("Processing %s" % dcard_name, i==1)
    f_in = file("../" + input_path + "/" + dcard_name)
    
    with open(dcard_name, "w") as f:
        # For-loop: All lines in open file
        for line in f_in:
            if "kmax" in line:
                f.write("kmax     *     number of parameters\n")
            elif not "statBin" in line:
                f.write(line)
        f.write("\n\n* autoMCStats 0")
        f.truncate()
        
dirName = ShellStyles.SuccessStyle() + output_directory_name + ShellStyles.NormalStyle()
Print("Barlow-Beeston datacards stored in directory %s" % (dirName), True)
