#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include<algorithm>
#include<functional>

namespace {
  template <typename T>
  struct PairFirstEq: public std::binary_function<T, std::string, bool> {
    bool operator()(const T& pair, const std::string& name) const {
      return name == pair.first;
    }
  };

  struct CallValidate {
    CallValidate(const edm::Event& iEvent): event(iEvent) {}
    template <typename T>
    void operator()(T& obj) const {
      obj.validate(event);
    }
    const edm::Event& event;
  };

  class ElectronValidation {
  public:
    /*
    ElectronValidation(const edm::InputTag& src, const std::vector<std::string>& ids):
      src_(src), ids_(ids) {}
    */
    ElectronValidation(const edm::ParameterSet& iConfig):
      src_(iConfig.getUntrackedParameter<edm::InputTag>("src")),
      ids_(iConfig.getUntrackedParameter<std::vector<std::string> >("electronIDs")) {}

    void validate(const edm::Event& iEvent) {
      edm::Handle<edm::View<pat::Electron> > hele;
      iEvent.getByLabel(src_, hele);

      if(!hele->empty()) {
        const pat::Electron& ele = hele->at(0);
        const std::vector<pat::Electron::IdPair>& ids = ele.electronIDs();
        for(std::vector<std::string>::const_iterator iId = ids_.begin(); iId != ids_.end(); ++iId) {
          if(std::find_if(ids.begin(), ids.end(), std::bind2nd(PairFirstEq<pat::Electron::IdPair>(), *iId)) == ids.end())
            edm::LogError("PatValidation") << "Electron ID " << *iId << " not found from collection " << src_.encode() << std::endl;
        }
      }
    }

  private:
    edm::InputTag src_;
    std::vector<std::string> ids_;

  };
}

class HPlusPatTupleValidationAnalyzer: public edm::EDAnalyzer {
 public:
  explicit HPlusPatTupleValidationAnalyzer(const edm::ParameterSet&);
  ~HPlusPatTupleValidationAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  std::vector<ElectronValidation> electronValidation_;
};

HPlusPatTupleValidationAnalyzer::HPlusPatTupleValidationAnalyzer(const edm::ParameterSet& iConfig) {
  std::vector<edm::ParameterSet> electrons = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("electrons");
  electronValidation_.reserve(electrons.size());
  for(std::vector<edm::ParameterSet>::const_iterator iParam = electrons.begin(); iParam != electrons.end(); ++iParam) {
    electronValidation_.push_back(ElectronValidation(*iParam));
  }
}

HPlusPatTupleValidationAnalyzer::~HPlusPatTupleValidationAnalyzer() {}

void HPlusPatTupleValidationAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::for_each(electronValidation_.begin(), electronValidation_.end(), CallValidate(iEvent));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPatTupleValidationAnalyzer);
