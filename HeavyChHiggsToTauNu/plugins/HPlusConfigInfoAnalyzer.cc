#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

#include<iostream>

class HPlusConfigInfoAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusConfigInfoAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusConfigInfoAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

private:
  double crossSection;
};

HPlusConfigInfoAnalyzer::HPlusConfigInfoAnalyzer(const edm::ParameterSet& pset): 
  crossSection(pset.getUntrackedParameter<double>("crossSection"))
{}

HPlusConfigInfoAnalyzer::~HPlusConfigInfoAnalyzer() {}

void HPlusConfigInfoAnalyzer::beginJob() {
}

void HPlusConfigInfoAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusConfigInfoAnalyzer::endJob() {
  edm::Service<TFileService> fs;
  TH1F *info = fs->make<TH1F>("configinfo", "configinfo", 2, 0, 2);

  info->GetXaxis()->SetBinLabel(1, "control");
  info->GetXaxis()->SetBinLabel(2, "crossSection");

  info->AddBinContent(1, 1);
  info->AddBinContent(2, crossSection);

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusConfigInfoAnalyzer);
