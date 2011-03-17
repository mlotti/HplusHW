// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FactorizationTable_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FactorizationTable_h

#include <vector>
#include <string>

#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace HPlus {
  /**
   * Class for containing a lookup table of factorized coefficients
   */
  class FactorizationTable {
  enum FactorizationTableType {
    kByPt,
    kByEta,
    kByPtVsEta
  };
  public:
    /// Constructor for obtaining automatically the table corresponding to certain tau algorithm 
    FactorizationTable(const edm::ParameterSet& iConfig);
    /// Constructor for manually setting the factorization table
    FactorizationTable(const edm::ParameterSet& iConfig, std::string tableNamePrefix);
    ~FactorizationTable();

    double getWeightByPtAndEta(double pt, double eta) const;

  private:
    /// Initialization called from the constructor
    void initialize(const edm::ParameterSet& factorizationConfig, const edm::ParameterSet& factorizationTableConfig, std::string tableNamePrefix, std::string tableTypeName);
  
    int calculateTableIndex(const double value, const std::vector<double>& edges) const;
  
    /// Protection for the case the factorization is not used
    bool fFactorizationEnabled;
    /// Type of table
    FactorizationTableType fTableType;
    /// Low bin edges by pT
    std::vector<double> fPtLowEdges;
    /// Low bin edges by eta
    std::vector<double> fEtaLowEdges;
    /// Weights by pT
    std::vector<double> fPtTable;
    /// Weights by eta
    std::vector<double> fEtaTable;
    /// Weights by pT vs eta
    std::vector<double> fPtVsEtaTable;
    
    std::string fTauAlgorithm;
  };
}

#endif
