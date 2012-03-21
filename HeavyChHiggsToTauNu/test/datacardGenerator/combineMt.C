#include <TCanvas.h>
#include <TH1.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TFile.h>
#include <TColor.h>
#include <THStack.h>
#include <TMath.h>
#include <TLatex.h>

#include <iostream>
#include <iomanip>
#include <sstream>


bool paperStatus = true;
//bool paperStatus = false;

using namespace std;

void plot(int mass) {
  double myQCDRelUncert = 0.038;
  double myEWKRelUncert = 0.131;
  double myFakesRelUncert = 0.238;
  double delta = 1.4;
  double br = 0.05;
  bool debug = false;
  bool log = false;
  double ymin = 0.001;
  double ymax = 48;
  
  static bool bMessage = false;
  if (!bMessage) {
    cout << "Values used as relative uncertainty (please check):" << endl;
    cout << "  QCD: " << myQCDRelUncert << endl;
    cout << "  EWK genuine tau: " << myEWKRelUncert << endl;
    cout << "  EWK fake tau: " << myFakesRelUncert << endl << endl;
    bMessage = true;
  }
  cout << "Processing mass point: " << mass << " GeV/c2" << endl;
  
  gStyle->SetOptFit(1);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  gStyle->SetTitleFont(43, "xyz");
  gStyle->SetTitleSize(33, "xyz");
  gStyle->SetLabelFont(43, "xyz");
  gStyle->SetLabelSize(27, "xyz");
  
  //std::string infile = "EPS_data_nodeltaphi/hplus_100.root";
  //std::string infile = "EPS_data_deltaphi160/hplus_100.root";
  std::stringstream s;
  s << "lands_histograms_hplushadronic_m" << mass << ".root";

  std::string infile = s.str();
  
 // Canvas
  TCanvas *myCanvas = new TCanvas("myCanvas", "",0,0,600,600);
  myCanvas->SetHighLightColor(2);
  myCanvas->Range(0,0,1,1);
  myCanvas->SetFillColor(0);
  myCanvas->SetBorderMode(0);
  myCanvas->SetBorderSize(2);
  if (log)
    myCanvas->SetLogy();
  myCanvas->SetTickx(1);
  myCanvas->SetTicky(1);
  myCanvas->SetLeftMargin(0.16);
  myCanvas->SetRightMargin(0.05);
  myCanvas->SetTopMargin(0.05);
  myCanvas->SetBottomMargin(0.08);
  myCanvas->SetFrameFillStyle(0);
  myCanvas->SetFrameBorderMode(0);
  myCanvas->SetFrameFillStyle(0);
  myCanvas->SetFrameBorderMode(0);
  myCanvas->cd();

  Int_t ci;

  TFile* f = TFile::Open(infile.c_str());
  s.str("");
  s << "HW" << mass << "_1";
  TH1* hw = (TH1*)f->Get(s.str().c_str());
  s.str("");
  s << "HH" << mass << "_1";
  TH1* hh = (TH1*)f->Get(s.str().c_str());
  TH1* data = (TH1*)f->Get("data_obs");
  data->SetLineWidth(2);
  data->SetMarkerStyle(20);
  data->SetMarkerSize(1.2);

  TH1* ewktau = (TH1*)f->Get("EWK_Tau");
  ci = TColor::GetColor("#993399");
  ewktau->SetFillColor(ci);
  ewktau->SetLineWidth(0);
  TH1* ewkDY = (TH1*)f->Get("EWK_DYx");
  TH1* ewkVV = (TH1*)f->Get("EWK_VVx");
  ewktau->Add(ewkDY);
  ewktau->Add(ewkVV);
  
  //TH1* qcd = (TH1*)f->Get("QCDInv");
  TH1* qcd = (TH1*)f->Get("QCD");
  ci = TColor::GetColor("#ffcc33");
  qcd->SetFillColor(ci);
  qcd->SetLineWidth(0);
  TH1* fakett = (TH1*)f->Get("fake_tt");
  ci = TColor::GetColor("#669900");
  fakett->SetFillColor(ci);
  fakett->SetLineWidth(0);
  TH1* fakeW = (TH1*)f->Get("fake_W");
  ci = TColor::GetColor("#cc3300");
  fakeW->SetFillColor(ci);
  fakeW->SetLineWidth(0);
  TH1* faket = (TH1*)f->Get("fake_t");

  TH1F *hFrame = new TH1F("hFrame","",20,0,400);
  hFrame->SetMinimum(ymin);
  if (log)
    hFrame->SetMaximum(ymax*1.5);
  else
    hFrame->SetMaximum(ymax);
  hFrame->SetDirectory(0);
  hFrame->SetStats(0);
  hFrame->SetLineStyle(0);
  hFrame->SetMarkerStyle(20);
  hFrame->SetXTitle("Transverse mass (#tau jet, E_{T}^{miss}) (GeV/c^{2})");
  hFrame->SetYTitle("Events / 20 GeV/c^{2}");
  if (paperStatus) {
    hFrame->SetXTitle("Transverse mass (#tau_{h}, E_{T}^{miss}) (GeV)");
    hFrame->SetYTitle("Events / 20 GeV");
  }
  hFrame->GetXaxis()->SetTitleSize(0);
  hFrame->GetXaxis()->SetLabelSize(0);
  hFrame->GetYaxis()->SetTitleFont(43);
  hFrame->GetYaxis()->SetTitleSize(27);
  hFrame->GetYaxis()->SetTitleOffset(1.3);
  

  // signal
  hh->Scale(br*br);
  hw->Scale(2*br*(1.0-br));
  TH1* signal = (TH1*)hh->Clone();
  signal->Add(hw);

  ci = TColor::GetColor("#ff3399");
  signal->SetLineColor(ci);
  signal->SetLineStyle(2);
  signal->SetLineWidth(2);

  // Fakes
  TH1* fakes = (TH1*)(fakett->Clone());
  fakes->Add(fakeW);
  fakes->Add(faket);

  // stacked backgrounds
  THStack *exp = new THStack();
  exp->SetName("exp");
  exp->SetTitle("exp");
  exp->Add(fakes);
  exp->Add(ewktau);
  exp->Add(qcd);
  exp->Add(signal);
  
  TH1* hExpBkg = (TH1*)fakes->Clone();
  hExpBkg->Add(ewktau);
  hExpBkg->Add(qcd);
  
  // uncertainty
  TH1* uncert = (TH1*)fakeW->Clone();
  uncert->Add(fakett);
  uncert->Add(ewktau);
  uncert->Add(qcd);
  uncert->SetFillColor(1);
  uncert->SetFillStyle(3344);
  uncert->SetLineColor(0);
  uncert->SetLineStyle(0);
  uncert->SetLineWidth(0);

  TH1* hExpBkgTotalUncert = (TH1*)uncert->Clone();
  hExpBkgTotalUncert->SetFillStyle(3354);

  TH1* hAgreement = (TH1*)data->Clone();
  hAgreement->Divide(hExpBkg);
  TGraphErrors* hAgreementRelUncert = new TGraphErrors(hAgreement->GetNbinsX());
  hAgreementRelUncert->SetLineWidth(2);
  hAgreementRelUncert->SetLineColor(kBlack);
  for (int i = 1; i <= hFrame->GetNbinsX(); ++i) {
    double myQCDTotalUncert = TMath::Power(qcd->GetBinError(i), 2)
      + TMath::Power(qcd->GetBinContent(i)*myQCDRelUncert, 2);
    double myEWKTotalUncert = TMath::Power(ewktau->GetBinError(i), 2)
      + TMath::Power(ewktau->GetBinContent(i)*myEWKRelUncert, 2);
    double myFakesTotalUncert = TMath::Power(fakes->GetBinError(i), 2)
      + TMath::Power(fakes->GetBinContent(i)*myFakesRelUncert, 2);
    hExpBkgTotalUncert->SetBinError(i, TMath::Sqrt(myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert));

    if (hExpBkg->GetBinContent(i) > 0) {
      hAgreementRelUncert->SetPoint(i-1, hExpBkg->GetBinCenter(i), data->GetBinContent(i) / hExpBkg->GetBinContent(i));
      double myUncertData = 0;
      if (data->GetBinContent(i) > 0)
        myUncertData = TMath::Power(data->GetBinError(i) / data->GetBinContent(i), 2);
      double myUncertBkg = (myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert) / TMath::Power(hExpBkg->GetBinContent(i), 2);
      hAgreementRelUncert->SetPointError(i-1, 0,  data->GetBinContent(i) / hExpBkg->GetBinContent(i) * TMath::Sqrt(myUncertData + myUncertBkg));
    } else {
      hAgreementRelUncert->SetPoint(i-1, hExpBkg->GetBinCenter(i), 0);
      hAgreementRelUncert->SetPointError(i-1, 0, 0);
    }
    if (debug) {
      cout << "Point: " << hAgreementRelUncert->GetX()[i-1]-10 << "-" << hAgreementRelUncert->GetX()[i-1]+10
          << " GeV/c2, agreement: " << hAgreementRelUncert->GetY()[i-1] << ", uncert: " << hAgreement->GetBinError(i) << ", " << hAgreementRelUncert->GetErrorY(i-1) << endl;
      cout << "  bkg. stat. uncert. " << hExpBkg->GetBinError(i) << " (i.e. " << hExpBkg->GetBinError(i) / hExpBkg->GetBinContent(i) * 100.0 << " %)"
          << ", stat+syst uncert. " << TMath::Sqrt(myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert) 
          << " (i.e. " << TMath::Sqrt(myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert) / hExpBkg->GetBinContent(i) * 100.0 << " %)" << endl;
    }
  }

  // Agreement pad
  TPad* pad = new TPad("ratiopad","ratiopad",0.,0.,1.,.3);
  pad->Draw();
  pad->cd();
  pad->Range(0,0,1,1);
  pad->SetFillColor(0);
  pad->SetFillStyle(4000);
  pad->SetBorderMode(0);
  pad->SetBorderSize(2);
  pad->SetTickx(1);
  pad->SetTicky(1);
  pad->SetLeftMargin(0.16);
  pad->SetRightMargin(0.05);
  pad->SetTopMargin(0);
  pad->SetBottomMargin(0.34);
  pad->SetFrameFillStyle(0);
  pad->SetFrameBorderMode(0);
  // Plot here ratio
  if (1.0-delta > 0)
    hAgreement->SetMinimum(1.0-delta);
  else
    hAgreement->SetMinimum(0.);
  hAgreement->SetMaximum(1.0+delta);
  hAgreement->GetXaxis()->SetLabelOffset(0.007);
  hAgreement->GetXaxis()->SetLabelFont(43);
  hAgreement->GetXaxis()->SetLabelSize(27);
  hAgreement->GetYaxis()->SetLabelFont(43);
  hAgreement->GetYaxis()->SetLabelSize(27);
  hAgreement->GetYaxis()->SetLabelOffset(0.007);
  hAgreement->GetYaxis()->SetNdivisions(505);
  hAgreement->GetXaxis()->SetTitleFont(43);
  hAgreement->GetYaxis()->SetTitleFont(43);
  hAgreement->GetXaxis()->SetTitleSize(33);
  hAgreement->GetYaxis()->SetTitleSize(33);
  hAgreement->SetTitleSize(27, "xyz");
  hAgreement->GetXaxis()->SetTitleOffset(3.2);
  hAgreement->GetYaxis()->SetTitleOffset(1.3);
  hAgreement->SetXTitle(hFrame->GetXaxis()->GetTitle());
  hAgreement->SetYTitle("Data/#Sigmabkg");
  hAgreement->Draw("e2");
  // Plot line at zero
  TH1* hAgreementLine = dynamic_cast<TH1*>(hAgreement->Clone());
  for (int i = 1; i <= hAgreementLine->GetNbinsX(); ++i) {
    hAgreementLine->SetBinContent(i,1.0);
    hAgreementLine->SetBinError(i,0.0);
  }
  hAgreementLine->SetLineColor(kRed);
  hAgreementLine->SetLineWidth(2);
  hAgreementLine->SetLineStyle(3);
  hAgreementLine->Draw("hist same");
  hAgreement->Draw("same");
  hAgreementRelUncert->Draw("[]");
  pad->RedrawAxis();

  myCanvas->cd();
  
  TPad* plotpad = new TPad("plotpad", "plotpad",0,0.3,1.,1.);
  plotpad->Draw();
  plotpad->cd();
  plotpad->Range(0,0,1,1);
  plotpad->SetFillColor(0);
  plotpad->SetFillStyle(4000);
  plotpad->SetBorderMode(0);
  plotpad->SetBorderSize(2);
  //if (logy)
  //  plotpad->SetLogy();
  plotpad->SetTickx(1);
  plotpad->SetTicky(1);
  plotpad->SetLeftMargin(0.16);
  plotpad->SetRightMargin(0.05);
  plotpad->SetTopMargin(0.065);
  plotpad->SetBottomMargin(0.0);
  plotpad->SetFrameFillStyle(0);
  plotpad->SetFrameBorderMode(0);
  
  hFrame->GetXaxis()->SetTitleSize(0);
  hFrame->GetXaxis()->SetLabelSize(0);
  hFrame->GetYaxis()->SetTitleFont(43);
  hFrame->GetYaxis()->SetTitleSize(33);
  hFrame->GetYaxis()->SetTitleOffset(1.3);
  
  // Draw objects
  hFrame->Draw();
  exp->Draw("hist same");
  uncert->Draw("E2 same");
  hExpBkgTotalUncert->Draw("E2 same");
  // Data
  data->Draw("same");
  
  //signal->Draw("same");
  TLegend *leg = new TLegend(0.53,0.6,0.87,0.91,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(63);
  leg->SetTextSize(18);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(kWhite);
  //leg->SetFillStyle(4000); // enabling this will cause the plot to be erased from the pad
  TLegendEntry* entry = leg->AddEntry(data, "Data", "P");
  s.str("");
  s << "with H^{#pm}#rightarrow#tau^{#pm}#nu";
  entry = leg->AddEntry(signal, s.str().c_str(), "L");
  entry = leg->AddEntry(qcd, "QCD (meas.)", "F");
  entry = leg->AddEntry(ewktau, "EWK genuine #tau (meas.)", "F");
  entry = leg->AddEntry(fakes, "EWK fake #tau (MC)", "F");
  entry = leg->AddEntry(uncert, "stat. uncert.", "F");
  entry = leg->AddEntry(hExpBkgTotalUncert, "stat. #oplus syst. uncert.", "F");
  leg->Draw();
  
  string myTitle = "CMS Preliminary";
  if (paperStatus)
    myTitle = "CMS";

  TLatex *tex = new TLatex(0.62,0.945,myTitle.c_str());
  tex->SetNDC();
  tex->SetTextFont(43);
  tex->SetTextSize(27);
  tex->SetLineWidth(2);
  tex->Draw();
  tex = new TLatex(0.2,0.945,"#sqrt{s} = 7 TeV");
  tex->SetNDC();
  tex->SetTextFont(43);
  tex->SetTextSize(27);
  tex->SetLineWidth(2);
  tex->Draw();
  tex = new TLatex(0.43,0.945,"2.3 fb^{-1}");
  tex->SetNDC();
  tex->SetTextFont(43);
  tex->SetTextSize(27);
  tex->SetLineWidth(2);
  tex->Draw();

  s.str("");
  if(paperStatus)
    s << "m_{H^{#pm}} = " << mass << " GeV";
  else
    s << "m_{H^{#pm}} = " << mass << " GeV/c^{2}";
  tex = new TLatex(0.28,0.865,s.str().c_str());
  tex->SetNDC();
  tex->SetTextFont(63);
  tex->SetTextSize(20);
  tex->SetLineWidth(2);
  tex->Draw();
  s.str("");
  s << "BR(t#rightarrowbH^{#pm})=" << setprecision(2) << br;
  tex = new TLatex(0.28,0.805,s.str().c_str());
  tex->SetNDC();
  tex->SetTextFont(63);
  tex->SetTextSize(20);
  tex->SetLineWidth(2);
  tex->Draw();

  
  plotpad->RedrawAxis();
  plotpad->Modified();

  s.str("");
  s << "mT_datadriven_m" << mass << ".png";
  myCanvas->Print(s.str().c_str());
  s.str("");
  s << "mT_datadriven_m" << mass << ".C";
  myCanvas->Print(s.str().c_str());
  s.str("");
  s << "mT_datadriven_m" << mass << ".eps";
  myCanvas->Print(s.str().c_str());
   

}

void combineMt(){
  plot(80);
  plot(100);
  plot(120);
  plot(140);
  plot(150);
  plot(155);
  plot(160);
}
