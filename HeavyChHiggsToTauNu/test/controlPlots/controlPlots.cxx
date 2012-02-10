#include <vector>
#include <iostream>
#include <sstream>
#include <string>
#include <sstream>
#include <TFile.h>
#include <TH1D.h>
#include <TGraphErrors.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TStyle.h>
#include "TLegend.h"
#include "THStack.h"
#include "TColor.h"
#include "TLatex.h"

using namespace std;

class ControlPlot {
public:
  ControlPlot(string label, string sourceHisto);
  ControlPlot(string label, TH1* h);
  virtual ~ControlPlot();
  /// Extract plot from supplied info
  virtual bool extract(vector<TFile*> data, vector<TFile*> mc, TH1* frameHisto);
  void setNormalisationInfo(string configInfoHisto, string counterHisto, double lumiPb) { sConfigInfoHisto = configInfoHisto; sCounterHisto = counterHisto; fLuminosityInPb = lumiPb; }
  
  TH1* getPlot() { return hPlot; }
  string getLabel() { return sDatasetLabel; }
  
protected:
  double getNormFactor(TFile* f);
  bool loopOverFiles(std::vector< TFile* > files, string source, TH1* histo);

protected:
  string sSourceHisto;
  TH1* hPlot;
  
private:
  string sDatasetLabel;
  string sCounterHisto;
  string sConfigInfoHisto;
  double fLuminosityInPb;
};

ControlPlot::ControlPlot(string label, string sourceHisto)
: sSourceHisto(sourceHisto),
  hPlot(0),
  sDatasetLabel(label),
  fLuminosityInPb(0) {

}
ControlPlot::ControlPlot(string label, TH1* h)
: sSourceHisto(""),
  hPlot(h),
  sDatasetLabel(label),
  fLuminosityInPb(0) {
  
}

ControlPlot::~ControlPlot() {

}

bool ControlPlot::extract(std::vector< TFile* > data, std::vector< TFile* > mc, TH1* frameHisto) {
  if (!sSourceHisto.size()) return true;
  hPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
  hPlot->Sumw2();
  // Loop over data
  if (!loopOverFiles(data, sSourceHisto, hPlot)) return false;
  // Loop over MC
  if (!loopOverFiles(mc, sSourceHisto, hPlot)) return false;
  return true;
}

bool ControlPlot::loopOverFiles(std::vector< TFile* > files, string source, TH1* histo) {
  for (size_t i = 0; i < files.size(); ++i) {
    double myNormFactor = 1.0;
    // Obtain plot
    TH1* h = dynamic_cast<TH1*>(files[i]->Get(source.c_str()));
    if (!h) {
      cout << "Error: Cannot open histogram " << source << "!" << endl;
      return false;
    }
    // Obtain normalisation
    myNormFactor = getNormFactor(files[i]); // returns 1 if file contains data
    //cout << "file = " << files[i]->GetName() << " norm=" << myNormFactor << endl;
    if (myNormFactor < 0) return false;
    // Check axis scale
    if (TMath::Abs(h->GetXaxis()->GetXmax() - histo->GetXaxis()->GetXmax()) > 0.0001 ||
        TMath::Abs(h->GetXaxis()->GetXmin() - histo->GetXaxis()->GetXmin()) > 0.0001){
      cout << "Error: " << source << ": Range in histograms is different! Asked for " << h->GetXaxis()->GetXmin() << " - " << h->GetXaxis()->GetXmax() 
           << " but input has " << histo->GetXaxis()->GetXmin() << " - " << histo->GetXaxis()->GetXmax() << endl;
      return false;
    }
    
    // Check binning   
    if (h->GetNbinsX() > histo->GetNbinsX()) {
      h->Rebin(h->GetNbinsX() / histo->GetNbinsX());
      if (h->GetNbinsX() != histo->GetNbinsX()) {
        cout << "Error: Automatic rebin failed: ended up with " << histo->GetNbinsX() << " but only " << h->GetNbinsX() << " available in histogram " << source << "!" << endl;
        return false;
      }
    }
    else if (h->GetNbinsX() < histo->GetNbinsX()) {
      cout << "Error: asked for " << histo->GetNbinsX() << " but only " << h->GetNbinsX() << " available in histogram " << source << "!" << endl;
      return false;
    }
    histo->Add(h, myNormFactor);
  }
  return true;
}

double ControlPlot::getNormFactor(TFile* f) {
  // Get config info histo
  TH1* myConfigHisto = dynamic_cast<TH1*>(f->Get(sConfigInfoHisto.c_str()));
  if (!myConfigHisto) {
    cout << "Error: Cannot open histogram " << sConfigInfoHisto << "! (" << f->GetName() << ")" << endl;
    return -1.;
  }
  // Get counter histo
  TH1* myCounterHisto = dynamic_cast<TH1*>(f->Get(sCounterHisto.c_str()));
  if (!myCounterHisto) {
    cout << "Error: Cannot open histogram " << sCounterHisto << "!" << endl;
    return -1.;
  }
  // Check if file is data
  for (int i = 1; i <= myConfigHisto->GetNbinsX(); ++i) {
    string myLabel = myConfigHisto->GetXaxis()->GetBinLabel(i);
    if (myLabel == "isData") {
      if (myConfigHisto->GetBinContent(i) > 0)
        return 1.0;
    }
  }
  
  // Calculate normalisation
  double myXsection = myConfigHisto->GetBinContent(2) / myConfigHisto->GetBinContent(1);
  //std::cout << myXsection << std::endl;
  double myAllEvents = myCounterHisto->GetBinContent(1);
  //cout << "    xsec=" << myXsection << " all evt = " << myAllEvents << " norm. fact=" << myXsection * fLuminosityInPb / myAllEvents << endl;
  if (myAllEvents > 0)
    return myXsection * fLuminosityInPb / myAllEvents;
  return 0;
}

class QCDControlPlot : public ControlPlot {
public:
  QCDControlPlot(string sourceHisto, bool sourceIsBinned, string beforeTauIDHisto, string passedTauIDHisto);
  ~QCDControlPlot();
  
  bool extract(vector<TFile*> data, vector<TFile*> mc, TH1* frameHisto);
  
private:
  bool bSourceIsBinned;
  string sBeforeTauID;
  string sAfterTauID;
};

QCDControlPlot::QCDControlPlot(string sourceHisto, bool sourceIsBinned, string beforeTauIDHisto, string passedTauIDHisto)
: ControlPlot("QCD (meas.)", sourceHisto),
  bSourceIsBinned(sourceIsBinned),
  sBeforeTauID(beforeTauIDHisto),
  sAfterTauID(passedTauIDHisto) {

}

QCDControlPlot::~QCDControlPlot() { }
  
