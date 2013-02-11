#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
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

std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);

namespace HPlus {
  GlobalElectronVeto::Data::Data():
    fPassedEvent(false),
    fSelectedElectronPt(0.),
    fSelectedElectronEta(0.),
    fSelectedElectronPtBeforePtCut(0.) { }
  GlobalElectronVeto::Data::~Data() {}

  GlobalElectronVeto::GlobalElectronVeto(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fElecCollectionName(iConfig.getUntrackedParameter<edm::InputTag>("ElectronCollectionName")),
    fVertexSrc(vertexSrc),
    fConversionSrc(iConfig.getUntrackedParameter<edm::InputTag>("conversionSrc")),
    fBeamspotSrc(iConfig.getUntrackedParameter<edm::InputTag>("beamspotSrc")),
    fRhoSrc(iConfig.getUntrackedParameter<edm::InputTag>("rhoSrc")),
    fElecSelection(iConfig.getUntrackedParameter<std::string>("ElectronSelection")),
    fElecPtCut(iConfig.getUntrackedParameter<double>("ElectronPtCut")),
    fElecEtaCut(iConfig.getUntrackedParameter<double>("ElectronEtaCut")),
    fElecSelectionSubCountAllEvents(eventCounter.addSubCounter("GlobalElectron Selection", "All events")),
    fElecSelectionSubCountElectronPresent(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Present")),
    fElecSelectionSubCountElectronHasGsfTrkOrTrk(eventCounter.addSubCounter("GlobalElectron Selection", "Electron has gsfTrack or track")),
    fElecSelectionSubCountFiducialVolumeCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron fiducial volume")),
    fElecSelectionSubCountId(eventCounter.addSubCounter("GlobalElectron Selection", "Electron ID")),
    fElecSelectionSubCountEtaCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Eta")),
    fElecSelectionSubCountPtCut(eventCounter.addSubCounter("GlobalElectron Selection", "Electron Pt " )),
    fElecSelectionSubCountSelected(eventCounter.addSubCounter("GlobalElectron Selection", "Electron selected")),
    fElecSelectionSubCountMatchingMCelectron(eventCounter.addSubCounter("GlobalElectron Selection","Electron matching MC electron")),
    fElecSelectionSubCountMatchingMCelectronFromW(eventCounter.addSubCounter("GlobalElectron Selection","Electron matching MC electron From W"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("GlobalElectronVeto");

    hElectronPt  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt", "GlobalElectronPt;isolated electron p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 160, 0.0, 400.0);
    hElectronEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronEta", "GlobalElectronEta;isolated electron #eta;N_{electrons} / 0.1", 90, -3.0, 3.0);
    hElectronEta_identified = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalElectronEta_identified", "GlobalElectronEta_identified;isolated electron #eta;N_{electrons} / 0.1", 90, -3.0, 3.0);
    hElectronPt_identified  = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "GlobalElectronPt_identified", "GlobalElectronPt;isolated electron p_{T}, GeV/c;N_{electrons} / 5 GeV/c", 160, 0, 400.0);
    hNumberOfSelectedElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NumberOfSelectedElectrons", "NumberOfSelectedElectrons", 30, 0., 30.);
    hElectronPt_matchingMCelectron  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_matchingMCelectron", "GlobalElectronPt_matchingMCelectron", 160, 0.0, 400.0);
    hElectronEta_matchingMCelectron = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronEta_matchingMCelectron", "GlobalElectronEta_matchingMCelectron", 90, -3.0, 3.0);
    hElectronPt_matchingMCelectronFromW  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_matchingMCelectronFromW", "GlobalElectronPt_matchingMCelectronFromW", 160, 0.0, 400.0);
    hElectronEta_matchingMCelectronFromW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronEta_matchingMCelectronFromW", "GlobalElectronEta_matchingMCelectronFromW", 90, -3.0, 3.0);
    hElectronPt_gsfTrack  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_gsfTrack", "GlobalElectronPt_gsfTrack", 160, 0.0, 400.0);
    hElectronEta_gsfTrack = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronEta_gsfTrack", "GlobalElectronEta_gsfTrack", 90, -3.0, 3.0);
    hElectronEta_superCluster = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronEta_superCluster", "GlobalElectronEta_superCluster", 60, -3.0, 3.0);
    hElectronPt_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_AfterSelection", "GlobalElectronPt_AfterSelection", 160, 0.0, 400.0);
    hElectronEta_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_AfterSelection", "GlobalElectronEta_AfterSelection", 90, -3.0, 3.0);
    hElectronPt_gsfTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_gsfTrack_AfterSelection", "GlobalElectronPt_gsfTrack_AfterSelection", 160, 0.0, 400.0);
    hElectronEta_gsfTrack_AfterSelection = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "GlobalElectronPt_gsfTrack_AfterSelection", "GlobalElectronPt_gsTrack_AfterSelection", 90, -3.0, 3.0);
    hElectronImpactParameter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ElectronImpactParameter", "ElectronImpactParameter", 100, 0.0, 0.1);

    hElectronEtaPhiForSelectedElectrons = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "ElectronEtaPhiForSelectedElectrons", "ElectronEtaPhiForSelectedElectrons;electron #eta; electronu #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);
    hMCElectronEtaPhiForPassedEvents = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
        "MCElectronEtaPhiForPassedEvents", "MCElectronEtaPhiForPassedEvents;MC electron #eta; MC electronu #phi",
        60, -3.0, 3.0, 72, -3.14159265, 3.14159265);

