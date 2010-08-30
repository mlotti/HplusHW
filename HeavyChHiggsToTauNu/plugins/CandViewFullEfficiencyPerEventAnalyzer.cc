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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionEfficiencyHisto.h"

#include<iostream>
#include<algorithm>

namespace {
  template <typename T>
  class ExpressionCutHisto: public ExpressionEfficiencyHistoPerEvent<T> {
    typedef ExpressionEfficiencyHistoPerEvent<T> Base;
  public:
    ExpressionCutHisto(const edm::ParameterSet& iConfig);
    ~ExpressionCutHisto();

    bool passesCut(const T& element) const {
      //std::cout << "  value " << this->function(element) << " cutValue " << cutValue_ << std::endl;
      return this->cmp->compare(this->function(element), cutValue_);
    }

    uint32_t getMinObjects() const {
      return this->minObjects_;
    }

  private:
    double cutValue_;
  };

  template <typename T>
  ExpressionCutHisto<T>::ExpressionCutHisto(const edm::ParameterSet& iConfig):
    Base(iConfig),
    cutValue_(iConfig.template getUntrackedParameter<double>("cutvalue"))
  {}
  template <typename T>
  ExpressionCutHisto<T>::~ExpressionCutHisto() {}
}


class CandViewFullEfficiencyPerEventAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit CandViewFullEfficiencyPerEventAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~CandViewFullEfficiencyPerEventAnalyzer();

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

  struct Collection {
    struct FailedCut {
      FailedCut(): n(0), lastIndex(0) {}
      size_t n;
      size_t lastIndex;
    };

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
        else // inds.size() >= 2
          return true;
      }

    private:
      std::vector<std::vector<size_t> > failIndices;
    };

    edm::InputTag src;
    uint32_t minObjects;
    Histograms histograms;
    //std::vector<size_t> cutsFailed;
    //std::vector<size_t> lastFailedCutIndex;
    //std::vector<FailedCut> cutsFailed;
    FailedCuts cutsFailed;
    size_t count0;
    size_t count1;
    //std::vector<size_t> cutsFailed0;
    //size_t cutsFailed0_count;
    //std::vector<size_t> cutsFailed1_ind;
  };

  /// Do we weight events?
  bool usingWeights_;
  /// label of the weight collection (can be null for weights = 1)
  edm::InputTag weights_;

  std::vector<Collection> colls_;
};

CandViewFullEfficiencyPerEventAnalyzer::CandViewFullEfficiencyPerEventAnalyzer(const edm::ParameterSet& par):
  usingWeights_(par.exists("weights")),
  weights_(par.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag("fake"))) {
  edm::Service<TFileService> fs;
  std::vector<std::string> histonames = par.getParameterNamesForType<edm::ParameterSet>(false); // take only untracked parameters

  std::string name("name");
  colls_.resize(histonames.size());
  for(size_t i=0; i<histonames.size(); ++i) {
    edm::ParameterSet pset = par.getUntrackedParameter<edm::ParameterSet>(histonames[i]);
    colls_[i].src= pset.getParameter<edm::InputTag>("src");
    //colls_[i].minObjects = pset.getParameter<uint32_t>("minObjects");

    std::vector<edm::ParameterSet> histograms = 
      pset.getParameter<std::vector<edm::ParameterSet> >("histograms");

    std::vector<edm::ParameterSet>::iterator it = histograms.begin();
    std::vector<edm::ParameterSet>::iterator end = histograms.end();

    uint32_t minObj = 0;
    colls_[i].histograms.reserve(histograms.size());
    for(; it != end; ++it) {
      it->insert(true, name, edm::Entry(name, histonames[i]+it->getUntrackedParameter<std::string>(name), false));

      HistoType* hist = new HistoType(*it);
      hist->initialize(*fs);
      if(minObj == 0)
        minObj = hist->getMinObjects();
      colls_[i].histograms.push_back(hist);

      if(minObj != hist->getMinObjects())
        throw cms::Exception("Configuration") << "The histograms of " << histonames[i] << " have different minObjects parameter" << std::endl;
    }
    colls_[i].minObjects = minObj;
  }
}

CandViewFullEfficiencyPerEventAnalyzer::~CandViewFullEfficiencyPerEventAnalyzer() {
  for(size_t i=0; i<colls_.size(); ++i) {
    // delete all histograms and clear the vector of pointers
    Histograms::iterator it = colls_[i].histograms.begin(); 
    Histograms::iterator end = colls_[i].histograms.end();
    for (;it!=end; ++it){
      delete *it;
    }
    colls_[i].histograms.clear(); 
  }
}

void CandViewFullEfficiencyPerEventAnalyzer::beginJob() {
}

void CandViewFullEfficiencyPerEventAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;
  if (usingWeights_) { 
    edm::Handle<double> weightColl;
    iEvent.getByLabel( weights_, weightColl ); 
    weight = *weightColl;
  }

  size_t nCollsWithCount0 = 0;
  size_t lastFailedCollIndex = 0;

  for(size_t i=0; i<colls_.size(); ++i) {
    edm::Handle<CollectionType> coll;
    iEvent.getByLabel( colls_[i].src, coll);

    size_t iHisto = 0;
    Histograms::iterator it = colls_[i].histograms.begin();
    Histograms::iterator end = colls_[i].histograms.end(); 

    //std::cout << std::endl
    //          << "Collection " << colls_[i].src.encode() << std::endl;

    // For each object, count the number of cuts the object fails a cut
    colls_[i].cutsFailed.setNobjects(coll->size());
    for(; it!= end; ++it, ++iHisto) {
      size_t iObj=0;
      //std::cout << "Checking cut " << iHisto << std::endl;
      for(CollectionType::const_iterator elem=coll->begin(); elem!=coll->end(); ++elem, ++iObj) {
        if(!(*it)->passesCut(*elem)) {
          //std::cout << "  Failed, adding to cutFailedForObj" << std::endl;
          colls_[i].cutsFailed.cutFailedForObj(iObj, iHisto);
        }
      }
    }

    // Count the number of objects which fail 0 or 1 cuts
    colls_[i].count0=0;
    colls_[i].count1=0;
    for(size_t j=0; j<coll->size(); ++j) {
      size_t nFailed = colls_[i].cutsFailed.failedCutsForObj(j);
      if(nFailed == 0)
        colls_[i].count0 += 1;
      else if(nFailed == 1)
        colls_[i].count1 += 1;
    }
    //std::cout << "Count0 " << colls_[i].count0 << std::endl
    //          << "Count1 " << colls_[i].count1 << std::endl
    //          << "minObjects " << colls_[i].minObjects << std::endl;
    

    // Update the bookkeeping between collections
    if(colls_[i].count0 >= colls_[i].minObjects)
      ++nCollsWithCount0;
    else
      lastFailedCollIndex = i;
    //std::cout << "nCollsWithCount0 " << nCollsWithCount0 << std::endl
    //          << "lastFailedCollIndex " << lastFailedCollIndex << std::endl;
  }

  if(nCollsWithCount0 == colls_.size()) {
    // The event passes all cuts, so we fill all cuts, but only for
    // those objects for which no other cut has failed.
    //std::cout << "Filling for all cuts" << std::endl;

    for(size_t i=0; i<colls_.size(); ++i) {
      edm::Handle<CollectionType> coll;
      iEvent.getByLabel( colls_[i].src, coll);
      //std::cout << " coll " << colls_[i].src.encode() << std::endl;

      size_t iHisto = 0;
      Histograms::iterator it = colls_[i].histograms.begin();
      Histograms::iterator end = colls_[i].histograms.end(); 
      for(; it!= end; ++it, ++iHisto) {
        size_t iObj = 0;
        for(CollectionType::const_iterator elem=coll->begin(); elem!=coll->end(); ++elem, ++iObj) {
          if(!colls_[i].cutsFailed.hasOtherCutFailedForObj(iObj, iHisto)) {
            // Fill only if no other cut has failed for this object
            //std::cout << "  filling for cut " << iHisto << " obj " << iObj << std::endl;
            if (!(*it)->fill( *elem, weight, iObj )) {
              break;
            }
          }
        }
        (*it)->endEvent();
      }
    }
  }
  else if(nCollsWithCount0+1 == colls_.size()) {
    // One collection had failed cuts, let's check that
    //std::cout << "Filling for failed collection only, lastFailedCollIndex " << lastFailedCollIndex << std::endl;

    size_t sum01 = colls_[lastFailedCollIndex].count1 + colls_[lastFailedCollIndex].count0;
    if(colls_[lastFailedCollIndex].cutsFailed.getNobjects() < colls_[lastFailedCollIndex].minObjects) {
      size_t i = lastFailedCollIndex;
      edm::Handle<CollectionType> coll;
      iEvent.getByLabel( colls_[i].src, coll);

      size_t iHisto = 0;
      Histograms::iterator it = colls_[i].histograms.begin();
      Histograms::iterator end = colls_[i].histograms.end(); 
      for(; it!= end; ++it, ++iHisto) {
        size_t iObj = 0;
        for(CollectionType::const_iterator elem=coll->begin(); elem!=coll->end(); ++elem, ++iObj) {
          //std::cout << "  filling for cut " << iHisto << " obj " << iObj << std::endl;
          if (!(*it)->fill( *elem, weight, iObj )) {
            break;
          }
        }
        (*it)->endEvent();
      }
    }
    else if(sum01 >= colls_[lastFailedCollIndex].minObjects) {
      // For each object in collection lastFailedCollIndex, there is
      // at most 1 failed cut. Each failed cut will be filled.

      size_t i = lastFailedCollIndex;
      edm::Handle<CollectionType> coll;
      iEvent.getByLabel( colls_[i].src, coll);

      size_t iHisto = 0;
      Histograms::iterator it = colls_[i].histograms.begin();
      Histograms::iterator end = colls_[i].histograms.end(); 
      for(; it!= end; ++it, ++iHisto) {
        size_t iObj = 0;
        for(CollectionType::const_iterator elem=coll->begin(); elem!=coll->end(); ++elem, ++iObj) {
          if(!colls_[i].cutsFailed.hasOtherCutFailedForObj(iObj, iHisto)) {
          //if(colls_[i].cutsFailed.hasCutFailedForObj(iObj, iHisto) &&
          //   !colls_[i].cutsFailed.hasOtherCutFailedForObj(iObj, iHisto)) {
            // Fill only if no other cut has failed for this object
            //std::cout << "  filling for cut " << iHisto << " obj " << iObj << std::endl;
            if (!(*it)->fill( *elem, weight, iObj )) {
              break;
            }
          }
        }
        (*it)->endEvent();
      }


    }
    // Otherwise, for some object in the collection, there are at
    // least 2 failed cuts and therefore nothing is filled
  }
  // Otherwise at least two collections had failed cuts, so there must
  // be at least two failed cuts, so nothing is filled
}

void CandViewFullEfficiencyPerEventAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(CandViewFullEfficiencyPerEventAnalyzer);