bool QCDControlPlot::extract(vector<TFile*> data, vector<TFile*> mc, TH1* frameHisto) {
  static int n = 0;
  stringstream s;
  s << "pthisto" << ++n;
  
  TH1D* myPtHisto = new TH1D(s.str().c_str(),s.str().c_str(),9,0,9);
  TH1D* hBeforeData = dynamic_cast<TH1D*>(myPtHisto->Clone());
  TH1D* hBeforeEWK = dynamic_cast<TH1D*>(myPtHisto->Clone());
  TH1D* hAfterData = dynamic_cast<TH1D*>(myPtHisto->Clone());
  TH1D* hAfterEWK = dynamic_cast<TH1D*>(myPtHisto->Clone());
  if (sBeforeTauID.size()) {
    // Obtain normalisation in bins of tau pT
    if (!loopOverFiles(data, sBeforeTauID, hBeforeData)) return false;
    if (!loopOverFiles(mc, sBeforeTauID, hBeforeEWK)) return false;
    if (!loopOverFiles(data, sAfterTauID, hAfterData)) return false;
    if (!loopOverFiles(mc, sAfterTauID, hAfterEWK)) return false;
  }
  
  if (bSourceIsBinned) {
    // Source is not binned, need to weight each histogram by separate weight
    // Clone frame histo
    TH1D* myResultPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
    myResultPlot->Sumw2();

    for (int j = 1; j <= myResultPlot->GetNbinsX(); ++j) {
      myResultPlot->SetBinContent(j, 0);
      myResultPlot->SetBinError(j, 0);
    }
    for (int i = 0; i < myPtHisto->GetNbinsX(); ++i) {
      double myBeforeCount = hBeforeData->GetBinContent(i+1) - hBeforeEWK->GetBinContent(i+1);
      double myAfterCount = hAfterData->GetBinContent(i+1) - hAfterEWK->GetBinContent(i+1);
      double myWeight = 0.0;
      double myWeightUncertainty = 0.0;
      if (myAfterCount > 0) {
        myWeight = myAfterCount / myBeforeCount;
        myWeightUncertainty = TMath::Sqrt(TMath::Power(hAfterData->GetBinError(i+1),2) + TMath::Power(hAfterEWK->GetBinError(i+1),2)) / myBeforeCount;
      }
      //cout << "Weight = " << myWeight << " +- " << myWeightUncertainty << endl;
      TH1D* myTmpDataPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
      TH1D* myTmpEWKPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
      myTmpDataPlot->Sumw2();
      myTmpEWKPlot->Sumw2();
      stringstream s;
      s << sSourceHisto << "bin" << i;
      if (!loopOverFiles(data, s.str(), myTmpDataPlot)) return false;
      if (!loopOverFiles(mc, s.str(), myTmpEWKPlot)) return false;
      for (int j = 1; j <= myTmpDataPlot->GetNbinsX(); ++j) {
        double myBinValue = myTmpDataPlot->GetBinContent(j)-myTmpEWKPlot->GetBinContent(j);
        double myBinError = TMath::Sqrt(TMath::Power(myTmpDataPlot->GetBinError(j),2) + TMath::Power(myTmpEWKPlot->GetBinError(j),2));
        //cout << "bin=" << i << " data=" << myTmpDataPlot->GetBinContent(j) << " ewk=" << myTmpEWKPlot->GetBinContent(j) << " value=" << myBinValue << " +- " << myBinError << endl;
        myResultPlot->SetBinContent(j, myResultPlot->GetBinContent(j) + myBinValue * myWeight);
        myResultPlot->SetBinError(j, TMath::Sqrt(TMath::Power(myResultPlot->GetBinError(j),2) + TMath::Power(myWeight*myBinError,2) + TMath::Power(myBinValue*myWeightUncertainty,2)));
        //cout << "bin=" << i << " content=" << myResultPlot->GetBinContent(j) << " +- " << myResultPlot->GetBinError(j) 
        //<< " weight uncert=" << myWeightUncertainty
        //<< " binerr=" << TMath::Sqrt(TMath::Power(myWeight*myBinError,2) + TMath::Power(myBinValue*myWeightUncertainty,2)) << endl;
      }
    }
    hPlot = myResultPlot;
  } else {
    // Source is not binned, just substract MCEWK from data bin by bin
    double myWeight = 1.0;
    double myWeightUncertainty = 0.0;
    if (sBeforeTauID.size()) {
      double myBeforeCount = hBeforeData->Integral() - hBeforeEWK->Integral();
      double myAfterCount = hAfterData->Integral() - hAfterEWK->Integral();
      myWeight = 0.0;
      if (myAfterCount > 0) {
        myWeight = myAfterCount / myBeforeCount;
        hAfterData->Rebin(hAfterData->GetNbinsX());
        hAfterEWK->Rebin(hAfterEWK->GetNbinsX());
        myWeightUncertainty = TMath::Sqrt(TMath::Power(hAfterData->GetBinError(1),2) + TMath::Power( hAfterEWK->GetBinError(1),2)) / myBeforeCount;
      }
    }
    //cout << "Weight = " << myWeight << " +- " << myWeightUncertainty << endl;
    // Clone frame histo
    TH1D* myResultPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
    myResultPlot->Sumw2();
    TH1D* myTmpDataPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
    TH1D* myTmpEWKPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
    myTmpDataPlot->Sumw2();
    myTmpEWKPlot->Sumw2();
    if (!loopOverFiles(data, sSourceHisto, myTmpDataPlot)) return false;
    if (!loopOverFiles(mc, sSourceHisto, myTmpEWKPlot)) return false;

    for (int i = 1; i <= myTmpDataPlot->GetNbinsX(); ++i) {
      double myBinValue = myTmpDataPlot->GetBinContent(i)-myTmpEWKPlot->GetBinContent(i);
      double myBinError = TMath::Sqrt(TMath::Power(myTmpDataPlot->GetBinError(i),2) + TMath::Power(myTmpEWKPlot->GetBinError(i),2));

      //cout << "bin=" << i << " data=" << myTmpDataPlot->GetBinContent(i) << " ewk=" << myTmpEWKPlot->GetBinContent(i) << " value=" << myBinValue << " +- " << myBinError << endl;
      myResultPlot->SetBinContent(i, myBinValue*myWeight);
      myResultPlot->SetBinError(i, TMath::Sqrt(TMath::Power(myWeight*myBinError,2) + TMath::Power(myBinValue*myWeightUncertainty,2)));
    }
    hPlot = myResultPlot;
  }
  return true;
}

class EWKControlPlot : public ControlPlot {
public:
  EWKControlPlot(string sourceHisto, double additionalEWKNormalisation);
  ~EWKControlPlot();

  bool extract(vector<TFile*> data, vector<TFile*> mc, TH1* frameHisto);

private:
  double fAdditionalEWKNormalisation;
};

EWKControlPlot::EWKControlPlot(string sourceHisto, double additionalEWKNormalisation)
: ControlPlot("EWK taus (meas.)", sourceHisto),
  fAdditionalEWKNormalisation(additionalEWKNormalisation) {

}

EWKControlPlot::~EWKControlPlot() { }

bool EWKControlPlot::extract(std::vector< TFile* > data, std::vector< TFile* > mc, TH1* frameHisto) {
  hPlot = dynamic_cast<TH1D*>(frameHisto->Clone());
  hPlot->Sumw2();
  // Loop over data
  if (!loopOverFiles(data, sSourceHisto, hPlot)) return false;
  // Scale by additional normalisation
  hPlot->Scale(fAdditionalEWKNormalisation); 
  return true;
}

