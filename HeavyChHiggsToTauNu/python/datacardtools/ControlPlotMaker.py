## \package ControlPlotMaker
# Classes for making control plots (surprise, surprise ...)

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import TDRStyle
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count

from math import pow,sqrt,log10
import os
import sys
import ROOT

##
class ControlPlotMaker:
    ## Constructor
    def __init__(self, opts, config, dirname, luminosity, observation, datasetGroups):
        if config.ControlPlots == None:
            return
        self._opts = opts
        self._config = config
        self._dirname = dirname
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups

        myEvaluator = SignalAreaEvaluator()

        # Make control plots
        print "\n"+HighlightStyle()+"Generating control plots"+NormalStyle()
        # Loop over mass points
        for m in self._config.MassPoints:
            selectionFlow = SelectionFlowPlotMaker(config, m)
            myBlindingCount = 0
            for c in self._config.ControlPlots:
                myMassSuffix = "_M%d"%m
                # Obtain frame
                hFrame = self._makeFrame(c.title+myMassSuffix+"Frame", c.details)
                # Obtain histograms
                hSignalHH = self._getControlPlot(m, c.details, c.signalHHid, c.title,"HH"+myMassSuffix)
                hSignalHW = self._getControlPlot(m, c.details, c.signalHWid, c.title,"HW"+myMassSuffix)
                hQCD = self._getControlPlot(m, c.details, c.QCDid, c.title,"QCD"+myMassSuffix)
                hEmbedded = self._getControlPlot(m, c.details, c.embeddingId, c.title,"EWKtau"+myMassSuffix)
                hEWKfake = self._getControlPlot(m, c.details, c.EWKfakeId, c.title,"EWKfake"+myMassSuffix)
                hData = self._getControlPlot(m, c.details, None, c.title,"Data"+myMassSuffix, c.blindedRange)
                # Obtain total expected and total signal
                hExpected = self._getExpectedPlot(c.details, c.title+myMassSuffix, [hQCD, hEmbedded, hEWKfake])
                hSignal = self._getSignalPlot(c.details, c.title+myMassSuffix, hSignalHH, hSignalHW)
                # Add data to selection flow plot
                if c.flowPlotCaption != "":
                    if myBlindingCount > 0:
                        selectionFlow.addColumn(label=c.flowPlotCaption,signal=hSignal,qcd=hQCD,EWKtau=hEmbedded,EWKfake=hEWKfake,data=None,expected=hExpected)
                    else:
                        selectionFlow.addColumn(label=c.flowPlotCaption,signal=hSignal,qcd=hQCD,EWKtau=hEmbedded,EWKfake=hEWKfake,data=hData,expected=hExpected)
                    if len(c.blindedRange) > 0:
                        myBlindingCount += 1
                # Apply blinding 
                if len(c.blindedRange) > 0:
                    self._applyBlinding(hData,c.blindedRange)
                # Obtain ratio plot
                hRatio = self._getRatioPlot(c.title+myMassSuffix, hData, hExpected)
                # Evaluate signal region
                if len(c.evaluationRange) > 0:
                    myEvaluator.addEntry(m,c.title,c.evaluationRange,hSignal,hQCD,hEmbedded,hEWKfake)
                # Construct plot and save
                self._construct(m,c.details,"M%d_ControlPlot_"%m+c.title,hFrame,hData,hSignal,hQCD,hEmbedded,hEWKfake,hExpected,hRatio,luminosity)
                # Delete histograms from memory
                hSignalHH.IsA().Destructor(hSignalHH)
                hSignalHW.IsA().Destructor(hSignalHW)
                hData.IsA().Destructor(hData)
                hQCD.IsA().Destructor(hQCD)
                hEmbedded.IsA().Destructor(hEmbedded)
                hEWKfake.IsA().Destructor(hEWKfake)
                hExpected.IsA().Destructor(hExpected)
                hSignal.IsA().Destructor(hSignal)
                hRatio.IsA().Destructor(hRatio)
            # Make selection flow plot
            hSelectionFlowRatio = self._getRatioPlot("SelectionFlow"+myMassSuffix,selectionFlow.data,selectionFlow.expected)
            self._construct(mass=m,details=selectionFlow.plotDetails,title="M%d_SelectionFlow_"%m,
                            hFrame=selectionFlow.hFrame,hData=selectionFlow.data,hSignal=selectionFlow.signal,
                            hQCD=selectionFlow.qcd,hEmbedded=selectionFlow.EWKtau,hEWKfake=selectionFlow.EWKfake,
                            hExpected=selectionFlow.expected,hRatio=hSelectionFlowRatio,luminosity=luminosity)
            hSelectionFlowRatio.IsA().Destructor(hSelectionFlowRatio)
        myEvaluator.save(dirname)
        print "Control plots done"

    def _getControlPlot(self, mass, details, columnIdList, title, titleSuffix, blindedRange = []):
        myShapeModifier = ShapeHistoModifier(details)
        myHisto = myShapeModifier.createEmptyShapeHistogram(title+titleSuffix)
        #mySystHisto = myShapeModifier.createEmptyShapeHistogram(title+"Syst"+titleSuffix)
        if columnIdList == None:
            # Data
            h = self._observation.getControlPlotByTitle(title)
            myShapeModifier.addShape(source=h,dest=myHisto)
        else:
            for g in self._datasetGroups:
                if g.isActiveForMass(mass):
                    # Find column with correct id
                    for c in columnIdList:
                        if g.getLandsProcess() == c:
                            h = g.getControlPlotByTitle(title)
                            # Add systematic uncertainty (yes, we have here access to full systematics!)
                            mySystError = 0.0
                            for result in g.getNuisanceResults():
                                if not result.resultIsStatUncertainty(): # ignore stat. uncert.
                                    # take average error from plus and minus if nuisance is shape stat or asymmetric
                                    if not ("QCD" in g.getLabel()):
                                        mySystError += pow(result.getResultAverage(),2)
                                    #print "group",g.getLabel(),"id",result.getId(),"syst",result.getResultAverage()
                            # Apply systematic uncertainty to shape histogram
                            #print "group",g.getLabel(),"syst=",sqrt(mySystError)
                            for i in range(1,h.GetNbinsX()+1):
                                h.SetBinError(i,sqrt(pow(h.GetBinError(i),2)+pow(mySystError,2)))
                            # Downscale MC ttbar according to branching ratio
                            if c == 1 or c == 2:
                                h.Scale(pow(1.0-self._config.OptionBr,2))
                            # Add to total histogram
                            myShapeModifier.addShape(source=h,dest=myHisto)
        myShapeModifier.finaliseShape(dest=myHisto)
        #mySystHisto.IsA().Destructor(mySystHisto)
        return myHisto

    def _applyBlinding(self,myHisto,blindedRange = []):
        for i in range (1, myHisto.GetNbinsX()+1):
            # Blind if any edge of the current bin is inside the blinded range or if bin spans over the blinded range
            if ((myHisto.GetXaxis().GetBinLowEdge(i) >= blindedRange[0] and myHisto.GetXaxis().GetBinLowEdge(i) <= blindedRange[1]) or
                (myHisto.GetXaxis().GetBinUpEdge(i) >= blindedRange[0] and myHisto.GetXaxis().GetBinUpEdge(i) <= blindedRange[1]) or 
                (myHisto.GetXaxis().GetBinLowEdge(i) <= blindedRange[0] and myHisto.GetXaxis().GetBinUpEdge(i) >= blindedRange[1])):
                myHisto.SetBinContent(i, -1.0)
                myHisto.SetBinError(i, 0.0)

    def _getExpectedPlot(self, details, title, hlist):
        myShapeModifier = ShapeHistoModifier(details)
        myHisto = myShapeModifier.createEmptyShapeHistogram(title+"Expected")
        for h in hlist:
            myShapeModifier.addShape(source=h,dest=myHisto)
        myShapeModifier.finaliseShape(dest=myHisto)
        return myHisto

    def _getSignalPlot(self, details, title, hh, hw):
        myShapeModifier = ShapeHistoModifier(details)
        myHisto = myShapeModifier.createEmptyShapeHistogram(title+"Signal")
        # Normalise
        hh.Scale(pow(self._config.OptionBr,2))
        myShapeModifier.addShape(source=hh,dest=myHisto)
        hw.Scale(2.0*(1.0-self._config.OptionBr)*self._config.OptionBr)
        myShapeModifier.addShape(source=hw,dest=myHisto)
        # Finalise
        myShapeModifier.finaliseShape(dest=myHisto)
        return myHisto

    ## Returns an empty frame
    def _makeFrame(self, title, details):
        myShapeModifier = ShapeHistoModifier(details)
        h = myShapeModifier.createEmptyShapeHistogram(title)
        return h

    ## Divides two plots with each other
    def _getRatioPlot(self, title, hData, hExpected):
        h = hData.Clone(title+"Ratio")
        h.Divide(hExpected)
        # Remove blinded part
        for i in range (1, h.GetNbinsX()+1):
            if hData.GetBinContent(i) < 0:
                h.SetBinContent(i, -100)
                h.SetBinError(i, 0)
        return h

    ## Sets axis fonts and sizes
    def _setHistoStyle(self, h):
        h.SetTitleFont(43, "xyz")
        h.SetTitleSize(27, "xyz")
        h.SetLabelFont(43, "xyz")
        h.SetLabelSize(24, "xyz")
        h.GetXaxis().SetLabelOffset(0.007)
        h.GetYaxis().SetLabelOffset(0.007)
        h.GetXaxis().SetTitleOffset(3.2)
        h.GetYaxis().SetTitleOffset(1.3)

    ## Creates a TLatex object
    def _createTopCaptionText(self, x, y, title):
        tex = ROOT.TLatex(x,y,title)
        tex.SetNDC()
        tex.SetTextFont(43)
        tex.SetTextSize(27)
        tex.SetLineWidth(2)
        return tex

    ## Creates a TLatex object
    def _createText(self, x, y, title):
        tex = ROOT.TLatex(x,y,title)
        tex.SetNDC()
        tex.SetTextFont(63)
        tex.SetTextSize(20)
        tex.SetLineWidth(2)
        return tex

    # Returns scale factor for max y to avoid overlap of captions or legend
    def _getMaxYFactor(self, low, high, width):
        if low/width < 0.145:
            if high/width > 0.145:
                return 0.81
            else:
                return 1.0
        elif low/width < 0.44:
            if high/width > 0.44:
                return 0.61
            elif high/width > 0.145:
                return 0.81
            else:
                return 1.0
        else:
            return 0.61

    # calculate maximum for frame
    def _findMaxY(self, hSignal, hExpected, hData, logstatus):
        myMax = 0.0
        histoWidth = hSignal.GetXaxis().GetBinUpEdge(hSignal.GetNbinsX()+1) - hSignal.GetXaxis().GetBinLowEdge(0)
        for i in range(1,hSignal.GetNbinsX()+1):
            #obtain max value for bin
            value = hData.GetBinContent(i)+hData.GetBinError(i)
            if hExpected.GetBinContent(i) + hExpected.GetBinError(i) > value:
                value = hExpected.GetBinContent(i) + hExpected.GetBinError(i)
            if hExpected.GetBinContent(i) + hSignal.GetBinContent(i) > value:
                value = hExpected.GetBinContent(i) + hSignal.GetBinContent(i)
            myCeiling = self._getMaxYFactor(hSignal.GetXaxis().GetBinLowEdge(i),hSignal.GetXaxis().GetBinUpEdge(i),histoWidth)
            
            if logstatus:
                value = pow(10,log10(value)/myCeiling)*1.5
            else:
                value = value/myCeiling*1.1
            if value > myMax:
                myMax = value
        return myMax

    ## Constructs canvas object and saves it
    def _construct(self,mass,details,title,hFrame,hData,hSignal,hQCD,hEmbedded,hEWKfake,hExpected,hRatio,luminosity):
        myStyle = TDRStyle()
        myStyle.setOptStat(False)
        # Make canvas
        c = ROOT.TCanvas(title+"Canvas",title+"Canvas",600,600)
        c.Range(0,0,1,1)
        c.cd()
        # Set histo settings
        hFrame.SetMinimum(details["ymin"])
        if hFrame.SetMaximum(details["ymax"]) < 0:
            hFrame.SetMaximum(self._findMaxY(hSignal,hExpected,hData,details["logy"]))
        else:
            hFrame.SetMaximum(details["ymax"])
        hFrame.SetXTitle("")
        # Construct range string to y-axis
        if len(details["unit"]) > 0:
            myRange = ""
            # Check for variable binning
            if len(details["variableBinSizeLowEdges"]) > 0:
                myMinWidth = 1e99
                myMaxWidth = 0
                for i in range(1,hFrame.GetNbinsX()+1):
                    myWidth = hFrame.GetXaxis().GetBinWidth(i)
                    if myWidth < myMinWidth:
                        myMinWidth = myWidth
                    if myWidth > myMaxWidth:
                        myMaxWidth = myWidth
                if myMinWidth == myMaxWidth:
                    if myWidth < 1.0:
                        myRange = "%.1f"%myMinWidth
                    else:
                        myRange = "%d"%myMinWidth
                else:
                    if myWidth < 1.0:
                        myRange = "%.1f-%.1f"%(myMinWidth,myMaxWidth)
                    else:
                        myRange = "%d-%d"%(myMinWidth,myMaxWidth)
            else:
                myWidth = hFrame.GetXaxis().GetBinWidth(1)
                if myWidth < 1.0:
                    myRange = "%.1f"%myWidth
                else:
                    myRange = "%d"%myWidth
            hFrame.SetYTitle(details["ytitle"]+" / %s %s"%(myRange,details["unit"]))
        else:
            hFrame.SetYTitle(details["ytitle"])
        self._setHistoStyle(hFrame)
        hFrame.GetXaxis().SetTitleSize(0)
        hFrame.GetXaxis().SetLabelSize(0)
        hData.SetLineWidth(2)
        hData.SetLineColor(ROOT.kBlack)
        hData.SetMarkerStyle(20)
        hData.SetMarkerSize(1.2)
        hRatio.SetLineWidth(2)
        hRatio.SetLineColor(ROOT.kBlack)
        hRatio.SetMarkerStyle(20)
        hRatio.SetMarkerSize(1.2)
        hRatio.SetMinimum(1.0-details["DeltaRatio"])
        hRatio.SetMaximum(1.0+details["DeltaRatio"])
        if len(details["unit"]) > 0:
            hRatio.SetXTitle(details["xtitle"]+", "+details["unit"])
        else:
            hRatio.SetXTitle(details["xtitle"])
        hRatio.SetYTitle("Data/Exp.")
        hRatio.GetYaxis().SetNdivisions(505)
        ci = ROOT.TColor.GetColor("#ff3399")
        hSignal.SetLineColor(ci)
        hSignal.SetLineStyle(2)
        hSignal.SetLineWidth(2)
        ci = ROOT.TColor.GetColor("#ffcc33")
        hQCD.SetFillColor(ci)
        hQCD.SetLineWidth(0)
        ci = ROOT.TColor.GetColor("#993399")
        hEmbedded.SetFillColor(ci)
        hEmbedded.SetLineWidth(0)
        ci = ROOT.TColor.GetColor("#669900")
        hEWKfake.SetFillColor(ci)
        hEWKfake.SetLineWidth(0)
        hExpected.SetFillColor(1)
        hExpected.SetFillStyle(3354)
        hExpected.SetLineColor(0)
        hExpected.SetLineStyle(0)
        hExpected.SetLineWidth(0)
        hExpected.SetMarkerSize(0)
        # Make stack for expected + signal
        hBkg = ROOT.THStack()
        hBkg.Add(hEWKfake)
        hBkg.Add(hEmbedded)
        hBkg.Add(hQCD)
        hBkg.Add(hSignal)
        # Agreement pad
        apad = ROOT.TPad(title+"apad",title+"apad",0,0,1,.3)
        apad.Draw()
        apad.cd()
        apad.Range(0,0,1,1)
        apad.SetLeftMargin(0.16)
        apad.SetRightMargin(0.05)
        apad.SetTopMargin(0)
        apad.SetBottomMargin(0.34)
        hLine = hRatio.Clone(title+"line")
        for i in range(1, hLine.GetNbinsX()+1):
            hLine.SetBinContent(i,1)
            hLine.SetBinError(i,0)
        hLine.SetLineColor(ROOT.kRed)
        hLine.SetLineWidth(2)
        hLine.SetLineStyle(3)
        self._setHistoStyle(hLine)
        hLine.Draw("hist")
        hRatio.Draw("ex0 same")
        # Cover pad
        c.cd()
        cpad = ROOT.TPad(title+"cpad",title+"cpad",0.105,0.300,0.155,0.36)
        cpad.Draw()
        cpad.cd()
        cpad.Range(0,0,1,1)
        # Plotpad
        c.cd()
        ppad = ROOT.TPad(title+"ppad",title+"ppad",0,0.3,1,1)
        ppad.Draw()
        ppad.cd()
        ppad.Range(0,0,1,1)
        ppad.SetLeftMargin(0.16)
        ppad.SetRightMargin(0.05)
        ppad.SetTopMargin(0.065)
        ppad.SetBottomMargin(0.0)
        if details["logy"]:
            ppad.SetLogy()
        hFrame.Draw()
        hBkg.Draw("hist same")
        hExpected.Draw("e2 same")
        hData.Draw("ex0 same")
        ppad.RedrawAxis()
        # Legend
        leg = ROOT.TLegend(0.53,0.63,0.87,0.91,"","brNDC")
        leg.SetBorderSize(0)
        leg.SetTextFont(63)
        leg.SetTextSize(18)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        #leg.SetFillStyle(4000)
        entry = leg.AddEntry(hData, "Data", "P")
        entry = leg.AddEntry(hSignal, "with H^{#pm}#rightarrow#tau^{#pm}#nu", "L")
        entry = leg.AddEntry(hQCD, "multijets (from data)", "F")
        #entry = leg.AddEntry(hEmbedded, "MC EWK+t#bar{t}", "F")
        entry = leg.AddEntry(hEmbedded, "EWK+t#bar{t} #tau (from data)", "F")
        entry = leg.AddEntry(hEWKfake, "EWK+t#bar{t} no-#tau (simul.)", "F")
        entry = leg.AddEntry(hExpected, "stat. #oplus syst. uncert.", "F")
        leg.Draw()
        # Labels
        CMSCaption = self._createTopCaptionText(0.62,0.945,"CMS Preliminary")
        CMSCaption.Draw()
        SqrtsCaption = self._createTopCaptionText(0.2,0.945,"#sqrt{s} = 7 TeV")
        SqrtsCaption.Draw()
        LumiCaption = self._createTopCaptionText(0.43,0.945,"L=%3.1f fb^{-1}"%(luminosity/1000.0))
        LumiCaption.Draw()
        MassCaption = self._createText(0.28,0.865,"m_{H^{+}} = %d GeV/c^{2}"%mass)
        MassCaption.Draw()
        BrCaption = self._createText(0.28,0.805,"#it{B}(t#rightarrowH^{+}b)=%.2f"%self._config.OptionBr)
        BrCaption.Draw()
        # Finalise
        c.Print(self._dirname+"/"+title+".png")
        c.Print(self._dirname+"/"+title+".eps")
        c.Print(self._dirname+"/"+title+".C")
        c.Close()
        print "Control plot %s generated"%(self._dirname+"/"+title+".png")

