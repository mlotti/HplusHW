#include "TH1.h"
#include "TF1.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TMath.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TLine.h"
#include "TLegend.h"
#include "TCanvas.h"

void calculateAndPlotEventYields(Double_t b, 
				 Double_t NHBR100, 
				 Double_t NttNoH, 
				 const Int_t nPoints, 
				 Double_t dataXmax, 
				  Double_t rangeMin, 
				 Double_t rangeMax, 
				 Double_t HiggsMass,
				 Double_t &retCLlimit, Double_t &retCLstatlimit,
				 bool doPlots,
				 bool QCDuncertainty100);



int calcPoissonLowerCL(int lambda) {
  // make calculation quicker by reading precalculated 
  // poisson limits from a file
  static bool initialized=false;
  static bool dataExists=false;
  const int maxLambdaInFile = 100000; 
  static int maxLambdaSuccesfullyReadFromFile=0;
  static Double_t data[maxLambdaInFile];
  
  if (!initialized) {
    initialized = true;
    ifstream logFile("precalculatedPoissonValues.txt",ios::in); 
    if (logFile) {
      int dummy;
      while ( maxLambdaSuccesfullyReadFromFile<maxLambdaInFile && logFile >> dummy >> data[maxLambdaSuccesfullyReadFromFile] ){
	maxLambdaSuccesfullyReadFromFile++;
      }
      cout << "maxLambdaSuccesfullyReadFromFile " << maxLambdaSuccesfullyReadFromFile << endl;
      dataExists=true;
    }
    else {
      cout << "No file with precalculated Poisson values!" << endl;
      cout << "Run 'root makePoissonFile.C' to make running much quicker (takes tens of minutes)!" 
	   << endl;
    }
  }

  //  if (dataExists && lambda<maxLambdaInFile){
  if (dataExists && lambda<maxLambdaSuccesfullyReadFromFile){
    return data[lambda];
  }

  // This lambda is a new value, 
  // calculate and save it

  cout<< "-- file with precalculated values does not exist (consider generating this), calculating " << lambda << endl;

  Double_t integral(0);
  int index=0;
  integral =  TMath::Poisson(0,lambda);

  // go through bins until left-side probability (the bin
  // in question included) is 5% or larger
  // then return index-1
  while (1) {
    index++;
    integral += TMath::Poisson(index,lambda);

    if (integral==0.05) {
      index++;
      break;
    }

    if (integral>0.05) {
      index--;
      break;
    }
  }
  return index;
}


int calcStatError(int nEntries) {
  return TMath::CeilNint(nEntries/10.0);
}


void plotPreliminaryText(char * plotTitle, bool QCDuncertainty100) {
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
  sprintf(temp,"#sqrt{s}=7 TeV, %s", plotTitle);
  //  text.DrawLatex(left,top -2*lineSpace,"#sqrt{s}=7 TeV, hard cuts, 3 jets");
  text.DrawLatex(left,top -2*lineSpace,temp);
  
  if (QCDuncertainty100) {
    sprintf(temp,"100%% uncertainty in QCD MC (few events)");
    text.SetTextColor(kMagenta);
    text.DrawLatex(left + 0.20, top -3*lineSpace,temp);
  }
  
  return;
}


void plotLuminosityText(Double_t myLumi){
  Double_t top       = 0.85;
  Double_t lineSpace = 0.038;
  Double_t left      = 0.185;

  TLatex text;
  text.SetTextAlign(12);
  text.SetTextSize(0.03);
  text.SetNDC();
  char temp[200];
  sprintf(temp,"L = %.2f pb^{-1}",myLumi);
  text.DrawLatex(left,top -3*lineSpace,temp);
  return;
}


void plotHiggsMassText(Double_t HiggsMass){
  Double_t top       = 0.85;
  Double_t lineSpace = 0.038;
  Double_t left      = 0.185;

  char temp[200];
  TLatex text;
  text.SetTextAlign(12);
  text.SetNDC();
  text.SetTextSize(0.03);
  sprintf(temp,"m_{H^{#pm}} = %d GeV/c^{2}",HiggsMass);
  text.DrawLatex(left,top -4*lineSpace ,temp);
  return;
}


