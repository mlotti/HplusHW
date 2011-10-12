#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

#include<vector>

class HPlusJetEnergyScaleVariation: public edm::EDProducer {
public:
  explicit HPlusJetEnergyScaleVariation(const edm::ParameterSet&);
  ~HPlusJetEnergyScaleVariation();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag src;
  std::string payloadName;
  std::string uncertaintyTag;

  std::vector<double> etaBins;
  std::vector<bool> plusVariations;
  bool defaultPlusVariation;
};

HPlusJetEnergyScaleVariation::HPlusJetEnergyScaleVariation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  payloadName(iConfig.getParameter<std::string>("payloadName")),
  uncertaintyTag(iConfig.getParameter<std::string>("uncertaintyTag")),
  defaultPlusVariation(iConfig.getParameter<bool>("defaultPlusVariation"))
{
  std::vector<edm::ParameterSet> bins = iConfig.getParameter<std::vector<edm::ParameterSet> >("etaBins");
  etaBins.reserve(bins.size());
  plusVariations.reserve(bins.size());
  for(size_t i=0; i<bins.size(); ++i) {
    double eta = bins[i].getParameter<double>("maxEta");
    if(!etaBins.empty() && eta >= etaBins.back())
      throw cms::Exception("Configuration") << "Bins must be in ascending order of etas (new "
                                            << eta << " previous " << etaBins.back() << ")" << std::endl;
    etaBins.push_back(eta);
    plusVariations.push_back(bins[i].getParameter<bool>("plusVariation"));
  }

  produces<pat::JetCollection>();
  
}
HPlusJetEnergyScaleVariation::~HPlusJetEnergyScaleVariation() {}

void HPlusJetEnergyScaleVariation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<pat::JetCollection> rescaledJets(new pat::JetCollection);

  typedef pat::Jet::LorentzVector LorentzVector;

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(src, hjets);

  edm::ESHandle<JetCorrectorParametersCollection> jetCorParColl;
  iSetup.get<JetCorrectionsRecord>().get(payloadName, jetCorParColl); 
  JetCorrectorParameters const &jetCorPar = (*jetCorParColl)[uncertaintyTag];
  JetCorrectionUncertainty jecUnc(jetCorPar);
  
  for(edm::View<pat::Jet>::const_iterator iJet = hjets->begin(); iJet != hjets->end(); ++iJet) {
    // JEC uncertainty is a function of corrected jet eta and pt
    jecUnc.setJetEta(iJet->eta());
    jecUnc.setJetPt(iJet->pt());
    
    bool plusVariation = defaultPlusVariation;
    std::vector<double>::const_iterator found = std::upper_bound(etaBins.begin(), etaBins.end(), iJet->eta());
    if(found != etaBins.end()) {
      size_t index = found - etaBins.begin();
      plusVariation = plusVariations[index];
      //std::cout << "Jet eta " << iJet->eta() << " index " << index << std::endl;
    }
    else {
      //std::cout << "Jet eta " << iJet->eta() << " using default " << std::endl;
    }

    // argument controls plus/minus variation (asymmetric uncertainty)
    double myChange = jecUnc.getUncertainty(plusVariation);
    double myFactor = 1. + myChange;
    LorentzVector p4 = iJet->p4()*myFactor; 

    pat::Jet jet = *iJet;
    jet.setP4(iJet->p4()*myFactor);
    jet.addUserFloat("originalPx", iJet->px());
    jet.addUserFloat("originalPy", iJet->py());
    rescaledJets->push_back(jet);
  }
  iEvent.put(rescaledJets);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetEnergyScaleVariation);
