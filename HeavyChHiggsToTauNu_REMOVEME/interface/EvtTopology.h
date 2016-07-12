//#######################################################################
// -*- C++ -*-
//       Filesph Name:  EvtTopology.h
// Original Author:  Alexandros Attikis
//         Created:  Mon 4 Oct 2010
//     Description:  Designed to calculate Evt Topology related variables                   
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h
// ROOT libraries
#include <Math/Vector3D.h>
#include <Math/Point3D.h>
#include <TVector3.h>
#include <TLorentzVector.h>
// C++ libraries
#include <functional>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <assert.h>
#include <iostream>
#include <vector>
// CMSSW libraries
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MathFunctions.h"
// Sphericity, Aplanarity, Planarity
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"
#include "DataFormats/Math/interface/deltaR.h"

namespace reco {
  class Candidate;
}

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class EvtTopology: public BaseSelection {
  public:
    typedef struct {
      float fAlphaT;
      float fJt; // Jt = Ht - TauJetEt - LdgJetEt
      float fHt;
      float fDeltaHt;
      float fMHt;
      vector<float> vDiJetMassesNoTau;
    } AlphaStruc;
    typedef struct {
      float fQOne;
      float fQTwo;
      float fQThree;
      float fSphericity;
      float fAplanarity;
      float fPlanarity;
      float fCircularity;
    } MomentumTensorStruc;
    typedef struct {
      float fQOne;
      float fQTwo;
      float fQThree;
      float fCparameter;
      float fDparameter;
      float fJetThrust;
    } SpherocityTensorStruc;

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

      const bool passedEvent() const { return fPassedEvent; }
      const double getSphericity() const { return sMomentumTensor.fSphericity; }
      const double getPlanarity() const { return sMomentumTensor.fPlanarity; }
      const double getAplanarity() const { return sMomentumTensor.fAplanarity; }
      const double getCircularity() const { return sMomentumTensor.fCircularity; }
      const double getCparameter() const { return sSpherocityTensor.fCparameter; }
      const double getDparameter() const { return sSpherocityTensor.fDparameter; }
      const double getJetThrust() const { return sSpherocityTensor.fJetThrust; }
      const EvtTopology::AlphaStruc alphaT() const { return sAlpha; }
      const EvtTopology::MomentumTensorStruc MomentumTensor() const { return sMomentumTensor; }
      const EvtTopology::SpherocityTensorStruc SpherocityTensor() const { return sSpherocityTensor; }

      friend class EvtTopology;

    private:
      bool fPassedEvent;
      EvtTopology::AlphaStruc sAlpha;
      EvtTopology::MomentumTensorStruc sMomentumTensor;
      EvtTopology::SpherocityTensorStruc sSpherocityTensor;
    };

    EvtTopology(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~EvtTopology();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
    // Data InvMassVetoOnJets( const edm::PtrVector<pat::Jet>& jets); obsolete

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
    bool CalcAlphaT(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output);
    vector<float> CalcMomentumTensorEigenValues(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output);
    vector<float> CalcSpherocityTensorEigenValues(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output);
    bool CalcCandDParameters(vector<float> eigenvalues, EvtTopology::Data& output);
    bool CalcSphericity(vector<float> eigenvalues, EvtTopology::Data& output);
    bool CalcAplanarity(vector<float> eigenvalues, EvtTopology::Data& output);
    bool CalcPlanarity(vector<float> eigenvalues, EvtTopology::Data& output);
    bool CalcCircularity(const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output);
    bool CalcJetThrust(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output);

    // Input parameters
    // std::string fDiscriminator;
    // double fDiscrCut;
    const double fAlphaTCut;
    const double fSphericityCut;
    const double fAplanarityCut;
    const double fPlanarityCut;
    const double fCircularityCut;
    const double fCparameterCut;
    const double fDparameterCut;
    const double fJetThrustCut;

    // Counters
    Count fEvtTopologyCount;
    Count fAlphaTCutCount;
    Count fSphericityCutCount;
    Count fAplanarityCutCount;
    Count fPlanarityCutCount;
    Count fCircularityCutCount;
    Count fCparameterCutCount;
    Count fDparameterCutCount;
    Count fJetThrustCutCount;

    // Histograms
    WrappedTH1 *hAlphaT;
    WrappedTH1 *hSphericity;
    WrappedTH1 *hAplanarity;
    WrappedTH1 *hPlanarity;
    WrappedTH1 *hCircularity;
    WrappedTH1 *hCparameter;
    WrappedTH1 *hDparameter;
    /*
      WrappedTH1 *hDiJetInvMass;
      WrappedTH1 *hDiJetInvMassCutFail;
      WrappedTH1 *hDiJetInvMassCutPass;
      WrappedTH1 *hDiJetInvMassWCutFail;
    */
    
  };
}

#endif
