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
#include "fstream.h"
#include "stdio.h"

int calcPoissonLowerCL(int lambda) {
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


void makePoissonFile()
{
  cout << "Calculating Poisson CL values, can take tens of minutes..." << endl;
  ofstream logFile("precalculatedPoissonValues.txt",ios::out);   // hard-coded file name

  const int nMax = 100000;
  for (int i=0; i<nMax; i++) {
    if ( i%(nMax/20)==0 ) 
      cout << 100.0*i/nMax << "% completed" << endl;
    logFile << i << " " << calcPoissonLowerCL(i) << endl;
  }
  cout << "100% completed" << endl;
}
