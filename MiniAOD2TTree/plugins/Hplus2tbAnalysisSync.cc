/** \class Hplus2tbAnalysisSync
 *
 *  
 *  Filter to select events for H+ -> tb fully hadronic (boosted)
 *
 *  \author Marina Kolosova 
 *
 */

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/MiniIsolation.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
// Marina
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Common/interface/PtrVector.h"
#include "DataFormats/Common/interface/RefToBase.h" 

#include <string>
#include <vector>
#include <memory>


#include "FWCore/Framework/interface/LuminosityBlock.h"

#include <iostream>
#include <regex>

class Hplus2tbAnalysisSync : public edm::EDFilter {

public:
  explicit Hplus2tbAnalysisSync(const edm::ParameterSet&);
  ~Hplus2tbAnalysisSync();

  virtual bool filter(edm::Event&, const edm::EventSetup& );

private:
  const bool cfg_verbose;
  edm::EDGetTokenT<edm::TriggerResults> cfg_trgResultsToken;
  std::vector<std::string> cfg_triggerBits;

  edm::EDGetTokenT<edm::View<pat::Jet>> cfg_jetToken;
  std::vector<std::string> cfg_jetUserFloats;
  const double cfg_jetEtCut;
  const double cfg_jetEtaCut;
  const int cfg_nJets;

  edm::EDGetTokenT<edm::View<pat::Jet>> cfg_ak8jetToken;
  const double cfg_ak8jetEtCut;
  const double cfg_ak8jetEtaCut;
  const int cfg_ak8nJets;
  
  // Marina - start
  edm::EDGetTokenT<edm::View<pat::PackedCandidate> > cfg_pfcandsToken;
  // Marina - end
  
  edm::EDGetTokenT<edm::View<reco::Vertex> > cfg_vertexToken;
  
  edm::EDGetTokenT<pat::ElectronCollection> cfg_electronToken;
  
  edm::EDGetTokenT<double> cfg_rhoToken;
  std::string cfg_electronID;
  edm::EDGetTokenT<edm::ValueMap<float> > cfg_electronMVAToken;
  // Marina - start
  const double cfg_electronMiniRelIsoEA;
  // Marina - end
  const double cfg_electronPtCut;
  const double cfg_electronEtaCut;
  const int cfg_electronNCut;

  edm::EDGetTokenT<edm::View<pat::Muon> > cfg_muonToken;
  std::string cfg_muonID;
 
  //const double cfg_muonRelIso04;
  // Marina - start
  const double cfg_muonMiniRelIsoEA;
  // Marina - end
  const double cfg_muonPtCut;
  const double cfg_muonEtaCut;
  const int cfg_muonNCut;

  // Marina - start
  edm::EDGetTokenT<edm::View<pat::Tau> > cfg_tauToken;
  std::vector<std::string>  cfg_tauDiscriminators;
  const double cfg_tauPtCut;
  const double cfg_tauEtaCut;
  const int cfg_tauNCut;
  // Marina - end

  int nEvents;
  int nSelectedEvents;
  
  // Marina
  int nEventsPassedElectronVeto = 0;
  int nEventsPassedMuonVeto     = 0;
  int nEventsPassedTauVeto      = 0;
  int nEventsPassedLeptonVeto   = 0;
};

