#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingHistos.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PFTauIsolationCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "TH1F.h"
#include "TH2F.h"

using hplus::te::Histo;
using hplus::te::HistoTrack;
using hplus::te::Histo2;
using hplus::te::HistoMet2;
using hplus::te::HistoIso;
using hplus::te::HistoIso2;

class HPlusTauEmbeddingAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusTauEmbeddingAnalyzer(const edm::ParameterSet&);
  ~HPlusTauEmbeddingAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef std::pair<const reco::GenParticle *, const reco::GenParticle *> GenParticlePair;
  template <typename I>
  GenParticlePair findTauNu(I begin, I end) const;
  template <typename I>
  GenParticlePair findMuNuFromW(const reco::Candidate& recoMu, I begin, I end) const;

  struct GenTauDaughters {
    GenTauDaughters(): nprongs(0), leadingChargedPion(0), visible() {}
    GenTauDaughters(size_t n, const reco::GenParticle *ptr, const reco::GenParticle::LorentzVector& vec):
      nprongs(n), leadingChargedPion(ptr), visible(vec) {}

    size_t nprongs;
    const reco::GenParticle *leadingChargedPion;
    reco::GenParticle::LorentzVector visible;
  };

  GenTauDaughters genTauDaughters(const reco::GenParticle& tau) const;

  edm::InputTag muonSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag pfCandSrc_;
  edm::InputTag vertexSrc_;
  edm::InputTag genParticleOriginalSrc_;
  edm::InputTag genParticleEmbeddedSrc_;

  double muonTauCone_;

  HPlus::EventWeight eventWeight_;
  HPlus::PFTauIsolationCalculator tauIsolationCalculator_;

  struct HistoAll {
    HistoAll(double metCut, const HPlus::EventWeight& eventWeight, const HPlus::PFTauIsolationCalculator& isoCalc):
      eventWeight_(eventWeight), tauIsolationCalculator_(isoCalc),
      metCut_(metCut), hMetNu(metCut, eventWeight_),
      hMuon(eventWeight_),
      hMuonTrack(eventWeight_),
      hTau(eventWeight_),
      hTauLead(eventWeight_),
      hTauLeadChargedHadr(eventWeight_),
      hTauIsoShrinkingCone(eventWeight_),
      hTauIsoShrinkingCone05(eventWeight_),
      hTauIsoHpsLoose(eventWeight_),
      hTauIsoHpsMedium(eventWeight_),
      hTauIsoHpsTight(eventWeight_),
      hMuonRelIsoTauIsoShrinkingCone(eventWeight_),
      hMuonRelIsoTauIsoHpsMedium(eventWeight_),
      hMuonRelIsoTauIsoHpsTight(eventWeight_),
      hPFCandLead(eventWeight_),
      hTauPFCandLead(eventWeight_),
      hPFCandLeadHadr(eventWeight_),
      hPFCandLeadHadrTrack(eventWeight_),
      hTauPFCandLeadHadr(eventWeight_),
      hTauGen(eventWeight_),
      hTauGenVis(eventWeight_),
      hNuGen(eventWeight_),
      hTauNuGen(eventWeight_),
      hTauGenLeadingChargedPi(eventWeight_),
      hTauGenTauGenLeadingChargedPi(eventWeight_),
      hTauGenVisTauGenLeadingChargedPi(eventWeight_),
      hMuonTau(eventWeight_),
      hMuonTauLdg(eventWeight_)
    {}
    ~HistoAll() {
      for(size_t i=0; i<hMets.size(); ++i) {
        delete hMets[i];
      }
    }

    void init(const edm::ParameterSet& pset, TFileDirectory& dir) {
      std::vector<std::string> metNames = pset.getParameterNames();
      for(std::vector<std::string>::const_iterator iName = metNames.begin(); iName != metNames.end(); ++iName) {
        if(*iName == "GenMetNu")
          throw cms::Exception("Configuration") << "GenMetNu is a reserved MET name" << std::endl;
        HistoMet2 *met = new HistoMet2(pset.getUntrackedParameter<edm::ParameterSet>(*iName), metCut_, eventWeight_);
        met->init(dir, *iName);
        hMets.push_back(met);
      }
      hMetNu.init(dir, "GenMetNu");      

      hMuon.init(dir, "Muon", "Muon");
      hMuonTrack.init(dir, "Muon", "Muon");
      /*
      hMuonTrkIso = HPlus::makeTH<TH1F>("Muon_IsoTrk", "Muon track isolation", 100, 0, 100);
      hMuonTrkRelIso = HPlus::makeTH<TH1F>("Muon_IsoTrkRel", "Muon track relative isolation", 100, 0, 1);
      hMuonCaloIso = HPlus::makeTH<TH1F>("Muon_IsoCalo", "Muon calo isolation", 100, 0, 100);
      hMuonCaloRelIso = HPlus::makeTH<TH1F>("Muon_IsoCaloRel", "Muon calo relative isolation", 100, 0, 1);
      hMuonIso = HPlus::makeTH<TH1F>("Muon_IsoTotal", "Muon total isolation", 50, 0, 50);
      */
      hMuonRelIso = HPlus::makeTH<TH1F>(dir, "Muon_IsoTotalRel", "Muon total relative isolation", 100, 0, 1);

      hTau.init(dir, "Tau", "Tau");
      hTauLead.init(dir, "Tau_LeadPFCand", "Tau leading cand");
      hTauLeadExists = HPlus::makeTH<TH1F>(dir, "Tau_LeadPFCand_Exists", "Tau leading cand exists", 2, 0, 2);
      hTauLeadChargedHadr.init(dir, "Tau_LeadPFChargedHadrCand", "Tau leading charged hadr cand");
      hTauLeadChargedHadrExists = HPlus::makeTH<TH1F>(dir, "Tau_LeadPFChargedHadrCand_Exists", "Tau leading charged hadr cand exists", 2, 0, 2);
      hTauLeadTrackExists = HPlus::makeTH<TH1F>(dir, "Tau_LeadTrack_Exists", "Tau leading track exists", 2, 0, 2);
      hTauR = HPlus::makeTH<TH1F>(dir, "Tau_Rtau", "Rtau", 120, 0., 1.2);

      hTauIsoShrinkingCone.init(dir, "Tau_IsoShrinkingCone");
      hTauIsoShrinkingCone05.init(dir, "Tau_IsoShrinkingCone05");
      hTauIsoHpsLoose.init(dir, "Tau_IsoHpsLoose");
      hTauIsoHpsMedium.init(dir, "Tau_IsoHpsMedium");
      hTauIsoHpsTight.init(dir, "Tau_IsoHpsTight");

      hMuonRelIsoTauIsoShrinkingCone.init(dir, "IsoTotalRel", "IsoShrinkingCone");
      hMuonRelIsoTauIsoHpsMedium.init(dir, "IsoTotalRel", "IsoHpsMedium");
      hMuonRelIsoTauIsoHpsTight.init(dir, "IsoTotalRel", "IsoHpsTight");
      /*
      hTauIsoChargedHadrPtSum = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPtSum", "Tau isolation charged hadr cand pt sum", 200, 0, 100);
      hTauIsoChargedHadrPt05Sum = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPt05Sum", "Tau isolation charged hadr cand pt sum, pt > 0.5", 200, 0, 100);
      hTauIsoChargedHadrPt10Sum = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPt10Sum", "Tau isolation charged hadr cand pt sum, pt > 1.0", 200, 0, 100);
      hTauIsoChargedHadrPtSumRel = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPtSumRel", "Tau isolation charged hadr cand relative pt sum", 200, 0, 20);
      hTauIsoChargedHadrPtMax = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPtMax", "Tau isolation charged hadr cand pt max", 100, 0, 100);
      hTauIsoChargedHadrPtMaxRel = HPlus::makeTH<TH1F>("Tau_IsoChargedHadrPtMaxRel", "Tau isolation charged hadr cand relative pt max", 200, 0, 20);
      hMuonTrkTauPtSumIso = HPlus::makeTH<TH2F>("Muon_IsoTrk_Tau_IsoChargedHadrPtSum", "Muon trk vs. tau ptsum isolation", 100,0,100, 100,0,100);
      hMuonTrkTauPtSumIsoRel = HPlus::makeTH<TH2F>("Muon_IsoTrkRel_Tau_IsoChargedHadrPtSumRel", "Muon trk vs. tau ptsum relative isolation", 200,0,1, 200,0,20);
      hMuonTauPtSumIso = HPlus::makeTH<TH2F>("Muon_IsoTotal_Tau_IsoChargedHadrPtSum", "Muon total vs. tau ptsum isolation", 100,0,100, 200,0,20);
      hMuonTauPtSumIsoRel = HPlus::makeTH<TH2F>("Muon_IsoTotal_Tau_IsoChargedHadrPtSumRel", "Muon total vs. tau ptsum relative isolation", 200,0,1, 200,0,20);
      */

      hPFCandNumber = HPlus::makeTH<TH1F>(dir, "PFCand_Number", "Number of PF Candidates", 100, 0, 100);
      hPFCandLead.init(dir, "PFCand_Leading", "Leading PF Candidate");
      hPFCandLeadParticleType = HPlus::makeTH<TH1F>(dir, "PFCand_Leading_ParticleType", "Leading PF Candidate particle type", 10, 0, 10);
      hPFCandLeadCharge = HPlus::makeTH<TH1F>(dir, "PFCand_Leading_Charge", "Leading PF Candidate charge", 5, -2, 2);
      hTauPFCandLead.init(dir, "Tau_PFCand_Leading", "Tau vs. leading PF Candidate");

      hPFCandLeadHadr.init(dir, "PFCand_LeadingHadr", "Leading hadronic PF Candidate");
      hPFCandLeadHadrCharge = HPlus::makeTH<TH1F>(dir, "PFCand_LeadingHadr_Charge", "Leading hadronic PF Candidate charge", 5, -2, 2);
      hPFCandLeadHadrTrack.init(dir, "PFCand_LeadingHadr", "Leading hadronic PF Candidate");
      hTauPFCandLeadHadr.init(dir, "Tau_PFCand_LeadingHadr", "Tau vs. leading hadronic PF Candidate");

      hTauGen.init(dir, "GenTau", "Tau gen");
      hTauGenVis.init(dir, "GenTauVis", "Visible tau gen");
      hNuGen.init(dir, "GenTauNu", "Nu gen");
      hTauNuGen.init(dir, "GenTau_GenTauNu", "Gen tau vs. nu");
      hTauGenNprongs = HPlus::makeTH<TH1F>(dir, "GenTau_NProngs", "Number of charged pion daughters of generator tau", 10, 0, 10);
      hTauGenLeadingChargedPi.init(dir, "GenTauLeadingChargedPi", "Gen tau leading charged pi");
      hTauGenTauGenLeadingChargedPi.init(dir, "GenTau_GenTauLeadingChargedPi", "Gen tau vs. leading charged pi");
      hTauGenVisTauGenLeadingChargedPi.init(dir, "GenTauVis_GenTauLeadingChargedPi", "Visible gen tau vs. leading charged pi");

      hTauGenMass = HPlus::makeTH<TH1F>(dir, "GenTau_Mass", "Tau mass at generator level", 100, 1.7, 1.9);
      hTauGenDecayMass = HPlus::makeTH<TH1F>(dir, "GenTauDecay_Mass", "Tau mass from decay products at generator level", 100, 1.7, 1.9);

      hMuonTau.init(dir, "Muon_Tau", "Mu vs. tau");
      hMuonTauLdg.init(dir, "Muon_TauLdg", "Mu vs. tau ldg cand");
    }

    void fillMets(const reco::Muon& muon, const reco::BaseTau& tau,
                  const reco::GenParticle *muonNu, const reco::GenParticle *tauNu,
                  const edm::Event& iEvent) {
      for(size_t i=0; i<hMets.size(); ++i) {
        hMets[i]->fill(muon, tau, muonNu, tauNu, iEvent);
      }
    }

    void fillMuonTauIso(const pat::Muon& muon, const pat::Tau& tau) {
      const reco::MuonIsolation& iso = muon.isolationR03();
      double caloIso = iso.emEt+iso.hadEt;
      double totalIso = caloIso+iso.sumPt;
      double totalIsoRel = totalIso/muon.pt();

      /*
      hMuonTrkIso->Fill(iso.sumPt);
      hMuonTrkRelIso->Fill(iso.sumPt/muon.pt());
      hMuonCaloIso->Fill(caloIso);
      hMuonCaloRelIso->Fill(caloIso/muon.pt());
      hMuonIso->Fill(totalIso);
      */
      hMuonRelIso->Fill(totalIsoRel, eventWeight_.getWeight());

      double sumPt=0;
      double maxPt=0;
      size_t occupancy=0;

      tauIsolationCalculator_.calculateShrinkingConeByIsolation(tau, &sumPt, &maxPt, &occupancy);
      hTauIsoShrinkingCone.fill(sumPt, maxPt, occupancy);
      hMuonRelIsoTauIsoShrinkingCone.fill(totalIsoRel, sumPt, maxPt, occupancy);

      tauIsolationCalculator_.calculateShrinkingConeByIsolation(tau, 0.5, &sumPt, &maxPt, &occupancy);
      hTauIsoShrinkingCone05.fill(sumPt, maxPt, occupancy);

      tauIsolationCalculator_.calculateHpsLoose(tau, &sumPt, &maxPt, &occupancy);
      hTauIsoHpsLoose.fill(sumPt, maxPt, occupancy);

      tauIsolationCalculator_.calculateHpsMedium(tau, &sumPt, &maxPt, &occupancy);
      hTauIsoHpsMedium.fill(sumPt, maxPt, occupancy);
      hMuonRelIsoTauIsoHpsMedium.fill(totalIsoRel, sumPt, maxPt, occupancy);

      tauIsolationCalculator_.calculateHpsTight(tau, &sumPt, &maxPt, &occupancy);
      hTauIsoHpsTight.fill(sumPt, maxPt, occupancy);
      hMuonRelIsoTauIsoHpsTight.fill(totalIsoRel, sumPt, maxPt, occupancy);


      /*
      double ptSum = tau.isolationPFChargedHadrCandsPtSum();
      double ptMax = 0;
      double pt05Sum = 0.0;
      double pt10Sum = 0.0;
      const reco::PFCandidateRefVector& isoCands = tau.isolationPFChargedHadrCands();
      if(isoCands.isNonnull()) {
        for(reco::PFCandidateRefVector::const_iterator iCand = isoCands.begin(); iCand != isoCands.end(); ++iCand) {
          double pt = (*iCand)->pt();
          ptMax = std::max(ptMax, pt);
          if(pt > 0.5) {
            pt05Sum += pt;
            if(pt > 1.0) {
              pt10Sum += pt;
            }
          }
        }
      }
      hTauIsoChargedHadrPtSum->Fill(ptSum);
      hTauIsoChargedHadrPt05Sum->Fill(pt05Sum);
      hTauIsoChargedHadrPt10Sum->Fill(pt10Sum);
      hTauIsoChargedHadrPtSumRel->Fill(ptSum/tau.pt());
      hTauIsoChargedHadrPtMax->Fill(ptMax);
      hTauIsoChargedHadrPtMaxRel->Fill(ptMax/tau.pt());
      
      hMuonTrkTauPtSumIso->Fill(iso.sumPt, ptSum);
      hMuonTrkTauPtSumIsoRel->Fill(iso.sumPt/muon.pt(), ptSum/tau.pt());
      hMuonTauPtSumIso->Fill(totalIso, ptSum);
      hMuonTauPtSumIsoRel->Fill(totalIso/muon.pt(), ptSum/tau.pt());
      */
    }

    void fill(const pat::Muon& muon, const pat::Tau& tau,
              const reco::GenParticle *genMuon, const reco::GenParticle *genWNu,
              const reco::GenParticle *genTau, const reco::GenParticle *genTauNu,
              const GenTauDaughters& tauDaughters,
              const reco::Vertex& vertex,
              size_t pfCandsSize, const edm::Ptr<reco::PFCandidate>& pfCandLeading,
              const edm::Ptr<reco::PFCandidate>& pfCandLeadingHadr) {

      // Generator level tau mass from the tau daughters
      reco::GenParticle::LorentzVector tauDecaySum;
      for(reco::GenParticle::const_iterator iDaughter = genTau->begin(); iDaughter != genTau->end(); ++iDaughter) {
        tauDecaySum += iDaughter->p4();
      }
      double tauDecayMass = tauDecaySum.M();

      reco::GenParticle::LorentzVector nuWTauSum;
      if(genWNu && genTauNu) {
        nuWTauSum = genWNu->p4() + genTauNu->p4();
        hMetNu.fill(muon, tau, genWNu, genTauNu, genWNu->p4(), nuWTauSum);
      }


      hMuon.fill(muon);
      reco::TrackRef muonTrack= muon.globalTrack();
      if(muonTrack.isNonnull())
        hMuonTrack.fill(*muonTrack, vertex.position());

      hTau.fill(tau);
      hMuonTau.fill(muon, tau);

      const reco::PFCandidateRef leadCand = tau.leadPFCand();
      if(leadCand.isNonnull()) {
        hTauLeadExists->Fill(1.0, eventWeight_.getWeight());
        hTauLead.fill(*leadCand);
      }
      else {
        hTauLeadExists->Fill(0.0, eventWeight_.getWeight());
      }

      const reco::PFCandidateRef leadChargedCand = tau.leadPFChargedHadrCand();
      if(leadChargedCand.isNonnull()) {
        hTauLeadChargedHadrExists->Fill(1, eventWeight_.getWeight());
        hTauLeadChargedHadr.fill(*leadChargedCand);
        if(tau.p() > 0)
          hTauR->Fill(leadChargedCand->p()/tau.p(), eventWeight_.getWeight());
        hMuonTauLdg.fill(muon, *leadChargedCand);
      }
      else {
        hTauLeadChargedHadrExists->Fill(0.0, eventWeight_.getWeight());
      }
      if(tau.leadTrack().isNonnull()) {
        hTauLeadTrackExists->Fill(1.0, eventWeight_.getWeight());
      }
      else {
        hTauLeadTrackExists->Fill(0.0, eventWeight_.getWeight());
      }
                            
      fillMuonTauIso(muon, tau);

      hPFCandNumber->Fill(pfCandsSize, eventWeight_.getWeight());
      if(pfCandLeading.get()) {
        hPFCandLead.fill(*pfCandLeading);
        hPFCandLeadParticleType->Fill(pfCandLeading->particleId(), eventWeight_.getWeight());
        hPFCandLeadCharge->Fill(pfCandLeading->charge(), eventWeight_.getWeight());
        hTauPFCandLead.fill(tau, *pfCandLeading);
      }
      if(pfCandLeadingHadr.get()) {
        hPFCandLeadHadr.fill(*pfCandLeadingHadr);
        hPFCandLeadHadrCharge->Fill(pfCandLeadingHadr->charge(), eventWeight_.getWeight());
        reco::TrackRef track = pfCandLeadingHadr->trackRef();
        if(track.isNonnull()) {
          hPFCandLeadHadrTrack.fill(*track, vertex.position());
        }
        hTauPFCandLeadHadr.fill(tau, *pfCandLeadingHadr);
      }

      hTauGen.fill(*genTau);
      hTauGenVis.fill(tauDaughters.visible);
      hNuGen.fill(*genTauNu);
      hTauNuGen.fill(*genTau, *genTauNu);
      hTauGenNprongs->Fill(tauDaughters.nprongs, eventWeight_.getWeight());
      if(tauDaughters.leadingChargedPion) {
        hTauGenLeadingChargedPi.fill(*tauDaughters.leadingChargedPion);
        hTauGenTauGenLeadingChargedPi.fill(*genTau, *tauDaughters.leadingChargedPion);
        hTauGenVisTauGenLeadingChargedPi.fill(tauDaughters.visible, *tauDaughters.leadingChargedPion);
      }

      hTauGenMass->Fill(genTau->p4().M(), eventWeight_.getWeight());
      hTauGenDecayMass->Fill(tauDecayMass, eventWeight_.getWeight());
    }

    const HPlus::EventWeight& eventWeight_;
    const HPlus::PFTauIsolationCalculator& tauIsolationCalculator_;

    double metCut_;
    std::vector<HistoMet2 *> hMets;
    HistoMet2 hMetNu;

    Histo hMuon;
    HistoTrack hMuonTrack;
    /*
    TH1 *hMuonTrkIso;
    TH1 *hMuonTrkRelIso;
    TH1 *hMuonCaloIso;
    TH1 *hMuonCaloRelIso;
    TH1 *hMuonIso;
    */
    TH1 *hMuonRelIso;

    Histo hTau;
    Histo hTauLead;
    Histo hTauLeadChargedHadr;
    TH1 *hTauLeadExists;
    TH1 *hTauLeadTrackExists;
    TH1 *hTauLeadChargedHadrExists;
    TH1 *hTauR;

    HistoIso hTauIsoShrinkingCone;
    HistoIso hTauIsoShrinkingCone05;
    HistoIso hTauIsoHpsLoose;
    HistoIso hTauIsoHpsMedium;
    HistoIso hTauIsoHpsTight;

    HistoIso2 hMuonRelIsoTauIsoShrinkingCone;
    HistoIso2 hMuonRelIsoTauIsoHpsMedium;
    HistoIso2 hMuonRelIsoTauIsoHpsTight;

    /*
    TH1 *hTauIsoChargedHadrPtSum;
    TH1 *hTauIsoChargedHadrPt05Sum;
    TH1 *hTauIsoChargedHadrPt10Sum;
    TH1 *hTauIsoChargedHadrPtSumRel;
    TH1 *hTauIsoChargedHadrPtMax;
    TH1 *hTauIsoChargedHadrPtMaxRel;
    TH2 *hMuonTrkTauPtSumIso;
    TH2 *hMuonTrkTauPtSumIsoRel;
    TH2 *hMuonTauPtSumIso;
    TH2 *hMuonTauPtSumIsoRel;
    */

    TH1 *hPFCandNumber;
    Histo hPFCandLead;
    TH1 *hPFCandLeadParticleType;
    TH1 *hPFCandLeadCharge;
    Histo2 hTauPFCandLead;

    Histo hPFCandLeadHadr;
    HistoTrack hPFCandLeadHadrTrack;
    TH1 *hPFCandLeadHadrCharge;
    Histo2 hTauPFCandLeadHadr;

    Histo hTauGen;
    Histo hTauGenVis;
    Histo hNuGen;
    Histo2 hTauNuGen;
    TH1 *hTauGenNprongs;
    Histo hTauGenLeadingChargedPi;
    Histo2 hTauGenTauGenLeadingChargedPi;
    Histo2 hTauGenVisTauGenLeadingChargedPi;

    TH1 *hTauGenMass;
    TH1 *hTauGenDecayMass;

    Histo2 hMuonTau;
    Histo2 hMuonTauLdg;
  };

  HistoAll histos;
  HistoAll histosMatched;

};

HPlusTauEmbeddingAnalyzer::HPlusTauEmbeddingAnalyzer(const edm::ParameterSet& iConfig):
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  tauSrc_(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  pfCandSrc_(iConfig.getUntrackedParameter<edm::InputTag>("pfCandSrc")),
  vertexSrc_(iConfig.getUntrackedParameter<edm::InputTag>("vertexSrc")),
  genParticleOriginalSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleOriginalSrc")),
  genParticleEmbeddedSrc_(iConfig.getUntrackedParameter<edm::InputTag>("genParticleEmbeddedSrc")),
  muonTauCone_(iConfig.getUntrackedParameter<double>("muonTauMatchingCone")),
  eventWeight_(iConfig),
  tauIsolationCalculator_(iConfig.getUntrackedParameter<edm::ParameterSet>("tauIsolationCalculator")),
  histos(iConfig.getUntrackedParameter<double>("metCut"), eventWeight_, tauIsolationCalculator_),
  histosMatched(iConfig.getUntrackedParameter<double>("metCut"), eventWeight_, tauIsolationCalculator_)
{
  edm::Service<TFileService> fs;

  const edm::ParameterSet& pset = iConfig.getUntrackedParameter<edm::ParameterSet>("mets");

  histos.init(pset, *fs);
  TFileDirectory mdir = fs->mkdir("matched");
  histosMatched.init(pset, mdir);
}
HPlusTauEmbeddingAnalyzer::~HPlusTauEmbeddingAnalyzer() {}

void HPlusTauEmbeddingAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Muon> > hmuon;
  iEvent.getByLabel(muonSrc_, hmuon);
  if(hmuon->size() != 1)
    throw cms::Exception("LogicError") << "Expected muon size 1, got " << hmuon->size() << " from collection " << muonSrc_.encode() << std::endl;
  edm::Ptr<reco::Muon> muon = hmuon->ptrAt(0);

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(tauSrc_, htaus);
  if(htaus->empty())
    return;

  edm::Handle<edm::View<reco::PFCandidate> > hpfCands;
  iEvent.getByLabel(pfCandSrc_, hpfCands);

  edm::Handle<edm::View<reco::Vertex> > hvertices;
  iEvent.getByLabel(vertexSrc_, hvertices);
  edm::Ptr<reco::Vertex> pv = hvertices->ptrAt(0);

  edm::Ptr<pat::Tau> tau;
  double minDR = 99999;
  for(size_t i=0; i<htaus->size(); ++i) {
    double dR = reco::deltaR(*muon, htaus->at(i));
    if(dR < minDR) {
      minDR = dR;
      tau = htaus->ptrAt(i);
    }
  }

  edm::Ptr<reco::PFCandidate> pfCandLeading;
  edm::Ptr<reco::PFCandidate> pfCandLeadingHadr;
  double maxPt = 0;
  double maxPtHadr = 0;
  for(size_t i=0; i<hpfCands->size(); ++i) {
    if(maxPt < hpfCands->at(i).pt()) {
      maxPt = hpfCands->at(i).pt();
      pfCandLeading = hpfCands->ptrAt(i);
    }
    if(hpfCands->at(i).particleId() == reco::PFCandidate::h and maxPtHadr < hpfCands->at(i).pt()) {
      maxPtHadr = hpfCands->at(i).pt();
      pfCandLeadingHadr = hpfCands->ptrAt(i);
    }
  }

  eventWeight_.updatePrescale(iEvent); // set prescale
  tauIsolationCalculator_.beginEvent(iEvent);

  /*
  std::cout << "Muon pt " << muon->pt()
            << " eta " << muon->eta()
            << " phi " << muon->phi()
    //<< " dB " << muon->dB()
            << " dxy(PV) " << muon->globalTrack()->dxy(pv->position())
            << " dz(PV) " << muon->globalTrack()->dz(pv->position())
            << std::endl;
  std::cout << "Tau pt " << tau->pt()
            << " eta " << tau->eta()
            << " phi " << tau->phi()
            << " DR(mu, tau) " << minDR 
            << std::endl;
  if(pfCandLeading.get()) {
    std::cout << "PFCand pt " << pfCandLeading->pt() 
              << " eta " << pfCandLeading->eta() 
              << " phi " << pfCandLeading->phi() 
              << std::endl;
  }
  if(pfCandLeadingHadr.get()) {
    reco::TrackRef track = pfCandLeadingHadr->trackRef();
    std::cout << "PFCandHadr pt " << pfCandLeadingHadr->pt() 
              << " eta " << pfCandLeadingHadr->eta() 
              << " phi " << pfCandLeadingHadr->phi()
      //<< " dxy " << track->dxy(track->referencePoint())
      //<< " dz " << track->dz(track->referencePoint())
              << " dxy " << track->dxy(pv->position())
              << " dz " << track->dz(pv->position())

              << std::endl;
  }
  std::cout << std::endl;
  */

  GenParticlePair nuW(0, 0);
  edm::Handle<edm::View<reco::GenParticle> > hgenOriginal;
  iEvent.getByLabel(genParticleOriginalSrc_, hgenOriginal);
  if(hgenOriginal.isValid())
    nuW = findMuNuFromW(*muon, hgenOriginal->begin(), hgenOriginal->end());

  GenParticlePair nuTau(0, 0);
  GenTauDaughters tauDaughters;
  edm::Handle<edm::View<reco::GenParticle> > hgenEmbedded;
  iEvent.getByLabel(genParticleEmbeddedSrc_, hgenEmbedded);
  if(hgenEmbedded.isValid()) {
    nuTau = findTauNu(hgenEmbedded->begin(), hgenEmbedded->end());
    tauDaughters = genTauDaughters(*nuTau.second);
  }

  histos.fillMets(*muon, *tau, nuW.first, nuTau.first, iEvent);
  histos.fill(*muon, *tau,
              nuW.second, nuW.first,
              nuTau.second, nuTau.first,
              tauDaughters,
              *pv,
              hpfCands->size(), pfCandLeading, pfCandLeadingHadr);

  if(minDR < muonTauCone_) {
    histosMatched.fillMets(*muon, *tau, nuW.first, nuTau.first, iEvent);
    histosMatched.fill(*muon, *tau,
                       nuW.second, nuW.first,
                       nuTau.second, nuTau.first,
                       tauDaughters,
                       *pv,
                       hpfCands->size(), pfCandLeading, pfCandLeadingHadr);
  }
}

