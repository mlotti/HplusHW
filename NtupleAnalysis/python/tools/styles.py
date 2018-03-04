'''
\package styles

Histogram/graph (line/marker/fill) style classes and objects

\todo This package would benefit from a major overhaul...
'''

#================================================================================================  
# Import Modules
#================================================================================================  
import ROOT


#================================================================================================  
# Class Definition
#================================================================================================  
class StyleBase:
    '''
    Base class for styles
    
    The only abstraction it provides is forwarding the function call to
    apply() method call.
    
    Deribing classes should implement the \a apply() method.
    '''
    def __call__(self, h):
        '''
        Function call syntax
        
        \param h   histograms.Histo object
        
        Call apply() method with the ROOT histogram/graph object.
        '''
        self.apply(h.getRootHisto())

        gr = h.getSystematicUncertaintyGraph()
        if gr is not None:
            self.applyUncertainty(gr)

    def applyUncertainty(self, gr):
        pass

## Basic style (marker style, marker and line color)
class Style(StyleBase):
    ## Constructor
    #
    # \param marker   Marker style
    # \param color    Marker and line color
    def __init__(self, marker, color):
        self.marker = marker
        self.color = color

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
        h.SetLineWidth(2)
        h.SetLineColor(self.color)
        h.SetMarkerColor(self.color)
        h.SetMarkerStyle(self.marker)
        h.SetMarkerSize(1.2)
	h.SetFillColor(0)

    def clone(self):
        return Style(self.marker, self.color)

## Compound style
#
# Applies are contained styles
class StyleCompound(StyleBase):
    ## Constructor
    #
    # \param styles   List of style objects
    def __init__(self, styles=[]):
        self.styles = styles

    ## Append a style object
    def append(self, style):
        self.styles.append(style)

    ## Extend style objects
    def extend(self, styles):
        self.styles.extend(styles)

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
        for s in self.styles:
            s.apply(h)

    def applyUncertainty(self, gr):
        for s in self.styles:
            s.applyUncertainty(gr)

    # Clone the compound style
    def clone(self):
        return StyleCompound(self.styles[:])

## Fill style
#
# Contains a base style, and applies fill style and color on top of
# that.
#
# \todo Remove the holding of the style, this is done with
# styles.StyleCompound in much cleaner way
class StyleFill(StyleBase):
    ## Constructor
    #
    # \param style      Other style object
    # \param fillStyle  Fill style
    # \param fillColor  Fill color (if not given, line color is used as fill color)
    def __init__(self, style=None, fillStyle=1001, fillColor=None):
        self.style     = style
        self.fillStyle = fillStyle
	self.fillColor = fillColor

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
	if self.style != None:
            self.style.apply(h)
	if self.fillColor != None:
	    h.SetFillColor(self.fillColor)
	else:
	    h.SetFillColor(h.GetLineColor())
        h.SetFillStyle(self.fillStyle)

## Line style
class StyleLine(StyleBase):
    def __init__(self, lineStyle=None, lineWidth=None, lineColor=None):
        self.lineStyle = lineStyle
        self.lineWidth = lineWidth
        self.lineColor = lineColor

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
        if self.lineStyle != None:
            h.SetLineStyle(self.lineStyle)
        if self.lineWidth != None:
            h.SetLineWidth(self.lineWidth)
        if self.lineColor != None:
            h.SetLineColor(self.lineColor)

## Marker style
#
# \todo markerSizes should be handled in a cleaner way
class StyleMarker(StyleBase):
    ## Constructor
    #
    # \param markerSize   Marker size
    # \param markerColor  Marker color
    # \param markerStyle  Marker style
    # \param markerSizes  List of marker sizes. If given, marker sizes are drawn from this list succesively.
    def __init__(self, markerSize=1.2, markerColor=None, markerSizes=None, markerStyle=None):
        self.markerSize = markerSize
        self.markerColor = markerColor
        self.markerSizes = markerSizes
	self.markerStyle = markerStyle
        self.markerSizeIndex = 0

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
        if self.markerSizes == None:
            h.SetMarkerSize(self.markerSize)
        else:
            h.SetMarkerSize(self.markerSizes[self.markerSizeIndex])
            self.markerSizeIndex = (self.markerSizeIndex+1)%len(self.markerSizes)
        if self.markerColor != None:
            h.SetMarkerColor(self.markerColor)
	if self.markerStyle != None:
	    h.SetMarkerStyle(self.markerStyle)

