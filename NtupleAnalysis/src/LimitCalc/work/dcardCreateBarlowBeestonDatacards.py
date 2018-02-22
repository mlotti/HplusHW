# Script to replace bin-by-bin uncertainties by Barlow-Beeston uncertainties
# (see: https://cms-hcomb.gitbooks.io/combine/content/part2/bin-wise-stats.html )
# Usage: ./dcardCreateBarlowBeestonDatacards.py [path_to_datacard_directory]
# NB! Remember to the option --X-rtd MINIMIZER_analytic to Combine command line!
#
# Author: S. Laurila
# Last updated: 7.2.2018

import os
import sys

if len (sys.argv) != 2 :
    print "You must give exactly one path to datacard directory as an input!"
    sys.exit(1)

# make a copy of the input directory
input_path = sys.argv[1]
input_directory = input_path.rstrip('\\').rsplit('/', 1)[-1]
output_directory_name = input_directory+"_autoMCstats"
print "Copying directory %s into %s"%(input_directory,output_directory_name)
os.system("mkdir "+output_directory_name)
os.system("cp -r %s/combine* %s"%(input_path,output_directory_name))
print "Copying done."

# list all the datacard files
filenames = os.listdir(output_directory_name)
datacard_names = []
os.chdir(output_directory_name)
for filename in filenames:
    if "datacard" in filename and ".txt" in filename:
        datacard_names.append(filename)
if len(datacard_names)==0:
    print "No datacards found in input directory"
    sys.exit(1)

# remove old Combine output and limits from copied directory
#os.system("rm -rf CombineResults*")
    
print "Looping over files:"
# loop over datacard files, replacing bin-by-bin uncertainties with Barlow-Beeston command
for dcard_name in datacard_names:
    print "Processing datacard %s"%dcard_name
    f_in = file("../"+input_path+"/"+dcard_name)
    with open(dcard_name, "w") as f:
        for line in f_in:
            if "kmax" in line:
                f.write("kmax     *     number of parameters\n")
            elif not "statBin" in line:
                f.write(line)
        f.write("\n\n* autoMCStats 0")
        f.truncate()
        
print "Barlow-Beeston datacards created, they are stored in directory "+output_directory_name
