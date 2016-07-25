#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/ParameterSet/interface/Entry.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/ExpressionHisto.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include<iostream>
#include<algorithm>

namespace {
  template <typename T>
  class ExpressionCutHisto: public ExpressionHisto<T> {
    typedef ExpressionHisto<T> Base;
  public:
    ExpressionCutHisto(const edm::ParameterSet& iConfig);
    ~ExpressionCutHisto();

    bool passesCut(const T& element) const {
      return cut_(element);
    }

    uint32_t getMinObjects() const {
      return minObjects_;
    }

  private:
    StringCutObjectSelector<T, true> cut_;
    const uint32_t minObjects_;
  };

  template <typename T>
  ExpressionCutHisto<T>::ExpressionCutHisto(const edm::ParameterSet& iConfig):
    Base(iConfig),
    cut_(iConfig.template getUntrackedParameter<std::string>("cut")),
    minObjects_(iConfig.template getUntrackedParameter<uint32_t>("minObjects", 1))
  {}
  template <typename T>
  ExpressionCutHisto<T>::~ExpressionCutHisto() {}
}


class HPlusCandViewHistoAfterOtherCutsAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusCandViewHistoAfterOtherCutsAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusCandViewHistoAfterOtherCutsAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  typedef reco::CandidateView CollectionType;
  typedef ExpressionCutHisto<CollectionType::value_type> HistoType;
  typedef std::vector<HistoType *> Histograms;
  
  /*
  class FailedCuts {
  public:
    FailedCuts() {}
    ~FailedCuts() {}

    void setNobjects(size_t n) {
      failIndices.clear();
      failIndices.resize(n);
    }

    size_t getNobjects() const {
      return failIndices.size();
    }

    void cutFailedForObj(size_t iObj, size_t iCut) {
      failIndices[iObj].push_back(iCut);
    }

    size_t failedCutsForObj(size_t iObj) const {
      return failIndices[iObj].size();
    }

    bool hasCutFailedForObj(size_t iObj, size_t iCut) const {
      return std::find(failIndices[iObj].begin(), failIndices[iObj].end(), iCut) != failIndices[iObj].end();
    }

    bool hasOtherCutFailedForObj(size_t iObj, size_t iCut) const {
      const std::vector<size_t>& inds = failIndices[iObj];
      if(inds.size() == 0)
        return false;
      else if(inds.size() == 1) {
        return inds.front() != iCut;
      }
      else inds.size() >= 2
             return true;
    }

  private:
    std::vector<std::vector<size_t> > failIndices;
  };
  */

  edm::InputTag src;
  uint32_t minObjects;
  Histograms histograms;
  //FailedCuts cutsFailed;

  /// Do we weight events?
  bool usingWeights_;
  /// label of the weight collection (can be null for weights = 1)
  edm::InputTag weights_;

};

HPlusCandViewHistoAfterOtherCutsAnalyzer::HPlusCandViewHistoAfterOtherCutsAnalyzer(const edm::ParameterSet& pset):
  usingWeights_(pset.exists("weights")),
  weights_(pset.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag("fake"))) {
  edm::Service<TFileService> fs;

  src = pset.getParameter<edm::InputTag>("src");

  std::vector<edm::ParameterSet> histos = 
    pset.getParameter<std::vector<edm::ParameterSet> >("histograms");

  std::vector<edm::ParameterSet>::iterator it = histos.begin();
  std::vector<edm::ParameterSet>::iterator end = histos.end();

  uint32_t minObj = 0;
  histograms.reserve(histos.size());
  for(; it != end; ++it) {
    HistoType* hist = new HistoType(*it);
    hist->initialize(*fs);
    if(minObj == 0)
      minObj = hist->getMinObjects();
    histograms.push_back(hist);

    if(minObj != hist->getMinObjects())
      throw cms::Exception("Configuration") << "The histograms have different minObjects parameter" << std::endl;
  }
  minObjects = minObj;
}

HPlusCandViewHistoAfterOtherCutsAnalyzer::~HPlusCandViewHistoAfterOtherCutsAnalyzer() {
  // delete all histograms and clear the vector of pointers
  Histograms::iterator it = histograms.begin(); 
  Histograms::iterator end = histograms.end();
    for (;it!=end; ++it){
      delete *it;
    }
    histograms.clear(); 
}