## Error style
class StyleError(StyleBase):
    ## Constructor
    #
    # \param color      Fill color
    # \param style      Fill style
    # \param linecolor  Line color
    def __init__(self, color, style=3004, linecolor=None, styleSyst=3005):
        self.color = color
        self.style = style
        self.linecolor = linecolor
        self.styleSyst = styleSyst

    ## Apply the style
    #
    # \param h ROOT object
    def apply(self, h):
        h.SetFillStyle(self.style)
        h.SetFillColor(self.color)
        h.SetMarkerStyle(0)
        if self.linecolor != None:
            h.SetLineColor(self.color)
        else:
            h.SetLineStyle(0)
            h.SetLineWidth(0)
            h.SetLineColor(ROOT.kWhite)

    def applyUncertainty(self, gr):
        self.apply(gr)
        gr.SetFillStyle(self.styleSyst)
        

dataStyle = StyleCompound([Style(ROOT.kFullCircle, ROOT.kBlack)])
dataMcStyle = dataStyle.clone()
errorStyle = StyleCompound([StyleError(ROOT.kBlack, 3345, styleSyst=3354)])
errorStyle2 = StyleCompound([StyleError(ROOT.kGray+2, 3354)])
errorStyle3 = StyleCompound([StyleError(ROOT.kRed-10, 1001, linecolor=ROOT.kRed-10)])
errorRatioStatStyle = StyleCompound([StyleError(ROOT.kGray, 1001, linecolor=ROOT.kGray)])
errorRatioSystStyle = StyleCompound([StyleError(ROOT.kGray+1, 1001, linecolor=ROOT.kGray+1)])

ratioStyle = dataStyle.clone()
ratioLineStyle = StyleCompound([StyleLine(lineColor=ROOT.kRed, lineWidth=2, lineStyle=3)])

#mcStyle = Style(ROOT.kFullSquare, ROOT.kGreen-2)
mcStyle = StyleCompound([Style(ROOT.kFullSquare, ROOT.kRed+1)])
mcStyle2 = StyleCompound([Style(33, ROOT.kBlue-4)])
signalStyle = StyleCompound([Style(34, ROOT.kAzure+9), 
                             StyleLine(lineStyle=ROOT.kSolid, lineWidth=4)
                             ])
signalHHStyle = StyleCompound([Style(34, ROOT.kRed-8), 
                             StyleLine(lineStyle=8, lineWidth=6)
                             ])
signal80Style =  signalStyle.clone()
signal90Style =  signalStyle.clone()
signal100Style = signalStyle.clone()
signal120Style = signalStyle.clone()
signal140Style = signalStyle.clone()
signal150Style = signalStyle.clone()
signal155Style = signalStyle.clone()
signal160Style = signalStyle.clone()

signalHH80Style =  signalHHStyle.clone()
signalHH90Style =  signalHHStyle.clone()
signalHH100Style = signalHHStyle.clone()
signalHH120Style = signalHHStyle.clone()
signalHH140Style = signalHHStyle.clone()
signalHH150Style = signalHHStyle.clone()
signalHH155Style = signalHHStyle.clone()
signalHH160Style = signalHHStyle.clone()

signal145Style = signalStyle.clone()
signal150Style = signalStyle.clone()
signal155Style = signalStyle.clone()
signal160Style = signalStyle.clone()
signal165Style = signalStyle.clone()
signal170Style = signalStyle.clone()
signal175Style = signalStyle.clone()
signal180Style = signalStyle.clone()
signal190Style = signalStyle.clone()
signal200Style = signalStyle.clone()

