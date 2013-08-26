#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"

#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

#include<iostream>

class HPlusGenRunInfoAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusGenRunInfoAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusGenRunInfoAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  virtual void endRun(const edm::Run& run, const edm::EventSetup & setup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  edm::InputTag src_;
  TH1F *info;
};

HPlusGenRunInfoAnalyzer::HPlusGenRunInfoAnalyzer(const edm::ParameterSet& pset): 
  src_(pset.getUntrackedParameter<edm::InputTag>("src")),
  info(0)
{}

HPlusGenRunInfoAnalyzer::~HPlusGenRunInfoAnalyzer() {}

void HPlusGenRunInfoAnalyzer::beginJob() {
  edm::Service<TFileService> fs;
  info = fs->make<TH1F>("geninfo", "geninfo", 2, 0, 2);

  info->GetXaxis()->SetBinLabel(1, "control");
  info->GetXaxis()->SetBinLabel(2, "crossSection");
}

void HPlusGenRunInfoAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusGenRunInfoAnalyzer::endRun(const edm::Run& run, const edm::EventSetup& setup) {
  edm::Handle<GenRunInfoProduct> runInfo;
  run.getByLabel(src_, runInfo);

  // Allow running also on collision data
  if(!runInfo.isValid())
    return;

  info->AddBinContent(1, 1);
  info->AddBinContent(2, runInfo->crossSection());

  /*
  std::cout << "#######################################################" << std::endl;
  std::cout << "#" << std::endl;
  std::cout << "# Cross section " << runInfo->crossSection() << std::endl;
  std::cout << "#" << std::endl;
  std::cout << "#######################################################" << std::endl;
  */

}

void HPlusGenRunInfoAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGenRunInfoAnalyzer);
