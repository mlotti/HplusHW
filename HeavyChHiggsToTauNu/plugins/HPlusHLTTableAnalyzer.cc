#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <string>

class HPlusHLTTableAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusHLTTableAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusHLTTableAnalyzer();

 private:
  virtual void beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup);
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  HLTConfigProvider hltConfigProvider;
  std::string hltProcessName;
};


HPlusHLTTableAnalyzer::HPlusHLTTableAnalyzer(const edm::ParameterSet& iConfig):
  hltProcessName(iConfig.getUntrackedParameter<std::string>("hltProcessName"))
{}

HPlusHLTTableAnalyzer::~HPlusHLTTableAnalyzer() {}

void HPlusHLTTableAnalyzer::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup) {
  const char *cat = "HLTTableInfo";

  bool changed = false;
  bool success = hltConfigProvider.init(iRun, iSetup, hltProcessName, changed);
  /*
  if(!success) {
    edm::LogError(cat) << "HLTConfigProvider::init() returned false!" << std::endl;
    return;
  }
  */

  if(!success)
    throw cms::Exception("LogicError", "HLTConfigProvider::init() returned false!");

  edm::LogVerbatim(cat) << "Run " << iRun.run() 
                        << " HLT process '" << hltProcessName << "'"
                        << " HLT table '" << hltConfigProvider.tableName() << "'"
                        << std::endl;
}

void HPlusHLTTableAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}


//define this as a plug-in
DEFINE_FWK_MODULE(HPlusHLTTableAnalyzer);
