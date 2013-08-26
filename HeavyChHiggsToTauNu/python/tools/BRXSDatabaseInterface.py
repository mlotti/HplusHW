#!/usr/bin/env python

import sys
import re
from array import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

class BRXSDatabaseInterface:
    def __init__(self,rootfile):
        print "BRXSDatabaseInterface: reading file",rootfile
	self.rootfile  = rootfile
	self.fIN       = ROOT.TFile.Open(rootfile)
	self.program   = "FH"
	self.selection = ""

        self.BRvariable= "BR_tHpb*BR_Hp_taunu"

	self.expLimit  = {}

	self.tree      = self.fIN.Get(self.program+"_results")

	self.variables = []
	self.names     = []

	branches =  self.tree.GetListOfBranches()

    	for branch in branches:
	    #print branch.GetName()
            variable = array('d',[0.])
            branch.SetAddress(variable)
            self.variables.append(variable)
            self.names.append(branch.GetName())
        
    def setSelection(self,selection):
	self.selection = selection

    def floatSelection(self,selection,epsilon = 0.01):
        splitSelection = selection.split("&&")
        retList = []
        equals_re = re.compile("(?P<variable>(\S+))==(?P<value>(\S+))")
        for s in splitSelection:
            match = equals_re.search(s)
            if match:
                s = match.group("variable") + ">" + str(float(match.group("value"))-epsilon)
                s+= "&&" + match.group("variable") + "<" + str(float(match.group("value"))+epsilon)
            retList.append(s)
        returnSelection = ""
        for i,s in enumerate(retList):
            returnSelection+=s
            if i < len(retList) -1:
                returnSelection+="&&"
        return returnSelection
    
    def get(self,variable1,variable2,selection):
	if not self.selection == "":
	    selection = self.selection+"&&"+selection

	return self.getGraph(variable1,variable2,selection).Eval(self.getCutValue(variable2,selection))
    
    def getOLD(self,variable,selection):
        if not self.selection == "":
            selection = self.selection+"&&"+selection
	nev = self.tree.GetEntries()
	for i in range(nev):
	    self.tree.GetEvent(i)
	    if self.passed(selection):
	        return self.getValue(variable)
    
    def getValue(self,varname):
	variables = varname.split("*")
        value = 1
	for v in variables:
	    value = value * self.variables[self.names.index(v)][0]
	return value

    def getTanbLimits(self,xVariableName,selection):

	x = self.getValues(xVariableName,selection)

	y = []
	for xval in x:
	    yselection = xVariableName+"=="+str(xval)+"&&"+selection
	    expLimit = self.getExpLimit(yselection)
	    ylimit = self.getTanbFromLightHpBR(expLimit,yselection)
	    #print "x,y",xval,ylimit
	    y.append(ylimit)

        print "Tanb limits for selection",selection
        for i,xx in enumerate(x):
            print xx,y[i]
	return x,y

    def graphToTanBeta(self,graph,xVariableName,selection,highTanbRegion=True,limitBRtoMin=True):
        # Don't modify the original
        graph = graph.Clone()
        if highTanbRegion:
            print "GraphToTanBeta high tanb region",xVariableName,graph.GetName()
        else:
            print "GraphToTanBeta low tanb region",xVariableName,graph.GetName()
        for i in xrange(0, graph.GetN()):
            xval = graph.GetX()[i]
            yselection = xVariableName+"=="+str(xval)+"&&"+selection
            yval = graph.GetY()[i]
            ylimit = self.getTanbFromLightHpBR(yval,yselection,highTanbRegion)
            graph.SetPoint(i, xval, ylimit)
            print "    ",i, xval, yval, ylimit 
        graph.Sort()

        if limitBRtoMin:
            graph = self.graphToMinTanb(graph,xVariableName,selection,highTanbRegion)
        
        return graph

    def graphToTanBetaCombined(self,graph,xVariableName,selection):
        highTanbGraph = self.graphToTanBeta(graph,xVariableName,selection,highTanbRegion=True)
        lowTanbGraph  = self.graphToTanBeta(graph,xVariableName,selection,highTanbRegion=False)
        return self.mergeGraphs(highTanbGraph,lowTanbGraph)

    def mergeGraphs(self,graph1,graph2):
        graphX = []
        graphY = []

        for i in range(0,graph1.GetN()):
            N = graph1.GetN()
            x = graph1.GetX()[N-1-i]
            y = graph1.GetY()[N-1-i]
            graphX.append(x)
            graphY.append(y)
        graphX.append(0)
        graphY.append(0.5*(graph1.GetY()[0]+graph2.GetY()[0]))
        for i in range(0,graph2.GetN()):
            graphX.append(graph1.GetX()[i]) #intentional, get mass points from graph1
            graphY.append(graph2.GetY()[i])

        N = len(graphY)-1
        for i in range(0,N): # take only first point on limit tanb=1
            j = N-1-i
            if self.isEqual(graphY[j+1],1) and self.isEqual(graphY[j],1):
                graphX.pop()
                graphY.pop()
            else:
                break
                
        doublepoints = []
        for i in range(0,graph1.GetN()):
            j = graph1.GetN()-1-i
            k = graph1.GetN()+i
            if self.isEqual(graphX[j],graphX[k]) and self.isEqual(graphY[j],graphY[k]):
                doublepoints.append(j)
                doublepoints.append(k)
            else:
                break
        #merge last double, remove the rest = rm all but last point
        if len(doublepoints) > 0:
            doublepoints.pop()
        doublepoints = sorted(doublepoints)
        for i in range(0,len(doublepoints)):
            j = len(doublepoints)-1-i
            graphX.pop(doublepoints[j])
            graphY.pop(doublepoints[j])
        
        retGraph = ROOT.TGraph(len(graphX),array('d',graphX),array('d',graphY))
        retGraph.SetFillColor(graph1.GetFillColor())
        retGraph.SetLineWidth(graph1.GetLineWidth())
        retGraph.SetLineStyle(graph1.GetLineStyle())
        retGraph.SetMarkerStyle(graph1.GetMarkerStyle())
        retGraph.SetMarkerSize(graph1.GetMarkerSize())
        return retGraph
    
    def graphToMinTanb(self,graph,xVariableName,selection,highTanbRegion=True):
        graphX = []
        graphY = []
        pointsAtTanb1 = []
        pointBelowTanb1 = 0
        for i in xrange(0, graph.GetN()):
