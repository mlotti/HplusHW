#include "EventSelection/interface/CommonPlots.h"

CommonPlots::CommonPlots(const ParameterSet& config, const AnalysisType type, HistoWrapper& histoWrapper)
: fAnalysisType(type),
  //===== Histogram splitter
  fHistoSplitter(config, histoWrapper),
  //===== Settings for histogram binning
  fPtBinSettings(config.getParameter<ParameterSet>("ptBins")),
  fEtaBinSettings(config.getParameter<ParameterSet>("etaBins")),
  fPhiBinSettings(config.getParameter<ParameterSet>("phiBins")),
  fDeltaPhiBinSettings(config.getParameter<ParameterSet>("deltaPhiBins")),
  fRtauBinSettings(config.getParameter<ParameterSet>("rtauBins")),
  fNjetsBinSettings(config.getParameter<ParameterSet>("njetsBins")),
  fMetBinSettings(config.getParameter<ParameterSet>("metBins")),
  fBJetDiscriminatorBinSettings(config.getParameter<ParameterSet>("bjetDiscrBins")),
  fAngularCuts1DSettings(config.getParameter<ParameterSet>("angularCuts1DBins")),
  //fTopMassBinSettings(config.getParameter<ParameterSet>("topMassBins")),
  //fWMassBinSettings(config.getParameter<ParameterSet>("WMassBins")),
  fMtBinSettings(config.getParameter<ParameterSet>("mtBins"))
  //fInvmassBinSettings(config.getParameter<ParameterSet>("invmassBins")),
{

}

CommonPlots::~CommonPlots() { }

void CommonPlots::book(TDirectory *dir) { 
  fHistoSplitter.bookHistograms(dir);
  
}