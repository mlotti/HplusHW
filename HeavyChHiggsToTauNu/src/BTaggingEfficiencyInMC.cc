// New code for calculating the b-tagging efficiency in MC. Responsible persons in Summer 2013: Shih-Yen and Stefan.
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingEfficiencyInMC.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);
bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasMother(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
bool  hasDaughter(const reco::Candidate& p, int id);
void  printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);

namespace HPlus {
  BTaggingEfficiencyInMC::Data::Data():
    fSomeDataMember(0)
  { }

  BTaggingEfficiencyInMC::Data::~Data() { }

  BTaggingEfficiencyInMC::BTaggingEfficiencyInMC(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper)
    // (possibly) read configuration and add counters
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("BTaggingEfficiencyInMC");
    // Create histograms
  }

  BTaggingEfficiencyInMC::~BTaggingEfficiencyInMC() { }

  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::silentAnalyze(const edm::Event& iEvent) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent);
  }
  
  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::analyze(const edm::Event& iEvent) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent);
  }
  
  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::privateAnalyze(const edm::Event& iEvent) {
    // basically all the actual code goes here
    Data output;
    return output;
  }
}
