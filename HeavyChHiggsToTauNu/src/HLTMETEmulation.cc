#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HLTMETEmulation.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

HLTMETEmulation::HLTMETEmulation(const edm::ParameterSet& iConfig) :
    metSrc(iConfig.getParameter<edm::InputTag>("metSrc"))
{}

HLTMETEmulation::~HLTMETEmulation(){}

void HLTMETEmulation::setParameters(double theCut){
	metCut = theCut;
}

bool HLTMETEmulation::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup){
        edm::Handle<edm::View<reco::MET> > hmet;
        iEvent.getByLabel(metSrc, hmet);

        edm::Ptr<reco::MET> met = hmet->ptrAt(0);

        return met->et() > metCut;
}

