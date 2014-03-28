/*
  PURPOSE
  Create vectors of different types of jets that can be used to calculate the b-(mis)tagging efficiency in MC. The efficiency measurement can be done at
  several points in the event selection flow by creating several BTaggingEfficiencyInMC::Data objects in SignalAnalysis.cc (for instance). For this
  reason, the actual histograms and counters are defined and handled in SignalAnalysis.cc (for instance).
*/
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingEfficiencyInMC.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

namespace HPlus {
  BTaggingEfficiencyInMC::Data::Data() { }

  BTaggingEfficiencyInMC::Data::~Data() { }

  BTaggingEfficiencyInMC::BTaggingEfficiencyInMC(EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    // (possibly) read configuration and add counters
    allJetsCount(eventCounter.addSubCounter("allJetsCount","All jets")),
    genuineBJetsCount(eventCounter.addSubCounter("genuineBJetsCount","Genuine b-jets")),
    genuineBJetsWithBTagCount(eventCounter.addSubCounter("genuineBJetsWithBTagCount","Genuine b-jets with b-tag"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("BTaggingEfficiencyInMC");
    // Create histograms
  }

  BTaggingEfficiencyInMC::~BTaggingEfficiencyInMC() { }

  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,
								     const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent, iSetup, jets, bTagData);
  }
  
  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,
							       const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, bTagData);
  }
  
  BTaggingEfficiencyInMC::Data BTaggingEfficiencyInMC::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup,
								      const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData) {
    // Throw exception if b-tagging data are not available (i.e. if BTagging::privateAnalyze() has not been called
    // TODO implement

    // Set up
    Data output;
    output.fGenuineBJets.reserve(jets.size());
    output.fGenuineBJetsWithBTag.reserve(jets.size());
    output.fGenuineGJets.reserve(jets.size());
    output.fGenuineGJetsWithBTag.reserve(jets.size());
    output.fGenuineUDSJets.reserve(jets.size());
    output.fGenuineUDSJetsWithBTag.reserve(jets.size());
    output.fGenuineCJets.reserve(jets.size());
    output.fGenuineCJetsWithBTag.reserve(jets.size());
    output.fGenuineLJets.reserve(jets.size());
    output.fGenuineLJetsWithBTag.reserve(jets.size());

    // End run with default output if the event is not MC. Otherwise, continue.
    if (iEvent.isRealData()) return output;

    // Make vectors of jets for the output. This way, their p_T, eta, ... can be put into histograms, which in turn can be used to
    // calculate the efficiencies in bins of p_T, eta, ...
    classifyJetsForEfficiencyCalculation(jets, bTagData, output);
    return output;
  }


  
  void BTaggingEfficiencyInMC::classifyJetsForEfficiencyCalculation(const edm::PtrVector<pat::Jet>& jets, const BTagging::Data& bTagData,
								    BTaggingEfficiencyInMC::Data& output) {
    int iFlavour = 0;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      increment(allJetsCount);
      edm::Ptr<pat::Jet> iJet = *iter;
      iFlavour = std::abs(iJet->partonFlavour());
      if (iFlavour == 5) {
	// B-jet found.
	output.fGenuineBJets.push_back(iJet);
	increment(genuineBJetsCount);
	if (isBTagged(iJet, bTagData)) {
	  output.fGenuineBJetsWithBTag.push_back(iJet); // B-tagged b-jet found.
	  increment(genuineBJetsWithBTagCount);
	}
      } else if (iFlavour == 21) {
        // Gluon flavour jet found.
        output.fGenuineGJets.push_back(iJet);
        if (isBTagged(iJet, bTagData)) output.fGenuineGJetsWithBTag.push_back(iJet); // B-tagged gluon flavour jet found.
      } else if (iFlavour == 1 || iFlavour == 2 || iFlavour == 3) {
        // UDS flavour jet found.
        output.fGenuineUDSJets.push_back(iJet);
        if (isBTagged(iJet, bTagData)) output.fGenuineUDSJetsWithBTag.push_back(iJet); // B-tagged uds flavour jet found.
      } else if (iFlavour == 4) {
	// C flavour jet found
	output.fGenuineCJets.push_back(iJet);
	if (isBTagged(iJet, bTagData)) output.fGenuineCJetsWithBTag.push_back(iJet); // B-tagged c-jet found
      }
      if (iFlavour != 5 && iFlavour != 4) {
	// Light flavour jet found.
	output.fGenuineLJets.push_back(iJet);
	if (isBTagged(iJet, bTagData)) output.fGenuineLJetsWithBTag.push_back(iJet); // B-tagged light flavour jet found.
      }
    }
  }


 
  bool BTaggingEfficiencyInMC::isBTagged(edm::Ptr<pat::Jet>& jet, const BTagging::Data& bTagData) {
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bTagData.getSelectedJets().begin(); iBjet != bTagData.getSelectedJets().end(); ++iBjet) {
      if (jet == *iBjet) return true;
    }
    return false;
  }  
}
