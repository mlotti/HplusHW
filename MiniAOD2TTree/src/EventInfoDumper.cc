#include "HiggsAnalysis/MiniAOD2TTree/interface/EventInfoDumper.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

EventInfoDumper::EventInfoDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
: puSummaryToken(iConsumesCollector.consumes<std::vector<PileupSummaryInfo>>(pset.getParameter<edm::InputTag>("PileupSummaryInfoSrc"))),
  lheToken(iConsumesCollector.consumes<LHEEventProduct>(pset.getUntrackedParameter<edm::InputTag>("LHESrc", edm::InputTag("")))),
  vertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(pset.getParameter<edm::InputTag>("OfflinePrimaryVertexSrc"))) {

}

EventInfoDumper::~EventInfoDumper(){}

void EventInfoDumper::book(TTree* tree){
    tree->Branch("event",&event);
    tree->Branch("run",&run);     
    tree->Branch("lumi",&lumi);
    tree->Branch("nPUvertices",&nPU);
    tree->Branch("NUP",&NUP);
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
    iEvent.getByToken(puSummaryToken, hpileup);
    if(hpileup.isValid()) { // protection for data
        for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV) {
            if(iPV->getBunchCrossing() == 0) {
                nPU = iPV->getTrueNumInteractions();
                break;
            }
        }
    }

    // number of jets for combining W+Jets/Z+jets inclusive with exclusive
    edm::Handle<LHEEventProduct> lheHandle;
    iEvent.getByToken(lheToken, lheHandle);
    if (lheHandle.isValid()) {
        // Store NUP = number of partons
        NUP = lheHandle->hepeup().NUP;
    }

    // PV
    nGoodOfflinePV = 0;
    edm::Handle<edm::View<reco::Vertex> > hoffvertex;
    if(iEvent.getByToken(vertexToken, hoffvertex)){
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