// x:BR, y:Nevents
void makePlotEventYields(int nPoints, 
			 Double_t * dataX,
			 Double_t * dataH,
			 Double_t * dataHH,
			 Double_t * dataW,
			 Double_t background,
			 Double_t HiggsMass,
			 char * plotTitle,
			 Double_t lumi,
			 bool QCDuncertainty100
			 )
{
  TCanvas * mycan = new TCanvas();

  TLegend* l1 = new TLegend(0.5, 0.8, 0.95, 0.93);
  l1->SetFillStyle(0);
  l1->SetBorderSize(0);

  TGraph *tg1 = new TGraph(  nPoints,dataX,dataH);
  tg1->SetLineWidth(3);
  tg1->SetLineColor(kRed);
  tg1->Draw("AL");
  l1->AddEntry(tg1, "t#bar{t}#rightarrowW^{#pm}H^{#pm}b#bar{b}", "l");

  tg1->GetYaxis()->SetNdivisions(410);
  tg1->GetYaxis()->SetTitle("N_{events}");
  tg1->GetXaxis()->SetNdivisions(410);
  tg1->GetXaxis()->SetTitle("BR(t#rightarrowH^{+}b) [%]");

  // do not take HH into account
//   TGraph *tg2 = new TGraph(  nPoints,dataX,dataHH);
//   tg2->SetLineWidth(3);
//   tg2->SetLineStyle(5);
//   gStyle->SetLineStyleString(11,"40 40");
//   tg2->SetLineStyle(11);
//   tg2->SetLineColor(kGreen+3);
//   tg2->Draw("L");
//   l1->AddEntry(tg2, "t#bar{t}#rightarrowH^{+}H^{-}b#bar{b}", "l");

  TGraph *tg3 = new TGraph(  nPoints,dataX,dataW);
  tg3->SetLineWidth(3);
  tg3->SetLineStyle(7);
  tg3->SetLineColor(kBlue);
  tg3->Draw("L");
  l1->AddEntry(tg3, "t#bar{t}#rightarrowW^{+}W^{-}b#bar{b}", "l");

  TLine * myLine = new TLine(0,background,dataX[nPoints-1],background);
  myLine->SetLineWidth(5);
  //  myLine->SetLineStyle(10);
  myLine->SetLineStyle(2);
  //  myLine->SetLineColor(kOrange);
  myLine->SetLineColor(414);//green
  myLine->Draw();
  char temp[200];
  sprintf(temp,"other bkg at %i (QCD + W jets)", background);
  l1->AddEntry(myLine,temp,"l");

  l1->Draw();

  plotPreliminaryText(plotTitle,QCDuncertainty100);
  plotLuminosityText(lumi);
  plotHiggsMassText(HiggsMass);

  sprintf(temp,"eventYields_%i.png",HiggsMass);
  mycan->Print(temp);

  return ;
}


