// -*- c++ -*-                                                                                                                                          

// New code for calculating the b-tagging efficiency in MC. Responsible persons in Summer 2013: Shih-Yen and Stefan.
/*
TODO:
* Read BTagging::Data
* Modify BTagging::Data to contain the number of genuine b quarks



*/

#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTaggingEfficiencyInMC_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTaggingEfficiencyInMC_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class BTaggingEfficiencyInMC: public BaseSelection {
  public:
    class Data {
    public:
      Data();
      ~Data();
      
      const edm::PtrVector<pat::Jet>& getGenuineBJets() const { return fGenuineBJets; }
      const edm::PtrVector<pat::Jet>& getGenuineBJetsWithBTag() const { return fGenuineBJetsWithBTag; }
      const edm::PtrVector<pat::Jet>& getGenuineGJets() const { return fGenuineGJets; }
      const edm::PtrVector<pat::Jet>& getGenuineGJetsWithBTag() const { return fGenuineGJetsWithBTag; }
      const edm::PtrVector<pat::Jet>& getGenuineUDSJets() const { return fGenuineUDSJets; }
      const edm::PtrVector<pat::Jet>& getGenuineUDSJetsWithBTag() const { return fGenuineUDSJetsWithBTag; }
      const edm::PtrVector<pat::Jet>& getGenuineCJets() const { return fGenuineCJets; }
      const edm::PtrVector<pat::Jet>& getGenuineCJetsWithBTag() const { return fGenuineCJetsWithBTag; }
      const edm::PtrVector<pat::Jet>& getGenuineLJets() const { return fGenuineLJets; }
      const edm::PtrVector<pat::Jet>& getGenuineLJetsWithBTag() const { return fGenuineLJetsWithBTag; }

      friend class BTaggingEfficiencyInMC;
    private:
      // private member variables
      edm::PtrVector<pat::Jet> fGenuineBJets;
      edm::PtrVector<pat::Jet> fGenuineBJetsWithBTag;
      edm::PtrVector<pat::Jet> fGenuineGJets;
      edm::PtrVector<pat::Jet> fGenuineGJetsWithBTag;
      edm::PtrVector<pat::Jet> fGenuineUDSJets;
      edm::PtrVector<pat::Jet> fGenuineUDSJetsWithBTag;
      edm::PtrVector<pat::Jet> fGenuineCJets;
      edm::PtrVector<pat::Jet> fGenuineCJetsWithBTag;
      edm::PtrVector<pat::Jet> fGenuineLJets;
      edm::PtrVector<pat::Jet> fGenuineLJetsWithBTag;
    };

    BTaggingEfficiencyInMC(EventCounter& eventCounter, HistoWrapper& histoWrapper); // constructor
    ~BTaggingEfficiencyInMC(); // destructor

    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData);
    void classifyJetsForEfficiencyCalculation(const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData, 
					      BTaggingEfficiencyInMC::Data& output);
    bool isBTagged(edm::Ptr<pat::Jet>& jet, const BTagging::Data& bTagData);

    // counters and histograms
    Count allJetsCount;
    Count genuineBJetsCount;
    Count genuineBJetsWithBTagCount;
  };
}

#endif
