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
  bool doVariation;
};

HPlusJetEnergyScaleVariation::HPlusJetEnergyScaleVariation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  payloadName(iConfig.getParameter<std::string>("payloadName")),
  uncertaintyTag(iConfig.getParameter<std::string>("uncertaintyTag")),
  defaultPlusVariation(iConfig.getParameter<bool>("defaultPlusVariation")),
  doVariation(iConfig.getParameter<bool>("doVariation"))
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
  typedef pat::Jet::LorentzVector LorentzVector;

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(src, hjets);

  std::auto_ptr<pat::JetCollection> rescaledJets(new pat::JetCollection);
  rescaledJets->reserve(hjets->size());

  edm::ESHandle<JetCorrectorParametersCollection> jetCorParColl;
  iSetup.get<JetCorrectionsRecord>().get(payloadName, jetCorParColl); 
  JetCorrectorParameters const &jetCorPar = (*jetCorParColl)[uncertaintyTag];
  JetCorrectionUncertainty jecUnc(jetCorPar);
  /*
  std::cout << "JetCorrectorParameters "
            << " (0)xmin(0) " << jetCorPar.record(0).xMin(0)
            << " (0)xmax(0) " << jetCorPar.record(0).xMax(0)
            << " (-1)xmin(0) " << jetCorPar.record(jetCorPar.size()-1).xMin(0)
            << " (-1)xmax(0) " << jetCorPar.record(jetCorPar.size()-1).xMax(0)
            << " binVars " << jetCorPar.definitions().binVar().size()
            << " binVar(0) " << jetCorPar.definitions().binVar(0)
            << " parVar(0) " << jetCorPar.definitions().parVar(0)
            << std::endl;
  */

  // Hack to be able to work with jets with |eta| > 5.5
  const size_t etaIndex = 0;
  if(jetCorPar.definitions().binVar(etaIndex) != "JetEta") {
    throw cms::Exception("Assert") << "Assumption that JetEta has the index " << etaIndex << " in jetCorPar failed at " << __FILE__ << ":" << __LINE__ << std::endl;
  }
  const float etaMin = jetCorPar.record(0).xMin(etaIndex);
  const float etaMax = jetCorPar.record(jetCorPar.size()-1).xMax(etaIndex);
  if(etaMin >= etaMax)
    throw cms::Exception("Assert") << "etaMin (" << etaMin << ") >= etaMax (" << etaMax << ") at " << __FILE__ << ":" << __LINE__ << std::endl;
  
  for(edm::View<pat::Jet>::const_iterator iJet = hjets->begin(); iJet != hjets->end(); ++iJet) {
    // JEC uncertainty is a function of corrected jet eta and pt
    double eta = iJet->eta();
    if(eta < etaMin) eta = etaMin + 1e-5;
    else if(eta > etaMax) eta = etaMax - 1e-5;
               
    jecUnc.setJetEta(eta);
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

    /*
    std::cout << "Jet i " << (iJet-hjets->begin()) 
              << " pt " << iJet->pt() 
              << " eta " << eta
              << " variation " << plusVariation
              << std::endl;
    */

    // argument controls plus/minus variation (asymmetric uncertainty)
    double myChange = jecUnc.getUncertainty(plusVariation);
    double myFactor = 1. + myChange;
    LorentzVector p4 = iJet->p4()*myFactor; 

    pat::Jet jet = *iJet;
    if(doVariation)
      jet.setP4(iJet->p4()*myFactor);
    jet.addUserFloat("originalPx", iJet->px());
    jet.addUserFloat("originalPy", iJet->py());
    /*
    std::cout << "Jet i " << (iJet-hjets->begin()) 
              << " original " << iJet->pt() << " " << iJet->p4()
              << " variated " << jet.pt() << " " << jet.p4()
              << std::endl;
    */
    rescaledJets->push_back(jet);
  }
  iEvent.put(rescaledJets);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetEnergyScaleVariation);
