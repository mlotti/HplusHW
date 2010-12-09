#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTTauEmulation.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "Math/VectorUtil.h"


HLTTauEmulation::HLTTauEmulation(const edm::ParameterSet& iConfig,double tauPt,double lTrackPt) :
  tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  tauPtCut(iConfig.getParameter<double>("TauPtCut")),
  tauLTrkCut(iConfig.getParameter<double>("TauLeadTrkPtCut"))
{
	tauPtCut    = tauPt;
	tauLTrkCut = lTrackPt;
}

HLTTauEmulation::~HLTTauEmulation(){}

bool HLTTauEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup, LorentzVector cand){

	bool passed = false;

        edm::Handle<edm::View<reco::CaloTau> > htaus;
        iEvent.getByLabel(tauSrc, htaus);
        edm::PtrVector<reco::CaloTau> taus = htaus->ptrVector();

        for(edm::PtrVector<reco::CaloTau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
                edm::Ptr<reco::CaloTau> iTau = *iter;

                double DR = ROOT::Math::VectorUtil::DeltaR(cand,iTau->p4());

                if(DR > 0.4) continue;

                if(!(iTau->pt() > tauPtCut)) continue;
		if(iTau->isolationECALhitsEtSum() > 5) continue;
//                counter_l2++;

                reco::TrackRef leadTrk = iTau->leadTrack();
                if(leadTrk.isNull() || !(leadTrk->pt() > tauLTrkCut)) continue;
//                counter_l25++;

                if(iTau->isolationTracks().size()) continue;
//                counter_l3++;

                passed = true;
        }

	return passed;
}