#            print "check x,y",graph.GetX()[i],graph.GetY()[i]
            yval = graph.GetY()[i]
            if yval < 1:
                pointBelowTanb1+=1
            if self.isEqual(yval,1):
                pointsAtTanb1.append(i)
                graphX.append(graph.GetX()[i])
                ymin = self.getMinimumTanb(self.BRvariable,selection+"&&"+xVariableName+"==%s"%graph.GetX()[i])
                graphY.append(ymin)
        if len(pointsAtTanb1) == 0 and pointBelowTanb1 == 0:
            return graph

        if len(pointsAtTanb1) > 0:
            xmin = graph.GetX()[0]
            xmax = graph.GetX()[graph.GetN()-1]
            firstUnExcludedPoint = pointsAtTanb1[len(pointsAtTanb1)-1]+1
#            print "check firstUnExcludedPoint",firstUnExcludedPoint
            if firstUnExcludedPoint < graph.GetN():
                xmax = graph.GetX()[firstUnExcludedPoint]

            x1 = graph.GetX()[firstUnExcludedPoint]
            y1 = graph.GetY()[firstUnExcludedPoint]
            x2 = graph.GetX()[firstUnExcludedPoint+1]
            y2 = graph.GetY()[firstUnExcludedPoint+1]
#            print "check x1,y1,x2,y2",x1,y1,x2,y2
            graph = graph.Clone()
            for i,val in enumerate(pointsAtTanb1):
                graph.RemovePoint(len(pointsAtTanb1)-1 - i)
            
            ymin = self.getMinimumTanb(self.BRvariable,selection+"&&"+xVariableName+"==%s"%graph.GetX()[firstUnExcludedPoint-1])

            # y = ax+b
            b = float(x1*y2 - y1*x2)/(x1-x2)
            a = float(y1-b)/x1
            xmin = (ymin - b)/a

            dx = 0.1
            xs = [xmin-dx,xmin+dx]
            for x in xs:
                y = self.linearFunction(x,x1,y1,x2,y2)
                graphX.append(x)
                if highTanbRegion:
                    if y > ymin:
                        graphY.append(y)
                    else:
                        graphY.append(ymin)
                else:
                    if y <= 1:
                        graphY.append(ymin)
                    else:
                        graphY.append(y)

        for i in xrange(0, graph.GetN()):
            graphX.append(graph.GetX()[i])
            graphY.append(graph.GetY()[i])

        if not highTanbRegion:
            lastUnExcludedPoint = 0
            for i in range(1,graph.GetN()):
                if self.isEqual(-1,graph.GetY()[i]):
                    lastUnExcludedPoint = i - 1
                    break
            xmin = graph.GetX()[lastUnExcludedPoint]
            xmax = graph.GetX()[graph.GetN()-1]
                                                            
            x1 = graph.GetX()[lastUnExcludedPoint-1]
            y1 = graph.GetY()[lastUnExcludedPoint-1]
            x2 = graph.GetX()[lastUnExcludedPoint]
            y2 = graph.GetY()[lastUnExcludedPoint]

            ymin = 1
            # y = ax+b
            b = float(x1*y2 - y1*x2)/(x1-x2)
            a = float(y1-b)/x1
            xmin = (ymin - b)/a
            for i in range(1,len(graphX)):
                if self.isEqual(graphY[i],-1):
                    graphY[i] = 1
                if self.isbetween(xmin,graphX[i-1],graphX[i]):
                    graphX.insert(i,xmin)
                    graphY.insert(i,ymin)
