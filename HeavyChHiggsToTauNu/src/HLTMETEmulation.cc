#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTMETEmulation.h"

HLTMETEmulation::HLTMETEmulation(const edm::ParameterSet& iConfig,double theCut) :
    metSrc(iConfig.getParameter<edm::InputTag>("metSrc"))
{
	metCut = theCut;
}

HLTMETEmulation::~HLTMETEmulation(){}

bool HLTMETEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup){
        edm::Handle<edm::View<reco::MET> > hmet;
        iEvent.getByLabel(metSrc, hmet);

        edm::Ptr<reco::MET> met = hmet->ptrAt(0);

        return met->et() > metCut;
}