// x:MH, y:BR
void makePlotBRlimits(const Int_t nPoints, 
		      Double_t * myx,
		      Double_t * myYup,
		      Double_t * myYlow,
		      char * plotTitle,
		      Double_t myluminosity,
		      bool QCDuncertainty100){
  TCanvas * mycan = new TCanvas();
  TGraph * mygraup = new TGraph(nPoints,myx,myYup);
  mygraup->SetLineWidth(4);
  mygraup->SetLineColor(418);
  mygraup->SetMarkerColor(418);
  mygraup->SetMarkerSize(1.4);
  mygraup->Draw("ALP");
  int brlimitymax = 28;
  mygraup->GetYaxis()->SetRangeUser(0,brlimitymax);
  TGraph * mygralow = new TGraph(nPoints,myx,myYlow);
  mygralow->SetLineWidth(4);
  mygralow->SetLineColor(4);
  mygralow->SetLineStyle(2);
  mygralow->SetMarkerColor(4);
  mygralow->SetMarkerSize(1.4);
  mygralow->SetFillColor(4);
  mygralow->SetFillStyle(3021);
  mygralow->Draw("LP");

  Double_t areaX[nPoints*2];
  Double_t areaYup[nPoints*2];
  Double_t areaYlow[nPoints*2];
  for (int i=0; i<nPoints; i++){
    areaX[i]=myx[i];
    areaYup[i]=myYup[i];
    areaYlow[i]=myYlow[i];
    areaX[2*nPoints-1-i]=myx[i];
    areaYup[2*nPoints-1-i]=myYlow[i];
    areaYlow[2*nPoints-1-i]=0;
    //    cout << "x1 " << areaX[i] << "  y " << areaYup[i] << endl;
    //    cout << "x1 " << areaX[2*nPoints-1-i] << "  y " << areaYup[2*nPoints-1-i] << endl;
  }
  TGraph * upperArea = new TGraph(2*nPoints,areaX,areaYup);
  upperArea->SetFillColor(418);
  upperArea->SetFillStyle(3004);
  upperArea->SetLineColor(418);
  upperArea->SetLineWidth(0);
  upperArea->Draw("F");
  TGraph * lowerArea = new TGraph(2*nPoints,areaX,areaYlow);
  lowerArea->SetFillColor(4);
  lowerArea->SetFillStyle(3021);
  lowerArea->SetLineColor(4);
  lowerArea->SetLineWidth(0);
  lowerArea->Draw("F");

  mygraup->GetYaxis()->SetNdivisions(410);
  mygraup->GetYaxis()->SetTitle("BR(t#rightarrowH^{+}b) [%]");
  mygraup->GetXaxis()->SetNdivisions(410);
  mygraup->GetXaxis()->SetTitle("M_{H^{#pm}} [GeV/c^{2}]");
  
  bool plotTevatron1fb = true;
  TGraph * tevaGraph;
  if (plotTevatron1fb) {
    Double_t tevax[] = {  90,  110,  130,  150};
    Double_t tevay[] = {  15,   15,   17,   19};
    tevaGraph = new TGraph(4,tevax,tevay);
    tevaGraph->SetLineColor(kRed);
    tevaGraph->SetLineStyle(2);
    tevaGraph->SetLineWidth(4);
    tevaGraph->SetMarkerColor(kRed);
    tevaGraph->SetMarkerSize(1.4);
    tevaGraph->Draw("LP");
  }

  TLegend* l1 = new TLegend(0.55, 0.8, 0.95, 0.93, "BR exclusion limits ");
  l1->SetFillStyle(0);
  l1->SetLineWidth(0);
  l1->SetBorderSize(0);
  if (plotTevatron1fb)
    l1->AddEntry(tevaGraph, "Tevatron limits with 1 fb^{-1}", "LP");
  //  l1->AddEntry(upperArea, "95% CL + 10% syst. error", "F");
  l1->AddEntry(mygraup, "95% CL + 10% syst. error", "L");
  //  l1->AddEntry(lowerArea, "95% CL", "F");
  l1->AddEntry(mygralow, "95% CL", "L");
  l1->Draw();

  plotPreliminaryText(plotTitle,QCDuncertainty100);
  plotLuminosityText(myluminosity);

  char temp[200];
  sprintf(temp,"BRlimits.png");
  mycan->Print(temp);

  return;
}


void makeLuminosityPlot(Double_t b, 
			Double_t NHBR100, 
			Double_t NttNoH, 
			const Int_t nPoints, 
			Double_t dataXmax, 
			const Double_t rangeMin, 
			const Double_t rangeMax, 
			Double_t HiggsMass,
			Double_t myLuminosity,
			char * plotTitle,
			bool QCDuncertainty100) {

  TCanvas * mycan = new TCanvas();
  mycan->SetLogx();
  
  Double_t CLlimit, CLstatlimit;
  Double_t maxY=0;
  Double_t minY=0;
  Double_t maxX=0;
  Double_t minX=0;
  
  const int lumiPoints = 5;
  Double_t myx[lumiPoints], myyup[lumiPoints],myydo[lumiPoints];
  Double_t areaX[2*lumiPoints], areaYup[2*lumiPoints], areaYlow[2*lumiPoints];
  for (int i=0; i<lumiPoints; i++) {
    //    const Double_t C = 2* (i+1.0)/lumiPoints;
    const Double_t C = 1.0/10 * TMath::Power(sqrt(10),i);
    myx[i] = myLuminosity * C;
    calculateAndPlotEventYields(C * b, 
				C * NHBR100, 
				C * NttNoH, 
				nPoints, 
				dataXmax, 
				rangeMin, 
				rangeMax, 
				HiggsMass, 
				CLlimit, 
				CLstatlimit,
				false,
				plotTitle,
				myLuminosity,
				QCDuncertainty100);
    myydo[i] = CLlimit;
    myyup[i] = CLstatlimit;

    areaX[i] = myx[i];
    areaYup[i] =myyup[i];
    areaYlow[i]=myydo[i];
    areaX[2*lumiPoints-1-i]=myx[i];
    areaYup[2*lumiPoints-1-i]=myydo[i];
    areaYlow[2*lumiPoints-1-i]=0;

    if (i==0){
      minX = myx[i];
      maxX = myx[i];

    }
    if (myx[i]<minX) minX = myx[i];
    if (myx[i]>maxX) maxX = myx[i];
    //    if (CLstatlimit>maxY) maxY=CLstatlimit;
    //        cout << "lumi " << myx[i] << " CL " << myydo[i] << " stat " << myyup[i] << endl;
  }
  
  TGraph *mygraup = new TGraph(lumiPoints,myx,myyup);
  mygraup->SetLineWidth(4);
  mygraup->SetLineColor(418);
  mygraup->SetMarkerColor(418);
  mygraup->SetMarkerSize(1.4);  
  mygraup->Draw("ALP");
  TGraph *mygralow = new TGraph(lumiPoints,myx,myydo);
  mygraup->Draw("APL");
  mygralow->SetLineWidth(4);
  mygralow->SetLineColor(4);
  mygralow->SetLineStyle(7); // does not work for
  mygralow->SetMarkerColor(4);
  mygralow->SetMarkerSize(1.4);
  mygralow->SetFillColor(4);
  mygralow->SetFillStyle(3021);
  mygralow->Draw("PL");
  mygraup->GetYaxis()->SetRangeUser(0,30);
  mygraup->GetXaxis()->SetRangeUser(minX,1.1*maxX);

  TGraph * upperArea = new TGraph(2*lumiPoints,areaX,areaYup);
  upperArea->SetFillColor(418);
  upperArea->SetFillStyle(3004);
  upperArea->SetLineColor(418);
  upperArea->SetLineWidth(0);
  upperArea->Draw("F");
  TGraph * lowerArea = new TGraph(2*lumiPoints,areaX,areaYlow);
  lowerArea->SetFillColor(4);
  lowerArea->SetFillStyle(3021);
  lowerArea->SetLineColor(4);
  lowerArea->SetLineWidth(0);
  lowerArea->Draw("F");

  TLegend* l1 = new TLegend(0.55, 0.8, 0.95, 0.93, "BR exclusion limits ");
  l1->SetFillStyle(0);
  l1->SetLineWidth(0);
  l1->SetBorderSize(0);
  l1->AddEntry(mygraup, "95% CL + 10% syst. error", "L");
  l1->AddEntry(mygralow, "95% CL", "L");
  l1->Draw();

  plotPreliminaryText(plotTitle,QCDuncertainty100);
  plotHiggsMassText(HiggsMass);

  mygraup->GetYaxis()->SetNdivisions(410);
  mygraup->GetYaxis()->SetTitle("BR(t#rightarrowH^{+}b) [%]");
  mygraup->GetXaxis()->SetNdivisions(410);
  mygraup->GetXaxis()->SetTitle("L [pb^{-1}]");

  char temp[200];
  sprintf(temp,"luminosity_%d.png",HiggsMass);
  mycan->Print(temp);

  return;
}


