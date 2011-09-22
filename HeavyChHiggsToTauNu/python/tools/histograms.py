## \package histograms
# Histogram utilities and classes
#
# The package contains classes and utilities for histogram management.

import os, sys
import glob
import array

from optparse import OptionParser

import ROOT

import dataset

## Class to provide default positions of the various texts.
#
# The attributes which can be set are the x and y coordinates and the
# text size.
#
# \todo Set the text fonts to non-bold
class TextDefaults:
    def __init__(self):
        self._setDefaults("cmsPreliminary", x=0.62, y=0.96)
        self._setDefaults("energy", x=0.2, y=0.96)
        self._setDefaults("lumi", x=0.43, y=0.96)

    ## Modify the default values
    # 
    # \param name   Name of the property ('cmsPreliminary', 'energy', 'lumi')
    # \param kwargs Keyword arguments
    #
    # <b>Keyword arguments</b>
    # \li \a x     X coordinate
    # \li \a y     Y coordinate
    # \li \a size  Font size
    def _setDefaults(self, name, **kwargs):
        for x, value in kwargs.iteritems():
            setattr(self, name+"_"+x, value)
            
    ## Modify the default position of "CMS Preliminary" text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setCmsPreliminaryDefaults(self, **kwargs):
        self._setDefaults("cmsPreliminary", **kwargs)

    ## Modify the default position of center-of-mass energy text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setEnergyDefaults(self, **kwargs):
        self._setDefaults("energy", **kwargs)
        
    ## Modify the default position of integrated luminosity text
    #
    # \param kwargs  Keyword arguments (forwarded to _setDefaults())
    def setLuminosityDefaults(self, **kwargs):
        self._setDefaults("lumi", **kwargs)

    ## Get the (x, y) values for property
    #
    # \param name  Name of property
    # \param x     X coordinate, if None, use the default
    # \param y     Y coordinate, if None, use the default
    def getValues(self, name, x, y):
        if x == None:
            x = getattr(self, name+"_x")
        if y == None:
            y = getattr(self, name+"_y")
        return (x, y)

    ## Get the size for property
    #
    # \param name  Name of property
    #
    # \return The text size, taken from ROOT.gStyle if no value has been set
    def getSize(self, name):
        try:
            return getattr(self, name+"_size")
        except AttributeError:
            return ROOT.gStyle.GetTextSize()

## Provides default text positions and sizes
#
# In order to modify the global defaults, modify this object.
#
# Used by histograms.addCmsPreliminaryText(),
# histograms.addEnergyText(), histograms.addLuminosityText().
textDefaults = TextDefaults()

