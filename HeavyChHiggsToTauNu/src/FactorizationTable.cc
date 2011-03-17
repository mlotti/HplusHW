#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"

#include <iostream>

#include "FWCore/Utilities/interface/Exception.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  FactorizationTable::FactorizationTable(const edm::ParameterSet& iConfig) :
    fFactorizationEnabled(false) {
    // Check if factorization was enabled
    std::string myOperatingModeSelection = iConfig.getUntrackedParameter<std::string>("operatingMode");
    if (myOperatingModeSelection == "factorized") {
      fFactorizationEnabled = true;
    } else {
      return;
    }
    // Obtain correct parameterset
    const edm::ParameterSet myFactorizationConfig = iConfig.getUntrackedParameter<edm::ParameterSet>("factorization"); 
    const edm::ParameterSet myFactorizationTablesConfig =
      myFactorizationConfig.getUntrackedParameter<edm::ParameterSet>("factorizationTables");
    // Determine type of table
    std::string myTableType = myFactorizationConfig.getUntrackedParameter<std::string>("factorizationTableType");
    // Determine tauID algorithm
    std::string tauAlgorithm = "";
    std::string mySelection = iConfig.getUntrackedParameter<std::string>("selection");
    if     (mySelection == "CaloTauCutBased")             tauAlgorithm = "signalAnalysisTauSelectionCaloTauCutBased";
    else if(mySelection == "ShrinkingConePFTauCutBased")  tauAlgorithm = "signalAnalysisTauSelectionShrinkingConeCutBased";
    else if(mySelection == "ShrinkingConePFTauTaNCBased") tauAlgorithm = "signalAnalysisTauSelectionShrinkingConeTaNCBased";
    else if(mySelection == "HPSTauBased")                 tauAlgorithm = "signalAnalysisTauSelectionHPSTauBased";
    else if(mySelection == "CombinedHPSTaNCTauBased") tauAlgorithm = "signalAnalysisTauSelectionCombinedHPSTaNCBased";
    else throw cms::Exception("Configuration") << "FactorizationTable: no or unknown tau selection used! Options for 'selection' are: CaloTauCutBased, ShrinkingConePFTauCutBased, ShrinkingConePFTauTaNCBased, HPSTauBased, CombinedHPSTaNCTauBased (you chose '" << mySelection << "')" << std::endl;
    fTauAlgorithm = tauAlgorithm;
    std::string myPrefix = "tauIDFactorizationByPt_"+tauAlgorithm;
    // Initialize
    initialize(myFactorizationConfig, myFactorizationTablesConfig, myPrefix, myTableType);
  }

  FactorizationTable::FactorizationTable(const edm::ParameterSet& iConfig, std::string tableNamePrefix)
  : fFactorizationEnabled(true),
  fTauAlgorithm("NA") {
    // Obtain correct parameterset
    const edm::ParameterSet myFactorizationConfig = iConfig.getUntrackedParameter<edm::ParameterSet>("factorization"); 
    const edm::ParameterSet myFactorizationTablesConfig =
      myFactorizationConfig.getUntrackedParameter<edm::ParameterSet>("factorizationTables");
    // Determine type of table
    std::string myTableType = myFactorizationConfig.getUntrackedParameter<std::string>("factorizationTableType");
    // Initialize
    initialize(myFactorizationConfig, myFactorizationTablesConfig, tableNamePrefix, myTableType);
  }

  FactorizationTable::~FactorizationTable() {}

  void FactorizationTable::initialize(const edm::ParameterSet& factorizationConfig, const edm::ParameterSet& factorizationTableConfig, std::string tableNamePrefix, std::string tableTypeName) {
    // Check table type
    if      (tableTypeName == "byPt")      fTableType = kByPt;
    else if (tableTypeName == "byEta")     fTableType = kByEta;
    else if (tableTypeName == "byPtVsEta") fTableType = kByPtVsEta;
    else throw cms::Exception("Configuration") << "FactorizationTable: factorizationSourceName is unknown (was '" << tableTypeName << "')! Options: byPt, byEta, byPtVsEta";
    // Obtain limits
    if (fTableType == kByPt || fTableType == kByPtVsEta)
      fPtLowEdges = factorizationConfig.getUntrackedParameter<std::vector<double> >("ptBinLowEdges");
    if (fTableType == kByEta || fTableType == kByPtVsEta)
      fEtaLowEdges = factorizationConfig.getUntrackedParameter<std::vector<double> >("etaBinLowEdges");
    // Obtain coefficient tables and check that their size is correct
    bool myDimensionStatus = true;
    if (fTableType == kByPt) {
      fWeightTable = factorizationTableConfig.getUntrackedParameter<std::vector<double> >(tableNamePrefix+"_Coefficients");
      if (fPtLowEdges.size()+1 != fWeightTable.size())
        myDimensionStatus = false;
    }
    if (fTableType == kByEta) {
      fWeightTable = factorizationTableConfig.getUntrackedParameter<std::vector<double> >(tableNamePrefix+"_Coefficients");
      if (fEtaLowEdges.size()+1 != fWeightTable.size())
        myDimensionStatus = false;
    }
    if (fTableType == kByPtVsEta) {
      fWeightTable = factorizationTableConfig.getUntrackedParameter<std::vector<double> >(tableNamePrefix+"_Coefficients");
      if ((fPtLowEdges.size()+1)*(fEtaLowEdges.size()+1) != fWeightTable.size())
        myDimensionStatus = false;
    }
    // Throw exception if coefficient table dimension is incorrect
    if (!myDimensionStatus) {
      throw cms::Exception("Error") 
        << "FactorizationTable: dimensions of the bins and coefficient tables do not match!" << std::endl
        << "Regenerate the coefficient tables to get correct dimensions!" << std::endl;
    }
    
    // Fill control histogram with coefficients
    edm::Service<TFileService> fs;
    int myCoefficientBinCount = getCoefficientTableSize();
    std::string myName = "FactorizationTableCoefficients_"+tableNamePrefix;
    std::string myLabel = myName+";bin;weight coefficient";
    hUsedCoefficients = fs->make<TH1F>(myName.c_str(), myLabel.c_str(), myCoefficientBinCount, 0., myCoefficientBinCount);
    for (size_t i = 0; i < fWeightTable.size(); ++i) {
      hUsedCoefficients->Fill(i, fWeightTable[i]);
    }
  }

  double FactorizationTable::getWeightByPtAndEta(double pt, double eta) const {
    if (!fFactorizationEnabled) return 1.;
    // Just for debugging
    //std::cout << "debug: " << fTauAlgorithm << " pt=" << pt << " index=" << calculateTableIndex(pt, fPtLowEdges)
    //          << " eta=" << eta << " index=" << calculateTableIndex(eta, fEtaLowEdges) << std::endl;

    // Return output of correct index of correct table
    if (fTableType == kByPt)
      return fWeightTable[calculateTableIndex(pt, fPtLowEdges)];
    else if (fTableType == kByEta)
      return fWeightTable[calculateTableIndex(eta, fEtaLowEdges)];
    else if (fTableType == kByPtVsEta) {
      int myEtaIndex = calculateTableIndex(eta, fEtaLowEdges);
      int myPtIndex = calculateTableIndex(pt, fPtLowEdges);
      return fWeightTable[myEtaIndex*(fPtLowEdges.size()+1) + myPtIndex];
    }
    return 0.;
  }

  int FactorizationTable::getCoefficientTableSize() const {
    return fWeightTable.size();
  }

  int FactorizationTable::getCoefficientTableIndexByPtAndEta(double pt, double eta) const {
    if (fTableType == kByPt)
      return calculateTableIndex(pt, fPtLowEdges);
    else if (fTableType == kByEta)
      return calculateTableIndex(eta, fEtaLowEdges);
    else if (fTableType == kByPtVsEta) {
      int myEtaIndex = calculateTableIndex(eta, fEtaLowEdges);
      int myPtIndex = calculateTableIndex(pt, fPtLowEdges);
      return myEtaIndex*fPtLowEdges.size() + myPtIndex;
    }
    return 0;
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