class SignalAreaEvaluator:
    def __init__(self):
        self._output = ""

    def addEntry(self,mass,title,evaluationRange,hSignal,hQCD,hEmbedded,hEWKfake):
        # Obtain event counts
        mySignal = self._evaluate(evaluationRange,hSignal)
        myQCD = self._evaluate(evaluationRange,hQCD)
        myEmbedded = self._evaluate(evaluationRange,hEmbedded)
        myEWKfake = self._evaluate(evaluationRange,hEWKfake)
        # Produce output
        myOutput = "%s, mass=%d, range=%d-%d\n"%(title,mass,evaluationRange[0],evaluationRange[1])
        myOutput += "  signal: %f +- %f\n"%(mySignal.value(),mySignal.uncertainty())
        myOutput += "  QCD: %f +- %f\n"%(myQCD.value(),myQCD.uncertainty())
        myOutput += "  EWKtau: %f +- %f\n"%(myEmbedded.value(),myEmbedded.uncertainty())
        myOutput += "  EWKfake: %f +- %f\n"%(myEWKfake.value(),myEWKfake.uncertainty())
        myExpected = Count(0.0, 0.0)
        myExpected.add(myQCD)
        myExpected.add(myEmbedded)
        myExpected.add(myEWKfake)
        myOutput += "  Total expected: %f +- %f\n"%(myExpected.value(),myExpected.uncertainty())
        mySignal.divide(myExpected)
        myOutput += "  signal/expected: %f +- %f\n"%(mySignal.value(),mySignal.uncertainty())
        myOutput += "\n"
        self._output += myOutput

    def save(self,dirname):
        myFilename = dirname+"/signalAreaEvaluation.txt"
        myFile = open(myFilename, "w")
        myFile.write(self._output)
        myFile.close()
        print HighlightStyle()+"Signal area evaluation written to: "+NormalStyle()+myFilename
        self._output = ""

    def _evaluate(self,evaluationRange,h):
        myResult = 0.0
        myError = 0.0
        for i in range(1,h.GetNbinsX()+1):
            if (h.GetXaxis().GetBinLowEdge(i) >= evaluationRange[0] and
                h.GetXaxis().GetBinUpEdge(i) <= evaluationRange[1]):
                myResult += h.GetBinContent(i)
                myError += pow(h.GetBinError(i),2)
        return Count(myResult,sqrt(myError))

