// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FactorizationTable_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FactorizationTable_h

#include <vector>
#include <string>

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "TH1F.h"

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

    /// Getter for weight (depends on table type selected)
    double getWeightByPtAndEta(double pt, double eta) const;
    /// Getter for table dimension (returns number of bins, i.e. table size + 1)
    int getCoefficientTableSize() const;
    /// Getter for bin index (for histogramming)
    int getCoefficientTableIndexByPtAndEta(double pt, double eta) const;
    /// Getter for bin low edges
    std::vector<double> getBinLowEdges() const;

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
    /// Weights table
    std::vector<double> fWeightTable;
    
    std::string fTauAlgorithm;
    
    TH1* hUsedCoefficients;
  };
}

#endif
