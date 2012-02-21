#!/usr/bin/env python

import sys
import os
import ROOT

from datetime import date, time, datetime

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

def getagreementwithcolor(ratio):
    myoutput = ""
    if abs(ratio-1) < 0.0001:
        myoutput += "<td></td>"
    elif abs(ratio-1) < 0.01:
        myoutput += "<td align=center>%1.5f</td>" % ratio
    elif abs(ratio-1) < 0.03:
        myoutput += "<td align=center bgcolor=#d0d000>%1.5f</td>" % ratio
    else:
        myoutput += "<td align=center bgcolor=#d00000>%1.5f</td>" % ratio
    return myoutput

def report(oldrow,row,counter1,counter2):
    # obtain event counts
    value1 = findValue(row,counter1)
    value2 = findValue(row,counter2)
    myoutput = "<tr>\n"
    myoutput += "<td><b>"+row+"</b></td>"
    myoutput += "<td align=center>"+str(value1)+"</td>"
    myoutput += "<td align=center>"+str(value2)+"</td>"
    if value1 == value2:
        myoutput += "<td></td>"
        print format(row,value1,value2)
    else:
        myratio = -1;
        if value2 > 0:
            myratio = float(value1) / float(value2)
        myoutput += getagreementwithcolor(myratio)
        print format(row,value1,value2),"ratio=",myratio
    # obtain efficiencies
    oldvalue1 = 0
    oldvalue2 = 0
    eff1 = 0
    eff2 = 0
    if not oldrow == "":
        oldvalue1 = findValue(oldrow,counter1)
        oldvalue2 = findValue(oldrow,counter2)
    if oldvalue1 > 0:
        eff1 = float(value1) / float(oldvalue1)
    if oldvalue2 > 0:
        eff2 = float(value2) / float(oldvalue2)
    myratio = 1.0;
    if eff2 > 0:
         myratio = eff1 / eff2
    myoutput += "<td align=center>%1.5f</td>" % eff1
    myoutput += "<td align=center>%1.5f</td>" % eff2
    myoutput += getagreementwithcolor(myratio)

    myoutput += "</tr>\n"
    return myoutput
    
def validateCounterValues(rownames,counter1,counter2):
    # Make table in output
    myoutput = "<table>\n"
    myoutput += "<tr><td><b>Counter</b></td>"
    myoutput += "<td><b>Ref.counts</b></td><td><b>New counts</b></td><td><b>Ref./New</b></td>"
    myoutput += "<td><b>Ref. eff.</b></td><td><b>New eff.</b></td><td><b>Ref./New</b></td>"
    myoutput += "</tr>\n"
    oldrow = ""
    for row in rownames:
        myoutput += report(oldrow, row,counter1,counter2)
        oldrow = row
    myoutput += "</table>\n"
    return myoutput
    
    
def validateCounters(dataset1,dataset2):
    eventCounter1 = counter.EventCounter(dataset1)
    counter1 = eventCounter1.getMainCounter().getTable()
    rownames1 = counter1.getRowNames()

    eventCounter2 = counter.EventCounter(dataset2)
    counter2 = eventCounter2.getMainCounter().getTable()
    rownames2 = counter2.getRowNames()

    rownames = validateNames(rownames1,rownames2)

    myoutput = validateCounterValues(rownames,counter1,counter2)
    return myoutput

def getHistogram(dataset, histoname, isRef):
    roothisto = dataset.getDatasetRootHisto(histoname[0])
    roothisto.normalizeToOne()
    h = roothisto.getHistogram()
    # Rebin
    a = (h.GetXaxis().GetXmax() - h.GetXaxis().GetXmin()) / h.GetNbinsX()
    if histoname[1] > a:
        h.Rebin(int(histoname[1] / a))
    # Set attributes
    h.SetStats(1)
    if isRef:
        h.SetName("Reference")
        h.SetFillStyle(1001)
        h.SetFillColor(ROOT.kBlue-6)
        h.SetLineColor(ROOT.kBlue-6)
        #statbox.SetTextColor(ROOT.kBlue-6)
    else:
        h.SetName("New")
        h.SetMarkerColor(ROOT.kBlack)
        h.SetLineColor(ROOT.kBlack)
        h.SetMarkerStyle(20)
        h.SetMarkerSize(1.0)
        #statbox.SetTextColor(ROOT.kBlack)

