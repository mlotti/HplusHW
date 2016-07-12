#! /usr/bin/env python
import os
import sys

_blackList = []
doTauNuTransverseMassPlots = True
doTauNuInvariantMassPlots = True
doTBTransverseMassPlots = False

def getMassPoints(selected):
    m = []
    for item in selected:
        myList = os.listdir("./%s"%item)
        for i in myList:
            if "lands_datacard" in i:
                myMass = i.replace("lands_datacard_hplushadronic_m","").replace(".txt","")
                if not myMass in m:
                    m.append(myMass)
    return m

def getTailKillerScenarios(selected):
    myList = []
    for item in selected:
        mySplit = item.split("_")
        for i in mySplit:
            if "OptQCDTailKiller" in i:
                myScenario = i.replace("OptQCDTailKiller","")
                if not myScenario in myList:
                    myList.append(myScenario)
    return myList

def hasMassPoint(item, mass):
    myStatus = False
    myList = os.listdir("./%s"%item)
    for i in myList:
        if "lands_datacard" in i:
            myMass = i.replace("lands_datacard_hplushadronic_m","").replace(".txt","")
            if mass == myMass:
                myStatus = True
    return myStatus

def hasTailKillerScenario(item, scenario):
    myStatus = False
    mySplit = item.split("_")
    for i in mySplit:
        if "OptQCDTailKiller" in i:
            myScenario = i.replace("OptQCDTailKiller","")
            if myScenario == scenario:
                myStatus = True
    return myStatus

def isLight(item):
    mySplit = item.split("_")
    for i in range(0,len(mySplit)):
        if "Run201" in mySplit[i]:
            return "Light" in mySplit[i+1]
    return False

def isHeavy(item):
    mySplit = item.split("_")
    for i in range(0,len(mySplit)):
        if "Run201" in mySplit[i]:
            return "Heavy" in mySplit[i+1]
    return False

def isTransverseMass(item):
    return "TransverseMass" in item

def isInvariantMass(item):
    return "FullMass" in item


def isTauNu(item):
    return not "TBbar" in item

def getHeader():
    s = "\\documentclass[11pt,a4paper]{article}\n"
    s += "\\usepackage{graphicx}\n"
    #s += "\\renewcommand{\\headrulewidth}{0pt}\n"
    #s += "\\renewcommand{\\footrulewidth}{0pt}\n"
    s += "\\setlength{\\textheight}{255mm}\n"
    s += "\\setlength{\\textwidth}{185mm}\n"
    s += "\\setlength{\\topmargin}{-25mm}\n"
    s += "\\setlength{\\hoffset}{-25mm}\n"
    s += "\\begin{document}\n"
    return s

def getFigure(figureList):
    mySortedList = []
    for i in range(0,len(figureList)):
        mySortedList.append(figureList[i][1])
    mySortedList.sort()

    rows = 1
    columns = 3
    if len(figureList) <= 15:
        rows = 3
        columns = 5
    if len(figureList) <= 12:
        rows = 3
        columns = 4
    if len(figureList) <= 9:
        rows = 3
        columns = 3
    if len(figureList) <= 6:
        rows = 2
    if len(figureList) <= 3:
        rows = 1

    s = "\\noindent"
    for i in range(0,rows):
        for j in range(0,columns):
            n = i*columns + j
            myPath = None
            if n < len(figureList):
                for k in range(0,len(figureList)):
                    if figureList[k][1] == mySortedList[n]:
                        myPath = figureList[k][0]
            if columns == 3:
                s += "  \\begin{minipage}{.30\\textwidth}\n"
            elif columns == 4:
                s += "  \\begin{minipage}{.23\\textwidth}\n"
            if n < len(figureList):
                s += "    \\includegraphics[width=\\textwidth,keepaspectratio]{%s} \\\\ \n"%myPath
                s += "    {\\footnotesize%s}\n"%mySortedList[n]
            else:
                s += "    \\includegraphics[width=\\textwidth,keepaspectratio]{placeholder}\n"
            s += "  \\end{minipage}\n" 
        s += "\\\\ \n"
    return s

def getFooter():
    s = "\end{document}\n"
    return s

if __name__ == "__main__":
    # Obtain directory listing
    myList = os.listdir(".")
    mySelected = []
    for item in myList:
        myStatus = True
        if not os.path.isdir(item):
            myStatus = False
        for b in _blackList:
            if b in item:
                myStatus = False
        if myStatus:
            mySelected.append(item)
    mySelected.sort()
    # Sniff mass points and scenarios
    myScenarios = getTailKillerScenarios(mySelected)
    myM = getMassPoints(mySelected)
    # Obtain header
    out = getHeader()
    # Do plots for transverse mass
    if doTauNuTransverseMassPlots:
        for m in myM:
            for s in myScenarios:
                i = 0
                myList = []
                for item in mySelected:
                    if isTauNu(item) and isTransverseMass(item) and hasMassPoint(item,m) and hasTailKillerScenario(item,s):
                        i += 1
                        mySplit = item.split("_")
                        k = 0
                        while not s in mySplit[k]:
                            k += 1
                        myList.append(["%s/controlPlots/DataDrivenCtrlPlot_M%s_09_TransverseMass"%(item,m)," ".join(map(str,mySplit[k+1:]))])
                if len(myList) > 0:
                    out += "{\\bf H+ to tau nu, Transverse mass, Tail killer: %s, m=%s GeV}\n\n"%(s,m)
                    out += getFigure(myList)
                    out += "\\newpage \n"
    # Do plots for invariant mass
    if doTauNuInvariantMassPlots:
        for m in myM:
            for s in myScenarios:
                i = 0
                myList = []
                for item in mySelected:
                    if isTauNu(item) and isInvariantMass(item) and hasMassPoint(item,m) and hasTailKillerScenario(item,s) and int(m) < 180:
                        i += 1
                        mySplit = item.split("_")
                        k = 0
                        while not s in mySplit[k]:
                            k += 1
                        myList.append(["%s/controlPlots/DataDrivenCtrlPlot_M%s_09_FullMass"%(item,m)," ".join(map(str,mySplit[k+1:]))])
                if len(myList) > 0:
                    out += "{\\bf H+ to tau nu, Invariant mass, Tail killer: %s, m=%s GeV}\n\n"%(s,m)
                    out += getFigure(myList)
                    out += "\\newpage \n"
    # Do plots for TBbar
    if doTBTransverseMassPlots:
        for m in myM:
            for s in myScenarios:
                i = 0
                myList = []
                for item in mySelected:
                    if not isTauNu(item) and isTransverseMass(item) and hasMassPoint(item,m) and hasTailKillerScenario(item,s):
                        i += 1
                        mySplit = item.split("_")
                        k = 0
                        while not s in mySplit[k]:
                            k += 1
                        myList.append(["%s/controlPlots/DataDrivenCtrlPlot_M%s_09_TransverseMass"%(item,m)," ".join(map(str,mySplit[k+1:]))])
                if len(myList) > 0:
                    out += "{\\bf H+ to tb, Transverse mass, Tail killer: %s, m=%s GeV}\n\n"%(s,m)
                    out += getFigure(myList)
                    out += "\\newpage \n"  

    out += getFooter()
    f = open("optimizationFigures.tex", "w")
    f.write(out)
    f.close()
    os.system("pdflatex optimizationFigures.tex")
