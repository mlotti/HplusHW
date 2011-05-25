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
    TauIDPFShrinkingCone(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFShrinkingCone();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDIsolation;
  };

  // TauIDPFHPSBase ---------------------------------------------
  class TauIDPFHPSBase: public TauIDPFTauBase {
  public:
    TauIDPFHPSBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel, TFileDirectory& myDir);
    virtual ~TauIDPFHPSBase();

    bool passTauCandidateEAndMuVetoCuts(const edm::Ptr<pat::Tau> tau);
  };

  /**
   * \todo The class should be renamed to e.g. TauIDPFHPS (there's no shrinking cone here)
   */
  class TauIDPFHPSTight : public TauIDPFHPSBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPS tau ID functionality
     */
    TauIDPFHPSTight(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFHPSTight();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
  };

  // TauIDPFShrinkingConeHPSLoose ---------------------------------------
  class TauIDPFHPSVeryLoose : public TauIDPFHPSBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPSMedium tau ID functionality
     */
    TauIDPFHPSVeryLoose(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFHPSVeryLoose();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
  };

  // TauIDPFShrinkingConeHPSLoose ---------------------------------------
  class TauIDPFHPSLoose : public TauIDPFHPSBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPSMedium tau ID functionality
     */
    TauIDPFHPSLoose(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFHPSLoose();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDHPS;
  };

  /**
   * \todo The class should be renamed to e.g. TauIDPFHPSMedium (there's no shrinking cone here)
   */
  class TauIDPFHPSMedium : public TauIDPFHPSBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeHPSMedium tau ID functionality
     */
    TauIDPFHPSMedium(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFHPSMedium();

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
    TauIDPFShrinkingConeTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
    ~TauIDPFShrinkingConeTaNC();

    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);

  private:
    // Tau ID selections related to isolation
    size_t fIDTaNC;
  };

  /**
   * \todo The class should be renamed to e.g. TauIDPFCombinedHPSTaNC (there's no shrinking cone here)
   */
  class TauIDPFShrinkingConeCombinedHPSTaNC : public TauIDPFHPSBase {
   public:
    /**
     * Implementation of the TauIDPFShrinkingConeCombinedHPSTaNC tau ID functionality
     */
    TauIDPFShrinkingConeCombinedHPSTaNC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongCount, std::string label, TFileDirectory& myDir);
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