Hplus2tbAnalysisSync::Hplus2tbAnalysisSync(const edm::ParameterSet& iConfig)
  : cfg_verbose(iConfig.getParameter<bool>("Verbose")),
    cfg_trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
    cfg_triggerBits(iConfig.getParameter<std::vector<std::string> >("HLTPaths")),
    
    cfg_jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("JetCollection"))),
    cfg_jetUserFloats(iConfig.getParameter<std::vector<std::string> >("JetUserFloats")),
    cfg_jetEtCut(iConfig.getParameter<double>("JetEtCut")),
    cfg_jetEtaCut(iConfig.getParameter<double>("JetEtaCut")),
    cfg_nJets(iConfig.getParameter<int>("NJets")),
    
    cfg_ak8jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("AK8JetCollection"))),
    cfg_ak8jetEtCut(iConfig.getParameter<double>("AK8JetEtCut")),
    cfg_ak8jetEtaCut(iConfig.getParameter<double>("AK8JetEtaCut")),
    cfg_ak8nJets(iConfig.getParameter<int>("AK8NJets")),

    // Marina
    cfg_pfcandsToken(consumes<edm::View<pat::PackedCandidate> >(iConfig.getParameter<edm::InputTag>("PackedCandidatesCollection"))),
    
    cfg_vertexToken(consumes<edm::View<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("VertexCollection"))),
    
    cfg_electronToken(consumes<pat::ElectronCollection>(iConfig.getParameter<edm::InputTag>("ElectronCollection"))),
    cfg_rhoToken(consumes<double>(iConfig.getParameter<edm::InputTag>("ElectronRhoSource"))),
    cfg_electronID(iConfig.getParameter<std::string>("ElectronID")),
    // Marina - start
    cfg_electronMVAToken(consumes<edm::ValueMap<float> >(iConfig.getParameter<edm::InputTag>("ElectronMVA"))),
    cfg_electronMiniRelIsoEA(iConfig.getParameter<double>("ElectronMiniRelIsoEA")),
    // Marina - end
    cfg_electronPtCut(iConfig.getParameter<double>("ElectronPtCut")),
    cfg_electronEtaCut(iConfig.getParameter<double>("ElectronEtaCut")),
    cfg_electronNCut(iConfig.getParameter<int>("ElectronNCut")),
    cfg_muonToken(consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("MuonCollection"))),
    cfg_muonID(iConfig.getParameter<std::string>("MuonID")),
    // Marina - start
    cfg_muonMiniRelIsoEA(iConfig.getParameter<double>("MuonMiniRelIsoEA")),
    // Marina - end
    cfg_muonPtCut(iConfig.getParameter<double>("MuonPtCut")),
    cfg_muonEtaCut(iConfig.getParameter<double>("MuonEtaCut")),
    cfg_muonNCut(iConfig.getParameter<int>("MuonNCut")),

    // Marina - start
    cfg_tauToken(consumes<edm::View<pat::Tau> >(iConfig.getParameter<edm::InputTag>("TauCollection"))),
    cfg_tauDiscriminators(iConfig.getParameter<std::vector<std::string> >("TauDiscriminators")),
    cfg_tauPtCut(iConfig.getParameter<double>("TauPtCut")),
    cfg_tauEtaCut(iConfig.getParameter<double>("TauEtaCut")),
    cfg_tauNCut(iConfig.getParameter<int>("TauNCut")),
    // Marina - end

    
    nEvents(0),
    nSelectedEvents(0)
{
  
}


Hplus2tbAnalysisSync::~Hplus2tbAnalysisSync(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "Hplus2tbAnalysisSync: " //  	edm::LogVerbatim("Hplus2tbAnalysisSync") 
	      << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
    
    std::cout<<"  Number of events passing electron veto = "<<nEventsPassedElectronVeto<<std::endl;
    std::cout<<"  Number of events passing muon veto     = "<<nEventsPassedMuonVeto<<std::endl;
    std::cout<<"  Number of events passing tau veto      = "<<nEventsPassedTauVeto<<std::endl;
    std::cout<<"  Number of events passing lepton veto   = "<<nEventsPassedLeptonVeto<<std::endl;
}


