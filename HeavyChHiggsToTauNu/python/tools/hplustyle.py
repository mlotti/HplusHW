from ROOT import *
from array import array

class HPlusStyle:
  HplusStyle = TStyle("HplusStyle", "Neat style");
  
  HplusStyle.SetCanvasBorderMode(0)
  HplusStyle.SetCanvasColor(kWhite)
  HplusStyle.SetPadBorderMode(0)
  HplusStyle.SetPadColor(kWhite)
  HplusStyle.SetTitleFillColor(kWhite)
  HplusStyle.SetGridColor(0)
  HplusStyle.SetFrameBorderMode(0)
  HplusStyle.SetFrameBorderSize(1)
  HplusStyle.SetFrameFillColor(0)
  HplusStyle.SetFrameFillStyle(0)
  HplusStyle.SetFrameLineColor(1)
  HplusStyle.SetFrameLineStyle(1)
  HplusStyle.SetFrameLineWidth(1)
  #HplusStyle.SetFillColor(kWhite)
  HplusStyle.SetOptTitle(0)
  HplusStyle.SetTitleFont(42, "XYZ")
  HplusStyle.SetTitleFontSize(0.05)
  HplusStyle.SetTitleSize(0.06, "XYZ")
  HplusStyle.SetTextFont(42)
  HplusStyle.SetTitleXOffset(0.9)
  HplusStyle.SetTitleYOffset(1.25)
  
  HplusStyle.SetLabelColor(1, "XYZ")
  HplusStyle.SetLabelFont(42, "XYZ")
  HplusStyle.SetLabelOffset(0.007, "XYZ")
  HplusStyle.SetLabelSize(0.05, "XYZ")
  HplusStyle.SetPadTickX(1)
  HplusStyle.SetPadTickY(1)
  HplusStyle.SetNdivisions(508,"XYZ")
  
  HplusStyle.SetPadTopMargin(0.05)
  HplusStyle.SetPadBottomMargin(0.12)
  HplusStyle.SetPadLeftMargin(0.16)
  HplusStyle.SetPadRightMargin(0.04)
  HplusStyle.SetCanvasDefH(1280)
  HplusStyle.SetCanvasDefW(1024)
  HplusStyle.SetCanvasDefX(0)
  HplusStyle.SetCanvasDefY(0)
  HplusStyle.SetPaintTextFormat("5.2f")
  #HplusStyle.SetPalette(1, 0)
  #HplusStyle.SetOptStat(0)
  HplusStyle.SetOptStat(1111)
### Statistics Box
  HplusStyle.SetStatX(0.9)
  HplusStyle.SetStatY(0.9)
  #HplusStyle.SetStatW(0.19) #default
  #HplusStyle.SetStatH(0.1) #default
  HplusStyle.SetStatW(0.15)
  HplusStyle.SetStatH(0.1)
  HplusStyle.cd()
  
