#ifndef HPLUSANALYSISMET_H
#define HPLUSANALYSISMET_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

/**
Class for storing MET

	@author 2.7.2010/S.Lehti
*/

class HPlusMET : public HPlusAnalysis::HPlusAnalysisBase, public HPlusAnalysis::HPlusSelectionBase {
    public:
  	/// Default constructor
	HPlusMET(const edm::ParameterSet& iConfig);
  	/// Default destructor
  	~HPlusMET();
  
  	void beginJob();
  	void endJob();
  	/// Applies the trigger selection; returns true if trigger was passed
  	bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
    private:
  	/// Name of muon collection
  	edm::InputTag fCollectionName;
  
  	// Counter ID's
  	/// IDs of the event counters
	int fMET_All;
	int fMET_Selected;
};
#endif
