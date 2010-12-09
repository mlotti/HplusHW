#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTNJetsEmulation.h"
#include "Math/VectorUtil.h"


HLTNJetsEmulation::HLTNJetsEmulation(const edm::ParameterSet& iConfig) :
  jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc"))
{}

HLTNJetsEmulation::~HLTNJetsEmulation(){}

void HLTNJetsEmulation::setParameters(int nJets,double ptCut){
        jetPtCut = ptCut;
        nJetsMin = nJets;
}

bool HLTNJetsEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup, std::vector<LorentzVector> l1jets){

	int njets = 0;

        edm::Handle<edm::View<reco::CaloJet> > hjets;
        iEvent.getByLabel(jetSrc, hjets);
        edm::PtrVector<reco::CaloJet> jets = hjets->ptrVector();

        for(edm::PtrVector<reco::CaloJet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
                edm::Ptr<reco::CaloJet> iJet = *iter;

		for(std::vector<LorentzVector>::const_iterator iL1 = l1jets.begin();
		                                               iL1!= l1jets.end(); ++iL1){
			double DR = ROOT::Math::VectorUtil::DeltaR(*iL1,iJet->p4());
			if(DR > 0.4) continue;

			if(iJet->pt() < jetPtCut) continue;
			njets++;
		}
	}

	return njets >= nJetsMin;
}
