#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/GenMET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include<vector>

#include<TH1F.h>

class METResolutionAnalysis: public edm::EDAnalyzer {
    public:

  	explicit METResolutionAnalysis(const edm::ParameterSet&);
  	~METResolutionAnalysis();

    private:
  	virtual void beginJob();
  	virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  	virtual void endJob();

  	edm::InputTag recoSrc;
  	edm::InputTag mcSrc;

	TH1* hDMet;
	TH1* hDMetRel;
	TH1* hDPhiMet;
};

METResolutionAnalysis::METResolutionAnalysis(const edm::ParameterSet& iConfig):
  recoSrc(iConfig.getParameter<edm::InputTag>("recoMETSrc")),
  mcSrc(iConfig.getParameter<edm::InputTag>("mcMETSrc"))
{
	edm::Service<TFileService> fs;

	TFileDirectory dir = fs->mkdir("");//METResolution");

	hDMet = HPlus::makeTH<TH1F>(dir, "DMet", "Met(MCMet=0)", 20, 0., 200);
	hDMetRel = HPlus::makeTH<TH1F>(dir, "DMetRel", "(Met - MCMet)/MCMet", 30, -1., 2.);
	hDPhiMet = HPlus::makeTH<TH1F>(dir, "DPhiMet", "Met - MCMet", 90, 0., 180);
}
METResolutionAnalysis::~METResolutionAnalysis() {}
void METResolutionAnalysis::beginJob() {}

void METResolutionAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

        edm::Handle<edm::View<reco::MET> > hmet;
        iEvent.getByLabel(recoSrc, hmet);

	edm::Handle<edm::View<reco::GenMET> > hMCmet;
	iEvent.getByLabel(mcSrc, hMCmet);

	double dmet = (hmet->at(0).et() - hMCmet->at(0).et());
	if(hMCmet->at(0).et() == 0) {
		hDMet->Fill(dmet);
	}else{
		hDMetRel->Fill(dmet/hMCmet->at(0).et());
	}

	double dphi = fabs( hmet->at(0).phi() - hMCmet->at(0).phi() );
	dphi = 180/ROOT::Math::Pi()*dphi;
	if(fabs(dphi) > 180) dphi = 360 - fabs(dphi);
	hDPhiMet->Fill(dphi);
}

void METResolutionAnalysis::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(METResolutionAnalysis);
