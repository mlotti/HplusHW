#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"

#include <iostream>

#include "FWCore/Utilities/interface/Exception.h"

namespace HPlus {
  FactorizationTable::FactorizationTable(const edm::ParameterSet& iConfig) {
    // Obtain correct parameterset
    const edm::ParameterSet myFactorizationConfig = iConfig.getUntrackedParameter<edm::ParameterSet>("factorization"); 
    const edm::ParameterSet myFactorizationTablesConfig =
      myFactorizationConfig.getUntrackedParameter<edm::ParameterSet>("factorizationTables");
    // Determine type of table
    std::string myTableType = myFactorizationConfig.getUntrackedParameter<std::string>("factorizationTableType");
    if      (myTableType == "byPt")      fTableType = kByPt;
    else if (myTableType == "byEta")     fTableType = kByEta;
    else if (myTableType == "byPtVsEta") fTableType = kByPtVsEta;
    else throw cms::Exception("Error") << "FactorizationTable: factorizationSourceName is unknown! Options: byPt, byEta, byPtVsEta";
    // Determine tauID algorithm
    std::string tauAlgorithm = "";
    std::string mySelection = iConfig.getUntrackedParameter<std::string>("selection");
    if     (mySelection == "CaloTauCutBased")             tauAlgorithm = "signalAnalysisTauSelectionCaloTauCutBased";
    else if(mySelection == "ShrinkingConePFTauCutBased")  tauAlgorithm = "signalAnalysisTauSelectionShrinkingConeCutBased";
    else if(mySelection == "ShrinkingConePFTauTaNCBased") tauAlgorithm = "signalAnalysisTauSelectionShrinkingConeTaNCBased";
    else if(mySelection == "HPSTauBased")                 tauAlgorithm = "signalAnalysisTauSelectionHPSTauBased";
    else throw cms::Exception("Error") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: CaloTauCutBased, ShrinkingConePFTauCutBased, ShrinkingConePFTauTaNCBased, HPSTauBased" << std::endl;
    fTauAlgorithm = tauAlgorithm; // FIXME: DEBUG
    // Obtain limits
    fPtLowEdges = myFactorizationConfig.getUntrackedParameter<std::vector<double> >("ptBinLowEdges");
    fEtaLowEdges = myFactorizationConfig.getUntrackedParameter<std::vector<double> >("etaBinLowEdges");
    // Obtain coefficient tables
    fPtTable = myFactorizationTablesConfig.getUntrackedParameter<std::vector<double> >("tauIDFactorizationByPt_"+tauAlgorithm+"_Coefficients");
    fEtaTable = myFactorizationTablesConfig.getUntrackedParameter<std::vector<double> >("tauIDFactorizationByEta_"+tauAlgorithm+"_Coefficients");
    fPtVsEtaTable = myFactorizationTablesConfig.getUntrackedParameter<std::vector<double> >("tauIDFactorizationByPtVsEta_"+tauAlgorithm+"_Coefficients");
    
    // Check dimensions
    if (fPtLowEdges.size()+1 != fPtTable.size() ||
        fEtaLowEdges.size()+1 != fEtaTable.size() ||
        (fPtLowEdges.size()+1)*(fEtaLowEdges.size()+1) != fPtVsEtaTable.size()) {
      throw cms::Exception("Error") 
        << "FactorizationTable: dimensions of the bins and coefficient tables do not match!" << std::endl
        << "Regenerate the coefficient tables to get correct dimensions!" << std::endl;
    }
  }

  FactorizationTable::~FactorizationTable() {}

  double FactorizationTable::getWeightByPtAndEta(double pt, double eta) const {
    // Just for debugging
    //std::cout << "debug: " << fTauAlgorithm << " pt=" << pt << " index=" << calculateTableIndex(pt, fPtLowEdges)
    //          << " eta=" << eta << " index=" << calculateTableIndex(eta, fEtaLowEdges) << std::endl;

    // Return output of correct index of correct table
    if (fTableType == kByPt)
      return fPtTable[calculateTableIndex(pt, fPtLowEdges)];
    else if (fTableType == kByEta)
      return fEtaTable[calculateTableIndex(eta, fEtaLowEdges)];
    else if (fTableType == kByPtVsEta) {
      int myEtaIndex = calculateTableIndex(eta, fEtaLowEdges);
      int myPtIndex = calculateTableIndex(pt, fPtLowEdges);
      return fPtVsEtaTable[myEtaIndex*(fPtLowEdges.size()+1) + myPtIndex];
    }
    return 0.;
  }

  int FactorizationTable::calculateTableIndex(const double value, const std::vector<double>& edges) const {
    int myIndex = 0;
    int mySize = static_cast<int>(edges.size());
    while (value >= edges[myIndex] && myIndex < mySize) {
      ++myIndex;
    }
    return myIndex;
  }
}