void makePlotEfficiency(Double_t * dataA, Double_t * dataB,Double_t * limitPlotX,const int nMassPoints, Double_t lumi,char *plotTitle,bool QCDuncertainty100)
{
  char temp[200];
  Double_t dataC[nMassPoints];

  TCanvas * mycan = new TCanvas();
  mycan->SetLogy();

  for (int i=0; i<nMassPoints; i++) {
    dataA[i]*=100;
    dataB[i]*=100;
  }

  TGraph * myGraph1 = new TGraph(nMassPoints,limitPlotX,dataA);
  myGraph1->SetLineColor(kBlue);
  myGraph1->SetLineWidth(3);
  myGraph1->SetMarkerStyle(8);
  myGraph1->SetMarkerColor(kBlue);
  myGraph1->SetMarkerSize(1.6);
  myGraph1->Draw("APL");

  TGraph * myGraph2 = new TGraph(nMassPoints,limitPlotX,dataB);
  myGraph2->SetLineColor(414);
  myGraph2->SetLineWidth(3);
  myGraph2->SetMarkerStyle(8);
  myGraph2->SetMarkerColor(414);
  myGraph2->SetMarkerSize(1.6);
  myGraph2->Draw("PL");

  for (int i=0; i<nMassPoints; i++)
    dataC[i] = dataA[i] * dataB[i] / 100.0;
  TGraph * myGraph3 = new TGraph(nMassPoints,limitPlotX,dataC);
  myGraph3->SetLineColor(1);
  myGraph3->SetLineWidth(4);
  myGraph3->SetMarkerStyle(8);
  myGraph3->SetMarkerColor(1);
  myGraph3->SetMarkerSize(1.6);
  myGraph3->Draw("PL");

  TLegend* l1 = new TLegend(0.55, 0.8, 0.9, 0.93);
  l1->SetFillStyle(0);
  l1->SetLineWidth(0);
  l1->SetBorderSize(0);
  l1->AddEntry(myGraph1, "3 jets selection", "l");
  l1->AddEntry(myGraph2, "other selections", "l");
  l1->AddEntry(myGraph3, "all selections", "l");
  l1->Draw();

  plotPreliminaryText(plotTitle,QCDuncertainty100);

  myGraph1->GetXaxis()->SetNdivisions(410);
  myGraph1->GetXaxis()->SetTitle("M_{H^{#pm}} [GeV/c^{2}]");
  myGraph1->GetYaxis()->SetNdivisions(410);
  myGraph1->GetYaxis()->SetTitle("efficiency [%]");
  /*  Double_t rangeMin=dataA[0], rangeMax=dataA[0];
  for (int i=0; i<nMassPoints; i++){
    if (dataA[i]<rangeMin) rangeMin=0.9*dataA[i];;
    if (dataA[i]>rangeMax) rangeMax=1.2*dataA[i];
    if (dataB[i]<rangeMin) rangeMin=0.9*dataB[i];;
    if (dataB[i]>rangeMax) rangeMax=1.2*dataB[i];
    if (dataC[i]<rangeMin) rangeMin=0.9*dataC[i];;
    if (dataC[i]>rangeMax) rangeMax=1.2*dataC[i];
    }*/
  rangeMax = 100;
  rangeMin = 1;
  myGraph1->GetYaxis()->SetRangeUser(rangeMin,rangeMax);

  sprintf(temp,"efficiencies.png",plotTitle);
  mycan->Print(temp);

  return;
}

