#include <iostream>
#include <cmath>

#include "Rtypes.h"

#include "LHCHiggsUtils.h"
// #ifndef __CINT__
#include "LHCHiggsStyle.C"
// #endif

#include "TCanvas.h"
#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TRandom.h"
#include "TGraphErrors.h"

using namespace std;

void LHCHiggsExample() 
{ 

#ifdef __CINT__
  gROOT->LoadMacro("LHCHiggsUtils.C");
#endif

  SetLHCHiggsStyle();

  TCanvas* c1 = new TCanvas("c1","Higgs Cross Section",50,50,600,600);
  TPad* thePad = (TPad*)c1->cd();
  thePad->SetLogy();

  Double_t ymin=1.e-2;  Double_t ymax=1.e2;
  Double_t xmin=90.00;  Double_t xmax=600.;
  TH1F *h1 = thePad->DrawFrame(xmin,ymin,xmax,ymax);
  h1->SetYTitle("#sigma_{pp #rightarrow H} [pb]");
  h1->SetXTitle("M_{H}  [GeV]");
  h1->GetYaxis()->SetTitleOffset(1.4);
  h1->GetXaxis()->SetTitleOffset(1.4);
  //h1->GetXaxis()->SetNdivisions(5);
  h1->Draw();

  myText(0.2,0.88,1,"#sqrt{s}= 13 TeV");
  myBoxText(0.55,0.67,0.05,5,"NNLO QCD");

  LHCHIGGS_LABEL(0.98,0.725);
  myText(0.2,0.2,1,"Preliminary");

  c1->Print("LHCHiggsExample.eps");
  c1->Print("LHCHiggsExample.png");
  c1->Print("LHCHiggsExample.pdf");

}

#ifndef __CINT__

int main()  { 
  
  LHCHiggsExample();

  return 0;
}

#endif