"""
# Problem with StyleCompound: solid signal histo in control plots. 13122016/SL
signal200Style = StyleCompound([
        Style(ROOT.kFullCross, ROOT.kBlue), 
        StyleMarker(markerSize=1.2, markerColor=ROOT.kBlue, markerSizes=None, markerStyle=ROOT.kFullCross),
        StyleFill(fillStyle=1001, fillColor=ROOT.kBlue), 
        StyleLine(lineStyle=ROOT.kDashed, lineWidth=3, lineColor=ROOT.kBlue) ])
signal220Style = signalStyle.clone()
signal250Style = signalStyle.clone()
signal300Style = StyleCompound([
        Style(ROOT.kFullTriangleUp, ROOT.kRed), 
        StyleMarker(markerSize=1.2, markerColor=ROOT.kRed, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
        StyleFill(fillStyle=1001, fillColor=ROOT.kRed), 
        StyleLine(lineStyle=ROOT.kSolid, lineWidth=3, lineColor=ROOT.kRed) ])
signal350Style = signalStyle.clone()
signal400Style = StyleCompound([
        Style(ROOT.kFullTriangleDown, ROOT.kSpring+5), 
        StyleMarker(markerSize=1.2, markerColor=ROOT.kSpring+5, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
        StyleFill(fillStyle=1001, fillColor=ROOT.kSpring+5), 
        StyleLine(lineStyle=ROOT.kSolid, lineWidth=3, lineColor=ROOT.kSpring+5) ])
signal500Style = StyleCompound([
        Style(ROOT.kFullCircle, ROOT.kBlue+3), 
        StyleMarker(markerSize=1.2, markerColor=ROOT.kBlue+3, markerSizes=None, markerStyle=ROOT.kFullCircle),
        StyleFill(fillStyle=1001, fillColor=ROOT.kBlue+3), 
        StyleLine(lineStyle=ROOT.kDashed, lineWidth=3, lineColor=ROOT.kBlue+3) ])
"""
signal180Style  = signalStyle.clone()
signal200Style  = signalStyle.clone()
signal220Style  = signalStyle.clone()
signal250Style  = signalStyle.clone()
signal300Style  = signalStyle.clone()   
signal350Style  = signalStyle.clone()   
signal400Style  = signalStyle.clone()   
signal500Style  = signalStyle.clone()   
signal600Style  = signalStyle.clone()
signal650Style  = signalStyle.clone()
signal700Style  = signalStyle.clone()
signal750Style  = signalStyle.clone()
signal800Style  = signalStyle.clone()
signal1000Style = signalStyle.clone()
signal1500Style = signalStyle.clone()
signal2000Style = signalStyle.clone()
signal2500Style = signalStyle.clone()
signal3000Style = signalStyle.clone()
signal5000Style = signalStyle.clone()
signal7000Style = signalStyle.clone()
signal1000Style = signalStyle.clone()