template <typename I>
HPlusTauEmbeddingAnalyzer::GenParticlePair HPlusTauEmbeddingAnalyzer::findTauNu(I begin, I end) const {
  for(I iGen = begin; iGen != end; ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
      const reco::GenParticle *particle = &(*(iGen));
      bool isFromTau = false;
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(particle->mother())) {
        particle = mother;
        if(std::abs(particle->pdgId()) == 15) {
          isFromTau = true;
          break;
        }
      }
      if(isFromTau)
        return std::make_pair(&(*iGen), particle); // neutrino, tau
    }
  }
  return GenParticlePair(0, 0);
}

template <typename I>
HPlusTauEmbeddingAnalyzer::GenParticlePair HPlusTauEmbeddingAnalyzer::findMuNuFromW(const reco::Candidate& recoMu, I begin, I end) const {

  GenParticlePair nearest(0, 0);
  double maxDR = 9999;
  for(I iGen = begin; iGen != end; ++iGen) {
    int pdgId = std::abs(iGen->pdgId());
    if(pdgId == 12 || pdgId == 14 || pdgId == 16) {
      const reco::GenParticle *particle = &(*(iGen));
      bool isFromMu = false;
      while(const reco::GenParticle *mother = dynamic_cast<const reco::GenParticle *>(particle->mother())) {
        particle = mother;
        if(std::abs(particle->pdgId()) == 24) {
          for(reco::GenParticle::const_iterator iDaughter = particle->begin(); iDaughter != particle->end(); ++iDaughter) {
            if(std::abs(iDaughter->pdgId()) == 13) {
              isFromMu = true;
              break;
            }
          }
          if(isFromMu)
            break;
        }
      }
      double deltaR = reco::deltaR(recoMu, *particle);
      if(isFromMu &&  deltaR < maxDR) {
        nearest = std::make_pair(&(*iGen), particle); // neutrino, mu
        maxDR = deltaR;
      }
    }
  }
  return nearest;
}