#p1->SetX1NDC(xmin);
#p1->SetX2NDC(xmax);
#p1->SetY1NDC(ymin);
#p1->SetY2NDC(ymax);
    return h

def setframeextrema(myframe, h1, h2, logstatus):
    # obtain and set x range
    xmin = h1.GetXaxis().GetXmin()
    if h2.GetXaxis().GetXmin() > h1.GetXaxis().GetXmin():
        xmin = h2.GetXaxis().GetXmin()
    xmax = h1.GetXaxis().GetXmax()
    if h2.GetXaxis().GetXmax() > h1.GetXaxis().GetXmax():
        xmax = h2.GetXaxis().GetXmax()
    myframe.GetXaxis().Set(1, xmin, xmax)
    # obtain and set minimum y value
    ymin = 0.0
    if logstatus == "log":
        ymin = 1.5
        for i in range(1, h1.GetNbinsX()):
            if h1.GetBinContent(i) > 0 and h1.GetBinContent(i) < ymin:
                ymin = h1.GetBinContent(i)
        for i in range(1, h2.GetNbinsX()):
            if h2.GetBinContent(i) > 0 and h2.GetBinContent(i) < ymin:
                ymin = h2.GetBinContent(i)
        if ymin > 1:
            ymin = 1.5
    myscalefactor = 1.1
    if logstatus == "log":
        myscalefactor = 1.5
        myframe.SetMinimum(ymin / myscalefactor)
    else:
        myframe.SetMinimum(ymin)
    # obtain and set minimum x value
    ymax = h1.GetMaximum()    
    if h2.GetMaximum() > h1.GetMaximum():
        ymax = h2.GetMaximum()
    myframe.SetMaximum(ymax*myscalefactor)

def analysehistodiff(canvas,h1,h2):
    if not h1.GetNbinsX() == h2.GetNbinsX():
        canvas.SetFillColor(ROOT.kOrange)
    else:
        # same number of bins in histograms
        diff = 0.0
        zerocount = 0
        for i in range(1, h1.GetNbinsX()):
            if h2.GetBinContent(i) > 0:
                diff += abs(h1.GetBinContent(i) / h2.GetBinContent(i) - 1.0)
            elif h1.GetBinContent(i) > 0:
                zerocount = zerocount + 1
        if (diff > 0.03 or zerocount > 3):
            canvas.SetFillColor(ROOT.kRed+2)
        elif (diff > 0.01 or zerocount > 1):
            canvas.SetFillColor(ROOT.kOrange)
        

