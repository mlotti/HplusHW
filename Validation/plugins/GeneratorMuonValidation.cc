/*class MuonValidation
 *  
 *  Class to fill Event Generator dqm monitor elements; works on HepMCProduct
 *
 *  $Date: 2011/02/14 09:52:07 $
 *  $Revision: 1.7 $
 *
 */

// framework & common header files
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Run.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

//DQM services
#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

class MuonValidation : public edm::EDAnalyzer
{
    public:
	// mother particles 
	enum  {other,
	       gamma,
	       Z,
	       W,
	       HSM,
	       H0,
	       A0,
	       Hpm};

    public:
	explicit MuonValidation(const edm::ParameterSet&);
	virtual ~MuonValidation();
	virtual void beginJob();
	virtual void endJob();  
	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void beginRun(const edm::Run&, const edm::EventSetup&);
	virtual void endRun(const edm::Run&, const edm::EventSetup&);

    private:
	int particleMother(const reco::GenParticle&);
        int findMother(const reco::GenParticle&);
        bool genMuonMatchingRecoMuon(const reco::GenParticle&,const edm::Event&);

    	edm::InputTag src,recoMuonSrc;
	double DRmin;

  	/// PDT table
  	edm::ESHandle<HepPDT::ParticleDataTable> fPDGTable ;
  
  	///ME's "container"
  	DQMStore *dbe;

        MonitorElement *nEvt;
        MonitorElement *MuPt, *MuEta, *MuPhi,
	  *MuPtW, *MuEtaW, *MuPhiW,
          *MuPtReco, *MuEtaReco, *MuPhiReco,
          *MuonMothers;
};

#include "CLHEP/Units/defs.h"
#include "CLHEP/Units/PhysicalConstants.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

using namespace edm;

MuonValidation::MuonValidation(const edm::ParameterSet& iPSet):  
  src(iPSet.getParameter<edm::InputTag>("src")),
  recoMuonSrc(iPSet.getParameter<edm::InputTag>("RecoMuons")),
  DRmin(iPSet.getParameter<double>("MCRecoMatchingCone"))
{    
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

MuonValidation::~MuonValidation() {}

void MuonValidation::beginJob()
{
  return;
}

void MuonValidation::endJob(){
  return;
}

void MuonValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup)
{
  ///Get PDT Table
//  iSetup.getData( fPDGTable );

  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/GeneratorMuon");
    
    // Number of analyzed events
    nEvt = dbe->book1D("nEvt", "n analyzed Events", 1, 0., 1.);

    //Kinematics
    MuPt             = dbe->book1D("MuPt","Mu pT", 100 ,0,100);
    MuEta            = dbe->book1D("MuEta","Mu eta", 100 ,-2.5,2.5);
    MuPhi            = dbe->book1D("MuPhi","Mu phi", 100 ,-3.14,3.14);

    MuPtW            = dbe->book1D("MuPtW","Mu (from W) pT", 100 ,0,100);
    MuEtaW           = dbe->book1D("MuEtaW","Mu (from W) eta", 100 ,-2.5,2.5);
    MuPhiW           = dbe->book1D("MuPhiW","Mu (from W) phi", 100 ,-3.14,3.14);

    std::string label = "Mu (matching " + recoMuonSrc.label() + ")";
    MuPtReco         = dbe->book1D("MuPtReco",(label+" pT").c_str(), 100 ,0,100);
    MuEtaReco        = dbe->book1D("MuEtaReco",(label+" eta").c_str(), 100 ,-2.5,2.5);
    MuPhiReco        = dbe->book1D("MuPhiReco",(label+" phi").c_str(), 100 ,-3.14,3.14);

    MuonMothers        = dbe->book1D("MuonMothers","Muon mother particles", 10 ,0,10);
	MuonMothers->setBinLabel(1+other,"?");
	MuonMothers->setBinLabel(1+gamma,"#gamma");
	MuonMothers->setBinLabel(1+Z,"Z");
	MuonMothers->setBinLabel(1+W,"W");
	MuonMothers->setBinLabel(1+HSM,"H_{SM}/h^{0}");
	MuonMothers->setBinLabel(1+H0,"H^{0}");
	MuonMothers->setBinLabel(1+A0,"A^{0}");
	MuonMothers->setBinLabel(1+Hpm,"H^{#pm}");
  }

  return;
}
void MuonValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){return;}
void MuonValidation::analyze(const edm::Event& iEvent,const edm::EventSetup& iSetup)
{ 
  nEvt->Fill(0.5);

  Handle<reco::GenParticleCollection> genParticles;
  iEvent.getByLabel(src, genParticles);
  if(genParticles.isValid()){
    for(size_t i = 0; i < genParticles->size(); ++ i) {
      const reco::GenParticle & p = (*genParticles)[i];
      int mother  = particleMother(p);
      if(abs(p.pdgId())==13 && abs(mother) != 13){
	MuPt->Fill(p.pt());
	MuEta->Fill(p.eta());
	MuPhi->Fill(p.phi());
	if(abs(mother) == 24){
	  MuPtW->Fill(p.pt());
	  MuEtaW->Fill(p.eta());
	  MuPhiW->Fill(p.phi());
	}

	if(genMuonMatchingRecoMuon(p,iEvent)){
	  MuPtReco->Fill(p.pt());
	  MuEtaReco->Fill(p.eta());
	  MuPhiReco->Fill(p.phi());
	}
      }
    }
  }
}//analyze


int MuonValidation::findMother(const reco::GenParticle& particle){
        return particle.mother()->pdgId();
}

int MuonValidation::particleMother(const reco::GenParticle& particle){

  if(abs(particle.pdgId()) != 13) return -1;

	int mother_pid = findMother(particle);
	if(mother_pid == -1) return -1;

	int label = other;
	if(abs(mother_pid) == 24) label = W;
        if(abs(mother_pid) == 23) label = Z;
	if(abs(mother_pid) == 22) label = gamma;
	if(abs(mother_pid) == 25) label = HSM;
	if(abs(mother_pid) == 35) label = H0;
	if(abs(mother_pid) == 36) label = A0;
	if(abs(mother_pid) == 37) label = Hpm;

	MuonMothers->Fill(label);

	return mother_pid;
}

bool MuonValidation::genMuonMatchingRecoMuon(const reco::GenParticle& particle, const edm::Event& iEvent){

    bool match = false;

    edm::Handle<edm::View<pat::Muon> > myMuonHandle;
    iEvent.getByLabel(recoMuonSrc, myMuonHandle);
    edm::PtrVector<pat::Muon> muons = myMuonHandle->ptrVector();

    for(edm::PtrVector<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
	double DR = ROOT::Math::VectorUtil::DeltaR(particle.p4(),(*iMuon)->p4());
	if(DR < DRmin) match = true;
    }

    return match;
}

//define this as a plug-in
DEFINE_FWK_MODULE(MuonValidation);