## Add the "CMS Preliminary" text to the pad
#
# \param x   X coordinate of the text (None for default value)
# \param y   Y coordinate of the text (None for default value)
def addCmsPreliminaryText(x=None, y=None):
    (x, y) = textDefaults.getValues("cmsPreliminary", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(l.GetTextFont()-20) # bold -> normal
    l.SetTextSize(textDefaults.getSize("cmsPreliminary"))
    l.DrawLatex(x, y, "CMS Preliminary")

## Add the center-of-mass energy text to the pad
#
# \param x   X coordinate of the text (None for default value)
# \param y   Y coordinate of the text (None for default value)
# \param s   Center-of-mass energy text with the unit
def addEnergyText(x=None, y=None, s="7 TeV"):
    (x, y) = textDefaults.getValues("energy", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(l.GetTextFont()-20) # bold -> normal
    l.SetTextSize(textDefaults.getSize("energy"))
    l.DrawLatex(x, y, "#sqrt{s} = "+s)

## Add the integrated luminosity text to the pad
#
# \param x     X coordinate of the text (None for default value)
# \param y     Y coordinate of the text (None for default value)
# \param lumi  Value of the integrated luminosity
# \param unit  Unit of the integrated luminosity value
def addLuminosityText(x, y, lumi, unit="fb^{-1}"):
    (x, y) = textDefaults.getValues("lumi", x, y)
    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(l.GetTextFont()-20) # bold -> normal
    l.SetTextSize(textDefaults.getSize("lumi"))
#    l.DrawLatex(x, y, "#intL=%.0f %s" % (lumi, unit))
#    l.DrawLatex(x, y, "L=%.0f %s" % (lumi, unit))
    l.DrawLatex(x, y, "%.2f %s" % (lumi/1000., unit))

## Class for generating legend creation functions with default positions.
#
# The intended usage is demonstrated in histograms.py below, i.e.
# \code
# createLegend = LegendCreator(x1, y1, x2, y2)
# createLegend.setDefaults(x1=0.4, y2=0.5)
# legend = createLegend()
# \endcode
class LegendCreator:
    ## Constructor
    #
    # \param x1          Default x1 (left x)
    # \param y1          Default y1 (lower y)
    # \param x2          Default x2 (right x)
    # \param y2          Default y2 (upper y)
    # \param textSize    Default text size
    # \param borderSize  Default border size
    # \param fillStyle   Default fill style
    # \param fillColor   Default fill color
    def __init__(self, x1=0.73, y1=0.62, x2=0.93, y2=0.92, textSize=0.03, borderSize=0, fillStyle=4000, fillColor=ROOT.kWhite):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.textSize = textSize
        self.borderSize = borderSize
        self.fillStyle = fillStyle
        self.fillColor = fillColor
        self._keys = ["x1", "y1", "x2", "y2"]

    ## Create a copy of the object
    def copy(self):
        return LegendCreator(self.x1, self.y1, self.x2, self.y2)

    ## Set new default positions
    #
    # <b>Keyword arguments</b>
    # \li \a x1          X1 coordinate
    # \li \a y1          Y1 coordinate
    # \li \a x2          X2 coordinate
    # \li \a y2          Y2 coordinate
    # \li \a textSize    Text size
    # \li \a borderSize  Border size
    # \li \a fillStyle   Fill style
    # \li \a fillColor   Fill color
    def setDefaults(self, **kwargs):
        for x, value in kwargs.iteritems():
            setattr(self, x, value)

    def moveDefaults(self, dx=0, dy=0, dw=0, dh=0):
        self.x1 += dx
        self.x2 += dx

        self.y1 += dy
        self.y2 += dy

        self.x2 += dw
        self.y2 += dh

    ## Create a new TLegend object (function call syntax)
    #
    # Arguments can be either
    # - Four numbers for the coordinates (x1, y1, x2, y2) as positional arguments
    # - Keyword arguments (x1, y1, x2, y2)
    #
    # If all 4 coordinates are specified, they are used. In the
    # keyword argument case, the coordinates which are not given are
    # taken from the default values.
    def __call__(self, *args, **kwargs):
        if len(args) == 4:
            if len(kwargs) != 0:
                raise Exception("Got 4 positional arguments, no keyword arguments allowed")
            for i, k in enumerate(self._keys):
                kwargs[k] = args[i]
        elif len(args) != 0:
            raise Exception("If positional arguments given, must give 4")
        else:
            for i in self._keys:
                if not i in kwargs:
                    kwargs[i] = getattr(self, i)

        legend = ROOT.TLegend(kwargs["x1"], kwargs["y1"], kwargs["x2"], kwargs["y2"])
        legend.SetFillStyle(self.fillStyle)
        if self.fillStyle != 0:
            legend.SetFillColor(self.fillColor)
        legend.SetBorderSize(self.borderSize)
        if legend.GetTextFont() % 10 == 3:
            legend.SetTextFont(legend.GetTextFont()-1) # From x3 to x2
        legend.SetTextSize(self.textSize)
        #legend.SetMargin(0.1)
        return legend

    ## \var x1
    # X1 coordinate
    ## \var y1
    # Y1 coordinate
    ## \var x2
    # X2 coordinate
    ## \var y2
    # Y2 coordinate
    ## \var textSize
    # Text size
    ## \var boderSize
    # Border size
    ## \var _keys
    # List of valid coordinate names for __call__() function


## Default legend creator object
createLegend = LegendCreator()

## Move TLegend
def moveLegend(legend, dx=0, dy=0, dw=0, dh=0):
    legend.SetX1(legend.GetX1() + dx)
    legend.SetX2(legend.GetX2() + dx)
    legend.SetY1(legend.GetY1() + dy)
    legend.SetY2(legend.GetY2() + dy)

    legend.SetX1(legend.GetX1() + dw)
    legend.SetY1(legend.GetY1() + dh)
    
    return legend
    

## Update the style of palette Z axis according to ROOT.gStyle.
#
# This function is needed because the style is not propageted to the Z
# axis automatically.
def updatePaletteStyle(histo):
    ROOT.gPad.Update()
    paletteAxis = histo.GetListOfFunctions().FindObject("palette")
    if paletteAxis == None:
        return
    paletteAxis.SetLabelColor(ROOT.gStyle.GetLabelColor())
    paletteAxis.SetLabelFont(ROOT.gStyle.GetLabelFont())
    paletteAxis.SetLabelOffset(ROOT.gStyle.GetLabelOffset())
    paletteAxis.SetLabelSize(ROOT.gStyle.GetLabelSize())

## Sum TH1 histograms
#
# \param rootHistos  List of TH1 objects
# \param postfix     Postfix for the sum histo name
def sumRootHistos(rootHistos, postfix="_sum"):
    h = rootHistos[0].Clone()
    h.SetName(h.GetName()+"_sum")
    for a in rootHistos[1:]:
        h.Add(a)
    return h

def isLessThan(**kwargs):
    if len(kwargs) != 1:
        raise Exception("Should give only either 'lessThan' or 'greaterThan' as a keyword argument")
    elif "lessThan" in kwargs:
        return kwargs["lessThan"]
    elif "greaterThan" in kwargs:
        return not kwargs["greaterThan"]
    else:
        raise Exception("Must give either 'lessThan' or 'greaterThan' as a keyword argument")

## Convert TH1 distribution to TH1 of number of passed events as a function of cut value
def dist2pass(hdist, **kwargs):
    lessThan = isLessThan(**kwargs)

    # for less than
    integral = None
    if lessThan:
        integral = lambda h, bin: h.Integral(0, bin)
    else:    
        integral = lambda h, bin: h.Integral(bin, h.GetNbinsX()+1)
        
    # bin 0             underflow bin
    # bin 1             first bin
    # bin GetNbinsX()   last bin
    # bin GetNbinsX()+1 overflow bin

    # Here we assume that all the bins in hdist have equal widths. If
    # this doesn't hold, the output must be TGraph
    bw = hdist.GetBinWidth(1);
    for bin in xrange(2, hdist.GetNbinsX()+1):
        if abs(bw - hdist.GetBinWidth(bin))/bw > 0.01:
            raise Exception("Input histogram with variable bin width is not supported (yet). The bin width of bin1 was %f, and bin width of bin %d was %f" % (bw, bin, hdist.GetBinWidth(bin)))

    # Construct the low edges of the passed histogram. Set the low
    # edges such that the bin centers correspond to the edges of the
    # distribution histogram. This makes sense because the only
    # sensible cut points in the distribution histogram are the bin
    # edges, and if one draws the passed histogram with points, the
    # points are placed to bin centers.
    nbins = hdist.GetNbinsX()+1
    firstLowEdge = hdist.GetXaxis().GetBinLowEdge(1) - bw/2
    lastUpEdge = hdist.GetXaxis().GetBinUpEdge(hdist.GetNbinsX()) + bw/2
    name = "passed_"+hdist.GetName()
    hpass = ROOT.TH1F("cumulative_"+hdist.GetName(), "Cumulative "+hdist.GetTitle(),
                      nbins, firstLowEdge, lastUpEdge)

    #print "dist bins %d, pass bins %d" % (hdist.GetNbinsX(), hpass.GetNbinsX())

    #for bin in xrange(1, hpass.GetNbinsX()):
    #total = hdist.Integral(0, hdist.GetNbinsX()+1)
    #print "total %f" % total
    for bin in xrange(0, hdist.GetNbinsX()+2):
        passed = integral(hdist, bin)
        #print "bin %d content %f, passed/total = %f/%f = %f" % (bin, hdist.GetBinContent(bin), passed, total, passed/total)
        hpass.SetBinContent(bin+1, passed)
    #print "bin N, N+1 %f, %f" % (hpass.GetBinContent(hpass.GetNbinsX()), hpass.GetBinContent(hpass.GetNbinsX()+1))
    return hpass


def th1ApplyBin(th1, function):
    for bin in xrange(0, th1.GetNbinsX()+2):
        th1.SetBinContent(bin, function(th1.GetBinContent(bin)))

## Convert TH1 distribution to TH1 of efficiency as a function of cut value
def dist2eff(hdist, **kwargs):
    hpass = dist2pass(hdist, **kwargs)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    th1ApplyBin(hdist, lambda value: value/total)
    return hpass

## Convert TH1 distribution to TH1 of 1-efficiency as a function of cut value
def dist2rej(hdist, **kwargs):
    hpass = dist2pass(hdist, **kwargs)
    total = hdist.Integral(0, hdist.GetNbinsX()+1)
    th1ApplyBin(hdist, lambda value: 1-value/total)
    return hpass


## Infer the frame bounds from the histograms and keyword arguments
#
# \param histos  List of histograms.HistoBase objects
# \param kwargs  Dictionary of keyword arguments to parse
#
# Used e.g. in histograms.CanvasFrame and histograms.CanvasFrameTwo
def _boundsArgs(histos, kwargs):
    ymaxfactor = kwargs.get("ymaxfactor", 1.1)

    if not "ymax" in kwargs:
        kwargs["ymax"] = ymaxfactor * max([h.getYmax() for h in histos])
    if not "ymin" in kwargs:
        if "yminfactor" in kwargs:
            kwargs["ymin"] = kwargs["yminfactor"]*kwargs["ymax"]
        else:
            kwargs["ymin"] = min([h.getYmin() for h in histos])

    if not "xmin" in kwargs:
        kwargs["xmin"] = min([h.getXmin() for h in histos])
    if not "xmax" in kwargs:
        kwargs["xmax"] = max([h.getXmax() for h in histos])

## Create TCanvas and frame for one TPad.
class CanvasFrame:
    ## Create TCanvas and TH1 for the frame.
    #
    # \param histoManager  histograms.HistoManager object to take the histograms for automatic axis ranges
    # \param name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
    # \param kwargs        Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a ymin     Minimum value of Y axis
    # \li\a ymax     Maximum value of Y axis
    # \li\a xmin     Minimum value of X axis
    # \li\a xmax     Maximum value of X axis
    # \li\a ymaxfactor  Maximum value of Y is \a ymax*\a ymaxfactor (default 1.1)
    # \li\a yminfactor  Minimum value of Y is \a ymax*\a yminfactor (yes, calculated from \a ymax )
    #
    # By default \a ymin, \a ymax, \a xmin and \a xmax are taken as
    # the maximum/minimums of the histogram objects such that frame
    # contains all histograms. The \a ymax is then multiplied with \a
    # ymaxfactor
    #
    # The \a yminfactor/\a ymaxfactor are used only if \a ymin/\a ymax
    # is taken from the histograms, i.e. \a ymax keyword argument is
    # \b not given.
    def __init__(self, histoManager, name, **kwargs):
        histos = histoManager.getHistos()
        if len(histos) == 0:
            raise Exception("Empty set of histograms!")

        self.canvas = ROOT.TCanvas(name)
        self.pad = self.canvas.GetPad(0)

        opts = kwargs
        if "opts" in kwargs:
            tmp = {}
            tmp.update(kwargs)
            if "opts2" in tmp:
                del tmp["opts2"]
            if len(tmp) != 1:
                raise Exception("If giving 'opts' as keyword argument, no other keyword arguments can be given (except opts2, which is ignored)")
            opts = kwargs["opts"]

        if "yfactor" in opts:
            if "ymaxfactor" in opts:
                raise Exception("Only one of ymaxfactor, yfactor can be given")
            opts["ymaxfactor"] = opts["yfactor"]

        _boundsArgs(histos, opts)

        self.frame = self.canvas.DrawFrame(opts["xmin"], opts["ymin"], opts["xmax"], opts["ymax"])
        self.frame.GetXaxis().SetTitle(histos[0].getRootHisto().GetXaxis().GetTitle())
        self.frame.GetYaxis().SetTitle(histos[0].getRootHisto().GetYaxis().GetTitle())

    ## \var canvas
    # TCanvas for the canvas
    ## \var frame
    # TH1 for the frame
    ## \var pad
    # TPad of the plot

## Create TCanvas and frames for two TPads.
class CanvasFrameTwo:
    ## Create TCanvas and TH1 for the frame.
    #
    # \param histoManager1 HistoManager object to take the histograms for automatic axis ranges for upper pad
    # \param histos2       List of TH1s to take the histograms for automatic axis ranges for lower pad
    # \param name          Name for TCanvas (will be the file name, if TCanvas.SaveAs(".png") is used)
    # \param kwargs        Keyword arguments (see below)
    #
    # <b>Keyword arguments</b>
    # \li\a opts1/\a opts           Dictionary for histoManager1 options
    # \li\a opts2                   Dictionary for histos2 options
    # \li\a canvasFactor            Multiply the canvas height by this factor (default 1.25)
    # \li\a canvasHeightCorrection  Add this to the height of the lower pad (default 0.022)
    #
    # <b>Options</b>
    # \li\a ymin     Minimum value of Y axis
    # \li\a ymax     Maximum value of Y axis
    # \li\a xmin     Minimum value of X axis (only for opts1)
    # \li\a xmax     Maximum value of X axis (only for opts1)
    # \li\a ymaxfactor  Maximum value of Y is ymax*ymaxfactor (default 1.1)
    # \li\a yminfactor  Minimum value of Y is ymax*yminfactor (yes, calculated from ymax
    #
    # By default \a ymin, \a ymax, \a xmin and \a xmax are taken as
    # the maximum/minimums of the histogram objects such that frame
    # contains all histograms. The \a ymax is then multiplied with \a
    # ymaxfactor
    #
    # The \a yminfactor/\a ymaxfactor are used only if \a ymin/\a ymax
    # is taken from the histograms, i.e. \a ymax keyword argument is \b
    # not given.
    def __init__(self, histoManager1, histos2, name, **kwargs):
        class FrameWrapper:
            """Wrapper to provide the CanvasFrameTwo.frame member.

            The GetXaxis() is forwarded to the frame of the lower pad,
            and the GetYaxis() is forwared to the frame of the upper pad.
            """
            def __init__(self, frame1, frame2):
                self.frame1 = frame1
                self.frame2 = frame2

            def GetXaxis(self):
                return self.frame2.GetXaxis()

            def GetYaxis(self):
                return self.frame1.GetYaxis()


            def getXmin(self):
                return self.frame2.GetXaxis().GetBinLowEdge(self.frame2.GetXaxis().GetFirst())

            def getXmax(self):
                return self.frame2.GetXaxis().GetBinUpEdge(self.frame2.GetXaxis().GetLast())


        class HistoWrapper:
            """Wrapper to provide the getXmin/getXmax functions for _boundsArgs function."""
            def __init__(self, histo):
                self.histo = histo

            def getRootHisto(self):
                return self.histo

            def getXmin(self):
                return self.histo.GetXaxis().GetBinLowEdge(self.histo.GetXaxis().GetFirst())

            def getXmax(self):
                return self.histo.GetXaxis().GetBinUpEdge(self.histo.GetXaxis().GetLast())

            def getYmin(self):
                return self.histo.GetMinimum()

            def getYmax(self):
                return self.histo.GetMaximum()

        histos1 = histoManager1.getHistos()
        if len(histos1) == 0:
            raise Exception("Empty set of histograms for first pad!")
        if len(histos2) == 0:
            raise Exception("Empty set of histograms for second pad!")

        canvasFactor = kwargs.get("canvasFactor", 1.25)
        canvasHeightCorrection = kwargs.get("canvasHeightCorrection", 0.022)
        divisionPoint = 1-1/canvasFactor

        # Do it like this (create empty, update from kwargs) in order
        # to make a copy and NOT modify the dictionary in the caller
        opts1 = {}
        opts1.update(kwargs.get("opts", {}))
        if "opts1" in kwargs:
            if "opts" in kwargs:
                raise Exception("Can not give both 'opts' and 'opts1' as keyword arguments")
            opts1 = kwargs["opts1"]
        opts2 = {}
        opts2.update(kwargs.get("opts2", {}))

        if "xmin" in opts2 or "xmax" in opts2:
            raise Exception("No 'xmin' or 'xmax' allowed in opts2, values are taken from opts/opts1")
        

        _boundsArgs(histos1, opts1)
        opts2["xmin"] = opts1["xmin"]
        opts2["xmax"] = opts1["xmax"]
        _boundsArgs([HistoWrapper(h) for h in histos2], opts2)

        # Create the canvas, divide it to two
        self.canvas = ROOT.TCanvas(name, name, ROOT.gStyle.GetCanvasDefW(), int(ROOT.gStyle.GetCanvasDefH()*canvasFactor))
        self.canvas.Divide(1, 2)
        
        # Set the lower point of the upper pad to divisionPoint
        self.pad1 = self.canvas.cd(1)
        (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
        self.pad1.GetPadPar(xlow, ylow, xup, yup)
        self.pad1.SetPad(xlow, divisionPoint, xup, yup)
        self.pad1.SetFillStyle(4000) # transparent

        # Set the upper point of the lower pad to divisionPoint
        self.pad2 = self.canvas.cd(2)
        self.pad2.GetPadPar(xlow, ylow, xup, yup)
        self.pad2.SetPad(xlow, ylow, xup,
                         divisionPoint+ROOT.gStyle.GetPadBottomMargin()-ROOT.gStyle.GetPadTopMargin()+canvasHeightCorrection)
        self.pad2.SetFillStyle(4000) # transparent
        self.pad2.SetTopMargin(0.0)
        #self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.06)
        self.pad2.SetBottomMargin(self.pad2.GetBottomMargin()+0.16)

        self.canvas.cd(1)

        yoffsetFactor = canvasFactor*1.15
        #xoffsetFactor = canvasFactor*1.6
        #xoffsetFactor = canvasFactor*2
        xoffsetFactor = 0.5*canvasFactor/(canvasFactor-1) * 1.3

        self.frame1 = self.pad1.DrawFrame(opts1["xmin"], opts1["ymin"], opts1["xmax"], opts1["ymax"])
        (labelSize, titleSize) = (self.frame1.GetXaxis().GetLabelSize(), self.frame1.GetXaxis().GetTitleSize())
        self.frame1.GetXaxis().SetLabelSize(0)
        self.frame1.GetXaxis().SetTitleSize(0)
        self.frame1.GetYaxis().SetTitle(histos1[0].getRootHisto().GetYaxis().GetTitle())
        self.frame1.GetYaxis().SetTitleOffset(self.frame1.GetYaxis().GetTitleOffset()*yoffsetFactor)

        self.canvas.cd(2)
        self.frame2 = self.pad2.DrawFrame(opts2["xmin"], opts2["ymin"], opts2["xmax"], opts2["ymax"])
        self.frame2.GetXaxis().SetTitle(histos1[0].getRootHisto().GetXaxis().GetTitle())
        self.frame2.GetYaxis().SetTitle(histos2[0].GetYaxis().GetTitle())
        self.frame2.GetYaxis().SetTitleOffset(self.frame2.GetYaxis().GetTitleOffset()*yoffsetFactor)
        self.frame2.GetXaxis().SetTitleOffset(self.frame2.GetXaxis().GetTitleOffset()*xoffsetFactor)
        self.frame2.GetYaxis().SetLabelSize(int(self.frame2.GetYaxis().GetLabelSize()*0.8))

        self.canvas.cd(1)
        self.frame = FrameWrapper(self.frame1, self.frame2)
        self.pad = self.pad1

    ## \var frame1
    # TH1 for the upper frame
    ## \var frame2
    # TH2 for the lower frame
    ## \var canvas
    # TCanvas for the canvas
    ## \var pad
    # TPad for the upper pad
    ## \var pad1
    # TPad for the upper pad
    ## \var pad2
    # TPad for the lower pad
    ## \var frame
    # Wrapper for the two frames
    #
    # The y axis of the wrapper is taken from the upper frame, and the
    # xa xis from the lower frame.

## Base class for all Histo classes.
class HistoBase:
    ## Constructor
    #
    # \todo test draw style "9"
    #
    # \param rootHisto    ROOT histogram object (TH1)
    # \param name         Name of the histogram
    # \param legendStyle  Style string for TLegend (third parameter for TLegend.AddEntry())
    # \param drawStyle    Style string for Draw (string parameter for TH1.Draw())
    def __init__(self, rootHisto, name, legendStyle, drawStyle):
        self.rootHisto = rootHisto
        self.name = name
        self.legendLabel = name
        self.legendStyle = legendStyle
        self.drawStyle = drawStyle

    ## Get the ROOT histogram object (TH1)
    def getRootHisto(self):
        return self.rootHisto

    ## Get the histogram name
    def getName(self):
        return self.name

    ## Set the histogram name
    #
    # \param name  New histogram name
    def setName(self, name):
        self.name = name

    ## Set the legend label
    #
    # \param label  New histogram label for TLegend
    def setLegendLabel(self, label):
        self.legendLabel = label

    ## Set the legend style
    #
    # \param style  New histogram style for TLegend
    def setLegendStyle(self, style):
        self.legendStyle = style

    ## Add the histogram to a TLegend
    #
    # \param legend   TLegend object
    def addToLegend(self, legend):
        # Hack to get the black border to the legend, only if the legend style is fill
        if "f" in self.legendStyle.lower():
            h = self.rootHisto.Clone(self.rootHisto.GetName()+"_forLegend")
            h.SetLineWidth(1)
            if self.rootHisto.GetLineColor() == self.rootHisto.GetFillColor():
                h.SetLineColor(ROOT.kBlack)

            legend.AddEntry(h, self.legendLabel, self.legendStyle)
            self.rootHistoForLegend = h # keep the reference in order to avoid segfault
        else:
            labels = self.legendLabel.split("\n")
            legend.AddEntry(self.rootHisto, labels[0], self.legendStyle)
            for lab in labels[1:]:
                legend.AddEntry(None, lab, "")

    ## Call a function with self as an argument.
    #
    # \param func  Function with one parameter
    #
    # \todo This resembles the Visitor pattern, perhaps this should be
    # renamed to visit()?
    def call(self, func):
        func(self)

    ## Draw the histogram
    #
    # \param opt  Drawing options (in addition to the draw style)
    def draw(self, opt):
        self.rootHisto.Draw(self.drawStyle+" "+opt)

    ## Get the minimum value of the X axis
    def getXmin(self):
        return self.rootHisto.GetXaxis().GetBinLowEdge(self.rootHisto.GetXaxis().GetFirst())

    ## Get the maximum value of the X axis
    def getXmax(self):
        return self.rootHisto.GetXaxis().GetBinUpEdge(self.rootHisto.GetXaxis().GetLast())

    ## Get the minimum value of the Y axis
    def getYmin(self):
        return self.rootHisto.GetMinimum()

    ## Get the maximum value of the Y axis
    def getYmax(self):
        return self.rootHisto.GetMaximum()

    ## Get the width of a bin
    #
    # \param bin  Bin number
    def getBinWidth(self, bin):
        return self.rootHisto.GetBinWidth(bin)

    ## \var rootHisto
    # ROOT histogram object (TH1)
    ## \var name
    # Histogram name
    ## \var legendLabel
    # Label for TLegend
    ## \var legendStyle
    # Style string for TLegend
    ## \var drawStyle
    # Style string for Draw()

## Represents one (TH1/TH2) histogram
class Histo(HistoBase):
    ## Constructor
    #
    # \param dataset    dataset.Dataset object
    # \param rootHisto  TH1 object
    # \param name       Name of the Histo
    #
    #    The default legend label is the dataset name
    def __init__(self, dataset, rootHisto, name):
        HistoBase.__init__(self, rootHisto, name, "l", "HIST")
        self.dataset = dataset

    ## Is the histogram from MC?
    def isMC(self):
        return self.dataset.isMC()

    ## Is the histogram from collision data?
    def isData(self):
        return self.dataset.isData()

    ## Get the dataset.Dataset object
    def getDataset(self):
        return self.dataset

    ## \var dataset
    # The histogram is from this dataset.Dataset object

## Represents combined (statistical) uncertainties of multiple histograms.
class HistoTotalUncertainty(HistoBase):
    ## Constructor
    #
    # \param histos  List of histograms.HistoBase objects
    # \param name    Name of the uncertainty histogram
    def __init__(self, histos, name):
        rootHistos = []
        for h in histos:
            if hasattr(h, "getSumRootHisto"):
                rootHistos.append(h.getSumRootHisto())
            else:
                rootHistos.append(h.getRootHisto())

        HistoBase.__init__(self, rootHistos[0].Clone(), name, "F", "E2")
        self.rootHisto.SetName(self.rootHisto.GetName()+"_errors")
        self.histos = histos

        for h in rootHistos[1:]:
            self.rootHisto.Add(h)

    ## Is the histogram from MC?
    def isMC(self):
        return self.histos[0].isMC()

    ## Is the histogram from collision data?
    def isData(self):
        return self.histos[0].isData()

    ## \var histos
    # List of histograms.HistoBase objects from which the total uncertaincy is calculated

## Represents stacked TH1 histograms
#
# Stacking is done with the help of THStack object
class HistoStacked(HistoBase):
    ## Constructor.
    #
    # \param histos  List of Histo objects to stack
    # \param name    Name of the stacked histogram
    def __init__(self, histos, name):
        HistoBase.__init__(self, ROOT.THStack(name+"stackHist", name+"stackHist"), name, None, "HIST")
        self.histos = histos

        rootHistos = [d.getRootHisto() for d in self.histos]
        rootHistos.reverse()
        for h in rootHistos:
            self.rootHisto.Add(h)

    ## Get the list of original TH1 histograms.
    def getAllRootHistos(self):
        return [x.getRootHisto() for x in self.histos]

    ## Get the sum of the original histograms.
    def getSumRootHisto(self):
        return sumRootHistos([d.getRootHisto() for d in self.histos])

    ## Is the histogram from MC?
    def isMC(self):
        return self.histos[0].isMC()

    ## Is the histogram from collision data?
    def isData(self):
        return self.histos[0].isData()

    def setLegendLabel(self, label):
        for h in self.histos:
            h.setLegendLabel(label)

    def setLegendStyle(self, style):
        for h in self.histos:
            h.setLegendStyle(style)

    def addToLegend(self, legend):
        for h in self.histos:
            h.addToLegend(legend)

    ## Call a function for each Histo in the stack.
    #
    # \param function  Function with one parameter
    #
    # \todo This resembles the Visitor pattern, perhaps this should be
    # renamed to visit()?
    def call(self, function):
        for h in self.histos:
            h.call(function)

    def getXmin(self):
        return min([h.getXmin() for h in self.histos])

    def getXmax(self):
        return max([h.getXmax() for h in self.histos])

    def getBinWidth(self, bin):
        return self.histos[0].getBinWidth(bin)

    ## \var histos
    # List of histograms.Histo objects which are stacked

class HistoGraph(HistoBase):
    def __init__(self, rootGraph, name, legendStyle="l", drawStyle="L"):
        HistoBase.__init__(self, rootGraph, name, legendStyle, drawStyle)

    def getRootGraph(self):
        return self.getRootHisto()

    def getXmin(self):
        values = self.getRootGraph().GetX()
        return min([values[i] for i in xrange(0, self.getRootGraph().GetN())])

    def getXmax(self):
        values = self.getRootGraph().GetX()
        return max([values[i] for i in xrange(0, self.getRootGraph().GetN())])

    def getYmin(self):
        values = self.getRootGraph().GetY()
        return min([values[i] for i in xrange(0, self.getRootGraph().GetN())])

    def getYmax(self):
        values = self.getRootGraph().GetY()
        return max([values[i] for i in xrange(0, self.getRootGraph().GetN())])

    def getBinWidth(self, bin):
        raise Exception("getBinWidth() is meaningless for HistoGraph (name %s)" % self.getName())

## Implementation of HistoManager.
#
# Intended to be used only from HistoManager. This class contains all
#  the methods which require the Histo objects (and only them).
class HistoManagerImpl:
    ## Constructor.
    #
    # \param histos    List of histograms.HistoBase objects
    def __init__(self, histos=[]):

        # List for the Draw() order, keep it reversed in order to draw
        # the last histogram in the list first. i.e. to the bottom
        self.drawList = histos[:]

        # List for the legend order, first histogram is also first in
        # the legend
        self.legendList = histos[:]

        # Dictionary for accessing the histograms by name
        self._populateMap()

    ## Get the number of managed histograms.HistoBase objects
    def __len__(self):
        return len(self.drawList)

    ## Populate the name -> histograms.HistoBase map
    def _populateMap(self):
        self.nameHistoMap = {}
        for h in self.drawList:
            self.nameHistoMap[h.getName()] = h

    ## Append a histograms.HistoBase object.
    def appendHisto(self, histo):
        self.drawList.append(histo)
        self.legendList.append(histo)
        self._populateMap()

    ## Extend with a list of histograms.HistoBase objects.
    def extendHistos(self, histos):
        self.drawList.extend(histos)
        self.legendList.extend(histos)
        self._populateMap()

    ## Insert histograms.HistoBase to position i.
    #
    # \param i      Index of the position to insert the histogram
    # \param histo  histograms.HistoBase object to insert
    # \param kwargs Keyword arguments
    # 
    # <b>Keyword arguments</b>
    # \li \a legendIndex  Index of the position to insert the histogram in
    #                     the legend list (default is the same as i). Can
    #                     be useful for e.g. separate uncertainty histogram.
    def insertHisto(self, i, histo, **kwargs):
        drawIndex = i
        legendIndex = i

        if "legendIndex" in kwargs:
            legendIndex = kwargs["legendIndex"]

        self.drawList.insert(drawIndex, histo)
        self.legendList.insert(legendIndex, histo)
        self._populateMap()

    def removeHisto(self, name):
        del self.nameHistoMap[name]
        for i, h in enumerate(self.drawList):
            if h.getName() == name:
                del self.drawList[i]
                break
        for i, h in enumerate(self.legendList):
            if h.getName() == name:
                del self.legendList[i]
                break

    ## Call a function for a named histograms.HistoBase object.
    #
    # \param name   Name of histogram
    # \param func   Function taking one parameter (histograms.HistoBase), return value is not used
    def forHisto(self, name, func):
        try:
            self.nameHistoMap[name].call(func)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to call a function for histogram '%s', which doesn't exist." % name

    ## Call each MC histograms.HistoBase with a function.
    #
    # \param func   Function taking one parameter (histograms.HistoBase), return value is not used
    def forEachMCHisto(self, func):
        def forMC(histo):
            if histo.isMC():
                func(histo)

        self.forEachHisto(forMC)

    ## Call each collision data histograms.HistoBase with a function.
    #
    # \param func  Function taking one parameter (Histo, return value is not used
    def forEachDataHisto(self, func):
        def forData(histo):
            if histo.isData():
                func(histo)
        self.forEachHisto(forData)

    ## Call each histograms.HistoBase with a function.
    #
    # \param func  Function taking one parameter (Histo), return value is not used
    def forEachHisto(self, func):
        for d in self.drawList:
            d.call(func)

    ## Check if a histograms.HistoBase with a given name exists
    #
    # \param name   Name of histograms.HistoBase to check
    def hasHisto(self, name):
        return name in self.nameHistoMap

    ## Get histograms.HistoBase of a given name
    #
    # \param name  Name of histograms.HistoBase to get
    def getHisto(self, name):
        return self.nameHistoMap[name]

    ## Get all histograms.HistoBase objects
    def getHistos(self):
        return self.drawList[:]

    ## Set legend names for given histograms.
    #
    # \param nameMap   Dictionary with name->label mappings
    def setHistoLegendLabelMany(self, nameMap):
        for name, label in nameMap.iteritems():
            try:
                self.nameHistoMap[name].setLegendLabel(label)
            except KeyError:
                print >> sys.stderr, "WARNING: Tried to set legend label for histogram '%s', which doesn't exist." % name

    ## Set the legend style for a given histogram.
    #
    # \param name   Name of the histogram
    # \param style  Style for the legend (given to TLegend as 3rd argument)
    def setHistoLegendStyle(self, name, style):
        try:
            self.nameHistoMap[name].setLegendStyle(style)
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set legend style for histogram '%s', which doesn't exist." % name

    ## Set the legend style for all histograms.
    #
    # \param style  Style for the legend (given to TLegend as 3rd argument)
    def setHistoLegendStyleAll(self, style):
        for d in self.legendList:
            d.setLegendStyle(style)

    ## Set histogram drawing style for a given histogram.
    #
    # \param name   Name of the histogram
    # \param style  Style for obj.Draw() call
    def setHistoDrawStyle(self, name, style):
        try:
            self.nameHistoMap[name].drawStyle = style
        except KeyError:
            print >> sys.stderr, "WARNING: Tried to set draw style for histogram '%s', which doesn't exist." % name

    ## Set the histogram drawing style for all histograms.
    #
    # \param style  Style for obj.Draw() call
    def setHistoDrawStyleAll(self, style):
        for d in self.drawList:
            d.drawStyle = style

    ## Add histograms to a given TLegend.
    #
    # \param legend  TLegend object
    def addToLegend(self, legend):
        for d in self.legendList:
            d.addToLegend(legend)

    ## Draw histograms.
    def draw(self):
        # Reverse the order of histograms so that the last histogram
        # is drawn first, i.e. on the bottom
        histos = self.drawList[:]
        histos.reverse()

        for h in histos:
            h.draw("same")

    ## Stack histograms.
    #
    # \param newName   Name of the histogram stack
    # \param nameList  List of histogram names to stack
    def stackHistograms(self, newName, nameList):
        (selected, notSelected, firstIndex) = dataset._mergeStackHelper(self.drawList, nameList, "stack")
        if len(selected) == 0:
            return

        stacked = HistoStacked(selected, newName)
        notSelected.insert(firstIndex, stacked)
        self.drawList = notSelected

        self.legendList = filter(lambda x: x in notSelected, self.legendList)
        self.legendList.insert(firstIndex+1, stacked)

        self._populateMap()

    ## Add MC uncertainty band histogram
    #
    # \param style        Style function for the uncertainty histogram
    # \param name         Name of the unceratinty histogram
    # \param legendLabel  Legend label for the uncertainty histogram
    # \param nameList     List of histogram names to include to the uncertainty band (\a None corresponds all MC)
    def addMCUncertainty(self, style, name="MCuncertainty", legendLabel="MC stat. unc.", nameList=None):
        mcHistos = filter(lambda x: x.isMC(), self.drawList)
        if len(mcHistos) == 0:
            print >> sys.stderr, "WARNING: Tried to create MC uncertainty histogram, but there are not MC histograms!"
            return

        if nameList != None:
            mcHistos = filter(lambda x: x.getName() in nameList, mcHistos)
        if len(mcHistos) == 0:
            print >>sys.stderr, "WARNING: No MC histograms to use for uncertainty band"
            return

        hse = HistoTotalUncertainty(mcHistos, name)
        hse.setLegendLabel(legendLabel)
        hse.call(style)

        firstMcIndex = len(self.drawList)
        for i, h in enumerate(self.drawList):
            if h.isMC():
                firstMcIndex = i
                break
        self.insertHisto(firstMcIndex, hse, legendIndex=len(self.drawList))
        
    ## \var drawList
    # List of histograms.HistoBase objects for drawing
    #
    # The histograms are drawn in the <i>reverse</i> order, i.e. the
    # first histogram is on the top, anbd the last histogram is on the
    # bottom.
    #
    ## \var legendList
    # List of histograms.HistoBase objects for TLegend
    #
    # The histograms are added to the TLegend in the order they are in
    # the list.
    #
    ## \var nameHistoMap
    # Dictionary from histograms.HistoBase names to the objects


## Collection of histograms which are managed together.
#
# The histograms in a HistoManager are drawn to one plot.

# The implementation is divided to this and HistoManagerImpl class.
# The idea is that here are the methods, which don't require Histo
# objects (namely setting the normalization), and HistoManagerImpl has
# all the methods which require the histograms.HistoBase objects. User
# can set freely the normalization scheme as many times as (s)he
# wants, and at the first time some method not implemented in
# HistoManagerBase is called, the Histo objects are created and the
# calls are delegated to HistoManagerImpl class.
class HistoManager:
    ## Constructor.
    #
    # \param args   Positional arguments
    # \param kwargs Keyword arguments
    #
    # <b>Positional arguments</b>
    # \li \a datasetMgr   DatasetManager object to take the histograms from
    # \li \a name         Path to the TH1 objects in the DatasetManager ROOT files
    #
    # <b>Keyword arguments</b>
    # \li \a datasetRootHistos   Initial list of DatasetRootHisto objects
    #
    # Only either both positional arguments or the keyword argument
    # can be given.
    #
    # \todo The interface should be fixed to have only the keyword
    #       argument (also as the only positional argument). This is
    #       not done yet for backward compatibility.
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if len(kwargs) != 1:
                raise Exception("If positional arguments are not given, there must be exactly 1 keyword argument")
            self.datasetRootHistos = kwargs["datasetRootHistos"]
        else:
            if len(args) != 2:
                raise Exception("Must give exactly 2 positional arguments (got %d)" % len(args))
            if len(kwargs) != 0:
                raise Exception("If positional arguments are given, there must not be any keyword arguments")
            datasetMgr = args[0]
            name = args[1]

            self.datasetRootHistos = datasetMgr.getDatasetRootHistos(name)

        self.impl = None
        self.luminosity = None

    ## Delegate the calls which require the histograms.HistoBase objects to the implementation class.
    #
    # \param name  Name of the attribute to get
    def __getattr__(self, name):
        if self.impl == None:
            self._createImplementation()
        return getattr(self.impl, name)

    ## Append dataset.DatasetRootHistoBase object
    #
    # \param datasetRootHisto  dataset.DatasetRootHistoBase object
    def append(self, datasetRootHisto):
        if self.impl != None:
            raise Exception("Can't append after the histograms have been created!")
        if not isinstance(datasetRootHisto, dataset.DatasetRootHistoBase):
            raise Exception("Can append only DatasetRootHistoBase derived objects, got %s" % str(datasetRootHisto))
        self.datasetRootHistos.append(datasetRootHisto)

    ## Extend with another HistoManager or a list of dataset.DatasetRootHistoBase objects
    #
    # \param datasetRootHistos  HistoManager object, or a list of dataset.DatasetRootHistoBase objects
    def extend(self, datasetRootHistos):
        if self.impl != None:
            raise Exception("Can't extend after the histograms have been created!")
        if isinstance(datasetRootHistos, HistoManager):
            if datasetRootHistos.impl != None:
                raise Exception("Can't extend from HistoManagerBase whose histograms have been created!")
            datasetRootHistos = HistoManagerBase.datasetRootHistos
        for d in datasetRootHistos:
            if not isinstance(datasetRootHisto, dataset.DatasetRootHistoBase):
                raise Exception("Can extend only DatasetRootHistoBase derived objects, got %s" % str(d))
        self.datasetRootHistos.extend(datasetRootHistos)

    ## Set the histogram normalization scheme to <i>to one</i>.
    #
    # All histograms are normalized to unit area.
    def normalizeToOne(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            h.normalizeToOne()
        self.luminosity = None

    ## Set the MC histogram normalization scheme to <i>by cross section</i>.
    #
    # All histograms from MC datasets are normalized by their cross
    # section.
    def normalizeMCByCrossSection(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            if h.getDataset().isMC():
                h.normalizeByCrossSection()
        self.luminosity = None

    ## Set the MC histogram normalization <i>by luminosity</i>.
    #
    # The set of histograms is required to contain one, and only one
    # histogram from data dataset (if there are many data datasets,
    # they should be merged first). All histograms from MC datasets
    # are normalized to the integrated luminosity of the the data
    # dataset.
    def normalizeMCByLuminosity(self):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        lumi = None
        for h in self.datasetRootHistos:
            if h.getDataset().isData():
                if lumi != None:
                    raise Exception("Unable to normalize by luminosity, more than one data datasets (you might want to merge data datasets)")
                lumi = h.getDataset().getLuminosity()

        if lumi == None:
            raise Exception("Unable to normalize by luminosity, no data datasets")

        self.normalizeMCToLuminosity(lumi)

    ## Set the MC histogram normalization <i>to luminosity</i>.
    #
    # \param lumi   Integrated luminosity (pb^-1)
    #
    # All histograms from MC datasets are normalized to the given
    # integrated luminosity.
    def normalizeMCToLuminosity(self, lumi):
        if self.impl != None:
            raise Exception("Can't normalize after the histograms have been created!")
        for h in self.datasetRootHistos:
            if h.getDataset().isMC():
                h.normalizeToLuminosity(lumi)
        self.luminosity = lumi

#    def scale(self, value):
#        """Scale the histograms with a value."""
#        if self.impl != None:
#            raise Exception("Can't scale after the histograms have been created!")
#        for h in self.datasetRootHistos:
#            h.scale(value)

    ## Get the integrated luminosity to which the MC datasets have been normalized to.
    def getLuminosity(self):
        if self.luminosity == None:
            raise Exception("No normalization by or to luminosity!")
        return self.luminosity

    ## Draw the text for the integrated luminosity.
    #
    # \param x   X coordinate of the text (\a None for default)
    # \param y   Y coordinate of the text (\a None for default)
    def addLuminosityText(self, x=None, y=None):
        addLuminosityText(x, y, self.getLuminosity())

    ## Create the HistoManagerImpl object.
    def _createImplementation(self):
        self.impl = HistoManagerImpl([Histo(h.getDataset(), h.getHistogram(), h.getName()) for h in self.datasetRootHistos])

    ## Stack all MC histograms to one named <i>StackedMC</i>.
    def stackMCHistograms(self):
        histos = self.getHistos()
        
        self.stackHistograms("StackedMC", [h.getName() for h in filter(lambda h: h.isMC(), self.getHistos())])

    ## \var datasetRootHistos
    # List of dataset.DatasetRootHisto objects to manage
    ## \var impl
    # histograms.HistoManagerImpl object for the implementation
    ## \var luminosity
    # Total integrated luminosity ofthe managed collision data (None if not set)