def validateHistograms(mydir,dataset1,dataset2):
    mysubdir = mydir+"/"+dataset1.getName()
    os.mkdir(mysubdir)

    myoutput = "<br><b>Histograms for validation:</b><br>\n"
    myoutput += "Color legend: blue histogram = reference, red points = dataset to be validated<br><br>\n"
    print "Generating validation histograms"
    histolist = [
        ["signalAnalysis/transverseMass", 20, "log"]
    ]

    mycount = 0
    mycolumns = 3
    myscale = 200.0 / float(mycolumns)
    
    myoutput += "<table>\n"
    for histoname in histolist:
        if mycount == 0:
            myoutput += "<tr>\n"
        mycount = mycount + 1
        myoutput += "<td width=%f%%>" % myscale
        myoutput += "src="+histoname[0]+"<br>"
        if dataset1.hasRootHisto(histoname[0]) and dataset2.hasRootHisto(histoname[0]):
            # construct output name
            myname = histoname[0].replace("/", "_")
            # Obtain histograms and make canvas
            h1 = getHistogram(dataset1, histoname, True)
            h2 = getHistogram(dataset1, histoname, False)
            canvas = ROOT.TCanvas(histoname[0],histoname[0],600,400)
            canvas.SetFrameFillColor(ROOT.TColor.GetColor("#fdffff"))
            canvas.SetFrameFillStyle(1001)
            
            myscalefactory = 1.1
            if histoname[2] == "log":
                canvas.SetLogy()
                myscalefactory = 1.5
            # Obtain minimum and maximum
            # Make frame and set its extrema
            myframe = h1.Clone("hclone");
            myframe.SetBinContent(1,0)
            myframe.SetStats(0)
            setframeextrema(myframe,h1,h2,histoname[2])
            # Analyse similarity
            analysehistodiff(canvas,h1,h2)
            # Draw and generate image
            canvas.Draw()
            myframe.Draw()
            h1.Draw("histo sames")
            h2.Draw("e1 sames")
            # Modify stat boxes
            ROOT.gPad.Update()
            h1.FindObject("stats").SetLineColor(ROOT.kBlue-6)
            h1.FindObject("stats").SetTextColor(ROOT.kBlue-6)
            h2.FindObject("stats").SetY1NDC(0.615)
            h2.FindObject("stats").SetY2NDC(0.775)
            # Save plot
            canvas.RedrawAxis()
            canvas.Modified()
            canvas.Print(mysubdir+"/"+myname+".png")
            myoutput += "<img width=%f%%" % myscale
            myoutput += " height=%f%%" % myscale
            myoutput += " src="+mysubdir+"/"+myname+".png alt="+histoname[0]+"><br>"
        else:
            # cannot create figure because one or both histograms are not available
            if not dataset1.hasRootHisto(histoname):
                print "  Warning: Did not find histogram",histoname,"in",dataset1.getName()
                myoutput += "<text color=e00000>Not found for reference!</text><br>"
            if not dataset2.hasRootHisto(histoname):
                print "  Warning: Did not find histogram",histoname,"in",dataset2.getName()
                myoutput += "<text color=e00000>Not found for new dataset!</text><br>"
        # close cell (and if necessary also row) in table
        myoutput += "</td>\n"
        if mycount == mycolumns:
            myoutput += "</tr>\n"
            mycount = 0
    # close if necessary row in table
    if mycount > 0:
        myoutput += "</tr>\n"
    myoutput += "</table>\n"
    print "\nHistograms done for dataset",dataset1.getName()
    print "Legend: blue histogram = reference, red points = dataset to be validated\n"
    return myoutput

def makehtml(mydir, myoutput):
    myhtmlheader = "<html>\n<head>\n<title>ValidationResults</title>\n</head>\n<body>\n"
    myhtmlfooter = "</body>\n</html>\n"
    myfile = open(mydir+"/index.html","w")
    #myfile = open("index.html","w")
    myfile.write(myhtmlheader)
    myfile.write("<h1>Validation results for: "+mydir+"</h1><br>\n<hr><br>\n")
    myfile.write(myoutput)
    myfile.write(myhtmlfooter)
    myfile.close()

def main(argv):
    if not len(sys.argv) == 3:
        print "\n"
        print "### Usage:   EventCounterValidation.py <ref multi-crab path> <new multi-crab path>\n"
        print "\n"
        sys.exit()

    referenceData = sys.argv[1]
    validateData  = sys.argv[2]
    
    mytimestamp = datetime.now().strftime("%d%m%y_%H%M%S");
    mydir = "validation_"+mytimestamp
    os.mkdir(mydir)

    myoutput = ""

    print "Running script EventCounterValidation.py on"
    print
    print "          reference datasets = ",referenceData
    print "          validated datasets = ",validateData
    print

    myoutput += "<b>Shell command that was run:</b>"
    for arg in argv:
         myoutput += " "+arg
    myoutput += "<br><br>\n"
    myoutput += "<b>Reference datasets:</b> "+referenceData+"<br>\n"
    myoutput += "<b>New datasets to be validated:</b> "+validateData+"<br>\n<hr><br>\n"

    refDatasetNames = getDatasetNames(referenceData)
    valDatasetNames = getDatasetNames(validateData)

    datasetNames = validateDatasetExistence(refDatasetNames,valDatasetNames)

    for datasetname in datasetNames:
        print "\n\n"
        print datasetname
        myoutput += "<h2>Dataset: "+datasetname+"</h2><br>\n"
        refDatasets = dataset.getDatasetsFromCrabDirs([referenceData+"/"+datasetname],counters=counters)
        valDatasets = dataset.getDatasetsFromCrabDirs([validateData+"/"+datasetname],counters=counters)

        myoutput += validateCounters(refDatasets,valDatasets)
        myoutput += validateHistograms(mydir,refDatasets.getDataset(datasetname),valDatasets.getDataset(datasetname))
        myoutput += "<hr><br>\n"
        
    print "\nResults saved into directory:",mydir
    makehtml(mydir,myoutput)

main(sys.argv[1:])


