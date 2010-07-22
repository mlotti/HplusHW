#ifndef HPLUSANALYSISHLTOBJECTS_H
#define HPLUSANALYSISHLTOBJECTS_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

/**
Class for storing HLT objects

	@author 8.7.2010/S.Lehti
*/

class HPlusHLTTaus : public HPlusAnalysis::HPlusAnalysisBase, public HPlusAnalysis::HPlusSelectionBase {
    public:
  	/// Default constructor
	HPlusHLTTaus(const edm::ParameterSet& iConfig);
  	/// Default destructor
  	~HPlusHLTTaus();
  
  	void beginJob();
  	void endJob();
  	/// Applies the trigger selection; returns true if trigger was passed
  	bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
    private:
  	/// collection
  	edm::InputTag fCollectionName;
  
  	// Counter ID's
  	/// IDs of the event counters
	int fAll;
	int fSelected;
};
#endif
