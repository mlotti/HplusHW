#include "TF1.h"
#include "Math/WrappedTF1.h"
//#include "Math/RootFinderAlgorithms.h"

// Create files "hplus_m.root" for mass points
// m=100,120,... containing mt distributions (shapes)
// for all processes of the data card

// This script reads the following files :
//   mt_ewk_lands.root
//   mt_lands_ritva3.root
//   mt_matti.root
//   fromAlexandros.root

int generateLandsRootFiles()
{
  makePlots(100);  
  makePlots(120);
  makePlots(160);

  return 0;
}


int makePlots(float mass)
{
  const int makeGraphs = 0;
  double rate_data = 104;   // ritva

  double rate_hh;
  double rate_hw;
  double rate_qcd  = 7.5;   // alexandros  
  double rate_ewk  = 71.2;  // matti

  // Check that these numbers correspond to 
  // the rates in the datacard
  if (mass==120) {
    rate_hh   = 608.872; // ritva
    rate_hw   = 303.188; // ritva
  }
  else if (mass==100) {
    rate_hh = 568.476;
    rate_hw   = 208.439;
  }
  else if (mass==160) {
    rate_hh = 233.449 ;
    rate_hw = 441.343 ;
  }
  else {
    cout<< "Illegal data point!" << endl;
    exit(-1); 
  }

  char tmp[200]; 
  int rebin = 1;

  // EWK from Matti
  TFile *file1 = new TFile("mt_ewk_lands.root","read");
  TH1F *histo1 = (TH1F *) file1->Get("mt_ewk"); 

  // from Ritva
  TFile *file2 = new TFile("mt_lands_ritva3.root","read");
  TH1F *histo21 = (TH1F *) file2->Get("mt_data");

  // now HW and HH from Matti's new file
  TFile *fileMatti = new TFile("mt_matti.root","read");
  sprintf(tmp,"mt_hw_%.0f",mass);
  cout << "getting histo " << tmp << endl;
  TH1F *histo22 = (TH1F *) fileMatti->Get(tmp);  
  sprintf(tmp,"mt_hh_%.0f",mass);
  TH1F *histo23 = (TH1F *) fileMatti->Get(tmp);  

  // from Alexandros
  TFile *file3 = new TFile("fromAlexandros.root");
  TH1F * histo3 = (TH1F *) file3->Get("Data_met_AfterBigBox");

  // empty dummy histos
  TH1F * histoD1;
  TH1F * histoD2;
  histoD1 = new TH1F("T2_tt","T2_tt",40/rebin,0,400);
  histoD2 = new TH1F("res.","res.",40/rebin,0,400);

  histo1 ->Scale( rate_ewk /histo1->Integral()  );
  histo21->Scale( rate_data/histo21->Integral()  );
  histo22->Scale( rate_hw  /histo22->Integral()  );
  histo23->Scale( rate_hh  /histo23->Integral()  );
  histo3-> Scale( rate_qcd /histo3->Integral()  );

  histo1->Rebin( rebin );
  histo21->Rebin( rebin );
  histo22->Rebin( rebin );
  histo23->Rebin( rebin );
  histo3->Rebin( rebin );
  histoD1->Rebin( rebin );
  histoD2->Rebin( rebin );

  if (makeGraphs) {
    int bgColor = kBlue-9;
    int sigColor= kRed-9;
    TCanvas * tc = new TCanvas(); tc->Divide(3,2);
    int index=1;
    tc->cd(index++); histo1->Draw(); // black
    histo21->SetMarkerColor(kBlue);
    histo21->SetFillColor(kBlue);
    histo21->SetFillStyle(kBlue);
    tc->cd(index++);histo21->Draw();// blue
    tc->cd(index++);histo22->Draw();//red
    tc->cd(index++);histo23->Draw();//brown
    histo3->SetMarkerColor(kGreen);
    tc->cd(index++);histo3 ->Draw();//green
    histoD1->SetMarkerColor(kOrange);
    tc->cd(index++);histoD1 ->Draw();//orange
    tc->SaveAs("hplus_test.png");

    TH1F * sumBG =  new TH1F("sumBg","sumBg",40/rebin,0,400);
    TH1F * sumSig =  new TH1F("sumSig","sumSig",40/rebin,0,400);
    TH1F * sumData;
    TCanvas * tu = new TCanvas();
    sumBG->Add(histo1);
    sumBG->Add(histo3);
    // sumBG->SetMarkerColor(kBlue);
    // sumBG->SetFillColor(kBlue);
    sumBG->SetFillColor(bgColor);
    // sumBG->SetFillStyle(1001);
    // sumBG->SetMarkerStyle(2);
    // sumBG->Draw("hist");
    const double f=0.1;
    sumSig->Add(histo23,f*f);
    sumSig->Add(histo22,2.0*(1.0-f)*f);
    // sumSig->SetMarkerColor(kRed);
    sumSig->SetFillColor(sigColor);
    // sumSig->SetMarkerStyle(2);
    // sumSig->Draw("same");
    sumData =  (TH1F * ) histo21->Clone("sumData");
    sumData->SetMarkerColor(kBlack);
    // sumData->Draw("same");

    THStack * st = new THStack();
    st->Add(sumBG);
    st->Add(sumSig);
    st->Draw("histe");
    THStack * st2 = st->Clone();
    sumData->Draw("same");
    st2->Draw("same E");
   

    TLatex text;
    text.SetTextAlign(12);
    text.SetTextSize(0.04);
    text.SetNDC();
    // char tmpLabel[30];
    // sprintf(tmpLabel,"Peak at %.3f",
    //	 myhi->GetBinCenter(myhi->GetMaximumBin()));
    text.SetTextColor(bgColor);
    text.DrawLatex(0.4,0.85,"background (ewk+qcd)");
    text.SetTextColor(sigColor);
    text.DrawLatex(0.4,0.75,"bg + signal (HW+HH, br_{t#rightarrowH^{+}b}=0.1) ");
    text.SetTextColor(kBlack);
    text.DrawLatex(0.4,0.65,"data");

    tu->SaveAs("hplus_test_db.png");
  }

  histo1 ->SetName("Type1");
  histo21->SetName("data_obs");
  histo22->SetName("HW_1");
  histo23->SetName("HH_1");
  histo3 ->SetName("QCD");

  sprintf(tmp,"hplus_%.0f.root",mass);
  TFile * fileOut = new TFile(tmp,"recreate");
  histo1->Write();
  histo21->Write();
  histo22->Write();
  histo23->Write();
  histo3->Write();
  histoD1->Write();
  histoD2->Write();

  fileOut->Close();

  return 0;
}
