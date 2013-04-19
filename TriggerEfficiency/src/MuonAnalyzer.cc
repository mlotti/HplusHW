#include "HiggsAnalysis/TriggerEfficiency/interface/MuonAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <TTree.h>
#include <iostream>

// Default constructor
MuonAnalyzer::MuonAnalyzer(){}


MuonAnalyzer::~MuonAnalyzer(){}

void MuonAnalyzer::Setup(const edm::ParameterSet& iConfig,TTree *trigtree)
{
	MuonSource = iConfig.getParameter<edm::InputTag>("MuonSource");
        muTauPairSource = iConfig.getParameter<edm::InputTag>("MuonTauPairSource");

  	// Setup branches
  	trigtree->Branch("MuonPt", &muonPt);
	trigtree->Branch("MuonEta",&muonEta);
	trigtree->Branch("MuonPhi",&muonPhi);
        trigtree->Branch("MuonIso03SumPt", &muonIso03SumPt);
        trigtree->Branch("MuonIso03EmEt", &muonIso03EmEt);
        trigtree->Branch("MuonIso03HadEt", &muonIso03HadEt);
        trigtree->Branch("MuonPFIsoChargedPt", &muonPFIsoCharged);
        trigtree->Branch("MuonPFIsoNeutralEt", &muonPFIsoNeutral);
        trigtree->Branch("MuonPFIsoGammaEt", &muonPFIsoGamma);
	trigtree->Branch("NMuons",&nMuons);

        trigtree->Branch("MuonTauInvMass", &muTauInvMass);
}

void MuonAnalyzer::fill(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau) {
  fill(iEvent, iSetup, tau.p4());
}

void MuonAnalyzer::fill(const edm::Event& iEvent, const edm::EventSetup& iSetup, const LorentzVector& tau) {

	muonPt  = -999;
	muonEta = -999;
	muonPhi = -999;
        muonIso03SumPt = -999;
        muonIso03EmEt = -999;
        muonIso03HadEt = -999;
        muonPFIsoCharged = -999;
        muonPFIsoNeutral = -999;
        muonPFIsoGamma = -999;
	nMuons  = 0;

        muTauInvMass = 0;

//
	edm::Handle<edm::View<pat::Muon> > muons;
        iEvent.getByLabel(MuonSource, muons);

        nMuons = muons->size();

        edm::Handle<edm::View<reco::CompositeCandidate> > hpairs;
        iEvent.getByLabel(muTauPairSource, hpairs);
        if(hpairs.isValid() && !hpairs->empty()) {

          const reco::CompositeCandidate *pair = 0;
          const pat::Muon *muon = 0;
          double minPt = 0;
          for(size_t i=0; i<hpairs->size(); ++i) {
            const reco::CompositeCandidate& muTau = hpairs->at(i);
            if(muTau.numberOfDaughters() != 2)
              throw cms::Exception("LogicError") << "MuonAnalyzer expected reco::CompositeCandidates with 2 daughters, got " << muTau.numberOfDaughters() << " from " << muTauPairSource.encode() << std::endl;

            if(reco::deltaR(*(muTau.daughter(1)), tau) < 0.01 &&
               muTau.daughter(0)->pt() > minPt) {
              pair = &muTau;
              muon = dynamic_cast<const pat::Muon *>(muTau.daughter(0));
              if(!muon)
                throw cms::Exception("LogicError") << "MuonAnalyzer expected reco::CompositeCandidates with pat::Muon as the first daughter!" << std::endl;
              minPt = muon->pt();
            }
          }

          // Found mu-tau pair matching to the given tau
          if(muon) {
            if(!pair)
              throw cms::Exception("LogicError") << "MuonAnalyzer found a muon, but not the mu-tau pair. This needs some debugging." << std::endl;

            muonPt  = muon->pt();
            muonEta = muon->eta();
            muonPhi = muon->phi();
            muonIso03SumPt = muon->isolationR03().sumPt;
            muonIso03EmEt = muon->isolationR03().emEt;
            muonIso03HadEt = muon->isolationR03().hadEt;

            muonPFIsoCharged = muon->userIsolation(pat::PfChargedHadronIso);
            muonPFIsoNeutral = muon->userIsolation(pat::PfNeutralHadronIso);
            muonPFIsoGamma = muon->userIsolation(pat::PfGammaIso);

            muTauInvMass = pair->mass();
          }
        }
}