#        print "check ret",graphX,graphY
        retGraph = ROOT.TGraph(len(graphX),array('d',graphX),array('d',graphY))
        retGraph.SetFillColor(graph.GetFillColor())
        retGraph.SetLineWidth(graph.GetLineWidth())
        retGraph.SetMarkerStyle(graph.GetMarkerStyle())
        retGraph.SetMarkerSize(graph.GetMarkerSize())
        return retGraph

    def isbetween(self,x,x1,x2):
        return (x1 < x < x2) or (x2 < x < x1)
            
    def minimumTanbGraph(self,xVariableName,selection):
        xs = self.getValues(xVariableName,selection)
        graphX = []
        graphY = []
        for x in xs:
            y = self.getMinimumTanb(self.BRvariable,selection+"&&"+xVariableName+"==%s"%x)
            graphX.append(x)
            graphY.append(y)
        retGraph = ROOT.TGraph(len(graphX),array('d',graphX),array('d',graphY))
        retGraph.SetName("MinTanb")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(3)
        return retGraph

    def mhLimit(self,higgs,xVariableName,selection,mhMeasurement):

        x = []
        y = []

        mHpStart = 200
        upper_x00 = []
        upper_y00 = []
        if higgs == "mh":
            lower_x00,lower_y00 = self.getLimitsLT(higgs,xVariableName,"tanb",selection+"&&tanb>=30&&"+xVariableName+">=%s"%mHpStart,self.lowerLimit(mhMeasurement))
            upper_x00,upper_y00 = self.getLimitsLT(higgs,xVariableName,"tanb",selection+"&&tanb>=30&&"+xVariableName+">=%s"%mHpStart,self.upperLimit(mhMeasurement))

            for i in range(0,len(lower_x00)):
                j = len(lower_x00) -1 -i
                x.append(lower_x00[j])
                y.append(lower_y00[j])

        tanbStart = 10
        if higgs == "mH" or higgs == "mA":
            tanbStart = 1
        lower_y0,lower_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.lowerLimit(mhMeasurement))
        upper_y0,upper_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.upperLimit(mhMeasurement))

        for i in range(0,len(lower_x0)):
            j = len(lower_x0) -1 -i
            if lower_y0[j] < 30:
                x.append(lower_x0[j])
                y.append(lower_y0[j])
            else:
                if lower_x0[j] <= mHpStart:
                    x.append(lower_x0[j])
                    y.append(lower_y0[j])
            #print "x,y(lower)",lower_x0[j],lower_y0[j]

#        for i in range(0,len(upper_x0)):
#            x.append(upper_x0[i])
#            y.append(upper_y0[i])
#            print "x,y(upper)",upper_x0[i],upper_y0[i]

        if higgs == "mh":
            lower_x,lower_y = self.getLimits(higgs,xVariableName,"tanb",selection,self.lowerLimit(mhMeasurement))
            upper_x,upper_y = self.getLimits(higgs,xVariableName,"tanb",selection,self.upperLimit(mhMeasurement))

            for i in range(0,len(lower_x)):
                if lower_x[i] > lower_x0[0]:
                    x.append(lower_x[i])
                    y.append(lower_y[i])
                    #print "x,y(lower)",lower_x[i],lower_y[i]

            for i in range(0,len(upper_x)):
                j = len(upper_x) -1 -i
                if upper_x[j] > upper_x0[0]:
                    x.append(upper_x[j])
                    y.append(upper_y[j])
                    #print "x,y(upper)",upper_x[j],upper_y[j]

        for i in range(0,len(upper_x0)):
            if len(upper_x00) == 0:
                x.append(upper_x0[i])
                y.append(upper_y0[i])
            else:
                if upper_x0[i] <= mHpStart or upper_y0[i] < 30:
                    x.append(upper_x0[i])
                    y.append(upper_y0[i])
                    #print "x,y(upper)",upper_x0[i],upper_y0[i]

        if higgs == "mh":
            for i in range(0,len(upper_x00)):
                x.append(upper_x00[i])
                y.append(upper_y00[i])
	    x.append(600)
	    y.append(100)
                                                
        if len(x) == 0:
            return None

        if higgs == "mH":
            x.append(0)
            y.append(100)