bool Hplus2tbAnalysisSync::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

    // ============================================================================================================================================================= Trigger bits
    edm::Handle<edm::TriggerResults> trghandle;
    iEvent.getByToken(cfg_trgResultsToken, trghandle);
    if(trghandle.isValid()){
        edm::TriggerResults tr = *trghandle;
        bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
        std::vector<std::string> hlNames; 
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);
	bool passed = false;
        bool trgBitFound = false;

	if (cfg_verbose) std::cout << "=== Trigger bits:" << std::endl;
	if(cfg_triggerBits.size() > 0){
          for(size_t i = 0; i < cfg_triggerBits.size(); ++i){
	    std::regex hlt_re(cfg_triggerBits[i]);
	    int n = 0;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
	      // if (cfg_verbose) std::cout << "\t" << *j << std::endl;
	      if (std::regex_search(*j, hlt_re)) {

		  if (cfg_verbose) std::cout << "\t" << *j << " = " << trghandle->accept(n) << std::endl;
		  trgBitFound = true;
		    if(trghandle->accept(n)) {
			passed = true;
                        break;
		    }
                }
		n++;
            }
          }
          if(!trgBitFound) {
            std::cout << "Skimming with trigger bit, but none of the triggers was found!" << std::endl;
            std::cout << "Looked for triggers:" << std::endl;
            for (auto& p: cfg_triggerBits) {
                std::cout << "    " << p << std::endl;
            }
            
            std::cout << "Available triggers in dataset:" << std::endl;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
                std::cout << "    " << *j << std::endl;
            }
            exit(1);
          }
        }else passed = true;
	if(!passed) return false; 
    }
    else
      {
	// trghandle.isValid() == False:
	// If the trigger handle is not valid, The event will always be accepted, regardless of whether any of the skim trigger-bits are true or not.
	// So for example, all non-reHLT samples will NOT be skimmed by any trigger. Instead all events will be regarded as having passed the skim trigger.
      }

    if (cfg_verbose) 
      {
	std::cout << "=== Passed Trigger:\n\t" << std::endl;
	for (auto& p: cfg_triggerBits) std::cout << p << "\n";
	std::cout << "\n" << std::endl;
      }	
    


    // ============================================================================================================================================================================= Jets
    edm::Handle<edm::View<pat::Jet> > jethandle;
    iEvent.getByToken(cfg_jetToken, jethandle);
    int nJets = 0;
    if(jethandle.isValid()){
      
      // For-loop: All jets
        for(size_t i=0; i<jethandle->size(); ++i) {
            const pat::Jet& obj = jethandle->at(i);

	    if(obj.p4().pt() < cfg_jetEtCut) continue;
	    if(fabs(obj.p4().eta()) > cfg_jetEtaCut) continue;
	    nJets++;
	}
    }
    // ============================================================================================================================================================================= AK8 Jets
    edm::Handle<edm::View<pat::Jet> > AK8jethandle;
    iEvent.getByToken(cfg_ak8jetToken, AK8jethandle);
    int ak8nJets = 0;
    if (AK8jethandle.isValid())
      {
	
	// FOr-loop: All AK8 jets
	for (unsigned i=0; i<AK8jethandle->size(); ++i)
	  {
	    const pat::Jet& obj = AK8jethandle->at(i);
	    
	    if (obj.p4().pt() < cfg_ak8jetEtCut) continue;
	    if (fabs(obj.p4().eta()) > cfg_ak8jetEtaCut) continue;
	    
	    

	    std::cout<<"Fat Jet ="<<i<<"   Pt = "<<obj.p4().pt()<<"   Eta = "<<obj.p4().eta()<<std::endl;
	    
	    
	    
	    ak8nJets++;
	  }
      }
    
    //============================================================================================================================================================================== Electrons
   
    edm::Handle<edm::View<reco::Vertex> > vertexHandle;
    iEvent.getByToken(cfg_vertexToken, vertexHandle);
    
    // Electrons
    edm::Handle<pat::ElectronCollection>  electronHandle;
    iEvent.getByToken(cfg_electronToken, electronHandle);
    int nElectrons = 0;
    
    edm::Handle<edm::ValueMap<float> > electronMVAHandle;
    iEvent.getByToken(cfg_electronMVAToken, electronMVAHandle);

    // Packed Candidates
    edm::Handle<edm::View<pat::PackedCandidate> > pfcandHandle;
    iEvent.getByToken(cfg_pfcandsToken, pfcandHandle);

    // Setup handles for rho
    edm::Handle<double> rhoHandle;
    iEvent.getByToken(cfg_rhoToken, rhoHandle);
    
    if(electronHandle.isValid()){
      
      // For-loop: All electrons
      int iEle = -1;
      for (const pat::Electron &obj: *electronHandle){
	
	iEle++;
	edm::RefToBase<pat::Electron> ref ( edm::Ref<pat::ElectronCollection >(electronHandle, iEle));
	
	// Calculate Mini relative isolarion for the electron with effective area
	double miniRelIsoEA = getMiniIsolation_EffectiveArea(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false, false, *rhoHandle);
	
	// Find a way to do the MVA thingie
	float mvaValue = (*electronMVAHandle)[ref];
	float AbsEta = fabs(obj.p4().eta());
	
	bool isLoose = false;
	if (AbsEta <= 0.8 and mvaValue >= -0.041)
	  {
	    isLoose = true;
	  }
	if (AbsEta > 0.8 and AbsEta < 1.479 and mvaValue >= 0.383)
	  {
	    isLoose = true;
	  }
	if (AbsEta >= 1.479 and mvaValue >= -0.515)
	  {
	    isLoose = true;
	  }
	
	//std::cout<<"Electron "<<iEle<<"  with mva value = "<<mvaValue<<"   and |eta|="<<AbsEta<<"  is Loose ="<<isLoose<<std::endl;
	// Apply acceptance cuts
	if (!isLoose) continue;	
	if (miniRelIsoEA > cfg_electronMiniRelIsoEA) continue;
	if(obj.p4().pt() < cfg_electronPtCut) continue;
	if(fabs(obj.p4().eta()) > cfg_electronEtaCut) continue;
	nElectrons++;
      }
    }
    
    //======================================================================================================================================================================== Muons
    edm::Handle<edm::View<pat::Muon> > muonHandle;
    iEvent.getByToken(cfg_muonToken, muonHandle);
    
    int nMuons = 0;
    if(muonHandle.isValid()){
      
      // For-loop: All muons
      for(size_t i = 0; i < muonHandle->size(); ++i) {
	const pat::Muon& obj = muonHandle->at(i);
	
	// bool isGlobal = obj.isGlobalMuon();
	bool isLoose  = obj.isLooseMuon();
	bool isMedium = obj.isMediumMuon();
	bool isTight  = false;
	if (vertexHandle->size() == 0) 
	  {
	    isTight = false;
	  } 
	else 
	  {
	    isTight = obj.isTightMuon(vertexHandle->at(0));
	  }
        
	// Apply muon selections
	double miniRelIsoEA = getMiniIsolation_EffectiveArea(pfcandHandle, dynamic_cast<const reco::Candidate *>(&obj), 0.05, 0.2, 10., false, false, *rhoHandle);
	
	if (cfg_muonID == "loose" || cfg_muonID == "Loose") 
	  {
	    if (isLoose  == false) continue;
	  } 
	else if (cfg_muonID == "medium" || cfg_muonID == "Medium") 
	  {
	    if (isMedium == false) continue;
	  } 
	else if (cfg_muonID == "tight" || cfg_muonID == "Tight") 
	  {
	    if (isTight == false) continue;
	  } 
	else {
	  throw cms::Exception("config") << "Invalid muonID option '" << cfg_muonID << "'! Options: 'loose', 'medium', 'tight'";
	} 
	
	// Apply acceptance cuts
	if (miniRelIsoEA > cfg_muonMiniRelIsoEA)  continue;
	if(obj.p4().pt() < cfg_muonPtCut)         continue;
	if(fabs(obj.p4().eta()) > cfg_muonEtaCut) continue;
	
	nMuons++;
      }
    }

    //===================================================================================================================================================================== Taus
    edm::Handle<edm::View<pat::Tau> > tauHandle;
    iEvent.getByToken(cfg_tauToken, tauHandle);

    int nTaus = 0;
    
    if(tauHandle.isValid()){
      
      // For-loop: All taus
      for (const pat::Tau &obj: *tauHandle){
	
	if (obj.p4().pt() < cfg_tauPtCut) continue;
	if (fabs(obj.p4().eta()) > cfg_tauEtaCut) continue;
	
	bool d = true;
	for(size_t j=0; j<cfg_tauDiscriminators.size(); ++j) {
	  d = d && obj.tauID(cfg_tauDiscriminators[j]);
	}
	if(!d) continue;
	nTaus++;
      }
    }
    //===================================================================================================================================================================== Passed all selections
    
    if (nElectrons <= cfg_electronNCut) nEventsPassedElectronVeto++;
    if (nMuons     <= cfg_muonNCut)     nEventsPassedMuonVeto++;
    if (nTaus      <= cfg_tauNCut)      nEventsPassedTauVeto++;
    
    // Apply Electron Veto
    if(nElectrons > cfg_electronNCut) return false;
    if (cfg_verbose) std::cout << "=== nElectrons:\n\t" << nElectrons << " < " << cfg_electronNCut << std::endl;
    
    // Apply Muon Veto
    if(nMuons > cfg_muonNCut) return false;
    if (cfg_verbose) std::cout << "=== Passed Muons:\n\t" << nMuons << " < " << cfg_muonNCut << std::endl;
    
    // Apply Tau Veto
    //if (nTaus > cfg_tauNCut) return false;
    //if (cfg_verbose) std::cout<< "=== Passed Taus:\n\t" << nTaus << " < "<< cfg_tauNCut << std::endl;
    
    nEventsPassedLeptonVeto++;
    
    // Apply Jet Selections
    if(nJets < cfg_nJets) return false;
    if (cfg_verbose) std::cout << "=== Passed Jets:\n\t" << nJets << " > " << cfg_nJets << std::endl;
    
    // All selections passed
    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(Hplus2tbAnalysisSync);   

