#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CorrelationAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "TH1F.h"

namespace HPlus {

  CorrelationAnalysis::CorrelationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter) {
    init();
  }
  CorrelationAnalysis::CorrelationAnalysis(EventCounter& eventCounter) {
    init();
  }
  CorrelationAnalysis::CorrelationAnalysis(){
    init();
  }

  CorrelationAnalysis::~CorrelationAnalysis() {}

  void CorrelationAnalysis::init(){
    edm::Service<TFileService> fs;
    hPtB1 = fs->make<TH1F>("bjet1_pt", "bjet1_pt", 100, 0., 200.);
    hPtB2 = fs->make<TH1F>("bjet2_pt", "bjet2_pt", 100, 0., 200.);
    hEtaB1 = fs->make<TH1F>("bjet1_eta", "bjet1_eta", 60, -3., 3.);
    hEtaB2 = fs->make<TH1F>("bjet2_eta", "bjet2_eta", 60, -3., 3.);
    hDeltaR_tauB1 = fs->make<TH1F>("DeltaR_tauB1", "DeltaR_tauB1", 100, 0., 5.);
    hDeltaR_tauB2 = fs->make<TH1F>("DeltaR_tauB2", "DeltaR_tauB2", 100, 0., 5.);
  }

  void CorrelationAnalysis::analyze(const edm::PtrVector<reco::Candidate>& input1,const edm::PtrVector<reco::Candidate>& input2){

    double DeltaR_tauB1 = -999;
    double DeltaR_tauB2 = -999;
    int ntaus = 0;
    // calculate DeltaR between the selected tau jet and tagged b jets
	for(edm::PtrVector<reco::Candidate>::const_iterator iter1 = input1.begin(); iter1 != input1.end(); ++iter1) {
		edm::Ptr<reco::Candidate> iCand1 = *iter1;
		if (ntaus > 1 ) continue;
		if( input2.size() > 0 ) {
		  DeltaR_tauB1 = reco::deltaR((*iCand1), *(input2[0]));
		  hDeltaR_tauB1->Fill(DeltaR_tauB1);
		  hPtB1->Fill((input2[0])->pt());
		  hEtaB1->Fill((input2[0])->eta());
		  if( input2.size() > 1 ) {
		    DeltaR_tauB2 = reco::deltaR((*iCand1), *(input2[1]));
		    hDeltaR_tauB2->Fill(DeltaR_tauB2);
		    hPtB2->Fill((input2[1])->pt());
		    hEtaB2->Fill((input2[1])->eta());
		  }
		}  
		ntaus++;	       
	}
  }
}
