#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "Math/GenVector/VectorUtil.h"

#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <string>

namespace HPlus {
  ElectronSelection::Data::Data():
    fSelectedElectronPt(0.),
    fSelectedElectronEta(0.),
    fSelectedElectronPtBeforePtCut(-1.),
    fHasElectronFromCjetStatus(false),
    fHasElectronFromBjetStatus(false) { }
  ElectronSelection::Data::~Data() {}

  ElectronSelection::ElectronSelection(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fGenParticleSrc(iConfig.getUntrackedParameter<edm::InputTag>("genParticleSrc")),
    fElecCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("ElectronCollectionName")),
    fVertexSrc(vertexSrc),
    fConversionSrc(iConfig.getUntrackedParameter<edm::InputTag>("conversionSrc")),
    fBeamspotSrc(iConfig.getUntrackedParameter<edm::InputTag>("beamspotSrc")),
    fRhoSrc(iConfig.getUntrackedParameter<edm::InputTag>("rhoSrc")),
    fElecSelectionVeto(iConfig.getUntrackedParameter<std::string>("ElectronSelectionVeto")),
    fElecSelectionMedium(iConfig.getUntrackedParameter<std::string>("ElectronSelectionMedium")),
    fElecSelectionTight(iConfig.getUntrackedParameter<std::string>("ElectronSelectionTight")),
    fElecPtCut(iConfig.getUntrackedParameter<double>("ElectronPtCut")),
    fElecEtaCut(iConfig.getUntrackedParameter<double>("ElectronEtaCut")),
    fElecSelectionSubCountAllEvents(eventCounter.addSubCounter("ElectronSelection", "All events")),
    fElecSelectionSubCountElectronPresent(eventCounter.addSubCounter("ElectronSelection", "Electron Present")),
    fElecSelectionSubCountElectronHasGsfTrkOrTrk(eventCounter.addSubCounter("ElectronSelection", "Electron has gsfTrack or track")),
    fElecSelectionSubCountFiducialVolumeCut(eventCounter.addSubCounter("ElectronSelection", "Electron fiducial volume")),
    fElecSelectionSubCountId(eventCounter.addSubCounter("ElectronSelection", "Electron ID")),
    fElecSelectionSubCountEtaCut(eventCounter.addSubCounter("ElectronSelection", "Electron Eta")),
    fElecSelectionSubCountPtCut(eventCounter.addSubCounter("ElectronSelection", "Electron Pt")),
    fElecSelectionSubCountSelectedVeto(eventCounter.addSubCounter("ElectronSelection", "Veto electron selected")),
    fElecSelectionSubCountMatchingMCelectron(eventCounter.addSubCounter("ElectronSelection","Electron matching MC electron")),
    fElecSelectionSubCountMatchingMCelectronFromW(eventCounter.addSubCounter("ElectronSelection","Electron matching MC electron From W")),
    fElecSelectionSubCountSelectedMedium(eventCounter.addSubCounter("ElectronSelection", "Medium electron selected")),
    fElecSelectionSubCountSelectedTight(eventCounter.addSubCounter("ElectronSelection", "Tight electron selected")),
    fElecSelectionSubCountPassedVeto(eventCounter.addSubCounter("ElectronSelection", "Electron veto passed")),
    fElecSelectionSubCountPassedVetoAndElectronFromCjet(eventCounter.addSubCounter("ElectronSelection", "Electron veto passed and e in c jet")),
    fElecSelectionSubCountPassedVetoAndElectronFromBjet(eventCounter.addSubCounter("ElectronSelection", "Electron veto passed and e in b jet"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, "ElectronSelection");

    hElectronPt_all  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_all", "ElectronPt_all;electron candidates p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 80, 0.0, 400.0);
    hElectronEta_all = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_all", "ElectronEta_all;electron candiates #eta;N_{electrons} / 0.1", 60, -3.0, 3.0);
    hElectronPt_gsfTrack_all = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_gsfTrack", "ElectronPt_gsfTrack;electron candidates p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 80, 0.0, 400.0);
    hElectronEta_gsfTrack_all = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_gsfTrack", "ElectronEta_gsfTrack;electron candidates #eta;N_{electrons}", 60, -3.0, 3.0);
    hElectronEta_superCluster = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_superCluster", "ElectronEta_superCluster", 60, -3.0, 3.0);
    hElectronEta_veto = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_veto", "ElectronEta_veto;veto electron #eta;N_{electrons} / 0.1", 60, -3.0, 3.0);
    hElectronPt_veto = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_veto", "ElectronPt_veto;veto electron p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 80, 0, 400.0);
    hNumberOfVetoElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfVetoElectrons", "NumberOfVetoElectrons;N_{veto electrons};N_{electrons}", 30, 0., 30.);
    hElectronPt_matchingMCelectron  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_matchingMCelectron", "ElectronPt_matchingMCelectron", 80, 0.0, 400.0);
    hElectronEta_matchingMCelectron = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_matchingMCelectron", "ElectronEta_matchingMCelectron", 60, -3.0, 3.0);
    hElectronPt_matchingMCelectronFromW  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_matchingMCelectronFromW", "ElectronPt_matchingMCelectronFromW", 80, 0.0, 400.0);
    hElectronEta_matchingMCelectronFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_matchingMCelectronFromW", "ElectronEta_matchingMCelectronFromW", 60, -3.0, 3.0);
    
    hElectronPt_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_AfterSelection", "ElectronPt_AfterSelection", 80, 0.0, 400.0);
    hElectronEta_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_AfterSelection", "ElectronEta_AfterSelection", 60, -3.0, 3.0);
    hElectronPt_gsfTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_gsfTrack_AfterSelection", "ElectronPt_gsfTrack_AfterSelection", 80, 0.0, 400.0);
    hElectronEta_gsfTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_gsfTrack_AfterSelection", "ElectronPt_gsTrack_AfterSelection", 60, -3.0, 3.0);

    hElectronEtaPhiForSelectedElectrons = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "ElectronEtaPhiForSelectedElectrons", "ElectronEtaPhiForSelectedElectrons;electron #eta; electron #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);
    hMCElectronEtaPhiForPassedEvents = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "MCElectronEtaPhiForPassedEvents", "MCElectronEtaPhiForPassedEvents;MC electron #eta; MC electron #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);

    hElectronEta_medium = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_medium", "ElectronEta_medium;medium electron #eta;N_{electrons} / 0.1", 60, -3.0, 3.0);
    hElectronPt_medium = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_medium", "ElectronPt_medium;medium electron p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 80, 0, 400.0);
    hNumberOfMediumElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfMediumElectrons", "NumberOfMediumElectrons;N_{medium electrons};N_{electrons}", 30, 0., 30.);

    hElectronEta_tight = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronEta_tight", "ElectronEta_tight;tight electron #eta;N_{electrons} / 0.1", 60, -3.0, 3.0);
    hElectronPt_tight = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronPt_tight", "ElectronPt_tight;tight electron p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 80, 0, 400.0);
    hNumberOfTightElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfTightElectrons", "NumberOfTightElectrons;N_{tight electrons};N_{electrons}", 30, 0., 30.);

    // Check Whether official eID will be applied
    fElectronIdEnumeratorVeto = translateWorkingPoint(fElecSelectionVeto);
    fElectronIdEnumeratorMedium = translateWorkingPoint(fElecSelectionMedium);
    fElectronIdEnumeratorTight = translateWorkingPoint(fElecSelectionTight);
  }

  ElectronSelection::~ElectronSelection() {}

  ElectronSelection::Data ElectronSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  ElectronSelection::Data ElectronSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  ElectronSelection::Data ElectronSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;

    edm::Handle<edm::View<pat::Electron> > myElectronHandle;
    iEvent.getByLabel(fElecCollectionName, myElectronHandle);
    edm::PtrVector<pat::Electron> electrons = myElectronHandle->ptrVector();

    increment(fElecSelectionSubCountAllEvents);

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel(fGenParticleSrc, genParticles);

    // Get Conversions, Vertices, BeamSpot, and Rho
    edm::Handle<reco::ConversionCollection> hConversion;
    iEvent.getByLabel(fConversionSrc, hConversion);
    edm::Handle<reco::VertexCollection> hVertex;
    iEvent.getByLabel(fVertexSrc, hVertex);
    edm::Handle<reco::BeamSpot> hBeamspot;
    iEvent.getByLabel(fBeamspotSrc, hBeamspot);
    edm::Handle<double> hRho;
    iEvent.getByLabel(fRhoSrc, hRho);

    // Reset/initialise variables
    float myHighestElecPt = -1.0;
    float myHighestElecEta = -999.99;
    // 
    bool bElecPresent = false;
    bool bElecHasGsfTrkOrTrk = false;
    bool bElecFiducialVolumeCut  = false;
    bool bPassedElecID = false;
    bool bElecPtCut = false;
    bool bElecEtaCut = false;
    bool bElectronSelected = false;
    bool bElecMatchingMCelectron = false;
    bool bElecMatchingMCelectronFromW = false;

    // Cache MC electrons to speed up code (only one loop over gen particles)
    std::vector<const reco::GenParticle*> myMCElectrons;
    if(!iEvent.isRealData()) {
      for (size_t i=0; i < genParticles->size(); ++i){  
        if ((*genParticles)[i].status() != 1) continue;
        if (std::abs((*genParticles)[i].pdgId()) != 11) continue;
        myMCElectrons.push_back(&((*genParticles)[i]));
      }
    }

    // Loop over all Electrons
    for(edm::PtrVector<pat::Electron>::const_iterator iElectron = electrons.begin(); iElectron != electrons.end(); ++iElectron) {
      // keep track of the electrons analyzed
      bElecPresent = true;
      // Obtain reference to an Electron track
      reco::GsfTrackRef myGsfTrackRef = (*iElectron)->gsfTrack(); // gsfElecs were selected to create the current PatTuples

      // Check that track was found
      if (myGsfTrackRef.isNull()) continue;
      bElecHasGsfTrkOrTrk = true;

      // Electron Variables (Pt, Eta etc..)
      float myElectronPt  = (*iElectron)->pt();
      float myElectronEta = (*iElectron)->eta();
      // float myElectronPhi = (*iElectron)->phi();

      // Apply electron fiducial volume cut
      // Obtain reference to the superCluster
      reco::SuperClusterRef mySuperClusterRef = (*iElectron)->superCluster();

      // Check that superCluster was found
      if ( mySuperClusterRef.isNull()) continue;

      hElectronEta_superCluster->Fill(mySuperClusterRef->eta());

      if ( std::fabs(mySuperClusterRef->eta()) > 1.4442 && std::fabs(mySuperClusterRef->eta()) < 1.566) continue;
      bElecFiducialVolumeCut = true;

      // Fill histos with all-Electrons Pt and Eta
      hElectronPt_all->Fill(myElectronPt);
      hElectronEta_all->Fill(myElectronEta);
      hElectronPt_gsfTrack_all->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack_all->Fill(myGsfTrackRef->eta());

      // 1) Apply Electron ID
      
      bool myVetoIdStatus = EgammaCutBasedEleId::PassWP(fElectronIdEnumeratorVeto, **iElectron, hConversion, *hBeamspot, hVertex,
                                                        (*iElectron)->chargedHadronIso(), (*iElectron)->photonIso(), (*iElectron)->neutralHadronIso(),
                                                        *hRho);
      bool myMediumIdStatus = EgammaCutBasedEleId::PassWP(fElectronIdEnumeratorMedium, **iElectron, hConversion, *hBeamspot, hVertex,
                                                          (*iElectron)->chargedHadronIso(), (*iElectron)->photonIso(), (*iElectron)->neutralHadronIso(),
                                                          *hRho);
      bool myTightIdStatus = EgammaCutBasedEleId::PassWP(fElectronIdEnumeratorTight, **iElectron, hConversion, *hBeamspot, hVertex,
                                                         (*iElectron)->chargedHadronIso(), (*iElectron)->photonIso(), (*iElectron)->neutralHadronIso(),
                                                         *hRho);
      bool myEtaStatus = std::fabs(myElectronEta) < fElecEtaCut;
      bool myPtStatus = myElectronPt > fElecPtCut;
      
      // Look at tight electrons
      if (myTightIdStatus) {
        hElectronEta_tight->Fill(myElectronEta);
        if (myEtaStatus) {
          hElectronPt_tight->Fill(myElectronPt);
          if (myPtStatus) {
            output.fSelectedElectronsTight.push_back(*iElectron);
          }
        }
      }
      // Look at medium electrons
      if (myMediumIdStatus) {
        hElectronEta_medium->Fill(myElectronEta);
        if (myEtaStatus) {
          hElectronPt_medium->Fill(myElectronPt);
          if (myPtStatus) {
            output.fSelectedElectronsMedium.push_back(*iElectron);
          }
        }
      }
      // Look at electrons that did not pass the loosest isolation
      if (!myVetoIdStatus && !myMediumIdStatus && !myTightIdStatus) {
        output.fSelectedNonIsolatedElectrons.push_back(*iElectron);
      }

      if (!myVetoIdStatus) continue;
      bPassedElecID = true;
      output.fSelectedElectronsBeforePtAndEtaCuts.push_back(*iElectron);
      hElectronEta_veto->Fill(myElectronEta);

      // 2) Apply Eta cut requirement
      if (std::abs(myElectronEta) >= fElecEtaCut) continue;
      bElecEtaCut = true;
      output.fSelectedElectronPtBeforePtCut = std::max(output.fSelectedElectronPtBeforePtCut, myElectronPt);
      hElectronPt_veto->Fill(myElectronPt);

      // 3) Apply Pt cut requirement
      if (myElectronPt < fElecPtCut) continue;
      bElecPtCut = true;
      output.fSelectedElectronsVeto.push_back(*iElectron);

      // If Electron survives all cuts (1->3) then it is considered an isolated Electron. Now find the max Electron Pt.
      if (myElectronPt > myHighestElecPt) {
        myHighestElecPt = myElectronPt;
        myHighestElecEta = myElectronEta;
      }
      bElectronSelected = true;
      // Fill histos after Selection
      hElectronPt_AfterSelection->Fill(myElectronPt);
      hElectronEta_AfterSelection->Fill(myElectronEta);
      hElectronPt_gsfTrack_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack_AfterSelection->Fill(myGsfTrackRef->eta());
      hElectronEtaPhiForSelectedElectrons->Fill((*iElectron)->eta(), (*iElectron)->phi());

      // Selection purity from MC
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < myMCElectrons.size(); ++i) {
          const reco::Candidate & p = *(myMCElectrons[i]);
          const reco::Candidate & electron = (**iElectron);
          double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() , electron.p4() );
          if ( deltaR > 0.05) continue;
          bElecMatchingMCelectron = true;

          std::vector<const reco::GenParticle*> mothers = getMothers(p);
          for(size_t d=0; d<mothers.size(); ++d) {
            const reco::GenParticle dparticle = *mothers[d];
            int idmother = dparticle.pdgId();
            if ( abs(idmother) == 24 ) {
              bElecMatchingMCelectronFromW = true;
            }
          }
        }
	if ( bElecMatchingMCelectron ) {
	  hElectronPt_matchingMCelectron->Fill(myGsfTrackRef->pt());
	  hElectronEta_matchingMCelectron->Fill(myGsfTrackRef->eta());
	  if ( bElecMatchingMCelectronFromW ) {
	    hElectronPt_matchingMCelectronFromW->Fill(myGsfTrackRef->pt());
	    hElectronEta_matchingMCelectronFromW->Fill(myGsfTrackRef->eta());
	  }
	}	
      }
    }//eof: for(pat::ElectronCollection::const_iterator iElectron = myElectronHandle->begin(); iElectron != myElectronHandle->end(); ++iElectron) {
    if(bElecPresent) increment(fElecSelectionSubCountElectronPresent);
    if(bElecHasGsfTrkOrTrk) increment(fElecSelectionSubCountElectronHasGsfTrkOrTrk);
    if(bElecFiducialVolumeCut) increment(fElecSelectionSubCountFiducialVolumeCut);
    if(bPassedElecID) increment(fElecSelectionSubCountId);
    if(bElecEtaCut) increment(fElecSelectionSubCountEtaCut);
    if(bElecPtCut) increment(fElecSelectionSubCountPtCut);
    if(output.fSelectedElectronsVeto.size()) increment(fElecSelectionSubCountSelectedVeto);
    if(bElecMatchingMCelectron) increment(fElecSelectionSubCountMatchingMCelectron);
    if(bElecMatchingMCelectronFromW) increment(fElecSelectionSubCountMatchingMCelectronFromW);
    if(output.fSelectedElectronsMedium.size()) increment(fElecSelectionSubCountSelectedMedium);
    if(output.fSelectedElectronsTight.size()) increment(fElecSelectionSubCountSelectedTight);

    hNumberOfVetoElectrons->Fill(output.fSelectedElectronsVeto.size());
    hNumberOfMediumElectrons->Fill(output.fSelectedElectronsMedium.size());
    hNumberOfTightElectrons->Fill(output.fSelectedElectronsTight.size());

    // Now store the highest Electron Pt and Eta
    output.fSelectedElectronPt = myHighestElecPt;
    output.fSelectedElectronEta = myHighestElecEta;

    // Look further at MC electrons
    if(!iEvent.isRealData()) {
      for (size_t i=0; i < myMCElectrons.size(); ++i) {
        const reco::Candidate & p = (*genParticles)[i];
        if (p.pt() < fElecPtCut) continue;
        // Plot eta-phi map of MC electrons above pT threshold if event passed electron veto
        if (output.passedElectronVeto())
          hMCElectronEtaPhiForPassedEvents->Fill(p.eta(), p.phi());
        if (std::fabs(p.eta()) > fElecEtaCut) continue;
        // Check if there are MC electrons in the acceptance coming from b or c quarks
        const reco::Candidate* pmother = p.mother();
        while (pmother) {
          if (std::abs(pmother->pdgId()) == 4)
            output.fHasElectronFromBjetStatus = true;
          else if (std::abs(pmother->pdgId()) == 5)
            output.fHasElectronFromCjetStatus = true;
          // move to next
          pmother = pmother->mother();
        }
      }
    }

    if (output.passedElectronVeto()) {
      increment(fElecSelectionSubCountPassedVeto);
      if (output.eventContainsElectronFromCJet())
        increment(fElecSelectionSubCountPassedVetoAndElectronFromCjet);
      if (output.eventContainsElectronFromBJet())
        increment(fElecSelectionSubCountPassedVetoAndElectronFromBjet);
    }

    return output;
  }

  EgammaCutBasedEleId::WorkingPoint ElectronSelection::translateWorkingPoint(const std::string& wp) {
    if (wp == "VETO")
      return EgammaCutBasedEleId::VETO;
    else if (wp == "TIGHT")
      return EgammaCutBasedEleId::TIGHT;
    else if (wp == "MEDIUM")
      return EgammaCutBasedEleId::MEDIUM;
    else if (wp == "LOOSE")
      return EgammaCutBasedEleId::LOOSE;
    else
      throw cms::Exception("Error") << "The ElectronSelection \"" << wp << "\" used as input in the python config file is invalid!\nPlease choose one of the following valid options:" << std::endl
                                    << "'VETO', 'LOOSE', 'MEDIUM', 'TIGHT'" << std::endl;
  }
}
