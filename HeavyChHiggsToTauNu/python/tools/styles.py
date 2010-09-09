import ROOT

def applyStyle(h, ind):
    styles = [
        (3, ROOT.kBlack),
        (4, ROOT.kBlue),
        (5, ROOT.kRed),
        (1, ROOT.kGreen+2),
        (2, ROOT.kMagenta),
        (6, ROOT.kCyan),
        (7, ROOT.kYellow+2),
        (8, ROOT.kOrange+9),
        (9, ROOT.kOrange+3),
        (10, ROOT.kMagenta+3),
        (11, ROOT.kGray+2),
        (12, ROOT.kBlue+3),
        (13, ROOT.kOrange+1),
        (14, ROOT.kCyan-5),
        (0, ROOT.kBlue),
        ]

    style = 22 + styles[ind][0]
    color = styles[ind][1]

    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(style)
    h.SetMarkerSize(1)

