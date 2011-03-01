// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingAnalysis_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingAnalysis_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}
namespace reco {
  class Candidate;
}

class TFileDirectory;

class TH1;

namespace HPlus {
  class EventWeight;

  class TauEmbeddingAnalysis {
    // Class for one set of histograms
    class Histograms {
    public:
      Histograms();
      ~Histograms();

      void book(TFileDirectory& fd, const std::string& prefix);

      // Fill the histograms (add more objects to arguments if necessary)
      void fill(double weight, const reco::Candidate& originalMet);

    private:
      // Histograms
      TH1 *hOriginalMet;

    };

  public:
    TauEmbeddingAnalysis(EventWeight& eventWeight);
    ~TauEmbeddingAnalysis();

    // Initialize, only if the parameter set is available
    void init(const edm::ParameterSet& iConfig);

    // Read the objects from the event and fill the fBegin
    void beginEvent(const edm::Event&, const edm::EventSetup&);

    // Fill the rest of the histogram sets
    void fillAfterTauId();
    void fillAfterMetCut();
    void fillEnd();

  private:
    edm::InputTag fOriginalMetSrc;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histogram sets
    Histograms fBegin;
    Histograms fAfterTauId;
    Histograms fAfterMetCut;
    Histograms fEnd;

    // Holders of the objects
    edm::Ptr<reco::Candidate> fOriginalMet;

    bool fEnabled;
  };

}


#endif
