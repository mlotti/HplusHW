#!/usr/bin/env python

# Script for merging result directories

import sys
import os
import shutil

import ROOT

_debug = True

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," input_rootfile1 input_rootfile2 <...>"
    print
    sys.exit()

def readMulticrabDataset(dirName):
    dsets = []
    mcrabName = os.path.join(dirName, "multicrab.cfg")
    if not os.path.exists(mcrabName):
        raise Exception("Error: Cannot find file '%s'!"%mcrabName)
    f = open(mcrabName)
    for line in f.readlines():
        if len(line) > 1 and line[0] != '#':
            modLine = line.replace("[","").replace("]","").replace("\n","")
            extension = modLine.replace(dirName.replace("pseudoMulticrab_",""),"")
            dsets.append(extension)
    f.close()
    return dsets

def loopOverDirectory(dirname, inputFiles, outputFile):
    if _debug:
        print "  entering directory: "+dirname
    # Change directory for input files
    for f in inputFiles:
        status = f.cd(dirname)
        if not status:
            raise Exception("This should not happen")
    # Create dir to output file
    if dirname != "/":
        s = dirname.split("/")
        currentDir = outputFile
        if len(s) > 2:
            subdirName = "%s"%"/".join(map(str,s[1:len(s)-1]))
            currentDir = outputFile.Get(subdirName)
        dirobj = currentDir.mkdir(s[len(s)-1])
        if dirobj == None:
            raise Exception("Error: Could not create directory '%s'"%dirname)
        status = outputFile.cd(dirname)
        if not status:
            raise Exception("This should not happen")
    # Loop over current dir items
    keys = None
    if dirname == "/":
        keys = inputFiles[0].GetListOfKeys()
    else:
        keys = inputFiles[0].Get(dirname[1:]).GetListOfKeys()
    for i in range(keys.GetSize()):
        # Check if the item is a directory
        obj = keys.At(i).ReadObj()
        keyname = keys.At(i).GetName()
        className = keys.At(i).GetClassName()
        #status = inputFiles[0].cd(keyname)
        #print "DBG:    %s: %s"%(className, os.path.join(dirname, keyname))

        if isinstance(obj, ROOT.TDirectory):
            loopOverDirectory(os.path.join(dirname, keyname), inputFiles, outputFile)
        elif isinstance(obj, ROOT.TH1):
            if _debug:
                print "    merging %s: %s"%(className, os.path.join(dirname, keyname))
            clonedObj = obj.Clone() # This goes into the output file directory, because it is cd:d last
            #print "DBG: clone",clonedObj.GetBinContent(1),clonedObj.GetBinError(1)
            for f in inputFiles[1:]:
                h = f.Get(os.path.join(dirname, keyname))
                if h == None:
                    raise Exception("Error: Failed to obtain '%s' from file '%s'!"%(os.path.join(os.path.join(dirname, keyname), keyname), f.GetTitle()))
                clonedObj.Add(h)
                #print "DBG: add",h.GetBinContent(1),h.GetBinError(1)
                #print "DBG: sum",clonedObj.GetBinContent(1),clonedObj.GetBinError(1)
                h.Delete()
            clonedObj.Write()
        elif isinstance(obj, ROOT.TNamed):
            # Copy from first input file
            if _debug:
                  print "    copying %s: %s"%(className, os.path.join(dirname, keyname))
            clonedObj = obj.Clone() # This goes into the output file directory, because it is cd:d last
            clonedObj.Write()
        else:
            raise Exception("Unknown type: %s of type %s"%(os.path.join(dirname, keyname), className))