vector<TFile*> openFiles(string path, vector<string> names) {
  vector<TFile*> myFiles;
  for (size_t i = 0; i < names.size(); ++i) {
    string myFilename = path+"/"+names[i]+"/res/histograms-"+names[i]+".root";
    TFile* f = TFile::Open(myFilename.c_str());
    if (!f) return myFiles;
    myFiles.push_back(f);
  }
  return myFiles;
}

class Manager {
public:
  Manager(string label, TH1* frame, QCDControlPlot* qcd, EWKControlPlot* ewk, string fakeSource, string signalSource);
  Manager(string label, TH1* frame, TH1* qcd, TH1* ewk, TH1* fakes, TH1* hh, TH1* hw, TH1* data);
  ~Manager();

  void setNormalisationInfo(string configInfo, string qcdCounter, string ewkCounter, string fakeCounter, string signalCounter, double lumiPb);
  bool extract(vector<TFile*>& qcdData, vector<TFile*>& qcdMCEWK, vector<TFile*>& ewkData, vector<TFile*>& fakes, vector<TFile*>& hh, vector<TFile*>& hw, vector<TFile*>& signalData);
  void getIntegral(double& nqcd, double& newk, double& nfakes, double& nhh, double& nhw, double& ndata, double min = -1, double max = -1);
  void getIntegralUncert(double& nqcd, double& newk, double& nfakes, double& nhh, double& nhw, double &ndata, double min = -1, double max = -1);
  void makePlot(double xmin, double xmax, double ymin, double ymax, double delta, string xtitle, string ytitle, double br, double mass, bool logy = true);
  string getLabel() { return sLabel; }

  void printInfo(TH1* h, string label);
  void setRelativeUncertainty(int bin, double QCDUncert, double EWKUncert, double fakesUncert, double HHUncert, double HWUncert);
  
private:
  string sLabel;
  TH1* hFrame;
  ControlPlot* fQCD;
  ControlPlot* fEWK;
  ControlPlot* fFakes;
  ControlPlot* fHH;
  ControlPlot* fHW;
  ControlPlot* fData;
  vector<double> fQCDRelativeSystematicUncertainty;
  vector<double> fEWKRelativeSystematicUncertainty;
  vector<double> fFakesRelativeSystematicUncertainty;
  vector<double> fHHRelativeSystematicUncertainty;
  vector<double> fHWRelativeSystematicUncertainty;
};

Manager::Manager(string label, TH1* frame, QCDControlPlot* qcd, EWKControlPlot* ewk, string fakeSource, string signalSource)
: sLabel(label),
  hFrame(frame),
  fQCD(qcd),
  fEWK(ewk) {
  fFakes = new ControlPlot("EWKfakes", fakeSource);
  fHH = new ControlPlot("HH", signalSource);
  fHW = new ControlPlot("HW", signalSource);
  fData = new ControlPlot("Data", signalSource);
  
  for (int i = 1; i <= hFrame->GetNbinsX(); ++i) {
    fQCDRelativeSystematicUncertainty.push_back(0.);
    fEWKRelativeSystematicUncertainty.push_back(0.);
    fFakesRelativeSystematicUncertainty.push_back(0.);
    fHHRelativeSystematicUncertainty.push_back(0.);
    fHWRelativeSystematicUncertainty.push_back(0.);
  }  
}

Manager::Manager(string label, TH1* frame, TH1* qcd, TH1* ewk, TH1* fakes, TH1* hh, TH1* hw, TH1* data)
: sLabel(label),
  hFrame(frame),
  fQCD(new ControlPlot("QCD", qcd)),
  fEWK(new ControlPlot("EWK", ewk)),
  fFakes(new ControlPlot("EWKfakesfakes", fakes)),
  fHH(new ControlPlot("HH", hh)),
  fHW(new ControlPlot("HW", hw)),
  fData(new ControlPlot("Data", data)) {
  for (int i = 1; i <= hFrame->GetNbinsX(); ++i) {
    fQCDRelativeSystematicUncertainty.push_back(0.);
    fEWKRelativeSystematicUncertainty.push_back(0.);
    fFakesRelativeSystematicUncertainty.push_back(0.);
    fHHRelativeSystematicUncertainty.push_back(0.);
    fHWRelativeSystematicUncertainty.push_back(0.);
  }
}

Manager::~Manager() { }

void Manager::getIntegral(double& nqcd, double& newk, double& nfakes, double& nhh, double& nhw, double &ndata, double min, double max) {
  nqcd = 0.;
  newk = 0.;
  nfakes = 0.;
  nhh = 0.;
  nhw = 0.;
  ndata = 0.;
  int nbins = fQCD->getPlot()->GetNbinsX();
  for (int i = 0; i <= nbins+1; ++i) {
    if ((min < 0 || fQCD->getPlot()->GetXaxis()->GetBinLowEdge(i) >= min) && (max < 0 || fQCD->getPlot()->GetXaxis()->GetBinUpEdge(i) <= max)) {
      nqcd += fQCD->getPlot()->GetBinContent(i);
      newk += fEWK->getPlot()->GetBinContent(i);
      nfakes += fFakes->getPlot()->GetBinContent(i);
      nhh += fHH->getPlot()->GetBinContent(i);
      nhw += fHW->getPlot()->GetBinContent(i);
      ndata += fData->getPlot()->GetBinContent(i);
    }
  }
}

void Manager::getIntegralUncert(double& nqcd, double& newk, double& nfakes, double& nhh, double& nhw, double& ndata, double min, double max) {
  nqcd = 0.;
  newk = 0.;
  nfakes = 0.;
  nhh = 0.;
  nhw = 0.;
  ndata = 0.;
  int nbins = fQCD->getPlot()->GetNbinsX();
  for (int i = 0; i <= nbins+1; ++i) {
    if ((min < 0 || fQCD->getPlot()->GetXaxis()->GetBinLowEdge(i) >= min) && (max < 0 || fQCD->getPlot()->GetXaxis()->GetBinUpEdge(i) <= max)) {
      nqcd += TMath::Power(fQCD->getPlot()->GetBinError(i),2);
      newk += TMath::Power(fEWK->getPlot()->GetBinError(i),2);
      nfakes += TMath::Power(fFakes->getPlot()->GetBinError(i),2);
      nhh += TMath::Power(fHH->getPlot()->GetBinError(i),2);
      nhw += TMath::Power(fHW->getPlot()->GetBinError(i),2);
      ndata += TMath::Power(fData->getPlot()->GetBinError(i),2);
    }
  }
  nqcd = TMath::Sqrt(nqcd);
  newk = TMath::Sqrt(newk);
  nfakes = TMath::Sqrt(nfakes);
  nhh = TMath::Sqrt(nhh);
  nhw = TMath::Sqrt(nhw);
  ndata = TMath::Sqrt(ndata);
}

