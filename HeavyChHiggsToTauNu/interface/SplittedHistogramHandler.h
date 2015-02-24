// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SplittedHistogramHandler
#define HiggsAnalysis_HeavyChHiggsToTauNu_SplittedHistogramHandler_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <string>
#include <vector>

namespace edm {
  class ParameterSet;
}

namespace HPlus {

  class SplittedHistogramHandler {
  public:
    SplittedHistogramHandler(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper, bool doInfoHistogram=true);
    ~SplittedHistogramHandler();
    /// Reset pointer to current bin
    void initialize();
    /// Set pointer to current bin
    void setFactorisationBinForEvent(double pt, double eta, int nvtx, double deltaPhiTauMetInDegrees);
    /// Create a histogram for a shape in factorisation bins
    void createShapeHistogram(HistoWrapper::HistoLevel level, TFileDirectory& fdir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, std::string title, std::string label, int nbins, double min, double max);
    /// Create a histogram for a shape in factorisation bins
    void createShapeHistogram(HistoWrapper::HistoLevel level, TFileDirectory& fdir, std::vector<WrappedTH1*>& histoContainer, std::string title, std::string label, int nbins, double min, double max);
    /// Create a histogram for a 2D shape in factorisation bins
    void createShapeHistogram(HistoWrapper::HistoLevel level, TFileDirectory& fdir, std::vector<WrappedTH2*>& histoContainer, std::string title, std::string label, int nbinsX, double minX, double maxX, int nbinsY, double minY, double maxY);
    /// Fill method for a factorisation histogram containting a shape
    void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value);
    /// Fill method for a factorisation histogram containting a shape, with unconventional weight
    void fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight);
    /// Fill method for a factorisation histogram containting a shape
    void fillShapeHistogram(std::vector<WrappedTH1*>& histoContainer, double value);
    /// Fill method for a factorisation histogram containting a shape, with unconventional weight
    void fillShapeHistogram(std::vector<WrappedTH1*>& histoContainer, double value, double weight);
    /// Fill method for a 2D factorisation histogram containting a shape
    void fillShapeHistogram(std::vector<WrappedTH2*>& histoContainer, double valueX, double valueY);
    /// Fill method for a 2D factorisation histogram containting a shape, with unconventional weight
    void fillShapeHistogram(std::vector<WrappedTH2*>& histoContainer, double valueX, double valueY, double weight);

  private:
    /// Returns index to tau pT bin; 0 is underflow and size() is highest bin
    size_t getTauPtBinIndex(double pt) const;
    /// Returns index to tau eta bin; 0 is underflow and size() is highest bin
    size_t getTauEtaBinIndex(double eta) const;
    /// Returns index to nvtx bin; 0 is underflow and size() is highest bin
    size_t getNVerticesBinIndex(int nvtx) const;
    /// Returns index to delta phi(tau,MET) bin; 0 is underflow and size() is highest bin
    size_t getDeltaPhiTauMetBinIndex(double degrees) const;
    /// Returns index to unfolded bin index
    size_t getShapeBinIndex(size_t tauPtBinIndex, size_t tauEtaBinIndex, size_t nvtxBinIndex, size_t deltaPhiTauMetBinIndex) const;
    /// Constructs labels for the y axis
    void setAxisLabelsForUnfoldedHisto(WrappedUnfoldedFactorisationHisto* h) const;
    /// Check if the bin was updated for the event after calling initialize()
    void checkProperBinning() const;
    /// Get description string for all splits
    std::string getFullBinDescriptionStringByBinIndex(size_t tauPtBinIndex, size_t tauEtaBinIndex, size_t nvtxBinIndex, size_t deltaPhiTauMetBinIndex) const;
    /// Get description string for a given split
    std::string getBinDescriptionString(std::string label, size_t binIndex, const std::vector<int>& container, int precision) const;
    /// Get description string for a given split
    std::string getBinDescriptionString(std::string label, size_t binIndex, const std::vector<double>& container, int precision) const;

  private:
    HistoWrapper& fHistoWrapper;
    // Input settings
    std::vector<double> fTauPtBinLowEdges;
    std::vector<double> fTauEtaBinLowEdges;
    std::vector<int> fNVerticesBinLowEdges;
    std::vector<double> fDeltaPhiTauMetBinLowEdges;
    // Internal variables
    int fNUnfoldedBins;
    std::string fBinningString; // string holding the info of the binning
    // Pointer to current bin
    size_t fCurrentTauPtBinIndex;
    size_t fCurrentTauEtaBinIndex;
    size_t fCurrentNvtxBinIndex;
    size_t fCurrentDeltaPhiTauMetBinIndex;
    size_t fCurrentUnfoldedBinIndex;
    // Histogram for binning informatio
    WrappedTH1* hBinInfo;
  };
}
#endif
