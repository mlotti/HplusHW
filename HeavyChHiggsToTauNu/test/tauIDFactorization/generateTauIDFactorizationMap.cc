#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMath.h"
#include "TLatex.h"
#include "TCanvas.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

#include "tdrstyle.cc"

// ----------------------------------------------------------------------
class ConfigurationParser {
 public:
  ConfigurationParser(std::string filename);
  ~ConfigurationParser();
 
  const std::vector<double>& getEtaBinEdges() const { return fEtaBinEdges; }
  const std::vector<double>& getPtBinEdges() const { return fPtBinEdges; }

 private:
  void ParseValues(std::ifstream& input, std::vector<double>& edges);

  // Low edges of bins
  std::vector<double> fEtaBinEdges;
  std::vector<double> fPtBinEdges;
};

ConfigurationParser::ConfigurationParser(std::string filename) {
  const std::string myPtLabel = "  ptBinLowEdges";
  const std::string myEtaLabel = "  etaBinLowEdges";

  // Open file
  std::ifstream myFile(filename.c_str());
  if (myFile.bad()) {
    std::cout << "Error: Could not open configuration file '" << filename << "'!" << std::endl;
    return;
  }
  // Read file
  while (!myFile.eof()) {
    char myBuffer[1000];
    myFile.getline(myBuffer, 1000);
    std::string myString(myBuffer);
    if (myString.find(myEtaLabel.c_str()) == 0) {
      ParseValues(myFile, fEtaBinEdges);
    } else if (myString.find(myPtLabel.c_str()) == 0) {
      ParseValues(myFile, fPtBinEdges);
    }
  }
  // Check end result
  if (!fPtBinEdges.size()) {
    std::cout << "Error: could not find tag " << myPtLabel
	      << " in the configuration file '" << filename << "'!" << std::endl;
    return;
  }
  if (!fEtaBinEdges.size()) {
    std::cout << "Error: could not find tag " << myEtaLabel
	      << " in the configuration file '" << filename << "'!" << std::endl;
    return;
  }
}
ConfigurationParser::~ConfigurationParser() { }

void ConfigurationParser::ParseValues(std::ifstream& input, std::vector<double>& edges) {
  // Fill the values inside the vdouble(...) to the vector
  bool myStatus = true;
  while (myStatus && !input.eof()) {
    char myBuffer[100];
    double myValue;
    input >> myValue >> myBuffer;
    //std::cout << myValue << " - " << myBuffer << std::endl; // for debugging only
    edges.push_back(myValue);
    if (myBuffer[0] == ')')
      myStatus = false;
  }
}

// ----------------------------------------------------------------------
class FactorizationMap {
 public:
  /// Constructor for 1D factorization coefficient maps
  FactorizationMap(std::string label, std::string name, TFile* file,
                   std::string beforeName, std::string afterName,
                   std::string beforeUnweightedName, std::string afterUnweightedName,
                   const std::vector<double>& edges);
  /// Constructor for 2D factorization coefficient maps
  FactorizationMap(std::string label, std::string name, TFile* file,
                   std::string beforeName, std::string afterName,
                   std::string beforeUnweightedName, std::string afterUnweightedName,
                   const std::vector<double>& edgesX, const std::vector<double>& edgesY);
  ~FactorizationMap();

  /// Output map
  std::string writeMap() const;
  /// Draw histogram of the result
  void draw() const;
  /// Obtain error status
  bool errorStatus() const { return fErrorStatus; }

 private:
  void calculateWeights(const std::vector<double>& before, const std::vector<double>& after);
  void calculateUncertainty(const std::vector<double>& beforeUnweighted, const std::vector<double>& afterUnweighted);
  void calculateRelativeUncertainty(const std::vector<double>& afterUnweighted);
  double findMinimumForHistogram() const;
  double findMaximumForHistogram() const;

  const std::string fLabel;
  const std::string fName;
  const std::vector<double> fEdgesX;
  const std::vector<double> fEdgesY;
  std::vector<double> fWeights;     // for result
  std::vector<double> fUncertainty; // for statistical uncertainty
  std::vector<double> fRelativeUncertainty; // for statistical uncertainty

