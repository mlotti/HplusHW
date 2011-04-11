#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

#include <iostream>
using namespace std;

class PFTauChHadronCandidateValidation : public edm::EDAnalyzer {
    public:
	PFTauChHadronCandidateValidation(const edm::ParameterSet&);
	~PFTauChHadronCandidateValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag src;

  	DQMStore *dbe;

        MonitorElement *nEvt;
  	MonitorElement *nTracks, *nCands;
	MonitorElement *diffNtracksNcands;
	MonitorElement *nPFTaus;
	MonitorElement *signalConePtSum;
	MonitorElement *LtrDR,*LtrDpt;
};

PFTauChHadronCandidateValidation::PFTauChHadronCandidateValidation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

PFTauChHadronCandidateValidation::~PFTauChHadronCandidateValidation() {}

void PFTauChHadronCandidateValidation::beginJob(){}

void PFTauChHadronCandidateValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/PFTauChHadronCandidate");

    // Number of analyzed events
    nEvt = dbe->book1D("nEvt "+src.label(), "n analyzed Events", 1, 0., 1.);

    // Number of tracks
    int N = 10;
    nTracks	= dbe->book1D("nTracks "+src.label(),"ntracks", N ,0,N);
    nCands	= dbe->book1D("nCands "+src.label(),"nChHadronCands", N ,0,N);
    diffNtracksNcands = dbe->book1D("diffNtracksNcands "+src.label(),"diffTrkCands", N ,0,N);

    // Number of pftaus
    nPFTaus	= dbe->book1D("nPFTaus "+src.label(),"ltr lost", 2 ,0,2);

    // PFCandidate pt sum / PFTau pt
    signalConePtSum = dbe->book1D("signalConePtSum "+src.label(),"signal ptsum", 100 ,0,2);

    // Leading track vs leading chargedHadronCandidate
    LtrDR	= dbe->book1D("ltrack DR "+src.label(),"DR(ltrack,lcand)", 100 ,0,0.2);
    LtrDpt	= dbe->book1D("ltrack Dpt "+src.label(),"ltrack - lcand pt", 100 ,0,50);
  }
}

void PFTauChHadronCandidateValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void PFTauChHadronCandidateValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
    nEvt->Fill(0.5);

    edm::Handle<reco::PFTauCollection> PFTaus;
    if(iEvent.getByLabel(src, PFTaus)) {
	for(size_t i = 0; i < PFTaus->size(); ++i){
	  double pftaupt = PFTaus->at(i).pt();
	  
	  int nSignalTrk = PFTaus->at(i).signalTracks().size();
	  int nSignalCnd = PFTaus->at(i).signalPFChargedHadrCands().size();
	  int nIsolTrk   = PFTaus->at(i).isolationTracks().size();
	  int nIsolCnd   = PFTaus->at(i).isolationPFChargedHadrCands().size();
	  if(pftaupt > 10 && nSignalTrk > 0){

	    nPFTaus->Fill(0.5);

	    nTracks->Fill(nSignalTrk + nIsolTrk);
	    nCands->Fill(nSignalCnd + nIsolCnd);
	    diffNtracksNcands->Fill((nSignalTrk + nIsolTrk) - (nSignalCnd + nIsolCnd));

	    TLorentzVector p4sum(0,0,0,0);
	    const reco::PFCandidateRefVector signalCands = PFTaus->at(i).signalPFCands();
	    for(size_t iC = 0; iC < signalCands.size(); ++iC){
		p4sum += TLorentzVector(signalCands[iC]->px(),
                                        signalCands[iC]->py(),
		                        signalCands[iC]->pz(),
		                        signalCands[iC]->energy());
	    }
	    signalConePtSum->Fill(p4sum.Pt()/pftaupt);

	    TLorentzVector lCand = TLorentzVector(0,0,0,0);
	    if(PFTaus->at(i).leadPFChargedHadrCand().isNonnull()){
	    	lCand = TLorentzVector(PFTaus->at(i).leadPFChargedHadrCand()->px(),
	                                          PFTaus->at(i).leadPFChargedHadrCand()->py(),
                                                  PFTaus->at(i).leadPFChargedHadrCand()->pz(),
                                                  PFTaus->at(i).leadPFChargedHadrCand()->energy());
	    }
	    TLorentzVector lTrk = TLorentzVector(PFTaus->at(i).leadTrack()->px(),
                                                 PFTaus->at(i).leadTrack()->py(),
                                                 PFTaus->at(i).leadTrack()->pz(),
                                                 PFTaus->at(i).leadTrack()->p());
	    if(lCand.Pt() > 0){
	        double DR = ROOT::Math::VectorUtil::DeltaR(lCand,lTrk);
		LtrDR->Fill(DR);
	    }
	    double ptDiff = lTrk.Pt() - lCand.Pt();
	    LtrDpt->Fill(ptDiff);

	  }
	}
    }
}

void PFTauChHadronCandidateValidation::endJob(){}

DEFINE_FWK_MODULE(PFTauChHadronCandidateValidation);
