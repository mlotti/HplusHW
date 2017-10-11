#include "HiggsAnalysis/MiniAOD2TTree/interface/SoftBTagDumper.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "RecoVertex/VertexTools/interface/VertexDistance.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"


SoftBTagDumper::SoftBTagDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset)
  :  primaryVertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(pset.getParameter<edm::InputTag>("PrimaryVertexSrc"))),
     secondaryVertexToken(iConsumesCollector.consumes<edm::View<reco::VertexCompositePtrCandidate>>(pset.getParameter<edm::InputTag>("SecondaryVertexSrc")))
     //  topPtToken(iConsumesCollector.consumes<double>(pset.getParameter<edm::InputTag>("TopPtProducer")))
{
  
  svPt         = new std::vector<float>;
  svEta        = new std::vector<float>;
  svPhi        = new std::vector<float>;
  svMass       = new std::vector<float>;
  svNTks       = new std::vector<int>;
  svChi2       = new std::vector<float>;
  svNdof       = new std::vector<float>;
  svDxy        = new std::vector<float>;
  svDxyErr     = new std::vector<float>;
  svD3d        = new std::vector<float>;
  svD3dErr     = new std::vector<float>;
  costhetasvpv = new std::vector<float>;

  
}

SoftBTagDumper::~SoftBTagDumper(){}

void SoftBTagDumper::book(TTree* tree){
  
  // Secondary Vertex Collection
  tree->Branch("SV_pt"        , &svPt);
  tree->Branch("SV_eta"       , &svEta );
  tree->Branch("SV_phi"       , &svPhi );
  tree->Branch("SV_mass"      , &svMass );
  tree->Branch("SV_nTks"      , &svNTks );
  tree->Branch("SV_chi2"      , &svChi2 );
  tree->Branch("SV_ndof"      , &svNdof );
  tree->Branch("SV_dxy"       , &svDxy );
  tree->Branch("SV_dxyErr"    , &svDxyErr );
  tree->Branch("SV_d3d"       , &svD3d );
  tree->Branch("SV_d3dErr"    , &svD3dErr );
  tree->Branch("SV_dotPv", &costhetasvpv );
  
  return;
}

bool SoftBTagDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){

  // Initialise Variables
  nGoodOfflinePV = -1;
  nGoodOfflineSV = -1;

  svPt->clear();
  svEta->clear();
  svPhi->clear();
  svMass->clear();
  svNTks->clear();
  svChi2->clear();
  svNdof->clear();
  svDxy->clear();
  svDxyErr->clear();
  svD3d->clear();
  svD3dErr->clear();
  costhetasvpv->clear();

  // Get the Primary Vertex (PV)
  edm::Handle<edm::View<reco::Vertex> > h_primaryVertex;
  if(iEvent.getByToken(primaryVertexToken, h_primaryVertex)) nGoodOfflinePV = h_primaryVertex->size();

  // Sanity check
  //  std::cout << "nGoodOfflinePV = " << nGoodOfflinePV << std::endl;
  if (nGoodOfflinePV < 0) return false;

  // Get the Secondary Vertex (SV)
  reco::Vertex PV = h_primaryVertex->at(0); // the PV
  edm::Handle<edm::View<reco::VertexCompositePtrCandidate> > h_secondaryVertex;
  if(iEvent.getByToken(secondaryVertexToken, h_secondaryVertex)) nGoodOfflineSV = h_secondaryVertex->size();

  // Sanity check
  //std::cout << "nGoodOfflineSV = " << nGoodOfflineSV << std::endl;
  if (nGoodOfflineSV < 0) return false;

  // For-loop: All Secondary Verticies
  for(size_t isv = 0; isv < h_secondaryVertex->size(); isv++ )
    {
      const reco::VertexCompositePtrCandidate &sv = (*h_secondaryVertex)[isv];
      svPt->push_back(sv.pt());
      svEta->push_back(sv.eta());
      svPhi->push_back(sv.phi());
      svMass->push_back(sv.mass());
      svNTks->push_back(sv.numberOfDaughters());
      svChi2->push_back(sv.vertexChi2());
      svNdof->push_back(sv.vertexNdof());
      svDxy->push_back(vertexDxy(sv,PV).value());
      svDxyErr->push_back(vertexDxy(sv,PV).error());
      svD3d->push_back(vertexD3d(sv,PV).value());
      svD3dErr->push_back(vertexD3d(sv,PV).error());
      costhetasvpv->push_back(vertexDdotP(sv, PV));

    }//eof: loop on sec vertex
    
  return filter();
}

bool SoftBTagDumper::filter(){
  return true;
}

void SoftBTagDumper::reset(){
  //  This method of clearing the vectors do not work. So for now, it is done at the start of  fill()
  // svPt->clear();
  //svEta->clear();
  //svPhi->clear();
  //svMass->clear();
  //svNTks->clear();
  //svChi2->clear();
  //svNdof->clear();
  //svDxy->clear();
  //svDxyErr->clear();
  //svD3d->clear();
  //svD3dErr->clear();
  //costhetasvpv->clear();
}

Measurement1D SoftBTagDumper::vertexD3d(const reco::VertexCompositePtrCandidate &svcand,
					const reco::Vertex &pv) const{
  VertexDistance3D dist;
  reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
  reco::Vertex svtx(svcand.vertex(), csv);
  return dist.distance(svtx, pv);
}

Measurement1D SoftBTagDumper::vertexDxy(const reco::VertexCompositePtrCandidate &svcand,
					const reco::Vertex &pv) const{
  VertexDistanceXY dist;
  reco::Vertex::CovarianceMatrix csv; svcand.fillVertexCovariance(csv);
  reco::Vertex svtx(svcand.vertex(), csv);
  return dist.distance(svtx, pv);
}

float SoftBTagDumper::vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const
				  reco::Vertex &pv) const{
  reco::Candidate::Vector p = sv.momentum();
  reco::Candidate::Vector d(sv.vx() - pv.x(), sv.vy() - pv.y(), sv.vz() - pv.z());
  return p.Unit().Dot(d.Unit());
}
