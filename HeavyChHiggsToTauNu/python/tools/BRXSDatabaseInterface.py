#!/usr/bin/env python

import sys
import re
from array import array
import math

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kError

uncert_missing1loopEW  = 0.05
uncert_missing2loopQCD = 0.02
uncert_deltab          = 0.03
uncert_missing_HO_tt   = 0.03

class BRXSDatabaseInterface:
    def __init__(self,rootfile, silentStatus=False):
        self.silentStatus = silentStatus
        if not self.silentStatus:
            print "BRXSDatabaseInterface: reading file",rootfile
        self.rootfile  = rootfile
        self.fIN       = ROOT.TFile.Open(rootfile)
	self.program   = "FeynHiggs"
	self.selection = ""

        self.BRvariable= "BR_tHpb*BR_Hp_taunu"

	self.expLimit  = {}

	self.tree      = self.fIN.Get(self.program+"_results")

	self.variables = []
	self.names     = []
	self.variableDict = {}

	branches =  self.tree.GetListOfBranches()

    	for branch in branches:
	    #print branch.GetName()
            variable = array('d',[0.])
            branch.SetAddress(variable)
            self.variables.append(variable)
            self.names.append(branch.GetName())
            self.variableDict[branch.GetName()] = variable

    def __delete__(self):
        self.close()

    def close(self):
        if self.fIN != None:
            self.fIN.Close()
        self.fIN = None

    def getTheorUncert(self,graph,xVariable,selection,pm):

        sign = 1
        if pm == "-":
            sign = -1

        thvars = []
        for v in self.BRvariable.split("*"):
            if "BR" in v or "xsec" in v:
                thvars.append(v)

        xnew = []
        ynew = []

        print "Graph-------------------------------- obs %s1sigma theor"%pm

        masses = self.expLimit.keys()
        masses_int = []
        for m in masses:
            masses_int.append(int(m))
        for m in sorted(masses_int):
            modelIndependentLimit = float(self.expLimit[str(m)])

            tanb = graph.Eval(m)

            if m < 175 and tanb < 1:
                mintanb = self.getMinimumTanb(self.BRvariable,selection+"&& mHp==%s"%m)
                tanb = mintanb

            uncert = 0
            for v in thvars:
                if "xsec" in v:
####                    uncert += self.xsecUncert(xVariable,"tanb",v,m,tanb,pm)
                    uncert += self.xsecUncertOrig(xVariable,"tanb",v,m,tanb,pm)
                else:
                    uncert += self.brUncert(xVariable,"tanb",v,m,tanb,pm)
####                    if v == "BR_tHpb":
####                        uncert += uncert_missing_HO_tt # this uncert is moved to datacards 12122014/SL

            modelIndependentLimit = modelIndependentLimit*(1+sign*uncert)

            xnew.append(m)
            ynew.append(modelIndependentLimit)
        newGraph = ROOT.TGraph(len(xnew),array('d',xnew),array('d',ynew))
        newGraph.SetLineWidth(2)
        newGraph.SetLineStyle(9)
        #print "ThUncertGraph"                                                                                                                         
        #self.PrintGraph(newGraph)                                                                                                                     
        return newGraph

    ## Returns the relative uncertainty on the theoretical cross section
    def xsecUncert(self,xaxisName,yaxisName,v,x,y,pm):

        uncert = uncert_deltab
        tmpgraph = self.getGraph(yaxisName,"tHp_xsec","%s == %s"%(xaxisName,x))
        sigma = tmpgraph.Eval(y)
        tmpgraph.Delete()

        if pm == "+":
            xsecname = "tHp_xsec_plusErr"
        else:
            xsecname = "tHp_xsec_minusErr"

        tmpgraph = self.getGraph(yaxisName,xsecname,"%s == %s"%(xaxisName,x))
        sigma_prime = tmpgraph.Eval(y)
        tmpgraph.Delete()

        uncert += abs(sigma_prime - sigma) / sigma
        #print "xsec",sigma_prime,sigma,x,y,uncert                                                                                                     
        return uncert

    def xsecUncertOrig(self,xaxisName,yaxisName,v,x,y,pm):

        self.savecopy = self.tree
        self.tree = self.fIN.Get("LHCHXSWG_results")
        if self.tree == None:
            raise Exception("Cannot find tree for cross section uncertainties in root file!")

        uncert = uncert_deltab
        tmpgraph = self.getGraph(yaxisName,"tHp_xsec","%s == %s"%(xaxisName,x))
        sigma = tmpgraph.Eval(y)

        if pm == "+":
            xsecname = "tHp_xsec_plusErr"
        else:
            xsecname = "tHp_xsec_minusErr"

        tmpgraph = self.getGraph(yaxisName,xsecname,"%s == %s"%(xaxisName,x))
        sigma_prime = tmpgraph.Eval(y)
        tmpgraph.Delete()

        uncert += sigma_prime / sigma

        self.tree = self.savecopy
        return uncert
    
    ## Returns a dictionary of the relative uncertainties on the theoretical branching fraction v
    # \param xaxisName  name of the x-axis (e.g. "mHp")
    # \param yaxisName  name of the y-axis (e.g. "tanb")
    # \param v          list of branchings (e.g. ["BR_Hp_taunu"])
    # \param x          value for x variable (e.g. "200")
    # \param y          value for y variable (e.g. "20")
    # \param linearSummation  sum uncertainties linearly if true, otherwise squared sum
    # \param silentStatus  skip printing messages if true
    # \return Returns a dictionary of label/relative uncert. value pairs
    def brUncertLight(self,xaxisName,yaxisName,v,x,y,linearSummation=True,silentStatus=True):
        myVertices = []
        if not isinstance(v, list):
            myVertices.append(v)
        else:
            myVertices = v[:]
        # Obtain uncertainty for t->bH+ branching and value for the branching
        myTBHBrUncert = self._calcBrUncert(xaxisName,yaxisName,["BR_tHpb"],x,y,linearSummation,silentStatus)
        tmpgraph = self.getGraph(yaxisName,"BR_tHpb","%s == %s"%(xaxisName,x))
        br_TBH = tmpgraph.Eval(y)
        tmpgraph.Delete()
        # Obtain uncertainty for H+ branching and values for branching fractions
        myHplusBrUncert = self._calcBrUncert(xaxisName,yaxisName,v,x,y,linearSummation,silentStatus)
        br_Hp_i = {}
        for vtx in myVertices:
            tmpgraph = self.getGraph(yaxisName,vtx,"%s == %s"%(xaxisName,x))
            br_Hp_i[vtx] = tmpgraph.Eval(y)
            tmpgraph.Delete()
        # Initialize uncertainty list
        myUncertainties = {}
        # Calculate uncertainty for TBH i.e. multiply the obtained Delta_TBH by sqrt(sum(br_Hp_i^2))
        myFactor = 0.0
        for vtx in myVertices:
            myFactor += br_Hp_i[vtx]**2
        myFactor = math.sqrt(myFactor)
        myTBHUncert = myFactor*myTBHBrUncert[myTBHBrUncert.keys()[0]]
        # Calculate uncertainty for H+ branchings i.e. multiply the obtained Delta_Hp_i by Br_TBH)
        if len(v) > 1:
            raise Exception("Multiple H+ branchings not supported at the moment for light H+")
        for k in myHplusBrUncert.keys():
            a = br_TBH*myHplusBrUncert[k]
            if linearSummation:
                myUncertainties[k] = a + myTBHUncert
            else:
                myUncertainties[k] = math.sqrt(a**2 + myTBHUncert**2)
        # Return result
        return myUncertainties

    ## Returns a dictionary of the relative uncertainties on the theoretical branching fraction v
    # \param xaxisName  name of the x-axis (e.g. "mHp")
    # \param yaxisName  name of the y-axis (e.g. "tanb")
    # \param v          list of branchings (e.g. ["BR_Hp_taunu"])
    # \param x          value for x variable (e.g. "200")
    # \param y          value for y variable (e.g. "20")
    # \param linearSummation  sum uncertainties linearly if true, otherwise squared sum
    # \param silentStatus  skip printing messages if true
    # \return Returns a dictionary of label/relative uncert. value pairs
    def brUncertHeavy(self,xaxisName,yaxisName,v,x,y,linearSummation=True,silentStatus=True):
        return self._calcBrUncert(xaxisName,yaxisName,v,x,y,linearSummation,silentStatus)

    ## Returns a dictionary of the relative uncertainties on the theoretical branching fraction v
    # \param xaxisName  name of the x-axis (e.g. "mHp")
    # \param yaxisName  name of the y-axis (e.g. "tanb")
    # \param v          list of branchings (e.g. ["BR_Hp_taunu"])
    # \param x          value for x variable (e.g. "200")
    # \param y          value for y variable (e.g. "20")
    # \param linearSummation  sum uncertainties linearly if true, otherwise squared sum
    # \param silentStatus  skip printing messages if true
    # \return Returns a dictionary of label/relative uncert. value pairs
    def _calcBrUncert(self,xaxisName,yaxisName,v,x,y,linearSummation=True,silentStatus=True):
        myVertices = []
        if not isinstance(v, list):
            myVertices.append(v)
        else:
            myVertices = v[:]
        
        # Make list of branching fraction relative uncertainties
        myBrUncertaintySources = {}
        myBrUncertaintySources["MissingOneLoopEW"] = uncert_missing1loopEW
        myBrUncertaintySources["MissingTwoLoopQCD"] = uncert_missing2loopQCD
        myBrUncertaintySources["DeltaBCorrections"] = uncert_deltab

        # Obtain theoretical branching fractions for vertices
        br_i = {}
        for vtx in myVertices:
            tmpgraph = self.getGraph(yaxisName,vtx,"%s == %s"%(xaxisName,x))
            br_i[vtx] = tmpgraph.Eval(y)
            tmpgraph.Delete()
        
        # Obtain sum of Br of non-considered processes
        br_other = 1.0
        for vtx in myVertices:
            br_other -= br_i[vtx]

        # Obtain decay width (Gamma) for label v
        gamma_i = {}
        for vtx in myVertices:
            gamma_v = vtx.replace("BR","GAMMA")
            tmpgraph = self.getGraph(yaxisName,gamma_v,"%s == %s"%(xaxisName,x))
            gamma_i[vtx] = tmpgraph.Eval(y)
            tmpgraph.Delete()
            # Calculate total width
            gammatot = gamma_i[vtx]/br_i[vtx]

        # Use error propagation on Br_i = (Gamma_i) / (Gamma_i + Gamma_other)
        # I.e. vary Gamma_i, ..., and Gamma_other
        myResult = {}
        for v in myVertices:
            myTotalUncertainty = 0.0
            # Obtain uncertainty for B_i's; B_other = 1-B_i's 
            for k in myBrUncertaintySources.keys():
                myUncertainties = []
                # Add uncertainty from B_i's
                for vsub in myVertices:
                    myValue = myBrUncertaintySources[k]
                    if vtx == vsub:
                        myValue *= br_i[vtx] * (1.0 - br_i[vtx])
                    else:
                        myValue *= br_i[vtx] * br_i[vsub]
                    myUncertainties.append(myValue)
                    #print "***",vtx,vsub,myValue,k
                # Add uncertainty from other Br's
                myStatus = True
                if vtx == "BR_tHpb" and k == "DeltaBCorrections":
                    myStatus = False
                if myStatus:
                    # Do not add delta_b corrections for t->bW (== 1-Br(t->bH+))
                    myValue = myBrUncertaintySources[k]
                    myValue *= br_i[vtx] * br_other
                    myUncertainties.append(myValue)
                    #print "***",vtx,"other",myValue,k
                # Calculate total uncertainty
                myUncert = 0.0
                for a in myUncertainties:
                    if linearSummation:
                        myUncert += a
                    else:
                        myUncert += a**2
                if not linearSummation:
                    myUncert = math.sqrt(myUncert)
                    myResult["%s_%s"%(vtx,k)] = myUncert
                else:
                    myTotalUncertainty += myUncert
            if linearSummation:
                myResult["%s"%(vtx)] = myTotalUncertainty
        # Print info
        if not silentStatus:
            print "         ** Br uncertainties for %s=%s, %s=%s, %s:"%(xaxisName,x,yaxisName,y, self.rootfile)
            for k in myResult.keys():
                print "       ** Br uncert [%s] = %f"%(k, myResult[k])
        # Return dictionary with results
        return myResult


    #def brUncert2(self,xaxisName,yaxisName,v,w,x,y,pm):
        ## usage: uncert = self.brUncert2("mHp","tanb","BR_Hp_taunu","BR_Hp_tb",Hp_mass,tanb,"+")

        #gamma_uncert = uncert_missing1loopEW+uncert_missing2loopQCD+uncert_deltab

        ##### first Gamma
        #tmpgraph = self.getGraph(yaxisName,v,"%s == %s"%(xaxisName,x))
        #br_i = tmpgraph.Eval(y)
        #tmpgraph.Delete()

        #gamma_v = v.replace("BR","GAMMA")
        #tmpgraph = self.getGraph(yaxisName,gamma_v,"%s == %s"%(xaxisName,x))
        #gamma_i = tmpgraph.Eval(y)
        #tmpgraph.Delete()

        #gammatot = gamma_i/br_i

        ##### second Gamma
        #tmpgraph = self.getGraph(yaxisName,w,"%s == %s"%(xaxisName,x))
        #br_j = tmpgraph.Eval(y)
        #tmpgraph.Delete()

        #gamma_w = w.replace("BR","GAMMA")
        #tmpgraph = self.getGraph(yaxisName,gamma_w,"%s == %s"%(xaxisName,x))
        #gamma_j = tmpgraph.Eval(y)
        #tmpgraph.Delete()

        #####

        #sign = 1
        #if pm == "-":
            #sign = -1

        #br_prime1 = (gamma_i*(1+sign*gamma_uncert) + gamma_j)/ (gamma_i*(1+sign*gamma_uncert) + gamma_j + gammatot-gamma_i-gamma_j)
        #br_uncert1 = abs(br_prime1 - br_i - br_j) / (br_i + br_j)

        #br_prime2 = (gamma_i + gamma_j*(1+sign*gamma_uncert))/ (gamma_i + gamma_j*(1+sign*gamma_uncert) + gammatot-gamma_i-gamma_j)
        #br_uncert2 = abs(br_prime2 - br_i - br_j) / (br_i + br_j)

        #br_prime3 = (gamma_i + gamma_j)/ (gamma_i + gamma_j + (gammatot-gamma_i-gamma_j)*(1+sign*gamma_uncert))
        #br_uncert3 = abs(br_prime3 - br_i - br_j) / (br_i + br_j)

        #br_uncert = br_uncert1 + br_uncert2 + br_uncert3
        #return br_uncert

        
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

        #print "Tanb limits for selection",selection
        #for i,xx in enumerate(x):
            #print xx,y[i]
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
            if highTanbRegion and ylimit <= 1:
		#print "    ",i, xval, yval, ylimit
                ylimit = 80
            graph.SetPoint(i, xval, ylimit)
            #print "    ",i, xval, yval, ylimit 

        if limitBRtoMin:
            graph = self.graphToMinTanb(graph,xVariableName,selection,highTanbRegion)

        #for i in xrange(0, graph.GetN()):
            #print "    ",graph.GetX()[i],graph.GetY()[i]
        return graph

    def graphToTanBetaCombined(self,graph,xVariableName,selection):
        print "High tanb graph" 
        highTanbGraph = self.graphToTanBeta(graph,xVariableName,selection,highTanbRegion=True)
        print "Low tanb graph"
        lowTanbGraph  = self.graphToTanBeta(graph,xVariableName,selection,highTanbRegion=False)
        print "High+low merged"
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
#        graphX.append(0)
#        graphY.append(0.5*(graph1.GetY()[0]+graph2.GetY()[0]))
        for i in range(0,graph2.GetN()):
            x = graph2.GetX()[i]
            y = graph2.GetY()[i]
            graphX.append(x)
            graphY.append(y)

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
        for i in range(retGraph.GetN()):
            x = retGraph.GetX()[i]
            y = retGraph.GetY()[i]
            #print "check merge graph",x,y
        return retGraph
    
    def graphToMinTanb(self,graph_orig,xVariableName,selection,highTanbRegion=True):

        graph = graph_orig.Clone()

