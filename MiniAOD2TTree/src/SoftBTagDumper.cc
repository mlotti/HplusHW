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
  
}

SoftBTagDumper::~SoftBTagDumper(){}

void SoftBTagDumper::book(TTree* tree){

  // Secondary Vertex Collection
  tree->Branch("svPt"        , &svPt );
  tree->Branch("svEta"       , &svEta );
  tree->Branch("svPhi"       , &svPhi );
  tree->Branch("svMass"      , &svMass );
  tree->Branch("svNTks"      , &svNTks );
  tree->Branch("svChi2"      , &svChi2 );
  tree->Branch("svNdof"      , &svNdof );
  tree->Branch("svDxy"       , &svDxy );
  tree->Branch("svDxyErr"    , &svDxyErr );
  tree->Branch("svD3d"       , &svD3d );
  tree->Branch("svD3dErr"    , &svD3dErr );
  tree->Branch("costhetasvpv", &costhetasvpv );
  
  return;
}

bool SoftBTagDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){

  // Initialise Variables
  nGoodOfflinePV = -1;
  nGoodOfflineSV = -1;

  // Get the Primary Vertex (PV)
  edm::Handle<edm::View<reco::Vertex> > h_primaryVertex;
  if(iEvent.getByToken(primaryVertexToken, h_primaryVertex)) nGoodOfflinePV = h_primaryVertex->size();

  // Sanity check
  std::cout << "nGoodOfflinePV = " << nGoodOfflinePV << std::endl;
  if (nGoodOfflinePV < 0) return false;

  // Get the Secondary Vertex (SV)
  reco::Vertex PV = h_primaryVertex->at(0); // the PV
  edm::Handle<edm::View<reco::VertexCompositePtrCandidate> > h_secondaryVertex;
  if(iEvent.getByToken(secondaryVertexToken, h_secondaryVertex)) nGoodOfflineSV = h_secondaryVertex->size();

  // Sanity check
  std::cout << "nGoodOfflineSV = " << nGoodOfflineSV << std::endl;
  if (nGoodOfflineSV < 0) return false;

  // For-loop: All Secondary Verticies
  for(size_t isv = 0; isv < h_secondaryVertex->size(); isv++ )
    {
      const reco::VertexCompositePtrCandidate &sv = (*h_secondaryVertex)[isv];
      svPt         = sv.pt();
      svEta        = sv.eta();
      svPhi        = sv.phi();
      svMass       = sv.mass();
      svNTks       = sv.numberOfDaughters();
      svChi2       = sv.vertexChi2();
      svNdof       = sv.vertexNdof();
      svDxy        = vertexDxy(sv,PV).value();
      svDxyErr     = vertexDxy(sv,PV).error();
      svD3d        = vertexD3d(sv,PV).value();
      svD3dErr     = vertexD3d(sv,PV).error();
      costhetasvpv = vertexDdotP(sv, PV);
    }//eof: loop on sec vertex
    
  return filter();
}

bool SoftBTagDumper::filter(){
  return true;
}

void SoftBTagDumper::reset(){
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
