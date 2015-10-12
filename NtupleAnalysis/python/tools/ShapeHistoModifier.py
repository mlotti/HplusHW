import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import ROOT
from array import array
from math import sqrt

## Class for treating properly shape histograms with different axis ranges and or binning
# Allows tuning of shape histogram without having to rerun full analysis
# Note: After the adding is done, remember to call finalise! (adding treats errors as squares, finalising takes the sqrt of the squares)
class ShapeHistoModifier():
    def __init__(self, histoSpecs, histoObjectForSpecs=None, debugMode=False):
        if isinstance(histoSpecs,list):
            raise Exception(ShellStyles.ErrorLabel()+"ShapeHistoModifier: Requested a %d-dimensional histogram, but code currently supports only 1 dimension!"%len(histoSpecs))
        mySpecs = self._retrieveHistoSpecsFromHisto(histoObjectForSpecs, histoSpecs)
        self._nbins = mySpecs["bins"]
        self._min = mySpecs["rangeMin"]
        self._max = mySpecs["rangeMax"]
        self._binLowEdges = list(mySpecs["variableBinSizeLowEdges"])
        self._xtitle = mySpecs["xtitle"]
        self._ytitle = mySpecs["ytitle"]
        # Variable bin widths support
        if len(self._binLowEdges) == 0:
            # Create bins with uniform width
            binwidth = (self._max-self._min) / self._nbins
            for i in range(0,self._nbins):
                self._binLowEdges.append(i*binwidth+self._min)
        if debugMode:
            print "ShapeHistoModifier: nbins=%d, range=%f-%f"%(self._nbins,self._min,self._max)
            print"  bin low edges:",self._binLowEdges

    ## Returns an empty histogram created according to the specifications
    def createEmptyShapeHistogram(self, name, title=None):
        myEdges = self._binLowEdges
        myEdges.append(self._max) # ROOT needs bins+1 numbers, where the last one is the right edge of last bin
        h = None
        if title == None:
            h = ROOT.TH1F(name, name, self._nbins,array('f',myEdges))
        else:
            h = ROOT.TH1F(name, title, self._nbins,array('f',myEdges))
        h.Sumw2()
        h.SetXTitle(self._xtitle)
        h.SetYTitle(self._ytitle)
        return h


    ## Adds shape from the source to the destination histogram
    # Returns list of possible messages
    def addShape(self, source, dest, weight=1.0):
        return self._calculateShape(source,dest,weight,"+")

    ## Adds shape from the source to the destination histogram
    # Returns list of possible messages
    def subtractShape(self, source, dest, weight=1.0, purityCheck=False):
        return self._calculateShape(source,dest,weight,"-",purityCheck)

    ## Adds or subtracts the shape from the source to the destination histogram
    # Returns list of possible messages
    def _calculateShape(self, source, dest, weight, operation, purityCheck=False):
        if source == None or dest == None:
            return []
        myMsgList = []
        # Check that binning is meaningful
        for iDest in range(1,dest.GetNbinsX()+1):
            minExists = False
            maxExists = False
            for iSrc in range(1,source.GetNbinsX()+1):
                if abs(dest.GetXaxis().GetBinLowEdge(iDest) - source.GetXaxis().GetBinLowEdge(iSrc)) < 0.0001:
                    minExists = True
                if abs(dest.GetXaxis().GetBinLowEdge(iDest) - source.GetXaxis().GetBinUpEdge(iSrc)) < 0.0001:
                    maxExists = True
            if not minExists and not maxExists:
                # Bin edges do not match
                print iDest, dest.GetNbinsX()+1, source.GetXaxis().GetBinLowEdge(1), dest.GetXaxis().GetBinLowEdge(iDest), source.GetXaxis().GetBinUpEdge(source.GetNbinsX()+1),dest.GetXaxis().GetBinLowEdge(iDest)
                if source.GetXaxis().GetBinLowEdge(1) <= dest.GetXaxis().GetBinLowEdge(iDest) and source.GetXaxis().GetBinUpEdge(source.GetNbinsX()+1) >= dest.GetXaxis().GetBinLowEdge(iDest):
                    # Bin edge mismatch is not caused by underflow or overflow
                    myMsg = "Source bin low edges:"
                    for k in range(1,source.GetNbinsX()+1):
                        myMsg += " %.2f"%source.GetXaxis().GetBinLowEdge(k)
                    myMsg += "\nDestination bin low edges:"
                    for k in range(1,dest.GetNbinsX()+1):
                        myMsg += " %.2f"%dest.GetXaxis().GetBinLowEdge(k)
                    print ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Shape histogram binning mismatch!"
                    print myMsg
                    raise Exception()
        # Histogram binnings are consistent, loop bin by bin over the source histogram
        iDest = 0
        # If necessary, change starting destination bin
        while iDest < self._nbins and source.GetXaxis().GetBinUpEdge(0) > dest.GetXaxis().GetBinLowEdge(iDest+1):
            iDest += 1
        countSum = 0.0
        errorSum = 0.0
        for iSrc in range(0,source.GetNbinsX()+2):
            myDestBinWillChangeOnNextInteration = False
            # Check if one needs to change the bin on next iteration
            if iDest <= self._nbins:
                #print "iSrc=%d (%f-%f), iDest=%d (%f-%f)"%(iSrc,source.GetXaxis().GetBinLowEdge(iSrc),source.GetXaxis().GetBinUpEdge(iSrc),iDest,dest.GetXaxis().GetBinLowEdge(iDest),dest.GetXaxis().GetBinUpEdge(iDest))
                if abs(source.GetXaxis().GetBinUpEdge(iSrc) - dest.GetXaxis().GetBinLowEdge(iDest+1)) < 0.0001:
                    # This is last source bin for the destination
                    myDestBinWillChangeOnNextInteration = True
            countSum += source.GetBinContent(iSrc) * weight
            errorSum += (source.GetBinError(iSrc)**2) * weight
            #print "iSrc=%d,iDest=%d, sum=%f +- %f"%(iSrc,iDest,countSum,errorSum)
            if myDestBinWillChangeOnNextInteration:
                # Store result, Note: it is assumed here that bin error is squared!!!
                #print "iSrc=%d,iDest=%d, sum=%f+%f +- %f+%f"%(iSrc,iDest,countSum,dest.GetBinContent(iDest),errorSum,dest.GetBinError(iDest))
                if operation == "+":
                    dest.SetBinContent(iDest, dest.GetBinContent(iDest)+countSum)
                elif operation == "-":
                    if purityCheck:
                        if dest.GetBinContent(iDest) > 0.0:
                          myResidual = dest.GetBinContent(iDest)-countSum
                          myPurity = myResidual/dest.GetBinContent(iDest)
                          if myPurity < 0.5:
                               myMsgList.append(["Shape histo bin %d purity is low! (purity=%f, event count=%f)"%(iDest,myPurity,myResidual),myResidual])
                    dest.SetBinContent(iDest, dest.GetBinContent(iDest)-countSum)
                else:
                    raise Exception(ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Unknown operation (only + or - are valid)!")
                dest.SetBinError(iDest, dest.GetBinError(iDest)+errorSum)
                iDest += 1
                countSum = 0.0
                errorSum = 0.0
        # Take into account overflow bin of source
        if operation == "+":
            dest.SetBinContent(self._nbins+1, dest.GetBinContent(self._nbins+1)+countSum)
        elif operation == "-":
            if purityCheck:
                if dest.GetBinContent(iDest) > 0.0:
                  myResidual = dest.GetBinContent(iDest)-countSum
                  myPurity = myResidual/dest.GetBinContent(iDest)
                  if myPurity < 0.5:
                        myMsgList.append(["Shape histo bin %d purity is low! (purity=%f, event count=%f)"%(iDest,myPurity,myResidual),myResidual])
            dest.SetBinContent(self._nbins+1, dest.GetBinContent(self._nbins+1)-countSum)
        else:
            raise Exception(ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Unknown operation (only + or - are valid)!")
        dest.SetBinError(self._nbins+1, dest.GetBinError(self._nbins+1)+errorSum)
        return myMsgList

    ## Finalises the destination histogram (takes sqrt of the errors)
    def finaliseShape(self, dest):
        if dest == None:
            return
        # Do not move underflow events to first bin !!!
        if False:
            dest.SetBinContent(1, dest.GetBinContent(1)+dest.GetBinContent(0))
            dest.SetBinError(1, dest.GetBinError(1)+dest.GetBinError(0))
            dest.SetBinContent(0,0.0)
            dest.SetBinError(0,0.0)
        # Move overflow events to the last bin
        dest.SetBinContent(dest.GetNbinsX(), dest.GetBinContent(dest.GetNbinsX())+dest.GetBinContent(dest.GetNbinsX()+1))
        dest.SetBinError(dest.GetNbinsX(), dest.GetBinError(dest.GetNbinsX())+dest.GetBinError(dest.GetNbinsX()+1))
        dest.SetBinContent(dest.GetNbinsX()+1,0.0)
        dest.SetBinError(dest.GetNbinsX()+1,0.0)
        # Convert variances into uncertainties
        for iDest in range(0,dest.GetNbinsX()+2):
            dest.SetBinError(iDest, sqrt(dest.GetBinError(iDest)))

    ## Set negative bins to zero, but keep normalisation
    def correctNegativeBins(self, dest):
        if dest == None:
            return
        myIntegral = dest.Integral(0,dest.GetNbinsX()+2)
        for k in range(0,dest.GetNbinsX()+2):
            if dest.GetBinContent(k) < 0.0:
                dest.SetBinContent(k, 0.0)
                # Keep uncertainty like it is
        # Now rescale
        myNewIntegral = dest.Integral(0,dest.GetNbinsX()+2)
        dest.Scale(myIntegral / myNewIntegral)

    ## Retrieve the default specs from the histogram if necessary
    def _retrieveHistoSpecsFromHisto(self, histo, specs):
        if histo == None and specs == None:
            raise Exception(ShellStyles.ErrorLabel()+"Need to supply either a histogram or dictionary with bin specification for the histograms!")
        mySpecs = None
        if specs == None:
            mySpecs = {}
            specs = {}
        else:
            # Obtain specs from dictionary
            mySpecs = dict(specs)
        if histo != None:
            # Obtain specs from histogram
            if not "bins" in specs:
                mySpecs["bins"] = histo.GetXaxis().GetNbins()
            if not "rangeMin" in specs:
                mySpecs["rangeMin"] = histo.GetXaxis().GetXmin()
            if not "rangeMax" in specs:
                mySpecs["rangeMax"] = histo.GetXaxis().GetXmax()
            if not "xtitle" in specs:
                mySpecs["xtitle"] = histo.GetXaxis().GetTitle()
            if not "ytitle" in specs:
                mySpecs["ytitle"] = histo.GetYaxis().GetTitle()
            if not "variableBinSizeLowEdges" in specs:
                # Check if constant interval binning is used
                if histo.GetXaxis().GetXbins().GetSize() == 0:
                    mySpecs["variableBinSizeLowEdges"] = []
                else:
                    myArray = histo.GetXaxis().GetXbins()
                    myBinEdges = []
                    for i in range(0,myArray.GetSize()-1): # Ignore last bin since it is the right edge of the last bin
                        myBinEdges.append(myArray.GetAt(i))
                    mySpecs["variableBinSizeLowEdges"] = list(myBinEdges)
                    mySpecs["bins"] = len(myBinEdges)
        else:
            # No histogram provided
            if not "xtitle" in specs:
                mySpecs["xtitle"] = ""
            if not "ytitle" in specs:
                mySpecs["ytitle"] = ""
        if "variableBinSizeLowEdges" in mySpecs:
            if len(mySpecs["variableBinSizeLowEdges"]) > 0:
                mySpecs["bins"] = len(mySpecs["variableBinSizeLowEdges"])
        else:
            mySpecs["variableBinSizeLowEdges"] = []
        return mySpecs
