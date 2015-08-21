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
    tree->Branch("nPUvertices",&nPU);
//    tree->Branch("NUP",&NUP);
    tree->Branch("nGoodOfflineVertices",&nGoodOfflinePV);
    tree->Branch("pvZ",&pvZ);
    tree->Branch("pvPtSumRatioToNext",&ptSumRatio);
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
        pvZ = hoffvertex->at(0).z();
        ptSumRatio = -1.0;
        if (nGoodOfflinePV > 1) {
          double ptSum0 = 0.0;
          for (std::vector<reco::TrackBaseRef>::const_iterator iter = hoffvertex->at(0).tracks_begin(); iter != hoffvertex->at(0).tracks_end(); iter++) {
            ptSum0 += hoffvertex->at(0).trackWeight(*iter) * (*iter)->pt()*(*iter)->pt();
          }
          double ptSum1 = 0.0;
          for (std::vector<reco::TrackBaseRef>::const_iterator iter = hoffvertex->at(1).tracks_begin(); iter != hoffvertex->at(1).tracks_end(); iter++) {
            ptSum1 += hoffvertex->at(1).trackWeight(*iter) * (*iter)->pt()*(*iter)->pt();
          }
          if (ptSum0 > 0.0) {
            ptSumRatio = ptSum1 / ptSum0;
          }
        }
    }

    return filter();
}

bool EventInfoDumper::filter(){
    return true;
}

void EventInfoDumper::reset(){
}