#        for i in range(0,len(x)):
#            print "m,tanb",x[i],y[i]
        
        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("mhLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
#        retGraph.SetFillColor(ROOT.TColor.GetColor("#ffffcc"))
        retGraph.SetFillColor(7)
        retGraph.SetFillStyle(3008)
        return retGraph

    def getLimitsLT(self,higgs,xVariableName,yVariableName,selection,limit):

        xvalues = self.getValues(xVariableName,selection)

        limits_x = []
        limits_y = []

        for x in xvalues:
            theSelection = selection+"&&"+self.floatSelection(xVariableName+"==%s"%x)
            ymin = self.getMinimum(higgs,theSelection)
            if limit < ymin:
                continue
            ymax = self.getMaximum(higgs,theSelection)
            if limit > ymax:
                continue
            mh_vals  = self.getValues(higgs,theSelection,-1,sort=False)
            y_vals = self.getValues(yVariableName,theSelection,-1,sort=False)

            ys,mh = self.sort(y_vals,mh_vals)
            #print "check ys,mh",x,ys,mh

            y = 0
            for i in range(len(mh)):
                if self.isEqual(mh[i],limit,0.00001):
                    y = ys[i]
                    break
                if i > 0 and mh[i] < limit:
                    y = self.linearFunction(limit,mh[i-1],ys[i-1],mh[i],ys[i])
                    break

            limits_x.append(x)
            limits_y.append(y)

        return limits_x,limits_y
            
    def getLimits(self,higgs,xVariableName,yVariableName,selection,limit):

#        higgs = "mh"
#        higgs = "mH"

        xvalues = self.getValues(xVariableName,selection)

        limits_x = []
        limits_y = []

        for x in xvalues:
            theSelection = selection+"&&"+self.floatSelection(xVariableName+"==%s"%x)
            ymin = self.getMinimum(higgs,theSelection)
            #print "check ymin",ymin,higgs,theSelection
            if limit < ymin:
                continue
            ymax = self.getMaximum(higgs,theSelection)
            #print "check ymax",ymax,higgs,theSelection
            if limit > ymax:
                continue
            mh_vals  = self.getValues(higgs,theSelection,-1,sort=False)
            y_vals = self.getValues(yVariableName,theSelection,-1,sort=False)

            ys,mh = self.sort(y_vals,mh_vals)

            y = 0
            for i in range(len(mh)):
                if self.isEqual(mh[i],limit,0.00001):
                    y = ys[i]
                    break
                if i > 0 and mh[i] > limit:
                    y = self.linearFunction(limit,mh[i-1],ys[i-1],mh[i],ys[i])
                    break

            limits_x.append(x)
            limits_y.append(y)
            #print "check limit,x,y",limit,x,y
        #print "OUT",limits_x,limits_y
        return limits_x,limits_y

    def sort(self,x0,y0):
        # sorting by x
        x = x0
        y = y0
        for i in range(0,len(x)-1):
            for j in range(i+1,len(x)):
                if x[i] > x[j]:
                    x = self.swap(x,i,j)
                    y = self.swap(y,i,j)
        return x,y

    def swap(self,x,i,j):
        tmp = x[i]
        x[i] = x[j]
        x[j] = tmp
        return x
        
    def lowerLimit(self,mhMeasurement):
        value,error = self.getmh(mhMeasurement)
        return value - error

    def upperLimit(self,mhMeasurement):
        value,error = self.getmh(mhMeasurement)
        return value + error

    def getmh(self,mhMeasurement):
        value  =-1
        error1 = 0
        error2 = 0
#        mh_re = re.compile("(?P<value>\S+)\+-(?P<error1>\S+)\+-(?P<error2>\S+)")
        mh_re = re.compile("(?P<value>\S+)\+-(?P<error1>\S+)")
        match = mh_re.search(mhMeasurement)
        if match:
            value  = float(match.group("value"))
            error1 = float(match.group("error1"))
#            error2 = float(match.group("error2"))
        #print "mh value,error",value,error1+error2
        return value,error1+error2 # errors to be added linearly
                                                                                                                            
    def clean(self,graph):
        graph = graph.Clone()

        rmPoints = []
        for i in xrange(0, graph.GetN()):
            yval = graph.GetY()[i]
            print graph.GetX()[i],yval
            if yval < 0:
                rmPoints.append(i)
        for i in rmPoints:
            graph.RemovePoint(i)
        return graph

    def graphToMa(self,graph):
        for i in xrange(0, graph.GetN()):
            mHp = graph.GetX()[i]
            tanb = graph.GetY()[i]
            selection = "mHp=="+str(mHp)+"&&tanb=="+str(tanb)+"&&"+self.selection
            mA = self.get("mA","tanb",selection)
            graph.SetPoint(i, mA, tanb)

    def getGraph(self,xVariable,yVariable,selection):
        """
        xs = self.getValues(xVariable,selection)
        ys = []
        for x in xs:
            ys.append(self.getOLD(yVariable,selection+"&&"+xVariable+"==%s"%x))
            
        retGraph = ROOT.TGraph(len(xs),array('d',xs),array('d',ys))
        return retGraph
        """
        #print "check getGraph",xVariable,yVariable,selection
        graph = ROOT.TGraph()
        self.tree.Draw(yVariable+":"+xVariable,self.floatSelection(selection))
        graph = ROOT.gPad.GetPrimitive("Graph")
        return graph
        
    def getExpLimit(self,selection):
	selections = selection.split("&&")

	mHp_re = re.compile("mHp==(?P<value>(\d+))")

	massSelection = ""
	for s in selections:
	    match = mHp_re.search(s)
	    if match:
		if match.group("value") in self.expLimit.keys():
		    return float(self.expLimit[match.group("value")])
		else:
		    print "No explimit for mass",match.group("value"),"set, exiting.."
		    sys.exit()
	print "No mass selection in",selection,", cannot determine explimit. Exiting.."
	sys.exit()

    def addExperimentalBRLimit(self,mass,limit):
	self.expLimit[str(int(mass))] = str(limit)

    def excluded(self,obsGraph,name):

        excluded = ROOT.TGraph(obsGraph)
        excluded.SetName(name)
        excluded.SetFillColor(ROOT.kGray)
        excluded.SetPoint(excluded.GetN(), -1, 1)
        excluded.SetPoint(excluded.GetN(), -1, 100)
        if not obsGraph.GetY()[0] == 100:
            excluded.SetPoint(excluded.GetN(), obsGraph.GetX()[0], 100)
        excluded.SetPoint(excluded.GetN(), obsGraph.GetX()[0], obsGraph.GetY()[0])
        excluded.SetFillStyle(3354)
        excluded.SetLineWidth(0)
        excluded.SetLineColor(ROOT.kWhite)

        N = excluded.GetN() 
        for i in range(N):
            j = N - i - 1
            if j > 0 and excluded.GetY()[j] == 100 and excluded.GetY()[j-1] == 100 and excluded.GetX()[j-1] > 0:
                excluded.RemovePoint(j-1)

#	for i in range(N):
#	    print "check excluded",i,excluded.GetX()[i],excluded.GetY()[i]
        return excluded

    def passed(self,selection):
        epsilon = 0.001
        p = True
        selections = selection.split("&&")
        for s in selections:
            sele_re = re.compile("(?P<variable>(\S+))==(?P<value>(-*\S+))")
            match = sele_re.search(s) 
            if match:
                p = p and self.isEqual(self.getValue(match.group("variable")),float(match.group("value")),epsilon)
            if not p:   
                return False
        return p

    def isEqual(self,double1,double2,epsilon=0.001):
        if not double1 == 0:
            return (abs((double1 - double2)/double1) < epsilon)
        if not double2 == 0:
            return (abs((double1 - double2)/double2) < epsilon)
        return True
    
    def getValues(self,variable,selection,roundValues=0,sort=True):
        #print "check",variable,selection
        if not self.selection == "" and not selection == "":
            selection = self.selection+"&&"+selection
        values = []
####        graph = self.getGraph("tanb",variable,self.floatSelection(selection))
        if variable == "tanb":
            graph = self.getGraph("mHp",variable,selection)
        else:
            graph = self.getGraph("tanb",variable,self.floatSelection(selection))
        for i in range(0,graph.GetN()):
            value = graph.GetY()[i]
            if roundValues >= 0:
                value = round(value,roundValues)
            if not value in values:
                values.append(value)
        if sort:
            return sorted(values)
        return values
        """
        Values = []
        nev = self.tree.GetEntries()
        for i in range(nev):
            self.tree.GetEvent(i)
            if self.passed(selection):
                value = self.getValue(variable)
                if roundValues >= 0:
                    value = round(value,roundValues)
                if not value in values:
                    values.append(value)
	return sorted(values)
        """
    def getMinimum(self,variable,selection):
        min = 9999.
#        print "check getMinimum",variable,selection,self.getValues(variable,selection,roundValues=-1)
        for v in self.getValues(variable,selection,roundValues=-1):
            if v < min and v > 0:
                min = v
        return min

    def getMinimumTanb(self,variable,selection):
        min  = 9999.
        tanb = -1

        tanbs = self.getValues("tanb",selection,roundValues=1)
        for tgb in tanbs:
            value = self.get("tanb",variable,selection+"&&tanb==%s"%tgb)
            if value < min and value > 0:
                min = value
                tanb = tgb
        return tanb
    
    def getXVariableAtMinimumTanb(self,xvariable,yvariable,selection):
        min  = 9999.
        tanb = -1
        var = -1
        tanbs = self.getValues("tanb",selection,roundValues=1)
        xvars = self.getValues(xvariable,selection,roundValues=1)
        for tgb in tanbs:
            for xvar in xvars:
                varSelection = selection+"&&tanb==%s"%tgb
                varSelection+= "&&"+xvariable+"==%s"%xvar
                value = self.get(yvariable,"tanb",varSelection)
                if value < min:
                    min = value
                    tanb = tgb
                    var  = xvar
        return xvar
                                                                                        
    def getMaximum(self,variable,selection):
        max = -9999.
#        print "check getMaximum",len(self.getValues(variable,selection,roundValues=-1)),variable,selection,self.getValues(variable,selection,roundValues=-1)
        for v in self.getValues(variable,selection,roundValues=-1):
            if v > max:
                max = v
        return max

    def getMinTanbInterpolation(self,xvariable,xvalue,yvariable,selection):
        x1 = self.lowerPoint(xvariable,xvalue,selection)
        x2 = self.higherPoint(xvariable,xvalue,selection)

        y1 = self.getMinimumTanb(yvariable,selection+"&&"+xvariable+"==%s"%x1)
        y2 = self.getMinimumTanb(yvariable,selection+"&&"+xvariable+"==%s"%x2)
#        print "check getMinTanbInterpolation",x1,y1,x2,y2
        return self.linearFunction(xvalue,x1,y1,x2,y2)

    def linearFunction(self,x,x1,y1,x2,y2):
        # y = ax+b
        b = float(x1*y2 - y1*x2)/(x1-x2)
        a = float(y1-b)/x1

        return a*x + b

    
    def Print(self,variable="",selection=""):
        if variable == "":
            #print branch names
            result_re = re.compile(self.program+"_results")

            keys = self.fIN.GetListOfKeys()
            obj = keys.First()
            while obj:
                print "  ",obj.GetName()
                match = result_re.search(obj.GetName())
                if match:
                    tree = self.fIN.Get(match.group(0))
                    for branch in tree.GetListOfBranches():
                        print "    ",branch.GetName()
                obj = keys.After(obj)
            print
        else:
            #print stored variable values
            print "Variable  ",variable
            print "Selection ",selection
            tanbs = self.getValues("tanb",selection,roundValues=-1)
            print "tanb      ",variable
            for tanb in tanbs:
                sele = self.floatSelection(selection+"&&tanb==%s"%tanb)
                value = self.getValues(variable,sele,roundValues=-1)
                tanbstr = str(tanb)
                while len(tanbstr) < 10:
                    tanbstr += " "
                print tanbstr,value[0]

    def lowerPoint(self,variable,variableRef,selection):

	values = self.getValues(variable,selection,roundValues=-1)
#        print "      check lowerpoint",variable,variableRef,selection,values
        returnValue = 0
        for v in values:
            if v == variableRef:
                return v
            if v > variableRef:
                return returnValue
            returnValue = v
        return 0

    def higherPoint(self,variable,variableRef,selection):

        values = self.getValues(variable,selection,roundValues=-1)
#        print "      check higherPoint",variable,variableRef,selection,values
        returnValue = 0
        if variableRef < values[0]:
            return 0
        for v in values:
            if v > variableRef:
                return v
        return 0

    def interpolate(self,variable,tanb,selection):
	#return self.linearInterpolation(variable,tanb,selection)
        return self.tgraphInterpolation(variable,tanb,selection)
    
    def tgraphInterpolation(self,variable,tanb,selection):
        graph = self.getGraph("tanb",self.BRvariable,selection)
        return graph.Eval(tanb,None,"S")
    
    def linearInterpolation(self,variable,tanb,selection):
	tanb1 = self.lowerPoint("tanb",tanb,selection)
	tanb2 = self.higherPoint("tanb",tanb,selection)
        
	if tanb1 == 0 or tanb2 == 0 or tanb1 > tanb or tanb2 < tanb:
	    return 0

	fraction = 1
        if tanb1 < tanb2:
            fraction = (tanb - tanb1)/(tanb2 - tanb1)

	value1 = self.getOLD(variable,selection+"&&tanb=="+str(tanb1))
	value2 = self.getOLD(variable,selection+"&&tanb=="+str(tanb2))
    
	value = value1 + (value2 - value1)*fraction
	return value

    def linearBRInterpolation(self,variable,target,min,max,selection):
#        print "check linearBRInterpolation",variable,target,min,max,selection
#        print "      self.getMinimum(variable,selection)",self.getMinimum(variable,selection)
#        print "      self.getMaximum(variable,selection)",self.getMaximum(variable,selection)
#        print "tanbs",len(self.getValues("tanb",selection,roundValues=-1)),self.getValues("tanb",selection,roundValues=-1)
#        print variable,len(self.getValues(variable,selection,roundValues=-1))
        if min >= max:
	    tanbs = self.getValues("tanb",selection,roundValues=-1)
            newMin = 999
            newMax = tanbs[len(tanbs)-1]
            values = self.getValues(variable,selection,roundValues=-1)
            for i in range(0,len(tanbs)-1):
#                if tanb < 10:
#                    continue
#                value = self.getOLD(variable,selection+"&&tanb=="+str(tanb))
#                print "tanb,value",tanbs[i],values[i],min,max
                if values[i] < target:
                    newMin = tanbs[i]
                else:
                    newMax = tanbs[i]
                    break
            min = newMin
            max = newMax
#	print "check min,max",min,max
        if target < self.getMinimum(variable,selection):
            print "Warning,",variable,"target",target,"< minimum possible value",self.getMinimum(variable,selection),selection
            return 1
        if target > self.getMaximum(variable,selection):
            print "Warning,",variable,"target",target,"> maximum possible value",self.getMaximum(variable,selection),selection
            if max < 10:
                return -1
            return 100
        if max <= self.getMinimumTanb(variable,selection) and target > self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)):
            print "Warning,",variable,"target",target,"> maximum possible value (at tanb<",self.getMinimumTanb(variable,selection),")",self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)),selection
            return -1
        
        x1 = float(min)
        y1 = self.interpolate(variable,x1,selection)
        x2 = float(max)
        y2 = self.interpolate(variable,x2,selection)
