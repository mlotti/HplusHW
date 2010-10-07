#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

#include <string>

class HPlusCandViewMultiplicityAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusCandViewMultiplicityAnalyzer(const edm::ParameterSet& iConfig);
  /// Default EDAnalyzer destructor
  ~HPlusCandViewMultiplicityAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  edm::InputTag src_;
  TH1 *histo_;
};


HPlusCandViewMultiplicityAnalyzer::HPlusCandViewMultiplicityAnalyzer(const edm::ParameterSet& iConfig):
  src_(iConfig.getParameter<edm::InputTag>("src")),
  histo_(0)
{
  edm::Service<TFileService> fs;

  std::string title("multiplicity");
  if(iConfig.exists("title"))
    title = iConfig.getUntrackedParameter<std::string>("title");
  histo_ = fs->make<TH1F>("multiplicity", title.c_str(),
                          iConfig.getUntrackedParameter<int>("nbins"),
                          iConfig.getUntrackedParameter<int>("min"),
                          iConfig.getUntrackedParameter<int>("max"));

}

HPlusCandViewMultiplicityAnalyzer::~HPlusCandViewMultiplicityAnalyzer() {}

void HPlusCandViewMultiplicityAnalyzer::beginJob() {}

void HPlusCandViewMultiplicityAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(src_, hcands);

  histo_->Fill(hcands->size());

}

void HPlusCandViewMultiplicityAnalyzer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewMultiplicityAnalyzer);
