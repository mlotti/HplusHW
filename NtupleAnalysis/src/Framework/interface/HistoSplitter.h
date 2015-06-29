// -*- c++ -*-
#ifndef Framework_HistoSplitter_h
#define Framework_HistoSplitter_h

#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/ParameterSet.h"
#include "TDirectory.h"

#include <sstream>
#include <string>
#include <vector>

class ParameterSet;

/**
 * This class contains the information for splitting of histograms as a function of one chosen variable
 */
class HistoSplitterItem {
public:
  HistoSplitterItem(const ParameterSet& config);
  ~HistoSplitterItem() { }

  /// Returns the number of bins including under- and overflows
  const size_t getBinCount() const { return fBinLowEdges.size()+1; }
  /// Returns index of the bin where the value belongs to; 0 is underflow and size() is highest bin
  const size_t getBinIndex(const float value) const;
  /// Returns the label
  const std::string& getLabel() const { return sLabel; }
  /// Returns a descriptive string for the ith bin
  const std::string getBinDescription(const size_t i) const;
  
private:
  /// Short label characterizing the variable (keep it short for readability)
  const std::string sLabel;
  /// List of bin low edges (just low edges; underflow and overflow are automatically created)
  const std::vector<float> fBinLowEdges;
  /// Defines if absolute values of test value are used when using bin 
  const bool bUseAbsoluteValues;
};

/**
 * This class enables the splitting of histograms into n histograms as a function of chosen variables
 * Primary use case: splitting of QCD measurement into bins of tau pt
 */
class HistoSplitter {
public:
  using SplittedTH1s = std::vector<WrappedTH1*>;
  using SplittedTH2s = std::vector<WrappedTH2*>;
  
  HistoSplitter(const ParameterSet& config, HistoWrapper& histoWrapper);
  ~HistoSplitter();
  
  /// Books histograms (info about binning)
  void bookHistograms(TDirectory* dir);
  /// Reset pointer to current bin (call this at the beginning of each event; prevents double-counting of events)
  void initialize();
  /// Set pointer to current bin (call this for each event before filling the first histogram!)
  void setFactorisationBinForEvent(const std::vector<float>& values=std::vector<float>{});
  /// Create a histogram for a shape in factorisation bins using unfolding of splitted bins to y-axis
  void createShapeHistogram(const HistoLevel level, TDirectory* dir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, const std::string& title, const std::string& label, int nbins, double min, double max);
  /// Create a histogram for a 1D shape in factorisation bins
  void createShapeHistogram(const HistoLevel level, TDirectory* dir, SplittedTH1s& histoContainer, const std::string& title, const std::string& label, int nbins, double min, double max);
  /// Create a histogram for a 2D shape in factorisation bins
  void createShapeHistogram(const HistoLevel level, TDirectory* dir, SplittedTH2s& histoContainer, const std::string& title, const std::string& label, int nbinsX, double minX, double maxX, int nbinsY, double minY, double maxY);
  /// Fill method for a factorisation histogram containting a shape
  void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value);
  /// Fill method for a factorisation histogram containting a shape, with unconventional weight
  void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight);
  /// Fill method for a factorisation histogram containting a shape
  void fillShapeHistogram(SplittedTH1s& histoContainer, double value);
  /// Fill method for a factorisation histogram containting a shape, with unconventional weight
  void fillShapeHistogram(SplittedTH1s& histoContainer, double value, double weight);
  /// Fill method for a 2D factorisation histogram containting a shape
  void fillShapeHistogram(SplittedTH2s& histoContainer, double valueX, double valueY);
  /// Fill method for a 2D factorisation histogram containting a shape, with unconventional weight
  void fillShapeHistogram(SplittedTH2s& histoContainer, double valueX, double valueY, double weight);

protected: // Protected for easier unit testing
  /// Returns index to unfolded bin index
  const size_t getShapeBinIndex() const;
  /// Convert unfolded bin index into separate indices
  const std::vector<size_t> obtainIndicesFromUnfoldedIndex(size_t unfoldedIndex) const;
  /// Constructs labels for the y axis
  void setAxisLabelsForUnfoldedHisto(WrappedUnfoldedFactorisationHisto* h) const;
  /// Check if the bin was updated for the event after calling initialize()
  void checkIndexValidity() const;
  /// Get description string for a specific bin
  const std::string getFullBinDescriptionStringByBinIndex(const std::vector<size_t>& indices) const;
  
private:
  /// Copy of histowrapper for creating histograms
  HistoWrapper& fHistoWrapper;
  /// Containers of specs for splitting histograms as function of a variable
  std::vector<HistoSplitterItem> fHistoSplitterItems;
  
  // Internal variables
  /// Total number of splitted bins (excluding inclusive bin)
  size_t fNUnfoldedBins;
  /// String holding the info of the binning
  std::string fBinningString;
  /// Validity of current bin
  bool bIndicesAreValid;
  /// Indices of the current bin
  std::vector<size_t> fCurrentBinIndex;
  /// Unfolded index (in range 0..fNUnfoldedBins-1) for the current bin
  size_t fCurrentUnfoldedBinIndex;
  
  /// Histogram for binning information (used by QCD measurement scripts)
  WrappedTH1* hBinInfo;
};


#endif
