#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"

#include<cmath>

namespace {
  class ReweightBase {
  public:
    ReweightBase() {}
    virtual ~ReweightBase() {};
    virtual double getWeight(const TtGenEvent& ttGenEvent) const = 0;
  };

  // From https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
  // Use combined for all cases
  class TopPtReweightComb: public ReweightBase {
  public:
    explicit TopPtReweightComb(const edm::ParameterSet& pset):
      a(pset.getParameter<double>("a")),
      b(pset.getParameter<double>("b"))
    {}
    ~TopPtReweightComb() {}

    double getWeight(const TtGenEvent& ttGenEvent) const {
      const reco::GenParticle *top = ttGenEvent.top();
      const reco::GenParticle *topBar = ttGenEvent.topBar();
      if(!top) throw cms::Exception("Assert") << "Got null from ttGenEvent.top() in " << __FILE__ << ":" << __LINE__;
      if(!topBar) throw cms::Exception("Assert") << "Got null from ttGenEvent.topBar() in " << __FILE__ << ":" << __LINE__;

      return std::sqrt( sf(top) * sf(topBar) );
    }

  private:
    double sf(const reco::GenParticle *t) const { return sf(t->pt()); }
    double sf(double pt) const {
      if(pt > 400.0)
        return 1.0;
      return std::exp(a + b*pt);
    }

    const double a, b;
  };

  // From https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
  // Treat l+jets and dilepton separately, use 1.0 weight for all others
  class TopPtReweight: public ReweightBase {
  public:
    explicit TopPtReweight(const edm::ParameterSet& pset):
      ljets_a(pset.getParameter<double>("ljets_a")),
      ljets_b(pset.getParameter<double>("ljets_b")),
      dil_a(pset.getParameter<double>("dilepton_a")),
      dil_b(pset.getParameter<double>("dilepton_b")),
      tauIsNotLepton(pset.getParameter<bool>("treatTauAsNonLepton"))
    {}
    ~TopPtReweight() {}

    double getWeight(const TtGenEvent& ttGenEvent) const {
      if(ttGenEvent.isSemiLeptonic(tauIsNotLepton)) {
        const reco::GenParticle *lepTop = ttGenEvent.leptonicDecayTop();
        const reco::GenParticle *hadTop = ttGenEvent.hadronicDecayTop();
        if(!lepTop) throw cms::Exception("Assert") << "Got null from ttGenEvent.leptonicDecayTop() in " << __FILE__ << ":" << __LINE__;
        if(!hadTop) throw cms::Exception("Assert") << "Got null from ttGenEvent.hadronicDecayTop() in " << __FILE__ << ":" << __LINE__;
        
        return std::sqrt( sf_ljets(lepTop) * sf_ljets(hadTop) );
      }
      else if(ttGenEvent.isFullLeptonic(tauIsNotLepton)) {
        const reco::GenParticle *top = ttGenEvent.top();
        const reco::GenParticle *topBar = ttGenEvent.topBar();
        if(!top) throw cms::Exception("Assert") << "Got null from ttGenEvent.top() in " << __FILE__ << ":" << __LINE__;
        if(!topBar) throw cms::Exception("Assert") << "Got null from ttGenEvent.topBar() in " << __FILE__ << ":" << __LINE__;

        return std::sqrt( sf_dil(top) * sf_dil(topBar) );
      }

      return 1.0;
    }

  private:
    double sf_ljets(const reco::GenParticle *t) const { return sf_ljets(t->pt()); }
    double sf_ljets(double pt) const {
      if(pt > 400.0)
        return 1.0;
      return std::exp(ljets_a + ljets_b*pt);
    }
    double sf_dil(const reco::GenParticle *t) const { return sf_dil(t->pt()); }
    double sf_dil(double pt) const {
      if(pt > 400.0)
        return 1.0;
      return std::exp(dil_a + dil_b*pt);
    }

    const double ljets_a, ljets_b;
    const double dil_a, dil_b;
    const bool tauIsNotLepton;
  };


  // From https://indico.cern.ch/getFile.py/access?contribId=19&sessionId=2&resId=0&materialId=slides&confId=267832 and AN-2013-145
  class TopPtReweightTTH: public ReweightBase {
  public:
    explicit TopPtReweightTTH(const edm::ParameterSet& pset):
      a(pset.getParameter<double>("a")),
      b(pset.getParameter<double>("b")),
      c(pset.getParameter<double>("c")),
      constant(pset.getParameter<double>("constant"))
    {}
    ~TopPtReweightTTH() {}

    double getWeight(const TtGenEvent& ttGenEvent) const {
      const reco::GenParticle *top = ttGenEvent.top();
      const reco::GenParticle *topBar = ttGenEvent.topBar();
      if(!top) throw cms::Exception("Assert") << "Got null from ttGenEvent.top() in " << __FILE__ << ":" << __LINE__;
      if(!topBar) throw cms::Exception("Assert") << "Got null from ttGenEvent.topBar() in " << __FILE__ << ":" << __LINE__;

      return std::sqrt( sf(top) * sf(topBar) );
    }
  private:
    double sf(const reco::GenParticle* t) const { return sf(t->pt()); }
    double sf(double pt) const {
      if(pt > c) 
        return constant;
      return a + b*pt * (pt-2*c);
    }

    const double a, b, c;
    const double constant;        
  };

  ReweightBase *weightFactory(const edm::ParameterSet& iConfig) {
    std::string mode = iConfig.getParameter<std::string>("mode");
    const edm::ParameterSet modePSet = iConfig.getParameter<edm::ParameterSet>(mode);
    if(mode == "TopPtCombined")
      return new TopPtReweightComb(modePSet);
    else if(mode == "TopPtSeparate")
      return new TopPtReweight(modePSet);
    else if(mode == "TTH")
      return new TopPtReweightTTH(modePSet);
    throw cms::Exception("Configuration") << "Invalid value '" << mode << "' for parameter 'mode', valid values are TopPtCombined, TopPtSeparated, TTH";
  }
}


class HPlusTopPtWeightProducer: public edm::EDProducer {
public:
  explicit HPlusTopPtWeightProducer(const edm::ParameterSet&);
  ~HPlusTopPtWeightProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  const edm::InputTag fSrc;
  const std::string fAlias;
  const ReweightBase *weighter;
  const int fVariationDir;
  const bool fEnabled;
  const bool fVariationEnabled;
};

HPlusTopPtWeightProducer::HPlusTopPtWeightProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("ttGenEventSrc")),
  fAlias(iConfig.getParameter<std::string>("alias")),
  weighter(weightFactory(iConfig)),
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
    
    weight = weighter->getWeight(*hGenEvent);
    if(fVariationEnabled) {
      if(fVariationDir < 0) {
        weight = 1.0;
      }
      else if(fVariationDir > 0) {
        weight = weight*weight; // FIXME: this is probably wrong for TTH, but it is not clear from the AN what exactly they do
      }
    }
  }

  iEvent.put(std::auto_ptr<double>(new double(weight)));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTopPtWeightProducer);