dibStyle          = Style(ROOT.kMultiply, ROOT.kBlue-4)
dyStyle           = Style(ROOT.kStar, ROOT.kTeal-9)
ewkFillStyle      = StyleCompound([StyleFill(fillColor=ROOT.kMagenta-2)])
ewkStyle          = Style(ROOT.kFullTriangleDown, ROOT.kRed-4)
ewkfakeFillStyle  = StyleCompound([StyleFill(fillColor=ROOT.kGreen+2)])
qcdBEnrichedStyle = Style(ROOT.kOpenTriangleUp, ROOT.kOrange-3)
qcdFillStyle      = StyleCompound([StyleFill(fillColor=ROOT.kOrange-2)])
qcdStyle          = Style(ROOT.kFullTriangleUp, ROOT.kOrange-2)
singleTopStyle    = Style(ROOT.kOpenDiamond, ROOT.kTeal+9)
stStyle           = Style(ROOT.kPlus, ROOT.kSpring+4)
stsStyle          = Style(ROOT.kPlus, ROOT.kSpring-9)
sttStyle          = Style(ROOT.kPlus, ROOT.kSpring-7)
sttwStyle         = stStyle
ttStyle           = Style(ROOT.kFullSquare, ROOT.kMagenta-2)
ttbbStyle         = Style(ROOT.kOpenCross, ROOT.kPink-9)
ttjetsStyle       = Style(ROOT.kPlus, ROOT.kMagenta-4)
ttttStyle         = Style(ROOT.kFullStar, ROOT.kYellow-9)
ttwStyle          = Style(ROOT.kOpenSquare, ROOT.kSpring+9)
ttzStyle          = Style(ROOT.kFullDiamond, ROOT.kAzure-4)
wStyle            = Style(ROOT.kFullTriangleDown, ROOT.kOrange+9)
wjetsStyle        = Style(ROOT.kStar, ROOT.kOrange+9)
wwStyle           = Style(ROOT.kMultiply, ROOT.kPink-9)
wzStyle           = Style(ROOT.kMultiply, ROOT.kPink-7)
zjetsStyle        = Style(ROOT.kFullCross, ROOT.kRed-7)
zzStyle           = Style(ROOT.kMultiply, ROOT.kPink-5)
ttXStyle          = Style(ROOT.kOpenSquare, ROOT.kAzure-4)
noTopStyle        = Style(ROOT.kOpenSquare, ROOT.kRed+1) #ROOT.kRed-9)
#StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kBlue-3, markerSizes=None, markerStyle=4),
#                                   StyleLine(lineColor=ROOT.kBlue-3, lineStyle=ROOT.kSolid, lineWidth=4), 
#                                   StyleFill(fillColor=ROOT.kBlue-3, fillStyle=3001)])

baselineStyle     = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kBlue, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
                                   StyleLine(lineColor=ROOT.kBlue, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kBlue, fillStyle=1001)])
baselineLineStyle = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kAzure+2, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
                                   StyleLine(lineColor=ROOT.kAzure+2, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kAzure+2, fillStyle=0)])
invertedStyle     = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kRed-4, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kRed-4, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kRed-4, fillStyle=1001)])
altEwkStyle       = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kMagenta-2, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kMagenta-2, lineStyle=ROOT.kSolid, lineWidth=3),
                                   StyleFill(fillColor=ROOT.kMagenta-2, fillStyle=1001)])
altEwkLineStyle   = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kMagenta-2, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kMagenta-2, lineStyle=ROOT.kSolid, lineWidth=3),
                                   StyleFill(fillColor=ROOT.kMagenta-2, fillStyle=0)])
invertedLineStyle = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kRed, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kRed, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kRed, fillStyle=0)])
altQCDStyle       = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kOrange-2, markerSizes=None, markerStyle=ROOT.kFullDiamond),
                                   StyleLine(lineColor=ROOT.kOrange-2, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kOrange-2, fillStyle=3001)])
genuineBStyle     = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kAzure-2, markerSizes=None, markerStyle=ROOT.kFullCircle),
                                   StyleLine(lineColor=ROOT.kAzure-2, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kAzure-2, fillStyle=1001)])
genuineBLineStyle = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kGreen+2, markerSizes=None, markerStyle=ROOT.kFullCircle),
                                   StyleLine(lineColor=ROOT.kGreen+2, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kGreen+2, fillStyle=0)])
fakeBStyle        = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kOrange-3, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kOrange-3, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kOrange-3, fillStyle=1001)]) #fillStyle=3005)])
fakeBLineStyle    = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kOrange-3, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kOrange-3, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kOrange-3, fillStyle=0)])
fakeBLineStyle1   = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kRed, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kRed, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kRed, fillStyle=0)])
signalStyleHToTB  = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kRed-7, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kRed-7, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kRed-7, fillStyle=0)])
signalFillStyleHToTB  = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kYellow-7, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kYellow-7, lineStyle=ROOT.kSolid, lineWidth=1), 
                                   StyleFill(fillColor=ROOT.kYellow-7, fillStyle=10001)])
