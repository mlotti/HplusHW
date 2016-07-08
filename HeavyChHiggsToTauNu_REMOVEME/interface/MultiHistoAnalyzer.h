// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_HPlusMultiHistoAnalyzer_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_HPlusMultiHistoAnalyzer_h
/** \class HPlusMultiHistoAnalyzer
 *
 * HistoAnalyzer used as a template
 * 
 * Template parameters:
 * - C : Concrete candidate collection type
 *
 */
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/Entry.h"

namespace HPlus {
  template <template <class> class H>
  struct MultiHistoAnalyzerTraits {
    template <typename T>
    static void endEvent(H<T> *histo) {
    }
  };

  template<typename C, template <class> class H, typename Traits = MultiHistoAnalyzerTraits<H> >
  class MultiHistoAnalyzer : public edm::EDAnalyzer {
  public:
    /// constructor from parameter set
    MultiHistoAnalyzer( const edm::ParameterSet& );
    /// destructor
    ~MultiHistoAnalyzer();
  
  protected:
    /// process an event
    virtual void analyze( const edm::Event&, const edm::EventSetup& );

  private:
    /// label of the collection to be read in
    std::vector<edm::InputTag> srcs_;
    /// Do we weight events?
    bool usingWeights_;
    /// label of the weight collection (can be null for weights = 1)
    edm::InputTag weights_;
    /// vector of the histograms
    typedef H<typename C::value_type> Histogram;
    typedef std::vector<Histogram *> Histograms;

    struct HistoObject {
      edm::InputTag src_;
      Histograms histograms_;
    };
    std::vector<HistoObject> histograms_;
  };

  template<typename C, template <class> class H, typename Traits>
  MultiHistoAnalyzer<C, H, Traits>::MultiHistoAnalyzer( const edm::ParameterSet& par ) : 
    usingWeights_(par.exists("weights")),
    weights_(par.template getUntrackedParameter<edm::InputTag>("weights", edm::InputTag("fake")))
  {
    edm::Service<TFileService> fs;
    std::vector<std::string> histonames = par.template getParameterNamesForType<edm::ParameterSet>(false); // take only untracked parameters

    /*
      std::vector<edm::ParameterSet> histotypes = 
      par.template getParameter<std::vector<edm::ParameterSet> >("histogramTypes");
      std::vector<edm::ParameterSet>::const_iterator it = histotypes.begin();
      std::vector<edm::ParameterSet>::const_iterator end = histotypes.end();
    */
    histograms_.resize(histonames.size());

    std::string name("name");

    // create the histograms from the given parameter sets 
    for (size_t i=0; i<histonames.size(); ++i) {
      edm::ParameterSet pset = par.template getUntrackedParameter<edm::ParameterSet>(histonames[i]);
      histograms_[i].src_ = pset.template getParameter<edm::InputTag>("src");

      std::vector<edm::ParameterSet> histograms = 
        pset.template getParameter<std::vector<edm::ParameterSet> >("histograms");

      std::vector<edm::ParameterSet>::iterator it = histograms.begin();
      std::vector<edm::ParameterSet>::iterator end = histograms.end();

      for(; it != end; ++it) {
        it->insert(true, name, edm::Entry(name, histonames[i]+it->getUntrackedParameter<std::string>(name), false));

        Histogram* hist = new Histogram(*it);
        hist->initialize(*fs);
        histograms_[i].histograms_.push_back(hist);
      }   
    }
  }

  template<typename C, template <class> class H, typename Traits>
  MultiHistoAnalyzer<C, H, Traits>::~MultiHistoAnalyzer() 
  {
    for(size_t i=0; i<histograms_.size(); ++i) {
      // delete all histograms and clear the vector of pointers
      typename Histograms::iterator it = histograms_[i].histograms_.begin(); 
      typename Histograms::iterator end = histograms_[i].histograms_.end();
      for (;it!=end; ++it){
        delete *it;
      }
      histograms_[i].histograms_.clear(); 
    }
  }

  template<typename C, template <class> class H, typename Traits>
  void MultiHistoAnalyzer<C, H, Traits>::analyze( const edm::Event& iEvent, const edm::EventSetup& ) 
  {
    double weight = 1.0;
    if (usingWeights_) { 
      edm::Handle<double> weightColl;
      iEvent.getByLabel( weights_, weightColl ); 
      weight = *weightColl;
    }

    for(size_t i=0; i<histograms_.size(); ++i) {
      edm::Handle<C> coll;
      iEvent.getByLabel( histograms_[i].src_, coll);

      typename Histograms::iterator it = histograms_[i].histograms_.begin();
      typename Histograms::iterator end = histograms_[i].histograms_.end(); 

      for (;it!=end; ++it){
        uint32_t j = 0;
        for( typename C::const_iterator elem=coll->begin(); elem!=coll->end(); ++elem, ++j ) {
          if (!(*it)->fill( *elem, weight, j )) {
            break;
          }
        }
        Traits::endEvent(*it);
      }
    }
  }
}
#endif
