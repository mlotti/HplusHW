#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperCaloTau.h"

#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"

//jets
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
//#include "JetMETCorrections/Algorithms/interface/JetPlusTrackCorrector.h"
//#include "RecoJets/JetPlusTracks/interface/JetPlusTrackCorrector.h"
#include "DataFormats/JetReco/interface/JetExtendedAssociation.h"
#include "DataFormats/JetReco/interface/JetID.h"
// taus
#include "DataFormats/TauReco/interface/CaloTau.h"
#include "RecoTauTag/TauTagTools/interface/CaloTauElementsOperators.h"
#include "RecoTauTag/RecoTau/interface/TauDiscriminationProducerBase.h"
//
// muons and tracks
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"

// ecal
//#include "DataFormats/EgammaCandidates/interface/PixelMatchGsfElectron.h"
#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/EgammaReco/interface/ClusterShapeFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
// candidates
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <string>

namespace HPlusAnalysis {

HPlusTauDumperCaloTau::HPlusTauDumperCaloTau(edm::EDProducer& producer,
                                             edm::ParameterSet& aTauCollectionParameterSet,
                                             Counter* counter)
: HPlusTauDumperBase(producer, aTauCollectionParameterSet, counter) {
  calojetsSrc      = aTauCollectionParameterSet.getParameter< std::string > ("calojets");
  jetsIDSrc        = aTauCollectionParameterSet.getParameter< std::string > ("jetsID");
  
  fEMFractionCutValue = 0.0;
  if (aTauCollectionParameterSet.exists("EMFractionCutValue")) {
    fEMFractionCutValue = aTauCollectionParameterSet.getParameter<double>("EMFractionCutValue");
  } else {
    edm::LogWarning("HPlus") << "HPlusTauDumperCaloTau: You forgot to define 'EMFractionCutValue' in the config!" << std::endl;
  }
  fmfHPDCutValue = 0.0;
  if (aTauCollectionParameterSet.exists("mfHPDCutValue")) {
    fmfHPDCutValue = aTauCollectionParameterSet.getParameter<double>("mfHPDCutValue");
  } else {
    edm::LogWarning("HPlus") << "HPlusTauDumperCaloTau: You forgot to define 'mfHPDCutValue' in the config!" << std::endl;
  }  

  fmN90HitsCutValue = 0.0;
  if (aTauCollectionParameterSet.exists("mN90HitsCutValue")) {
    fmN90HitsCutValue = aTauCollectionParameterSet.getParameter<double>("mN90HitsCutValue");
  } else {
    edm::LogWarning("HPlus") << "HPlusTauDumperCaloTau: You forgot to define 'mN90HitsCutValue' in the config!" << std::endl;
  } 
 
  fCaloTauEtCutValue = 0.0;
  if (aTauCollectionParameterSet.exists("CaloTauEtCutValue")) {
    fCaloTauEtCutValue = aTauCollectionParameterSet.getParameter<double>("CaloTauEtCutValue");
  } else {
    edm::LogWarning("HPlus") << "HPlusTauDumperCaloTau: You forgot to define 'CaloTauEtCutValue' in the config!" << std::endl;
  }  
  fCaloTauEtaCutValue = 0.0;
  if (aTauCollectionParameterSet.exists("CaloTauEtaCutValue")) {
    fCaloTauEtaCutValue = aTauCollectionParameterSet.getParameter<double>("CaloTauEtaCutValue");
  } else {
    edm::LogWarning("HPlus") << "HPlusTauDumperCaloTau: You forgot to define 'CaloTauEtaCutValue' in the config!" << std::endl;
  }  
  // Common tau variable aliases are created in the base class constructor
  // Discriminator aliases are created in the base class constructor
  std::string alias;
  producer.produces<int>(alias = "SelectedJetsCount").setBranchAlias(alias);


  eventCount = 0;
  jetCount = 0;
  jet2Count = 0;
}

HPlusTauDumperCaloTau::~HPlusTauDumperCaloTau() {
  cout << " counted events " << eventCount << endl;
  cout << " counted jets " << jetCount << endl;
  cout << " counted jets > 1 " << jet2Count << endl;
}

/*
void HPlusTauDumperCaloTau::setupSpecificRootTreeBranches() {
  fRootTree->Branch("dByLeadingTrackFinding", &fdByLeadingTrackFinding);
  fRootTree->Branch("dByLeadingTrackPtCut", &fdByLeadingTrackPtCut);
  fRootTree->Branch("dByIsolation", &fdByIsolation);
  fRootTree->Branch("dAgainstElectron", &fdAgainstElectron); 
  fRootTree->Branch("jtau", &fjtau); 
  fRootTree->Branch("PVx",&fPVx);
  fRootTree->Branch("PVy",&fPVy);
  fRootTree->Branch("PVz",&fPVz); 
  fRootTree->Branch("DrLdgChargedHadronJet",&fDrLdgChargedHadronJet);
  fRootTree->Branch("MinSignalTrackPt",&fMinSignalTrackPt);
  fRootTree->Branch("MinIsolationTrackPt",&fMinIsolationTrackPt);
  fRootTree->Branch("DzTrackLdgChargedHadron",&fDzTrackLdgChargedHadron); 
  eventCount = 0;
  jetCount = 0; 
  jet2Count = 0; 
}

void HPlusTauDumperCaloTau::initializeSpecificBranchData() {
  fdByLeadingTrackFinding = -1;
  fdByLeadingTrackPtCut = -1;
  fdByIsolation = -1;
  fdAgainstElectron = -1;
  fjtau = -1;
  fDrLdgChargedHadronJet = -1;
  fMinSignalTrackPt = -1;
  fPVx = -1;
  fPVy = -1;
  fPVz = -1;
  fMinIsolationTrackPt = -1;
  fDzTrackLdgChargedHadron = -1;


}
*/

bool HPlusTauDumperCaloTau::setData(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // Create pointers to data
  
  // Jet direction
  std::auto_ptr<std::vector<math::XYZVector> > myDataJetE(new std::vector<math::XYZVector>);
  // Leading track properties
  std::auto_ptr<std::vector<math::XYZVector> > myDataLdgChargedHadronP(new std::vector<math::XYZVector>);
  std::auto_ptr<std::vector<float> > myDataLdgChargedHadronJetDR(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataLdgChargedHadronHits(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataLdgChargedHadronNormalizedChi(new std::vector<float>);
  std::auto_ptr<std::vector<math::XYZVector> > myDataLdgChargedHadronIP(new std::vector<math::XYZVector>);
  std::auto_ptr<std::vector<float> > myDataLdgChargedHadronIPTSignificance(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataRtau(new std::vector<float>);
  // Charge related
  std::auto_ptr<std::vector<int> > myDataChargeSum(new std::vector<int>);
  // Charged track isolation related
  std::auto_ptr<std::vector<int> > myDataTrIsoSignalTrackCount(new std::vector<int>);
  std::auto_ptr<std::vector<float> > myDataTrIsoSignalMinTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<int> > myDataTrIsoIsolationTrackCount(new std::vector<int>);
  std::auto_ptr<std::vector<float> > myDataTrIsoHighestIsolationTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataTrIsoIsolationMinTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataTrIsoIsolationMaxDz(new std::vector<float>);
  // Jet energy details
  std::auto_ptr<std::vector<float> > myDataEMFraction(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataMaxHCALOverLdgP(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataECALIsolationET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataMaxHCALClusterET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataChargedHadronET(new std::vector<float>);

  std::auto_ptr<int> myDataSelectedJets(new int);

  // Flight path related
  std::auto_ptr<std::vector<math::XYZVector> > myDataFlightPathLength(new std::vector<math::XYZVector>);
  std::auto_ptr<std::vector<float> > myDataFlightPathTransverseSignificance(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataFlightPathSignificance(new std::vector<float>);
  // Invariant mass related
  std::auto_ptr<std::vector<float> > myDataInvariantMassFromTracksOnly(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataInvariantMassFull(new std::vector<float>);
  
  std::auto_ptr<math::XYZVector> myDataPV(new math::XYZVector);
  
  eventCount++; // FIXME: use the event counter object (fCounter) for this kind of purpose 
  
  // Get discriminators
  std::vector<std::vector<float> > myDiscriminatorData;
  size_t myDiscriminatorCount = fTauDiscriminators.size();
  std::vector<edm::Handle<reco::CaloTauDiscriminator> > myDiscriminatorHandles;
  myDiscriminatorHandles.reserve(myDiscriminatorCount);
  for (size_t i = 0; i < myDiscriminatorCount; ++i) {
    edm::Handle<reco::CaloTauDiscriminator> myEmptyHandle;
    myDiscriminatorHandles.push_back(myEmptyHandle);
    //    cout <<  "Discriminator label " << fTauDiscriminators[i].label() << std::endl;
    if (!iEvent.getByLabel(fTauDiscriminators[i], myDiscriminatorHandles[i])) {
      throw cms::Exception("HPlus") << "Discriminator " << fTauDiscriminators[i].label() << " not found in dataset!" << std::endl;
    }
  }
  // calo jets
  edm::Handle<CaloJetCollection> calojets;
  iEvent.getByLabel(calojetsSrc, calojets); // FIXME set to InputTag instead of string 

  // calo taus
  Handle<CaloTauCollection> theCaloTauHandle;
  iEvent.getByLabel("caloRecoTauProducer",theCaloTauHandle);
  const CaloTauCollection & caloTaus = *(theCaloTauHandle.product());
  int nCaloTaus = caloTaus.size();

  // calo tau discriminators // FIXME: duplicate code
  /*//   
  Handle<CaloTauDiscriminator> theCaloTauDiscriminatorByLeadingTrackFinding;
  iEvent.getByLabel("caloRecoTauDiscriminationByLeadingTrackFinding",theCaloTauDiscriminatorByLeadingTrackFinding);
  //
  Handle<CaloTauDiscriminator> theCaloTauDiscriminatorByLeadingTrackPtCut;
  iEvent.getByLabel("caloRecoTauDiscriminationByLeadingTrackPtCut",theCaloTauDiscriminatorByLeadingTrackPtCut);
  //
  Handle<CaloTauDiscriminator> theCaloTauDiscriminatorByIsolation;
  iEvent.getByLabel("caloRecoTauDiscriminationByIsolation",theCaloTauDiscriminatorByIsolation);
  //
  Handle<CaloTauDiscriminator> theCaloTauDiscriminatorAgainstElectron;
  iEvent.getByLabel("caloRecoTauDiscriminationAgainstElectron",theCaloTauDiscriminatorAgainstElectron);
*/
  Handle<ValueMap<reco::JetID> > jetsID;
  iEvent.getByLabel(jetsIDSrc,jetsID);
  if (!jetsID.isValid()) {
    std::cout << "jetsID handle is a zero pointer" << std::endl;
  }
  
    // get vertex // FIXME: vertex handling to base class
  Handle<reco::VertexCollection> recVtxs;
  iEvent.getByLabel("offlinePrimaryVertices",recVtxs);
  
  // FIXME: move this PV code to base class 
  int nvtx = 0;
  int ntrkV = 0;
  double  PVx, PVy, PVz;
  PVx = -1000.; 
  PVy = -1000.; 
  PVz = -1000.;

  for(unsigned int ind = 0; ind < recVtxs->size(); ind++) {
    if (!((*recVtxs)[ind].isFake())) {
      nvtx = nvtx + 1;
      if(nvtx == 1) {
        PVx  = (*recVtxs)[ind].x();
        PVy  = (*recVtxs)[ind].y();
        PVz  = (*recVtxs)[ind].z();
             //      ntrkV = (*recVtxs)[ind].tracksSize();
        reco::Vertex::trackRef_iterator ittrk;
        for(ittrk =(*recVtxs)[ind].tracks_begin();ittrk != (*recVtxs)[ind].tracks_end(); ++ittrk)
          if( (*recVtxs)[ind].trackWeight(*ittrk)>0.5 ) ntrkV++;
      }
    }
  }

  fPVx = PVx;
  fPVy = PVy;
  fPVz = PVz;
  math::XYZVector myPV(PVx, PVy, PVz);
  *myDataPV = myPV;
  // FIXME: end of block to be moved 

  //  cout << " calo tau vertex  " << nvtx << " calo tau vertex tracks " << ntrkV << endl;
  int jtau = 0;

  double DRMAX = 1000.;
  CaloTau theCaloTau;

  CaloTauCollection::const_iterator iTau;
  int iTauInd = 0;

  // FIXME: not used at all
  float DiscriminatorByLeadingTrackFinding = 0.;
  float DiscriminatorByLeadingTrackPtCut   = 0;
  float DiscriminatorByIsolation           = 0;
  float DiscriminatorAgainstElectron       = 0;

  CaloTauRef theSelectedCaloTauRef;

  if( (nvtx != 1) || (ntrkV < 3) || (ntrkV > 100) ) return false;

  std::vector<CaloTauRef> mySelectedCaloTauRefs;
  // Loop over CaloTau's
  for(iTau = caloTaus.begin(); iTau != caloTaus.end(); iTau++) {
    // Make first cuts and check that the required objects exist
    
    theCaloTau = *iTau;
    iTauInd++;
    CaloTauTagInfoRef myInfo = theCaloTau.caloTauTagInfoRef();
    //std::cout << "tau tag info count=" << myInfoCollection->size() << std::endl;
    //for (myInfoCollection::iterator iTauInfo = myInfoCollection->begin();
    //   iTauInfo = myInfoCollection->end(); ++iTauInfo) {
    // check that tauinfo is not zero pointer
    if (myInfo.isNull())continue;
    const CaloJetRef myJetRef = myInfo->calojetRef();
    // check that jetref is not zero pointer
    if (myJetRef.isNull())continue;    
        
    double mN90  =  myJetRef->n90();
    double mEmf  =  myJetRef->emEnergyFraction(); 
    double mN90Hits = (*jetsID)[myJetRef].n90Hits;
    double mfHPD    = (*jetsID)[myJetRef].fHPD;
    double mfRBX    = (*jetsID)[myJetRef].fRBX;  
    
    // jet ID selections // FIXME: Set the cut values in config file
   
    if(mEmf < fEMFractionCutValue) continue;  // default value = 0.01
    if(mfHPD > fmfHPDCutValue) continue;  // default value = 0.98
    if(mN90Hits < fmN90HitsCutValue) continue;  // default value = 2
     
    // consider only jets with raw ET > 4 GeV. // FIXME: Set the cut values in config file
    if( theCaloTau.pt() < fCaloTauEtCutValue ) continue;
    if(fabs(theCaloTau.eta()) > fCaloTauEtaCutValue ) continue;

    
    // Obtain leading track (0.5 around jet axis) // FIXME: Set the cut values in config file
    string metric = "DR"; // can be DR,angle,area
    double ip = -1;
    // settings for tau isolation
    double matchingConeSize  = 0.10;
    double signalConeSize    = 0.07;
    double isolationConeSize = 0.5;
    //      double isolationConeSize = 0.4;
    double ptLeadingTrackMin = 0.;
    double ptOtherTracksMin  = 0.;
    //      double ptLeadingTrackMin = 6.;
    //      double ptOtherTracksMin  = 1.;
    unsigned int isolationAnnulus_Tracksmaxn = 0;
    
    CaloTauElementsOperators op(theCaloTau);
    const TrackRef myLdgChargedHadronTrackRef = op.leadTk(metric,isolationConeSize,ptLeadingTrackMin);
    if (myLdgChargedHadronTrackRef.isNull()) continue;

    CaloTauRef theCaloTauRef(theCaloTauHandle,iTauInd);
    if (theCaloTauRef.isNull()) continue;

    // NOTE: No more continue-calls after this line!!!
    // Otherwise the data will be corrupt, since the data vector sizes will be different

    mySelectedCaloTauRefs.push_back(theCaloTauRef);
    
    //math::XYZVector(theCaloTau.px(), theCaloTau.py(), theCaloTau.pz());
    math::XYZVector myJetVector = theCaloTau.momentum();
    myDataJetE->push_back(myJetVector);
    myDataEMFraction->push_back(mEmf); // FIXME move to appropriate place
    
    /* 
    DiscriminatorByLeadingTrackFinding = (*theCaloTauDiscriminatorByLeadingTrackFinding)[theCaloTauRef];
    DiscriminatorByLeadingTrackPtCut   = (*theCaloTauDiscriminatorByLeadingTrackPtCut)[theCaloTauRef];
    DiscriminatorByIsolation           = (*theCaloTauDiscriminatorByIsolation)[theCaloTauRef];
    DiscriminatorAgainstElectron       = (*theCaloTauDiscriminatorAgainstElectron)[theCaloTauRef];
    */
    
    /*
    // Set discriminator variables FIXME
    for (size_t j = 0; j < myDiscriminatorCount; ++j) {
      myDiscriminatorData[j]
      fTauDiscriminatorValues[j] = (*myDiscriminatorHandles[j])[theCaloTauRef];
    }  
    */

    cout << " theCaloTau.isolationECALhitsEtSum()   " << theCaloTau.isolationECALhitsEtSum()  << endl;     
    cout << " theCaloTau.isolationTracksEtSum()   " << theCaloTau.isolationTracksPtSum()  << endl;      
        // e.m. isolation
    float pisol = -1.;
    if (DiscriminatorByLeadingTrackPtCut == 1.) { pisol = theCaloTau.isolationECALhitsEtSum();} // FIXME
    myDataECALIsolationET->push_back(pisol);
    
    /*fdByLeadingTrackFinding = DiscriminatorByLeadingTrackFinding;
    fdByLeadingTrackPtCut = DiscriminatorByLeadingTrackPtCut;
    fdByIsolation = DiscriminatorByIsolation;
    fdAgainstElectron = DiscriminatorAgainstElectron;*/
    
    
    //    std::cout << " DiscriminatorByLeadingTrackFinding =" << DiscriminatorByLeadingTrackFinding  << "   DiscriminatorByLeadingTrackPtCut " << DiscriminatorByLeadingTrackPtCut << "    DiscriminatorByIsolation " <<  DiscriminatorByIsolation  << " DiscriminatorAgainstElectron " << DiscriminatorAgainstElectron << endl;
    
    // Charged track isolation
    double d_trackIsolation = 
      op.discriminatorByIsolTracksN(metric,
				    matchingConeSize,
				    ptLeadingTrackMin,
				    ptOtherTracksMin,
				    metric,
				    signalConeSize,
				    metric,
				    isolationConeSize,
				    isolationAnnulus_Tracksmaxn);
    
    // Leading track
    math::XYZVector myLeadingChargedTrack = myLdgChargedHadronTrackRef->momentum();
    myDataLdgChargedHadronP->push_back(myLeadingChargedTrack);
    myDataLdgChargedHadronHits->push_back(myLdgChargedHadronTrackRef->numberOfValidHits());
    myDataLdgChargedHadronNormalizedChi->push_back(myLdgChargedHadronTrackRef->normalizedChi2());
    myDataLdgChargedHadronIP->push_back(math::XYZVector(-1.,-1.,-1.)); // FIXME 
    myDataLdgChargedHadronIPTSignificance->push_back(-1.); // FIXME
    
    //double DRltrjet = deltaR(myLdgChargedHadronTrackRef->eta(),myLdgChargedHadronTrackRef->phi(),theCaloTau.eta(),theCaloTau.phi()); 
    myDataLdgChargedHadronJetDR->push_back(deltaR(myJetVector, myLeadingChargedTrack));
    
    if ( theCaloTau.p()) {
      myDataRtau->push_back(myLdgChargedHadronTrackRef->p() / theCaloTau.p());
    } else {
      myDataRtau->push_back(-1.);
    }
    
    //	  cout << " rtau  " << fRtau << "  fLdgChargedHadronIPT " << fLdgChargedHadronIPT  <<endl;  
    
    // Charged track isolation, signal cone
    const TrackRefVector signalTracks = op.tracksInCone(myLdgChargedHadronTrackRef->momentum(),metric,signalConeSize,ptOtherTracksMin);
    //	    ntrsign->push_back(signalTracks.size());
    double pTtrkMin = 1000.;
    double pTmin = 1000.;
    int mySignalTrackCount = 0;
    int myChargeSum = 0;
    math::XYZVector myPtSum(0,0,0);
    if( signalTracks.size() > 0 ) {
      for (reco::TrackRefVector::const_iterator it = signalTracks.begin(); it != signalTracks.end(); ++it) {
	const double pt  = (*it)->pt();
	//	    const reco::TrackRef myTrack = (*it)->trackRef();
	if (pt  > 1 ) {
	  ++mySignalTrackCount;
	  myChargeSum += (*it)->charge();
	  myPtSum += (*it)->momentum();
	}
	if(pt < pTmin) {
	  pTmin = pt;
	  pTtrkMin = pt;;
	}
      }
    }
    myDataChargeSum->push_back(myChargeSum);
    myDataTrIsoSignalTrackCount->push_back(mySignalTrackCount);
    myDataTrIsoSignalMinTrackPt->push_back(pTtrkMin);
    myDataChargedHadronET->push_back(sqrt(myPtSum.Perp2()));
    
    // Charged track isolation, isolation cone
    // FIXME: does this look at the tracks in isolation cone or isolation annulus? 
    double myHighestIsolationTrackPt = 0;
    int myIsolationTrackCount = 0;
    const TrackRefVector isolatTracks = op.tracksInCone(myLdgChargedHadronTrackRef->momentum(),metric,isolationConeSize,ptOtherTracksMin);
    pTtrkMin = 1000.;
    pTmin = 1000.;
    double dzMax = 0.;
    for (reco::TrackRefVector::const_iterator it = isolatTracks.begin(); it != isolatTracks.end(); ++it) {
      const double pt  = (*it)->pt();
      ++myIsolationTrackCount;
      double dz = fabs(myLdgChargedHadronTrackRef->vz()-(*it)->vz());
      if(dz > dzMax) {
	dzMax = dz;
      }
      if(pt < pTmin) {
	pTmin = pt;
	pTtrkMin = pt;
      }
      if ((*it)->pt() > myHighestIsolationTrackPt ) {
	myHighestIsolationTrackPt = (*it)->pt();
	//	      ++myIsolationTrackCount;
      }
    }
    myDataTrIsoIsolationTrackCount->push_back(myIsolationTrackCount);
    myDataTrIsoHighestIsolationTrackPt->push_back(myHighestIsolationTrackPt);
    myDataTrIsoIsolationMinTrackPt->push_back(pTtrkMin);
    myDataTrIsoIsolationMaxDz->push_back(dzMax);
    
    // Jet energy details
    myDataMaxHCALOverLdgP->push_back(-1.); // FIXME
    myDataMaxHCALClusterET->push_back(-1.); // FIXME
    
    // Flight path - FIXME: move this code to the base class
    myDataFlightPathLength->push_back(math::XYZVector(-1.,-1.,-1.));
    myDataFlightPathTransverseSignificance->push_back(-1.);
    myDataFlightPathSignificance->push_back(-1.);
    
    // Invariant mass FIXME: move this code to the base class (if possible)
    myDataInvariantMassFromTracksOnly->push_back(-1.);
    myDataInvariantMassFull->push_back(-1.);
    
    // FIXME: Are the following counters used for anything?
    jtau++;
    jetCount++;
    if ( jtau > 1 ) jet2Count++;
    
    fjtau = jtau;
  }
  *myDataSelectedJets = mySelectedCaloTauRefs.size();
  
  // Put event data
  if (!mySelectedCaloTauRefs.size()) return false;
  // Jet direction
  iEvent.put(myDataJetE, "jetE");

  iEvent.put(myDataSelectedJets, "SelectedJetsCount");

  // Leading track properties
  iEvent.put(myDataLdgChargedHadronP, "ldgChargedHadronP");
  iEvent.put(myDataLdgChargedHadronJetDR, "ldgChargedHadronJetDR");
  iEvent.put(myDataLdgChargedHadronHits, "ldgChargedHadronHits");
  iEvent.put(myDataLdgChargedHadronNormalizedChi, "ldgChargedHadronNormalizedChi");
  iEvent.put(myDataLdgChargedHadronIP, "ldgChargedHadronIP");
  iEvent.put(myDataLdgChargedHadronIPTSignificance, "ldgChargedHadronIPTSignificance");
  iEvent.put(myDataRtau, "Rtau");
  // Charge related
  iEvent.put(myDataChargeSum, "chargeSum");
  // Charged track isolation related
  iEvent.put(myDataTrIsoSignalTrackCount, "trIsoSignalTrackCount");
  iEvent.put(myDataTrIsoSignalMinTrackPt, "trIsoSignalMinTrackPt");
  iEvent.put(myDataTrIsoIsolationTrackCount, "trIsoIsolationTrackCount");
  iEvent.put(myDataTrIsoHighestIsolationTrackPt, "trIsoHighestIsolationTrackPt");
  iEvent.put(myDataTrIsoIsolationMinTrackPt, "trIsoIsolationMinTrackPt");
  iEvent.put(myDataTrIsoIsolationMaxDz, "trIsoIsolationMaxDz");
  // Jet energy details
  iEvent.put(myDataEMFraction, "EMFraction");
  iEvent.put(myDataMaxHCALOverLdgP, "maxHCALOverLdgP");
  iEvent.put(myDataECALIsolationET, "ECALIsolationET");
  iEvent.put(myDataMaxHCALClusterET, "maxHCALClusterET");
  iEvent.put(myDataChargedHadronET, "chargedHadronET");
  // Flight path related
  iEvent.put(myDataFlightPathLength, "flightPathLength");
  iEvent.put(myDataFlightPathTransverseSignificance, "flightPathTransverseSignificance");
  iEvent.put(myDataFlightPathSignificance, "flightPathSignificance");
  // Invariant mass related
  iEvent.put(myDataInvariantMassFromTracksOnly, "invariantMassFromTracksOnly");
  iEvent.put(myDataInvariantMassFull, "invariantMassFull");
  // Discriminators
  for (size_t j = 0; j < myDiscriminatorCount; ++j) {
    std::auto_ptr<std::vector<float> > myDiscriminatorValues(new std::vector<float>);
    for (std::vector<reco::CaloTauRef>::const_iterator it = mySelectedCaloTauRefs.begin(); it != mySelectedCaloTauRefs.end(); ++it) {
      myDiscriminatorValues->push_back((*myDiscriminatorHandles[j])[*it]);
    }
    iEvent.put(myDiscriminatorValues, "mydisc"+fTauDiscriminators[j].label());
  }
  
  // Other
  iEvent.put(myDataPV, "primaryVertex");
  
  myDiscriminatorHandles.clear();
  return true;
}
  /*


 
    if( calojets->size() > 0 ) {
      int jc = 0;
      for( CaloJetCollection::const_iterator cjet = calojets->begin(); 
           cjet != calojets->end(); ++cjet ){ 
        
        // raw jet selection 
        RefToBase<Jet> jetRef(Ref<CaloJetCollection>(calojets,jc));
        double mN90  = (*calojets)[jc].n90();
        double mEmf  = (*calojets)[jc].emEnergyFraction(); 
	if (jetRef.isNull())continue;   
	double mN90Hits = (*jetsID)[jetRef].n90Hits;
	double mfHPD    = (*jetsID)[jetRef].fHPD;
	double mfRBX    = (*jetsID)[jetRef].fRBX; 
     
        jc++;

        // jet ID selections

        if(mEmf < 0.01) continue;
        if(mfHPD>0.98) continue;
        if(mN90Hits < 2) continue;
        if(fabs(cjet->eta()) > 2.5) continue;

        // consider only jets with raw ET > 4 GeV.

        if( cjet->pt() < 4.0 ) continue;


        // Set tau jet related variables
        TLorentzVector myTauJetVector(cjet->px(), cjet->py(), cjet->pz(), cjet->energy()); 
        fJetET = myTauJetVector.Perp();
	if (fJetET > 0) {
	  fJetEta = myTauJetVector.Eta();
	  fJetPhi = myTauJetVector.Phi(); 
	}
    
        
        // match calo tau with calo jet
        double DRMAX = 1000.;
        CaloTau theCaloTau;

        CaloTauCollection::const_iterator iTau;
        int iTauInd = 0;

        float DiscriminatorByLeadingTrackFinding = 0.;
        float DiscriminatorByLeadingTrackPtCut   = 0;
        float DiscriminatorByIsolation           = 0;
        float DiscriminatorAgainstElectron       = 0;

	CaloTauRef theSelectedCaloTauRef;
        for(iTau = caloTaus.begin(); iTau != caloTaus.end(); iTau++) {
          double DR = deltaR(cjet->eta(),cjet->phi(),iTau->eta(),iTau->phi());
          if(DR < DRMAX) {
            theCaloTau = *iTau;
            DRMAX = DR;
            CaloTauRef  theCaloTauRef(theCaloTauHandle,iTauInd);
	    if (theCaloTauRef.isNonnull()) {
	      theSelectedCaloTauRef = theCaloTauRef;
	      iTauInd++;
	      DiscriminatorByLeadingTrackFinding = (*theCaloTauDiscriminatorByLeadingTrackFinding)[theCaloTauRef];
	      DiscriminatorByLeadingTrackPtCut   = (*theCaloTauDiscriminatorByLeadingTrackPtCut)[theCaloTauRef];
	      DiscriminatorByIsolation           = (*theCaloTauDiscriminatorByIsolation)[theCaloTauRef];
	      DiscriminatorAgainstElectron       = (*theCaloTauDiscriminatorAgainstElectron)[theCaloTauRef];
	      // Set discriminator variables
	      for (size_t j = 0; j < myDiscriminatorCount; ++j) {
		fTauDiscriminatorValues[j] = (*myDiscriminatorHandles[j])[theCaloTauRef];
	      }   	
	    }
          }
        }


	//	if (theSelectedCaloTauRef.isNull()) continue;
	if (theSelectedCaloTauRef.isNonnull()) {

	//   cout << " theCaloTau.isolationECALhitsEtSum()   " << theSelectedCaloTauRef->isolationECALhitsEtSum()  << endl;     
      
        // e.m. isolation
        float pisol = 1000.;
        if(DiscriminatorByLeadingTrackPtCut == 1.) { pisol = theSelectedCaloTauRef->isolationECALhitsEtSum();}

	f, ationET = pisol;	  
	fdByLeadingTrackFinding = DiscriminatorByLeadingTrackFinding;
	fdByLeadingTrackPtCut = DiscriminatorByLeadingTrackPtCut;
	fdByIsolation = DiscriminatorByIsolation;
	fdAgainstElectron = DiscriminatorAgainstElectron;

 
        // settings for tau isolation
        double matchingConeSize  = 0.10;
        double signalConeSize    = 0.07;
        double isolationConeSize = 0.5;
        //      double isolationConeSize = 0.4;
        double ptLeadingTrackMin = 0.;
        double ptOtherTracksMin  = 0.;
        //      double ptLeadingTrackMin = 6.;
        //      double ptOtherTracksMin  = 1.;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0;

        CaloTauElementsOperators op(theCaloTau);
        double d_trackIsolation = 
	  op.discriminatorByIsolTracksN(metric,
            matchingConeSize,
            ptLeadingTrackMin,
            ptOtherTracksMin,
            metric,
            signalConeSize,
            metric,
            isolationConeSize,
            isolationAnnulus_Tracksmaxn);
           
        // leading track in cone 0.5 around jet axis
        const TrackRef myLdgChargedHadronTrackRef =op.leadTk(metric,isolationConeSize,ptLeadingTrackMin);

	////if ( myLdgChargedHadronTrackRef.isNull() ) continue;

	double ip = -1;
	bool myLdgChargedHadronTrackExists = false;
	if (myLdgChargedHadronTrackRef.isNonnull()) {
	  myLdgChargedHadronTrackExists = true;
	  fLdgChargedHadronPT = myLdgChargedHadronTrackRef->pt();
	  fLdgChargedHadronHits = myLdgChargedHadronTrackRef->numberOfValidHits();
	  fLdgChargedHadronNormalizedChi = myLdgChargedHadronTrackRef->normalizedChi2();
	  // FIXME: add IP information
	  fLdgChargedHadronIPT = -1;
	  fLdgChargedHadronIPTSignificance = -1;
	  fLdgChargedHadronIPz = -1;    
	  fLdgChargedHadronIPT = fabs(myLdgChargedHadronTrackRef->dxy((*recVtxs)[0].position()));
	  double DRltrjet = deltaR(myLdgChargedHadronTrackRef->eta(),myLdgChargedHadronTrackRef->phi(),cjet->eta(),cjet->phi()); 
	  fDrLdgChargedHadronJet = DRltrjet;
	  if (myTauJetVector.P()) {
	    fRtau = myLdgChargedHadronTrackRef->p() / myTauJetVector.P();
	  }
	 
////	}
       	 
	//	  cout <<  " rtau " << fRtau << endl;	

    
	// tracks in signal cone
	const TrackRefVector signalTracks = op.tracksInCone(myLdgChargedHadronTrackRef->momentum(),metric,signalConeSize,ptOtherTracksMin);
	//	    ntrsign->push_back(signalTracks.size());
	double pTtrkMin = 1000.;
	double pTmin = 1000.;
	int mySignalTrackCount = 0;
	int myChargeSum = 0;
	math::XYZVector myPtSum(0,0,0);
	if( signalTracks.size() > 0 ) {
	  for (reco::TrackRefVector::const_iterator it = signalTracks.begin(); it != signalTracks.end(); ++it) {
	    const double pt  = (*it)->pt();
	    //	    const reco::TrackRef myTrack = (*it)->trackRef();
	    if (pt  > 1 ) {
	      ++mySignalTrackCount;
	      myChargeSum += (*it)->charge();
	      myPtSum += (*it)->momentum();
	    }
	    if(pt < pTmin) {
	      pTmin = pt;
	      pTtrkMin = pt;;
	    }
	  }
	}

	fTrIsoSignalTrackCount = mySignalTrackCount;
	fMinSignalTrackPt = pTtrkMin;
	fChargeSum = myChargeSum;
       
	//	  cout <<  " signalTracks.size() " << signalTracks.size() << endl;	
	/// Charged track isolation
	// const double tracktorefpoint_maxDZ,const double refpoint_Z)const;
	double myHighestIsolationTrackPt = 0;
	int myIsolationTrackCount = 0;
	const TrackRefVector isolatTracks = op.tracksInCone(myLdgChargedHadronTrackRef->momentum(),metric,isolationConeSize,ptOtherTracksMin);
	pTtrkMin = 1000.;
	pTmin = 1000.;
	double dzMax = 0.;
	for (reco::TrackRefVector::const_iterator it = isolatTracks.begin(); it != isolatTracks.end(); ++it) {
	  const double pt  = (*it)->pt();
	  ++myIsolationTrackCount;
	  double dz = fabs(myLdgChargedHadronTrackRef->vz()-(*it)->vz());
	  if(dz > dzMax) {
	    dzMax = dz;
	  }
	  if(pt < pTmin) {
	    pTmin = pt;
	    pTtrkMin = pt;
	  }
	  if ((*it)->pt() > myHighestIsolationTrackPt ) {
	    myHighestIsolationTrackPt = (*it)->pt();
	    //	      ++myIsolationTrackCount;
	  }
	}

	fTrIsoIsolationTrackCount = myIsolationTrackCount;
	fTrIsoHighestIsolationTrackPt = myHighestIsolationTrackPt;
	fMinIsolationTrackPt = pTtrkMin;
	fDzTrackLdgChargedHadron = dzMax;

	  
   // Calorimetry related
	fEMFraction = (*calojets)[jc].emEnergyFraction(); 
	fChargedHadronET = sqrt(myPtSum.Perp2());

       
      }//end of if (myLdgChargedHadronTrackRef.isNonnull())

	// Set discriminator variables
	for (size_t j = 0; j < myDiscriminatorCount; ++j) {
	  fTauDiscriminatorValues[j] = (*myDiscriminatorHandles[j])[theSelectedCaloTauRef];
	}   
	

	}


	jtau++;
	jetCount++;
	if ( jtau > 1 ) jet2Count++;
   
	fjtau = jtau;
	// Save tau-jet info to ROOT tree
	if(jtau >= 1) fRootTree->Fill();

      }

  */


    
    // Calorimetry related
	//	fMaxHCALOverLdgP = (*calojets)[jc].hcalMaxOverPLead();
    /*
    if (myLdgChargedHadronTrackExists) {
             f, ationET = myTauJetRef->isolationPFGammaCandsEtSum(); // nan if ldg track does not exist
           }
             fMaxHCALClusterET = myTauJetRef->maximumHCALPFClusterEt();
             fChargedHadronET = sqrt(myPtSum.Perp2());
    
    // Flight path related
             fFlightPathTransverseLength = -1; // FIXME
             fFlightPathTransverseSignificance = -1;// FIXME
             fFlightPathSignificance = -1;// FIXME
             fInvariantMassFromTracksOnly = -1;// FIXME
             fInvariantMassFull = -1;// FIXME
    
    // PF specific
             fPFElectronPreIDOutput = myTauJetRef->electronPreIDOutput();
             fPFElectronPreIDDecision = myTauJetRef->electronPreIDDecision();
    // Loop over all candidate tracks to calculate neutral hadron, gamma, and PF electron ET 
    
    
             fPFNeutralHadronET = -1;// FIXME
             fPFGammaET = -1;// FIXME
             fPFElectronET = -1;// FIXME
    

    // Set discriminator variables
             for (size_t j = 0; j < myDiscriminatorCount; ++j) {
             fTauDiscriminatorValues[j] = (*myDiscriminatorHandles[j])[myTauJetRef];
           }
 
    

             if(jtau >= 1) t1->Fill();
         */
  /*


    }

    myDiscriminatorHandles.clear();
  }  
*/

}
