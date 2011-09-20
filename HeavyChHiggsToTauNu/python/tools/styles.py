import ROOT

class StyleBase:
    def __call__(self, h):
        self.apply(h.getRootHisto())

class Style(StyleBase):
    def __init__(self, marker, color):
        self.marker = marker
        self.color = color

    def apply(self, h):
        h.SetLineWidth(2)
        h.SetLineColor(self.color)
        h.SetMarkerColor(self.color)
        h.SetMarkerStyle(self.marker)
        h.SetMarkerSize(1.2)
	h.SetFillColor(0)

class StyleCompound(StyleBase):
    def __init__(self, styles=[]):
        self.styles = styles

    def append(self, style):
        self.styles.append(style)

    def apply(self, h):
        for s in self.styles:
            s.apply(h)

    def clone(self):
        return StyleCompound(self.styles[:])

class StyleFill(StyleBase):
    def __init__(self, style, fillStyle=1001):
        self.style = style
        self.fillStyle = fillStyle

    def apply(self, h):
        self.style.apply(h)
        h.SetFillColor(self.style.color)
        #h.SetFillStyle(3002)
        h.SetFillStyle(self.fillStyle)

class StyleLine(StyleBase):
    def __init__(self, lineStyle=None, lineWidth=None, lineColor=None):
        self.lineStyle = lineStyle
        self.lineWidth = lineWidth
        self.lineColor = lineColor

    def apply(self, h):
        if self.lineStyle != None:
            h.SetLineStyle(self.lineStyle)
        if self.lineWidth != None:
            h.SetLineWidth(self.lineWidth)
        if self.lineColor != None:
            h.SetLineColor(self.lineColor)

class StyleMarker(StyleBase):
    def __init__(self, markerSize=1.2, markerColor=None, markerSizes=None):
        self.markerSize = markerSize
        self.markerColor = markerColor
        self.markerSizes = markerSizes
        self.markerSizeIndex = 0

    def apply(self, h):
        if self.markerSizes == None:
            h.SetMarkerSize(self.markerSize)
        else:
            h.SetMarkerSize(self.markerSizes[self.markerSizeIndex])
            self.markerSizeIndex = (self.markerSizeIndex+1)%len(self.markerSizes)
        if self.markerColor != None:
            h.SetMarkerColor(self.markerColor)

class StyleError(StyleBase):
    def __init__(self, color, style=3004, linecolor=None):
        self.color = color
        self.style = style
        self.linecolor = linecolor

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

dataStyle = StyleCompound([Style(ROOT.kFullCircle, ROOT.kBlack)])
dataMcStyle = dataStyle.clone()
errorStyle = StyleCompound([StyleError(ROOT.kBlack, 3354)])
errorStyle2 = StyleCompound([StyleError(ROOT.kGray+2, 3354)])
errorStyle3 = StyleCompound([StyleError(ROOT.kRed-10, 1001, linecolor=ROOT.kRed-10)])

#mcStyle = Style(ROOT.kFullSquare, ROOT.kGreen-2)
mcStyle = StyleCompound([Style(ROOT.kFullSquare, ROOT.kRed+1)])
signalStyle = StyleCompound([Style(34, ROOT.kPink-9), 
                             StyleLine(lineStyle=ROOT.kDashed, lineWidth=6)
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

signal180Style = signalStyle.clone()
signal190Style = signalStyle.clone()
signal200Style = signalStyle.clone()
signal220Style = signalStyle.clone()
signal250Style = signalStyle.clone()
signal300Style = signalStyle.clone()

qcdStyle = Style(ROOT.kFullTriangleUp, ROOT.kOrange-2)
ewkStyle = Style(ROOT.kFullTriangleDown, ROOT.kRed-4)
ttStyle = Style(ROOT.kFullSquare, ROOT.kMagenta-2)
wStyle = Style(ROOT.kFullTriangleDown, ROOT.kOrange+9)

wwStyle = Style(ROOT.kMultiply, ROOT.kPink-9)
wzStyle = Style(ROOT.kMultiply, ROOT.kPink-7)
zzStyle = Style(ROOT.kMultiply, ROOT.kPink-5)
dibStyle = Style(ROOT.kMultiply, ROOT.kBlue-4)

stsStyle = Style(ROOT.kPlus, ROOT.kSpring-9)
sttStyle = Style(ROOT.kPlus, ROOT.kSpring-7)
sttwStyle = Style(ROOT.kPlus, ROOT.kSpring+4)
stStyle = sttwStyle

dyStyle = Style(ROOT.kStar, ROOT.kTeal-9)

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


def applyStyle(h, ind):
    styles[ind].apply(h)

def getDataStyle():
    return dataStyle

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
