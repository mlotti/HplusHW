#include "TF1.h"

void plotTxtMh(double lumi, int mH); 
void plotTxt(double lumi);
void readValuesFromLandsFile(char * temp, double &my_obs,double * my_exp);

int brlimit()
{
  gROOT->ProcessLine(".L tdrstyle_mod.cxx");
  setTDRStyle();

  tdrStyle->SetTitleFillColor(0);
  tdrStyle->SetTitleFontSize(0.05);
  tdrStyle->SetTitleX(0.3); // Set the position of the title box

  // --- Read initial values from input files ---
  // "rest" contains dibosons, single top and Drell-Yan 
  double L;
  ifstream fileLumi(  "input_luminosity",ios::in); fileLumi   >> L;

  // --- Data: mass points and efficiencies  --- 
   const int nData = 7; // 90 not yet ready
   double mH[nData]   = 
     {80,
      100,     
      120,     
      140,         
      150,    
      155, 
      160};

  // --- Read values from LandS files ---
  // obs, exp, exp+-1sigma, exp+-2sigma
  char temp[200];
  double valueLandS_obs[nData];
  double valueLandS_exp[nData][5];
  cout << "----- reading values from LandS files -----" << endl;
  for (int i=0; i<nData; i++){
    sprintf(temp,"output_LandS_HPlusHadronic_%d",mH[i]);
    readValuesFromLandsFile(temp,valueLandS_obs[i],valueLandS_exp[i]);
  }

  // --- Plot #events vs. Br ---
  // for mH = 120
  const int plot_this = 1; // makes plots for illustration, 1 for mH=120 
  // --- Plot Br 95% CL limit plot ---
  double BR_95_obs[nData],BR_95_exp[nData], BR_95_exp_p1[nData], BR_95_exp_m1[nData], BR_95_exp_p2[nData], BR_95_exp_m2[nData];
  for (int i=0; i<nData; i++){ 
    BR_95_obs[i] = valueLandS_obs[i]    ;
    BR_95_exp[i] =  valueLandS_exp[i][2] ;
    BR_95_exp_p1[i] = valueLandS_exp[i][2+1] ;
    BR_95_exp_m1[i] = valueLandS_exp[i][2-1] ;
    BR_95_exp_p2[i] = valueLandS_exp[i][2+2] ;
    BR_95_exp_m2[i] = valueLandS_exp[i][2-2] ;
  }
  TCanvas * can_br = new TCanvas();
  can_br->SetTitle("95\% CL limit for BR");
  TGraph * tg_obs = new TGraph(nData, mH, BR_95_obs);
  tg_obs->SetTitle("95\% CL limit for BR");
  tg_obs->SetMarkerStyle(20);
  tg_obs->SetFillStyle(3005);
  tg_obs->SetMarkerSize(1.4);
  tg_obs->SetLineWidth(3);
  tg_obs->Draw("LPA");
  tg_obs->GetYaxis()->SetRangeUser(0,0.4);
  tg_obs->GetYaxis()->SetTitle("95\% CL limit for Br(t#rightarrow bH^{#pm})");
  tg_obs->GetXaxis()->SetTitle("m_{H^{+}} (GeV/c^{2})");
  TGraph * tg_exp = new TGraph(nData, mH, BR_95_exp);
  tg_exp->SetLineColor(2);
  tg_exp->SetMarkerColor(2);
  tg_exp->SetMarkerStyle(21);
  tg_exp->SetMarkerSize(1.4);
  tg_exp->SetLineWidth(3);
  tg_exp->SetLineStyle(2);
  tg_exp->Draw("LP");
  double BR_95_exp_contour1[2*nData], BR_95_exp_contour2[2*nData], myx[2*nData];
  for (int i=0; i<nData; i++){
    BR_95_exp_contour1[i]       = BR_95_exp_m1[i];
    BR_95_exp_contour1[nData+i] = BR_95_exp_p1[nData-1-i];
    BR_95_exp_contour2[i]       = BR_95_exp_m2[i];
    BR_95_exp_contour2[nData+i] = BR_95_exp_p2[nData-1-i];
    myx[i]       = mH[i];
    myx[nData+i] = mH[nData-1-i];
  }
  TGraph * tg_exp_cont1 = new TGraph(2*nData, myx, BR_95_exp_contour1);
  TGraph * tg_exp_cont2 = new TGraph(2*nData, myx, BR_95_exp_contour2);
  tg_exp_cont1->SetFillColor(5);
  tg_exp_cont2->SetFillColor(kOrange);
  tg_exp_cont2->Draw("F");
  tg_exp_cont1->Draw("F");

  TLegend *pl = new TLegend(0.5,0.70,0.8,0.92);
  pl->SetTextSize(0.03);
  pl->SetFillStyle(4000);
  pl->SetTextFont(132);
  pl->SetBorderSize(0);
  TLegendEntry *ple;
  ple = pl->AddEntry(tg_obs, "Observed", "lp");
  ple = pl->AddEntry(tg_exp, "Expected median", "lp");
  char temp[200];
  sprintf(temp,"Expected median #pm1 #sigma");
  ple = pl->AddEntry(tg_exp_cont1, temp, "f");
  sprintf(temp,"Expected median #pm2 #sigma");
  ple = pl->AddEntry(tg_exp_cont2, temp, "f");
  pl->Draw();
  // Redraw lines on top of filled area
  tg_obs->Draw("LP same");
  tg_exp->Draw("LP same");

  plotTxt(L);

  // --- Plot LIP and Tevatron results, obs(black) ---
  if (0) plotLipResults(pl);
  if (0) plotTevatronResults(pl);

  // Save TGraphs and plots
  TFile myfi("brlimits.root","recreate");
  tg_obs->SetName("tg_obs"); tg_obs->Write();
  tg_exp->SetName("tg_exp"); tg_exp->Write();
  tg_exp_cont1->SetName("tg_exp_cont1"); tg_exp_cont1->Write();
  tg_exp_cont2->SetName("tg_exp_cont2"); tg_exp_cont2->Write();
  myfi.Close();
  can_br->SaveAs("brlimits.eps");
  can_br->SaveAs("brlimits.png");
  can_br->SaveAs("brlimits.C");
  
  return 0;
}


