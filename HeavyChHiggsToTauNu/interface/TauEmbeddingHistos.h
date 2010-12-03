// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingHistos_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingHistos_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
}
namespace reco {
  class Candidate;
  class BaseTau;
  class GenParticle;
}
namespace pat {
  class Muon;
}
class TFileDirectory;

class TH1;
class TH2;

namespace hplus {
  namespace te {

    /**
     * Histogram naming convention:
     *
     * TH1
     * Particle_Quantity
     *
     * TH2
     * ParticleX_ParticleY_Quantity (if the quantity is the same for both axes)
     * ParticleX_QuantityX_ParticleY_QuantityY
     *
     * If Quantity is a function of two particles, then
     * Particle1,Particle2_Quantity
     * Particle1,Particle2X_Particle1,Particle2Y_Quantity
     * Particle1,Particle2X_QuantityX_Particle1,Particle2Y_QuantityY
     *
     * Custom annotation can be given as _Annotation postfix
     *
     * Particles:
     * Muon
     * Tau
     * GenTau
     * Met
     * GenMet...
     * ...MetOriginal
     * GenWNu
     * GenTauNu
     * GenWNuTauNu
     *
     * Quantities:
     * Pt
     * Eta
     * Phi
     * Et
     * X
     * Y
     * DQuantity for difference (particle1, particle2)
     */

    class Histo {
    public:
      Histo();
      ~Histo();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title);
      void fill(const reco::Candidate& cand);

    private:
      TH1 *hPt;
      TH1 *hEta;
      TH1 *hPhi;
    };

    class Histo2 {
    public:
      Histo2();
      ~Histo2();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title);
      void fill(const reco::Candidate& cand1, const reco::Candidate& cand2);

    private:
      TH2 *hPt;
      TH2 *hEta;
      TH2 *hPhi;

      TH1 *hDPt;
      TH1 *hDR;
      TH1 *hDEta;
      TH1 *hDPhi;
    };


    class HistoMet {
    public:
      explicit HistoMet(const edm::InputTag src);
      HistoMet();
      ~HistoMet();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title,
                const std::string& candName, const std::string& nuName);

      const math::XYZTLorentzVector fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const edm::Event& iEvent);
      void fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const math::XYZTLorentzVector& met);

    private:
      edm::InputTag src_;

      TH1 *hMet;
      TH1 *hMetX;
      TH1 *hMetY;
      TH1 *hMetPhi;

      TH1 *hCandMetDPhi;
      TH1 *hNuMetDPhi;
    };


    class HistoMet2 {
    public:
      HistoMet2(const edm::ParameterSet& pset, double metCut);
      explicit HistoMet2(double metCut);
      ~HistoMet2();

      void init(TFileDirectory& dir, const std::string& name);

      void fill(const pat::Muon& muon, const reco::BaseTau& tau,
                const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                const edm::Event& iEvent);

      void fill(const reco::Candidate& muon, const reco::Candidate& tau,
                const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                const math::XYZTLorentzVector& metOrig, const math::XYZTLorentzVector& met);

    private:
      void fillInternal(const reco::Candidate& muon, const reco::Candidate& tau,
                        const reco::GenParticle *wNu, const reco::GenParticle *tauNu,
                        const math::XYZTLorentzVector& metOrig, const math::XYZTLorentzVector& met);

      edm::InputTag embeddedSrc_;
      edm::InputTag originalSrc_;

      double metCut_;

      HistoMet hMet;
      HistoMet hOrigMet;

      TH1 *hOrigMetAfterCut;

      TH2 *hMetMet;
      TH2 *hMetMetX;
      TH2 *hMetMetY;
      TH2 *hMetMetPhi;

      TH1 *hMuonMetDPhi;
      TH1 *hTauOrigMetDPhi;
      TH2 *hMuonOrigMetTauMetDPhi;

      TH1 *hWTauNuMetDPhi;
      TH2 *hWNuOrigMetMuonTauNuMetDPhi;

      TH1 *hMetOrigDiff;
      TH1 *hMetOrigDPhi;
      TH2 *hMuonOrigMetDPhiMetOrigDiff;
    };
  }
}

#endif
