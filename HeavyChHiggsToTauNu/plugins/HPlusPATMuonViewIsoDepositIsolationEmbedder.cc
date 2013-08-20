#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "PhysicsTools/IsolationAlgos/interface/IsoDepositVetoFactory.h"
#include "PhysicsTools/IsolationAlgos/interface/EventDependentAbsVeto.h"

// Only for the CandIsolatorFromDeposits::Mode enumeration
#include "PhysicsTools/IsolationAlgos/plugins/CandIsolatorFromDeposits.h"

#include<memory>
#include<vector>

class HPlusPATMuonViewIsoDepositIsolationEmbedder: public edm::EDProducer {
  // Example from PhysicsTools/IsolationAlgos/plugins/CandIsolatorFromDeposits.cc
  class SingleDeposit {
  public:
    SingleDeposit(const edm::ParameterSet& iConfig, const std::string& prefix):
      fEmbedName(prefix+iConfig.getParameter<std::string>("embedName")),
      fDeltaR(iConfig.getParameter<double>("deltaR")),
      fSkipDefaultVeto(iConfig.getParameter<bool>("skipDefaultVeto"))
    {
      std::string mode = iConfig.getParameter<std::string>("mode");
      if       (mode == "sum")         fMode = CandIsolatorFromDeposits::Sum; 
      else if (mode == "sumRelative")  fMode = CandIsolatorFromDeposits::SumRelative; 
      else if (mode == "sum2")         fMode = CandIsolatorFromDeposits::Sum2;                  
      else if (mode == "sum2Relative") fMode = CandIsolatorFromDeposits::Sum2Relative;
      else if (mode == "max")          fMode = CandIsolatorFromDeposits::Max;                  
      else if (mode == "maxRelative")  fMode = CandIsolatorFromDeposits::MaxRelative;
      else if (mode == "nearestDR")    fMode = CandIsolatorFromDeposits::NearestDR;
      else if (mode == "count")        fMode = CandIsolatorFromDeposits::Count;
      else throw cms::Exception("Not Implemented") << "Mode '" << mode << "' not implemented." << std::endl;

      // See e.g. PhysicsTools/PatAlgos/plugins/PATMuonProducer.cc
      std::string isolationKey = iConfig.getParameter<std::string>("isolationKey");
      if     (isolationKey == "pfAllParticles")     fIsolationKey = pat::PfAllParticleIso;
      else if(isolationKey == "pfChargedHadrons")   fIsolationKey = pat::PfChargedHadronIso;
      else if(isolationKey == "pfChargedAll")       fIsolationKey = pat::PfChargedAllIso;
      else if(isolationKey == "pfPUChargedHadrons") fIsolationKey = pat::PfPUChargedHadronIso;
      else if(isolationKey == "pfNeutralHadrons")   fIsolationKey = pat::PfNeutralHadronIso;
      else if(isolationKey == "pfPhotons")          fIsolationKey = pat::PfGammaIso;
      else throw cms::Exception("Not Implemented") << "PAT Isolation key '" << isolationKey << "' not implemented." << std::endl;

      // Construct the Vetos
      std::vector<std::string> vetos = iConfig.getParameter<std::vector<std::string> >("vetos");
      reco::isodeposit::EventDependentAbsVeto *evdep = 0;
      for (std::vector<std::string>::const_iterator it = vetos.begin(), ed = vetos.end(); it != ed; ++it) {
        fVetos.push_back(IsoDepositVetoFactory::make(it->c_str(), evdep));
        if (evdep) fEvdepVetos.push_back(evdep);
      }
    }
    
    void cleanup() {
      for(size_t i=0; i<fVetos.size(); ++i) {
        delete fVetos[i];
        fVetos[i] = 0;
      }
      fVetos.clear();
       // NOTE: we DON'T have to delete the fEvdepVetos, they have already been deleted above. We just clear the vectors
      fEvdepVetos.clear();
    }

    void open(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
      for (reco::isodeposit::EventDependentAbsVetos::iterator it = fEvdepVetos.begin(), ed = fEvdepVetos.end(); it != ed; ++it) {
        (*it)->setEvent(iEvent,iSetup);
      }
    }

    void embed(pat::Muon &muon) {
      double value = compute(muon);
      //std::cout << "  " << fEmbedName << " " << value << std::endl;
      muon.addUserFloat(fEmbedName, value);
    }

  private:
    double compute(const pat::Muon &muon) {
      const reco::IsoDeposit *depPtr = muon.isoDeposit(fIsolationKey);
      if(!depPtr) throw cms::Exception("Assert") << "Null IsoDeposit for isolation key " << fIsolationKey << ". See DataFormats/PatCandidates/interface/Isolation.h for the meaning of the values." << std::endl;

      const reco::IsoDeposit &dep = *depPtr;
      double eta = dep.eta(), phi = dep.phi(); // better to center on the deposit direction
                                               // that could be, e.g., the impact point at calo
      for (reco::isodeposit::AbsVetos::iterator it = fVetos.begin(), ed = fVetos.end(); it != ed; ++it) {
        (*it)->centerOn(eta, phi);
      }
      switch (fMode) {
      case CandIsolatorFromDeposits::Count:        return dep.countWithin(fDeltaR, fVetos, fSkipDefaultVeto);
      case CandIsolatorFromDeposits::Sum:          return dep.sumWithin(fDeltaR,   fVetos, fSkipDefaultVeto);
      case CandIsolatorFromDeposits::SumRelative:  return dep.sumWithin(fDeltaR,   fVetos, fSkipDefaultVeto) / dep.candEnergy() ;
      case CandIsolatorFromDeposits::Sum2:         return dep.sum2Within(fDeltaR,  fVetos, fSkipDefaultVeto);
      case CandIsolatorFromDeposits::Sum2Relative: return dep.sum2Within(fDeltaR,  fVetos, fSkipDefaultVeto) / (dep.candEnergy() * dep.candEnergy()) ;
      case CandIsolatorFromDeposits::Max:          return dep.maxWithin(fDeltaR,   fVetos, fSkipDefaultVeto);
      case CandIsolatorFromDeposits::NearestDR:    return dep.nearestDR(fDeltaR,   fVetos, fSkipDefaultVeto);
      case CandIsolatorFromDeposits::MaxRelative:  return dep.maxWithin(fDeltaR,   fVetos, fSkipDefaultVeto) / dep.candEnergy() ;
      }
      throw cms::Exception("LogigError") << "Should not happen at " << __FILE__ << ", line " << __LINE__; // avoid gcc warning
    }

    reco::isodeposit::AbsVetos fVetos;
    reco::isodeposit::EventDependentAbsVetos fEvdepVetos; // note: these are a subset of the above. Don't delete twice!
    std::string fEmbedName;
    double fDeltaR;
    CandIsolatorFromDeposits::Mode fMode;
    pat::IsolationKeys fIsolationKey;
    bool fSkipDefaultVeto;
  };

public:
  explicit HPlusPATMuonViewIsoDepositIsolationEmbedder(const edm::ParameterSet& iConfig):
    fMuonSrc(iConfig.getParameter<edm::InputTag>("src"))
  {
    std::string embedPrefix = iConfig.getParameter<std::string>("embedPrefix");

    typedef std::vector<edm::ParameterSet> VPSet;
    VPSet depPSets = iConfig.getParameter<VPSet>("deposits");
    for (VPSet::const_iterator it = depPSets.begin(), ed = depPSets.end(); it != ed; ++it) {
      fDeposits.push_back(SingleDeposit(*it, embedPrefix));
    }
    if (fDeposits.size() == 0) throw cms::Exception("Configuration") << "Please specify at least one deposit!";

    produces<std::vector<pat::Muon> >();
  }

  HPlusPATMuonViewIsoDepositIsolationEmbedder() {
    for(size_t i=0; i<fDeposits.size(); ++i) {
      fDeposits[i].cleanup();
    }
  }

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fMuonSrc, hmuons);

    for(size_t iDeposit=0; iDeposit<fDeposits.size(); ++iDeposit) {
      fDeposits[iDeposit].open(iEvent, iSetup);
    }

    std::auto_ptr<std::vector<pat::Muon> > prod(new std::vector<pat::Muon>());
    prod->reserve(hmuons->size());
    for(size_t iMuon=0; iMuon<hmuons->size(); ++iMuon) {
      // Make a copy from the original
      pat::Muon copy = (*hmuons)[iMuon];

      //std::cout << "Muon " << iMuon << std::endl;
      for(size_t iDeposit=0; iDeposit<fDeposits.size(); ++iDeposit) {
        fDeposits[iDeposit].embed(copy);
      }

      prod->push_back(copy);
    }
    //if(!hmuons->empty()) std::cout << std::endl;
    iEvent.put(prod);
  }

private:
  edm::InputTag fMuonSrc;
  std::vector<SingleDeposit> fDeposits;
};

DEFINE_FWK_MODULE( HPlusPATMuonViewIsoDepositIsolationEmbedder );