    // Check Whether official eID will be applied
    if (fElecSelection == "VETO") fElectronIdEnumerator = EgammaCutBasedEleId::VETO;
    else{
      throw cms::Exception("Error") << "The ElectronSelection \"" << fElecSelection << "\" used as input in the python config file is invalid!\nPlease choose one of the following valid options:" << std::endl
				    << "'VETO'" << std::endl;
    }
  }

  GlobalElectronVeto::~GlobalElectronVeto() {}

  GlobalElectronVeto::Data GlobalElectronVeto::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup);
  }

  GlobalElectronVeto::Data GlobalElectronVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup);
  }

  GlobalElectronVeto::Data GlobalElectronVeto::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    Data output;

    edm::Handle<edm::View<pat::Electron> > myElectronHandle;
    iEvent.getByLabel(fElecCollectionName, myElectronHandle);
    edm::PtrVector<pat::Electron> electrons = myElectronHandle->ptrVector();

    increment(fElecSelectionSubCountAllEvents);
    // In the case where the Electron Collection handle is empty...
    if ( !myElectronHandle->size() ) {
      output.fPassedEvent = true;
      return output;
    }

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles); // FIXME: bad habbit to hard-code InputTags

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
    float myHighestElecPtBeforePtCut = -1.0;
    float myHighestElecEta = -999.99;
    // 
    bool bElecPresent = false;
    bool bElecHasGsfTrkOrTrk = false;
    bool bElecFiducialVolumeCut  = false;
    bool bPassedElecID = false;
    bool bElecPtCut = false;
    bool bElecEtaCut = false;

    bool bElectronSelected = false;

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

      // Fill histos with all-Electrons Pt and Eta
      hElectronPt->Fill(myElectronPt);
      hElectronEta->Fill(myElectronEta);
      hElectronPt_gsfTrack->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack->Fill(myGsfTrackRef->eta());

      // Apply electron fiducial volume cut
      // Obtain reference to the superCluster
      reco::SuperClusterRef mySuperClusterRef = (*iElectron)->superCluster();

      // Check that superCluster was found
      if ( mySuperClusterRef.isNull()) continue;

      hElectronEta_superCluster->Fill(mySuperClusterRef->eta());

      if ( fabs(mySuperClusterRef->eta()) > 1.4442 && fabs(mySuperClusterRef->eta()) < 1.566) continue;
      bElecFiducialVolumeCut = true;

      // 1) Apply Electron ID (choose low efficiency => High Purity)

      bPassedElecID = EgammaCutBasedEleId::PassWP(fElectronIdEnumerator, **iElectron, hConversion, *hBeamspot, hVertex,
                                                  (*iElectron)->chargedHadronIso(), (*iElectron)->photonIso(), (*iElectron)->neutralHadronIso(),
                                                  *hRho);
      //std::cout << "Electron " << (iElectron-electrons.begin()) << "/" << electrons.size() << ": pass veto: " << bVeto << std::endl;
      if(!bPassedElecID) continue;
      output.fSelectedElectronsBeforePtAndEtaCuts.push_back(*iElectron);

      hElectronEta_identified->Fill(myElectronEta);

      if(std::abs(myElectronEta) < fElecEtaCut) {
        myHighestElecPtBeforePtCut = std::max(myHighestElecPtBeforePtCut, myElectronPt);
      hElectronPt_identified->Fill(myElectronPt);
      }

      // 2) Apply Eta cut requirement
      if (std::abs(myElectronEta) >= fElecEtaCut) continue;
      bElecEtaCut = true;
      if (myElectronPt > output.fSelectedElectronPtBeforePtCut)
        output.fSelectedElectronPtBeforePtCut = myElectronPt;

      // 3) Apply Pt cut requirement
      if (myElectronPt < fElecPtCut) continue;
      bElecPtCut = true;

      output.fSelectedElectrons.push_back(*iElectron);

      // If Electron survives all cuts (1->3) then it is considered an isolated Electron. Now find the max Electron Pt.
      if (myElectronPt > myHighestElecPt) {
        myHighestElecPt = myElectronPt;
        myHighestElecEta = myElectronEta;
      }
      bElectronSelected = true;
      // Fill histos after Selection
      hElectronPt_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronEta_AfterSelection->Fill(myGsfTrackRef->eta());
      hElectronPt_gsfTrack_AfterSelection->Fill(myGsfTrackRef->pt());
      hElectronEta_gsfTrack_AfterSelection->Fill(myGsfTrackRef->eta());
      hElectronEtaPhiForSelectedElectrons->Fill((*iElectron)->eta(), (*iElectron)->phi());

      bool bElecMatchingMCelectron = false;
      bool bElecMatchingMCelectronFromW = false;
      // Selection purity from MC
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < genParticles->size(); ++i){  
          const reco::Candidate & p = (*genParticles)[i];
          const reco::Candidate & electron = (**iElectron);
          int status = p.status();
          double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() , electron.p4() );
          if ( deltaR > 0.05 || status != 1) continue;
          int id = p.pdgId();
          if ( std::abs(id) == 11 ) {
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
    if(bElecPresent) {
      increment(fElecSelectionSubCountElectronPresent);
      if(bElecHasGsfTrkOrTrk) { 
        increment(fElecSelectionSubCountElectronHasGsfTrkOrTrk);
        if(bElecFiducialVolumeCut) {
          increment(fElecSelectionSubCountFiducialVolumeCut);
          if(bPassedElecID) {
            increment(fElecSelectionSubCountId);
            if(bElecEtaCut) {
              increment(fElecSelectionSubCountEtaCut);
              if(bElecPtCut) {
                increment(fElecSelectionSubCountPtCut);
                increment(fElecSelectionSubCountSelected);
		/*
		if(bElecMatchingMCelectron) {
		  increment(fElecSelectionSubCountMatchingMCelectron);
		  if(bElecMatchingMCelectronFromW) {
		    increment(fElecSelectionSubCountMatchingMCelectronFromW);
		  }
		}
		*/
	      }
            }
          }
        }
      }
    }
    

    hNumberOfSelectedElectrons->Fill(output.fSelectedElectrons.size());

    // Now store the highest Electron Pt and Eta
    output.fSelectedElectronPt = myHighestElecPt;
    output.fSelectedElectronEta = myHighestElecEta;

    // If a Global Electron (passing all selection criteria) is found, do not increment counter. Return false.
    if(bElectronSelected) {
      output.fPassedEvent = false;
      return output;
    } else {
      // Otherwise increment counter and return true.
      output.fPassedEvent = true;
      if(!iEvent.isRealData()) {
        for (size_t i=0; i < genParticles->size(); ++i) {
          const reco::Candidate & p = (*genParticles)[i];
          if (p.status() != 1) continue;
          if (std::abs(p.pdgId()) != 11) continue;
          if (p.pt() < fElecPtCut) continue;
          // Plot eta-phi map of MC electrons above pT threshold
          hMCElectronEtaPhiForPassedEvents->Fill(p.eta(), p.phi());
        }
      }
    }

    return output;
  }

}