void Manager::setNormalisationInfo(string configInfo, string qcdCounter, string ewkCounter, string fakeCounter, string signalCounter, double lumiPb) {
  fData->setNormalisationInfo(configInfo, signalCounter, lumiPb);
  fQCD->setNormalisationInfo(configInfo, qcdCounter, lumiPb);
  fEWK->setNormalisationInfo(configInfo, ewkCounter, lumiPb);
  fFakes->setNormalisationInfo(configInfo, fakeCounter, lumiPb);
  fHH->setNormalisationInfo(configInfo, signalCounter, lumiPb);
  fHW->setNormalisationInfo(configInfo, signalCounter, lumiPb);
  cout << "Normalisation info set for " << sLabel << " (lumi = " << lumiPb << " 1/pb)" << endl;
}

void Manager::printInfo(TH1* h, string label) {
  double n = 0;
  double nerr = 0;
  for (int i = 0; i <= h->GetNbinsX()+1; ++i) {
    n += h->GetBinContent(i);
    nerr += TMath::Power(h->GetBinError(i),2);
  }
  cout << label << ": events: " << n << " +- " << TMath::Sqrt(nerr) << endl;
}

bool Manager::extract(std::vector< TFile* >& qcdData, std::vector< TFile* >& qcdMCEWK, std::vector< TFile* >& ewkData, std::vector< TFile* >& fakes, std::vector< TFile* >& hh, std::vector< TFile* >& hw, std::vector< TFile* >& signalData) {
  // Make plots
  vector<TFile*> myDummyList;
  if (!fQCD->extract(qcdData, qcdMCEWK, hFrame)) return false;
  printInfo(fQCD->getPlot(), "QCD");
  if (!fEWK->extract(ewkData, myDummyList, hFrame)) return false;
  printInfo(fEWK->getPlot(), "EWK");
  if (!fFakes->extract(myDummyList, fakes, hFrame)) return false;
  printInfo(fFakes->getPlot(), "Fakes");
  if (!fHH->extract(myDummyList, hh, hFrame)) return false;
  printInfo(fHH->getPlot(), "HH");
  if (!fHW->extract(myDummyList, hw, hFrame)) return false;
  printInfo(fHW->getPlot(), "HW");
  if (!fData->extract(signalData, myDummyList, hFrame)) return false;
  printInfo(fData->getPlot(), "Data");
  return true;
}

void Manager::setRelativeUncertainty(int bin, double QCDUncert, double EWKUncert, double fakesUncert, double HHUncert, double HWUncert) {
  if (bin < 0) {
    // Fill same uncert for each bin
    for (int i = 0; i < fQCD->getPlot()->GetNbinsX(); ++i) {
      fQCDRelativeSystematicUncertainty[i] = QCDUncert;
      fEWKRelativeSystematicUncertainty[i] = EWKUncert;
      fFakesRelativeSystematicUncertainty[i] = fakesUncert;
      fHHRelativeSystematicUncertainty[i] = HHUncert;
      fHWRelativeSystematicUncertainty[i] = HWUncert;
    }
  } else {
    if (bin > hFrame->GetNbinsX()) {
      cout << "Error: when setting relative uncertainty, use a bin that is smaller than the frame bin size (" << sLabel << ")" << endl;
      return;
    }
    // Fill uncert for a specific bin
    fQCDRelativeSystematicUncertainty[bin-1] = QCDUncert;
    fEWKRelativeSystematicUncertainty[bin-1] = EWKUncert;
    fFakesRelativeSystematicUncertainty[bin-1] = fakesUncert;
    fHHRelativeSystematicUncertainty[bin-1] = HHUncert;
    fHWRelativeSystematicUncertainty[bin-1] = HWUncert;
  }
}

