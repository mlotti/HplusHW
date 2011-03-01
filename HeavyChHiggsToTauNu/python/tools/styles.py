import ROOT

class Style:
    def __init__(self, style, color):
        self.style = 22 + style
        self.color = color

    def apply(self, h):
        h.SetLineWidth(2)
        h.SetLineColor(self.color)
        h.SetMarkerColor(self.color)
        h.SetMarkerStyle(self.style)
        h.SetMarkerSize(1)
	h.SetFillColor(0)

    def __call__(self, h):
        self.apply(h.getRootHisto())

class StyleFill:
    def __init__(self, style, fillStyle=1001):
        self.style = style
        self.fillStyle = fillStyle

    def apply(self, h):
        self.style.apply(h)
        h.SetFillColor(self.style.color)
        #h.SetFillStyle(3002)
        h.SetFillStyle(self.fillStyle)

    def __call__(self, h):
        self.apply(h.getRootHisto())

class StyleError:
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

    def __call__(self, h):
        self.apply(h.getRootHisto())

dataStyle = Style(-2, ROOT.kBlack)
errorStyle = StyleError(ROOT.kBlack, 3354)
errorStyle2 = StyleError(ROOT.kGray+2, 3354)
errorStyle3 = StyleError(ROOT.kRed-10, 1001, linecolor=ROOT.kRed-10)

#signal90Style =  Style(4, ROOT.kBlue)
signal90Style =  Style(5, ROOT.kRed+1)
signal100Style = Style(4, ROOT.kBlue)
signal120Style = Style(4, ROOT.kBlue)
signal140Style = Style(4, ROOT.kBlue)
signal160Style = Style(4, ROOT.kBlue)

qcdStyle = Style(7, ROOT.kYellow+1)
wStyle = Style(1, ROOT.kGreen+2)
#ttStyle = Style(5, ROOT.kRed+1)
ttStyle = Style(4, ROOT.kBlue)
dyStyle = Style(5, ROOT.kRed+1)
#dyStyle = Style(12, ROOT.kBlue-3)
stStyle = Style(2, ROOT.kMagenta)
dibStyle = Style(6, ROOT.kCyan)

styles = [
    Style(4, ROOT.kBlue),
    Style(5, ROOT.kRed),
    wStyle,
    stStyle,
    dibStyle,
    Style(7, ROOT.kYellow+2),
    Style(8, ROOT.kOrange+9),
    Style(9, ROOT.kOrange+3),
    Style(10, ROOT.kMagenta+3),
    Style(11, ROOT.kGray+2),
    Style(12, ROOT.kBlue+3),
    Style(13, ROOT.kOrange+1),
    Style(14, ROOT.kCyan-5),
    Style(0, ROOT.kBlue),
    Style(3, ROOT.kBlack)
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

    def reset(self):
        self.index = 0

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
