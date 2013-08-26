#!/usr/bin/env python

import sys

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

analysis = "signalAnalysis"
counters = analysis+"Counters"


def getDatasetNames(multiCrabDir):
    datasets = dataset.getDatasetsFromMulticrabDirs([multiCrabDir],counters=counters)
    return datasets.getAllDatasetNames()

def validateDatasetExistence(dataset1names,dataset2names):
    print
    print "Validating dataset names.."
    return validateNames(dataset1names,dataset2names)

def validateNames(names1,names2):
    names = []
    for name1 in names1:
        match = False
        for name2 in names2:
            if name2 == name1:
                match = True
        if match:
            names.append(name1)
        else:
            print "    ",name1,"found in the reference datasets, but not in the validated datasets"
    print
    for name2 in names2:
        match = False
        for name1 in names1:
            if name2 == name1:
                match = True
        if not match:
            print "    ",name2,"found in the validated datasets, but not in the reference datasets"
    print

    return names

def findValue(row,counter):
    for i in xrange(counter.getNrows()):
        if row == counter.rowNames[i]:
            return int(counter.getCount(i,0).value())
    print "Counter value not found, exiting.."
    sys.exit()

def format(row,value1,value2):
    fString = "    "
    fString += row
    while len(fString) < 40:
        fString += " "
    fString += str(value1)
    while len(fString) < 50:
        fString += " "
    fString += str(value2)
    while len(fString) < 60:
        fString += " "
    return fString

def report(rownames,counter1,counter2):
    for row in rownames:
        value1 = findValue(row,counter1)
        value2 = findValue(row,counter2)

        if not value1 == value2:
            ratio = 0
            if not value2 == 0:
                ratio = float(value1)/value2
            print format(row,value1,value2),"ratio=",ratio
        else:
            print format(row,value1,value2)
    
def validateCounterValues(rownames,counter1,counter2):
    discrepancyFound = False
    for row in rownames:
        value1 = findValue(row,counter1)
        value2 = findValue(row,counter2)

        if value1 != value2:
            discrepancyFound = True
            
    if discrepancyFound:
        report(rownames,counter1,counter2)

    return discrepancyFound
    
def validateCounters(dataset1,dataset2):
    eventCounter1 = counter.EventCounter(dataset1)
    counter1 = eventCounter1.getMainCounter().getTable()
    rownames1 = counter1.getRowNames()

    eventCounter2 = counter.EventCounter(dataset2)
    counter2 = eventCounter2.getMainCounter().getTable()
    rownames2 = counter2.getRowNames()

    rownames = validateNames(rownames1,rownames2)

    discrepancyFound = validateCounterValues(rownames,counter1,counter2)
    if not discrepancyFound:
        print "    Validated OK"

def main(argv):

    if not len(sys.argv) == 3:
        print "\n"
        print "### Usage:   EventCounterValidation.py <ref multi-crab path> <new multi-crab path>\n"
        print "\n"
        sys.exit()

    referenceData = sys.argv[1]
    validateData  = sys.argv[2]

    print "Running script EventCounterValidation.py on"
    print
    print "          reference datasets = ",referenceData
    print "          validated datasets = ",validateData
    print

    refDatasetNames = getDatasetNames(referenceData)
    valDatasetNames = getDatasetNames(validateData)

    datasetNames = validateDatasetExistence(refDatasetNames,valDatasetNames)

    for datasetname in datasetNames:
        print "\n\n"
	print datasetname
	refDatasets = dataset.getDatasetsFromCrabDirs([referenceData+"/"+datasetname],counters=counters)
        valDatasets = dataset.getDatasetsFromCrabDirs([validateData+"/"+datasetname],counters=counters)

	validateCounters(refDatasets,valDatasets)


main(sys.argv[1:])