#        print "    check linInt x1,y1,x2,y2",x1,y1,x2,y2
        if x1 < 1 and x2 < 1:
            return 1
        #low tanb region br increases as tanb decreases. To prevent patological oscillation which never converges

        # y = ax+b
        b = float(x1*y2 - y1*x2)/(x1-x2)
        a = float(y1-b)/x1
        x = (target - b)/a
#        print "    check x",x
        newx1 = self.lowerPoint("tanb",x,selection)
        newx2 = self.higherPoint("tanb",x,selection)
#        print "    check newx1,newx2 a",newx1,newx2
        if x > self.getMaximum("tanb",selection):
            newx1 = x2
            newx2 = self.getMaximum("tanb",selection) - 1

        if x < self.getMinimum("tanb",selection):
            newx1 = self.getMinimum("tanb",selection)
            newx2 = newx1 + 0.1

        if x < 1:
#            print "    x < 1"
            return 1
#        print "    check newx1,newx2 b",newx1,newx2
#        if int(10*newx1) == int(10*x1) and int(10*newx2) == int(10*x2):
        if self.isEqual(newx1,x1) and self.isEqual(newx2,x2):
            return x
        else:
            return self.linearBRInterpolation(variable,target,newx1,newx2,selection)
        
    def getTanbFromLightHpBR(self,targetBR,selection,highTanbRegion=True):
	# for light H+
        tanbmin = 2
        tanbmax = 5
        if highTanbRegion:
            tanbmin = 10
            tanbmax = 20
        return self.linearBRInterpolation(self.BRvariable,targetBR,tanbmin,tanbmax,self.floatSelection(selection))
            
    def getCutValue(self,variable,selection):
	var_re = re.compile(variable+"==(?P<value>(\d+))")
	for s in selection.split("&&"):
	    match = var_re.search(s)
	    if match:
		return float(match.group("value"))
	return -1
        
    
