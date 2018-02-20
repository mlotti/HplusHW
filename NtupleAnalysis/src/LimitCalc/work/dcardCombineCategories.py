# Script to combine datacards of two or three categories into one
# Usage: run inside a CMSSW workspace with Combine installed
# Author: S. Laurila
# Last updated: 6.2.2018

import os
import re
import time
import datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--a", action="store", type="string", dest="dir1",
                  help="datacard directory for category A")
parser.add_option("-b", "--b", action="store", type="string", dest="dir2",
                  help="datacard directory for category B")
parser.add_option("-c", "--c", action="store", type="string", dest="dir3",
                  help="datacard directory for category C", default = None)
(options, args) = parser.parse_args()

# make a new directory for combined datacards
date = datetime.date.today().strftime('%y%m%d') 
t = datetime.datetime.now().strftime('%H%M%S')
dirname = "datacards_combine_multicategory_%s_%s"%(date,t)
os.system("mkdir %s"%dirname)

# copy and rename old category A root and txt files
os.system("cp %s/*.root %s"%(options.dir1,dirname))
os.system("cp %s/*.txt %s"%(options.dir1,dirname))
filenames = os.listdir(dirname)
os.chdir(dirname)
mass_points_a = []
for filename in filenames:
    if ".root" in filename:
        os.rename(filename, filename.replace(".root","_a.root"))
    if ".txt" in filename:
        os.rename(filename, filename.replace(".txt","_a.txt"))
    mass_points_a.append(int(filter(str.isdigit, filename)))

os.chdir("..")

# copy and rename old category B root and txt files
os.system("cp %s/*.root %s"%(options.dir2,dirname))
os.system("cp %s/*.txt %s"%(options.dir2,dirname))
filenames = os.listdir(dirname)
os.chdir(dirname)
mass_points_b = []
for filename in filenames:
    if not "_a." in filename and not "_c." in filename and ".root" in filename:
        os.rename(filename, filename.replace(".root","_b.root"))
    if not "_a." in filename and not "_c." in filename and ".txt" in filename:        
        os.rename(filename, filename.replace(".txt","_b.txt"))
    mass_points_b.append(int(filter(str.isdigit, filename)))

os.chdir("..")

# copy and rename old category C root and txt files
if options.dir3 != None:
    os.system("cp %s/*.root %s"%(options.dir3,dirname))
    os.system("cp %s/*.txt %s"%(options.dir3,dirname))
    filenames = os.listdir(dirname)
    os.chdir(dirname)
    mass_points_c = []
    for filename in filenames:
        if not "_a." in filename and not "b." in filename and ".root" in filename:
            os.rename(filename, filename.replace(".root","_c.root"))
        if not "_a." in filename and not "_b." in filename and ".txt" in filename:        
            os.rename(filename, filename.replace(".txt","_c.txt"))
        mass_points_c.append(int(filter(str.isdigit, filename)))

# update references to root files in txt datacards
firstline = "" # first line of category A file, to be used later
for filename in os.listdir("."):
    if "_a.txt" in filename:
        with open(filename, "r+") as f:
            firstline = f.readline()
            f.seek(0)
            s = f.read()
            s = s.replace(".root", "_a.root")
            f.seek(0)
            f.write(s)
            f.truncate()
    if "_b.txt" in filename:
        with open(filename, "r+") as f:
            s = f.read()
            s = s.replace(".root", "_b.root")
            f.seek(0)
            f.write(s)
            f.truncate()
    if "_c.txt" in filename:
        with open(filename, "r+") as f:
            s = f.read()
            s = s.replace(".root", "_c.root")
            f.seek(0)
            f.write(s)
            f.truncate()

# run combineCards.py for mass points available in all categories considered
lumi = re.findall(r'luminosity=\d+\.\d+', firstline)
for m in mass_points_a:
    if m in mass_points_b and (options.dir3==None or m in mass_points_c):
        dcard = "combine_datacard_hplushadronic_m%d"%m
        text = ""
        if options.dir3==None:
            os.system("combineCards.py taunuhadr_a=%s_a.txt taunuhadr_b=%s_b.txt > %s.txt"%(dcard,dcard,dcard))
            text += "Description: Combine datacard (combined from two categories) mass=%d, %s 1/pb\n"%(m,lumi[0])
        else:
            os.system("combineCards.py taunuhadr_a=%s_a.txt taunuhadr_b=%s_b.txt taunuhadr_c=%s_c.txt > %s.txt"%(dcard,dcard,dcard,dcard))
            text += "Description: Combine datacard (combined from three categories) mass=%d, %s 1/pb\n"%(m,lumi[0])
        # add mass, lumi and other information to the new datacard as first line
        text += "Date: %s\n"%time.ctime()
        with file(dcard+".txt", 'r') as old: data = old.read()
        data = data[data.find('\n')+1:-1] # remove the default description by combineCards.py
        with file(dcard+".txt", 'w') as modified: modified.write(text+data)
print "New datacards saved to directory "+dirname

# remove original, category-specific datacards
for filename in os.listdir("."):
    if "a.txt" in filename or "b.txt" in filename or "c.txt" in filename:
        os.system("rm %s"%filename)
