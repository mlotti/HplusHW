//
// LHCHIGGS Style, based on a style file from BaBar and ATLAS
//

#include <iostream>

#include "Plotter/interface/LHCHiggsStyle.h"

#include "TROOT.h"

void SetLHCHiggsStyle ()
{
  static TStyle* lhchiggsStyle = 0;
////  std::cout << "\nApplying LHCHIGGS style settings...\n" << std::endl ;
  if ( lhchiggsStyle==0 ) lhchiggsStyle = LHCHiggsStyle();
  gROOT->SetStyle("LHCHIGGS");
  gROOT->ForceStyle();
}

TStyle* LHCHiggsStyle() 
{
  TStyle *lhchiggsStyle = new TStyle("LHCHIGGS","LHCHiggs style");

  // use plain black on white colors
  Int_t icol=0; // WHITE
  lhchiggsStyle->SetFrameBorderMode(icol);
  lhchiggsStyle->SetFrameFillColor(icol);
  lhchiggsStyle->SetCanvasBorderMode(icol);
  lhchiggsStyle->SetCanvasColor(icol);
  lhchiggsStyle->SetPadBorderMode(icol);
  lhchiggsStyle->SetPadColor(icol);
  lhchiggsStyle->SetStatColor(icol);
  //lhchiggsStyle->SetFillColor(icol); // don't use: white fill color for *all* objects

  // set the paper & margin sizes
  lhchiggsStyle->SetPaperSize(20,26);

  // set margin sizes
  lhchiggsStyle->SetPadTopMargin(0.05);
  lhchiggsStyle->SetPadRightMargin(0.05);
  lhchiggsStyle->SetPadBottomMargin(0.16);
  lhchiggsStyle->SetPadLeftMargin(0.16);

  // set title offsets (for axis label)
  lhchiggsStyle->SetTitleXOffset(1.4);
  lhchiggsStyle->SetTitleYOffset(1.4);

  // set label offsets 
  lhchiggsStyle->SetTitleOffset(0.9,"x");
  lhchiggsStyle->SetTitleOffset(0.8,"y");

  // use large fonts
  //Int_t font=72; // Helvetica italics
  Int_t font=42; // Helvetica
  Double_t tsize=0.05;
  lhchiggsStyle->SetTextFont(font);

  lhchiggsStyle->SetTextSize(tsize);
  lhchiggsStyle->SetLabelFont(font,"x");
  lhchiggsStyle->SetTitleFont(font,"x");
  lhchiggsStyle->SetLabelFont(font,"y");
  lhchiggsStyle->SetTitleFont(font,"y");
  lhchiggsStyle->SetLabelFont(font,"z");
  lhchiggsStyle->SetTitleFont(font,"z");
  
  lhchiggsStyle->SetLabelSize(tsize,"x");
  lhchiggsStyle->SetTitleSize(tsize,"x");
  lhchiggsStyle->SetLabelSize(tsize,"y");
  lhchiggsStyle->SetTitleSize(tsize,"y");
  lhchiggsStyle->SetLabelSize(tsize,"z");
  lhchiggsStyle->SetTitleSize(tsize,"z");

  // use bold lines and markers
  lhchiggsStyle->SetMarkerStyle(20);
  lhchiggsStyle->SetMarkerSize(1.2);
  lhchiggsStyle->SetHistLineWidth(2.);
  lhchiggsStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes

  // get rid of X error bars 
  //lhchiggsStyle->SetErrorX(0.001);
  // get rid of error bar caps
  lhchiggsStyle->SetEndErrorSize(0.);

  // do not display any of the standard histogram decorations
  lhchiggsStyle->SetOptTitle(0);
  //lhchiggsStyle->SetOptStat(1111);
  lhchiggsStyle->SetOptStat(0);
  //lhchiggsStyle->SetOptFit(1111);
  lhchiggsStyle->SetOptFit(0);

  // put tick marks on top and RHS of plots
  lhchiggsStyle->SetPadTickX(1);
  lhchiggsStyle->SetPadTickY(1);

  return lhchiggsStyle;

}

