#include "HiggsAnalysis/MiniAOD2TTree/interface/SoftBTagDumper.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "RecoVertex/VertexTools/interface/VertexDistance.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"


SoftBTagDumper::SoftBTagDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets)
//: // primaryVertexToken(iConsumesCollector.consumes<edm::View<reco::Vertex>>(pset.getParameter<edm::InputTag>("PrimaryVertexSrc"))),
  //   secondaryVertexToken(iConsumesCollector.consumes<edm::View<reco::VertexCompositePtrCandidate>>(pset.getParameter<edm::InputTag>("SecondaryVertexSrc")))
{

  inputCollections = psets;
  booked           = false;

  svPt         = new std::vector<double>[inputCollections.size()];
  svEta        = new std::vector<double>[inputCollections.size()];
  svPhi        = new std::vector<double>[inputCollections.size()];
  svMass       = new std::vector<double>[inputCollections.size()];
  svNTks       = new std::vector<int>[inputCollections.size()];
  svChi2       = new std::vector<double>[inputCollections.size()];
  svNdof       = new std::vector<double>[inputCollections.size()];
  svDxy        = new std::vector<double>[inputCollections.size()];
  svDxyErr     = new std::vector<double>[inputCollections.size()];
  svD3d        = new std::vector<double>[inputCollections.size()];
  svD3dErr     = new std::vector<double>[inputCollections.size()];
  costhetasvpv = new std::vector<double>[inputCollections.size()];

  primaryVertexToken   = new edm::EDGetTokenT<edm::View<reco::Vertex> >[inputCollections.size()];
  secondaryVertexToken = new edm::EDGetTokenT<edm::View<reco::VertexCompositePtrCandidate> >[inputCollections.size()];
  for(size_t i = 0; i < inputCollections.size(); ++i){

    edm::InputTag inputtagPV = inputCollections[i].getParameter<edm::InputTag>("PrimaryVertexSrc");
    primaryVertexToken[i] = iConsumesCollector.consumes<edm::View<reco::Vertex>>(inputtagPV);

    edm::InputTag inputtagSV = inputCollections[i].getParameter<edm::InputTag>("SecondaryVertexSrc");
    secondaryVertexToken[i] = iConsumesCollector.consumes<edm::View<reco::VertexCompositePtrCandidate>>(inputtagSV);
  }

  
}

SoftBTagDumper::~SoftBTagDumper(){}

void SoftBTagDumper::book(TTree* tree){
  booked = true;
  
  for(size_t i = 0; i < inputCollections.size(); ++i){
    std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
    if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();
    tree->Branch((name+"_pt").c_str()     , &svPt[i]);
    tree->Branch((name+"_eta").c_str()    , &svEta[i]);
    tree->Branch((name+"_phi").c_str()    , &svPhi[i]);
    tree->Branch((name+"_mass").c_str()   , &svMass[i]);
    tree->Branch((name+"_nTks").c_str()   , &svNTks[i]);
    tree->Branch((name+"_chi2").c_str()   , &svChi2[i]);
    tree->Branch((name+"_ndof").c_str()   , &svNdof[i]);
    tree->Branch((name+"_dxy").c_str()    , &svDxy[i]);
    tree->Branch((name+"_dxyErr").c_str() , &svDxyErr[i]);
    tree->Branch((name+"_d3d").c_str()    , &svD3d[i]);
    tree->Branch((name+"_d3dErr").c_str() , &svD3dErr[i]);
    tree->Branch((name+"_dotPv").c_str()  , &costhetasvpv[i]);
    
  }
    
  //return;
}

bool SoftBTagDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;
  
  reset();
 
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    // Initialise Variables
    nGoodOfflinePV = -1;
    nGoodOfflineSV = -1;
    
    // Get the Primary Vertex (PV)
    edm::Handle<edm::View<reco::Vertex> > h_primaryVertex;
    iEvent.getByToken(primaryVertexToken[ic], h_primaryVertex);
    nGoodOfflinePV = h_primaryVertex->size();
    
    // Sanity check
    // std::cout << "nGoodOfflinePV = " << nGoodOfflinePV << std::endl;
    if (nGoodOfflinePV < 0) return false;
    reco::Vertex PV = h_primaryVertex->at(0); // the PV
    
    // Get the Secondary Vertex (SV)
    edm::Handle<edm::View<reco::VertexCompositePtrCandidate> > h_secondaryVertex;
    iEvent.getByToken(secondaryVertexToken[ic], h_secondaryVertex);
    nGoodOfflineSV = h_secondaryVertex->size();
    
    // Sanity check
    // std::cout << "nGoodOfflineSV = " << nGoodOfflineSV << std::endl;
    if (nGoodOfflineSV < 0) return false;
    
    if(h_secondaryVertex.isValid())
      {
    
	// For-loop: All Secondary Verticies
	for(size_t isv = 0; isv < h_secondaryVertex->size(); isv++ )
	  {
	    const reco::VertexCompositePtrCandidate &sv = (*h_secondaryVertex)[isv];

	    svPt[ic].push_back(sv.pt());
	    svEta[ic].push_back(sv.eta());
	    svPhi[ic].push_back(sv.phi());
	    svMass[ic].push_back(sv.mass());
	    svNTks[ic].push_back(sv.numberOfDaughters());
	    svChi2[ic].push_back(sv.vertexChi2());
	    svNdof[ic].push_back(sv.vertexNdof());
	    svDxy[ic].push_back(vertexDxy(sv,PV).value());
	    svDxyErr[ic].push_back(vertexDxy(sv,PV).error());
	    svD3d[ic].push_back(vertexD3d(sv,PV).value());
	    svD3dErr[ic].push_back(vertexD3d(sv,PV).error());
	    costhetasvpv[ic].push_back(vertexDdotP(sv, PV));
	    
	    
	  }//eof: loop on sec vertex
      }
  
   
  }//eof: loop on inputcollections
  return filter();
}

//bool SoftBTagDumper::filter(){
//  return true;
//}

void SoftBTagDumper::reset(){
  
  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    svPt[ic].clear();
    svEta[ic].clear();
    svPhi[ic].clear();
    svMass[ic].clear();
    svNTks[ic].clear();
    svChi2[ic].clear();
    svNdof[ic].clear();
    svDxy[ic].clear();
    svDxyErr[ic].clear();
    svD3d[ic].clear();
    svD3dErr[ic].clear();
    costhetasvpv[ic].clear();
  }
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

double SoftBTagDumper::vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const
				  reco::Vertex &pv) const{
  reco::Candidate::Vector p = sv.momentum();
  reco::Candidate::Vector d(sv.vx() - pv.x(), sv.vy() - pv.y(), sv.vz() - pv.z());
  return p.Unit().Dot(d.Unit());
}
