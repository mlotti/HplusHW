#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TF1.h"

#include<cmath>

namespace {
  class WeightCalculator {
  public:
    explicit WeightCalculator(const edm::ParameterSet& iConfig):
      fSFFormulaAllHadronic("AllHadr", iConfig.getParameter<std::string>("allhadronic").c_str()),
      fSFFormulaLeptonJets("LepJets", iConfig.getParameter<std::string>("leptonjets").c_str()),
      fSFFormulaDiLepton("DiLep", iConfig.getParameter<std::string>("dilepton").c_str())
    {}
    ~WeightCalculator() {}

    double weight(const TtGenEvent& ttGenEvent) const {
      const reco::GenParticle *top = ttGenEvent.top();
      const reco::GenParticle *topBar = ttGenEvent.topBar();
      if(!top) throw cms::Exception("Assert") << "Got null from ttGenEvent.top() in " << __FILE__ << ":" << __LINE__;
      if(!topBar) throw cms::Exception("Assert") << "Got null from ttGenEvent.topBar() in " << __FILE__ << ":" << __LINE__;

      const double topPt = top->pt();
      const double topBarPt = topBar->pt();

      const int nleptons = HPlus::GenParticleTools::calculateTTBarNumberOfLeptons(ttGenEvent);
      switch(nleptons) {
      case 0: return fSFFormulaAllHadronic.Eval(topPt) * fSFFormulaAllHadronic.Eval(topBarPt);
      case 1: return fSFFormulaLeptonJets.Eval(topPt)  * fSFFormulaLeptonJets.Eval(topBarPt);
      case 2: return fSFFormulaDiLepton.Eval(topPt)    * fSFFormulaDiLepton.Eval(topBarPt);
      }
      throw cms::Exception("Assert") << "Got number of leptons " << nleptons << ", which is not 0,1,2 in " << __FILE__ << ":" << __LINE__;
    }

  private:
    const TF1 fSFFormulaAllHadronic;
    const TF1 fSFFormulaLeptonJets;
    const TF1 fSFFormulaDiLepton;
  };
}

class HPlusTopPtWeightProducer: public edm::EDProducer {
public:
  explicit HPlusTopPtWeightProducer(const edm::ParameterSet&);
  ~HPlusTopPtWeightProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  const edm::InputTag fSrc;
  const std::string fAlias;
  const WeightCalculator fWeightCalculator;
  const int fVariationDir;
  const bool fEnabled;
  const bool fVariationEnabled;
};

HPlusTopPtWeightProducer::HPlusTopPtWeightProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("ttGenEventSrc")),
  fAlias(iConfig.getParameter<std::string>("alias")),
  fWeightCalculator(iConfig.getParameter<edm::ParameterSet>(iConfig.getParameter<std::string>("scheme"))),
  fVariationDir(iConfig.getParameter<int>("variationDirection")),
  fEnabled(iConfig.getParameter<bool>("enabled")),
  fVariationEnabled(iConfig.getParameter<bool>("variationEnabled"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusTopPtWeightProducer::~HPlusTopPtWeightProducer() {}

void HPlusTopPtWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;

  if(fEnabled) {
    edm::Handle<TtGenEvent> hGenEvent;
    iEvent.getByLabel(fSrc, hGenEvent);
    
    weight = fWeightCalculator.weight(*hGenEvent);
    if(fVariationEnabled) {
      if(fVariationDir < 0) {
        weight = 1.0;
      }
      else if(fVariationDir > 0) {
        weight = weight*weight;
      }
    }
  }

  iEvent.put(std::auto_ptr<double>(new double(weight)));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTopPtWeightProducer);