  int fDimension; // Dimension of table in x direction
  bool fErrorStatus;
  int fPassedEntries; // number of passed entries
};

FactorizationMap::FactorizationMap(std::string label, std::string name, TFile* file,
                                   std::string beforeName, std::string afterName,
                                   std::string beforeUnweightedName, std::string afterUnweightedName,
                                   const std::vector<double>& edges)
  : fLabel(label), fName(name), fEdgesX(edges), fErrorStatus(false) {
  // Get histograms
  TH1F* hBefore = dynamic_cast<TH1F*>(file->Get(beforeName.c_str()));
  TH1F* hAfter = dynamic_cast<TH1F*>(file->Get(afterName.c_str()));
  TH1F* hBeforeUnweighted = dynamic_cast<TH1F*>(file->Get(beforeUnweightedName.c_str()));
  TH1F* hAfterUnweighted = dynamic_cast<TH1F*>(file->Get(afterUnweightedName.c_str()));
  if (!hBefore) std::cout << "Error: Could not find histograms for item '" << beforeName << "' in root file!" << std::endl;
  if (!hAfter) std::cout << "Error: Could not find histograms for item '" << afterName << "' in root file!" << std::endl;
  if (!hBeforeUnweighted) std::cout << "Error: Could not find histograms for item '" << beforeUnweightedName << "' in root file!" << std::endl;
  if (!hAfterUnweighted) std::cout << "Error: Could not find histograms for item '" << afterUnweightedName << "' in root file!" << std::endl;
  if (!hBefore || !hAfter || !hBeforeUnweighted || !hAfterUnweighted) {
    fErrorStatus = true;
    return;
  }
  // Initialize
  fPassedEntries = 0;
  int iTableBin = 0;
  int myTableBinCount = edges.size();
  std::vector<double> myBeforeCounts;
  std::vector<double> myAfterCounts;
  std::vector<double> myBeforeCountsUnweighted;
  std::vector<double> myAfterCountsUnweighted;

  // Resize the output vectors (+1 is to take also the underflow bin, which is the first entry)
  fWeights.resize(myTableBinCount+1);
  fUncertainty.resize(fWeights.size());
  fRelativeUncertainty.resize(fWeights.size());
  myBeforeCounts.resize(fWeights.size());
  myAfterCounts.resize(fWeights.size());
  myBeforeCountsUnweighted.resize(fWeights.size());
  myAfterCountsUnweighted.resize(fWeights.size());
  for (int i = 0; i <= myTableBinCount; ++i) {
    myBeforeCounts[i] = 0.;
    myAfterCounts[i] = 0.;
    myBeforeCountsUnweighted[i] = 0.;
    myAfterCountsUnweighted[i] = 0.;
  }
  fDimension = fWeights.size();
  // Loop over the histogram (note that also the underflow and overflow bins are taken into account)
  for (int iHistoBin = 0; iHistoBin <= hBefore->GetXaxis()->GetNbins()+1; ++iHistoBin) {
    // Search bin
    while (hBefore->GetXaxis()->GetBinLowEdge(iHistoBin) >= edges[iTableBin]
	   && iTableBin < myTableBinCount) {
      ++iTableBin;
    }
    //std::cout << "bin=" << hBefore->GetXaxis()->GetBinLowEdge(iHistoBin) << " table=" << edges[iTableBin] << std::endl; // debugging only
    myBeforeCounts[iTableBin] += hBefore->GetBinContent(iHistoBin);
    myAfterCounts[iTableBin] += hAfter->GetBinContent(iHistoBin);
    myBeforeCountsUnweighted[iTableBin] += hBeforeUnweighted->GetBinContent(iHistoBin);
    myAfterCountsUnweighted[iTableBin] += hAfterUnweighted->GetBinContent(iHistoBin);
    fPassedEntries += hAfterUnweighted->GetBinContent(iHistoBin);
  }
  // Calculate weight (i.e. ratio of after vs. before)
  calculateWeights(myBeforeCounts, myAfterCounts);
  calculateUncertainty(myBeforeCountsUnweighted, myAfterCountsUnweighted);
  calculateRelativeUncertainty(myAfterCountsUnweighted);
}

