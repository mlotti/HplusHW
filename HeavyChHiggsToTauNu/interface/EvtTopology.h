//#######################################################################
// -*- C++ -*-
//       File Name:  EvtTopology.h
// Original Author:  Alexandros Attikis
//         Created:  Mon 4 Oct 2010
//     Description:  Designed to calculate Evt Topology related variables                   
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EvtTopology_h
/// ROOT libraries
#include <Math/Vector3D.h>
#include <Math/Point3D.h>
#include <TVector3.h>
#include <TLorentzVector.h>
/// C++ libraries
#include <functional>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <assert.h>
#include <iostream>
#include <vector>
/// CMSSW libraries
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MathFunctions.h"

struct AlphaStruc{
  float fAlphaT;
  float fJt; // Jt = Ht - TauJetEt - LdgJetEt
  float fHt;
  float fDeltaHt;
  float fMHt;
  vector<float> vDiJetMassesNoTau;
};

namespace reco {
  class Candidate;
}

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {

  class EvtTopology {
  public:
    EvtTopology(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~EvtTopology();

    bool analyze( const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets);
    AlphaStruc alphaT( void );
    
  private:
    // Input parameters
    // std::string fDiscriminator;
    // double fDiscrCut;
    double fAlphaTCut;

    // Counters
    Count fEvtTopologyCount;
    Count fAlphaTCutCount;
    
    // Histograms
    TH1 *hAlphaT;
    
    /// Other variables
    AlphaStruc sAlpha;
    MathFunctions oMath;
  };
}

#endif
