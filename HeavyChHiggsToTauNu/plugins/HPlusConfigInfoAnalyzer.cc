#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

#include<limits>
#include<string>

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
  std::string dataVersion;
  double crossSection;
  bool isData;
  bool hasCrossSection;
  bool hasIsData;
};

HPlusConfigInfoAnalyzer::HPlusConfigInfoAnalyzer(const edm::ParameterSet& pset): 
  dataVersion(pset.getUntrackedParameter<std::string>("dataVersion", "")),
  crossSection(std::numeric_limits<double>::quiet_NaN()),
  isData(false),
  hasCrossSection(false), hasIsData(false)
{
  if(pset.exists("crossSection")) {
    crossSection = pset.getUntrackedParameter<double>("crossSection");
    hasCrossSection = true;
  }
  if(pset.exists("isData")) {
    isData = pset.getUntrackedParameter<bool>("isData");
    hasIsData = true;
  }
}

HPlusConfigInfoAnalyzer::~HPlusConfigInfoAnalyzer() {}

void HPlusConfigInfoAnalyzer::beginJob() {
}

void HPlusConfigInfoAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusConfigInfoAnalyzer::endJob() {
  edm::Service<TFileService> fs;

  int nbins = 1+hasCrossSection+hasIsData;
  TH1F *info = fs->make<TH1F>("configinfo", "configinfo", nbins, 0, nbins);

  int bin = 1;
  info->GetXaxis()->SetBinLabel(bin, "control");
  info->AddBinContent(bin, 1);
  ++bin;

  if(hasCrossSection) {
    info->GetXaxis()->SetBinLabel(bin, "crossSection");
    info->AddBinContent(bin, crossSection);
    ++bin;
  }
  if(hasIsData) {
    info->GetXaxis()->SetBinLabel(bin, "isData");
    info->AddBinContent(bin, isData);
    ++bin;
  }

  TNamed *dv = fs->make<TNamed>("dataVersion", dataVersion.c_str());

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusConfigInfoAnalyzer);
