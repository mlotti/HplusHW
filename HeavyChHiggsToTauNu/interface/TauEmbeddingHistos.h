// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingHistos_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauEmbeddingHistos_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Point3D.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
}
namespace reco {
  class Candidate;
  class BaseTau;
  class GenParticle;
  class Track;
}
namespace pat {
  class Muon;
}
class TFileDirectory;

class TH1;
class TH2;

namespace HPlus {
  class EventWeight;
}

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
      explicit Histo(const HPlus::EventWeight& eventWeight);
      ~Histo();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title);
      //void fill(const reco::Candidate& cand);
      void fill(const math::XYZTLorentzVector& cand);

      template <typename T>
      void fill(const T& cand) {
        fill(cand.p4());
      }

    private:
      const HPlus::EventWeight& fEventWeight;

      TH1 *hPt;
      TH1 *hEta;
      TH1 *hPhi;
    };

    class HistoTrack {
    public:
      explicit HistoTrack(const HPlus::EventWeight& eventWeight);
      ~HistoTrack();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title);
      void fill(const reco::Track& track, const math::XYZPoint& vertex);

    private:
      const HPlus::EventWeight& fEventWeight;

      TH1 *hNhits;
      TH1 *hChi2Norm;
      TH1 *hDxy;
      TH1 *hDz;
    };

    class Histo2 {
    public:
      explicit Histo2(const HPlus::EventWeight& eventWeight);
      ~Histo2();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title);
      //void fill(const reco::Candidate& x, const reco::Candidate& y);
      void fill(const math::XYZTLorentzVector& x, const math::XYZTLorentzVector& y);
      template <typename T>
      void fill(const math::XYZTLorentzVector& x, const T& y) {
        fill(x, y.p4());
      }
      template <typename T>
      void fill(const T& x, const math::XYZTLorentzVector& y) {
        fill(x.p4(), y);
      }
      template <typename T1, typename T2>
      void fill(const T1& x, const T2& y) {
        fill(x.p4(), y.p4());
      }

    private:
      const HPlus::EventWeight& fEventWeight;

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
      explicit HistoMet(const edm::InputTag src, const HPlus::EventWeight& eventWeight);
      explicit HistoMet(const HPlus::EventWeight& eventWeight);
      ~HistoMet();

      void init(TFileDirectory& dir, const std::string& name, const std::string& title,
                const std::string& candName, const std::string& nuName);

      const math::XYZTLorentzVector fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const edm::Event& iEvent);
      void fill(const reco::Candidate& cand, const reco::GenParticle *candNu, const math::XYZTLorentzVector& met);

    private:
      edm::InputTag src_;
      const HPlus::EventWeight& fEventWeight;

      TH1 *hMet;
      TH1 *hMetX;
      TH1 *hMetY;
      TH1 *hMetPhi;

      TH1 *hCandMetDPhi;
      TH1 *hNuMetDPhi;
    };


    class HistoMet2 {
    public:
      HistoMet2(const edm::ParameterSet& pset, double metCut, const HPlus::EventWeight& eventWeight);
      HistoMet2(double metCut, const HPlus::EventWeight& eventWeight);
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
      const HPlus::EventWeight& fEventWeight;

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

      TH1 *hMuonOrigMetMt;
      TH1 *hTauMetMt;

      TH1 *hWTauNuMetDPhi;
      TH2 *hWNuOrigMetMuonTauNuMetDPhi;

      TH1 *hMetOrigDiff;
      TH1 *hMetOrigDPhi;
      TH2 *hMuonOrigMetDPhiMetOrigDiff;
    };

    class HistoIso {
    public:
      explicit HistoIso(const HPlus::EventWeight& eventWeight);
      ~HistoIso();

      void init(TFileDirectory& dir, const std::string& name);

      void fill(double sumPt, double maxPt, size_t occupancy);

    private:
      const HPlus::EventWeight& fEventWeight;
      TH1 *hSumPt;
      TH1 *hMaxPt;
      TH1 *hOccupancy;
    };

    class HistoIso2 {
    public:
      explicit HistoIso2(const HPlus::EventWeight& eventWeight);
      ~HistoIso2();

      void init(TFileDirectory& dir, const std::string& muonName, const std::string& tauName);

      void fill(double muonIso, double tauSumPt, double tauMaxPt, size_t tauOccupancy);

    private:
      const HPlus::EventWeight& fEventWeight;
      TH2 *hSumPt;
      TH2 *hMaxPt;
      TH2 *hOccupancy;
    };
  }
}

#endif
