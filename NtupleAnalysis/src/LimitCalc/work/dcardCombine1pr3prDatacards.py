# Script to combine datacards from 1-prong and 3-prong analyses into one
# Usage: run inside CMSSW workspace with Combine installed
# Author: S. Laurila

import os
import re
import time
import datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-1", "--1pr", action="store", type="string", dest="dir1",
                  help="datacard directory from 1-prong analysis")
parser.add_option("-3", "--3pr", action="store", type="string", dest="dir3",
                  help="datacard directory from 3-prong analysis")
(options, args) = parser.parse_args()

# make a new directory for combined datacards
date = datetime.date.today().strftime('%y%m%d') 
t = datetime.datetime.now().strftime('%H%M%S')
dirname = "datacards_combine_1+3pr_%s_%s"%(date,t)
os.system("mkdir %s"%dirname)

# copy and rename old 1-prong root and txt files
os.system("cp %s/*.root %s"%(options.dir1,dirname))
os.system("cp %s/*.txt %s"%(options.dir1,dirname))
filenames = os.listdir(dirname)
os.chdir(dirname)
mass_points_1pr = []
for filename in filenames:
    if ".root" in filename:
        os.rename(filename, filename.replace(".root","_1pr.root"))
    if ".txt" in filename:
        os.rename(filename, filename.replace(".txt","_1pr.txt"))
    mass_points_1pr.append(int(filter(str.isdigit, filename)))

os.chdir("..")

# copy and rename old 3-prong root and txt files
os.system("cp %s/*.root %s"%(options.dir3,dirname))
os.system("cp %s/*.txt %s"%(options.dir3,dirname))
filenames = os.listdir(dirname)
os.chdir(dirname)
mass_points_3pr = []
for filename in filenames:
    if not "1pr" in filename and ".root" in filename:
        os.rename(filename, filename.replace(".root","_3pr.root"))
    if not "1pr" in filename and ".txt" in filename:        
        os.rename(filename, filename.replace(".txt","_3pr.txt"))
    mass_points_3pr.append(int(filter(str.isdigit, filename)))

# update references to root files in txt datacards
firstline = "" # first line of 1pr file, to be used later
for filename in os.listdir("."):
    if "_1pr.txt" in filename:
        with open(filename, "r+") as f:
            firstline = f.readline()
            f.seek(0)
            s = f.read()
            s = s.replace(".root", "_1pr.root")
            f.seek(0)
            f.write(s)
            f.truncate()
    if "_3pr.txt" in filename:
        with open(filename, "r+") as f:
            s = f.read()
            s = s.replace(".root", "_3pr.root")
            f.seek(0)
            f.write(s)
            f.truncate()

# run combineCards.py for all mass points available 
# from both 1-prong and 3-prong analyses
lumi = re.findall(r'luminosity=\d+\.\d+', firstline)
for m in mass_points_1pr:
    if m in mass_points_3pr:
        dcard = "combine_datacard_hplushadronic_m%d"%m
        os.system("combineCards.py taunuhadr1pr=%s_1pr.txt taunuhadr3pr=%s_3pr.txt > %s.txt"%(dcard,dcard,dcard))
        # add mass, lumi and other information to the new datacard as first line
        text = "Description: Combine datacard (combined from 1-prong and 3-prong datacards) mass=%d, %s 1/pb\n"%(m,lumi[0])
        text += "Date: %s\n"%time.ctime()
        with file(dcard+".txt", 'r') as old: data = old.read()
        data = data[data.find('\n')+1:-1] # remove the default description by combineCards.py
        with file(dcard+".txt", 'w') as modified: modified.write(text+data)
print "New datacards saved to directory "+dirname

# remove 1pr and 3pr only datacards
for filename in os.listdir("."):
    if "pr.txt" in filename:
        os.system("rm %s"%filename)
