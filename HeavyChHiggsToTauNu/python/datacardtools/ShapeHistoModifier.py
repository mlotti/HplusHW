from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
import ROOT
from array import array
from math import pow,sqrt

## Class for treating properly shape histograms with different axis ranges and or binning
# Allows tuning of shape histogram without having to rerun full analysis
# Note: After the adding is done, remember to call finalise! (adding treats errors as squares, finalising takes the sqrt of the squares)
class ShapeHistoModifier():
    def __init__(self, histoSpecs, debugMode=False):
        self._nbins = histoSpecs["bins"]
        self._min = histoSpecs["rangeMin"]
        self._max = histoSpecs["rangeMax"]
        self._binLowEdges = []
        self._binLowEdges.extend(histoSpecs["variableBinSizeLowEdges"])
        self._xtitle = histoSpecs["xtitle"]
        self._ytitle = histoSpecs["ytitle"]
        # Variable bin widths support
        if len(self._binLowEdges) > 0:
            # Check that all bins are given
            if len(self._binLowEdges) != self._nbins:
                raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" shape histo definition for variable bin widths has %d entries, but nbins=%d!"%(len(self._binLowEdges),self._nbins))
        else:
            # Create bins with uniform width
            binwidth = (self._max-self._min) / self._nbins
            for i in range(0,self._nbins):
                self._binLowEdges.append(i*binwidth)
        if debugMode:
            print "ShapeHistoModifier: nbins=%d, range=%f-%f"%(self._nbins,self._min,self._max)
            print"  bin low edges:",self._binLowEdges

    ## Returns an empty histogram created according to the specifications
    def createEmptyShapeHistogram(self, name):
        myEdges = self._binLowEdges
        myEdges.append(self._max) # ROOT needs bins+1 numbers, where the last one is the right edge of last bin
        h = ROOT.TH1F(name, name, self._nbins,array('f',myEdges))
        h.Sumw2()
        h.SetXTitle(self._xtitle)
        h.SetYTitle(self._ytitle)
        return h


    ## Adds shape from the source to the destination histogram
    def addShape(self, source, dest):
        self._calculateShape(source,dest,"+")

    ## Adds shape from the source to the destination histogram
    def subtractShape(self, source, dest):
        self._calculateShape(source,dest,"-")

    ## Adds or subtracts the shape from the source to the destination histogram
    def _calculateShape(self, source, dest, operation):
        # Check that binning is meaningful
        for iDest in range(1,dest.GetNbinsX()+2):
            minExists = False
            maxExists = False
            for iSrc in range(1,source.GetNbinsX()+1):
                if dest.GetXaxis().GetBinLowEdge(iDest) == source.GetXaxis().GetBinLowEdge(iSrc):
                    minExists = True
                if dest.GetXaxis().GetBinLowEdge(iDest) == source.GetXaxis().GetBinUpEdge(iSrc):
                    maxExists = True
            if not minExists and not maxExists:
                # Bin edges do not match
                if source.GetXaxis().GetBinLowEdge(1) <= dest.GetXaxis().GetBinLowEdge(iDest) and source.GetXaxis().GetBinUpEdge(source.GetNbinsX()+1) >= dest.GetXaxis().GetBinLowEdge(iDest):
                    # Bin edge mismatch is not caused by underflow or overflow
                    myMsg = "Source bin low edges:"
                    for k in range(1,source.GetNbinsX()+1):
                        myMsg += " %.2f"%source.GetXaxis().GetBinLowEdge(k)
                    myMsg += "\nDestination bin low edges:"
                    for k in range(1,dest.GetNbinsX()+1):
                        myMsg += " %.2f"%dest.GetXaxis().GetBinLowEdge(k)
                    print ErrorStyle()+"Error:"+NormalStyle()+" Shape histogram binning mismatch!"
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
            countSum += source.GetBinContent(iSrc)
            errorSum += pow(source.GetBinError(iSrc),2)
            #print "iSrc=%d,iDest=%d, sum=%f +- %f"%(iSrc,iDest,countSum,errorSum)
            if myDestBinWillChangeOnNextInteration:
                # Store result, Note: it is assumed here that bin error is squared!!!
                #print "iSrc=%d,iDest=%d, sum=%f+%f +- %f+%f"%(iSrc,iDest,countSum,dest.GetBinContent(iDest),errorSum,dest.GetBinError(iDest))
                if operation == "+":
                    dest.SetBinContent(iDest, dest.GetBinContent(iDest)+countSum)
                elif operation == "-":
                    dest.SetBinContent(iDest, dest.GetBinContent(iDest)-countSum)
                else:
                    raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Unknown operation (only + or - are valid)!")
                dest.SetBinError(iDest, dest.GetBinError(iDest)+errorSum)
                iDest += 1
                countSum = 0.0
                errorSum = 0.0
        # Take into account overflow bin of source
        if operation == "+":
            dest.SetBinContent(self._nbins+1, dest.GetBinContent(self._nbins+1)+countSum)
        elif operation == "-":
            dest.SetBinContent(self._nbins+1, dest.GetBinContent(self._nbins+1)-countSum)
        else:
            raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Unknown operation (only + or - are valid)!")
        dest.SetBinError(self._nbins+1, dest.GetBinError(self._nbins+1)+errorSum)

    ## Finalises the destination histogram (takes sqrt of the errors)
    def finaliseShape(self, dest):
        # Move underflow events to first bin
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
