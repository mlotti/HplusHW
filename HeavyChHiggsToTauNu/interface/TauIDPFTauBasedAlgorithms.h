// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBasedAlgorithms_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIDPFTauBasedAlgorithms_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBase.h"

namespace HPlus {
  // TauIDPFHPS ---------------------------------------------
  class TauIDPFHPS : public TauIDPFTauBase {
  public:
    /**
     * Implementation of the HPS tau ID functionality
     */
    TauIDPFHPS(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel, TFileDirectory& myDir);
    ~TauIDPFHPS();

    bool passDecayModeFinding(const edm::Ptr<pat::Tau>& tau);
  };
  
  // TauIDPFShrinkingConeTaNC --------------------------------------------
  class TauIDPFTaNC : public TauIDPFTauBase {
   public:
    /**
     * Implementation of the TaNC tau ID functionality
     */
    TauIDPFTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label, TFileDirectory& myDir);
    ~TauIDPFTaNC();

    bool passDecayModeFinding(const edm::Ptr<pat::Tau>& tau);

  private:
  };

//  /**
//   * \todo The class should be renamed to e.g. TauIDPFCombinedHPSTaNC (there's no shrinking cone here)
//   */
//  class TauIDPFCombinedHPSTaNC : public TauIDPFHPS {
//   public:
//    /**
//     * Implementation of the Combined TaNC+HPS tau ID functionality
//     */
//    TauIDPFShrinkingConeCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
//    ~TauIDPFShrinkingConeCombinedHPSTaNC();
//
//    bool passDecayModeFinding(const edm::Ptr<pat::Tau>& tau);
//
//  private:
//  };

}

#endif