class SelectionFlowPlotMaker:
    def __init__(self, config, mass):
        self._config = config
        self._mass = mass
        # Calculate number of bins
        myBinCount = 0
        for c in self._config.ControlPlots:
            if c.flowPlotCaption != "":
                myBinCount += 1
        self.plotDetails = { "bins": myBinCount,
                            "rangeMin": 0.0,
                            "rangeMax": myBinCount,
                            "variableBinSizeLowEdges": [], # if an empty list is given, then uniform bin width is used
                            "xtitle": "Step",
                            "ytitle": "Events",
                            "unit": "",
                            "logy": True,
                            "DeltaRatio": 0.5,
                            "ymin": 0.9,
                            "ymax": -1 }
        # Make an empty frame
        myPlotName = "SelectionFlow_%d"%mass
        self.hFrame = ROOT.TH1F(myPlotName,myPlotName,myBinCount,0,myBinCount)
        self.hFrame.SetYTitle("Events")
        # Make empty histograms for HH, HW, QCD, EWKtau, EWKfake, datacard
        self.signal = self.hFrame.Clone("SelectionFlow_signal_%d"%mass)
        self.qcd = self.hFrame.Clone("SelectionFlow_qcd_%d"%mass)
        self.EWKtau = self.hFrame.Clone("SelectionFlow_EWKtau_%d"%mass)
        self.EWKfake = self.hFrame.Clone("SelectionFlow_EWKfake_%d"%mass)
        self.data = self.hFrame.Clone("SelectionFlow_data_%d"%mass)
        self.expected = self.hFrame.Clone("SelectionFlow_expected_%d"%mass)
        # Initialise column pointer
        self._myCurrentColumn = 0

    def addColumn(self,label,signal,qcd,EWKtau,EWKfake,data,expected):
        self._myCurrentColumn += 1
        self.data.GetXaxis().SetBinLabel(self._myCurrentColumn, label)
        self._addColumnData(signal,self.signal,self._myCurrentColumn)
        self._addColumnData(qcd,self.qcd,self._myCurrentColumn)
        self._addColumnData(EWKtau,self.EWKtau,self._myCurrentColumn)
        self._addColumnData(EWKfake,self.EWKfake,self._myCurrentColumn)
        if data != None:
            self._addColumnData(data,self.data,self._myCurrentColumn)
        else:
            # Blinding
            self.data.SetBinContent(self._myCurrentColumn,-1)
            self.data.SetBinError(self._myCurrentColumn,0)
        self._addColumnData(expected,self.expected,self._myCurrentColumn)
 
    def _addColumnData(self,source,dest,bin):
        # Set value
        dest.SetBinContent(bin,source.Integral())
        # Set error
        myError = 0.0
        for i in range(1,source.GetNbinsX()+1):
            myError += pow(source.GetBinError(i),2)
        dest.SetBinError(bin,sqrt(myError))
