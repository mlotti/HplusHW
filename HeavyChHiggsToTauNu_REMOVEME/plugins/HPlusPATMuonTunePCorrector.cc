#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/MuonReco/interface/MuonCocktails.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

// https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#New_Version_recommended
class HPlusPATMuonTunePCorrector: public edm::EDProducer {
public:
  explicit HPlusPATMuonTunePCorrector(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src")),
    fOriginalSrc(iConfig.getParameter<edm::InputTag>("originalSrc")),
    fIdFunction(iConfig.getParameter<std::string>("idCut"), true),
    fIdMaxChi2(iConfig.getParameter<double>("idMaxChi2")),
    fIdMaxPtError(iConfig.getParameter<double>("idMaxPtError")),
    fDoId(iConfig.getParameter<bool>("finalizeId"))
  {
    produces<std::vector<pat::Muon> >();
    produces<std::vector<pat::Muon> >("original");
  }
  ~HPlusPATMuonTunePCorrector() {}

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fSrc, hmuons);

    edm::Handle<edm::View<pat::Muon> > hmuonsOrig;
    iEvent.getByLabel(fOriginalSrc, hmuonsOrig);

    if(hmuons->size() != hmuonsOrig->size())
      throw cms::Exception("Assert") << "Muon " << fSrc.encode() << " size " << hmuons->size()
                                     << " != original muon " << fOriginalSrc.encode() << " size " << hmuonsOrig->size();

    std::auto_ptr<std::vector<pat::Muon> > prod(new std::vector<pat::Muon>());
    std::auto_ptr<std::vector<pat::Muon> > prodOrig(new std::vector<pat::Muon>());

    for(size_t iMuon=0; iMuon<hmuons->size(); ++iMuon) {
      // Make copy of the original
      pat::Muon copy = (*hmuons)[iMuon];

      //throw cms::Exception("NotYetImplemented") << "TuneP needs update of DataFormats/MuonReco, which is not yet integrated to the common checkoutTags.sh in " << __FILE__ << ":" << __LINE__;
      reco::Muon::MuonTrackTypePair cktTrackType = (muon::tevOptimized(copy, 200, 30., 0., 0.25));
      if(copy.pt() < 200.0 && cktTrackType.first->pt() < 200.0) {
        if(fDoId) {
          if(copy.normChi2() >= fIdMaxChi2) {
            continue;
          }
          if(!fIdFunction(copy)) {
            continue;
          }
        }
      }
      else { // TuneP correction
        if(fDoId) {
          if(cktTrackType.first->ptError()/cktTrackType.first->pt() >= fIdMaxPtError) {
            continue;
          }
          if(!fIdFunction(copy)) {
            continue;
          }
        }
        math::XYZTLorentzVector p4 = copy.p4();
        p4.SetPx(cktTrackType.first->px());
        p4.SetPy(cktTrackType.first->py());
        p4.SetPz(cktTrackType.first->pz());
        copy.setP4(p4);
      }

      prod->push_back(copy);
      prodOrig->push_back((*hmuonsOrig)[iMuon]);
    };

    iEvent.put(prod);
    iEvent.put(prodOrig, "original");
  }

private:
  const edm::InputTag fSrc;
  const edm::InputTag fOriginalSrc;
  StringCutObjectSelector<pat::Muon> fIdFunction;
  const double fIdMaxChi2;
  const double fIdMaxPtError;
  const bool fDoId;
};

DEFINE_FWK_MODULE( HPlusPATMuonTunePCorrector );
