#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperPF.h"

#include "DataFormats/TauReco/interface/PFTauDecayMode.h"
#include "DataFormats/TauReco/interface/PFTauDecayModeAssociation.h"
#include "DataFormats/TauReco/interface/PFTauTagInfo.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "RecoTauTag/TauTagTools/interface/TauTagTools.h"
#include "DataFormats/TauReco/interface/PFTauTagInfoFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Math/interface/Vector.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/deltaR.h"
// Required for secondary vertex fitting
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
//#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "PhysicsTools/RecoAlgos/plugins/KalmanVertexFitter.h"
#include "RecoTauTag/RecoTau/interface/PFRecoTauAlgorithmBase.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h" //flightPathSignificance
#include "DataFormats/VertexReco/interface/Vertex.h"

namespace HPlusAnalysis {
  
  HPlusTauDumperPF::HPlusTauDumperPF(edm::EDProducer& producer, edm::ParameterSet& aTauCollectionParameterSet,
				     Counter* counter)
    : HPlusTauDumperBase(producer, aTauCollectionParameterSet, counter) {
    std::string alias;
    // Declare produced items (class-specific): BDT output from Electron PreID
    producer.produces<std::vector<float> >(alias = "PFElectronPreIDOutput").setBranchAlias(alias);
    // Declare produced items (class-specific): Decision from Electron PreID
    producer.produces<std::vector<float> >(alias = "PFElectronPreIDDecision").setBranchAlias(alias);
    producer.produces<std::vector<float> >(alias = "PFNeutralHadronET").setBranchAlias(alias);
    producer.produces<std::vector<float> >(alias = "PFGammaET").setBranchAlias(alias);
    producer.produces<std::vector<float> >(alias = "PFElectronET").setBranchAlias(alias);
    // Initialize counters    
    fCounter0pr = fCounter->addCounter("0prong PFTau");
    fCounter1pr = fCounter->addCounter("1prong PFTau");
    fCounter2pr = fCounter->addCounter("2prong PFTau");
    fCounter3pr = fCounter->addCounter("3prong PFTau");
    fCounterXpr = fCounter->addCounter("Xprong PFTau");
    fCounterPFelectronsSignalCone  = fCounter->addCounter("PFelectronsSignalCone");
    fCounterPFNeutHadrsSignalCone  = fCounter->addCounter("PFNeutHadrsSignalCone");
    fCounterPFelectronsIsolCone    = fCounter->addCounter("PFelectronsIsolCone");
    fCounterPFNeutHadrsIsolCone    = fCounter->addCounter("PFNeutHadrsIsolCone"); 
    
    // Common tau variable aliases are created in the base class constructor
    // Discriminator aliases are created in the base class constructor
  }

HPlusTauDumperPF::~HPlusTauDumperPF() {

}

/*void HPlusTauDumperPF::setupSpecificRootTreeBranches() {
  fRootTree->Branch("fPFElectronPreIDOutput", &fPFElectronPreIDOutput);
  fRootTree->Branch("fPFElectronPreIDDecision", &fPFElectronPreIDDecision);
  fRootTree->Branch("fPFNeutralHadronET", &fPFNeutralHadronET);
  fRootTree->Branch("fPFGammaET", &fPFGammaET);
  fRootTree->Branch("fPFElectronET", &fPFElectronET);
}

void HPlusTauDumperPF::initializeSpecificBranchData() {
  fPFElectronPreIDOutput = -1;
  fPFElectronPreIDDecision = -1;
  fPFNeutralHadronET = -1;
  fPFGammaET = -1;
  fPFElectronET = -1;
}
*/
bool HPlusTauDumperPF::setData(edm::Event& iEvent, const edm::EventSetup& iSetup) {
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
  std::auto_ptr<std::vector<float> > myDataTrIsoLowestSignalTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<int> > myDataTrIsoIsolationTrackCount(new std::vector<int>);
  std::auto_ptr<std::vector<float> > myDataTrIsoHighestIsolationTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataTrIsoSignalMinTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataTrIsoIsolationMinTrackPt(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataTrIsoIsolationMaxDz(new std::vector<float>);
  // Jet energy details
  std::auto_ptr<std::vector<float> > myDataEMFraction(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataMaxHCALOverLdgP(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataECALIsolationET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataMaxHCALClusterET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataChargedHadronET(new std::vector<float>);
  // Flight path related
  // std::auto_ptr<std::vector<math::XYZVector> > myDataFlightPathLength(new std::vector<math::XYZVector>);
  std::auto_ptr<std::vector<float> > myDataFlightPathLength(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataFlightPathSignificance(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataFlightPathTransverseLength(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataFlightPathTransverseSignificance(new std::vector<float>);
  // Invariant mass related
  std::auto_ptr<std::vector<float> > myDataInvariantMassFromTracksOnly(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataInvariantMassFull(new std::vector<float>);
  // PF specific
  std::auto_ptr<std::vector<float> > myDataPFElectronPreIDOutput(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataPFElectronPreIDDecision(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataPFNeutralHadronET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataPFGammaET(new std::vector<float>);
  std::auto_ptr<std::vector<float> > myDataPFElectronET(new std::vector<float>);
  // other
  std::auto_ptr<math::XYZVector> myDataPV(new math::XYZVector);
  math::XYZVector myPV(-1., -1., -1.);
  *myDataPV = myPV;
  std::cout << "myPV = " << myPV << std::endl;
  
  // Primary vertex
  reco::Vertex PV;
  edm::Handle<edm::View<reco::Vertex> > vertexHandle;
  iEvent.getByLabel("offlinePrimaryVertices", vertexHandle);
  const edm::View<reco::Vertex>& vertexCollection(*vertexHandle);
  PV = *(vertexCollection.begin());

  // Get tau jets
  edm::Handle<reco::PFTauCollection> myTauJets;
  if (!iEvent.getByLabel(fTauCollection, myTauJets)) {
    throw cms::Exception("HPlus") << "tau collection not found" << std::endl;
  }
  size_t myTauJetCount = myTauJets->size();

  edm::Handle<reco::PFTauDecayModeAssociation> theDMAssoc; // Get the PFTau->PFTauDecayMode association from event
  iEvent.getByLabel( "shrinkingConePFTauDecayModeProducer", theDMAssoc); // Get the PFTau Decay Modes: associate an inputTag to a handle
    
  // Get discriminators
  size_t myDiscriminatorCount = fTauDiscriminators.size();
  std::vector<edm::Handle<reco::PFTauDiscriminator> > myDiscriminatorHandles;
  myDiscriminatorHandles.reserve(myDiscriminatorCount);
  for (size_t i = 0; i < myDiscriminatorCount; ++i) {
    edm::Handle<reco::PFTauDiscriminator> myEmptyHandle;
    myDiscriminatorHandles.push_back(myEmptyHandle);
    if (!iEvent.getByLabel(fTauDiscriminators[i], myDiscriminatorHandles[i])) {
      throw cms::Exception("HPlus") << "Discriminator " << fTauDiscriminators[i].label() << " not found in dataset!" << std::endl;
    }
  }
  std::vector<reco::PFTauRef> mySelectedPFTauRefs;
  // Loop over the tau jets
  for (size_t i = 0; i < myTauJetCount; ++i) {
    reco::PFTauRef myTauJetRef(myTauJets, i);
    const PFTauDecayMode& theDecayMode = (*theDMAssoc)[myTauJetRef]; //get PFTauDecayMode associated to this PFTau
     
    const PFCandidateRef& myLdgChargedHadronCandidateRef = myTauJetRef->leadPFChargedHadrCand();
    if (myLdgChargedHadronCandidateRef.isNull()) continue;
    // FIXME: add a counter here
    
    const reco::TrackRef myLdgChargedHadronTrackRef = myLdgChargedHadronCandidateRef->trackRef();
    if (myLdgChargedHadronTrackRef.isNull()) continue;
    // FIXME: add a counter here
    
    // NOTE: No more continue-calls after this line!!!
    // Otherwise the data will be corrupt, since the data vector sizes will be different
    
    mySelectedPFTauRefs.push_back(myTauJetRef);
    
    // Set tau jet related variables
    LorentzVector myTauJetVector(myTauJetRef->px(), myTauJetRef->py(), myTauJetRef->pz(), myTauJetRef->energy()); 
    //     fJetET = myTauJetVector.Perp();1
    //     fJetEta = myTauJetVector.Eta();
    //     fJetPhi = myTauJetVector.Phi(); 
    math::XYZVector myJetVector = myTauJetRef->momentum();
    GlobalVector tauDir(myTauJetVector.px(), myTauJetVector.py(), myTauJetVector.pz());
    myDataJetE->push_back(myJetVector);
    
    // Leading charged hadron related
    // const reco::TrackRef myLdgChargedHadronTrackRef = myLdgChargedHadronCandidateRef->trackRef();
    math::XYZVector myLdgChargedHadronMomentum = myLdgChargedHadronTrackRef->momentum();
    myDataLdgChargedHadronP->push_back(myLdgChargedHadronMomentum);
    myDataLdgChargedHadronJetDR->push_back(deltaR(myJetVector, myLdgChargedHadronMomentum));
    myDataLdgChargedHadronHits->push_back(myLdgChargedHadronTrackRef->numberOfValidHits());
    myDataLdgChargedHadronNormalizedChi->push_back(myLdgChargedHadronTrackRef->normalizedChi2());
    // IP information
    myDataLdgChargedHadronIP->push_back(math::XYZVector(myLdgChargedHadronTrackRef->dxy(),myLdgChargedHadronTrackRef->dxy(),myLdgChargedHadronTrackRef->dz())); // Note: dx,dy=dxy! i.e. Transverse Impact Parameter!
    myDataLdgChargedHadronIPTSignificance->push_back(myTauJetRef->leadPFChargedHadrCandsignedSipt());
    if (myJetVector.Mag2()) {
      myDataRtau->push_back(sqrt(myLdgChargedHadronMomentum.Mag2() / myJetVector.Mag2()));
    }
    // Track quality cuts have already been applied to all the PF tracks
    
    // Charged track isolation
    const PFCandidateRefVector& mySignalPFCandidates = myTauJetRef->signalPFCands(); // Leading track is included here 
    const PFCandidateRefVector& myIsolationPFCandidates = myTauJetRef->isolationPFCands(); // Leading track is included here
    const PFCandidateRefVector& mySignalPFGammaCandidates = myTauJetRef->signalPFGammaCands();
    RefVector<PFCandidateCollection>::const_iterator iCand;
    
    // Count the number of signal tracks in the signal cone above a certain pt threshold
    int mySignalTrackCount = 0;
    int myChargeSum = 0;
    double myMinPt = 9999.;
    math::XYZVector myPtSum(0,0,0);
    LorentzVector mySignalPFChHadronsP4; 
    LorentzVector mySignalPFelectronP4;
    LorentzVector myTrackP4;
    LorentzVector myCandP4;
    LorentzVector mySignalPFNeutHadronsP4;
    LorentzVector mySignalPFgammaP4;
    float fphotonEnergy = 0.0;
    
    // Loop over particles within the signal cone  
    for (iCand = mySignalPFCandidates.begin(); iCand != mySignalPFCandidates.end(); ++iCand) {
      // For each Signal PF Candidates return a reference to the corresponding track, if charged.
      const reco::TrackRef myTrack = (*iCand)->trackRef();
      if (myTrack.isNonnull()) {
	// Look at charged hadrons only
	if( ((*iCand)->particleId() == reco::PFCandidate::h) && (myTrack->pt() > 1.0) ) { 
	  double myTrackPt = myTrack->pt();
	  ++mySignalTrackCount; // number of charged tracks in signal cone
	  myChargeSum += myTrack->charge();
	  myPtSum += myTrack->momentum();
	  myTrackP4.SetPxPyPzE( myTrack->momentum().x(), myTrack->momentum().y(), myTrack->momentum().z(), sqrt(myTrack->momentum().Mag2() + 0.139*0.139) ); // mass used is that of charged pion : 0.139 GeV
	  mySignalPFChHadronsP4 += myTrackP4; 	  
	  if (myTrackPt < myMinPt){myMinPt = myTrackPt;}
	}
	// Look at PFelectrons. Apply pt quality cut on track.
	if (myTrack->pt() > 1 && (*iCand)->particleId() == reco::PFCandidate::e){
	  myTrackP4.SetPxPyPzE( myTrack->momentum().x(), myTrack->momentum().y(), myTrack->momentum().z(), sqrt(myTrack->momentum().Mag2() + 0.00051*0.00051) ); // mass used is that of electron: 0.51 MeV (0.00051 GeV)
	  mySignalPFelectronP4  += myTrackP4; 
	  fCounter->addCount(fCounterPFelectronsSignalCone);
	}
      }
      else{
	// Look at neutral hadrons
	if ((*iCand)->particleId() == reco::PFCandidate::h0) {
	  myCandP4.SetPxPyPzE( (*iCand)->momentum().x(), (*iCand)->momentum().y(), (*iCand)->momentum().z(), sqrt((*iCand)->momentum().Mag2() + 0.135*0.135) ); // mass used is that of neutral pion: 0.135 GeV (0.00051 GeV)
	  mySignalPFNeutHadronsP4 += myCandP4; 
	  fCounter->addCount(fCounterPFNeutHadrsSignalCone);
	}
	// Look at PFgammas
	if((*iCand)->particleId() == reco::PFCandidate::gamma){
	  myCandP4.SetPxPyPzE((*iCand)->momentum().x(), (*iCand)->momentum().y(), (*iCand)->momentum().z(), sqrt((*iCand)->momentum().Mag2()));
	  mySignalPFgammaP4 += myCandP4;
	  fphotonEnergy += (*iCand)->ecalEnergy() + (*iCand)->hcalEnergy();
	}
      }
      // Reset variables for next iteration
      myTrackP4.SetPxPyPzE(0, 0, 0, 0);
      myCandP4.SetPxPyPzE(0, 0, 0, 0); 
    } //end of loop
    // Basic Counters
    fCounter->addCount(fCounterXpr);
    if(mySignalTrackCount==0){ fCounter->addCount(fCounter0pr); }
    if(mySignalTrackCount==1){ fCounter->addCount(fCounter1pr); }
    if(mySignalTrackCount==2){ fCounter->addCount(fCounter2pr); }
    if(mySignalTrackCount==3){ fCounter->addCount(fCounter3pr); }
    // Store variables
    myDataChargeSum->push_back(myChargeSum);
    myDataTrIsoSignalTrackCount->push_back(mySignalTrackCount);
    myDataTrIsoLowestSignalTrackPt->push_back(myMinPt);

    // Reset variables
    double myHighestIsolationTrackPt = 0;
    int myIsolationTrackCount = 0;
    LorentzVector myIsolPFelectronP4;
    LorentzVector myIsolPFNeutHadronsP4;
    LorentzVector myIsolPFgammaP4;
    myMinPt = 9999.;
    
    // Loop over particles within the isolation cone
    for (iCand = myIsolationPFCandidates.begin(); iCand != myIsolationPFCandidates.end(); ++iCand) {
      const reco::TrackRef myTrack = (*iCand)->trackRef();
      if (myTrack.isNonnull()) {
	// Look at charged hadrons only
	if ((*iCand)->particleId() == reco::PFCandidate::h) {
          double myTrackPt = myTrack->pt();
          if (myTrackPt > myHighestIsolationTrackPt) {
            myHighestIsolationTrackPt = myTrackPt;
            ++myIsolationTrackCount;
          }
          if (myTrackPt < myMinPt)
            myMinPt = myTrackPt;
        }
	// Look at PFelectrons. Apply pt quality cut on track.
	if (myTrack->pt() > 1 && (*iCand)->particleId() == reco::PFCandidate::e){   // alex
	  myTrackP4.SetPxPyPzE( myTrack->momentum().x(), myTrack->momentum().y(), myTrack->momentum().z(), sqrt(myTrack->momentum().Mag2() + 0.00051*0.00051) ); // mass used is that of electron: 0.51 MeV (0.00051 GeV)
	  myIsolPFelectronP4  += myTrackP4; //alex
	  fCounter->addCount(fCounterPFelectronsIsolCone);
	}
      }
      else{
	// Look at neutral hadrons
	if ((*iCand)->particleId() == reco::PFCandidate::h0) {
	  myCandP4.SetPxPyPzE( (*iCand)->momentum().x(), (*iCand)->momentum().y(), (*iCand)->momentum().z(), sqrt((*iCand)->momentum().Mag2() + 0.135*0.135) ); // mass used is that of electron: 0.51 MeV (0.00051 GeV)
	  myIsolPFNeutHadronsP4 += myCandP4;
	  fCounter->addCount(fCounterPFNeutHadrsIsolCone);
	}
	// Look at PFgammas
	if ((*iCand)->particleId() == reco::PFCandidate::gamma){
	  myCandP4.SetPxPyPzE((*iCand)->momentum().x(), (*iCand)->momentum().y(), (*iCand)->momentum().z(), sqrt((*iCand)->momentum().Mag2()));
	  myIsolPFgammaP4 += myCandP4;
	  fphotonEnergy += (*iCand)->ecalEnergy() + (*iCand)->hcalEnergy();
	}
      }
      // Reset variables for next iteration
      myTrackP4.SetPxPyPzE(0, 0, 0, 0);
      myCandP4.SetPxPyPzE(0, 0, 0, 0);
    } //end of loop
    // Basic Counters
    
    // Store variables
    myDataTrIsoIsolationTrackCount->push_back(myIsolationTrackCount);
    myDataTrIsoHighestIsolationTrackPt->push_back(myHighestIsolationTrackPt);
    myDataTrIsoIsolationMinTrackPt->push_back(myMinPt);
    myDataTrIsoIsolationMaxDz->push_back(-1.); // FIXME
  
    // Calorimetry related
    myDataEMFraction->push_back(myTauJetRef->emFraction()); // fEMFraction = Ecal/Hcal Cluster Energy
    myDataMaxHCALOverLdgP->push_back(myTauJetRef->hcalMaxOverPLead()); //  = (Max. Hcal Cluster Energy)/(leadPFChargedHadron P)
    myDataECALIsolationET->push_back(myTauJetRef->isolationPFGammaCandsEtSum()); // Et Sum of gamma PFCandidates in isolation annulus around Lead PF". Set to nan if ldg track does not exist
    myDataMaxHCALClusterET->push_back(myTauJetRef->maximumHCALPFClusterEt()); // // Et of the highest Et HCAL PFCluster  
    myDataChargedHadronET->push_back(sqrt(myPtSum.Perp2()));
    
    // Invariant mass FIXME: move this code to the base class (if possible)
    myDataInvariantMassFromTracksOnly->push_back(mySignalPFChHadronsP4.M());  // includes 1prong. Remove the 1prong?
    myDataInvariantMassFull->push_back(theDecayMode.mass());

    // PF specific
    myDataPFElectronPreIDOutput->push_back(myTauJetRef->electronPreIDOutput());
    myDataPFElectronPreIDDecision->push_back(myTauJetRef->electronPreIDDecision());
    
    // Loop over all candidate tracks to calculate neutral hadron, gamma, and PF electron ET 
    myDataPFNeutralHadronET->push_back( myIsolPFNeutHadronsP4.Et()); // CHECKME
    myDataPFGammaET->push_back(myIsolPFgammaP4.Et()); // CHECKME
    myDataPFElectronET->push_back(myIsolPFelectronP4.Et()); // CHECKME

  
    // 3Prong and 5Prong related variables
    // ***********************************
    Vertex SV;
    bool withPVError = true;
   
    if(mySignalTrackCount==3){
      SV = threeProng(myTauJetRef, iEvent, iSetup);
      
      // Flight path - FIXME: move this code to the base class
      myDataFlightPathLength->push_back(reco::SecondaryVertex::computeDist3d(PV, SV, tauDir, withPVError).value());
      myDataFlightPathSignificance->push_back(reco::SecondaryVertex::computeDist3d(PV, SV, tauDir, withPVError).significance());
      myDataFlightPathTransverseLength->push_back(reco::SecondaryVertex::computeDist2d(PV, SV, tauDir, withPVError).value());
      myDataFlightPathTransverseSignificance->push_back(reco::SecondaryVertex::computeDist2d(PV, SV, tauDir, withPVError).significance());
    }
    else if(mySignalTrackCount==5){ 
      SV = fiveProng(myTauJetRef, iEvent, iSetup);
      // Flight path - FIXME: move this code to the base class
      myDataFlightPathLength->push_back(reco::SecondaryVertex::computeDist3d(PV, SV, tauDir, withPVError).value());
      myDataFlightPathSignificance->push_back(reco::SecondaryVertex::computeDist3d(PV, SV, tauDir, withPVError).significance());
      myDataFlightPathTransverseLength->push_back(reco::SecondaryVertex::computeDist2d(PV, SV, tauDir, withPVError).value());
      myDataFlightPathTransverseSignificance->push_back(reco::SecondaryVertex::computeDist2d(PV, SV, tauDir, withPVError).significance());
    }
    else{
      // Flight path - FIXME: move this code to the base class
      myDataFlightPathLength->push_back(-1.0);
      myDataFlightPathSignificance->push_back(-1.0);
      myDataFlightPathTransverseLength->push_back(-1.0);
      myDataFlightPathTransverseSignificance->push_back(-1.0);
    }

    // Reset variables for next Event
    mySignalPFChHadronsP4.SetPxPyPzE(0, 0, 0, 0);
    myTrackP4.SetPxPyPzE(0, 0, 0, 0);
    myCandP4.SetPxPyPzE(0, 0, 0, 0);
    mySignalPFelectronP4.SetPxPyPzE(0, 0, 0, 0); 
    myIsolPFelectronP4.SetPxPyPzE(0, 0, 0, 0); 
    myIsolPFgammaP4.SetPxPyPzE(0, 0, 0, 0); 
    mySignalPFNeutHadronsP4.SetPxPyPzE(0, 0, 0, 0);
    mySignalPFgammaP4.SetPxPyPzE(0, 0, 0, 0);

  } //eof: for (size_t i = 0; i < myTauJetCount; ++i) {

  // ***********************************************************************************

  // Put event data
  if (!mySelectedPFTauRefs.size()) return false;
  
  // Jet direction
  iEvent.put(myDataJetE, "jetE");
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
  iEvent.put(myDataFlightPathSignificance, "flightPathSignificance");
  iEvent.put(myDataFlightPathTransverseLength, "flightPathTransverseLength");
  iEvent.put(myDataFlightPathTransverseSignificance, "flightPathTransverseSignificance");
  // Invariant mass related
  iEvent.put(myDataInvariantMassFromTracksOnly, "invariantMassFromTracksOnly");
  iEvent.put(myDataInvariantMassFull, "invariantMassFull");
  // PF specific
  iEvent.put(myDataPFElectronPreIDOutput, "PFElectronPreIDOutput");
  iEvent.put(myDataPFElectronPreIDDecision, "PFElectronPreIDDecision");
  iEvent.put(myDataPFNeutralHadronET, "PFNeutralHadronET");
  iEvent.put(myDataPFGammaET, "PFGammaET");
  iEvent.put(myDataPFElectronET, "PFElectronET");
  // Discriminators
  for (size_t j = 0; j < myDiscriminatorCount; ++j) {
    std::auto_ptr<std::vector<float> > myDiscriminatorValues(new std::vector<float>);
    for (std::vector<reco::PFTauRef>::const_iterator it = mySelectedPFTauRefs.begin(); it != mySelectedPFTauRefs.end(); ++it) {
      myDiscriminatorValues->push_back((*myDiscriminatorHandles[j])[*it]);
    }
    iEvent.put(myDiscriminatorValues, fTauDiscriminators[j].label());
  }
  // Other
  iEvent.put(myDataPV, "primaryVertex");
  
  myDiscriminatorHandles.clear();
  return true;
}

  reco::Vertex HPlusTauDumperPF::threeProng(reco::PFTauRef myPFTau, edm::Event& myEvent, const edm::EventSetup& myEvtSetup) {
    
    // Primary vertex
    reco::Vertex primaryVertex;
    edm::Handle<edm::View<reco::Vertex> > vertexHandle;
    myEvent.getByLabel("offlinePrimaryVertices", vertexHandle);
    const edm::View<reco::Vertex>& vertexCollection(*vertexHandle);
    primaryVertex = *(vertexCollection.begin());
    
    // Secondary Vertex
    reco::Vertex secondaryVertex; 
    
    // Transient Tracks
    edm::ESHandle<TransientTrackBuilder> myTransientTrackBuilder; // create a handle for the transient track builder
    myEvtSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",myTransientTrackBuilder); // attach collection to handle
    const TransientTrackBuilder *TransientTrackBuilder_ = myTransientTrackBuilder.product();
    
    // Get hadrons reference vector
    reco::PFCandidateRefVector hadrons = myPFTau->signalPFChargedHadrCands();
     // Get individual hadrons
     PFCandidateRef  h1  = hadrons.at(0);
     PFCandidateRef  h2  = hadrons.at(1);
     PFCandidateRef  h3  = hadrons.at(2);
  
     if(h1->trackRef().isNonnull() && h2->trackRef().isNonnull() && h3->trackRef().isNonnull() ) {
       // Make transient(extrapolated) tracks for each hadron
       std::vector<TransientTrack> transientTracks;

       transientTracks.push_back(TransientTrackBuilder_->build(h1->trackRef()));
       transientTracks.push_back(TransientTrackBuilder_->build(h2->trackRef()));
       transientTracks.push_back(TransientTrackBuilder_->build(h3->trackRef()));
       if(transientTracks.size() > 1){
	 // Apply the Vertex Fit 
	 KalmanVertexFitter fitter(true); // if true it returns the new, fitted Lorentz Vector
	 TransientVertex myVertex = fitter.vertex(transientTracks); 
	 
	 // Require a valid vertex and 3 refitted tracks
	 if(myVertex.isValid() && myVertex.hasRefittedTracks() && myVertex.refittedTracks().size()==3) {
	   
	   // response=true;
	   math::XYZPoint vtx(myVertex.position().x(),myVertex.position().y(),myVertex.position().z());
	   
	   // Create a TLorentzVector for each refitted track
	   math::XYZTLorentzVector p1(myVertex.refittedTracks().at(0).track().px(),
				      myVertex.refittedTracks().at(0).track().py(),
				      myVertex.refittedTracks().at(0).track().pz(),
				      sqrt(myVertex.refittedTracks().at(0).track().momentum().mag2() +0.139*0.139));
	   
	   math::XYZTLorentzVector p2(myVertex.refittedTracks().at(1).track().px(),
				      myVertex.refittedTracks().at(1).track().py(),
				      myVertex.refittedTracks().at(1).track().pz(),
				      sqrt(myVertex.refittedTracks().at(1).track().momentum().mag2() +0.139*0.139));
	   
	   math::XYZTLorentzVector p3(myVertex.refittedTracks().at(2).track().px(),
				      myVertex.refittedTracks().at(2).track().py(),
				      myVertex.refittedTracks().at(2).track().pz(),
				      sqrt(myVertex.refittedTracks().at(2).track().momentum().mag2() +0.139*0.139));

	   secondaryVertex = myVertex;
	   
	   // Update the myPFTau p4
	   // myPFTau->setP4(p1+p2+p3); // need a PFTau and NOT a PFTauRef
	   // Update the vertex
	   // myPFTau->setVertex(vtx);   // need a PFTau and NOT a PFTauRef
	 }
       }
     }
     return secondaryVertex;
  }

  

  reco::Vertex HPlusTauDumperPF::fiveProng(reco::PFTauRef myPFTau, edm::Event& myEvent, const edm::EventSetup& myEvtSetup) {
    
    // Primary vertex
    reco::Vertex primaryVertex;
    edm::Handle<edm::View<reco::Vertex> > vertexHandle;
    myEvent.getByLabel("offlinePrimaryVertices", vertexHandle);
    const edm::View<reco::Vertex>& vertexCollection(*vertexHandle);
    primaryVertex = *(vertexCollection.begin());
    
    // Secondary Vertex
    reco::Vertex secondaryVertex; 
    
    // Transient Tracks
    edm::ESHandle<TransientTrackBuilder> myTransientTrackBuilder; // create a handle for the transient track builder
    myEvtSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",myTransientTrackBuilder); // attach collection to handle
    const TransientTrackBuilder *TransientTrackBuilder_ = myTransientTrackBuilder.product();
    
    // Get hadrons reference vector
    reco::PFCandidateRefVector hadrons = myPFTau->signalPFChargedHadrCands();
    // Get individual hadrons   
    PFCandidateRef  h1  = hadrons.at(0);
    PFCandidateRef  h2  = hadrons.at(1);
    PFCandidateRef  h3  = hadrons.at(2);
    PFCandidateRef  h4  = hadrons.at(3);
    PFCandidateRef  h5  = hadrons.at(4);
    
    // Make transient(extrapolated) tracks for each hadron
    std::vector<TransientTrack> transientTracks;
    transientTracks.push_back(TransientTrackBuilder_->build(h1->trackRef()));
    transientTracks.push_back(TransientTrackBuilder_->build(h2->trackRef()));
    transientTracks.push_back(TransientTrackBuilder_->build(h3->trackRef()));
    transientTracks.push_back(TransientTrackBuilder_->build(h4->trackRef()));
    transientTracks.push_back(TransientTrackBuilder_->build(h5->trackRef()));
    
    // Apply the Vertex Fit 
    KalmanVertexFitter fitter(true);    // if true it returns the new, fitted Lorentz Vector
    
    TransientVertex myVertex = fitter.vertex(transientTracks); 
    
    // Require a valid vertex and 5 refitted tracks
    if(myVertex.isValid() && myVertex.hasRefittedTracks() && myVertex.refittedTracks().size()==5) {
      
      // response=true;
      math::XYZPoint vtx(myVertex.position().x(),myVertex.position().y(),myVertex.position().z());
      
      // Create a TLorentzVector for each refitted track
      math::XYZTLorentzVector p1(myVertex.refittedTracks().at(0).track().px(),
				myVertex.refittedTracks().at(0).track().py(),
				myVertex.refittedTracks().at(0).track().pz(),
				sqrt(myVertex.refittedTracks().at(0).track().momentum().mag2() +0.139*0.139));
      
      math::XYZTLorentzVector p2(myVertex.refittedTracks().at(1).track().px(),
				myVertex.refittedTracks().at(1).track().py(),
				myVertex.refittedTracks().at(1).track().pz(),
				sqrt(myVertex.refittedTracks().at(1).track().momentum().mag2() +0.139*0.139));
      
      math::XYZTLorentzVector p3(myVertex.refittedTracks().at(2).track().px(),
				myVertex.refittedTracks().at(2).track().py(),
				myVertex.refittedTracks().at(2).track().pz(),
				sqrt(myVertex.refittedTracks().at(2).track().momentum().mag2() +0.139*0.139));
      
      math::XYZTLorentzVector p4(myVertex.refittedTracks().at(3).track().px(),
				myVertex.refittedTracks().at(3).track().py(),
				myVertex.refittedTracks().at(3).track().pz(),
				sqrt(myVertex.refittedTracks().at(3).track().momentum().mag2() +0.139*0.139));
      
      math::XYZTLorentzVector p5(myVertex.refittedTracks().at(4).track().px(),
				myVertex.refittedTracks().at(4).track().py(),
				myVertex.refittedTracks().at(4).track().pz(),
				sqrt(myVertex.refittedTracks().at(4).track().momentum().mag2() +0.139*0.139));
      
      secondaryVertex = myVertex;
      
      // Update the myPFTau p4
      // myPFTau->setP4(p1+p2+p3); // need a PFTau and NOT a PFTauRef
      // Update the vertex
      // myPFTau->setVertex(vtx);   // need a PFTau and NOT a PFTauRef
    }
    return secondaryVertex;
}
  
  
} //eof: namespace HPlusAnalysis {
