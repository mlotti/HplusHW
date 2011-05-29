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

  struct Data {
    Data(edm::InputTag s, TH1 *h): src(s), histo(h) {}

    edm::InputTag src;
    TH1 *histo;
  };

  std::vector<Data> data_;
  edm::InputTag weights_;
  bool usingWeights_;
};


HPlusCandViewMultiplicityAnalyzer::HPlusCandViewMultiplicityAnalyzer(const edm::ParameterSet& iConfig):
  weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag("fake"))),
  usingWeights_(iConfig.exists("weights") {
  edm::Service<TFileService> fs;

  std::vector<std::string> names = iConfig.getParameterNamesForType<edm::ParameterSet>(false); // take only untracked parameters
  data_.reserve(names.size());

  for(size_t i=0; i<names.size(); ++i) {
    edm::ParameterSet pset = iConfig.getUntrackedParameter<edm::ParameterSet>(names[i]);
    
    std::string title("multiplicity");
    std::string name = names[i]+"_multiplicity";
    if(iConfig.exists("title"))
      title = pset.getUntrackedParameter<std::string>("title");
    TH1 *histo = fs->make<TH1F>(name.c_str(), title.c_str(),
                                pset.getUntrackedParameter<int>("nbins"),
                                pset.getUntrackedParameter<int>("min"),
                                pset.getUntrackedParameter<int>("max"));
    data_.push_back(Data(pset.getParameter<edm::InputTag>("src"), histo));
  }
}

HPlusCandViewMultiplicityAnalyzer::~HPlusCandViewMultiplicityAnalyzer() {}

void HPlusCandViewMultiplicityAnalyzer::beginJob() {}

void HPlusCandViewMultiplicityAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;
  if(usingWeights_) {
    edm::Handle<double> hweight;
    iEvent.getByLabel(weights_, hweight);
    weight = *hweight;
  }

  for(size_t i=0; i<data_.size(); ++i) {
    edm::Handle<edm::View<reco::Candidate> > hcands;
    iEvent.getByLabel(data_[i].src, hcands);

    data_[i].histo->Fill(hcands->size(), weight);
  }
}

void HPlusCandViewMultiplicityAnalyzer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewMultiplicityAnalyzer);
