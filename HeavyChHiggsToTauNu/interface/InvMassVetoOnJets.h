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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MathFunctions.h"
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;

namespace reco {
  class Candidate;
}

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class InvMassVetoOnJets: public BaseSelection {
  public:

    /**
     * Class to encapsulate the access to the data members.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data();
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      // const InvMassVetoOnJets::AlphaStruc alphaT() const { return fInvMassVetoOnJets->sAlpha; }

      friend class InvMassVetoOnJets;
    private:
      bool fPassedEvent;
    };

    InvMassVetoOnJets(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~InvMassVetoOnJets();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    const double fPtCut;
    const double fEtaCut;
    const bool fSetTrueToUseModule;
    // Counters
    Count fDiJetsCutSubCount;
    Count fTriJetsCutSubCount;

    Count fInvMassWWindow10SubCount;
    Count fInvMassWWindow15SubCount;
    Count fInvMassWWindow20SubCount;
    Count fInvMassWWindow25SubCount;

    Count fInvMassTopWindow10SubCount;
    Count fInvMassTopWindow15SubCount;
    Count fInvMassTopWindow20SubCount;
    Count fInvMassTopWindow25SubCount;

    // Histograms
    WrappedTH1 *hDiJetInvMass;
    WrappedTH1 *hDiJetInvMassCutFail;
    WrappedTH1 *hDiJetInvMassCutPass;
    WrappedTH1 *hDiJetInvMassWCutFail;

    WrappedTH1 *hTriJetInvMass;
    WrappedTH1 *hTriJetInvMassCutFail;
    WrappedTH1 *hTriJetInvMassCutPass;
    WrappedTH1 *hTriJetInvMassTopCutFail;

    WrappedTH1 *hInvMass;
    WrappedTH1 *hInvMassCutFail;
    WrappedTH1 *hInvMassCutPass;

  };
}

#endif