HPlusTauEmbeddingAnalyzer::GenTauDaughters HPlusTauEmbeddingAnalyzer::genTauDaughters(const reco::GenParticle& tau) const {
  GenTauDaughters ret;

  double maxPt = 0.0;
  for(reco::GenParticle::const_iterator iDaughter = tau.begin(); iDaughter != tau.end(); ++iDaughter) {
    if(iDaughter->numberOfDaughters() > 0) {
      GenTauDaughters res = genTauDaughters(dynamic_cast<const reco::GenParticle&>(*iDaughter));
      ret.nprongs += res.nprongs;
      ret.visible += res.visible;
      if(res.leadingChargedPion && maxPt < res.leadingChargedPion->pt()) {
        maxPt = res.leadingChargedPion->pt();
        ret.leadingChargedPion = res.leadingChargedPion;
      }
    }
    else {
      unsigned pdgId = std::abs(iDaughter->pdgId());
      
      if(pdgId != 12 && pdgId != 14 && pdgId != 16) {
        ret.visible += iDaughter->p4();
      }

      if(pdgId == 211) {
        ret.nprongs += 1;
        if(maxPt < iDaughter->pt()) {
          maxPt = iDaughter->pt();
          ret.leadingChargedPion = dynamic_cast<const reco::GenParticle *>(&(*iDaughter));
        }
      }
    }
  }
  return ret; 
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEmbeddingAnalyzer);
