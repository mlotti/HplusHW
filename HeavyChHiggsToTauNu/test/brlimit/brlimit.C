#include "TF1.h"

void plotTxtMh(double lumi, int mH); 
void plotTxt(double lumi);

int brlimit()
{
  gROOT->ProcessLine(".L tdrstyle_mod.C");
  setTDRStyle();

  tdrStyle->SetTitleFillColor(0);
  tdrStyle->SetTitleFontSize(0.05);
  tdrStyle->SetTitleX(0.3); // Set the position of the title box

  double L, Nwjets, Nttww, Nrest, sigma, ett; // rest contains dibosons, single top and Drell-Yan 
  ifstream fileLumi("input_luminosity",ios::in); fileLumi   >> L;
  ifstream fileNwjets("input_nwjets",ios::in);   fileNwjets >> Nwjets;
  ifstream fileNttww("input_nttww",ios::in);     fileNttww  >> Nttww;
  ifstream fileNrest("input_nrest",ios::in);     fileNrest  >> Nrest;
  ifstream fileSigma("input_sigma",ios::in);     fileSigma  >> sigma;
  ifstream fileEtt("input_ett",ios::in);         fileEtt    >> ett;

  // -- my data -- 
   const int nData = 6; // 90 not yet ready
   double mH[nData]   = 
     {100,     
      120,     
      140,         
      150,    
      155, 
      160};
   double e_HW[nData] = {
     0.001845,
     0.002301,
     0.002490,
     0.002788,
     0.003202,
     0.002619 };

  double e_HH[nData] =
    {
      0.003782,
      0.004135,
      0.003318,
      0.002129,
      0.001470,
      0.001123
    } ;
  
  char temp[200];
  double valueLandS_obs[nData];
  double valueLandS_exp[nData][5];
  cout << "----- reading values from LandS files -----" << endl;
  for (int i=0; i<nData; i++){
    sprintf(temp,"output_LandS_%d",mH[i]);
    cout << temp << endl;
    ifstream logFile(temp,ios::in);    
    if (!logFile) {
      cout << "No input file " << temp << endl;
      exit (-1) ;
    }
    logFile >> valueLandS_obs[i];
    cout << "Observed: " << valueLandS_obs[i] << endl;
    for (int j=0; j<5; j++) logFile >> valueLandS_exp[i][j];
    cout << "Expected ";
  for (int j=0; j<5; j++) 
    cout << valueLandS_exp[i][j] << "  ";
  cout << endl;
  }

  // Plot #events vs. Br
  // for mH = 120
  double solution;
  const int plot_this = 1; // 1 for mH=120
  double ehh =  e_HH[plot_this];
  double kappa=e_HW[plot_this]/ett-1;
  double Nbkg=Nwjets + Nttww + Nrest;//Nwjets + L*sigma*ett;
  double coef1=L*sigma*e_HW[plot_this]*2;
  //double coef1=L*sigma*ett*2*kappa;
  double coef2_hw=L*sigma*ett*(2*kappa+1); //remember that this should be negative
  double coef2_hwhh=-L*sigma*(e_HH[plot_this]-2*e_HW[plot_this]);//remember that this should be negative
  make_plot_simple(Nbkg,coef1,coef2_hwhh,coef2_hw,L,mH[plot_this]);
  make_plot_shaded(Nbkg,coef1,coef2_hwhh,coef2_hw, valueLandS_exp[plot_this],L,mH[plot_this]);

  // Plot Br limit plot
  //  cout << "--- BR limits --- " << endl; 
  double BR_95_obs[nData],BR_95_exp[nData], BR_95_exp_p1[nData], BR_95_exp_m1[nData], BR_95_exp_p2[nData], BR_95_exp_m2[nData];
  for (int i=0; i<nData; i++){ 
    coef1=L*sigma*e_HW[i]*2;
    coef2_hwhh=-L*sigma*(e_HH[i]-2*e_HW[i]);
    double ev_obs = valueLandS_obs[i]    + Nbkg;
    double ev_exp = valueLandS_exp[i][2] + Nbkg;
    double ev_exp_p1 = valueLandS_exp[i][2+1] + Nbkg;
    double ev_exp_m1 = valueLandS_exp[i][2-1] + Nbkg;
    double ev_exp_p2 = valueLandS_exp[i][2+2] + Nbkg;
    double ev_exp_m2 = valueLandS_exp[i][2-2] + Nbkg;
    BR_95_obs[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_obs);
    BR_95_exp[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_exp);
    BR_95_exp_p1[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_exp_p1);
    BR_95_exp_m1[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_exp_m1);
    BR_95_exp_p2[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_exp_p2);
    BR_95_exp_m2[i] = calculate_BR(Nbkg,coef1,coef2_hwhh,ev_exp_m2);
    //    cout << "calc " << BR_95_exp_p1[i] << "  " << BR_95_exp_m1[i] << endl;
    // cout<< "limit is " <<  calculate_BR(Nbkg,coef1,coef2_hwhh,10) << endl;
    //    cout<< "mH = " <<  mH[i] << "   BR95 = " << BR_95_obs[i] << endl;
  }
  TCanvas * can_br = new TCanvas();
  can_br->SetTitle("95\% CL limit for BR");
  TGraph * tg_obs = new TGraph(nData, mH, BR_95_obs);

  tg_obs->SetTitle("95\% CL limit for BR");
  //  tg_obs->SetLineWidth(2505);
  tg_obs->SetMarkerStyle(20);
  tg_obs->SetFillStyle(3005);
  tg_obs->SetMarkerSize(1.4);
  tg_obs->SetLineWidth(3);
  tg_obs->Draw("LPA");
//   TGraph * tg_obs_shade = new TGraph(nData, mH, BR_95_obs);
//   tg_obs_shade->SetLineWidth(2000);
//   tg_obs_shade->SetFillStyle(3005);
//   tg_obs_shade->Draw("F same");
  tg_obs->GetYaxis()->SetRangeUser(0,1.0); 
  tg_obs->GetYaxis()->SetTitle("95\% CL limit for Br(t#rightarrow bH^{#pm})");
  tg_obs->GetXaxis()->SetTitle("m_{H^{+}} (GeV/c^{2})");
  TGraph * tg_exp = new TGraph(nData, mH, BR_95_exp);
  // tg_exp->SetLineStyle(2);
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
    myx[i]           = mH[i];
    myx[nData+i] = mH[nData-1-i];
    //   cout << myx[i] << "  " << BR_95_exp_contour[i] << endl;
  }
  TGraph * tg_exp_cont1 = new TGraph(2*nData, myx, BR_95_exp_contour1);
  TGraph * tg_exp_cont2 = new TGraph(2*nData, myx, BR_95_exp_contour2);
  tg_exp_cont1->SetFillColor(5);
  tg_exp_cont2->SetFillColor(kOrange);
  tg_exp_cont2->Draw("F");
  tg_exp_cont1->Draw("F");
  //   for (int i=0 ; i<nData; i++)
  //     cout << myx[i] << "  " << BR_95_exp_contour2[i] 
  // 	 << "  " << BR_95_exp_contour1[i] 
  // 	 << "  " << BR_95_exp_contour1[nData+i] 
  // 	 << "  " << BR_95_exp_contour2[nData+i] 
  // 	 << endl;

  TLegend *pl = new TLegend(0.5,0.70,0.8,0.92);
  pl->SetTextSize(0.03);
  pl->SetFillStyle(4000);
  pl->SetTextFont(132);
  pl->SetBorderSize(0);
  TLegendEntry *ple;
  ple = pl->AddEntry(tg_obs, "Observed", "lp");
  ple = pl->AddEntry(tg_exp, "Expected", "lp");
  char temp[200];
  sprintf(temp,"Expected #pm1 #sigma");
  ple = pl->AddEntry(tg_exp_cont1, temp, "f");
  sprintf(temp,"Expected #pm2 #sigma");
  ple = pl->AddEntry(tg_exp_cont2, temp, "f");
  //  ple->SetMarkerSize(0.1);
  pl->Draw();

  // Redraw lines on top of filled area
  tg_obs->Draw("LP same");
  tg_exp->Draw("LP same");

  // Plot LIP results, obs(black) 
  // from approval of 10.3.2011
  if (1) {
    double xLip[] = {80,100,120,140,  150,  155,160};
    double yLipObs[] = {.25 , .23 , .24 , .27, .327, .385, .53};
    double yLipExp[] = {.255, .235, .245, .28, .34 , .405, .58};
    TGraph * tgLIPObs = new TGraph(7,xLip,yLipObs);
    TGraph * tgLIPExp = new TGraph(7,xLip,yLipExp);
    tgLIPObs->SetLineWidth(1);
    tgLIPObs->SetLineStyle(3);
    tgLIPObs->SetMarkerStyle(22);
    tgLIPObs->SetMarkerSize(1.1);
    //    tgLIPObs->SetFillStyle(3005);
    tgLIPExp->SetLineWidth(1);
    tgLIPExp->SetLineColor(2);
    tgLIPExp->SetLineStyle(3);
    tgLIPExp->SetMarkerColor(2);
    tgLIPExp->SetMarkerStyle(23);
    tgLIPExp->SetMarkerSize(1.1);
    tgLIPObs->Draw("LP");
    tgLIPExp->Draw("LP");
    ple = pl->AddEntry(tgLIPObs, "hadr.#tau+e/#mu channel, observed", "lp");
    ple = pl->AddEntry(tgLIPExp, "hadr.#tau+e/#mu channel, expected", "lp");
  }

  // Plot Tevatron results
  if (1) {
    TGraph * tevaGraph;

    //    Double_t tevax[] = {  90,  110,  130,  150};
    //    Double_t tevay[] = {  0.15,  0.15, 0.17,0.19};

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
    ple = pl->AddEntry(tgObsTeva, "D0 1.0 fb^{-1} observed, approximate", "lp");
  }

  plotTxt(L);

  // Save TGraphs and plots
  TFile myfi("brlimits.root","recreate");
  tg_obs->SetName("tg_obs"); tg_obs->Write();
  tg_exp->SetName("tg_exp"); tg_exp->Write();
  tg_exp_cont1->SetName("tg_exp_cont1"); tg_exp_cont1->Write();
  tg_exp_cont2->SetName("tg_exp_cont2"); tg_exp_cont2->Write();
  myfi.Close();
  can_br->SaveAs("brlimits.eps");
  can_br->SaveAs("brlimits.png");
  
  return 0;
}