void Manager::makePlot(double xmin, double xmax, double ymin, double ymax, double delta, string xtitle, string ytitle, double br, double mass, bool logy) {
  cout << endl << "Making plots for " << sLabel << endl;
  stringstream s;
  // Make canvas
  TCanvas* c = new TCanvas(sLabel.c_str(), sLabel.c_str(), 600, 600);
  gStyle->SetOptFit(1);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  gStyle->SetTitleFont(43, "xyz");
  gStyle->SetTitleSize(33, "xyz");
  gStyle->SetLabelFont(43, "xyz");
  gStyle->SetLabelSize(27, "xyz");

  c->SetLogy();
  c->SetHighLightColor(2);
  c->Range(0,0,1,1);
  //c->Range(-81.01265,-3.836876,425.3165,2.600629);
  c->SetFillColor(0);
  c->SetBorderMode(0);
  c->SetBorderSize(2);
  c->SetTickx(1);
  c->SetTicky(1);
  c->SetLeftMargin(0.16);
  c->SetRightMargin(0.05);
  c->SetTopMargin(0.05);
  c->SetBottomMargin(0.8);
  c->SetFrameFillStyle(0);
  c->SetFrameBorderMode(0);
  c->SetFrameFillStyle(0);
  c->SetFrameBorderMode(0);
  // Set minimum and maximum
  hFrame->SetMinimum(ymin);
  hFrame->SetMaximum(ymax);
  hFrame->GetXaxis()->SetRangeUser(xmin, xmax);
  //hFrame->SetAxisRange(xmin, xmax, "x");
  hFrame->SetTitleSize(0.05, "x");
  hFrame->GetYaxis()->SetLabelSize(27);
  //hFrame->GetYaxis()->SetTitleSize(27);
  hFrame->GetYaxis()->SetLabelFont(43);
  hFrame->GetYaxis()->SetLabelOffset(0.007);
  // Get plots
  int ci = 0;
  TH1* hQCD = fQCD->getPlot();
  ci = TColor::GetColor("#ffcc33");
  hQCD->SetFillColor(ci);
  hQCD->SetLineWidth(0);
  TH1* hEWK = fEWK->getPlot();
  ci = TColor::GetColor("#993399");
  hEWK->SetFillColor(ci);
  hEWK->SetLineWidth(0);
  TH1* hFakes = fFakes->getPlot();
  ci = TColor::GetColor("#669900");
  hFakes->SetFillColor(ci);
  hFakes->SetLineWidth(0);
  TH1* hHH = fHH->getPlot();
  TH1* hHW = fHW->getPlot();
  //hHH->Scale(TMath::Power(br,2));
  //hHW->Scale((1.0 - br)*br*2.0);
  TH1* hData = fData->getPlot();
  hData->SetLineWidth(2);
  hData->SetMarkerStyle(20);
  hData->SetMarkerSize(1.2);
  // Make stacks
  TH1* hSignal = dynamic_cast<TH1*>(hHH->Clone());
  hSignal->Scale(TMath::Power(br,2));
  cout << "hh unscaled: " << hHH->Integral() << endl;
  cout << "hh scaled:"  << hSignal->Integral() << endl;
  hSignal->Add(hHW, (1.0 - br)*br*2.0);
  cout << "signal: " << hSignal->Integral() << endl;
  ci = TColor::GetColor("#ff3399");
  hSignal->SetLineColor(ci);
  hSignal->SetLineStyle(2);
  hSignal->SetLineWidth(2);
  THStack* hBkg = new THStack();
  hBkg->Add(hFakes);
  hBkg->Add(hEWK);
  hBkg->Add(hQCD);
  hBkg->Add(hSignal);
  TH1* hBkgUncert = dynamic_cast<TH1*>(hEWK->Clone());
  hBkgUncert->Add(hFakes);
  hBkgUncert->Add(hQCD);
  hBkgUncert->SetFillColor(1);
  hBkgUncert->SetFillStyle(3354); // FIXME 3354
  hBkgUncert->SetLineColor(0);
  hBkgUncert->SetLineStyle(0);
  hBkgUncert->SetLineWidth(0);
  // Set new x axis
  hSignal->GetXaxis()->SetRangeUser(xmin, xmax);
  hFakes->GetXaxis()->SetRangeUser(xmin, xmax);
  hEWK->GetXaxis()->SetRangeUser(xmin, xmax);
  hQCD->GetXaxis()->SetRangeUser(xmin, xmax);
  hBkgUncert->GetXaxis()->SetRangeUser(xmin, xmax);
  hData->GetXaxis()->SetRangeUser(xmin, xmax);
  // Data vs mc 
  TH1* hAgreement = dynamic_cast<TH1*>(hData->Clone());
  hAgreement->Divide(hBkgUncert);
  // Relative uncertainty
  bool bRelUncertInUse = false;
  TH1* hBkgRelUncert = dynamic_cast<TH1*>(hBkgUncert->Clone());
  TGraphErrors* hAgreementRelUncert = new TGraphErrors(hFrame->GetNbinsX());
  if (fEWKRelativeSystematicUncertainty[0] > 0) {
    bRelUncertInUse = true;
    hBkgUncert->SetFillStyle(3344);
    hAgreementRelUncert->SetLineWidth(2);
    for (int i = 1; i <= hFrame->GetNbinsX(); ++i) {
      double myQCDTotalUncert = TMath::Power(hQCD->GetBinError(i), 2)
        + TMath::Power(hQCD->GetBinContent(i)*fQCDRelativeSystematicUncertainty[i-1], 2);
      double myEWKTotalUncert = TMath::Power(hEWK->GetBinError(i), 2)
        + TMath::Power(hEWK->GetBinContent(i)*fEWKRelativeSystematicUncertainty[i-1], 2);
      double myFakesTotalUncert = TMath::Power(hFakes->GetBinError(i), 2)
        + TMath::Power(hFakes->GetBinContent(i)*fFakesRelativeSystematicUncertainty[i-1], 2);
      hBkgRelUncert->SetBinError(i, TMath::Sqrt(myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert));

      if (hBkgUncert->GetBinContent(i) > 0) {
        hAgreementRelUncert->SetPoint(i-1, hBkgUncert->GetBinCenter(i), hData->GetBinContent(i) / hBkgUncert->GetBinContent(i));
        double myUncertData = 0;
        if (hData->GetBinContent(i) > 0)
          myUncertData = TMath::Power(hData->GetBinError(i) / hData->GetBinContent(i), 2);
        double myUncertBkg = (myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert) / TMath::Power(hBkgUncert->GetBinContent(i), 2);
        hAgreementRelUncert->SetPointError(i-1, 0,  hData->GetBinContent(i) / hBkgUncert->GetBinContent(i) * TMath::Sqrt(myUncertData + myUncertBkg));
      } else {
        hAgreementRelUncert->SetPoint(i-1, hBkgUncert->GetBinCenter(i), 0);
        hAgreementRelUncert->SetPointError(i-1, 0, 0);
      }
      cout << "point: " << hAgreementRelUncert->GetX()[i-1] << ", " << hAgreementRelUncert->GetY()[i-1] << ", uncert: " << hAgreementRelUncert->GetErrorX(i-1) << ", " << hAgreementRelUncert->GetErrorY(i-1) << endl;
      cout << "  bkg. stat. uncert. " << hBkgUncert->GetBinError(i) << ", stat+syst uncert. " << TMath::Sqrt(myQCDTotalUncert + myEWKTotalUncert + myFakesTotalUncert) << endl;
      
    }
  }

  // Agreement pad
  s << sLabel << "_pad";
  TPad* pad = new TPad(s.str().c_str(),s.str().c_str(),0.,0.,1.,.3);
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
  hAgreement->SetTitleSize(27, "xyz");
  hAgreement->GetXaxis()->SetTitleOffset(3.2);
  hAgreement->GetYaxis()->SetTitleOffset(1.3);
  hAgreement->SetXTitle(xtitle.c_str());
  hAgreement->SetYTitle("Data/#Sigmabkg");
  hAgreement->Draw("e2");
  // Plot line at zero
  TH1* hAgreementLine = dynamic_cast<TH1*>(hFrame->Clone());
  for (int i = 1; i <= hAgreementLine->GetNbinsX(); ++i) {
    hAgreementLine->SetBinContent(i,1.0);
    hAgreementLine->SetBinError(i,0.0);
  }
  hAgreementLine->SetLineColor(kRed);
  hAgreementLine->SetLineWidth(2);
  hAgreementLine->SetLineStyle(3);
  hAgreementLine->Draw("hist same");
  hAgreement->Draw("same");
  if (bRelUncertInUse)
    hAgreementRelUncert->Draw("[]");
  pad->RedrawAxis();
  
  // ylempi pad x-akseli label size ja title size 0
  
  // coverpad
  c->cd();
  TPad* coverpad = new TPad("coverpad", "coverpad",0.105,0.300,0.155,0.36);
  coverpad->Draw();
  coverpad->cd();
  coverpad->Range(0,0,1,1);
  coverpad->SetFillColor(0);
  coverpad->SetBorderMode(0);
  coverpad->SetBorderSize(2);
  coverpad->SetTickx(1);
  coverpad->SetTicky(1);
  coverpad->SetLeftMargin(0.16);
  coverpad->SetRightMargin(0.05);
  coverpad->SetTopMargin(0.05);
  coverpad->SetBottomMargin(0.13);
  coverpad->SetFrameFillStyle(0);
  coverpad->SetFrameBorderMode(0);
  coverpad->Modified();
  c->cd();
  
  //controlPlots_SelectedTau_eta_AfterStandardSelections_log->cd();
  
  // plot pad
  TPad* plotpad = new TPad("plotpad", "plotpad",0,0.3,1.,1.);
  plotpad->Draw();
  plotpad->cd();
  plotpad->Range(0,0,1,1);
  plotpad->SetFillColor(0);
  plotpad->SetFillStyle(4000);
  plotpad->SetBorderMode(0);
  plotpad->SetBorderSize(2);
  if (logy)
    plotpad->SetLogy();
  plotpad->SetTickx(1);
  plotpad->SetTicky(1);
  plotpad->SetLeftMargin(0.16);
  plotpad->SetRightMargin(0.05);
  plotpad->SetTopMargin(0.065);
  plotpad->SetBottomMargin(0.0);
  plotpad->SetFrameFillStyle(0);
  plotpad->SetFrameBorderMode(0);
  plotpad->SetFrameFillStyle(0);
  plotpad->SetFrameBorderMode(0);
  hFrame->GetXaxis()->SetTitleSize(0);
  hFrame->GetXaxis()->SetLabelSize(0);
  hFrame->GetYaxis()->SetTitleFont(43);
  hFrame->GetYaxis()->SetTitleSize(27);
  hFrame->GetYaxis()->SetTitleOffset(1.3);
  hFrame->SetYTitle(ytitle.c_str());

  // Draw
  hFrame->Draw();
  hBkg->Draw("hist same");
  hBkgUncert->Draw("E2 same");
  if (bRelUncertInUse)
    hBkgRelUncert->Draw("E2 same");
  hData->Draw("same");


  // Legend
  TLegend *leg = new TLegend(0.53,0.63,0.87,0.91,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(63);
  leg->SetTextSize(18);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(4000);
  TLegendEntry* entry = leg->AddEntry(hData, "Data", "P");
  s.str("");
  s << "with H^{#pm}#rightarrow#tau^{#pm}#nu";
  entry = leg->AddEntry(hSignal, s.str().c_str(), "L");
  entry = leg->AddEntry(hQCD, "QCD (meas.)", "F");
  entry = leg->AddEntry(hEWK, "EWK genuine #tau (meas.)", "F");
  entry = leg->AddEntry(hFakes, "EWK fake #tau (MC)", "F");
  entry = leg->AddEntry(hBkgUncert, "stat. uncert.", "F");
  if (bRelUncertInUse)
    entry = leg->AddEntry(hBkgRelUncert, "stat. #oplus syst. uncert.", "F");
  leg->Draw();

  TLatex* tex = new TLatex(0.62,0.945,"CMS Preliminary");
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
  tex = new TLatex(0.43,0.945,"2.2 fb^{-1}");
  tex->SetNDC();
  tex->SetTextFont(43);
  tex->SetTextSize(27);
  tex->SetLineWidth(2);
  tex->Draw();
  tex = new TLatex(0.28,0.865,"m_{H^{#pm}} = 120 GeV/c^{2}");
  tex->SetNDC();
  tex->SetTextFont(63);
  tex->SetTextSize(20);
  tex->SetLineWidth(2);
  tex->Draw();
  tex = new TLatex(0.28,0.805,"BR(t#rightarrowbH^{#pm})=0.05");
  tex->SetNDC();
  tex->SetTextFont(63);
  tex->SetTextSize(20);
  tex->SetLineWidth(2);
  tex->Draw();
  
  plotpad->RedrawAxis();

  s.str("");
  s << "dataDrivenControlPlot_" << sLabel << mass << ".png";
  c->Print(s.str().c_str());
  s.str("");
  s << "dataDrivenControlPlot_" << sLabel << mass << ".C";
  c->Print(s.str().c_str());
  s.str("");
  s << "dataDrivenControlPlot_" << sLabel << mass << ".eps";
  c->Print(s.str().c_str());
}

void addEntryToSelectionFlow(Manager* m, int bin, TH1* hqcd, TH1* hewk, TH1* hfakes, TH1* hhh, TH1* hhw, TH1* hdata, double min, double max) {
  double nQCD = 0;
  double nEWK = 0;
  double nFakes = 0;
  double nHH = 0;
  double nHW = 0;
  double nData = 0;
  // Get event counts
  m->getIntegral(nQCD, nEWK, nFakes, nHH, nHW, nData, min, max);
  hqcd->SetBinContent(bin, nQCD);
  hewk->SetBinContent(bin, nEWK);
  hfakes->SetBinContent(bin, nFakes);
  hhh->SetBinContent(bin, nHH);
  hhw->SetBinContent(bin, nHW);
  hdata->SetBinContent(bin, nData);
  // Get stat. uncertainty
  m->getIntegralUncert(nQCD, nEWK, nFakes, nHH, nHW, nData, min, max);
  hqcd->SetBinError(bin, nQCD);
  hewk->SetBinError(bin, nEWK);
  hfakes->SetBinError(bin, nFakes);
  hhh->SetBinError(bin, nHH);
  hhw->SetBinError(bin, nHW);
  hdata->SetBinError(bin, nData);
}

int main() {
  int myMassPoint = 120;
  
  // Define data sample names
  vector<string> myDataNames;
  myDataNames.push_back("Tau_160431-161176_May10");
  myDataNames.push_back("Tau_161217-163261_May10");
  myDataNames.push_back("Tau_163270-163869_May10");
  myDataNames.push_back("Tau_165088-165633_Prompt");
  myDataNames.push_back("Tau_165970-166164_Prompt");
  myDataNames.push_back("Tau_166346-166346_Prompt");
  myDataNames.push_back("Tau_166374-167043_Prompt");
  myDataNames.push_back("Tau_167078-167913_Prompt");
  myDataNames.push_back("Tau_170722-172619_Aug05");
  myDataNames.push_back("Tau_172620-173198_Prompt");
  myDataNames.push_back("Tau_173236-173692_Prompt");
  vector<string> myEWKDataNames;
  /*
  myEWKDataNames.push_back("SingleMu_Mu_160431-163261_May10");
  myEWKDataNames.push_back("SingleMu_Mu_163270-163869_May10");
  myEWKDataNames.push_back("SingleMu_Mu_165088-166150_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_166161-166164_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_166346-166346_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_166374-167043_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_167078-167913_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_170722-172619_Aug05");
  myEWKDataNames.push_back("SingleMu_Mu_172620-173198_Prompt");
  myEWKDataNames.push_back("SingleMu_Mu_173236-173692_Prompt");
  */
  myEWKDataNames.push_back("Data");
  myEWKDataNames.push_back("DYJetsToLL_M50_TuneZ2_Summer11"); // residual (normal - embedded)
  myEWKDataNames.push_back("WW_TuneZ2_Summer11"); // residual (normal - embedded)
  // Define EWK MC sample namespace
  vector<string> myMCEWKNames;
  myMCEWKNames.push_back("TTJets_TuneZ2_Summer11");
  myMCEWKNames.push_back("WJets_TuneZ2_Summer11");
  myMCEWKNames.push_back("DYJetsToLL_M50_TuneZ2_Summer11");
  myMCEWKNames.push_back("T_s-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("Tbar_s-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("T_t-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("Tbar_t-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("T_tW-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("Tbar_tW-channel_TuneZ2_Summer11");
  myMCEWKNames.push_back("WW_TuneZ2_Summer11");
  myMCEWKNames.push_back("WZ_TuneZ2_Summer11");
  myMCEWKNames.push_back("ZZ_TuneZ2_Summer11");
  // Define MC signals
  stringstream s;
  vector<string> mySignalHHNames;
  s << "TTToHplusBHminusB_M" << myMassPoint << "_Summer11";
  mySignalHHNames.push_back(s.str());
  vector<string> mySignalHWNames;
  s.str("");
  s << "TTToHplusBWB_M" << myMassPoint << "_Summer11";
  mySignalHWNames.push_back(s.str());
  
  // Open files
  vector<TFile*> myQCDDataFiles = openFiles("qcdpath", myDataNames);
  vector<TFile*> myQCDMCEWKFiles = openFiles("qcdpath", myMCEWKNames);
  vector<TFile*> myEWKDataFiles = openFiles("ewkpath", myEWKDataNames);
  vector<TFile*> myEWKFakeFiles = openFiles("fakespath", myMCEWKNames);
  vector<TFile*> mySignalHHFiles = openFiles("signalpath", mySignalHHNames);
  vector<TFile*> mySignalHWFiles = openFiles("signalpath", mySignalHWNames);
  vector<TFile*> myDataFiles = openFiles("signalpath", myDataNames);
  if (myQCDDataFiles.size() != myDataNames.size() ||
      myEWKDataFiles.size() != myEWKDataNames.size() ||
      myQCDMCEWKFiles.size() != myMCEWKNames.size() ||
      myEWKFakeFiles.size() != myMCEWKNames.size() ||
      mySignalHHNames.size() != mySignalHHFiles.size() ||
      mySignalHWNames.size() != mySignalHWFiles.size() ||
      myDataFiles.size() != myDataNames.size())
    return -1;
  // Empty list
  vector<TFile*> myEmptyFiles;
  
  double myLuminosityInPb = 2177.9;
  double myBr = 0.05;
  
  string QCDprefix = "QCDMeasurement/QCDMeasurementVariation_METcut50_DeltaPhiTauMETCut160_tauIsol1/";
  string EWKprefix = "signalAnalysis/ControlPlots/";
  string signalprefix = "signalAnalysis/ControlPlots/";
  string configInfo = "configInfo/configinfo";
  
  double EWKeff1 = 1.0; // no longer needed
  double EWKeff2 = 1.0; // no longer needed
  
  vector<Manager*> myManagers;
  
  // tau pT

  TH1D* myTauPtFrame = new TH1D("tauPt","tauPt",40,0,400);
  QCDControlPlot myTauPtQCD(QCDprefix+"ControlPlots/SelectedTau_pT_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myTauPtEWK(EWKprefix+"SelectedTau_pT_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myTauPt = new Manager("TauPt", myTauPtFrame, &myTauPtQCD, &myTauPtEWK, signalprefix+"SelectedTau_pT_AfterStandardSelections", signalprefix+"SelectedTau_pT_AfterStandardSelections");
  myManagers.push_back(myTauPt);
  // tau eta
  TH1D* myTauEtaFrame = new TH1D("TauEta","TauEta",30,-3.,3.);
  QCDControlPlot myTauEtaQCD(QCDprefix+"ControlPlots/SelectedTau_eta_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myTauEtaEWK(EWKprefix+"SelectedTau_eta_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myTauEta = new Manager("TauEta", myTauEtaFrame, &myTauEtaQCD, &myTauEtaEWK, signalprefix+"SelectedTau_eta_AfterStandardSelections", signalprefix+"SelectedTau_eta_AfterStandardSelections");
  myManagers.push_back(myTauEta);
  // tau phi
  /*TH1D* myTauPhiFrame = new TH1D("TauPhi","TauPhi",18,0.,180.);
  QCDControlPlot myTauPhiQCD(QCDprefix+"ControlPlots/SelectedTau_phi_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myTauPhiEWK(EWKprefix+"SelectedTau_phi_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myTauPhi = new Manager("TauPhi", myTauPhiFrame, &myTauPhiQCD, &myTauPhiEWK, signalprefix+"SelectedTau_phi_AfterStandardSelections", signalprefix+"SelectedTau_phi_AfterStandardSelections");
  myManagers.push_back(myTauPhi);*/
  // rtau
  TH1D* myTauRtauFrame = new TH1D("TauRtau","TauRtau",24,0.,1.2);
  QCDControlPlot myTauRtauQCD(QCDprefix+"ControlPlots/SelectedTau_Rtau_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myTauRtauEWK(EWKprefix+"SelectedTau_Rtau_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myTauRtau = new Manager("TauRtau", myTauRtauFrame, &myTauRtauQCD, &myTauRtauEWK, signalprefix+"SelectedTau_Rtau_AfterStandardSelections", signalprefix+"SelectedTau_Rtau_AfterStandardSelections");
  myManagers.push_back(myTauRtau);
  // leading track pt
  TH1D* myTauLeadingTrackPtFrame = new TH1D("TauLeadingTrackPt","TauLeadingTrackPt",40,0.,400.);
  QCDControlPlot myTauLeadingTrackPtQCD(QCDprefix+"ControlPlots/SelectedTau_LeadingTrackPt_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myTauLeadingTrackPtEWK(EWKprefix+"SelectedTau_LeadingTrackPt_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myTauLeadingTrackPt = new Manager("TauLeadingTrackPt", myTauLeadingTrackPtFrame, &myTauLeadingTrackPtQCD, &myTauLeadingTrackPtEWK, signalprefix+"SelectedTau_LeadingTrackPt_AfterStandardSelections", signalprefix+"SelectedTau_LeadingTrackPt_AfterStandardSelections");
  myManagers.push_back(myTauLeadingTrackPt);
  // identified electron pt
  TH1D* myElectronPtFrame = new TH1D("ElectronPt","ElectronPt",20,0.,20.);
  QCDControlPlot myElectronPtQCD(QCDprefix+"ControlPlots/IdentifiedElectronPt_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myElectronPtEWK(EWKprefix+"IdentifiedElectronPt_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myElectronPt = new Manager("ElectronPt", myElectronPtFrame, &myElectronPtQCD, &myElectronPtEWK, signalprefix+"IdentifiedElectronPt_AfterStandardSelections", signalprefix+"IdentifiedElectronPt_AfterStandardSelections");
  myManagers.push_back(myElectronPt);
  // identified muon pt
  TH1D* myMuonPtFrame = new TH1D("MuonPt","MuonPt",20,0.,20.);
  QCDControlPlot myMuonPtQCD(QCDprefix+"ControlPlots/IdentifiedMuonPt_AfterStandardSelections_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myMuonPtEWK(EWKprefix+"IdentifiedMuonPt_AfterStandardSelections", EWKeff1*EWKeff2);
  Manager* myMuonPt = new Manager("MuonPt", myMuonPtFrame, &myMuonPtQCD, &myMuonPtEWK, signalprefix+"IdentifiedMuonPt_AfterStandardSelections", signalprefix+"IdentifiedMuonPt_AfterStandardSelections");
  myManagers.push_back(myMuonPt);

  // btag
  TH1D* myNjetsFrame = new TH1D("jets","jets",10,0,10); // FIXME
  QCDControlPlot myNjetsQCD(QCDprefix+"ControlPlots/Njets_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myNjetsEWK(EWKprefix+"Njets", EWKeff1*EWKeff2);
  Manager* myNjets = new Manager("Njets", myNjetsFrame, &myNjetsQCD, &myNjetsEWK, signalprefix+"Njets", signalprefix+"Njets");
  myManagers.push_back(myNjets);

  // MET
  TH1D* myMetFrame = new TH1D("MET","MET",20,0,500);
  QCDControlPlot myMetQCD(QCDprefix+"ControlPlots/MET_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myMetEWK(EWKprefix+"MET", EWKeff1*EWKeff2);
  Manager* myMet = new Manager("MET", myMetFrame, &myMetQCD, &myMetEWK, signalprefix+"MET", signalprefix+"MET");
  myManagers.push_back(myMet);
  
  // btag
  TH1D* myNBjetsFrame = new TH1D("btag","btag",10,0,10); // FIXME
  QCDControlPlot myNBjetsQCD(QCDprefix+"ControlPlots/NBjets_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myNBjetsEWK(EWKprefix+"NBjets", EWKeff1*EWKeff2);
  Manager* myNBjets = new Manager("NBjets", myNBjetsFrame, &myNBjetsQCD, &myNBjetsEWK, signalprefix+"NBjets", signalprefix+"NBjets");
  myManagers.push_back(myNBjets);
  
  // delta phi
  TH1D* myDeltaPhiFrame = new TH1D("deltaphi","deltaphi",9,0,180);
  QCDControlPlot myDeltaPhiQCD(QCDprefix+"ControlPlots/DeltaPhi_taupT", true, "QCDMeasurement/QCDStandardSelections/AfterJetSelection", QCDprefix+"Leg2AfterTauIDWithRtau");
  EWKControlPlot myDeltaPhiEWK("signalAnalysis/deltaPhi", EWKeff1*EWKeff2);
  Manager* myDeltaPhi = new Manager("DeltaPhi", myDeltaPhiFrame, &myDeltaPhiQCD, &myDeltaPhiEWK, "signalAnalysis/deltaPhi", "signalAnalysis/deltaPhi");
  myManagers.push_back(myDeltaPhi);
  
  // Do normalisation
  for (size_t i = 0; i < myManagers.size(); ++i) {
    myManagers[i]->setNormalisationInfo(configInfo, "QCDMeasurementCounters/weighted/counter",
                                        "signalAnalysisCounters/weighted/counter",
                                        "signalAnalysisCounters/weighted/counter",
                                        "signalAnalysisCounters/weighted/counter", myLuminosityInPb);
  }
  // Extract plots
  for (size_t i = 0; i < myManagers.size(); ++i) {
    cout << endl << myManagers[i]->getLabel() << endl;
    if (!myManagers[i]->extract(myQCDDataFiles, myQCDMCEWKFiles, myEWKDataFiles, myEWKFakeFiles, mySignalHHFiles, mySignalHWFiles, myDataFiles))
      return -1;
  }
  // Make plots 
  myTauPt->makePlot(40, 249, 8e-2, 5e2, 1.2, "#tau-jet p_{T} (GeV/c)", "Events / 10 GeV/c", myBr, myMassPoint);
  myTauEta->makePlot(-2.3, 2.3, 8e-2, 9e2, 0.9, "#tau-jet #eta", "Events / 0.2", myBr, myMassPoint);
  //myTauPhi->makePlot(0, 180, 5e-1, 2e2, 0.5, "#tau #phi, ^{o}", "Events / 10^{o}", myBr, myMassPoint);
  myTauRtau->makePlot(0.0, 1.04, 5e-2, 5e4, 0.3, "#tau-jet R_{#tau}", "Events / 0.1", myBr, myMassPoint);
  myTauLeadingTrackPt->makePlot(20, 249, 5e-2, 1e3, 0.5, "#tau-jet leading charged particle p_{T} (GeV/c)", "Events / 10 GeV/c", myBr, myMassPoint);
  myElectronPt->makePlot(0, 250, 5e-3, 1e3, 0.5, "Identified isolated electron p_{T}, GeV/c", "Events / 2 GeV/c", myBr, myMassPoint);
  myMuonPt->makePlot(0, 250, 5e-3, 1e3, 0.5, "Identified isolated muon p_{T}, GeV/c", "Events / 2 GeV/c", myBr, myMassPoint);
  myMet->makePlot(0, 449, 2e-2, 5e2, 0.7, "Uncorrected PF E_{T}^{miss} (GeV)", "Events / 25 GeV", myBr, myMassPoint);
  myNjets->makePlot(3, 7.9, 5e-3, 5e3, 0.7, "Number of selected jets", "Events", myBr, myMassPoint);
  myNBjets->makePlot(0, 4.9, 2e-1, 1.1e3, 0.5, "Number of selected b jets", "Events", myBr, myMassPoint);
  myDeltaPhi->makePlot(0, 180, 2e-1, 2e2, 1.8, "#Delta#phi(#tau jet, E_{T}^{miss}) (^{o})", "Events / 20^{o}", myBr, myMassPoint);

  // Make selection flow plot
  int nbins = 5;
  TH1* hSelectionFlowFrame = new TH1D("SelectionFlow","SelectionFlow",nbins,0,nbins);
  hSelectionFlowFrame->GetXaxis()->SetBinLabel(1, "N_{jets}");
  hSelectionFlowFrame->GetXaxis()->SetBinLabel(2, "E_{T}^{miss}");
  hSelectionFlowFrame->GetXaxis()->SetBinLabel(3, "N_{b jets}");
  hSelectionFlowFrame->GetXaxis()->SetBinLabel(4, "#Delta#phi<160^{o}");
  if (nbins >= 5)
    hSelectionFlowFrame->GetXaxis()->SetBinLabel(5, "#Delta#phi<130^{o}");
  TH1* hSelectionFlowQCD = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowQCD"));
  TH1* hSelectionFlowEWK = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowEWK"));
  TH1* hSelectionFlowFakes = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowFakes"));
  TH1* hSelectionFlowHH = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowHH"));
  TH1* hSelectionFlowHW = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowHW"));
  TH1* hSelectionFlowData = dynamic_cast<TH1*>(hSelectionFlowFrame->Clone("SelectionFlowData"));
  addEntryToSelectionFlow(myMet,1,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData, -1, -1);
  addEntryToSelectionFlow(myNBjets,2,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData, -1, -1);
  addEntryToSelectionFlow(myDeltaPhi,3,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData, -1, -1);
  addEntryToSelectionFlow(myDeltaPhi,4,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData, 0., 160.);
  if (nbins >= 5)
    addEntryToSelectionFlow(myDeltaPhi,5,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData, 0., 130.);
  Manager* mySelectionFlow = new Manager("SelectionFlow",hSelectionFlowFrame,hSelectionFlowQCD,hSelectionFlowEWK,hSelectionFlowFakes,hSelectionFlowHH,hSelectionFlowHW,hSelectionFlowData);
  mySelectionFlow->setRelativeUncertainty(-1, 0.038, 0.131, 0.241, 0., 0.); // removing btag uncertainty makes very little difference
  mySelectionFlow->makePlot(0, nbins, 1, 2e3*1.5, 0.3, "", "Events", myBr, myMassPoint, !false);
  /*
  TFile* myOutFile = TFile::Open("controlPlots.root","RECREATE");
  myOutFile->cd();
  myTauPtQCD.getPlot()->Clone();
  myOutFile->Write();
  myOutFile->Close();
  
  cout << "Written file controlPlots.root" << endl;
  */
  return 0;
}