signalStyleHToTB180 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kGray, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kGray, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kGray, fillStyle=0)])
signalStyleHToTB200 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kPink-2, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kPink-2, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kPink-2, fillStyle=0)])
signalStyleHToTB300 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kTeal+3, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kTeal+3, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kTeal+3, fillStyle=0)])
signalStyleHToTB400 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kOrange-2, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kOrange-2, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kOrange-2, fillStyle=0)])
signalStyleHToTB500 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kAzure-1, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kAzure-1, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kAzure-1, fillStyle=0)])
signalStyleHToTB800 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kSpring-4, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kSpring-4, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kSpring-4, fillStyle=0)])
signalStyleHToTB1000 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kOrange+2, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kOrange+2, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kOrange+2, fillStyle=0)])
signalStyleHToTB2000 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kViolet-9, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kViolet-9, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kViolet-9, fillStyle=0)])
signalStyleHToTB3000 = StyleCompound([StyleMarker(markerSize=0, markerColor=ROOT.kRed+2, markerSizes=None, markerStyle=4),
                                   StyleLine(lineColor=ROOT.kRed+2, lineStyle=ROOT.kDashed, lineWidth=4), 
                                   StyleFill(fillColor=ROOT.kRed+2, fillStyle=0)])

# FakeB Style
FakeBStyle1 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kRed, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
                                   StyleLine(lineColor=ROOT.kRed, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kRed, fillStyle=1001)])
FakeBStyle2 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kOrange-3, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kOrange-3, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kOrange-3, fillStyle=1001)])
FakeBStyle3 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kBlue, markerSizes=None, markerStyle=ROOT.kFullCircle),
                                   StyleLine(lineColor=ROOT.kBlue, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kBlue, fillStyle=1001)])
FakeBStyle4 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kAzure+1, markerSizes=None, markerStyle=ROOT.kFullSquare),
                                   StyleLine(lineColor=ROOT.kAzure+1, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kAzure+1, fillStyle=1001)])
FakeBStyle5 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kPink-2, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
                                   StyleLine(lineColor=ROOT.kPink-2, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kPink-2, fillStyle=1001)])
FakeBStyle6 = StyleCompound([StyleMarker(markerSize=1.2, markerColor=ROOT.kViolet-5, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
                                   StyleLine(lineColor=ROOT.kViolet-5, lineStyle=ROOT.kSolid, lineWidth=3), 
                                   StyleFill(fillColor=ROOT.kViolet-5, fillStyle=1001)])

styles = [ 
    Style(26, ROOT.kBlue),
    Style(27, ROOT.kRed),
    Style(23, ROOT.kGreen+2),
    Style(24, ROOT.kMagenta),
    Style(28, ROOT.kCyan),
    Style(29, ROOT.kYellow+2),
    Style(30, ROOT.kOrange+9),
    Style(31, ROOT.kOrange+3),
    Style(32, ROOT.kMagenta+3),
    Style(33, ROOT.kGray+2),
    Style(34, ROOT.kBlue+3),
    Style(35, ROOT.kOrange+1),
    Style(36, ROOT.kCyan-5),
    Style(22, ROOT.kBlue),
    Style(25, ROOT.kBlack)
    ]

stylesCompound = [ 
    StyleCompound([
            StyleMarker(markerSize=1.2, markerColor=ROOT.kBlack, markerSizes=None, markerStyle=ROOT.kFullCircle),
            StyleLine(lineColor=ROOT.kBlack, lineStyle=ROOT.kSolid, lineWidth=3), 
            StyleFill(fillColor=ROOT.kBlack, fillStyle=1001)]),
    StyleCompound([
            StyleMarker(markerSize=1.2, markerColor=ROOT.kOrange-2, markerSizes=None, markerStyle=ROOT.kFullTriangleUp),
            StyleLine(lineColor=ROOT.kOrange-2, lineStyle=ROOT.kDashed, lineWidth=3), 
            StyleFill(fillColor=ROOT.kOrange-2, fillStyle=1001)]),
    StyleCompound([
            StyleMarker(markerSize=1.2, markerColor=ROOT.kMagenta-2, markerSizes=None, markerStyle=ROOT.kFullTriangleDown),
            StyleLine(lineColor=ROOT.kMagenta-2, lineStyle=ROOT.kSolid, lineWidth=3),  #ROOT.kDashDotted
            StyleFill(fillColor=ROOT.kMagenta-2, fillStyle=3001)]),
    StyleCompound([
            StyleMarker(markerSize=1.2, markerColor=ROOT.kGreen+2, markerSizes=None, markerStyle=ROOT.kFullCross),
            StyleLine(lineColor=ROOT.kGreen+2, lineStyle=ROOT.kDotted, lineWidth=3), 
            StyleFill(fillColor=ROOT.kGreen+2, fillStyle=1001)]),
    ]


def applyStyle(h, ind):
    styles[ind].apply(h)

def getDataStyle():
    return dataStyle

def getEWKStyle():
    return ewkFillStyle

def getAltEWKStyle():
    return altEwkStyle

def getAltEWKLineStyle():
    return altEwkLineStyle

def getEWKFillStyle():
    return ewkFillStyle

def getEWKLineStyle():
    return ewkStyle

def getEWKFakeStyle():
    return ewkfakeFillStyle

def getAltQCDStyle():
    return altQCDStyle

def getQCDStyle():
    return qcdFillStyle

def getQCDFillStyle():
    return qcdFillStyle

def getQCDLineStyle():
    return qcdStyle

def getABCDStyle(region):
    if region == "SR":
        return FakeBStyle1
    elif region == "CR1" or region == "CRone":
        return FakeBStyle2
    elif region == "VR":
        return FakeBStyle3
    elif region == "CR2" or region == "CRtwo":
        return FakeBStyle4
    elif region == "CR3" or region == "CRthree":
        return FakeBStyle5
    elif region == "CR4" or region == "CRfour":
        return FakeBStyle6
    else:
        print "Invalid region \"%s\". Returning qcd style" % (region)
        return qcdStyle

def getBaselineStyle():
    return baselineStyle

def getBaselineLineStyle():
    return baselineLineStyle

def getGenuineBStyle():
    return genuineBStyle

def getGenuineBLineStyle():
    return genuineBLineStyle

def getFakeBStyle():
    return fakeBStyle

def getFakeBLineStyle():
    return fakeBLineStyle

def getInvertedStyle():
    return invertedStyle

def getInvertedLineStyle():
    return invertedLineStyle

def getSignalStyle():
    return signalStyle

def getSignalStyleHToTB():
    return signalStyleHToTB

def getSignalStyleHToTB():
    return signalFillStyleHToTB

def getSignalStyleHToTB_M(myMass):

    mass = str(myMass)
    if mass == "180":
        return signalStyleHToTB180
    elif mass == "200":
        return signalStyleHToTB200
    elif mass == "300":
        return signalStyleHToTB300
    elif mass == "400":
        return signalStyleHToTB400
    elif mass == "500":
        return signalStyleHToTB500
    elif mass == "650":
        return signalStyleHToTB650
    elif mass == "800":
          return signalStyleHToTB800
    elif mass == "1000":
        return signalStyleHToTB1000
    elif mass == "2000":
        return signalStyleHToTB2000
    elif mass == "3000":
        return signalStyleHToTB3000
    else:
        print "Invalid mass point \"%s\". Returning default style" % (mass)
    return signalStyleHToTB500        

def getErrorStyle():
    return errorStyle

def getStyles():
    return styles

def getStylesFill(**kwargs):
    return [StyleFill(s, **kwargs) for s in styles]

class Generator:
    def __init__(self, styles):
        self.styles = styles
        self.index = 0

    def reset(self, index=0):
        self.index = index

    def reorder(self, indices):
        self.styles = [self.styles[i] for i in indices]

    def next(self):
        self.index = (self.index+1) % len(self.styles)

    def __call__(self, h):
        self.styles[self.index](h)
        self.next()

def generator(fill=False, **kwargs):
    if fill:
        return Generator(getStylesFill(**kwargs))
    else:
        return Generator(getStyles(**kwargs))

def generator2(styleCustomisations, styles=styles):
    if not isinstance(styleCustomisations, list):
        styleCustomisations = [styleCustomisations]
    return Generator([StyleCompound([s]+styleCustomisations) for s in styles])
