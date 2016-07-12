// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MCAnalysisOfSelectedEvents_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MCAnalysisOfSelectedEvents_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class MCAnalysisOfSelectedEvents: public BaseSelection {
  public:
    typedef math::XYZTLorentzVector XYZTLorentzVector;
    /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();


      friend class MCAnalysisOfSelectedEvents;

    private:
      // Variables
     
    };

    MCAnalysisOfSelectedEvents(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~MCAnalysisOfSelectedEvents();

    void silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData );

    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData );


  private:
    
    void privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData );
    void init();
    

    edm::InputTag fSrc;
    edm::InputTag fOneProngTauSrc;
    edm::InputTag fOneAndThreeProngTauSrc;

 

    Count fElectronNotInTauCounter;
    Count fElectronNotInTauFromWCounter;
    Count fElectronNotInTauFromBottomCounter;
    Count fElectronNotInTauFromTauCounter;

    Count fMuonNotInTauCounter;
    Count fMuonNotInTauFromWCounter;
    Count fMuonNotInTauFromBottomCounter;
    Count fMuonNotInTauFromTauCounter;

    Count fTauNotInTauCounter;
    Count fTauNotInTauFromWCounter;
    Count fTauNotInTauFromBottomCounter;
    Count fTauNotInTauFromHplusCounter;

    Count fObservableMuonsCounter;
    Count fObservableElectronsCounter;
    Count fObservableTausCounter;

    Count fElectronOrMuonFoundCounter;
    Count fNoElectronOrMuonFoundCounter;
    Count fNoElectronOrMuonFoundRealTauCounter;

    Count fLeptonFoundCounter;
    Count fNoLeptonFoundCounter;
    Count fNoLeptonFoundRealTauCounter;

    Count fTauIsHadronFromHplusCounter;
    Count fTauIsElectronFromHplusCounter;
    Count fTauIsMuonFromHplusCounter;
    Count fTauIsQuarkFromWCounter;
    Count fTauIsQuarkFromZCounter;
    Count fTauIsElectronFromWCounter;
    Count fTauIsElectronFromZCounter;
    Count fTauIsMuonFromWCounter;
    Count fTauIsHadronFromWTauCounter;
    Count fTauIsElectronFromWTauCounter;
    Count fTauIsMuonFromWTauCounter;
    Count fTauIsMuonFromZCounter;
    Count fTauIsHadronFromZTauCounter;
    Count fTauIsElectronFromZTauCounter;
    Count fTauIsMuonFromZTauCounter;
    Count fTauIsElectronFromBottomCounter;
    Count fTauIsMuonFromBottomCounter;
    Count fTauIsHadronFromBottomCounter;
    Count fTauIsElectronFromJetCounter;
    Count fTauIsMuonFromJetCounter;
    Count fTauIsHadronFromJetCounter;


    // Histograms
    WrappedTH1 *hgenWmass;
    WrappedTH1 *hGenMET;
    WrappedTH1 *hdeltaPhiMetGenMet;
    WrappedTH1 *hdeltaEtMetGenMet;
    WrappedTH1 *htransverseMassAll;
    WrappedTH1 *htransverseMassMuonNotInTau;
    WrappedTH1 *htransverseMassMuonFromW;
    WrappedTH1 *htransverseMassMuonFromBottom;
    WrappedTH1 *htransverseMassMuonFromTau;
    WrappedTH1 *htransverseMassElectronFromW;
    WrappedTH1 *htransverseMassElectronFromBottom;
    WrappedTH1 *htransverseMassElectronFromTau;
    WrappedTH1 *htransverseMassElectronNotInTau;
    WrappedTH1 *htransverseMassTauNotInTau;
    WrappedTH1 *htransverseMassMetReso02;
    WrappedTH1 *htransverseMassLeptonNotInTau;
    WrappedTH1 *htransverseMassElMuNotInTau;
    WrappedTH1 *htransverseMassNoLeptonNotInTau;
    WrappedTH1 *htransverseMassNoElMuNotInTau;
    WrappedTH1 *htransverseMassNoLeptonGoodMet;
    WrappedTH1 *htransverseMassNoLeptonGoodMetGoodTau;
    WrappedTH1 *htransverseMassLeptonRealSignalTau;
    WrappedTH1 *htransverseMassNoLeptonRealSignalTau;
    WrappedTH1 *htransverseMassNoElMuRealSignalTau;
    WrappedTH1 *htransverseMassLeptonFakeSignalTau;
    WrappedTH1 *htransverseMassNoObservableLeptons;
    WrappedTH1 *htransverseMassObservableLeptons;
    WrappedTH1 *htransverseMassElectronOrMuonFound;
    WrappedTH1 *htransverseMassNoElectronOrMuonFound;
   
  };
}

#endif