void poisson(int choice=0, Double_t myLuminosity = 40,//pb-1
	     bool QCDuncertainty100 = false ) {
  if (choice==0) {
    cout << "No choice made!" << endl << endl
	 << "Usage in root: .x poisson.C(n)" << endl
	 << "where n=1 for hard cuts, 3 jets" << endl
	 << "      n=2 for soft cuts, 3 jets" << endl
	 << "      n=3 for hard cuts, 4 jets, 2 b-jets" << endl
	 << "      n=4 for soft cuts, 3 jets, 1 b-jet" << endl
	 << "      n=5 for TaNC (soft cuts, 3 jets, 1 b-jet)" << endl
	 << "      n=6 for TaNC (4 jets)" << endl
	 << "      n=7 for HPS Tau ID (3 jets, 1 b-jet, MET>70, tau jet ET>30)" << endl; //    qcd = 0.0016;
    NttNoH = 0.0522; // tt
    wjets = 0.0257;

    cout << "Additionnally, you can - override the default luminosity setting (example 100/pb) and" << endl
	 << "                       - use 100% uncertainty for QCD" << endl 
	 << "with this command: .x poisson.C(6,100,true)" << endl;
    return;
  }

  bool plotLumi = true; // if false, the time-consuming luminosity plot is skipped
 
  const Int_t nMaxMassPoints = 6; // needed for array initializations
  Int_t nMassPoints = 6;
  Double_t limitPlotX[] = {  80,    90,    100,  120, 140   , 160}; // default

  char plotTitle[200];

  Double_t NttNoH, wjets, qcd;

  if (choice==1) {
    Double_t NHBR100[]    = {2.023, 2.088, 2.218, 2.665, 3.034, 2.977};
    NttNoH = 0.294;
    wjets = 0.214; 
    qcd = 0.181;
    Double_t dataA[] = {0.656 ,0.651 , 0.6325 , 0.591 , 0.515 , 0.410};
    Double_t dataB[] = {0.0190,0.0198,0.0216,0.0279,0.0363,0.0447};
    sprintf(plotTitle,"hard cuts, 3 jets");
  }
  else if (choice==2) {
    Double_t NHBR100[]    = {6.285, 6.589, 6.849, 7.161, 6.858, 5.947};
    NttNoH = 1.216;
    wjets = 0.999; 
    qcd = 6.518;
    Double_t dataA[] = {0.657, 0.651, 0.634, 0.594, 0.509, 0.407};
    Double_t dataB[] = {0.0543,0.0624,0.0666,0.0746,0.0829,0.0870}; 
    sprintf(plotTitle,"soft cuts, 3 jets");
  }
  else if (choice==3)
    {
      // corrections calculated earlier
      Double_t NHBR100[]    = {0.65445,0.59556,0.64531,0.70310,0.70609,0.45883};
      wjets = 0.015; 
      qcd = 0.0082;
      NttNoH = 0.077;
      //      Double_t dataA[] = {0.657, 0.651, 0.634, 0.594, 0.509, 0.407};
      //      Double_t dataB[] = {0.0543,0.0624,0.0666,0.0746,0.0829,0.0870}; 
      sprintf(plotTitle,"at least 4 jets, 2 tagged b-jets");     
    }
  else if (choice==4)
    {
      // corrections calculated earlier
      Double_t NHBR100[]    = {1.55433,1.55072,1.67255,1.96454,2.11826,1.92707};
      wjets = 0.020; 
      qcd = 0.36; 
      NttNoH = 0.183; // tt
      sprintf(plotTitle,"at least 3 jets, 1 tagged b-jet");     
    }
  else if (choice==5)
    {
      // corrections calculated earlier
      Double_t NHBR100[]    = {	1.61466, 1.66309, 1.77659, 2.09895, 2.29478, 2.17943 };
      wjets = 0.0266; 
      qcd = 0.1297;
      NttNoH = 0.1926; // tt
      sprintf(plotTitle,"at least 3 jets, 1 tagged b-jet, TaNC");     
    }
  else if (choice==6)
    {
      //      Double_t NHBR100[]    = {	1.61466, 1.66309, 1.77659, 2.09895, 2.29478, 2.17943 };
      Double_t NHBR100[]    = {	0.0640, 0.0580, 0.0530, 0.0380, 0.0180, 0.0023 };
      // calculate corrections here
      Double_t BR_t_bH[] =    {0.05395, 0.04809, 0.04050, 0.02526, 0.01165, 0.002216};
      Double_t BR_H_taunu[] = {0.95800, 0.97200, 0.97700, 0.98200, 0.98400, 0.985700};
      for (int i=0; i<nMassPoints; i++){
	NHBR100[i] = NHBR100[i] /
	  ( 2.0*BR_t_bH[i]*(1.0-BR_t_bH[i])*BR_H_taunu[i] );
      }
      qcd = 0.0165;
      NttNoH = 0.083; // tt
      wjets = 0.0176;
      sprintf(plotTitle,"at least 4 jets, 2 tagged b-jets, TaNC");     
    }
  else if (choice==7)
    {
      // Here only 5 mass points, no point m=80

      // change 0.04 to correct values

      nMassPoints = 5;
      int i=0;
      limitPlotX[i++] = 90;
      limitPlotX[i++] = 100;
      limitPlotX[i++] = 120;
      limitPlotX[i++] = 140;
      limitPlotX[i++] = 160;

      Double_t NHBR100[]    = {	0.04812, 0.044, 0.0334, 0.0169, 0.00324 };
      // calculate corrections here
      Double_t BR_t_bH[] =    { 0.04809, 0.04050, 0.02526, 0.01165, 0.002216};
      Double_t BR_H_taunu[] = { 0.97200, 0.97700, 0.98200, 0.98400, 0.985700};
      for (int i=0; i<nMassPoints; i++){
	NHBR100[i] = NHBR100[i] /
	  ( 2.0*BR_t_bH[i]*(1.0-BR_t_bH[i])*BR_H_taunu[i] );
      }
      qcd = 0.0016;
      NttNoH = 0.0522; // tt
      wjets = 0.0257;
      sprintf(plotTitle,"HPS TauID, MET>70 GeV, 3 jets");     
	      //HPS Tau ID (3 jets, 1 b-jet, MET>70, tau jet ET>30)
    }

  else {
    cout << "Inappropriate choice!" << endl;
    return;
  }

  Double_t backgr;
  if (QCDuncertainty100)
    backgr = wjets + 2*qcd;
  else
    backgr = wjets +   qcd;

  cout << endl << "Making plots for " << plotTitle << endl;

  gROOT->ProcessLine(".L tdrstyle.C");
  setTDRStyle();

  //  makePlotEfficiency(dataA,dataB,limitPlotX,nMassPoints,10,plotTitle,QCDuncertainty100);

  Double_t limitPlotYlow[nMaxMassPoints];
  Double_t limitPlotYup[nMaxMassPoints];
  Double_t CLlimit=0, CLstatlimit=0;

  for (int i=0; i<nMassPoints; i++) {
    Double_t HiggsMass = limitPlotX[i];
    //    Double_t myLuminosity = 40;//pb-1
    Double_t myB=backgr*myLuminosity;
    Double_t myNHBR100=NHBR100[i]*myLuminosity; // if BR=100 required, number of H
    Double_t myNttNoH=NttNoH*myLuminosity,; // number of tt without H or HH
    const Int_t nPoints = 200;
    Double_t dataXmax = 25;
    const Double_t rangeMin = 10000;  //enlarged if necessary
    const Double_t rangeMax = 50;//enlarged if necessary
    //    cout << "b " << myB << " " << myNHBR100 << " " <<myNttNoH << " " << nPoints << " " << dataXmax << " " <<rangeMin << " " << rangeMax << " " <<HiggsMass<< " " <<endl; 
    calculateAndPlotEventYields(myB, myNHBR100, myNttNoH, nPoints, dataXmax, rangeMin, rangeMax, HiggsMass, CLlimit, CLstatlimit,true,plotTitle,myLuminosity,QCDuncertainty100);

    if (plotLumi)
      makeLuminosityPlot(myB, myNHBR100, myNttNoH, nPoints, dataXmax, rangeMin, rangeMax, HiggsMass,myLuminosity,plotTitle,QCDuncertainty100);
    cout << "---- masspoint" << HiggsMass << ", BR limits " << CLlimit << " and " << CLstatlimit << endl;
    limitPlotYlow[i] = CLlimit;
    limitPlotYup[i]  = CLstatlimit;
  }

  makePlotBRlimits(nMassPoints,limitPlotX,limitPlotYup,limitPlotYlow,plotTitle,myLuminosity,QCDuncertainty100);

  return;
}