void HPlusCandViewHistoAfterOtherCutsAnalyzer::beginJob() {
}

void HPlusCandViewHistoAfterOtherCutsAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;
  if (usingWeights_) { 
    edm::Handle<double> weightColl;
    iEvent.getByLabel( weights_, weightColl ); 
    weight = *weightColl;
  }

  edm::Handle<CollectionType> coll;
  iEvent.getByLabel( src, coll);

  std::vector<int> nFailedCuts(coll->size(), 0);
  std::vector<int> lastFailedCutIndex(coll->size(), -1);
  //std::vector<int> 
  size_t nEventFailedCuts = 0;
  int eventLastFailedCutIndex = -1;

  // For each physics object, count the number cuts it fails, and
  // record the index of the last failed cut
  // For each cut, count how many objects pass (N). If N >=
  // minObjects, event passes that cut. Count the number of cuts the
  // event fails.

  // As an optimization, if two or more cuts fail at the event level,
  // there's nothing to fill and we can just return from the whole
  // function.
  int iCut = 0;
  Histograms::iterator it = histograms.begin();
  Histograms::iterator end = histograms.end(); 
  for(; it!= end; ++it, ++iCut) {
    size_t iObj=0;
    size_t nObjectsPassed = 0;
    for(CollectionType::const_iterator elem=coll->begin(); elem != coll->end(); ++elem, ++iObj) {
      if((*it)->passesCut(*elem)) {
        ++nObjectsPassed;
      }
      else {
        nFailedCuts[iObj] += 1;
        lastFailedCutIndex[iObj] = iCut;
      }
    }

    if(nObjectsPassed < minObjects) {
      ++nEventFailedCuts;
      eventLastFailedCutIndex = iCut;
      if(nEventFailedCuts >= 2)
        return;
    }
  }

  /*
    Laske jokaiselle objektille, montako leikkausta feilaa

    Laske niiden objektien lukumäärä,
      jotka feilaavat nolla leikkausta (M0)
      jotka feilaavat yhden leikkauksen (M1)

    Jos M0 >= N, täytä kaikki leikkaukset kaikille objekteille

    Muuten, jos M1 >= N,
      objekteille, jotka feilaavat 0 leikkausta, täytä kaikki leikkauset
                   jotka feilaavat 1 leikkausta, täytä se yksi leikkaus
   */


  if(nEventFailedCuts == 0) {
    // If number of cuts which failed the event is zero:
    // - for each object which has passed all cuts, fill all cuts for that object
    // - for each object which has failed one cut, fill that cut for that object

    for(size_t iObj=0; iObj<nFailedCuts.size(); ++iObj) {
      if(nFailedCuts[iObj] == 0) {
        CollectionType::const_reference elem((*coll)[iObj]);
        Histograms::iterator it = histograms.begin();
        Histograms::iterator end = histograms.end(); 
        for(; it!= end; ++it) {
          (*it)->fill(elem, weight, iObj);
        }
      }
      else if(nFailedCuts[iObj] == 1) {
        if(lastFailedCutIndex[iObj] < 0)
          throw cms::Exception("LogicError") << "lastFailedCutIndex[iObj] was not set for iObj " << iObj << std::endl;
        histograms[lastFailedCutIndex[iObj]]->fill((*coll)[iObj], weight, iObj);
      }
    }
  }
  else if(nEventFailedCuts == 1) {
    // If only one cut failed the event, then for that cut fill all
    // objects that have failed at most one time at that cut
    
    for(size_t iObj=0; iObj<nFailedCuts.size(); ++iObj) {
      if(nFailedCuts[iObj] == 0 || (nFailedCuts[iObj] == 1 && lastFailedCutIndex[iObj] == eventLastFailedCutIndex)) {
        histograms[eventLastFailedCutIndex]->fill((*coll)[iObj], weight, iObj);
      }
    }
  }
}

void HPlusCandViewHistoAfterOtherCutsAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewHistoAfterOtherCutsAnalyzer);

