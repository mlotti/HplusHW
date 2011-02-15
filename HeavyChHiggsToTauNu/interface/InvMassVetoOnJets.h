//#######################################################################
// -*- C++ -*-
//       File Name:  InvMassVetoOnJets.h
// Original Author:  Alexandros Attikis
//         Created:  Mon 4 Oct 2010
//     Description:  Designed to calculate DiJet and TriJet invariant 
//                   masses and veto if they match specific mothers.
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_InvMassVetoOnJets_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_InvMassVetoOnJets_h
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
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MathFunctions.h"
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;

namespace reco {
  class Candidate;
}

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {
  
  class InvMassVetoOnJets {
  public:

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
      Data(const InvMassVetoOnJets *invMassVetoOnJets, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      // const InvMassVetoOnJets::AlphaStruc alphaT() const { return fInvMassVetoOnJets->sAlpha; }
    
    private:
      const InvMassVetoOnJets *fInvMassVetoOnJets;
      const bool fPassedEvent;
    };

    InvMassVetoOnJets(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~InvMassVetoOnJets();

    // Data analyze( const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
    Data analyze( const edm::PtrVector<pat::Jet>& jets );

  private:
    const double fPtCut;
    const double fEtaCut;
    // Counters
    Count fInvMassVetoOnJetsCount;
    Count fInvMassVetoOnJetsPtCutSubCount;
    Count fInvMassVetoOnJetsEtaCutSubCount;
    Count fInvMassVetoOnJetsDiJetsCutSubCount;
    Count fInvMassVetoOnJetsTriJetsCutSubCount;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histograms
    TH1 *hDiJetInvMass;
    TH1 *hDiJetInvMassCutFail;
    TH1 *hDiJetInvMassCutPass;
    TH1 *hDiJetInvMassWCutFail;

    TH1 *hTriJetInvMass;
    TH1 *hTriJetInvMassCutFail;
    TH1 *hTriJetInvMassCutPass;
    TH1 *hTriJetInvMassTopCutFail;

    TH1 *hInvMass;
    TH1 *hInvMassCutFail;
    TH1 *hInvMassCutPass;

  };
}

#endif
