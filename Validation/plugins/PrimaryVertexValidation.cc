#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include <iostream>
using namespace std;

class PrimaryVertexValidation : public edm::EDAnalyzer {
    public:
	PrimaryVertexValidation(const edm::ParameterSet&);
	~PrimaryVertexValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag beamSpotSrc;
	edm::InputTag primaryVertexSrc;

  	DQMStore *dbe;

        MonitorElement *nEvt;
  	MonitorElement *PV_X, *PV_Y, *PV_XY;
	MonitorElement *BS_X, *BS_Y, *BS_XY;
	MonitorElement *BS_WidthX, *BS_WidthY;
};

PrimaryVertexValidation::PrimaryVertexValidation(const edm::ParameterSet& iConfig):
    beamSpotSrc(iConfig.getParameter<edm::InputTag>("BeamSpot")),
    primaryVertexSrc(iConfig.getParameter<edm::InputTag>("PrimaryVertex"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

PrimaryVertexValidation::~PrimaryVertexValidation() {}

void PrimaryVertexValidation::beginJob(){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/PrimaryVertex");

    // Number of analyzed events
    nEvt    = dbe->book1D("nEvt ", "n analyzed Events", 1, 0., 1.);

    double range = 100;
    //Position
    PV_X	= dbe->book1D("PrimaryVertex X "+primaryVertexSrc.label(),"PrimaryVertex X", 100 ,-range,range);
    PV_Y        = dbe->book1D("PrimaryVertex Y "+primaryVertexSrc.label(),"PrimaryVertex Y", 100 ,-range,range);
    PV_XY	= dbe->book2D("PrimaryVertex X Y "+primaryVertexSrc.label(),"PrimaryVertex X Y", 100 ,-range,range, 100 ,-range,range);

    BS_X        = dbe->book1D("BeamSpot X "+beamSpotSrc.label(),"BeamSpot X", 100 ,-range,range);
    BS_Y        = dbe->book1D("BeamSpot Y "+beamSpotSrc.label(),"BeamSpot Y", 100 ,-range,range);
    BS_XY       = dbe->book2D("BeamSpot X Y "+beamSpotSrc.label(),"BeamSpot X Y", 100 ,-range,range, 100 ,-range,range);

    BS_WidthX   = dbe->book1D("BeamSpot X width "+beamSpotSrc.label(),"BeamSpot X Width", 100 ,-range,range);
    BS_WidthY   = dbe->book1D("BeamSpot Y width "+beamSpotSrc.label(),"BeamSpot Y Width", 100 ,-range,range);
  }
}

void PrimaryVertexValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}
void PrimaryVertexValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void PrimaryVertexValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){

    nEvt->Fill(0.5);

    edm::Handle<reco::BeamSpot> beamSpot;
    iEvent.getByLabel(beamSpotSrc,beamSpot);

    if(beamSpot.isValid()){
	double bs_x = beamSpot->position().x();
	double bs_y = beamSpot->position().y();
	BS_X->Fill(bs_x);
	BS_Y->Fill(bs_y);
	BS_XY->Fill(bs_x,bs_y);

	BS_WidthX->Fill(beamSpot->BeamWidthX());
	BS_WidthY->Fill(beamSpot->BeamWidthY());
    }

    edm::Handle<reco::VertexCollection> primaryVertices;
    iEvent.getByLabel(primaryVertexSrc,primaryVertices);

    const reco::VertexCollection vertexCollection = *(primaryVertices.product());
    if(vertexCollection.size() > 0){
	double pv_x = vertexCollection.begin()->x();
	double pv_y = vertexCollection.begin()->y();
	PV_X->Fill(pv_x);
	PV_Y->Fill(pv_y);
	PV_XY->Fill(pv_x,pv_y);
    }
}

void PrimaryVertexValidation::endJob(){}

DEFINE_FWK_MODULE(PrimaryVertexValidation);
