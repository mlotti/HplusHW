// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SignalAnalysisTree_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Ptr.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include <MagneticField/Engine/interface/MagneticField.h>
#include "FWCore/Framework/interface/ESHandle.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

class TFileDirectory;

class TTree;


namespace HPlus {
  class SignalAnalysisTree {
  public:
    typedef math::XYZTLorentzVector XYZTLorentzVector;

    explicit SignalAnalysisTree(const edm::ParameterSet& iConfig, const std::string& bDiscriminator);
    ~SignalAnalysisTree();

    void init(TFileDirectory& dir);

    void setPrescaleWeight(double w) { fPrescaleWeight = w; }
    void setPileupWeight(double w)   { fPileupWeight = w; }
    void setTriggerWeight(double w)  { fTriggerWeight = w; }
    void setFillWeight(double w)  { fFillWeight = w; }
    void enableNonIsoLeptons(bool enableNonIsoLeptons)  { fillNonIsoLeptonVars = enableNonIsoLeptons; }
    void setNvertices(unsigned int n) { fNVertices = n; }
    void setBTagging(bool passed, double scaleFactor) { fPassedBTagging = passed; fBTaggingWeight = scaleFactor; }
    void setTop(const XYZTLorentzVector& top) { fTop = top; }

    void setRawMET(const edm::Ptr<reco::MET>& met) { fRawMet = met->p4(); fRawMetSumEt = met->sumEt(); }
    void setType1MET(const edm::Ptr<reco::MET>& met) { fType1Met = met->p4(); }
    void setType2MET(const edm::Ptr<reco::MET>& met) { fType2Met = met->p4(); }
    void setGenMET(const edm::Ptr<reco::GenMET>& met) { fGenMet = met->p4(); }

    void setHltTaus(const pat::TriggerObjectRefVector& hltTaus);
    void setNonIsoLeptons(const edm::Event& iEvent, edm::PtrVector<pat::Muon> nonIsoMuons, edm::PtrVector<pat::Electron> nonIsoElectrons);

    void fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
              const edm::PtrVector<pat::Jet>& jets,
	      double alphaT);


  private:
    void reset();

    struct TauId {
      TauId(const std::string& n): name(n), value(false) {}
      void reset() { value = false; }
      std::string name;
      bool value;
    };

    const std::string fBdiscriminator;
    const bool fDoFill;
    const bool fTauEmbeddingInput;

    edm::InputTag fTauEmbeddingMuonSource;
    edm::InputTag fTauEmbeddingMetSource;
    edm::InputTag fTauEmbeddingCaloMetSource;

    TTree *fTree;

    bool fillNonIsoLeptonVars;
    unsigned int fEvent;
    unsigned int fLumi;
    unsigned int fRun;

    double fPrescaleWeight;
    double fPileupWeight;
    double fTriggerWeight;
    double fBTaggingWeight;
    double fFillWeight;

    unsigned int fNVertices;

    std::vector<XYZTLorentzVector> fHltTaus;

    XYZTLorentzVector fTau;
    XYZTLorentzVector fTauLeadingChCand;
    unsigned int fTauSignalChCands;
    std::vector<TauId> fTauIds;

    std::vector<XYZTLorentzVector> fJets;
    std::vector<double> fJetsBtags;
    std::vector<double> fJetsChf;
    std::vector<double> fJetsNhf;
    std::vector<double> fJetsElf;
    std::vector<double> fJetsPhf;
    std::vector<double> fJetsMuf;
    std::vector<int> fJetsChm;
    std::vector<int> fJetsNhm;
    std::vector<int> fJetsElm;
    std::vector<int> fJetsPhm;
    std::vector<int> fJetsMum;
    std::vector<double> fJetsJec;
    std::vector<double> fJetsArea;
    std::vector<bool> fJetsLooseId;
    std::vector<bool> fJetsTightId;

    // nonIsoMuons
    std::vector<XYZTLorentzVector> fNonIsoMuons;
    std::vector<bool> fNonIsoMuons_IsGlobalMuon;
    std::vector<bool> fNonIsoMuons_IsTrackerMuon;
    std::vector<bool> fNonIsoMuons_AllMuons;
    std::vector<bool> fNonIsoMuons_AllGlobalMuons;
    std::vector<bool> fNonIsoMuons_AllStandAloneMuons;
    std::vector<bool> fNonIsoMuons_AllTrackerMuons;
    std::vector<bool> fNonIsoMuons_TrackerMuonArbitrated;
    std::vector<bool> fNonIsoMuons_AllArbitrated;
    std::vector<bool> fNonIsoMuons_GlobalMuonPromptTight;
    std::vector<bool> fNonIsoMuons_TMLastStationLoose;
    std::vector<bool> fNonIsoMuons_TMLastStationTight;
    std::vector<bool> fNonIsoMuons_TMOneStationLoose;
    std::vector<bool> fNonIsoMuons_TMLastStationOptimizedLowPtLoose;
    std::vector<bool> fNonIsoMuons_TMLastStationOptimizedLowPtTight;
    std::vector<bool> fNonIsoMuons_GMTkChiCompatibility;
    std::vector<bool> fNonIsoMuons_GMTkKinkTight;
    std::vector<bool> fNonIsoMuons_TMLastStationAngLoose;
    std::vector<bool> fNonIsoMuons_TMLastStationAngTight;
    std::vector<bool> fNonIsoMuons_TMLastStationOptimizedBarrelLowPtLoose;
    std::vector<bool> fNonIsoMuons_TMLastStationOptimizedBarrelLowPtTight;
    std::vector<int> fNonIsoMuons_InnerTrackNTrkHits;
    std::vector<int> fNonIsoMuons_InnerTrackNPixelHits;
    std::vector<int> fNonIsoMuons_GlobalTrackNMuonHits;
    std::vector<bool> fNonIsoMuons_NormChiSquare;
    std::vector<float> fNonIsoMuons_IPTwrtBeamLine; 
    std::vector<float> fNonIsoMuons_IPZwrtPV;
    std::vector<float> fNonIsoMuons_TrackIso;
    std::vector<float> fNonIsoMuons_EcalIso;
    std::vector<float> fNonIsoMuons_HcalIso;
    std::vector<float> fNonIsoMuons_RelIso;

    // nonIsoElectrons
    std::vector<XYZTLorentzVector> fNonIsoElectrons;
    std::vector<bool> fNonIsoElectrons_GsfTrkRefIsNull;
    std::vector<bool> fNonIsoElectrons_SuperClusterRefIsNull;
    std::vector<float> fNonIsoElectrons_SuperClusterRefEta;
    std::vector<float> fNonIsoElectrons_SuperClusterRefPhi;
    std::vector<bool> fNonIsoElectrons_SimpleId_Loose;
    std::vector<bool> fNonIsoElectrons_SimpleId_RobustLoose;
    std::vector<bool> fNonIsoElectrons_SimpleId_Tight;
    std::vector<bool> fNonIsoElectrons_SimpleId_RobustTight;
    std::vector<bool> fNonIsoElectrons_SimpleId_RobustHighEnergy;
    std::vector<float> fNonIsoElectrons_ID_EleId95relIso;
    std::vector<float> fNonIsoElectrons_ID_EleId90relIso;
    std::vector<float> fNonIsoElectrons_ID_EleId85relIso; 
    std::vector<float> fNonIsoElectrons_ID_EleId80relIso;
    std::vector<float> fNonIsoElectrons_ID_EleId70relIso;
    std::vector<float> fNonIsoElectrons_ID_EleId60relIso;
    std::vector<int> fNonIsoElectrons_NLostHitsInTrker;
    std::vector<float> fNonIsoElectrons_DeltaCotTheta;
    std::vector<float> fNonIsoElectrons_DistanceOSTrk;
    std::vector<float> fNonIsoElectrons_IPwrtBeamSpot;
    std::vector<float> fNonIsoElectrons_TrackIso;
    std::vector<float> fNonIsoElectrons_EcalIso;
    std::vector<float> fNonIsoElectrons_HcalIso;
    std::vector<float> fNonIsoElectrons_RelIso;
    std::vector<float> fNonIsoElectrons_ElectronMuonDeltaR;
    
    // MET is really 2-vector, but let's just use this for consistency
    XYZTLorentzVector fRawMet;
    double fRawMetSumEt;
    XYZTLorentzVector fType1Met;
    XYZTLorentzVector fType2Met;

    XYZTLorentzVector fTop;

    double fAlphaT;

    bool fPassedBTagging;

    // Gen level stuff
    XYZTLorentzVector fGenMet;

    // Tau embedding stuff
    XYZTLorentzVector fTauEmbeddingMuon;
    XYZTLorentzVector fTauEmbeddingMet;
    XYZTLorentzVector fTauEmbeddingCaloMet;
  };
}

#endif