void calculateAndPlotEventYields(Double_t b, 
				 Double_t NHBR100, 
				 Double_t NttNoH, 
				 const Int_t nPoints, 
				 Double_t dataXmax, 
				  Double_t rangeMin, 
				 Double_t rangeMax, 
				 Double_t HiggsMass,
				 Double_t &retCLlimit, Double_t &retCLstatlimit,
				 bool doPlots,
				 char * plotTitle,
				 Double_t myLuminosity,
				 bool QCDuncertainty100) {

  retCLlimit = 100; // back-up value in case the limit is not found

  //  cout << "Calculating data points for  m_H=" << HiggsMass << endl;
  Double_t dataY[nPoints];
  Double_t dataX[nPoints];
  Double_t dataHH[nPoints];
  Double_t dataH[nPoints];
  Double_t dataW[nPoints];
  
  for (int i=0; i<nPoints; i++){
    const Double_t BR=1.0*i*dataXmax/nPoints/100;
    const Double_t N = NHBR100;
    dataX[i] = BR*100;
    //    dataHH[i]= N*BR*BR;; // do not take into account
    dataH[i] = 2*N*(BR-BR*BR); // N*BR - N*BR*BR;
    dataW[i] = NttNoH*(1.0 - 2*BR + BR*BR); //NttNoH*(1.0 - BR - BR*BR);
    //dataY[i] = b + dataH[i] + dataHH[i] + dataW[i];
    dataY[i] = b + dataH[i] + dataW[i];
  }
  
  if (doPlots){
    //    cout << "making event yields plot for m_H=" << HiggsMass << endl;
    makePlotEventYields(nPoints,dataX,dataH,dataHH,dataW,b,HiggsMass,plotTitle,myLuminosity,QCDuncertainty100);
  }

  Double_t x1[nPoints], x2[2*nPoints], x3[2*nPoints], y1[nPoints], y2[2*nPoints], y3[2*nPoints];


  bool CLlimitFound=false;
  Double_t CLlimit=100, CLstatlimit=100;
  bool CLstatLimitFound=false;
  // ---------- copy data to graphs -------------
  for (int i=0; i<nPoints; i++) {
    Double_t myx = dataX[i];
    Double_t myy = dataY[i]; 

    Double_t myyCL   = calcPoissonLowerCL(myy);
    Double_t myyStat = myyCL-calcStatError(myy);

    x1[i] = myx;
    y1[i] = myy;

    x2[i] = myx;
    y2[i] = myy;
    x2[2*nPoints-1-i] = myx;
    y2[2*nPoints-1-i] = myyCL;

    if (CLlimitFound==false && y2[2*nPoints-1-i]>dataY[0]) {
      CLlimitFound=true;
      //      cout << "95 CL at " << myx << " , " << y2[2*nPoints-1-i] << endl;
      CLlimit = myx;
      retCLlimit = CLlimit;
    }

    x3[i] = myx;
    y3[i] = myyCL;
    x3[2*nPoints-1-i] = myx;
    y3[2*nPoints-1-i] = myyStat;
    if (CLstatLimitFound==false && y3[2*nPoints-1-i]>dataY[0]) {
      CLstatLimitFound=true;
      //      cout << "95 CL +stat at " << myx << " , " << y3[2*nPoints-1-i] << endl; 
      CLstatlimit = myx;
      //      retCLstatlimit = CLstatlimit;
    }

    if (rangeMax<myy) rangeMax=myy;
    if (rangeMin>myyStat) rangeMin=myyStat;
  }

  retCLstatlimit = CLstatlimit;

  if (doPlots) {
  TCanvas * mycan = new TCanvas();

  TGraph *tg1 = new TGraph(  nPoints,x1,y1);
  TGraph *tg2 = new TGraph(2*nPoints,x2,y2);
  TGraph *tg3 = new TGraph(2*nPoints,x3,y3);

  tg1->SetLineWidth(5.0);
  tg1->SetMarkerSize(1.4);
  tg1->SetLineColor(1);
  tg1->Draw("AL");
  
  tg3->SetFillColor(418);
  tg3->SetFillStyle(3004);
  tg3->SetLineColor(kWhite);
  tg3->SetLineWidth(0);
  tg3->Draw("F");

  tg2->SetFillColor(kWhite);
  tg2->SetFillStyle(1001);
  tg2->Draw("F");
  tg2->SetFillColor(4);
  tg2->SetFillStyle(3021);
  tg2->SetLineColor(kWhite);
  tg2->SetLineWidth(0);
  tg2->Draw("F");

  Double_t rangeWidth = rangeMax - rangeMin;
  Double_t plotYmin = rangeMin - rangeWidth*0.05;
  Double_t plotYmax = rangeMax + rangeWidth*0.22;
  tg1->GetYaxis()->SetRangeUser(plotYmin, plotYmax);
  tg1->GetYaxis()->SetNdivisions(410);
  tg1->GetYaxis()->SetTitle("N_{events}");
  tg1->GetXaxis()->SetNdivisions(410);
  tg1->GetXaxis()->SetTitle("BR(t#rightarrowH^{+}b) [%]");
  
  // redraw line
  tg1->Draw("L");

  
  plotPreliminaryText(plotTitle,QCDuncertainty100);
  plotLuminosityText(myLuminosity);
  plotHiggsMassText(HiggsMass);
  /*
  char temp[200];

  Double_t infoLineSpace = 5.0;
  Double_t infoY = 0.58;
  sprintf(temp,"m_{H^{#pm}} = %d GeV/c^{2}",HiggsMass);
  //  sprintf(temp,"m_{H^{#pm}} = xxx GeV/c^{2}");
  text.DrawLatex(0.2,0.7,temp);*/

  TLine * myLine = new TLine(0,dataY[0],dataX[nPoints-1],dataY[0]);
  myLine->SetLineWidth(4);
  myLine->SetLineStyle(2);
  myLine->Draw();
  TLatex text;
  text.SetTextAlign(12);
  text.SetTextSize(0.025);
  text.SetNDC(kFALSE);
  text.DrawLatex(13.1,dataY[0]-rangeWidth/40.0,"Expected from SM alone");

  if (CLlimitFound) {
    TLine * CLlimitline = new TLine(CLlimit,plotYmin,CLlimit,dataY[1]);
    CLlimitline->SetLineColor(kBlue);
    CLlimitline->SetLineWidth(3);
    CLlimitline->SetLineStyle(7);
    CLlimitline->Draw();
    text.SetTextSize(0.02);
    text.SetTextColor(kBlue);
    text.SetTextAngle(90);
    text.DrawLatex(CLlimit+0.5,rangeMin,"CL limit");
    //    cout << "line " << CLlimit << " " << rangeMin  << " " << CLlimit  << " " << rangeMax<<endl;
  }

  if (CLstatLimitFound) {
    TLine * CLstatlimitline = new TLine(CLstatlimit,plotYmin,CLstatlimit,dataY[1]);
    CLstatlimitline->SetLineColor(414);
    CLstatlimitline->SetLineWidth(3);
    CLstatlimitline->SetLineStyle(7);
    CLstatlimitline->Draw();
    text.SetTextSize(0.02);
    text.SetTextColor(414);
    text.SetTextAngle(90);
    text.DrawLatex(CLstatlimit+0.5,rangeMin+0.03,"CL + syst. limit");
    //    cout << "line " << CLlimit << " " << rangeMin  << " " << CLlimit  << " " << rangeMax<<endl;
  }

  TLegend* l1 = new TLegend(0.55, 0.8, 0.9, 0.93);
  l1->SetFillStyle(0);
  l1->SetLineWidth(0);
  l1->SetBorderSize(0);
  l1->AddEntry(tg1, "Selected events", "l");
  l1->AddEntry(tg2, "95% CL", "F");
  l1->AddEntry(tg3, "95% CL + 10% syst. error", "F");
  //   l1->AddEntry(h1, Form("binomial : mean = %4.2f RMS = \
    //      %4.2f", h1->GetMean(), h1->GetRMS()), "l");
    l1->Draw();
    
    char temp[200];
    sprintf(temp,"BRlimits_%i.png",HiggsMass);
    mycan->Print(temp);
  }
  
  return;
}
