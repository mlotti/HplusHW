// -*- c++ -*-
#ifndef EventSelection_CommonPlotsHelper_h
#define EventSelection_CommonPlotsHelper_h

#include <vector>
#include <string>

class Tau;

class CommonPlotsHelper {
public:
  CommonPlotsHelper();
  ~CommonPlotsHelper() { }
  
  //===== Tau source plot
  /// Returns number of bins for tau source histogram
  int getTauSourceBinCount() const { return static_cast<int>(tauSourceBinLabels.size()); }
  /// Returns string for bin label (index range : 0..NbinsX-1)
  std::string getTauSourceBinLabel(int i) const { return tauSourceBinLabels[i]; }
  /// Returns vector of bin indices that need to be filled
  std::vector<int> getTauSourceData(bool isRealData, const Tau& tau) const;
  
private:
  std::vector<std::string> tauSourceBinLabels;
  
};

#endif

