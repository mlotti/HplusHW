#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SplittedHistogramHandler.h"

#include <iomanip>

namespace HPlus {
  SplittedHistogramHandler::SplittedHistogramHandler(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper) :
    fHistoWrapper(histoWrapper) {
    // Create histogram with binning information
    edm::Service<TFileService> fs;
    hBinInfo = histoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "SplittedBinInfo", "SplittedBinInfo", 3, 0, 3.);
    std::stringstream s;
    // tau pt binning
    if (iConfig.exists("splitHistogramByTauPtBinLowEdges")) {
      fTauPtBinLowEdges = iConfig.getUntrackedParameter<std::vector<double> >("splitHistogramByTauPtBinLowEdges");
      s << "TauPt:" << fTauPtBinLowEdges.size()+1;
    }
    if (hBinInfo->isActive()) {
      hBinInfo->getHisto()->GetXaxis()->SetBinLabel(1, "TauPt");
      hBinInfo->SetBinContent(1, fTauPtBinLowEdges.size()+1);
    }
    // tau eta binning
    if (iConfig.exists("splitHistogramByTauEtaBinLowEdges")) {
      fTauEtaBinLowEdges = iConfig.getUntrackedParameter<std::vector<double> >("splitHistogramByTauEtaBinLowEdges");
      s << ":TauEta:" << fTauEtaBinLowEdges.size()+1;
    }
    if (hBinInfo->isActive()) {
      hBinInfo->getHisto()->GetXaxis()->SetBinLabel(2, "TauEta");
      hBinInfo->SetBinContent(2, fTauEtaBinLowEdges.size()+1);
    }
    // Nvertices binning
    if (iConfig.exists("splitHistogramByNVerticesBinLowEdges")) {
      fNVerticesBinLowEdges = iConfig.getUntrackedParameter<std::vector<int> >("splitHistogramByNVerticesBinLowEdges");
      s << ":Nvtx:" << fNVerticesBinLowEdges.size()+1;
    }
    if (hBinInfo->isActive()) {
      hBinInfo->getHisto()->GetXaxis()->SetBinLabel(3, "Nvtx");
      hBinInfo->SetBinContent(3, fNVerticesBinLowEdges.size()+1);
    }
    // Set binning info prefix string
    s << ":";
    fBinningString = s.str();
    // Set overall number of bins (+1 because one needs to add the underflow bin)
    fNUnfoldedBins = (static_cast<int>(fTauPtBinLowEdges.size()) + 1) *
                     (static_cast<int>(fTauEtaBinLowEdges.size()) + 1) *
                     (static_cast<int>(fNVerticesBinLowEdges.size()) + 1);
    // Set default bin index values
    initialize();
  }

  SplittedHistogramHandler::~SplittedHistogramHandler() { }

  void SplittedHistogramHandler::initialize() {
    fCurrentTauPtBinIndex = 9999;
    fCurrentTauEtaBinIndex = 9999;
    fCurrentNvtxBinIndex = 9999;
    fCurrentUnfoldedBinIndex = 9999;
  }

  void SplittedHistogramHandler::setFactorisationBinForEvent(double pt, double eta, int nvtx) {
    fCurrentTauPtBinIndex = getTauPtBinIndex(pt);
    fCurrentTauEtaBinIndex = getTauEtaBinIndex(eta);
    fCurrentNvtxBinIndex = getNVerticesBinIndex(nvtx);
    fCurrentUnfoldedBinIndex = getShapeBinIndex(fCurrentTauPtBinIndex, fCurrentTauEtaBinIndex, fCurrentNvtxBinIndex);
  }

  void SplittedHistogramHandler::createShapeHistogram(HistoWrapper::HistoLevel level, TFileDirectory& fdir, WrappedUnfoldedFactorisationHisto*& unfoldedHisto, std::string title, std::string label, int nbins, double min, double max) {
    // x-axis contains distribution, y-axis contains unfolded factorisation bins (including under- and overflows)
    // Create histo
    std::string s = fBinningString+title+";"+label;
    unfoldedHisto = fHistoWrapper.makeTH<TH2F>(fNUnfoldedBins, level, fdir, title.c_str(), s.c_str(), nbins, min, max);
    // Set labels to y-axis
    setAxisLabelsForUnfoldedHisto(unfoldedHisto);
  }

  void SplittedHistogramHandler::createShapeHistogram(HistoWrapper::HistoLevel level, TFileDirectory& fdir, std::vector<WrappedTH1*>& histoContainer, std::string title, std::string label, int nbins, double min, double max) {
    if (fNUnfoldedBins == 1) {
      // Create just one histogram
      std::string myHistoTitle = getFullBinDescriptionStringByBinIndex(0, 0, 0) + ";" + label;
      histoContainer.push_back(fHistoWrapper.makeTH<TH1F>(level, fdir, title.c_str(), myHistoTitle.c_str(), nbins, min, max));
      return;
    }

    // Create directory for the N x TH1 histograms, where N is the number of unfolded bins
    TFileDirectory myDir = fdir.mkdir(title.c_str());
    // Create N x TH1 histograms, where N is the number of unfolded bins
    int myTauPtBinIndexs = static_cast<int>(fTauPtBinLowEdges.size()) + 1;
    int myTauEtaBinIndexs = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    for (int k = 0; k < myNVerticesBins; ++k) {
      for (int j = 0; j < myTauEtaBinIndexs; ++j) {
        for (int i = 0; i < myTauPtBinIndexs; ++i) {
          std::stringstream s;
          s << title.c_str() << getShapeBinIndex(i,j,k);
          std::string myHistoTitle = getFullBinDescriptionStringByBinIndex(i, j, k) + ";" + label;
          histoContainer.push_back(fHistoWrapper.makeTH<TH1F>(level, myDir, s.str().c_str(), myHistoTitle.c_str(), nbins, min, max));
        }
      }
    }
  }

  void SplittedHistogramHandler::fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value) {
    checkProperBinning();
    h->Fill(value, fCurrentUnfoldedBinIndex);
    //std::cout << "Filling shape " << h->getHisto()->GetTitle() << " current bin=" << fCurrentUnfoldedBinIndex << std::endl;
  }

  void SplittedHistogramHandler::fillShapeHistogram(WrappedUnfoldedFactorisationHisto* h, double value, double weight) {
    checkProperBinning();
    h->Fill(value, fCurrentUnfoldedBinIndex, weight);
  }

  void SplittedHistogramHandler::fillShapeHistogram(std::vector<WrappedTH1*>& histoContainer, double value) {
    checkProperBinning();
    histoContainer[fCurrentUnfoldedBinIndex]->Fill(value);
  }

  void SplittedHistogramHandler::fillShapeHistogram(std::vector<WrappedTH1*>& histoContainer, double value, double weight) {
    checkProperBinning();
    histoContainer[fCurrentUnfoldedBinIndex]->Fill(value, weight);
  }

  size_t SplittedHistogramHandler::getTauPtBinIndex(double pt) const {
    size_t mySize = fTauPtBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (pt < fTauPtBinLowEdges[i])
        return i;
    }
    return mySize;
  }

  size_t SplittedHistogramHandler::getTauEtaBinIndex(double eta) const {
    size_t mySize = fTauEtaBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (eta < fTauEtaBinLowEdges[i])
        return i;
    }
    return mySize;
  }

  size_t SplittedHistogramHandler::getNVerticesBinIndex(int nvtx) const {
    size_t mySize = fNVerticesBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (nvtx < fNVerticesBinLowEdges[i])
        return i;
    }
    return mySize;
  }

  size_t SplittedHistogramHandler::getShapeBinIndex(size_t tauPtBinIndex, size_t tauEtaBinIndex, size_t nvtxBinIndex) const {
    size_t myTauPtBins = fTauPtBinLowEdges.size() + 1;
    size_t myTauEtaBins = fTauEtaBinLowEdges.size() + 1;
    //int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    //std::cout << " bin=" << tauPtBin << " taueta=" << tauEtaBin << " nvtx=" << nvtxBin << std::endl;
    //std::cout << "total index=" << nvtxBin + tauEtaBin*myNVerticesBins + tauPtBin*myNVerticesBins*myTauEtaBinIndexs << endl;
    return tauPtBinIndex + tauEtaBinIndex*myTauPtBins + nvtxBinIndex*myTauPtBins*myTauEtaBins;
  }

  void SplittedHistogramHandler::setAxisLabelsForUnfoldedHisto(WrappedUnfoldedFactorisationHisto* h) const {
    if (!h->isActive()) return;
    size_t myTauPtBinIndex = fTauPtBinLowEdges.size() + 1;
    size_t myTauEtaBinIndex = fTauEtaBinLowEdges.size() + 1;
    size_t myNVerticesBins = fNVerticesBinLowEdges.size() + 1;
    for (size_t k = 0; k < myNVerticesBins; ++k) {
      for (size_t j = 0; j < myTauEtaBinIndex; ++j) {
        for (size_t i = 0; i < myTauPtBinIndex; ++i) {
          std::string myInfoString = getFullBinDescriptionStringByBinIndex(i, j, k);
          h->getHisto()->GetYaxis()->SetBinLabel(getShapeBinIndex(i,j,k)+1, myInfoString.c_str());
        }
      }
    }
  }

  void SplittedHistogramHandler::checkProperBinning() const {
    if (fCurrentTauPtBinIndex == 9999 || fCurrentTauEtaBinIndex == 9999 || fCurrentNvtxBinIndex == 9999 || fCurrentUnfoldedBinIndex == 9999)
      throw cms::Exception("Logic") << "Need to call SplittedHistogramHandler::setFactorisationBinForEvent() for the event! Check your code!";
  }

  std::string SplittedHistogramHandler::getFullBinDescriptionStringByBinIndex(size_t tauPtBinIndex, size_t tauEtaBinIndex, size_t nvtxBinIndex) const {
    std::stringstream s;
    // tau pT
    if (fTauPtBinLowEdges.size()) {
      s << getBinDescriptionString("#tau p_{T}", tauPtBinIndex, fTauPtBinLowEdges, 0);
    }
    // tau eta
    if (fTauEtaBinLowEdges.size()) {
      if (s.str().size()) s << "/";
      s << getBinDescriptionString("#tau eta", tauEtaBinIndex, fTauEtaBinLowEdges, 2);
    }
    // Nvertices
    if (fNVerticesBinLowEdges.size()) {
      if (s.str().size()) s << "/";
      s << getBinDescriptionString("N_{vtx}", nvtxBinIndex, fNVerticesBinLowEdges, 0);
    }
    if (!s.str().size()) {
      s << "all bins";
    }
    return s.str();
  }

  std::string SplittedHistogramHandler::getBinDescriptionString(std::string label, size_t binIndex, const std::vector<int>& container, int precision) const {
    std::stringstream s;
    if (binIndex == 0)
      s << label << "<" << std::setprecision(precision) << static_cast<int>(container[0]);
    else if (binIndex == container.size())
      s << label << ">" << std::setprecision(precision) << static_cast<int>(container[container.size()-1]);
    else
      s << label << "=" << std::setprecision(precision) << static_cast<int>(container[binIndex-1]) << ".." << std::setprecision(precision) << static_cast<int>(container[binIndex]);
    return s.str();
  }

  std::string SplittedHistogramHandler::getBinDescriptionString(std::string label, size_t binIndex, const std::vector<double>& container, int precision) const {
    std::stringstream s;
    if (binIndex == 0)
      s << label << "<" << std::fixed << std::setprecision(precision) << static_cast<double>(container[0]);
    else if (binIndex == container.size())
      s << label << ">" << std::fixed << std::setprecision(precision) << static_cast<double>(container[container.size()-1]);
    else
      s << label << "=" << std::fixed << std::setprecision(precision) << static_cast<double>(container[binIndex-1]) << ".." << std::fixed << std::setprecision(precision) << static_cast<double>(container[binIndex]);
    return s.str();
  }

}