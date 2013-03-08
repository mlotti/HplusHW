#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/Handle.h"

namespace HPlus {
  METFilters::METFilters(const edm::ParameterSet& iConfig, EventCounter& eventCounter, const std::string& prefix):
    // Input items
    fBeamHaloFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("beamHaloSrc")),
    fBeamHaloFilterEnabled(iConfig.getUntrackedParameter<bool>("beamHaloEnabled")),
    fHBHENoiseFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterSrc")),
    fHBHENoiseFilterEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterEnabled")),
    fHBHENoiseFilterMETWGSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterMETWGSrc")),
    fHBHENoiseFilterMETWGEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterMETWGEnabled")),
    fTrackingFailureFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("trackingFailureFilterSrc")),
    fTrackingFailureFilterEnabled(iConfig.getUntrackedParameter<bool>("trackingFailureFilterEnabled")),
    fEcalDeadCellEventFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalDeadCellEventFilterSrc")),
    fEcalDeadCellEventFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalDeadCellEventFilterEnabled")),
    fEcalDeadCellTPFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalDeadCellTPFilterSrc")),
    fEcalDeadCellTPFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalDeadCellTPFilterEnabled")),
    fTriggerResultsSrc(iConfig.getUntrackedParameter<edm::InputTag>("triggerResultsSrc")),
    fHcalLaserFilterStrings(iConfig.getUntrackedParameter<std::vector<std::string> >("hcalLaserFilterStrings")),
    fHcalLaserFilterEnabled(iConfig.getUntrackedParameter<bool>("hcalLaserFilterEnabled")),
    fBadEESuperCrystalFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("badEESuperCrystalFilterSrc")),
    fBadEESuperCrystalFilterEnabled(iConfig.getUntrackedParameter<bool>("badEESuperCrystalFilterEnabled")),
    fEcalCrystalsWithLargeLaserCorrectionFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalCrystalsWithLargeLaserCorrectionFilterSrc")),
    fEcalCrystalsWithLargeLaserCorrectionFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalCrystalsWithLargeLaserCorrectionFilterEnabled")),
    fTrackingOddEventFilterStrings(iConfig.getUntrackedParameter<std::vector<std::string> >("trackingOddEventFilterStrings")),
    fTrackingOddEventFilterEnabled(iConfig.getUntrackedParameter<bool>("trackingOddEventFilterEnabled")),
    fMuonsWithWrongMomentaFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("muonsWithWrongMomentaFilterSrc")),
    fMuonsWithWrongMomentaFilterEnabled(iConfig.getUntrackedParameter<bool>("muonsWithWrongMomentaFilterEnabled")),
    fInconsistentMuonPFCandidateFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("inconsistentMuonPFCandidateFilterSrc")),
    fInconsistentMuonPFCandidateFilterEnabled(iConfig.getUntrackedParameter<bool>("inconsistentMuonPFCandidateFilterEnabled")),
    // Counters
    fAllEventCounter(eventCounter.addSubCounter(prefix, "All events")),
    fBeamHaloFilterCounter(eventCounter.addSubCounter(prefix, "Beam halo filter")),
    fHBHENoiseFilterCounter(eventCounter.addSubCounter(prefix, "HBHE Noise filter")),
    fHBHENoiseFilterMETWGCounter(eventCounter.addSubCounter(prefix, "HBHE METWG Noise filter")),
    fTrackingFailureFilterCounter(eventCounter.addSubCounter(prefix, "tracking Failure filter")),
    fEcalDeadCellEventFilterCounter(eventCounter.addSubCounter(prefix, "Ecal Dead Cell Event filter")),
    fEcalDeadCellTPFilterCounter(eventCounter.addSubCounter(prefix, "Ecal Dead Cell TP filter")),
    fHcalLaserFilterCounter(eventCounter.addSubCounter(prefix, "HCAL laser filter")),
    fBadEESuperCrystalFilterCounter(eventCounter.addSubCounter(prefix, "Bad EE supercrystal")),
    fEcalCrystalsWithLargeLaserCorrectionFilterCounter(eventCounter.addSubCounter(prefix, "ECAL cryst. with large corrections")),
    fTrackingOddEventFilterCounter(eventCounter.addSubCounter(prefix, "Tracking odd events")),
    fMuonsWithWrongMomentaFilterCounter(eventCounter.addSubCounter(prefix, "Muons with wrong momenta")),
    fInconsistentMuonPFCandidateFilterCounter(eventCounter.addSubCounter(prefix, "Inconsistent PF muons")),
    fAllPassedCounter(eventCounter.addSubCounter(prefix, "Passed all filters")),
    fTriggerResultsListPrintedStatus(false)
  {}
  METFilters::~METFilters() {}

  bool METFilters::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    if (!iEvent.isRealData()) return true;

    increment(fAllEventCounter);
    // Obtain trigger results object (some filters have been stored as paths there)
    edm::Handle<edm::TriggerResults> triggerResults;
    iEvent.getByLabel(fTriggerResultsSrc, triggerResults);
    if (!triggerResults.isValid())
      throw cms::Exception("Assert") << "METFilters: edm::TriggerResults object is not valid!";
    const edm::TriggerNames& triggerNames = iEvent.triggerNames(*triggerResults);
    if (!fTriggerResultsListPrintedStatus) {
      std::cout << "TriggerResults list including METFilters (for information):" << std::endl;
      for (unsigned int i = 0; i < triggerResults->size(); ++i) {
        std::cout << "  " <<  triggerNames.triggerName(i) << " status=" << triggerResults->accept(i) << std::endl;
      }
      fTriggerResultsListPrintedStatus = true;
    }