def usage():
    print
    print "### Usage:  ",sys.argv[0],"<root file>"
    print "### Example:",sys.argv[0],"mhmax.root"
    print
    sys.exit()

def test():
    print "BRXSDatabase test program"

    if len(sys.argv) == 1:
	usage()

    ROOT.gROOT.SetBatch(True)
    
    root_re = re.compile("(?P<rootfile>(\S*\.root))")
    match = root_re.search(sys.argv[1])
    if match:

	db = BRXSDatabaseInterface(match.group(0))
#	db.Print()
#        db.Print(variable="BR_tHpb*BR_Hp_taunu",selection="mHp==155&&mu==200&&Xt==2000&&m2==200")
#        db.Print(variable="BR_Hp_taunu",selection="mHp==155&&mu==200&&Xt==2000&&m2==200")

#	db.setSelection("mu==500")
        db.mhLimit("mh","mHp","mu==200","125.9+-3.0")

        """
        x = array('d',[100.0,110,120.0,140.0,150.0,155.0,160.0,160.0,155.0,150.0,140.0,120.0,100.0])
        y = array('d',[7.4,7.4,5.93285611233,4.08070975404,2.74869717846,1.0,1.0,1.0,1.0,1.0,1.7449304635,2.63037522267,3.28961963754])
        graph1 = ROOT.TGraph(len(x),x,y)
#        graph = db.graphToMinTanb(graph1,"mHp","mu==200&&Xt==2000&&m2==200",highTanbRegion=False)
        x = array('d',[100.0,110,120.0,140.0,150.0,155.0,160.0,160.0,155.0,150.0,140.0,120.0,100.0])
        y = array('d',[7.4,7.4,9.23,13.4,19.2,25.09,35.37,67.65,51.08,37.925,27.508,20.79,16.4])
        graph2 = ROOT.TGraph(len(x),x,y)
        graph = db.mergeGraphs(graph1,graph2)
#        for i in range(0,len(x)):
#            print i,x[i],y[i]
#        print "merged"
#        for i in range(0,graph.GetN()):
#            print i,graph.GetX()[i],graph.GetY()[i]
        """
        """
	print "Float selection",db.selection,db.floatSelection(db.selection)
        print "Min tanb",db.getMinimumTanb("BR_tHpb","mHp==150")
#        print "mA for tanb==25&&mHp==150",db.get("mA","tanb==25&&mHp==150")
#	print "tanb values for mHp==150",db.getValues("tanb","mHp==150",1)
#        print "BR_tHpb values for mHp==150",db.getValues("BR_tHpb","mHp==150")
#        print "BR_tHpb for tanbx10==94&&mHp==120",db.get("BR_tHpb","tanbx10==93&&mHp==120")
        print "BR_tHpb for tanb==9.4&&mHp==120",db.get("BR_tHpb","tanb","tanb==9.4&&mHp==120")
        print "BR_tHpb for tanb==9.5&&mHp==120",db.get("BR_tHpb","tanb","tanb==9.5&&mHp==120")
        print "BR_tHpb for tanb==9.6&&mHp==120",db.get("BR_tHpb","tanb","tanb==9.6&&mHp==120")
        print "BR_tHpb for tanb==9.6&&mHp==120",db.getOLD("BR_tHpb","tanb==9.6&&mHp==120")
#        for tanb in db.getValues("tanb","mHp==150",1):
        for i in range(0,91):
            tanb = 10 - 0.1*i
            print "BR_tHpb*BR_Hp_taunu",tanb,db.get("tanb","BR_tHpb*BR_Hp_taunu","tanb==%s&&mHp==150"%tanb)
        print "Maximum",db.getMaximum("BR_tHpb*BR_Hp_taunu","mHp==150&&tanb<7.4")
        
        print "BR_tHpb for tanb==25&&mHp==150",db.get("BR_tHpb","tanb==25&&mHp==150")
	print "BR_Hp_taunu for tanb==25&&mHp==150",db.get("BR_Hp_taunu","tanb==25&&mHp==150")
        print "BR_tHpb*BR_Hp_taunu for tanb==25&&mHp==150",db.get("BR_tHpb*BR_Hp_taunu","tanb==25&&mHp==150")
        print "BR_tHpb*BR_Hp_taunu for tanb==25&&mHp==150",db.get("BR_tHpb*BR_Hp_taunu","tanb==25&&mHp==150")

#	print "interpolate tanb=22.5",db.interpolate("BR_tHpb*BR_Hp_taunu",22.5,"mu==200&&mHp==150&&Xt==-2000")
	
	print "tanb for 0.013, mHp==150",db.getTanbFromLightHpBR(0.013,"mHp==150&&Xt==-2000")
	print "tanb for 0.013, mHp==150",db.getTanbFromLightHpBR(0.013,"mHp==150&&Xt==-1000")
        print "tanb for 0.013, mHp==150",db.getTanbFromLightHpBR(0.013,"mHp==150&&Xt==0")
        print "tanb for 0.013, mHp==150",db.getTanbFromLightHpBR(0.013,"mHp==150&&Xt==1000")
        print "tanb for 0.013, mHp==150",db.getTanbFromLightHpBR(0.013,"mHp==150&&Xt==2000")


	db.addExperimentalBRLimit(150,0.013)
	print "Xt,tanb",db.getTanbLimits("Xt","mu==200&&mHp==150")
        """
if __name__ == "__main__":
    test()
