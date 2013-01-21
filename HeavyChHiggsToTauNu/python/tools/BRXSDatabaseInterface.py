#!/usr/bin/env python

import sys
import re
from array import array

import ROOT

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
        
        for i in xrange(0, graph.GetN()):
            xval = graph.GetX()[i]
            yselection = xVariableName+"=="+str(xval)+"&&"+selection
            yval = graph.GetY()[i]
            ylimit = self.getTanbFromLightHpBR(yval,yselection,highTanbRegion)
            graph.SetPoint(i, xval, ylimit)

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
            if firstUnExcludedPoint < graph.GetN():
                xmax = graph.GetX()[firstUnExcludedPoint]

            x1 = graph.GetX()[firstUnExcludedPoint]
            y1 = graph.GetY()[firstUnExcludedPoint]
            x2 = graph.GetX()[firstUnExcludedPoint+1]
            y2 = graph.GetY()[firstUnExcludedPoint+1]

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
    
    def getValues(self,variable,selection,roundValues=0):
        if not self.selection == "" and not selection == "":
            selection = self.selection+"&&"+selection
        values = []
        graph = self.getGraph("tanb",variable,selection)
        if variable == "tanb":
            graph = self.getGraph("mHp",variable,selection)
        for i in range(0,graph.GetN()):
            value = graph.GetY()[i]
            if roundValues >= 0:
                value = round(value,roundValues)
            if not value in values:
                values.append(value)
        return sorted(values)
        """
        values = []
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
        for v in self.getValues(variable,selection,roundValues=-1):
            if v < min:
                min = v
        return min

    def getMinimumTanb(self,variable,selection):
        min  = 9999.
        tanb = -1

        tanbs = self.getValues("tanb",selection,roundValues=1)
        for tgb in tanbs:
            value = self.get("tanb",variable,selection+"&&tanb==%s"%tgb)
            if value < min:
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
        for v in self.getValues(variable,selection,roundValues=-1):
            if v > max:
                max = v
        return max

    def getMinTanbInterpolation(self,xvariable,xvalue,yvariable,selection):
        x1 = self.lowerPoint(xvariable,xvalue,selection)
        x2 = self.higherPoint(xvariable,xvalue,selection)

        y1 = self.getMinimumTanb(yvariable,selection+"&&"+xvariable+"==%s"%x1)
        y2 = self.getMinimumTanb(yvariable,selection+"&&"+xvariable+"==%s"%x2)

        return self.linearFunction(xvalue,x1,y1,x2,y2)

    def linearFunction(self,x,x1,y1,x2,y2):
        # y = ax+b
        b = float(x1*y2 - y1*x2)/(x1-x2)
        a = float(y1-b)/x1

        return a*x + b

    
    def Print(self):
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



    def lowerPoint(self,variable,variableRef,selection):

	values = self.getValues(variable,selection,roundValues=-1)

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
        if target < self.getMinimum(variable,selection):
            print "Warning,",variable,"target",target,"< minimum possible value",self.getMinimum(variable,selection),selection
            return 1
        if target > self.getMaximum(variable,selection):
            print "Warning,",variable,"target",target,"> maximum possible value",self.getMaximum(variable,selection),selection
            return 1
        if max <= self.getMinimumTanb(variable,selection) and target > self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)):
            print "Warning,",variable,"target",target,"> maximum possible value (at tanb<",self.getMinimumTanb(variable,selection),")",self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)),selection
            return -1
        
        x1 = float(min)
        y1 = self.interpolate(variable,x1,selection)
        x2 = float(max)
        y2 = self.interpolate(variable,x2,selection)

        if x1 < 1 and x2 < 1:
            return 1
        #low tanb region br increases as tanb decreases. To prevent patological oscillation which never converges

        # y = ax+b
        b = float(x1*y2 - y1*x2)/(x1-x2)
        a = float(y1-b)/x1
        x = (target - b)/a

        newx1 = self.lowerPoint("tanb",x,selection)
        newx2 = self.higherPoint("tanb",x,selection)
        if x > self.getMaximum("tanb",selection):
            newx1 = x2
            newx2 = self.getMaximum("tanb",selection) - 1

        if x < self.getMinimum("tanb",selection):
            newx1 = self.getMinimum("tanb",selection)
            newx2 = newx1 + 0.1

        if int(10*newx1) == int(10*x1) and int(10*newx2) == int(10*x2):
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
        return self.linearBRInterpolation(self.BRvariable,targetBR,tanbmin,tanbmax,selection)
            
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
    print "BRXSDatabase test"

    if len(sys.argv) == 1:
	usage()

    ROOT.gROOT.SetBatch(True)
    
    root_re = re.compile("(?P<rootfile>(\S*\.root))")
    match = root_re.search(sys.argv[1])
    if match:

	db = BRXSDatabaseInterface(match.group(0))
#	db.Print()
	db.setSelection("mu==200&&Xt==2000&&m2==200")

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