//----- Beam halo filter
    if (fBeamHaloFilterEnabled) {
      edm::Handle<reco::BeamHaloSummary> hbeamhalo;
      iEvent.getByLabel(fBeamHaloFilterSrc, hbeamhalo);
      if (hbeamhalo->CSCTightHaloId()) // Returns true if event has been identified as a halo event
        return false;
    }
    increment(fBeamHaloFilterCounter);

//----- HBHE noise filter
    if(fHBHENoiseFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fHBHENoiseFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fHBHENoiseFilterCounter);

    if(fHBHENoiseFilterMETWGEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fHBHENoiseFilterMETWGSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fHBHENoiseFilterMETWGCounter);

//----- Tracking failure filter
    if(fTrackingFailureFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fTrackingFailureFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fTrackingFailureFilterCounter);

//----- ECAL dead cell filter
    if(fEcalDeadCellEventFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalDeadCellEventFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fEcalDeadCellEventFilterCounter);

    if (fEcalDeadCellTPFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalDeadCellTPFilterSrc, hresult);
      if(! *hresult)
        return false;
    }
    increment(fEcalDeadCellTPFilterCounter);

//----- HCAL laser filters
    if (fHcalLaserFilterEnabled) {
      for (std::vector<std::string>::const_iterator iName = fHcalLaserFilterStrings.begin(); iName != fHcalLaserFilterStrings.end(); ++iName) {
        bool myFoundStatus = false;
        for (unsigned int i = 0; i < triggerResults->size(); ++i) {
          if (triggerNames.triggerName(i) == *iName) {
            if (!triggerResults->accept(i))
              return false;
            myFoundStatus = true;
          }
        }
        if (!myFoundStatus)
          throw cms::Exception("Assert") << "METFilters: Path name '" << *iName << "' does not exist in edm::TriggerResults! Check your config!";
      }
      increment(fHcalLaserFilterCounter);
    }

//----- Bad EE supercrystals
    if (fBadEESuperCrystalFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fBadEESuperCrystalFilterSrc, hresult);
      if(! *hresult)
        return false;      
      increment(fBadEESuperCrystalFilterCounter);
    }
    
//----- Ecal crystals with large laser correction
    if (fEcalCrystalsWithLargeLaserCorrectionFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalCrystalsWithLargeLaserCorrectionFilterSrc, hresult);
      if(! *hresult)
        return false;      
      increment(fEcalCrystalsWithLargeLaserCorrectionFilterCounter);
    }
    
//----- Tracking odd events
    if (fTrackingOddEventFilterEnabled) {
      for (std::vector<std::string>::const_iterator iName = fTrackingOddEventFilterStrings.begin(); iName != fTrackingOddEventFilterStrings.end(); ++iName) {
        bool myFoundStatus = false;
        for (unsigned int i = 0; i < triggerResults->size(); ++i) {
          if (triggerNames.triggerName(i) == *iName) {
            if (!triggerResults->accept(i))
              return false;
            myFoundStatus = true;
          }
        }
        if (!myFoundStatus)
          throw cms::Exception("Assert") << "METFilters: Path name '" << *iName << "' does not exist in edm::TriggerResults! Check your config!";
      }
      increment(fTrackingOddEventFilterCounter);
    }
    
//----- Muon filters (optional)
    if (fMuonsWithWrongMomentaFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fMuonsWithWrongMomentaFilterSrc, hresult);
      if(! *hresult)
        return false;      
      increment(fMuonsWithWrongMomentaFilterCounter);
    }
    if (fInconsistentMuonPFCandidateFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fInconsistentMuonPFCandidateFilterSrc, hresult);
      if(! *hresult)
        return false;      
      increment(fInconsistentMuonPFCandidateFilterCounter);
    }    
    
    // Filters passed 
    increment(fAllPassedCounter);
    return true;
  }
}