def main():
    if len(sys.argv) < 3:
        usage()

    # Check for duplicate input files
    for i in range(1,len(sys.argv)):
        for j in range(i,len(sys.argv)):
            if i != j and sys.argv[i] == sys.argv[j]:
                raise Exception("Error: The input file '%s' is given twice as input!"%sys.argv[i])

    # Determine common name prefix
    namePrefix = ""
    i = 0
    imin = 99999
    for n in sys.argv[1:]:
        if len(n) < imin:
            imin = len(n)
    while namePrefix == "" and i < imin:
        for n in sys.argv[2:]:
            if sys.argv[1][i] != n[i]:
                if i > 1:
                    namePrefix = sys.argv[1][:i-1]
            else:
                i += 1
    #print namePrefix
    
    # Construct output directory
    outDirName = namePrefix+"_merged"
    for n in sys.argv[1:]:
        outDirName += n.replace(namePrefix, "")
    if os.path.exists(outDirName):
        shutil.rmtree(outDirName)
    os.mkdir(outDirName)
    
    # Find dataset names and check consistency between directories
    dsetExtensions = readMulticrabDataset(sys.argv[1])
    
    for n in sys.argv[2:]:
        otherDsetExtensions = readMulticrabDataset(n)
        if len(dsetExtensions) != len(otherDsetExtensions):
            raise Exception("Error: datasets are different between directories '%s' and '%s'!"%(sys.argv[1], n))
        for dsetExt in otherDsetExtensions:
            if not dsetExt in dsetExtensions:
                raise Exception("Error: dataset extension '%s' not found in all of the input directories!"%dsetExt)

    # Copy non-directory files
    for n in sys.argv[1:]:
        dirlist = os.listdir(n)
        for item in dirlist:
            if not os.path.isdir(os.path.join(n, item)):
                if item != "multicrab.cfg" and not os.path.exists(os.path.join(outDirName, item)):
                    print "Copying %s ..."%item
                    shutil.copyfile(os.path.join(n, item), os.path.join(outDirName, item))
    
    # Create multicrab.cfg
    f = open(os.path.join(outDirName,"multicrab.cfg"), "w")
    if f == None:
        raise Exception("Error: Cannot write '%s'!"%os.path.join(outDirName,"multicrab.cfg"))
    for dsetExt in dsetExtensions:
        f.write("[QCDMeasurement%s]\n"%dsetExt)
    f.close()
    print "Created multicrab.cfg"

    # Merge datasets
    for dsetExt in dsetExtensions:
        print "Merging dataset %s ..."%dsetExt
        # Create directory for output dataset
#        outDsetName = "QCDMeasurement%s"%dsetExt
        outDsetName = dsetExt
        outPath = os.path.join(outDirName, outDsetName, "res")
        os.mkdir(os.path.join(outDirName, outDsetName))
        os.mkdir(outPath)
        # Create output file
        #print "    out:",os.path.join(outPath, "histograms-%s.root"%outDsetName)
        outFile = ROOT.TFile.Open(os.path.join(outPath, "histograms-%s.root"%outDsetName), "recreate")
        if outFile == None:
            raise Exception("Error creating output file for dataset '%s'!"%outDsetName)
        # Open input root files
        fINs = []
        for n in sys.argv[1:]:
#            inname = n.replace("pseudoMulticrab_","")+dsetExt
            inname = dsetExt

#            if "pseudoMulticrab_" in n:
#                inname = n.replace("pseudoMulticrab_","")+dsetExt

            fname = os.path.join(n, inname, "res", "histograms-%s.root"%(inname))
            #print "     in:",fname
            if not os.path.exists(fname):
                raise Exception("Error: Cannot find file '%s'!"%fname)
            fINs.append(ROOT.TFile.Open(fname))
        # Loop over root file objects
        loopOverDirectory("/", fINs, outFile)
        
        # Close input root files
        for item in fINs:
            ROOT.gROOT.GetListOfFiles().Remove(item)
            item.Close()
        
        # Close output root file
        ROOT.gROOT.GetListOfFiles().Remove(outFile)
        outFile.Close()
    
    # Done
    print "\nDone merging '%s'"%outDirName

if __name__ == "__main__":
    main()
