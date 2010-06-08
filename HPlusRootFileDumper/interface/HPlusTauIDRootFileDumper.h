#ifndef HPlusTauIDRootFileDumper_h
#define HPlusTauIDRootFileDumper_h

// -*- C++ -*-
//
// Package:    HPlusTauIDRootFileDumper
// Class:      HPlusTauIDRootFileDumper
// 
/**\class HPlusTauIDRootFileDumper HPlusTauIDRootFileDumper.cc mycode/HPlusTauIDRootFileDumper/src/HPlusTauIDRootFileDumper.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
 */
//
// Original Author:  Lauri Wendland
//         Created:  Tue Apr 13 13:12:43 EEST 2010
// $Id$
//
//

// system include files
#include <memory>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperCaloTau.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperPF.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
//#include "HiggsAnalysis/HPlusRootFileDumper/src/classes.h"
//#include "HiggsAnalysis/HPlusRootFileDumper/interface/SelectionManager.h"

#include "TTree.h"

//
// class declaration
//

class HPlusTauIDRootFileDumper : public edm::EDProducer {
 public:
  /*enum TauCollectionSelection {
    kPFTau,
    kCaloTau,
    kTCTau,
    kUnknownTau
};*/
  /// Default EDAnalyzer constructor
  explicit HPlusTauIDRootFileDumper(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusTauIDRootFileDumper();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job 
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();
  
  // /// Applies tau-jet candidate cuts (true if passed, false if not passed)
  //bool applyTauJetCandidateCuts(const edm::Event& iEvent);
  
  //bool fillCaloJets();
  //void setupRootTreeBranches();
  //void initializeRootTreeVariables();
  
  // ----------member data ---------------------------
  edm::Service<TFileService> fFileService; // wrapper for TFile
  TTree* fRootTree;
  //std::string fRootFilename;
  // /// Object for handling event selections (event selections are specified in the config file)
  //HPlusAnalysis::SelectionManager* fSelectionManager;
  
  /// Object for handling the ROOT tree dumping of specific tau objects (owner)
  HPlusAnalysis::HPlusTauDumperBase* fTauDumper;
  
  // Tree variables
  //uint32_t fRunNumber, fLumiSection, fEventNumber;
  
  //edm::InputTag iPFTauProducer;
  
  //std::vector<edm::ParameterSet> fPFTaus;
  //edm::ParameterSet fTauCollection;
  //TauCollectionSelection fTauCollectionType;
  
  HPlusAnalysis::Counter* fCounter; ///< Pointer to the Counter (event counter) object (owner)
  int fCounterIdAllEvents;
  int fCounterIdSavedEvents;
};

#endif