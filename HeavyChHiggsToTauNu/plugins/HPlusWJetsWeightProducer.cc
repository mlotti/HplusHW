#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include<cstdio>

class HPlusWJetsWeightProducer: public edm::EDProducer {
public:
  explicit HPlusWJetsWeightProducer(const edm::ParameterSet&);
  ~HPlusWJetsWeightProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  struct JetBin {
    JetBin(double ixs, double ievt, double exs, double eevt):
      fExclusiveInclusiveCrossSectionRatio(exs / ixs),
      fInclusiveNumberOfEvents(ievt), fExclusiveNumberOfEvents(eevt) {}

    double getWeight() {
      /*
       * Calculate weight for jet bin i as
       *
       *          f_i * N_inc        sigma_NNLO
       * w_i = ----------------- (* ---------- )
       *       N_inc * f_i + N_i       N_inc
       *
       * where
       * inc    denotes the inclusive sample
       * f_i    = sigma_LO(i) / sigma_LO(inc) (LO cross sections from PREP)
       * N_inc  Number of all processed MC events in the inclusive sample
       * N_i    Number of all processed MC events in the jet bin i sample
       *
       * The number of processed MC events should be PU-reweighted
       *
       * sigma_NNLO  The NNLO cross section
       *
       * In this code, the first part of the weight is calculated. The
       * plotting system then takes automatically care of the second
       * part.
       */

      double f_i = fExclusiveInclusiveCrossSectionRatio;
      double N_inc = fInclusiveNumberOfEvents;
      double N_i = fExclusiveNumberOfEvents;

      double weight = (f_i * N_inc) / (N_inc * f_i + N_i);
      return weight;
    }

    double fExclusiveInclusiveCrossSectionRatio;
    unsigned fInclusiveNumberOfEvents;
    unsigned fExclusiveNumberOfEvents;
  };


  std::vector<JetBin> fJetBins;

  edm::InputTag fSrc;
  std::string fAlias;
  bool fEnabled;
};

HPlusWJetsWeightProducer::HPlusWJetsWeightProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("lheSrc")),
  fAlias(iConfig.getParameter<std::string>("alias")),
  fEnabled(iConfig.getParameter<bool>("enabled"))
{

  fJetBins.reserve(4);
  char tmp[10] = "";
  for(int jetBin=2; jetBin <= 4; ++jetBin) {
    snprintf(tmp, 10, "jetBin%d", jetBin);
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>(tmp);
    fJetBins.push_back(JetBin(iConfig.getParameter<double>("inclusiveCrossSection"),
                              iConfig.getParameter<double>("inclusiveNevents"),
                              pset.getParameter<double>("exclusiveCrossSection"),
                              pset.getParameter<double>("exclusiveNevents")));
  }

  produces<double>().setBranchAlias(fAlias);
}
HPlusWJetsWeightProducer::~HPlusWJetsWeightProducer() {}

void HPlusWJetsWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;

  if(fEnabled) {
    edm::Handle<LHEEventProduct> hlhe;
    iEvent.getByLabel(fSrc, hlhe);

    // Number of partons,
    // 5 -> 0 partons
    // 6 -> 1 partons
    // 7 -> 2 partons
    // 8 -> 3 partons
    // 9 -> 4 partons
    int nup = hlhe->hepeup().NUP;
    if(nup <= 6) {
      weight = 1.0;
    }
    else if(nup > 6 && nup <= 9) {
      int njet = nup-5;
      weight = fJetBins[njet-2].getWeight();
    }
    else
      throw cms::Exception("Assert") << "Encountered event with NUP " << nup << std::endl;
    
  }

  iEvent.put(std::auto_ptr<double>(new double(weight)));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusWJetsWeightProducer);
