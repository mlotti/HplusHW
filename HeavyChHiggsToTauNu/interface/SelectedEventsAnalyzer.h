// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SELECTEDEVENTSANALYZER_H
#define HiggsAnalysis_HeavyChHiggsToTauNu_SELECTEDEVENTSANALYZER_H

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerTauMETEmulation.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "TH1F.h"

namespace HPlus {
  class SelectedEventsAnalyzer {
  public:
    SelectedEventsAnalyzer(std::string prefix);
    ~SelectedEventsAnalyzer();

    void fill(edm::PtrVector<pat::Tau>& selectedTau,
	      const TauSelection::Data& tauData,
	      const GlobalElectronVeto::Data& eVetoData,
	      const GlobalMuonVeto::Data& muVetoData,
	      const JetSelection::Data& jetData,
	      const BTagging::Data& btagData,
	      const METSelection::Data& METData,
	      const FakeMETVeto::Data& fakeMETVetoData,
	      const ForwardJetVeto::Data& forwardVetoData,
	      const double weight);

  private:
    TH1 *hTauPtAfterAllSelections;
    TH1 *hTauEtaAfterAllSelections;
    TH1 *hTauPhiAfterAllSelections;
    TH1 *hRTauAfterAllSelections;
    TH1 *hNJetsAfterAllSelections;
    TH1 *hBJetsAfterAllSelections;
    TH1 *hMETAfterAllSelections;
    TH1 *hMETPhiAfterAllSelections;
    TH1 *hFakeMETVetoAfterAllSelections;
    TH1 *hDeltaPhiAfterAllSelections;
    TH1 *hTransverseMassAfterAllSelections;

    DeltaPhi fDeltaPhi;
    TransverseMass fTransverseMass;
  };
}

#endif