#        for i in range(graph.GetN()):
#            print "check graphToMinTanb input x,y",graph.GetX()[i],graph.GetY()[i]

        entryFound = False
        for i in reversed(range(graph.GetN()-1)):
            if self.isEqual(graph.GetY()[i],1):
                if graph.GetX()[i] > 175:
                    if entryFound and self.isEqual(graph.GetY()[i+1],1) and self.isEqual(graph.GetY()[i-1],1):
                        #print "check remove point0",i,graph.GetX()[i],graph.GetY()[i]
                        graph.RemovePoint(i)
                else:   
                    if entryFound and self.isEqual(graph.GetY()[i+1],1):
                        #print "check remove point1",i,graph.GetX()[i],graph.GetY()[i]
                        graph.RemovePoint(i)
            else:
                entryFound = True
                
        entryFound = False        
        for i in reversed(range(graph.GetN())):
            if self.isEqual(graph.GetY()[i],1):
                if not entryFound and self.isEqual(graph.GetY()[i-1],1):
                    #print "check remove point2",i,graph.GetX()[i],graph.GetY()[i]
                    graph.RemovePoint(i)
            else:
                entryFound = True
                    
#        for i in range(graph.GetN()):
#            print "check graphToMinTanb input2 x,y",graph.GetX()[i],graph.GetY()[i]

        graphX = []
        graphY = []

        if highTanbRegion:
            for i in range(graph.GetN()):
                x = graph.GetX()[i]
                y = graph.GetY()[i]
                if self.isEqual(y,1):
                    if x > 175:
                        y = 75
                    else:
                        ymin = self.getMinimumTanb(self.BRvariable,selection+"&&"+xVariableName+"==%s"%graph.GetX()[i])
                        y = ymin
                graphX.append(x)
                graphY.append(y)
        else:
            for i in range(graph.GetN()):
                x = graph.GetX()[i]
                y = graph.GetY()[i]
                if self.isEqual(y,1):
                    ymin = self.getMinimumTanb(self.BRvariable,selection+"&&"+xVariableName+"==%s"%graph.GetX()[i])
                    #print "check x",i,graph.GetN(),x,graph.GetX()[i+1]
                    if i > 0 and graph.GetX()[i-1] > x:
                        y = ymin
                    if i == 0 and graph.GetX()[i+1] > x:
                        y = ymin
                graphX.append(x)
                graphY.append(y)
            
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
            if y > 0:
                graphX.append(x)
                graphY.append(y)
        graphX.append(200)
        graphY.append(graphY[len(graphY)-1])
        retGraph = ROOT.TGraph(len(graphX),array('d',graphX),array('d',graphY))
        retGraph.SetName("MinTanb")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(3)
        return retGraph

    def LogicalAnd(self,selection1,selection2):
        if len(selection1) > 0 and len(selection2) > 0:
            return selection1 + "&&" + selection2
        if len(selection1) > 0 and len(selection2) == 0:
            return selection1
        if len(selection1) == 0 and len(selection2) > 0:
            return selection2
        return ""

    def inaccessible(self,xVariableName,selection):
        selection = self.LogicalAnd(selection,self.selection)

        graphX = []
        graphY = []

        yVariableName = "tanb"
        xValues = self.getValues(xVariableName,selection)
        graphX.append(xValues[0])
        graphY.append(0.5)
        
        for x in xValues:
            ysel = self.LogicalAnd(selection,self.floatSelection("%s==%s"%(xVariableName,x)))
            y = min(self.getValues(yVariableName,ysel,roundValues=-1))
            graphX.append(x)
            graphY.append(y)

        graphX.append(xValues[len(xValues)-1])
        graphY.append(0.5)

        retGraph = ROOT.TGraph(len(graphX),array('d',graphX),array('d',graphY))
        retGraph.SetName("TheoreticallyInaccessible")
        retGraph.SetFillColor(4)
        self.PrintGraph(retGraph)
        return retGraph
    

    def mhLimit(self,higgs,xVariableName,selection,mhMeasurement):
        #print higgs,xVariableName,selection,mhMeasurement
        
        s = mhMeasurement.split("+-")
        mySingleSidedMeasurementStatus = False
        if len(s) == 2 and float(s[1]) < 0.000001:
            mySingleSidedMeasurementStatus = True
        
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

        tanbStart = 5
        if higgs == "mH" or higgs == "mA":
            tanbStart = 1
        lower_y0,lower_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.lowerLimit(mhMeasurement))
        upper_y0,upper_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.upperLimit(mhMeasurement))
        #print "check lower x0, y0",mhMeasurement,lower_x0,lower_y0,upper_x0,upper_y0
        for i in range(0,len(lower_x0)):
            j = len(lower_x0) -1 -i
            if lower_y0[j] < 30:
                x.append(lower_x0[j])
                y.append(lower_y0[j])
            else:
                if lower_x0[j] <= mHpStart:
                    x.append(lower_x0[j])
                    y.append(lower_y0[j])

        #for i in range(len(x)):
            #print x[i],y[i]

        if higgs == "mh":
            lower_x,lower_y = self.getLimits(higgs,xVariableName,"tanb",selection,self.lowerLimit(mhMeasurement))
            upper_x,upper_y = self.getLimits(higgs,xVariableName,"tanb",selection,self.upperLimit(mhMeasurement))
            #print "check mhlimit lower x,y",lower_x,lower_y
            #print "check mhlimit upper x,y",upper_x,upper_y
            for i in range(0,len(lower_x)):
                if lower_x[i] > lower_x0[0]:
                    x.append(lower_x[i])
                    y.append(lower_y[i])

            # To not show a line on right edge of the plot in case there is an upper and lower band
            if len(upper_x) > 0:
                x.append(610)
                y.append(y[-1])
            
            
            if not mySingleSidedMeasurementStatus:
                for i in range(0,len(upper_x)):
                    j = len(upper_x) -1 -i
                    if upper_x[j] > upper_x0[0]:
                        x.append(upper_x[j])
                        y.append(upper_y[j])

        if not mySingleSidedMeasurementStatus:
            for i in range(0,len(upper_x0)):
                if i == 0 and upper_y0[0] == y[len(y)-1]:
                    continue
                if len(upper_x00) == 0:
                    x.append(upper_x0[i])
                    y.append(upper_y0[i])
                else:
                    if upper_x0[i] <= mHpStart or upper_y0[i] < 30:
                        x.append(upper_x0[i])
                        y.append(upper_y0[i])

        if higgs == "mh" and not mySingleSidedMeasurementStatus:
            for i in range(0,len(upper_x00)):
                x.append(upper_x00[i])
                y.append(upper_y00[i])
#            x.append(600)
#            y.append(100)

        if len(x) == 0:
            print "Failed to generate curve for %s=%s (not visible)!"%(higgs,mhMeasurement)
            x = [0]
            y = [0]
        elif higgs == "mH":
	    x.append(180)
	    y.append(100)
	    x.append(0)
            y.append(100)

        #for i in range(0,len(x)):
            #print "mhlimit:  m,tanb",x[i],y[i]
        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("mhLimit_%s%s"%(higgs,mhMeasurement))
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
#        retGraph.SetFillColor(ROOT.TColor.GetColor("#ffffcc"))
        retGraph.SetFillColor(7)
        retGraph.SetFillStyle(3008)
        return retGraph

    def mHLimit_mA(self,higgs,xVariableName,selection,mhMeasurement):
        #print "mHLimit_mA",higgs,xVariableName,selection

        graph1_x = []
        graph1_y = []

        graph2_x = []
        graph2_y = []

        graph3_x = []
        graph3_y = []

        xvalues = self.getValues(xVariableName,selection)
        #print xvalues
        limit = self.lowerLimit(mhMeasurement)
        for xv in xvalues:
#            print "x=",xv
            xval = float(xv)
            theSelection = selection+"&&"+self.floatSelection(xVariableName+"==%s"%xval)
            graph = self.getGraph("tanb",higgs,theSelection)
            xg,yg = self.graph2arrays(graph)
#            crossOverPoints0 = []
#            crossOverPoints1 = []
#            directions = []
            ntimes = 0
            for i in range(1,len(xg)):
                x0 = xg[i-1]
                y0 = yg[i-1]
                x1 = xg[i]
                y1 = yg[i]
                #print "mu,tanb,mH",xv,xg[i],yg[i]
                if y0 < limit and y1 > limit:
                    tanblimit = self.linearFunction(limit,y0,x0,y1,x1)
                    if ntimes == 0:
                        graph1_x.append(xval)
                        graph1_y.append(tanblimit)
                        ntimes += 1
                    else:
                        graph2_x.append(xval)
                        graph2_y.append(tanblimit)

                if y0 > limit and y1 < limit:
                    tanblimit = self.linearFunction(limit,y0,x0,y1,x1)
                    graph3_x.append(xval)
                    graph3_y.append(tanblimit)

        graph5_x = []
        graph5_y = []

        graph6_x = []
        graph6_y = []

        graph7_x = []
        graph7_y = []

        limit = self.upperLimit(mhMeasurement)
        for xv in xvalues:
#            print "x=",xv
            xval = float(xv)
            theSelection = selection+"&&"+self.floatSelection(xVariableName+"==%s"%xval)
            graph = self.getGraph("tanb",higgs,theSelection)
            xg,yg = self.graph2arrays(graph)
            ntimes = 0
            for i in range(1,len(xg)):
                x0 = xg[i-1]
                y0 = yg[i-1]
                x1 = xg[i]
                y1 = yg[i]

                if y0 < limit and y1 > limit:
                    tanblimit = self.linearFunction(limit,y0,x0,y1,x1)
                    if ntimes == 0:
                        graph5_x.append(xval)
                        graph5_y.append(tanblimit)
                        ntimes += 1
                    else:
                        graph6_x.append(xval)
                        graph6_y.append(tanblimit)
                if y0 > limit and y1 < limit:
                    tanblimit = self.linearFunction(limit,y0,x0,y1,x1)
                    graph7_x.append(xval)
                    graph7_y.append(tanblimit)

#                    crossOverPoints0.append(x0)
#                    crossOverPoints1.append(x1)
#                    directions.append(-1)
#            ys = []
#            for i in range(len(crossOverPoints0)):
#                tanbmin = crossOverPoints0[i]
#                tanbmax = crossOverPoints1[i]
#                print "tanbmin,max",tanbmin,tanbmax
#                self.nInterpolation = 0
#                tanblimit = self.linearFunction(limit,mHmin,tanbmin,mHmax,tanbmax)
#                ys.append(tanblimit)
    
#            print "ys",ys
#            self.PrintGraph(graph)
#        sys.exit()
#        tanbStart = 1
#        print "check mHLimit_mA",higgs,xVariableName,selection
#        lower_y0,lower_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.lowerLimit(mhMeasurement))
#        upper_y0,upper_x0 = self.getLimits(higgs,"tanb",xVariableName,selection+"&&tanb>=%s"%tanbStart,self.upperLimit(mhMeasurement))

#        print lower_y0,lower_x0
#        sys.exit()
#        for i in range(0,len(lower_x0)):
#            j = len(lower_x0) -1 -i
#            if lower_y0[j] < 30:
#                x.append(lower_x0[j])
#                y.append(lower_y0[j])
#            else:
#                if lower_x0[j] <= mHpStart:
#                    x.append(lower_x0[j])
#                    y.append(lower_y0[j])


        #print            
        #for i in range(len(graph1_x)):
            #print "                    %s, %s,"%(graph1_x[i],graph1_y[i])
        #print
        #for i in reversed(range(len(graph3_x))):
            #print "                    %s, %s,"%(graph3_x[i],graph3_y[i])
        #print
        #for i in range(len(graph2_x)):
            #print "                    %s, %s,"%(graph2_x[i],graph2_y[i])
        #print
##        for i in range(len(graph3_x)):
##            print "                    %s, %s,"%(graph3_x[i],graph3_y[i])
##        print
        #for i in reversed(range(len(graph5_x))):
            #print "                    %s, %s,"%(graph5_x[i],graph5_y[i])
        #print
        #for i in reversed(range(len(graph6_x))):
            #print "                    %s, %s,"%(graph6_x[i],graph6_y[i])
        #print
        #for i in range(len(graph7_x)):
            #print "                    %s, %s,"%(graph7_x[i],graph7_y[i])

        x = []
        y = []
        x.extend(xinc)
        y.extend(yinc)
#        x.extend(reversed(xdec))
#        y.extend(reversed(ydec))

        #for i in range(0,len(x)):
            #print "mhlimit:  m,tanb",x[i],y[i]
        sys.exit()    
        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("mhLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        retGraph.SetFillColor(7)
        retGraph.SetFillStyle(3008)
        return retGraph

    def getHardCoded_mH_limitForMu_mA(self,mass,region=0):
        data = []
        if mass == 110:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    1800.0, 0.854132486576,
                    1900.0, 0.99914738702,
                    2000.0, 1.12000529022,
                    2100.0, 1.24671046729,
                    2200.0, 1.38811361838,
                    2300.0, 1.56947172561,
                    2400.0, 1.8310179733,
                    2410.0, 1.86687719376,
                    2420.0, 1.90131151193,
                    2430.0, 1.94757719069,
                    2440.0, 1.99100507708,
                    2450.0, 2.04618952282,
                    2460.0, 2.10167495697,
                    2470.0, 2.17667259999,
                    2480.0, 2.2679850711,
                    2490.0, 2.39420811635,
                    2490.0, 3.20135489301,
                    2480.0, 3.51597560986,
                    2470.0, 3.92531042401,
                    2470.0, 4.34060804699,
                    2480.0, 4.63642573942,
                    2490.0, 4.79583908008,
                    2500.0, 4.91310503882,
                    2600.0, 5.50184465864,
                    2700.0, 5.77264941389,
                    2800.0, 5.92869959732,
                    2900.0, 6.02021573136,
                    3000.0, 6.06971683218,
                    3100.0, 6.08939343345,
                    3200.0, 6.08735144045,
                    3300.0, 6.06884643992,

                    3500.0, 6.0,
                    3500.0, 23.7,

                    3300.0, 23.7179108091,
                    3200.0, 25.2994600794,
                    3100.0, 27.0838402694,
                    3000.0, 29.1309411324,
                    2900.0, 31.5019452343,
                    2800.0, 34.2770039897,
                    2700.0, 37.60201053,
                    2600.0, 41.6873822408,
                    2500.0, 46.9261505569,
                    2400.0, 54.2523244912,
                    2300.0, 68.3855635511,

                    280.0, 72.7139444289,
                    270.0, 70.2778562327,
                    260.0, 67.8642225713,
                    250.0, 65.4627438648,
                    240.0, 63.0672229295,
                    230.0, 60.660591108,
                    220.0, 58.2318402539,
                    210.0, 55.7574199652,
                    200.0, 53.2071830624,

                    100.0, 40,

                    200.0, 24.5183379961,
                    210.0, 23.5290332815,
                    220.0, 22.6641518048,
                    230.0, 21.8870446993,
                    240.0, 21.2014059677,
                    250.0, 20.581887486,
                    260.0, 19.9859996724,
                    270.0, 19.4760503994,
                    280.0, 18.9639384265,
                    290.0, 18.5241367976,
                    300.0, 18.076685924,
                    400.0, 14.8585813979,
                    500.0, 12.7513458894,
                    600.0, 11.1889526711,
                    700.0, 9.94188555152,
                    800.0, 8.93012352062,
                    900.0, 8.06882728289,
                    1000.0, 7.31840136675,
                    1100.0, 6.65458545374,
                    1200.0, 6.05084697701,
                    1300.0, 5.53550867791,
                    1400.0, 5.08365856105,
                    1500.0, 4.67822768017,
                    1600.0, 4.31256884738,
                    1700.0, 3.95306255817,
                    1800.0, 3.59415089194,
                    1900.0, 3.22883986762,
                    2000.0, 2.83935975369,
                    2100.0, 2.33848046492,
                    2110.0, 2.26189830023,
                    2120.0, 2.16263791536,
                    2100.0, 1.6762319659,
                    2000.0, 1.37087645279,
                    1900.0, 1.18831423144,
                    1800.0, 1.04450965004,
                    1700.0, 0.903851991518,
                    1660.0, 0.838744349747,
                    1650.0, 0.818514828969,
                    1640.0, 0.8,
                    1630.0, 0.77,
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...                                                                                                 
                data = [
                    ]

        if mass == 140:
            if region == 0:
                # data: mu,tanb, mu,tanb,...                                                                                                 
                data = [

                    1900.0, 0.854594234856,
                    2000.0, 0.925465205775,
                    2100.0, 0.99330023211,
                    2200.0, 1.0614599614,
                    2210.0, 1.06805851318,
                    2220.0, 1.07468801065,
                    2230.0, 1.08137237353,
                    2240.0, 1.08813736601,
                    2250.0, 1.09501079666,
                    2260.0, 1.10228292342,
                    2270.0, 1.11015899727,
                    2280.0, 1.1178865973,
                    2290.0, 1.12547702577,
                    2300.0, 1.13294192473,
                    2310.0, 1.14029334631,
                    2400.0, 1.20461893525,
                    2500.0, 1.28568536635,
                    2600.0, 1.37547851167,
                    2700.0, 1.47630962412,
                    2800.0, 1.59315302022,
                    2810.0, 1.60610846207,
                    2820.0, 1.62122837512,
                    2830.0, 1.63602253697,
                    2840.0, 1.65050592148,
                    2850.0, 1.66469328465,
                    2860.0, 1.67859920028,
                    2870.0, 1.69223810928,
                    2880.0, 1.70763941972,
                    2890.0, 1.72542420108,
                    2900.0, 1.74280071852,
                    3000.0, 1.94153432173,
                    3100.0, 2.27634393257,
                    3110.0, 2.33087162867,
                    3120.0, 2.39210511409,
                    3130.0, 2.47337701317,
                    3140.0, 2.58158408276,
                    3150.0, 2.76368840664,

                    3150.0, 3.02129080594,
                    3140.0, 3.25421293234,
                    3130.0, 3.40572262171,
                    3120.0, 3.53155775679,
                    3110.0, 3.64494984562,
                    3100.0, 3.75036346677,
                    3000.0, 4.65688752156,
                    2900.0, 5.62089846744,
                    2890.0, 5.79467749462,

                    2890.0, 5.90032939913,
                    2900.0, 5.97641603594,
                    3000.0, 6.03079347159,
                    3100.0, 5.97386748483,
                    3110.0, 5.96695013308,
                    3120.0, 5.9599314519,
                    3130.0, 5.95281978802,
                    3140.0, 5.94562230279,
                    3150.0, 5.93834521047,
                    3160.0, 5.9309939226,
                    3170.0, 5.9235731948,
                    3180.0, 5.91608722309,
                    3190.0, 5.90853971249,
                    3200.0, 5.90093398858,
                    3300.0, 5.82245908891,

                    3500.0, 5.8,
                    3500.0, 10.7,

                    3300.0, 10.6991584193,
                    3200.0, 10.8234968864,
                    3190.0, 10.8349294403,
                    3180.0, 10.8461697924,
                    3170.0, 10.8572151475,
                    3160.0, 10.868062628,
                    3150.0, 10.8787092626,
                    3140.0, 10.8891520022,
                    3130.0, 10.8993876692,
                    3120.0, 10.9094130031,
                    3110.0, 10.9192246529,
                    3100.0, 10.9288191303,
                    3000.0, 11.0141984977,
                    2900.0, 11.0815519803,
                    2890.0, 11.0863110175,
                    2880.0, 11.0906766372,

                    2870.0, 11.0946391412,
                    2860.0, 11.0981883227,
                    2850.0, 11.1013135126,
                    2840.0, 11.1040035312,
                    2830.0, 11.1062466612,
                    2820.0, 11.108030615,
                    2810.0, 11.1093424978,
                    2800.0, 11.1101687831,
                    2700.0, 11.0881791564,
                    2600.0, 10.9963346755,
                    2500.0, 10.8273492631,
                    2400.0, 10.4857786653,
                    2310.0, 9.84459018792,
                    2300.0, 9.72899907843,
                    2290.0, 9.59241710144,
                    2280.0, 9.42177567799,
                    2270.0, 9.18403669588,

                    2270.0, 8.06679614195,
                    2280.0, 7.78195723276,
                    2290.0, 7.56559939746,
                    2300.0, 7.38192803438,
                    2310.0, 7.21981738414,
                    2400.0, 6.16877546906,
                    2500.0, 5.3413550539,
                    2600.0, 4.65542582929,
                    2700.0, 4.03019100166,
                    2800.0, 3.38944914231,
                    2810.0, 3.31834216638,
                    2820.0, 3.24408141947,
                    2830.0, 3.16587805124,
                    2840.0, 3.08214094485,
                    2850.0, 2.98966018248,
                    2860.0, 2.87908797196,
                    2870.0, 2.73222329284,

                    2870.0, 2.32581136291,
                    2860.0, 2.22270605111,
                    2850.0, 2.15400803826,
                    2840.0, 2.09380976977,
                    2830.0, 2.05010565045,
                    2820.0, 2.00436443931,
                    2810.0, 1.97051586584,
                    2800.0, 1.93681773453,
                    2700.0, 1.69309369551,
                    2600.0, 1.5361155526,
                    2500.0, 1.40974277028,
                    2400.0, 1.30599159577,
                    2310.0, 1.22713955996,
                    2300.0, 1.21763736127,
                    2290.0, 1.20790853644,
                    2280.0, 1.19855352251,
                    2270.0, 1.19142908776,
                    2260.0, 1.18421189753,
                    2250.0, 1.17688969248,
                    2240.0, 1.16945060875,
                    2230.0, 1.16188310993,
                    2220.0, 1.1541759229,
                    2210.0, 1.14631797626,
                    2200.0, 1.13829834295,
                    2100.0, 1.06270314641,
                    2000.0, 0.988987097841,
                    1900.0, 0.919892755008,
                    1800.0, 0.849618822569,
                    1700.0, 0.767531892104,
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    ]

        if len(data) == 0:
            return None

        x = []
        y = []
        for i in range(len(data)/2):
            xp = data[2*i]
            yp = data[2*i+1]
            x.append(xp)
            y.append(yp)

        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("mhLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        #retGraph.SetFillColor(ROOT.TColor.GetColor("#ffffcc"))                                                                              
        retGraph.SetFillColor(7)
        retGraph.SetFillStyle(3008)
        return retGraph

    def getHardCoded_mH_limitForMu(self,mass,region=0):

        data = []
        if mass == 90:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    200.0, 6.7965599109364803,
                    300.0, 5.4831801215288465,
                    400.0, 4.6286550249530762,
                    500.0, 3.9975031425888972,
                    600.0, 3.4956225261981615,
                    700.0, 3.0802471870314747,
                    800.0, 2.7137546773944621,
                    900.0, 2.3799000510875814,
                    1000.0, 2.0655857874490167,
                    1100.0, 1.7683399423353592,
                    1200.0, 1.4543536313809113,
                    1300.0, 1.1561217361315865,
                    1400.0, 1.0,
                    1500.0, 1.0,
                    1600.0, 2.5357649817378274,
                    1700.0, 3.2388535456507839,
                    1800.0, 3.7610457881411605,
#                    1800.0,4.4,
#                    1700.0,32.0,
#                    1600.0,63.0,
#                    1500.0,74.0,
#                    1400.0,75.0,
#                    1300.0,75.0,
#                    1200.0,75.0,
#                    1100.0,71.0,
#                    1000.0,65.0,
#                    900.0,60.0,
#                    800.0,56.0,
#                    700.0,53.0,
#                    600.0,49.0,
#                    500.0,46.0,
#                    400.0,44.0,
#                    300.0,41.0,
#                    200.0, 39.0
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    ]
        if mass == 100:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    200.0, 8.4982043404958176,
                    300.0, 6.8955889487555169,
                    400.0, 5.8562397665378398,
                    500.0, 5.0959478578252515,
                    600.0, 4.4953950868762718,
                    700.0, 3.9934330553453776,
                    800.0, 3.5563999033468292,
                    900.0, 3.1611378268508901,
                    1000.0, 2.7918680955298072,
                    1100.0, 2.4414295932867986,
                    1200.0, 2.0730932380767157,
                    1300.0, 1.65163226319995,
                    1400.0, 1.0710473649182894,
                    1500.0, 1.0,
                    1600.0, 1.0,
                    1700.0, 1.6499251465262574,
                    1800.0, 2.8491371750556027,
                    1900.0, 3.6912703720355466,
                    2000.0, 4.237178551700481,
                    2100.0, 4.6487246214273341,
                    2200.0, 4.9766035083943621,
                    2300.0, 5.2440581079063691,
                    2400.0, 5.4636783649141876,
                    2500.0, 5.6440132787050175,
#                    2500.0,9.8,
#                    2400.0,46.0,
#                    2300.0,57.0,
#                    2200.0,65.0,
#                    2100.0,75.0,
#                    2000.0,75.0,
#                    1900.0,75.0,
#                    1800.0,75.0,
#                    1700.0,75.0,
#                    1600.0,75.0,
#                    1500.0,75.0,
#                    1400.0,75.0,
#                    1300.0,75.0,
#                    1200.0,75.0,
#                    1100.0,75.0,
#                    1000.0,75.0,
#                    900.0,75.0,
#                    800.0,75.0,
#                    700.0,75.0,
#                    600.0,75.0,
#                    500.0,74.0,
#                    400.0,67.0,
#                    300.0,61.0,
#                    200.0,56.0
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    ]
        if mass == 120:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    200.0, 14.164237007641987,
                    300.0, 11.24306722053268,
                    400.0, 9.4543545554277557,
                    500.0, 8.2207535077887428,
                    600.0, 7.278460961024166,
                    700.0, 6.5147136645066155,
                    800.0, 5.8695752236459953,
                    900.0, 5.3064746874927664,
                    1000.0, 4.803891636983863,
                    1100.0, 4.347103598773657,
                    1200.0, 3.9207858542093987,
                    1300.0, 3.5242286905358213,
                    1400.0, 3.1321880855127091,
                    1500.0, 2.7845647701474334,
                    1600.0, 2.466939438965575,
                    1700.0, 2.0527628479008655,
                    1800.0, 1.0175306826699515,
                    1900.0, 1.2188003598798893,
                    2000.0, 1.4407389301035618,
                    2100.0, 1.7718638765000243,
                    2200.0, 3.6412216952643348,
                    2300.0, 4.676905927699579,
                    2400.0, 5.1481127924108421,
                    2500.0, 5.4577730506856312,
                    2600.0, 5.677202658726145,
                    2700.0, 5.8360042145510533,
                    2800.0, 5.9500010493612479,
                    2900.0, 6.0292156298314978,
                    3000.0, 6.0806788344554406,
                    3100.0, 6.1094753346157233,
                    3200.0, 6.1197537996149407,
                    3300.0, 6.1142517116978041,
#                    3300.0, 55.0,
#                    3200.0,60.0,
#                    3100.0,64.0,
#                    3000.0,68.0,
#                    2900.0,72.0,
#                    2800.0,75.0,
#                    2700.0,75.0,
#                    2600.0,75.0,
#                    2500.0,75.0,
#                    2400.0,75.0,
#                    2300.0,75.0,
#                    2200.0,75.0,
#                    2100.0,75.0,
#                    2000.0,75.0,
#                    1900.0,75.0,
#                    1800.0,75.0,
#                    1700.0,75.0,
#                    1600.0,75.0,
#                    1500.0,75.0,
#                    1400.0,75.0,
#                    1300.0,75.0,
#                    1200.0,75.0,
#                    1100.0,75.0,
#                    1000.0,75.0,
#                    900.0,75.0,
#                    800.0,75.0,
#                    700.0,75.0,
#                    600.0,75.0,
#                    500.0,75.0,
#                    400.0,75.0,
#                    300.0,75.0,
#                    200.0,56.214684565246898
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    ]
        if mass == 140:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    200.0, 28.834676428517014,
                    300.0, 21.050414526906707,
                    400.0, 17.267423730992391,
                    500.0, 14.772369991491814,
                    600.0, 12.923746151443709,
                    700.0, 11.502581509998834,
                    800.0, 10.311919321129267,
                    900.0, 9.2754747467266441,
                    1000.0, 8.4030815993157262,
                    1100.0, 7.635735079182183,
                    1200.0, 6.9494669659287638,
                    1300.0, 6.3432879137879752,
                    1400.0, 5.7865358238109366,
                    1500.0, 5.3302380859464336,
                    1600.0, 4.9533900691126718,
                    1700.0, 4.5784719667238605,
                    1800.0, 4.2109212625952495,
                    1900.0, 3.8519016317042585,
                    2000.0, 3.4941923395823338,
                    2100.0, 3.1256711094975387,
                    2200.0, 2.7211612830602832,
                    2200.0, 1.5333820286373108,
                    2100.0, 1.3410622795788596,
                    2000.0, 1.1971639007828219,
                    1900.0, 1.0815946988001435,
                    1900.0, 1.0,
                    2000.0, 1.0361127725930215,
                    2100.0, 1.13420213006395,
                    2200.0, 1.2375071681959171,
                    2300.0, 1.3533634949610942,
                    2400.0, 1.4887629788589916,
                    2500.0, 1.6707496851740391,
                    2600.0, 1.958633694884945,
                    2600.0, 3.824788451679126,
                    2600.0, 5.1859227070512475,
                    2700.0, 5.701842428134654,
                    2800.0, 5.9118125801222448,
                    2900.0, 6.0178860176573323,
                    3000.0, 6.0670166584456808,
                    3100.0, 6.079574651882325,
                    3200.0, 6.0669335793566859,
                    3300.0, 6.0358695434958918,
                    3300.0,18.803640497061338,
                    3200.0,19.884597582336141,
                    3100.0,21.067188246045021,
                    3000.0,22.406002664657876,
                    2900.0,23.881547567073312,
                    2800.0,25.545617231141023,
                    2700.0,27.415761411044286,
                    2600.0,29.541905797402706,
                    2500.0,31.972135559907883,
                    2400.0,34.795815128156846,
                    2300.0,38.087798663170815,
                    2200.0,41.974363083053049,
                    2100.0,46.610248594412042,
                    2000.0,51.93901921667748,
                    1900.0,57.811529597306617,
                    1800.0,64.520810818490645,
                    1700.0,72.035371833745558,
                    1600.0,75.0,
                    1500.0,75.0,
                    1400.0,75.0,
                    1300.0,75.0,
                    1200.0,75.0,
                    1100.0,75.0,
                    1000.0,75.0,
                    900.0,75.0,
                    800.0,75.0,
                    700.0,75.0,
                    600.0,75.0,
                    500.0,75.0,
                    400.0,75.0,
                    300.0,75.0,
                    200.0,52.883049130943618
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    ]
        if mass == 150:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    300.0,75.0,
                    300.0, 40.850393725223512,
                    400.0, 32.600578291396232,
                    500.0, 27.282710766442278,
                    600.0, 23.256282520832769,
                    700.0, 20.049914015910531,
                    800.0, 17.461077418216405,
                    900.0, 15.313507186570348, 
                    1000.0, 13.523721547300795,
                    1100.0, 11.989203361547425,
                    1200.0, 10.718586245684833,
                    1300.0, 9.5899890901809783,
                    1400.0, 8.6096471527319096,
                    1500.0, 7.8543321759305229,
                    1600.0, 7.2589925865183744,
                    1700.0, 6.6852450274988513,
                    1800.0, 6.1469973054246907,
                    1900.0, 5.6462445042984228,
                    2000.0, 5.1789919939965401,
                    2100.0, 4.7397532605924582,
                    2200.0, 4.3211504713349242,
                    2300.0, 3.9151977832109068,
                    2400.0, 3.509397618448979,
                    2500.0, 3.077078903586397,
                    2600.0, 2.5031074012655949,
                    2600.0, 1.970106264867276,
                    2500.0, 1.6345335297566894,
                    2400.0, 1.4617441252748629,
                    2300.0, 1.3332441988448078,
                    2200.0, 1.2274632733601618,
                    2100.0, 1.1358570819806499,
                    2000.0, 1.0514021124049762,
                    2000.0, 1.0,
                    2100.0, 1.0316832745047266,
                    2200.0, 1.106212731382856,
                    2300.0, 1.1856819328334771,
                    2400.0, 1.2724970953688355,
                    2500.0, 1.3680983727312221,
                    2600.0, 1.4776155066796179,
                    2700.0, 1.610462446811268,
                    2800.0, 1.7901010252999976,
                    2900.0, 2.08900679254495,
                    2900.0, 3.421141075576287,
                    2800.0, 4.3679581111702532,
                    2800.0, 5.8231507135282641,
                    2900.0, 6.0126169726958096,
                    3000.0, 6.0584781230627129,
                    3100.0, 6.0495959723424448,
                    3200.0, 6.0113951423432894,
                    3300.0, 5.9555143244808306,
                    3300.0, 13.852332238204269,
                    3200.0,14.398028848484159,
                    3100.0,14.952880232342352,
                    3000.0,15.561551755066546,
                    2900.0,16.184948966994398,
                    2800.0,16.849548338740249,
                    2700.0,17.560416256161147,
                    2600.0,18.306971645286126,
                    2500.0,19.098614171113582,
                    2400.0,19.949700218724502,
                    2300.0,20.867644650694047,
                    2200.0,21.853636272445669,
                    2100.0,22.918311094857131,
                    2000.0,24.078499805053411,
                    1900.0,25.353181170185621,
                    1800.0,26.746391802602147,
                    1700.0,28.282876126476822,
                    1600.0,29.967029613764907,
                    1500.0,31.843905479887781,
                    1400.0,33.815353864536746,
                    1300.0,36.003256221739321,
                    1200.0,39.381390986373844,
                    1100.0,44.784614735568539,
                    1000.0,51.865144334466549,
                    900.0,61.959676415732247,
                    800.0,75.0,
                    700.0,75.0,
                    600.0,75.0,
                    500.0,75.0,
                    400.0,75.0,
                    300.0,75.0
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                        ]
        if mass == 155:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    2000.0, 1.0,
                    2100.0, 1.0,
                    2200.0, 1.0614446071520542,
                    2300.0, 1.1315324432807932,
                    2400.0, 1.2009993056752262,
                    2500.0, 1.2813828198417849,
                    2600.0, 1.3690549838748203,
                    2700.0, 1.4677494473949859,
                    2900.0, 1.731863655367273, 
                    3000.0, 1.9420065668752091,
                    3100.0, 2.4135693061152352,
                    3100.0, 2.9595425794805124,
                    3000.0, 3.8917184226057202,
                    2900.0, 4.6864811751510871,
                    2700.0, 1.7652555764602553,
                    2600.0,1.5718492906472532,
                    2500.0,1.4362541454782862,
                    2400.0,1.3268418164440767,
                    2300.0,1.2346802457821886,
                    2200.0,1.1524955489669899,
                    2100.0,1.0748653795345366,
                    2000.0,1.0004294959059099
                    ]
            if region == 1:
                # data: mu,tanb, mu,tanb,...
                data = [
                    3300.0,11.836539752818254,
                    3200.0,12.187933100220135,
                    3100.0,12.552657158938359,
                    3000.0,12.903678076532515,
                    2900.0,13.277879570012658,
                    2800.0,13.650608297548786,
                    2700.0,14.007736601689089,
                    2600.0,14.395458451498143,
                    2500.0,14.762597659924836,
                    2400.0,15.122427999825902,
                    2300.0,15.487728589200628,
                    2200.0,15.822748993752555,
                    2100.0,16.139064423964555,
                    2000.0,16.431939609415849,
                    1900.0,16.66537361587649,
                    1800.0,16.818731955762246,
                    1700.0,16.854308282830061,
                    1600.0,16.697961279158676,
                    1500.0,16.216122451931597,
                    1500.0,12.023494381073476,
                    1600.0,10.452078307115357,
                    1700.0,9.1925196941315335,
                    1800.0,8.20541450843875,
                    1900.0,7.3796309562707592,
                    2000.0,6.6694636059731494,
                    2100.0,6.0450891897124137,
                    2200.0,5.4853610271059239,
                    2300.0,4.9748681249303601,
                    2400.0,4.4995323485058165,
                    2500.0,4.0471111323524696,
                    2600.0,3.5989450641423133,
                    2700.0,3.1200150303774734,
                    2900.0,6.006202438453812,
                    3000.0,6.0492524214846668,
                    3100.0,6.0176896220390574,
                    3200.0,5.9574743661941625,
                    3300.0,5.8829976989207609,
                    ]
                
        if mass == 160:
            if region == 0:
                # data: mu,tanb, mu,tanb,...
                data = [
                    2100.0, 1.0,
                    2200.0, 1.02422159335,
                    2300.0, 1.08377843676,
                    2400.0, 1.14982858135,
                    2500.0, 1.21481363254,
                    2600.0, 1.28638706473,
                    2700.0, 1.36693079774,
                    2800.0, 1.45555077965,
                    2900.0, 1.55752458919,
                    3000.0, 1.67940462652,
                    3100.0, 1.83996637387,
                    3200.0, 2.07951769161,
                    3200.0, 3.7056055193,
                    3100.0, 4.41270106234,
                    3000.0, 5.11492733086,
                    2900.0, 1.87379425719,
                    2800.0, 1.66766980808,
                    2700.0, 1.52517606186,
                    2600.0, 1.41212431659,
                    2500.0, 1.31913115013,
                    2400.0, 1.23845117716,
                    2300.0, 1.16391301604,
                    2200.0, 1.09164324755,
                    2100.0, 1.02863335196
                    ]
            if region == 1:
                data = [
                    3300.0, 9.96074171437,
                    3200.0, 10.1585621729,
                    3100.0, 10.3398432486,
                    3000.0, 10.4979847141,
                    2900.0, 10.6294547615,
                    2800.0, 10.7290709319,
                    2700.0, 10.7888601949,
                    2600.0, 10.7954788427,
                    2500.0, 10.7233319198,
                    2400.0, 10.513650499,
                    2300.0, 10.0063902203,
                    2300.0, 7.28173954291,
                    2400.0, 6.24857978033,
                    2500.0, 5.49837102127,
                    2600.0, 4.87513988807,
                    2700.0, 4.32059454326,
                    2800.0, 3.79702291518,
                    2900.0, 3.25389442957,
                    3000.0, 6.01788776183,
                    3100.0, 5.93768032095,
                    3200.0, 5.84558090543,
                    3300.0, 5.75004307772,
                    ]

        if len(data) == 0:
            return None
        
        x = []
        y = []
        for i in range(len(data)/2):
            xp = data[2*i]
            yp = data[2*i+1]
            x.append(xp)
            y.append(yp)

        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("mhLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        #retGraph.SetFillColor(ROOT.TColor.GetColor("#ffffcc"))
        retGraph.SetFillColor(7)
        retGraph.SetFillStyle(3008)
        return retGraph

    def muLimit(self,hmass,xVariableName,selection,obsLimit):

        print "    mu limit",hmass,obsLimit

        x = []
        y = []

        mus = self.getValues("mu","mHp==%s"%hmass)
        highTanbRegion = False

        for mu in mus:
            xval = mu
            yselection = xVariableName+"=="+str(xval) + "&&" + "mHp==%s"%hmass
            if len(selection) > 0:
                yselection += "&&"+selection

            graph = self.getGraph("tanb","BR_tHpb*BR_Hp_taunu","mu==%s&&mHp==%s"%(xval,hmass))
            first = graph.GetX()[0]
            last = graph.GetX()[graph.GetN()-1]
            crossOverPoints0,crossOverPoints1,directions = self.getCrossOver(graph,obsLimit)
            ys = []
            for i in range(len(crossOverPoints0)):
                tanbmin = crossOverPoints0[i]
                tanbmax = crossOverPoints1[i]
                self.nInterpolation = 0
                limit = self.linearBRInterpolation(self.BRvariable,obsLimit,tanbmin,tanbmax,self.floatSelection(yselection))
                #print tanbmin,tanbmax,limit
                ys.append(limit)
            #print ys
            if len(directions) == 0 or (len(directions) > 0 and directions[0] < 0):
                tmp = [first]
                tmp.extend(ys)
                ys = tmp
            if len(ys)%2:
                ys.append(last)
            #print xval,ys
            if len(ys) > 0:
                x.append(xval)
                y.append(ys)

        xgr = []
        ygr = []
        for i in range(len(x)):
            if len(y[i]) > 0:
                xgr.append(x[i])
                ygr.append(y[i][0])
        for i in reversed(range(len(x))):
            if i < len(x) and not len(y[i]) == len(y[i-1]):
                break
            if len(y[i]) > 1:
                xgr.append(x[i])
                ygr.append(y[i][1])
                if i == 0 and x[i] == mus[0]:
                    xgr.append(0)
                    ygr.append(y[i][1])
        for i in range(len(x)):
            if len(y[i]) > 2:
                xgr.append(x[i])
                ygr.append(y[i][2])
        yi = 3
        for i in reversed(range(len(x))):
            if len(y[i]) > yi:
                xgr.append(x[i])
                ygr.append(y[i][yi])
            if i < len(x) and not len(y[i]) == len(y[i-1]):
                    yi = 1

        xgr.append(x[0])
        ygr.append(y[0][0])

#        for i in range(len(xgr)):
#            print xgr[i],ygr[i]

        retGraph = ROOT.TGraph(len(xgr),array('d',xgr,),array('d',ygr))
        retGraph.SetName("muLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        retGraph.SetFillColor(8)
        retGraph.SetFillStyle(3008)
        return retGraph

    def muLimit_mA(self,mA,xVariableName,selection):

        print "    mu limit, mA =",mA

        x = []
        y = []

        mus = self.getValues(xVariableName,"mA==%s"%mA)
        highTanbRegion = False

        for mu in mus:
            xval = mu
            yselection = xVariableName+"=="+str(xval) + "&&" + "mA==%s"%mA
            if len(selection) > 0:
                yselection += "&&"+selection

            print yselection    
            graph = self.getGraph("tanb","BR_tHpb*BR_Hp_taunu","mu==%s&&mA==%s"%(xval,mA))
            xg,yg = self.graph2arrays(graph)
            first = xg[0]
            last = xg[len(xg)-1]
            crossOverPoints0 = []
            crossOverPoints1 = []
            directions = []
            for i in range(len(xg)-1):
                tanb = xg[i]
                br   = yg[i]
                mHpselection = yselection + "&& tanb == %s"%tanb
                mHp = self.getMHp(mA,mHpselection)
                expBRlimit = self.getExpLimitInterpolated(mHp,mHpselection)
                #print "Target brlimit",mHp,tanb,expBRlimit,br

                x0 = xg[i]
                y0 = yg[i]

                x1 = xg[i+1]
                y1 = yg[i+1]
                
                limit = expBRlimit

                if y0 < limit and y1 > limit:
                    crossOverPoints0.append(x0)
                    crossOverPoints1.append(x1)
                    directions.append(1)
                    print "Target brlimit",mHp,tanb,expBRlimit,br
                if y0 > limit and y1 < limit:
                    crossOverPoints0.append(x0)
                    crossOverPoints1.append(x1)
                    directions.append(-1)
                    print "Target brlimit",mHp,tanb,expBRlimit,br

            ys = []
            for i in range(len(crossOverPoints0)):
                tanbmin = crossOverPoints0[i]
                tanbmax = crossOverPoints1[i]

                mHpselection = yselection + "&& tanb == %s"%tanbmin
                mHp = self.getMHp(mA,mHpselection)
                #print "check mHp",mHp,mA,tanbmin,mu
                expBRlimit = self.getExpLimitInterpolated(mHp,mHpselection)
                obsLimit = expBRlimit

                self.nInterpolation = 0
                limit = self.linearBRInterpolation(self.BRvariable,obsLimit,tanbmin,tanbmax,self.floatSelection(yselection))
                ys.append(limit)

            if len(directions) == 0 or (len(directions) > 0 and directions[0] < 0):
                tmp = [first]
                tmp.extend(ys)
                ys = tmp
            if len(ys)%2:
                ys.append(last)

            if len(ys) > 0:
                x.append(xval)
                y.append(ys)

        xgr = []
        ygr = []
        for i in range(len(x)):
            if len(y[i]) > 0:
                xgr.append(x[i])
                ygr.append(y[i][0])
        for i in reversed(range(len(x))):
            if i < len(x) and not len(y[i]) == len(y[i-1]):
                break
            if len(y[i]) > 1:
                xgr.append(x[i])
                ygr.append(y[i][1])
                if i == 0 and x[i] == mus[0]:
                    xgr.append(0)
                    ygr.append(y[i][1])
        for i in range(len(x)):
            if len(y[i]) > 2:
                xgr.append(x[i])
                ygr.append(y[i][2])
        yi = 3
        for i in reversed(range(len(x))):
            if len(y[i]) > yi:
                xgr.append(x[i])
                ygr.append(y[i][yi])
            if i < len(x) and not len(y[i]) == len(y[i-1]):
                    yi = 1

        xgr.append(x[0])
        ygr.append(y[0][0])

        retGraph = ROOT.TGraph(len(xgr),array('d',xgr,),array('d',ygr))
        retGraph.SetName("muLimit")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        retGraph.SetFillColor(8)
        retGraph.SetFillStyle(3008)
#        self.PrintGraph(retGraph)
        for i in range(len(xgr)):
            print "    x.append(",xgr[i],"); y.append(",ygr[i],")"
        return retGraph

    def graph2arrays(self,graph):
        x = []
        y = []
        for i in range(graph.GetN()):
            x.append(graph.GetX()[i])
            y.append(graph.GetY()[i])
        return x,y

    def getCrossOver(self,graph,limit):
        crossover0 = []
        crossover1 = []
        direction = []
        for i in range(0,graph.GetN()-1):
            x0 = graph.GetX()[i]
            y0 = graph.GetY()[i]
            x1 = graph.GetX()[i+1]
            y1 = graph.GetY()[i+1]
            if y0 < limit and y1 > limit:
                crossover0.append(x0)
                crossover1.append(x1)
                direction.append(1)
            if y0 > limit and y1 < limit:
                crossover0.append(x0)
                crossover1.append(x1)
                direction.append(-1)
        return crossover0,crossover1,direction

    def getIsoMass(self,mHp,xaxis="mA"):
        print "Calculating isomass line for mHp =",mHp
        x = []
        y = []

        sele = self.selection
        #print "selection",sele
        tanbs = self.getValues("tanb",sele,roundValues=-1)
        for tanb in tanbs:
#            if not tanb == 25:
#                continue
            selection = "tanb==%s"%tanb
            mHps = self.getValues("mHp",selection,roundValues=-1)
            #print "check mHps",mHps
            mAs = []
            for m in mHps:
                sele = self.floatSelection(selection+"&&mHp==%s"%m)
                value = self.getValues(xaxis,sele,roundValues=-1)
                mAs.append(value[0])
            mgraph = ROOT.TGraph(len(mHps),array("d",mHps),array("d",mAs))
#            self.PrintGraph(mgraph)
#            print 
#            mA = mgraph.Eval(mHp,0,"S")
            mA = mgraph.Eval(mHp)
#            print mHp,mA
            if mA < 0:
                continue
            x.append(mA)
            y.append(tanb)
#            print "x,y",x,y
#            sys.exit()
        xarea = 160
	if mHp > 175:
            xarea = 100
        
	x.append(xarea)
        y.append(75)

        x.append(xarea)
        y.append(1)

        x.append(x[0])
        y.append(y[0])
        
        #for i in range(0,len(x)):
            #print "isomass:  m,tanb",x[i],y[i]

        retGraph = ROOT.TGraph(len(x),array('d',x,),array('d',y))
        retGraph.SetName("isomass")
        retGraph.SetLineWidth(1)
        retGraph.SetLineStyle(7)
        retGraph.SetFillColor(0)
        retGraph.SetFillStyle(1001)
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

#            for i in range(len(mh_vals)):
#                print "          ",mh_vals[i],y_vals[i]

            ys,mh = self.sort(y_vals,mh_vals)
#            for i in range(len(mh)):
#                print "          ",mh[i],ys[i]
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

#        for i in range(len(limits_x)):
#            print "          ",limits_x[i],limits_y[i]
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
        if graph == None:
            return
        print "Converting graph mHp -> mA ..."
        
        #self.PrintGraph(graph)
        for i in xrange(0, graph.GetN()):
            mHp = graph.GetX()[i]
            tanb = graph.GetY()[i]
            #print "check graphToMa",mHp,tanb
            if tanb < 0:
                continue

            massPoint = False
            deltam = 0.001
            for m in [80,90,100,120,140,150,155,160,180,190,200,220,250,300,400,500,600]:
                if self.isbetween(mHp,m-deltam,m+deltam):
                    massPoint = True
                    
            if massPoint:        
                sele = self.floatSelection("mHp==%s"%mHp)
                tanbs = self.getValues("tanb",sele,roundValues=-1)
                closestValues = [999,999]
                for t in tanbs:
                    if abs(t - tanb) < abs(closestValues[0] - tanb):
                        closestValues[0] = t
                        if abs(closestValues[0] - tanb) < abs(closestValues[1] - tanb):
                            tmp = closestValues[1]
                            closestValues[1] = closestValues[0]
                            closestValues[0] = tmp
                        
                #print "check closestValues",closestValues
                mAs = []
                for j in range(len(closestValues)):
                    mAval = self.getValues("mA",sele + "&&"+ self.floatSelection("tanb==%s"%closestValues[j]),roundValues=-1)
                    mAs.append(mAval[0])
                #print "check mAs",mAs
                mgraph = ROOT.TGraph(len(closestValues),array("d",closestValues),array("d",mAs))
                mA = mgraph.Eval(tanb,None,"S")
                #print "check mA",mA

                if mHp == 600:
                    mA = mHp
            elif mHp < 0.0001 or mHp == 1000:
                mA = mHp
            else:
                selection = "tanb==%s"%tanb
                mHps = self.getValues("mHp",selection,roundValues=-1)
                #print "check mHps",mHps
                mAs = []
                for x in mHps:
                    sele = self.floatSelection(selection+"&&mHp==%s"%x)
                    value = self.getValues("mA",sele,roundValues=-1)
                    #print "print check graphToMa",x,value[0]
                    mAs.append(value[0])
                mgraph = ROOT.TGraph(len(mHps),array("d",mHps),array("d",mAs))
                mA = mgraph.Eval(mHp,None,"S")
                
            #print "    mHp = %.2f -> mA = %.2f at tanbeta = %.1f"%(mHp, mA, tanb)
            graph.SetPoint(i, mA, tanb)
        
    def getGraph(self,xVariable,yVariable,selection):
        graph = ROOT.TGraph()
        self.tree.Draw(yVariable+":"+xVariable,self.floatSelection(selection))
        graph = ROOT.gPad.GetPrimitive("Graph")
        if graph == None:
            raise Exception("Error: could not find graph!")
        graph.Sort()
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

    def getExpLimitInterpolated(self,mHp,selection):
        massKeys = self.expLimit.keys()
        massValues = []
        for m in massKeys:
            massValues.append(int(m))
        massValues = sorted(massValues)
        massMin = 0
        massMax = 999
        for i in range(0,len(massValues)-1):
            if massValues[i] == mHp:
                return self.expLimit[str(massValues[i])]
            if massValues[i] < mHp and massValues[i+1] > mHp:
                x1 = massValues[i]
                y1 = float(self.expLimit[str(massValues[i])])
                x2 = massValues[i+1]
                y2 = float(self.expLimit[str(massValues[i+1])])
                return self.linearFunction(mHp,x1,y1,x2,y2)
        for i in reversed(range(1,len(massValues))):
            if massValues[i] < mHp and massValues[i-1] < mHp:
                x1 = massValues[i-1]
                y1 = float(self.expLimit[str(massValues[i-1])])
                x2 = massValues[i]
                y2 = float(self.expLimit[str(massValues[i])])
                return self.linearFunction(mHp,x1,y1,x2,y2)

        print "getExpLimitInterpolated: Mass out of range, exiting.."
        sys.exit()

    def getMHp(self,mA,selection):
        mAs = self.getValues("mA",selection,roundValues=-1)
        sele = self.floatSelection(selection+"&&mA==%s"%mA)
        mHp = self.getValues("mHp",sele,roundValues=-1)
        if len(mHp) > 1:
            print "getMHp: more than 1 mHp found, exiting..",mHp,mA,sele 
            sys.exit()
        return mHp[0]

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
    
    def getValues(self,variable,selection,roundValues=0,sort=True):
        #print "check getValues",variable,selection
        if not self.selection == "" and not selection == "":
            selection = self.selection+"&&"+selection
        values = []
####        graph = self.getGraph("tanb",variable,self.floatSelection(selection))
        if variable == "tanb":
####            graph = self.getGraph("mHp",variable,selection)
            graph = self.getGraph("mHp",variable,self.floatSelection(selection))
        else:
            graph = self.getGraph("tanb",variable,self.floatSelection(selection))
        for i in range(0,graph.GetN()):
            value = graph.GetY()[i]
            if roundValues >= 0:
                value = round(value,roundValues)
            if not value in values:
                values.append(value)
        if sort or variable == "tanb":
            return sorted(values)
        #print "check getValues return",values
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

    def getMinMaxTanb(self,variable,target,selection,highTanbRegion):
        previous = 0
        tanb = -1

        minTanb = self.getMinimumTanb(variable,selection)
        #print "check getMinMaxTanb minTanb",minTanb
        graph = self.getGraph("tanb",variable,selection)
        if highTanbRegion:
            for i in range(graph.GetN()):
                x = graph.GetX()[i]
                y = graph.GetY()[i]
                #print "    x,y,target",x,y,target
                if y == target:
                    return x,x
                if x > minTanb and y > target:
                    #print "check MIN,MAX",variable,target,selection,highTanbRegion,previous,x
                    return previous,x
                previous = x
        else:
            for i in reversed(range(graph.GetN())):
                x = graph.GetX()[i]
                y = graph.GetY()[i]
                #print "    x,y,target",x,y,target
                if x > minTanb:
                    continue
                #print "    x,y,target",x,y,target
                if y == target:
                    return x,x
                if y > target:
                    #print "check MIN,MAX",variable,target,selection,highTanbRegion,previous,x
                    return x,previous
                previous = x

        """
        for i in range(graph.GetN()):
            x = graph.GetX()[i]
            y = graph.GetY()[i]
            print "    x,y,target",x,y,target
            if y == target:
                return x,x
            if highTanbRegion:
                if x > minTanb and y > target:
                    #print "check MIN,MAX",variable,target,selection,highTanbRegion,previous,x
                    return previous,x
            else:
                if x < minTanb and y < target:
                    #print "check MIN,MAX",variable,target,selection,highTanbRegion,previous,x
                    return previous,x
            previous = x
        """    
        return None,None    
            
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
            selectionVariables = self.getCutVariables(selection)
            if "tanb" in selectionVariables:
                xs = self.getValues("mHp",selection,roundValues=-1)
                print "mHp      ",variable
                for x in xs:
                    if len(selection) > 0:
                        sele = self.floatSelection(selection+"&&mHp==%s"%x)
                    else:
                        sele = self.floatSelection("mHp==%s"%x)
                    value = self.getValues(variable,sele,roundValues=-1)
                    xstr = str(x)
                    while len(xstr) < 10:
                        xstr += " "
                    print xstr,value[0]
            else:    
                tanbs = self.getValues("tanb",selection,roundValues=-1)
                print "tanb      ",variable
                for tanb in tanbs:
                    if len(selection) > 0:
                        sele = self.floatSelection(selection+"&&tanb==%s"%tanb)
                    else:
                        sele = self.floatSelection("tanb==%s"%tanb)
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
        self.nInterpolation += 1
#        print "check linearBRInterpolation",variable,target,min,max,selection
#        print "      interpolation iteration round",self.nInterpolation
#        print "      self.getMinimum(variable,selection)",self.getMinimum(variable,selection)
#        print "      self.getMaximum(variable,selection)",self.getMaximum(variable,selection)

#        print "tanbs",len(self.getValues("tanb",selection,roundValues=-1)),self.getValues("tanb",selection,roundValues=-1)
#        print variable,len(self.getValues(variable,selection,roundValues=-1))

#        min,max = self.getMinMaxTanb(variable,target,selection,False)
#        print "check new min,max",min,max

        if min == None or max == None:
            return 1

        if min >= max:
            newMin = 999
            newMax = 0
            tanbs = self.getValues("tanb",selection,roundValues=-1)
            values = self.getValues(variable,selection,roundValues=-1)
            for i in range(0,len(tanbs)-1):
#                if tanb < 10:
#                    continue
#                value = self.getOLD(variable,selection+"&&tanb=="+str(tanb))
                #print "tanb,value",tanbs[i],values[i],min,max
                if values[i] < target:
                    newMin = tanbs[i]
                else:
                    newMax = tanbs[i]
                    break
            min = newMin
            max = newMax

        if target < self.getMinimum(variable,selection):
            #print "Warning,",variable,"target",target,"< minimum possible value",self.getMinimum(variable,selection),selection
            return self.getMinimumTanb(variable,selection)
        if target > self.getMaximum(variable,selection):
            #print "Warning,",variable,"target",target,"> maximum possible value",self.getMaximum(variable,selection),selection
            if max < 10:
                return -1
            return 100
        if max <= self.getMinimumTanb(variable,selection) and target > self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)):
            #print "Warning,",variable,"target",target,"> maximum possible value (at tanb<",self.getMinimumTanb(variable,selection),")",self.getMaximum(variable,selection+"&&tanb<%s"%self.getMinimumTanb(variable,selection)),selection
            return -1
        
        x1 = float(min)
        y1 = self.interpolate(variable,x1,selection)
        x2 = float(max)
        y2 = self.interpolate(variable,x2,selection)
        #print "    check linInt x1,y1,x2,y2",x1,y1,x2,y2
        if x1 < 1 and x2 < 1:
            return 1
        #low tanb region br increases as tanb decreases. To prevent patological oscillation which never converges

        # y = ax+b
        b = float(x1*y2 - y1*x2)/(x1-x2)
        a = float(y1-b)/x1
        x = (target - b)/a
        #print "    check x",x
        newx1 = self.lowerPoint("tanb",x,selection)
        newx2 = self.higherPoint("tanb",x,selection)
        #print "    check newx1,newx2 a",newx1,newx2
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
            #print "check lin interpolation result",x
            return x
        else:
            if self.nInterpolation < 10:
                return self.linearBRInterpolation(variable,target,newx1,newx2,selection)
            else:
                # linear interpolation failed
                print "Linear BR interpolation failed, maximum number of iterations reached,",self.nInterpolation
                print "Switching to tgraph BR interpolation"
                print "check return",self.tgraphBRInterpolation(variable,target,selection)
                sys.exit()
                return self.tgraphBRInterpolation(variable,target,selection)

    def tgraphBRInterpolation(self,variable,target,selection):
        #print "check tgraphBRInterpolation",self.BRvariable,target
        graph = self.getGraph("tanb",self.BRvariable,selection)
        x = graph.GetX()
        y = graph.GetY()
        reversedGraph = ROOT.TGraph(graph.GetN(),y,x)
        self.PrintGraph(graph,"tgraphBRInterpolation")
#        self.PrintGraph(reversedGraph,"tgraphBRInterpolation reversed")
#        print reversedGraph.Eval(target,None,"S")
        sys.exit()
        return graph.Eval(target,None,"S")
                    
    def getTanbFromLightHpBR(self,targetBR,selection,highTanbRegion=True):
	# for light H+
        tanbmin,tanbmax = self.getMinMaxTanb(self.BRvariable,targetBR,self.floatSelection(selection),highTanbRegion) 
#        tanbmin = 2
#        tanbmax = 5
#        if highTanbRegion:
#            tanbmin = 10
#            tanbmax = 20
        self.nInterpolation = 0    
        return self.linearBRInterpolation(self.BRvariable,targetBR,tanbmin,tanbmax,self.floatSelection(selection))
            
    def getCutValue(self,variable,selection):
	var_re = re.compile(variable+"==(?P<value>(\d+))")
	for s in selection.split("&&"):
	    match = var_re.search(s)
	    if match:
		return float(match.group("value"))
	return -1

    def getCutVariables(self,selection):
        variables = []
        var_re = re.compile("(?P<variable>(\S+))==(?P<value>(\d+))")
        for s in selection.split("&&"):
            match = var_re.search(s)
            if match:
                variables.append(match.group("variable"))
        return variables

    def PrintGraph(self,graph,comment=""):
        print comment
        for i in range(graph.GetN()):
            x = graph.GetX()[i]
            y = graph.GetY()[i]
            print x,y


    def getVersion(self,regexp):
        version_re = re.compile(regexp+"_version *= *(?P<version>\S+)")
        keys = self.fIN.GetListOfKeys()
        for i in range(len(keys)):
            keyName = keys.At(i).GetName()
            match = version_re.search(keyName)
            if match:
                return regexp + " " + match.group("version")
        return None

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
#        db.Print(variable="mH",selection="mA==110 && mu==3300")
#        db.Print(variable="BR_tHpb*BR_Hp_taunu",selection="mA==110 && mu==3300")
#        db.Print(variable="mHp",selection="mA==110 && mu==3300")

#        db.Print(variable="0.001*2*tHp_xsec*BR_Hp_taunu",selection="mHp==200")
        db.Print(variable="tHp_xsec",selection="mHp==200 && tanb== 40")

#        db.getExpLimitInterpolated(120,"")

#        graph = db.getIsoMass(160)
        
#        x = array('d',[180.0,190,200.0,220.0,250.0,300.0,400])
#        y = array('d',[26.8026641155,29.014188416,30.7101331784,35.8734454992,43.1435998472,52.0940183849,75.0])
#        graph1 = ROOT.TGraph(len(x),x,y)
#        db.graphToMa(graph1)
        
#        min,max = db.getMinMaxTanb("BR_tHpb*BR_Hp_taunu",0.0027,"mHp>159.99&&mHp<160.01&&mu>199.99&&mu<200.01",False)
#        print "check min,max",min,max
        sys.exit()
#        print db.getVersion("FeynHiggs")

#	db.Print()
#        db.Print(variable="mA",selection="mHp==200")
#        db.Print(variable="mA",selection="tanb==21")
#        db.Print(variable="BR_tHpb*BR_Hp_taunu",selection="mHp==160")
#        db.Print(variable="BR_Hp_taunu",selection="mHp==200")
	db.Print(variable="0.001*2*tHp_xsec*BR_Hp_taunu",selection="mHp==200")
        print "------------------------------------------------------------"
#        db.Print(variable="mh",selection="mHp==400")
#        db.Print(variable="2*0.001*tHp_xsec*BR_Hp_taunu",selection="mHp==500")

#        tanb = 20
#        selection = "mHp==200&&tanb==%s"%(tanb)
#        mA = db.get("tanb","mA",selection)
#        print "check graphToMa",selection,mA, tanb

        sys.exit()
        print "------------------------------------------------------------"
#        graph = db.mhLimit("mh","mHp","mu==200","125.9+-3.0")
#        for i in range(graph.GetN()):
#            print "check graph",graph.GetX()[i],graph.GetY()[i]

        x = [500,600]
        y = [30,40]
        graph = ROOT.TGraph(len(x),array("d",x),array("d",y))
        db.graphToMa(graph)
        db.PrintGraph(graph,"test graph")
        sys.exit()
#        db.Print(variable="BR_Hp_taunu",selection="mHp==155&&mu==200&&Xt==2000&&m2==200")
        """
	db.setSelection("mu==200&&Xt==2000&&m2==200")
        db.mhLimit("mHp","mu==200&&Xt==2000&&m2==200","125.9+-0.6+-0.2")
        """
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
