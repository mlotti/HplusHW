// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBasedAlgorithms_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBasedAlgorithms_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBase.h"

namespace HPlus {
  // TauIDPFShrinkingCone ------------------------------------------------
  class TauIDPFShrinkingCone : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingCone tau ID functionality
     */
    TauIDPFShrinkingCone(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount);
    ~TauIDPFShrinkingCone();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDIsolation;
  };

  // TauIDPFShrinkingConeHPS ---------------------------------------------
  class TauIDPFShrinkingConeHPS : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPS tau ID functionality
     */
    TauIDPFShrinkingConeHPS(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount);
    ~TauIDPFShrinkingConeHPS();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
  };

  // TauIDPFShrinkingConeHPSMedium ---------------------------------------
  class TauIDPFShrinkingConeHPSMedium : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPSMedium tau ID functionality
     */
    TauIDPFShrinkingConeHPSMedium(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount);
    ~TauIDPFShrinkingConeHPSMedium();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
  };
  
  // TauIDPFShrinkingConeTaNC --------------------------------------------
  class TauIDPFShrinkingConeTaNC : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPS tau ID functionality
     */
    TauIDPFShrinkingConeTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount);
    ~TauIDPFShrinkingConeTaNC();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDTaNC;
  };

  // TauIDPFShrinkingConeCombinedHPSTaNC -------------------------------------------
  class TauIDPFShrinkingConeCombinedHPSTaNC : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeCombinedHPSTaNC tau ID functionality
     */
    TauIDPFShrinkingConeCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount);
    ~TauIDPFShrinkingConeCombinedHPSTaNC();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
    size_t fIDTaNC;
  };

}

#endif
