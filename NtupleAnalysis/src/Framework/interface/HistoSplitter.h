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
  using SplittedTH3s = std::vector<WrappedTH3*>;
  using SplittedTripletTH1s = std::vector<WrappedTH1Triplet*>;
  using SplittedTripletTH2s = std::vector<WrappedTH2Triplet*>;
  using SplittedTripletTH3s = std::vector<WrappedTH3Triplet*>;
  
  HistoSplitter(const ParameterSet& config, HistoWrapper& histoWrapper);
  ~HistoSplitter();

  /// Books histograms (info about binning)
  void bookHistograms(TDirectory* dir);
  /// Reset pointer to current bin (call this at the beginning of each event; prevents double-counting of events)
  void initialize();
  /// Set pointer to current bin (call this for each event before filling the first histogram!)
  void setFactorisationBinForEvent(const std::vector<float>& values=std::vector<float>{});

  //===== Creating histograms
  /// Create a histogram for a shape in factorisation bins using unfolding of splitted bins to y-axis
  void createShapeHistogram(HistoLevel level, TDirectory* dir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, const std::string& title, const std::string& label, int nbins, double min, double max);
  /// Create a histogram for a 1D shape in factorisation bins
  template<typename T, typename ...Args> 
  void createShapeHistogram(HistoLevel level, TDirectory* dir, std::vector<typename HistoWrapperTraits<T>::type *>& histoContainer, const std::string& title, const std::string& label, Args&&... args);
  /// Create a histogram for a triplet shape in factorisation bins
  template<typename T, typename ...Args> 
  void createShapeHistogramTriplet(bool enableTrueHistogram, HistoLevel level, std::vector<TDirectory*>&, std::vector<typename HistoWrapperTripletTraits<T>::type *>& histoContainer, const std::string& title, const std::string& label, Args&&... args);
  
  //===== Filling histograms
  /// Fill method for a factorisation histogram containting a shape
  void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value);
  /// Fill method for a factorisation histogram containting a shape, with unconventional weight
  void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight);
  /// Fill method for a factorisation histogram containting a shape
  template<typename T, typename ...Args>
  void fillShapeHistogram(std::vector<T*>& histoContainer, Args&&... args);
  /// Fill method for a factorisation histogram containting a shape triplet
  template<typename T, typename ...Args>
  void fillShapeHistogramTriplet(std::vector<T*>& histoContainer, bool status, Args&&... args);
  
  //===== Editing histograms
  /// Set bin labels
  template<typename T>
  void SetBinLabel(std::vector<T*>& histoContainer, int i, std::string label);
  
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

//===== Implementation of templates

template<typename T, typename ...Args> 
void HistoSplitter::createShapeHistogram(HistoLevel level, TDirectory* dir, std::vector<typename HistoWrapperTraits<T>::type *>& histoContainer, const std::string& title, const std::string& label, Args&&... args) {
  if (fNUnfoldedBins == 1) { // Create just one histogram
    histoContainer.push_back(fHistoWrapper.makeTH<T>(level, dir, title.c_str(), label.c_str(), std::forward<Args>(args)...));
    return;
  }
  // Create directory for the N x THx histograms, where N is the number of unfolded bins
  TDirectory* myDir = dir->mkdir(title.c_str());
  // Create N x THx histograms, where N is the number of unfolded bins
  for (size_t i = 0; i < fNUnfoldedBins; ++i) {
    std::stringstream s;
    s << title.c_str() << i;
    std::string myHistoTitle = getFullBinDescriptionStringByBinIndex(obtainIndicesFromUnfoldedIndex(i)) + ";" + label;
    histoContainer.push_back(fHistoWrapper.makeTH<T>(level, myDir, s.str().c_str(), myHistoTitle.c_str(), std::forward<Args>(args)...));
  }
  // Create inclusive histogram
  std::string myTitle = title+"Inclusive";
  histoContainer.push_back(fHistoWrapper.makeTH<T>(level, myDir, myTitle.c_str(), myTitle.c_str(), std::forward<Args>(args)...));
}
/// Create a histogram for a triplet shape in factorisation bins
template<typename T, typename ...Args> 
void HistoSplitter::createShapeHistogramTriplet(bool enableTrueHistogram, HistoLevel level, std::vector<TDirectory*>& dir, std::vector<typename HistoWrapperTripletTraits<T>::type *>& histoContainer, const std::string& title, const std::string& label, Args&&... args) {
  if (fNUnfoldedBins == 1) { // Create just one histogram
    histoContainer.push_back(fHistoWrapper.makeTHTriplet<T>(enableTrueHistogram, level, dir, title.c_str(), label.c_str(), std::forward<Args>(args)...));
    return;
  }
  // Create separate directories for the N x THx histograms, where N is the number of unfolded bins
  std::vector <TDirectory*> splittedDirs;
  for (const auto& p: dir) {
    splittedDirs.push_back(p->mkdir(title.c_str())); // Note that base directory is separate
  }
  // Create the N x THx histograms, where N is the number of unfolded bins
  for (size_t i = 0; i < fNUnfoldedBins; ++i) {
    std::stringstream s;
    s << title.c_str() << i;
    std::string myHistoTitle = getFullBinDescriptionStringByBinIndex(obtainIndicesFromUnfoldedIndex(i)) + ";" + label;
    histoContainer.push_back(fHistoWrapper.makeTHTriplet<T>(enableTrueHistogram, level, splittedDirs, s.str().c_str(), myHistoTitle.c_str(), std::forward<Args>(args)...));
  }
  // Create inclusive histogram
  std::string myTitle = title+"Inclusive";
  histoContainer.push_back(fHistoWrapper.makeTHTriplet<T>(enableTrueHistogram, level, splittedDirs, myTitle.c_str(), myTitle.c_str(), std::forward<Args>(args)...));
}

template<typename T, typename ...Args>
void HistoSplitter::fillShapeHistogram(std::vector<T*>& histoContainer, Args&&... args) {
  checkIndexValidity();
  histoContainer[fCurrentUnfoldedBinIndex]->Fill(std::forward<Args>(args)...);
  // Fill inclusive histogram
  if (fNUnfoldedBins > 1)
    histoContainer[histoContainer.size()-1]->Fill(std::forward<Args>(args)...);
}

template<typename T, typename ...Args>
void HistoSplitter::fillShapeHistogramTriplet(std::vector<T*>& histoContainer, bool status, Args&&... args) {
  checkIndexValidity();
  histoContainer[fCurrentUnfoldedBinIndex]->Fill(status, std::forward<Args>(args)...);
  // Fill inclusive histogram
  if (fNUnfoldedBins > 1)
    histoContainer[histoContainer.size()-1]->Fill(status, std::forward<Args>(args)...);
}

template<typename T>
void HistoSplitter::SetBinLabel(std::vector<T*>& histoContainer, int i, std::string label) {
  for (auto p: histoContainer) {
    p->SetBinLabel(i, label);
  }
}

#endif
