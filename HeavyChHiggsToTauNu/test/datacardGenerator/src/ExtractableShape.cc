#include "ExtractableShape.h"
#include <iostream>
#include <sstream>

#include "TMath.h"
#include "TH1F.h"

ExtractableShape::ExtractableShape(std::string id, std::string distribution, std::string description,
                                   std::string histoName, std::string upPrefix, std::string downPrefix)
: Extractable(id, distribution, description),
  sHistoName(histoName),
  sUpPrefix(upPrefix),
  sDownPrefix(downPrefix) {
  hUp = new TH1F("hup","hup",20,0,400);
  hUp->Sumw2();
  hDown = new TH1F("hdown","hdown",20,0,400);
  hDown->Sumw2();
}

ExtractableShape::~ExtractableShape() {
  
}

double ExtractableShape::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info, double additionalNormalisation) {
  for (int i = 0; i <= hDown->GetNbinsX()+1; ++i) { 
    hUp->SetBinContent(i,0);
    hUp->SetBinError(i,0);
    hDown->SetBinContent(i,0);
    hDown->SetBinError(i,0);
  }

  // Loop over histograms to obtain result
  //double fCounterValue = 0.; // result in number of events
  for (size_t i = 0; i < datasets.size(); ++i) {
    std::stringstream s;
    s << sUpPrefix+"/"+sHistoName;
    TH1* h = dynamic_cast<TH1*>(datasets[i]->getFile()->Get(s.str().c_str()));
    //TH1* h = dynamic_cast<TH1*>(myPlot->Clone());
    if (!h) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not find histogram " << s.str() << " in file " << datasets[i]->getFilename() << "!" << std::endl;
      return -1.;
    }
    // Rebin
    if (h->GetNbinsX() > hUp->GetNbinsX()) {
      //std::cout << "bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
      h->Rebin(h->GetNbinsX() / hUp->GetNbinsX());
      //std::cout << "new bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
    } else if (h->GetNbinsX() < hUp->GetNbinsX()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m You asked for " << hUp->GetNbinsX() << ", but the mT histogram " << s.str() << " has only " << h->GetNbinsX() << " bins!" << std::endl;
    }
    // Set negative bins to zero prior to normalisation (occurs in EWK residual channels)
    double myOriginalIntegral = h->Integral();
    for (int j = 0; j < h->GetNbinsX()+1; ++j) {
      if (h->GetBinContent(j) < 0) {
        std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m up variation with negative value (" << h->GetBinContent(j) << "+-" << h->GetBinError(j)
                  << ") in bin " << h->GetXaxis()->GetBinLowEdge(j) << "-" << h->GetXaxis()->GetBinUpEdge(j)
                  << " set to 0+-0 prior to normalisation in column " << datasets[i]->getFilename() << std::endl;
        h->SetBinContent(j, 0);
        h->SetBinError(j, 0);
      }
    }
    // Normalise
    double myZeroSuppressionCorrection = 1.0;
    if (h->Integral() > 0)
      myZeroSuppressionCorrection = myOriginalIntegral / h->Integral();
    hUp->Add(h, info->getNormalisationFactor(datasets[i]->getFile()) * additionalNormalisation * myZeroSuppressionCorrection);

    s.str("");
    s << sDownPrefix+"/"+sHistoName;
    h = dynamic_cast<TH1*>(datasets[i]->getFile()->Get(s.str().c_str()));
    if (!h) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m Could not find histogram " << s.str() << " in file " << datasets[i]->getFilename() << "!" << std::endl;
      return -1.;
    }
    // Rebin
    if (h->GetNbinsX() > hDown->GetNbinsX()) {
      //std::cout << "bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
      h->Rebin(h->GetNbinsX() / hDown->GetNbinsX());
      //std::cout << "new bins " << myHisto->GetNbinsX() << "->" << myPlot->GetNbinsX() << " ratio=" << myHisto->GetNbinsX() / myPlot->GetNbinsX() << std::endl;
    } else if (h->GetNbinsX() < hDown->GetNbinsX()) {
      std::cout << "\033[0;41m\033[1;37mError:\033[0;0m You asked for " << hDown->GetNbinsX() << ", but the mT histogram " << s.str() << " has only " << h->GetNbinsX() << " bins!" << std::endl;
    }
    // Set negative bins to zero prior to normalisation (occurs in EWK residual channels)
    myOriginalIntegral = h->Integral();
    for (int j = 0; j < h->GetNbinsX()+1; ++j) {
      if (h->GetBinContent(j) < 0) {
        std::cout << "\033[0;43m\033[1;37mWarning:\033[0;0m down variation with negative value (" << h->GetBinContent(j) << "+-" << h->GetBinError(j)
                  << ") in bin " << h->GetXaxis()->GetBinLowEdge(j) << "-" << h->GetXaxis()->GetBinUpEdge(j)
                  << " set to 0+-0 prior to normalisation in column " << datasets[i]->getFilename() << std::endl;
        h->SetBinContent(j, 0);
        h->SetBinError(j, 0);
      }
    }
    // Normalise
    myZeroSuppressionCorrection = 1.0;
    if (h->Integral() > 0)
      myZeroSuppressionCorrection = myOriginalIntegral / h->Integral();
    hDown->Add(h, info->getNormalisationFactor(datasets[i]->getFile()) * additionalNormalisation * myZeroSuppressionCorrection);
  }
  return 0.;
}

void ExtractableShape::print() {
  std::cout << "Row / Shape: ";
  Extractable::print();
  //std::cout << " counter=" << sShapeItem << std::endl;
}

void ExtractableShape::addHistogramsToFile(std::string label, std::string id, TFile* f) {
  std::stringstream s;
  s << label << "_" << id << "Up";
  TH1F* h = new TH1F(s.str().c_str(), s.str().c_str(), 20, 0, 400);
  h->Sumw2();
  h->Add(hUp);
  h->SetDirectory(f);
  std::cout << "  Shape nuisance: Created histo " << s.str() << " with normalisation " << h->Integral() <<  std::endl;
  s.str("");
  s << label << "_" << id << "Down";
  h = new TH1F(s.str().c_str(), s.str().c_str(), 20, 0, 400);
  h->Sumw2();
  h->Add(hDown);
  h->SetDirectory(f);
  std::cout << "  Shape nuisance: Created histo " << s.str() << " with normalisation " << h->Integral() << std::endl;
}