#include "HiggsAnalysis/MiniAOD2TTree/interface/EventInfoDumper.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

EventInfoDumper::EventInfoDumper(edm::ParameterSet& pset){
    if (pset.exists("PileupSummaryInfoSrc")) pileupSummaryInfoSrc = pset.getParameter<edm::InputTag>("PileupSummaryInfoSrc");
//    lheSrc = pset.getParameter<edm::InputTag>("LHESrc");
    if (pset.exists("OfflinePrimaryVertexSrc")) offlinePrimaryVertexSrc = pset.getParameter<edm::InputTag>("OfflinePrimaryVertexSrc");
}
EventInfoDumper::~EventInfoDumper(){}

void EventInfoDumper::book(TTree* tree){
    tree->Branch("event",&event);
    tree->Branch("run",&run);     
    tree->Branch("lumi",&lumi);
    tree->Branch("nPU",&nPU);
//    tree->Branch("NUP",&NUP);
    tree->Branch("nGoodOfflinePV",&nGoodOfflinePV);
}

bool EventInfoDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){

    event = iEvent.id().event();
    run   = iEvent.run();
    lumi  = iEvent.luminosityBlock();

    // Amount of PU
    edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
    iEvent.getByLabel(pileupSummaryInfoSrc, hpileup);
    if(hpileup.isValid()) { // protection for data
        for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV) {
            if(iPV->getBunchCrossing() == 0) {
                nPU = iPV->getTrueNumInteractions();
                break;
            }
        }
    }
/*
    // number of jets for combining WJets inclusive with exclusive
    edm::Handle<LHEEventProduct> hlhe;
    if(iEvent.getByLabel(lheSrc, hlhe)){
        NUP = hlhe->hepeup().NUP;
    }
*/
    // PV
    nGoodOfflinePV = 0;
    edm::Handle<edm::View<reco::Vertex> > hoffvertex;
    if(iEvent.getByLabel(offlinePrimaryVertexSrc, hoffvertex)){
        nGoodOfflinePV = hoffvertex->size();  
    }

    return filter();
}

bool EventInfoDumper::filter(){
    return true;
}

void EventInfoDumper::reset(){
}