double make_plot_simple(double bkg, 
			double coef1, 
			double coef2_hwhh, 
			double coef2_hw, 
			int L, 
			int mH)
{
  char temp[500];
  const double c = bkg;

  TCanvas * can = new TCanvas();

  // print formula and draw function
  sprintf(temp,"%.2f+%.2f*x-%.2f*x^2",c,coef1,coef2_hwhh);//coef2_hwhh is negative
  TF1 * fu = new TF1("function",temp,0,1);
  fu->GetXaxis()->SetTitle("Br(t->bH+)");
  fu->GetYaxis()->SetTitle("Number of expected events");
  fu->SetLineColor(1);
  fu->SetLineWidth(3);
  fu->Draw();

  // draw hw line
  sprintf(temp,"%.2f+%.2f*x-%.2f*x^2",c,coef1,coef2_hw);//coef2_hwhh is negative
  TF1 * fuhw = new TF1("functionhw",temp,0,1);
  fuhw->SetLineStyle(2);
  fuhw->SetLineColor(1);
  fuhw->SetLineWidth(3);
  fuhw->Draw("same");

  plotTxt(L);

  can->SaveAs("Nevents.eps");
  can->SaveAs("Nevents.png");

  return 0;
}

double make_plot_shaded(double c, 
			double coef1, 
			double coef2_hwhh, 
			double coef2_hw, 
			double lands[],
			int L, 
			int mH)
{
  char temp[500];

  double Nlimit = lands[2];
  double Nlimitminus = lands[1];
  double Nlimitplus = lands[3];

  // print formula and draw function
  sprintf(temp,"%.2f+%.2f*x-%.2f*x^2",c,coef1,coef2_hwhh);//coef2_hwhh is negative
  cout << endl << "Equation is: " << temp << endl;
  TF1 * fu = new TF1("function",temp,0,0.35);
  fu->GetXaxis()->SetTitle("Br(t->bH+)");
  fu->GetYaxis()->SetTitle("Number of expected events");
  TCanvas * can = new TCanvas();
  fu->SetLineColor(1);
  fu->SetLineWidth(3);
  fu->Draw();

  // calculate solution (lower value) and its 1 sigma errors
  double solution = (-coef1 +sqrt(coef1*coef1 - 4*(-coef2_hwhh)*(c-Nlimit)))/(2*(-coef2_hwhh));//coef2_hwhh is negative
  double solutionplus = (-coef1 +sqrt(coef1*coef1 - 4*(-coef2_hwhh)*(c-Nlimitplus)))/(2*(-coef2_hwhh));//coef2_hwhh is negative
  double solutionminus = (-coef1 +sqrt(coef1*coef1 - 4*(-coef2_hwhh)*(c-Nlimitminus)))/(2*(-coef2_hwhh));//coef2_hwhh is negative
  cout << "sol " << solution << " min " << solutionminus << " plus  " << solutionplus <<  endl;
  double solution_hw = (-coef1 +sqrt(coef1*coef1 - 4*(-coef2_hw)*(c-Nlimit)))/(2*(-coef2_hw));//coef2_hwhh is negative
  cout << "Obtained Nlimit is " << solution << ", only considering HW events would give " << solution_hw << endl;

  // Draw yellow area
  double areaY[] = {Nlimitminus,  Nlimitminus,          0.001,         0.001,  Nlimitplus,Nlimitplus };
  double areaX[] = {        0.001,solutionminus,solutionminus,solutionplus,solutionplus,       0.001 };
  TGraph * area = new TGraph(6,areaX,areaY);
  area->SetFillColor(5);
  area->SetFillStyle(3001);
  area->Draw("F");
  fu->Draw("same"); // redraw

  // draw lines
  Double_t x1[2],y1[2];
  x1[0]=0.01;x1[1]=solution;
  y1[0]=Nlimit;y1[1]=Nlimit;
  TGraph * lineEvts = new TGraph(2,x1,y1);
  //lineEvts->SetLineWidth(1504);
  lineEvts->SetLineWidth(7);
  lineEvts->SetLineStyle(2);
  lineEvts->SetFillStyle(3005);
  lineEvts->Draw();

  x1[0]=solution;x1[1]=solution;
  y1[0]=0.01;y1[1]=fu(1.0); if (fu(0.5)>y1[1]) y1[1]=fu(0.5);
  TGraph * lineBr = new TGraph(2,x1,y1);
  //t1.Draw();
  lineBr->SetLineWidth(-16004);
  lineBr->SetLineColor(2);
  lineBr->SetLineStyle(2);
  lineBr->SetFillStyle(3004);
  lineBr->Draw();
  x1[0]=solutionminus;x1[1]=solutionminus;
  y1[0]=0.01;y1[1]=fu(solutionminus);

  TLatex text;
  //  text.SetNDC();
  text.SetTextSize(0.04);
  text.DrawLatex(solution+0.01,2.5,"Excluded");
  text.DrawLatex(solution+0.01,2,"Vr values");
  text.DrawLatex(solution-0.11,Nlimit-0.8,"N_{95\%}^{expected}");

  plotTxtMh(L,mH);

  can->SaveAs("Nevents_zoom.eps");
  can->SaveAs("Nevents_zoom.png");

  ofstream fileNsig("output_root_Nsig",ios::out); fileNsig<<Nlimit-c;
  ofstream fileNlimit("output_root_Nlimit",ios::out); fileNlimit<<Nlimit;
  ofstream fileSolution("output_root_N95",ios::out); fileSolution<<solution;
  ofstream fileSolutionp("output_root_N95plus",ios::out); fileSolutionp<<solutionplus-solution;
  ofstream fileSolutionm("output_root_N95minus",ios::out); fileSolutionm<<solution-solutionminus;

  return solution;
}


double calculate_BR(double c1, double coef1, double coef2_hwhh, double events)
{
  // return BR = 100% if cannot find answer
  double temp = coef1*coef1 - 4*(-coef2_hwhh)*(c1-events);
  if (temp<0) return 1.0;
  double BR = (-coef1 +sqrt( temp ))/(2*(-coef2_hwhh));

  return BR;
}


void plotTxt(double lumi) {
  Double_t linePos       = 0.9;
  Double_t lineSpace = 0.038;
  Double_t left      = 0.185;
  TLatex text;
  text.SetTextAlign(12);
  text.SetTextSize(0.04);
  text.SetNDC();
  //  text.DrawLatex(left,0.9,"CMS preliminary");

  text.SetTextSize(0.03);
  text.DrawLatex(left,linePos,"t#rightarrowH^{#pm}b, H^{#pm}#rightarrow#tau#nu");
  text.DrawLatex(left,linePos -= lineSpace,"Fully hadronic final state");
  char temp[300];
  //  sprintf(temp,"#sqrt{s}=7 TeV, %.0d pb^{-1}",lumi);
  //  text.DrawLatex(left,linePos -= lineSpace,temp);
  text.DrawLatex(left,linePos -= lineSpace,"Bayesian CL limit");
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
