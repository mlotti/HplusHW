// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_QCDTailKiller_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_QCDTailKiller_h

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class QCDTailKiller: public BaseSelection {
  public:
    enum CutShape { kNoCut, kRectangle, kTriangle, kCircle, kMinDeltaPhiJetMET };
    enum CutDirection { kCutUpperLeftCorner, kCutLowerRightCorner };

    /**
     * Class to encapsulate the access to the data members of
     * QCDTailKiller. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();

      void initialize(int maxEntries);

      const bool passedEvent() const { return fPassedEvent; }
      const bool passedBackToBackCuts() const;
      const bool passedCollinearCuts() const;
      const int getNConsideredJets() const { return fMaxEntries; }
      /// Getters for counted values (in degrees)
      const double getDeltaPhiTauMET() const { return fDeltaPhiTauMET; }
      const double getDeltaPhiJetMET(int njet) const;
      const double getRadiusFromBackToBackCorner(int njet) const { return std::sqrt(std::pow(180.-getDeltaPhiTauMET(),2)+std::pow(getDeltaPhiJetMET(njet),2)); }
      const double getRadiusFromCollinearCorner(int njet) const { return std::sqrt(std::pow(getDeltaPhiTauMET(),2)+std::pow(180.-getDeltaPhiJetMET(njet),2)); }
      const double getTailKillerYaxisIntercept(int njet) const { return getDeltaPhiJetMET(njet) - getDeltaPhiTauMET(); } // Assumes equilateral triangle: y = 1*x + c
      const bool passBackToBackCutForJet(int njet) const;
      const bool passCollinearCutForJet(int njet) const;
      const bool backToBackCutActiveForJet(int njet) const;
      const bool collinearCutActiveForJet(int njet) const;


      friend class QCDTailKiller;

    private:
      int fMaxEntries;
      bool fPassedEvent;
      std::vector<bool> fPassedBackToBackJet;
      std::vector<bool> fPassedCollinearJet;
      std::vector<bool> fCutActiveBackToBackJet;
      std::vector<bool> fCutActiveCollinearJet;
      double fDeltaPhiTauMET;
      std::vector<double> fDeltaPhiJetMET;

    };

    class CutItem {
    public:
      CutItem(EventCounter& eventCounter, std::string cutName, QCDTailKiller::CutDirection cutDirection);
      ~CutItem();
      void initialise(HistoWrapper& histoWrapper, TFileDirectory& histoDir, std::string cutShape, double cutX, double cutY, int jetN);
      bool passedCut(double x, double y);
      bool isActive() { return fCutShape != QCDTailKiller::kNoCut; }
      void fillAfterAllCuts(double x, double y);

    private:
      QCDTailKiller::CutShape fCutShape;
      double fCutX;
      double fCutY;
      QCDTailKiller::CutDirection fCutDirection;
      bool bIsInitialised;
      std::string fName;
      // Counters
      Count fPassedSubCounter;
      // Histograms
      WrappedTH1* hOptimisationPlot;
      WrappedTH2* hBeforeCut;
      WrappedTH2* hAfterAllCuts;
    };

    QCDTailKiller(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string postfix="");
    ~QCDTailKiller();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met);
    /// Number of jets to consider
    const uint32_t fMaxEntries;
    bool bDisableCollinearCuts;
    // Cut items for back to back (tau,MET) topology
    std::vector<CutItem> fBackToBackJetCut;
    // Cut items for collinear (tau,MET) topology
    std::vector<CutItem> fCollinearJetCut;
    // Counters
    Count fSubCountAllEvents;
    Count fSubCountPassedEvents;

    // Histograms
  };
}

#endif