FactorizationMap::FactorizationMap(std::string label, std::string name, TFile* file,
                                   std::string beforeName, std::string afterName,
                                   std::string beforeUnweightedName, std::string afterUnweightedName,
                                   const std::vector<double>& edgesX, const std::vector<double>& edgesY)
  : fLabel(label), fName(name), fEdgesX(edgesX), fEdgesY(edgesY), fErrorStatus(false) {
  // Get histograms
  TH2F* hBefore = dynamic_cast<TH2F*>(file->Get(beforeName.c_str()));
  TH2F* hAfter = dynamic_cast<TH2F*>(file->Get(afterName.c_str()));
  TH2F* hBeforeUnweighted = dynamic_cast<TH2F*>(file->Get(beforeUnweightedName.c_str()));
  TH2F* hAfterUnweighted = dynamic_cast<TH2F*>(file->Get(afterUnweightedName.c_str()));
  // Check success
  if (!hBefore) std::cout << "Error: Could not find histograms for item '" << beforeName << "' in root file!" << std::endl;
  if (!hAfter) std::cout << "Error: Could not find histograms for item '" << afterName << "' in root file!" << std::endl;
  if (!hBeforeUnweighted) std::cout << "Error: Could not find histograms for item '" << beforeUnweightedName << "' in root file!" << std::endl;
  if (!hAfterUnweighted) std::cout << "Error: Could not find histograms for item '" << afterUnweightedName << "' in root file!" << std::endl;
  if (!hBefore || !hAfter || !hBeforeUnweighted || !hAfterUnweighted) {
    fErrorStatus = true;
    return;
  }
  // Initialize
  fPassedEntries = 0;
  int iTableBinX = 0;
  int iTableBinY = 0;
  int myTableBinCountX = edgesX.size();
  int myTableBinCountY = edgesY.size();
  std::vector<double> myBeforeCounts;
  std::vector<double> myAfterCounts;
  std::vector<double> myBeforeCountsUnweighted;
  std::vector<double> myAfterCountsUnweighted;

  // Resize the output vectors (+1 is to take also the underflow bin)
  fWeights.resize((myTableBinCountX+1)*(myTableBinCountY+1));
  fUncertainty.resize(fWeights.size());
  fRelativeUncertainty.resize(fWeights.size());
  myBeforeCounts.resize(fWeights.size());
  myAfterCounts.resize(fWeights.size());
  myBeforeCountsUnweighted.resize(fWeights.size());
  myAfterCountsUnweighted.resize(fWeights.size());
  for (int i = 0; i < static_cast<int>(fWeights.size()); ++i) {
    myBeforeCounts[i] = 0.;
    myAfterCounts[i] = 0.;
    myBeforeCountsUnweighted[i] = 0.;
    myAfterCountsUnweighted[i] = 0.;
  }
  fDimension = myTableBinCountX+1;
  // Loop over the histogram (note that the underflow bin is taken already here)
  for (int iHistoBinX = 0; iHistoBinX <= hBefore->GetXaxis()->GetNbins()+1; ++iHistoBinX) {
    // Search X bin
    while (hBefore->GetXaxis()->GetBinLowEdge(iHistoBinX) >= edgesX[iTableBinX]
	   && iTableBinX < myTableBinCountX) {
      ++iTableBinX;
    }
    iTableBinY = 0;
    for (int iHistoBinY = 0; iHistoBinY <= hBefore->GetYaxis()->GetNbins()+1; ++iHistoBinY) {
      // Search Y bin
      while (hBefore->GetYaxis()->GetBinLowEdge(iHistoBinY) >= edgesY[iTableBinY]
	     && iTableBinY < myTableBinCountY) {
	++iTableBinY;
      }
      //std::cout << "bin=" << hBefore->GetXaxis()->GetBinLowEdge(iHistoBin) << " table=" << edges[iTableBin] << std::endl; // debugging only
      int myIndex = (iTableBinY)*(myTableBinCountX+1) + (iTableBinX);
      myBeforeCounts[myIndex] += hBefore->GetBinContent(iHistoBinX, iHistoBinY);
      myAfterCounts[myIndex] += hAfter->GetBinContent(iHistoBinX, iHistoBinY);
      myBeforeCountsUnweighted[myIndex] += hBeforeUnweighted->GetBinContent(iHistoBinX, iHistoBinY);
      myAfterCountsUnweighted[myIndex] += hAfterUnweighted->GetBinContent(iHistoBinX, iHistoBinY);
      fPassedEntries += hAfterUnweighted->GetBinContent(iHistoBinX, iHistoBinY);
    }
  }
  // Calculate weight (i.e. ratio of after vs. before)
  calculateWeights(myBeforeCounts, myAfterCounts);
  calculateUncertainty(myBeforeCountsUnweighted, myAfterCountsUnweighted);
  calculateRelativeUncertainty(myAfterCountsUnweighted);
}

FactorizationMap::~FactorizationMap() { }

void FactorizationMap::calculateWeights(const std::vector<double>& before, const std::vector<double>& after) {
  for (int i = 0; i < static_cast<int>(before.size()); ++i) {
    //std::cout << "i=" << i << " before=" << myBeforeCounts[i] << " after=" << myAfterCounts[i] << std::endl;
    if (before[i] > 0) {
      if (after[i] > 0) {
	fWeights[i] = after[i] / before[i];
      } else {
	fWeights[i] = 1.e-99;
      }
    } else {
      fWeights[i] = 1.e-99;
    }
  }  

}

void FactorizationMap::calculateUncertainty(const std::vector<double>& beforeUnweighted, const std::vector<double>& afterUnweighted) {
  for (int i = 0; i < static_cast<int>(beforeUnweighted.size()); ++i) {
    //std::cout << "i=" << i << " before=" << myBeforeCounts[i] << " after=" << myAfterCounts[i] << std::endl;
    if (beforeUnweighted[i] > 0) {
      if (afterUnweighted[i] > 0) {
	fUncertainty[i] = TMath::Sqrt(afterUnweighted[i]) / beforeUnweighted[i];
      } else {
	fUncertainty[i] = 1.0 / beforeUnweighted[i];
      }
    } else {
      fUncertainty[i] = 1.e-99; // note, this is not exactly true and must be properly handled elsewhere
                                 // the uncertainty is not zero but just smaller than the sample weight
                                 // coming from the normalization to cross-section and luminosity
    }
  }  
}

void FactorizationMap::calculateRelativeUncertainty(const std::vector<double>& afterUnweighted) {
  for (int i = 0; i < static_cast<int>(afterUnweighted.size()); ++i) {
    if (afterUnweighted[i] > 0) {
      fRelativeUncertainty[i] = 1.0 / TMath::Sqrt(afterUnweighted[i]);
    } else {
      fRelativeUncertainty[i] = 1.e-99;
    }
  }
}

void FactorizationMap::draw() const {
  if (fErrorStatus) return;
  TObject* myWeightObject = 0;
  TObject* myUncertaintyObject = 0;
  std::string myDrawOptions = "";

  TCanvas* c = new TCanvas();
  std::stringstream myStream;
  if (!fEdgesY.size()) {
    // 1D histogram
    c->SetLogy(true);
    TH1F* myWeightHisto = new TH1F(fName.c_str(),fName.c_str(),fEdgesX.size()+1, 0, fEdgesX.size()+1);
    myStream << fName << "uncertainty";
    TH1F* myUncertaintyHisto = new TH1F(myStream.str().c_str(),myStream.str().c_str(),fEdgesX.size()+1, 0, fEdgesX.size()+1);
    myWeightHisto->SetXTitle(fName.c_str());
    myUncertaintyHisto->SetXTitle(fName.c_str());
    myWeightHisto->SetYTitle("Jet#rightarrow#tau fake-rate");
    myUncertaintyHisto->SetYTitle("Jet#rightarrow#tau fake-rate relative uncertainty");
    // Set bin labels
    myStream.str("");
    myStream << "<" << fEdgesX[0];
    myWeightHisto->GetXaxis()->SetBinLabel(1, myStream.str().c_str());
    myUncertaintyHisto->GetXaxis()->SetBinLabel(1, myStream.str().c_str());
    for (int i = 0; i < static_cast<int>(fEdgesX.size())-1; ++i) {
      myStream.str("");
      myStream << fEdgesX[i] << ".." << fEdgesX[i+1];
      myWeightHisto->GetXaxis()->SetBinLabel(i+2, myStream.str().c_str());
      myUncertaintyHisto->GetXaxis()->SetBinLabel(i+2, myStream.str().c_str());
    }
    myStream.str("");
    myStream << ">" << fEdgesX[fEdgesX.size()-1];
    myWeightHisto->GetXaxis()->SetBinLabel(fEdgesX.size()+1, myStream.str().c_str());
    myUncertaintyHisto->GetXaxis()->SetBinLabel(fEdgesX.size()+1, myStream.str().c_str());
    // Fill histograms
    for (int i = 0; i < static_cast<int>(fWeights.size()); ++i) {
      myWeightHisto->Fill(i+1, fWeights[i]);
      myWeightHisto->SetBinError(i+1, fUncertainty[i]);
      myUncertaintyHisto->Fill(i+1, fRelativeUncertainty[i]);
    }
    // Set histogram extrema
    myWeightHisto->SetMinimum(findMinimumForHistogram());
    myWeightHisto->SetMaximum(findMaximumForHistogram());
    myUncertaintyHisto->SetMinimum(1.e-3);
    myUncertaintyHisto->SetMaximum(1.1);
    // Store pointers
    myWeightObject = myWeightHisto;
    myUncertaintyObject = myUncertaintyHisto;
  } else {
    // 2D histogram
    c->SetLogz(true);
    c->SetRightMargin(0.13);
    myDrawOptions = "COLZ";
    TH2F* myWeightHisto = new TH2F(fName.c_str(),fName.c_str(),
				   fEdgesX.size()+1, 0, fEdgesX.size()+1,
				   fEdgesY.size()+1, 0, fEdgesY.size()+1);
    myStream << fName << "uncertainty";
    TH2F* myUncertaintyHisto = new TH2F(myStream.str().c_str(),myStream.str().c_str(),
					fEdgesX.size()+1, 0, fEdgesX.size()+1,
					fEdgesY.size()+1, 0, fEdgesY.size()+1);
    myWeightHisto->SetXTitle(fName.c_str());
    myUncertaintyHisto->SetXTitle(fName.c_str());
    //myWeightHisto->SetYTitle("Jet#rightarrow#tau fake-rate");
    //myUncertaintyHisto->SetYTitle("Jet#rightarrow#tau fake-rate relative uncertainty");
    // Set bin labels in X direction
    myStream.str("");
    myStream << "<" << fEdgesX[0];
    myWeightHisto->GetXaxis()->SetBinLabel(1, myStream.str().c_str());
    myUncertaintyHisto->GetXaxis()->SetBinLabel(1, myStream.str().c_str());
    for (int i = 0; i < static_cast<int>(fEdgesX.size())-1; ++i) {
      myStream.str("");
      myStream << fEdgesX[i] << ".." << fEdgesX[i+1];
      myWeightHisto->GetXaxis()->SetBinLabel(i+2, myStream.str().c_str());
      myUncertaintyHisto->GetXaxis()->SetBinLabel(i+2, myStream.str().c_str());
    }
    myStream.str("");
    myStream << ">" << fEdgesX[fEdgesX.size()-1];
    myWeightHisto->GetXaxis()->SetBinLabel(fEdgesX.size()+1, myStream.str().c_str());
    myUncertaintyHisto->GetXaxis()->SetBinLabel(fEdgesX.size()+1, myStream.str().c_str());
    // Set bin labels in Y direction
    myStream.str("");
    myStream << "<" << fEdgesY[0];
    myWeightHisto->GetYaxis()->SetBinLabel(1, myStream.str().c_str());
    myUncertaintyHisto->GetYaxis()->SetBinLabel(1, myStream.str().c_str());
    for (int i = 0; i < static_cast<int>(fEdgesY.size())-1; ++i) {
      myStream.str("");
      myStream << fEdgesY[i] << ".." << fEdgesY[i+1];
      myWeightHisto->GetYaxis()->SetBinLabel(i+2, myStream.str().c_str());
      myUncertaintyHisto->GetYaxis()->SetBinLabel(i+2, myStream.str().c_str());
    }
    myStream.str("");
    myStream << ">" << fEdgesY[fEdgesY.size()-1];
    myWeightHisto->GetYaxis()->SetBinLabel(fEdgesY.size()+1, myStream.str().c_str());
    myUncertaintyHisto->GetYaxis()->SetBinLabel(fEdgesY.size()+1, myStream.str().c_str());
    // Fill histograms
    int myIndex = 0;
    int myRow = 0;
    while (myIndex < static_cast<int>(fWeights.size())) {
      for (int i = 0; i < fDimension; ++i) {
	myWeightHisto->Fill(i+1, myRow+1, fWeights[myIndex]);
	myWeightHisto->SetBinError(i+1, myRow+1, fUncertainty[myIndex]);
	myUncertaintyHisto->Fill(i+1, myRow+1, fRelativeUncertainty[myIndex]);
	++myIndex;
      }
      ++myRow;
    }
    // Set histogram extrema
    myWeightHisto->SetMinimum(findMinimumForHistogram());
    myWeightHisto->SetMaximum(findMaximumForHistogram());
    myUncertaintyHisto->SetMinimum(1.e-3);
    myUncertaintyHisto->SetMaximum(1.1);
    // Store pointers
    myWeightObject = myWeightHisto;
    myUncertaintyObject = myUncertaintyHisto;
  }
  // Draw weight histogram
  myWeightObject->Draw(myDrawOptions.c_str());
  myStream.str("");
  myStream << fLabel << "_" << fName << "_weights.png";
  c->Print(myStream.str().c_str());
  myStream.str("");
  myStream << fLabel << "_" << fName << "_weights.C";
  c->Print(myStream.str().c_str());
  // Draw uncertainty histogram
  myUncertaintyObject->Draw(myDrawOptions.c_str());
  TLatex* l = new TLatex(0.1, 1.35, fLabel.c_str());
  l->SetTextSize(0.02);
  l->Draw();
  myStream.str("");
  myStream << "entries=" << fPassedEntries; 
  l = new TLatex(0.1, 1.15, myStream.str().c_str());
  l->SetTextSize(0.02);
  l->Draw();
  myStream.str("");
  myStream << fLabel << "_" << fName << "_weights_uncertainty.png";
  c->Print(myStream.str().c_str());
  myStream.str("");
  myStream << fLabel << "_" << fName << "_weights_uncertainty.C";
  c->Print(myStream.str().c_str());
}

double FactorizationMap::findMinimumForHistogram() const {
  double myValue = 1.e99;
  for (int i = 0; i < static_cast<int>(fWeights.size()); ++i) {
    if (fWeights[i] > 1.e-90) {
      if (fWeights[i] - fUncertainty[i] < myValue) {
	if (fWeights[i] - fUncertainty[i] > 0) {
	  myValue = fWeights[i] - fUncertainty[i];
	} else {
	  myValue = fWeights[i] / 10.;
	}
      }
    }
  }
  if (myValue > 1.e90) return 1.;
  return myValue/1.5;
}

double FactorizationMap::findMaximumForHistogram() const {
  double myValue = 1.e-99;
  for (int i = 0; i < static_cast<int>(fWeights.size()); ++i) {
    if (fWeights[i] > 1.e-90) {
      if (fWeights[i] + fUncertainty[i] > myValue) {
	myValue = fWeights[i] + fUncertainty[i];
      }
    }
  }
  if (myValue < 1.e-90) return 1.;
  return myValue*1.5;
}

std::string FactorizationMap::writeMap() const {
  int mySize = fWeights.size();
  int myCount = 0;
  std::stringstream myStream;
  if (fErrorStatus) return myStream.str();
  
  myStream <<  "tauIDFactorizationBy" << fName << "_Coefficients = cms.untracked.vdouble( *(" << std::endl;
  while (myCount < mySize) {
    myStream << "  ";
    for (int i = 0; i < fDimension; ++i) {
      if (!i) 
	myStream << fWeights[myCount];
      else
	myStream << ", " << fWeights[myCount];
      ++myCount;
    }
    if (myCount+1 < mySize) myStream << ",";
    myStream << std::endl;
  }
  myStream << ") )," << std::endl << std::endl;
  myStream <<  "tauIDFactorizationBy" << fName << "_CoefficientUncertainty = cms.untracked.vdouble( *(" << std::endl;
  myCount = 0;
  while (myCount < mySize) {
    myStream << "  ";
    for (int i = 0; i < fDimension; ++i) {
      if (!i)
	myStream << fUncertainty[myCount];
      else
	myStream << ", " << fUncertainty[myCount];
      ++myCount;
    }
    if (myCount+1 < mySize) myStream << ",";
    myStream << std::endl;
  }
  myStream << ") )," << std::endl << std::endl;

  std::cout << myStream.str();
  return myStream.str();
}

// ----------------------------------------------------------------------
int main(int argc, char** argv) {
  // Set up string constants for config file location
  const std::string myConfigurationFilename = "../../python/HChTauIDFactorization_cfi.py";
  // Set up string constants for histograms
  const std::string myPtBeforeName = "factorization_calculation_pt_before_tauID";
  const std::string myPtAfterName = "factorization_calculation_pt_after_tauID";
  const std::string myPtBeforeUnweightedName = "factorization_calculation_pt_before_tauID_unweighted";
  const std::string myPtAfterUnweightedName = "factorization_calculation_pt_after_tauID_unweighted";
  const std::string myEtaBeforeName = "factorization_calculation_eta_before_tauID";
  const std::string myEtaAfterName = "factorization_calculation_eta_after_tauID";
  const std::string myEtaBeforeUnweightedName = "factorization_calculation_eta_before_tauID_unweighted";
  const std::string myEtaAfterUnweightedName = "factorization_calculation_eta_after_tauID_unweighted";
  const std::string myPtVsEtaBeforeName = "factorization_calculation_pt_vs_eta_before_tauID";
  const std::string myPtVsEtaAfterName = "factorization_calculation_pt_vs_eta_after_tauID";
  const std::string myPtVsEtaBeforeUnweightedName = "factorization_calculation_pt_vs_eta_before_tauID_unweighted";
  const std::string myPtVsEtaAfterUnweightedName = "factorization_calculation_pt_vs_eta_after_tauID_unweighted";
  // Set up string constants for tau algoritms
  std::vector<std::string> myTauAlgorithms;
  myTauAlgorithms.push_back("signalAnalysisTauSelectionShrinkingConeCutBased");
  myTauAlgorithms.push_back("signalAnalysisTauSelectionShrinkingConeTaNCBased");
  myTauAlgorithms.push_back("signalAnalysisTauSelectionHPSTauBased");
  myTauAlgorithms.push_back("signalAnalysisTauSelectionCaloTauCutBased");

  if (argc < 2) {
    std::cout << "Usage: generateTauIDFactorizationMap sample.root [sample2.root] [...]" << std::endl;
    return -1;
  }

  // Set style for histograms
  setTDRStyle();

  // Obtain table dimensions from the configuration file
  ConfigurationParser myParser(myConfigurationFilename);
  if (!myParser.getPtBinEdges().size() || !myParser.getEtaBinEdges().size()) return -1;

  // Loop over samples
  for (int i = 1; i < argc; ++i) {
    // Obtain stub of filename
    std::string myFilename(argv[i]);
    size_t myPos = myFilename.find_last_of('/');
    if (myPos == myFilename.size()) {
      myPos = 0;
    } else {
      ++myPos;
    }
    myFilename = myFilename.substr(myPos, myFilename.size());
    myFilename = myFilename.substr(0, myFilename.find_last_of('.'));
    // Replace any dash signs in filename stub with underscore (python does not like dashes)
    for (int j = 0; j < static_cast<int>(myFilename.size()); ++j) {
      if (myFilename[j] == '-') myFilename[j] = '_';
    }

    // Open file
    std::cout << "Processing sample: " << myFilename << std::endl;
    TFile* myFile = TFile::Open(argv[i]);
    if (!myFile) {
      std::cout << "Error: File '" << argv[i] << "' does not exist or could not be opened!" << std::endl;
      return -1;
    }

    // Calculate maps
    std::vector<FactorizationMap*> myMaps;
    for (std::vector<std::string>::const_iterator iTauAlgo = myTauAlgorithms.begin();
         iTauAlgo != myTauAlgorithms.end(); ++iTauAlgo) {
      // byPt
      myMaps.push_back(new FactorizationMap(myFilename+"_"+*iTauAlgo, "Pt_"+*iTauAlgo, myFile,
                                            *iTauAlgo+"/"+myPtBeforeName,
                                            *iTauAlgo+"/"+myPtAfterName,
                                            *iTauAlgo+"/"+myPtBeforeUnweightedName,
                                            *iTauAlgo+"/"+myPtAfterUnweightedName,
			                    myParser.getPtBinEdges()));
      if (myMaps[myMaps.size()-1]->errorStatus()) return -2;
      // byEta
      myMaps.push_back(new FactorizationMap(myFilename+"_"+*iTauAlgo, "Eta_"+*iTauAlgo, myFile,
                                            *iTauAlgo+"/"+myEtaBeforeName,
                                            *iTauAlgo+"/"+myEtaAfterName,
                                            *iTauAlgo+"/"+myEtaBeforeUnweightedName,
                                            *iTauAlgo+"/"+myEtaAfterUnweightedName,
			                    myParser.getEtaBinEdges()));
      if (myMaps[myMaps.size()-1]->errorStatus()) return -2;
      // byPtVsEta
      myMaps.push_back(new FactorizationMap(myFilename+"_"+*iTauAlgo, "PtVsEta_"+*iTauAlgo, myFile,
                                            *iTauAlgo+"/"+myPtVsEtaBeforeName,
                                            *iTauAlgo+"/"+myPtVsEtaAfterName,
                                            *iTauAlgo+"/"+myPtVsEtaBeforeUnweightedName,
                                            *iTauAlgo+"/"+myPtVsEtaAfterUnweightedName,
				            myParser.getPtBinEdges(),
				            myParser.getEtaBinEdges()));
      if (myMaps[myMaps.size()-1]->errorStatus()) return -2;
    }
    // Generate a config file
    std::string myConfigFilename = "FactorizationMap"+myFilename+"_cfi.py";
    std::ofstream myConfigFile(myConfigFilename.c_str());
    if (myConfigFile.fail()) {
      std::cout << "Error: Could not open file'" << myConfigFilename << "' for output!" << std::endl;
      return -1;
    }
    myConfigFile << "import FWCore.ParameterSet.Config as cms" << std::endl << std::endl;
    myConfigFile << "tauIDFactorizationCoefficients = cms.untracked.PSet(" << std::endl;
    myConfigFile << "factorizationSourceName = cms.untracked.string('" << myFilename << "')," << std::endl << std::endl;
    for (std::vector<FactorizationMap*>::const_iterator it = myMaps.begin(); it != myMaps.end(); ++it) {
      myConfigFile << (*it)->writeMap();
    }
    myConfigFile << ")" << std::endl;
    myConfigFile.close();
    std::cout << "Generated config file '" << myConfigFilename << "'" << std::endl;
    // Make some nice figures
    for (std::vector<FactorizationMap*>::const_iterator it = myMaps.begin(); it != myMaps.end(); ++it) {
      (*it)->draw();
    }
    // Release memory
    for (std::vector<FactorizationMap*>::const_iterator it = myMaps.begin(); it != myMaps.end(); ++it) {
      delete *it;
    }
  }

  return 0;
}