void plotTevatronResults(TLegend * pl){
    TGraph * tevaGraph;

    // Results fom arxiv:0908.181v2, table II, tauonic observed values
    Double_t tevax[] =    {  80, 100, 120, 140, 150, 160};
    Double_t tevayObs[] = { .16, .15, .17, .18, .19, .18}; 

    tgObsTeva = new TGraph(6,tevax,tevayObs);
    tgObsTeva->SetLineColor(kBlue);
    tgObsTeva->SetLineStyle(2);
    tgObsTeva->SetLineWidth(1);
    tgObsTeva->SetMarkerColor(kBlue);
    tgObsTeva->SetMarkerSize(1.0);
    tgObsTeva->Draw("LP");
    pl->AddEntry(tgObsTeva, "D0 1.0 fb^{-1} observed, approximate", "lp");
  return;
}


void plotLipResults(TLegend * pl){
  // from approval of 10.3.2011
  double xLip[] = {80,100,120,140,  150,  155,160};
  double yLipObs[] = {.25 , .23 , .24 , .27, .327, .385, .53};
  double yLipExp[] = {.255, .235, .245, .28, .34 , .405, .58};
  TGraph * tgLIPObs = new TGraph(7,xLip,yLipObs);
  TGraph * tgLIPExp = new TGraph(7,xLip,yLipExp);
  tgLIPObs->SetLineWidth(1);
  tgLIPObs->SetLineStyle(3);
  tgLIPObs->SetMarkerStyle(22);
  tgLIPObs->SetMarkerSize(1.1);
  tgLIPExp->SetLineWidth(1);
  tgLIPExp->SetLineColor(2);
  tgLIPExp->SetLineStyle(3);
  tgLIPExp->SetMarkerColor(2);
  tgLIPExp->SetMarkerStyle(23);
  tgLIPExp->SetMarkerSize(1.1);
  tgLIPObs->Draw("LP");
  tgLIPExp->Draw("LP");
  pl->AddEntry(tgLIPObs, "hadr.#tau+e/#mu channel, observed", "lp");
  pl->AddEntry(tgLIPExp, "hadr.#tau+e/#mu channel, expected", "lp");
  return;
}


void readValuesFromLandsFile(char * fileName, double &my_obs,double * my_exp)
{
  cout << fileName << endl;
  ifstream logFile(fileName,ios::in);    
  if (!logFile) {
    cout << "No LandS input file " << fileName << endl;
    exit (-1) ;
  }
  logFile >> my_obs;
  cout << "Observed: " << my_obs << endl;
  for (int j=0; j<5; j++) logFile >> my_exp[j];
  cout << "Expected ";
  for (int j=0; j<5; j++) {
    cout << my_exp[j] << "  ";
  }
  cout << endl;
  return;
}


void plotTxt(double lumi) {
  Double_t linePos       = 0.9;
  Double_t lineSpace = 0.038;
  Double_t left      = 0.185;
  TLatex text;
  text.SetTextAlign(12);
  text.SetNDC();
  text.SetTextSize(0.03);
  text.DrawLatex(left,linePos,"t#rightarrowH^{#pm}b, H^{#pm}#rightarrow#tau#nu");
  text.DrawLatex(left,linePos -= lineSpace,"Fully hadronic final state");
  char temp[300];
  //  sprintf(temp,"#sqrt{s}=7 TeV, %.0d pb^{-1}",lumi);
  //  text.DrawLatex(left,linePos -= lineSpace,temp);
  //  text.DrawLatex(left,linePos -= lineSpace,"Bayesian CL limit");
  text.DrawLatex(left,linePos -= lineSpace,"Br(H^{#pm}#rightarrow#tau^{#pm} #nu) = 1");

  // Style copied from python/tools/histograms.py
  double x = 0.62; double y= 0.96;
  TLatex l;
  l.SetNDC();
  l.SetTextFont(l.GetTextFont()-20); //# bold -> normal;
  l.DrawLatex(x,y,"CMS Preliminary");

  x = 0.45;
  sprintf(temp,"%.0f pb^{-1}",lumi);
  l.DrawLatex(x, y, temp);

  x = 0.2;
  l.DrawLatex(x, y, "#sqrt{s} = 7 TeV");

  return;
}


void plotTxtMh(double lumi, int mH) {
  Double_t top       = 0.85;
  Double_t lineSpace = 0.038;
  Double_t left      = 0.185;
  TLatex text;
  text.SetTextAlign(12);
  text.SetTextSize(0.04);
  text.SetNDC();
  text.DrawLatex(left,0.9,"CMS preliminary");

  text.SetTextSize(0.03);
  text.DrawLatex(left,top,"t#rightarrowH^{#pm}b, H^{#pm}#rightarrow#tau#nu");
  text.DrawLatex(left,top -  lineSpace,"Fully hadronic final state");
  char temp[300];
  sprintf(temp,"#sqrt{s}=7 TeV, %.0d pb^{-1}",lumi);
  text.DrawLatex(left,top -2*lineSpace,temp);
  text.DrawLatex(left,top -3*lineSpace,"Bayesian CL limit");
  text.DrawLatex(left,top -4*lineSpace,"Br(H^{#pm}#rightarrow#tau^{#pm} #nu) = 1");
  sprintf(temp,"M_{H}=%i",mH);
  text.DrawLatex(left,top -5*lineSpace,temp);

  return;
}
