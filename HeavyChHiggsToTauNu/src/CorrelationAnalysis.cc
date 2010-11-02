#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {

  CorrelationAnalysis::CorrelationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter) {
	init();
  }
  CorrelationAnalysis::CorrelationAnalysis(){
	init();
  }

  CorrelationAnalysis::~CorrelationAnalysis() {}

  void CorrelationAnalysis::init(){
    edm::Service<TFileService> fs;
    hPt = fs->make<TH1F>("jet_pt", "het_pt", 100, 0., 100.);
  }

  void CorrelationAnalysis::analyze(const edm::PtrVector<reco::Candidate>& input1,const edm::PtrVector<reco::Candidate>& input2){

	for(edm::PtrVector<reco::Candidate>::const_iterator iter1 = input1.begin(); iter1 != input1.end(); ++iter1) {
		edm::Ptr<reco::Candidate> iCand1 = *iter1;
		for(edm::PtrVector<reco::Candidate>::const_iterator iter2 = input2.begin(); iter2 != input2.end(); ++iter2) {
			edm::Ptr<reco::Candidate> iCand2 = *iter2;



		}
	}
  }
}
