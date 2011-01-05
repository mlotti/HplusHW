#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "TH1F.h"

#include<vector>
#include<string>
#include<cstdio>
#include<algorithm>

namespace {
  template <typename T>
  class Construct {
  public:
    Construct(TFileDirectory& fd, const TH1F& prototype, int *hindex): fd_(fd), prototype_(prototype), hindex_(hindex) {}

    T operator()(const edm::ParameterSet& pset) {
      return T(pset, fd_, prototype_, hindex_);
    }

  private:
    TFileDirectory& fd_;
    const TH1F& prototype_;
    int *hindex_;
  };

  template <typename T, typename S>
  T select(const T& collection, const S& selector) {
    T tmp;
    for(typename T::const_iterator iCand = collection.begin(); iCand != collection.end(); ++iCand) {
      if(selector(**iCand))
        tmp.push_back(*iCand);
    }
    return tmp;
  }

  template <typename T1, typename T2>
  T1 cleanCollection(const T1& collection, const T2& cand, double dR) {
    T1 tmp;
    for(typename T1::const_iterator iCand = collection.begin(); iCand != collection.end(); ++iCand) {
      if(deltaR(**iCand, cand) >= dR)
        tmp.push_back(*iCand);
    }
    return tmp;
  }
}


class HPlusMuonJetMetAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusMuonJetMetAnalyzer(const edm::ParameterSet&);
  ~HPlusMuonJetMetAnalyzer();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag muonSrc_;
  edm::InputTag jetSrc_;
  edm::InputTag metSrc_;

  template <typename T>
  struct CandSelector {
    explicit CandSelector(const edm::ParameterSet& pset, TFileDirectory& fd, const TH1F& prototype, int *hindex):
      selector(pset.getUntrackedParameter<std::string>("cut"))
    {
      histo = fd.make<TH1F>(prototype);
      char tmp[10] = "";
      std::snprintf(tmp, 10, "h%02d_", *hindex);
      *hindex += 1;
      histo->SetName((tmp+pset.getUntrackedParameter<std::string>("name")).c_str());
    }

    StringCutObjectSelector<T> selector;
    TH1F *histo;
  };

  typedef CandSelector<pat::Jet> JetSelector;
  typedef CandSelector<pat::Muon> MuonSelector;

  TH1F *hAllMet;

  std::vector<JetSelector> jetSelectors_;
  std::vector<MuonSelector> muonSelectors_;
  const unsigned njets_;
};

HPlusMuonJetMetAnalyzer::HPlusMuonJetMetAnalyzer(const edm::ParameterSet& iConfig):
  muonSrc_(iConfig.getUntrackedParameter<edm::InputTag>("muonSrc")),
  jetSrc_(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc")),
  metSrc_(iConfig.getUntrackedParameter<edm::InputTag>("metSrc")),
  njets_(iConfig.getUntrackedParameter<unsigned>("njets"))
{
  edm::Service<TFileService> fs;

  hAllMet = fs->make<TH1F>("h00_All", "MET", 200, 0., 200.);
  int hindex=1;

  std::vector<edm::ParameterSet> jetSelections = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("jetSelections");
  jetSelectors_.reserve(jetSelections.size());
  std::transform(jetSelections.begin(), jetSelections.end(), std::back_inserter(jetSelectors_), Construct<JetSelector>(*fs, *hAllMet, &hindex));

  std::vector<edm::ParameterSet> muonSelections = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("muonSelections");
  muonSelectors_.reserve(muonSelections.size());
  std::transform(muonSelections.begin(), muonSelections.end(), std::back_inserter(muonSelectors_), Construct<MuonSelector>(*fs, *hAllMet, &hindex));

}

HPlusMuonJetMetAnalyzer::~HPlusMuonJetMetAnalyzer() {}

void HPlusMuonJetMetAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Muon> > hmuons;
  iEvent.getByLabel(muonSrc_, hmuons);
  edm::PtrVector<pat::Muon> selectedMuons = hmuons->ptrVector();

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(jetSrc_, hjets);
  edm::PtrVector<pat::Jet> selectedJets = hjets->ptrVector();

  edm::Handle<edm::View<pat::MET> > hmet;
  iEvent.getByLabel(metSrc_, hmet);

  double met = hmet->at(0).et();
  hAllMet->Fill(met);

  for(std::vector<JetSelector>::iterator iSel = jetSelectors_.begin(); iSel != jetSelectors_.end(); ++iSel) {
    selectedJets = select(selectedJets, iSel->selector);
    if(selectedJets.size() < njets_)
      break;
    
    iSel->histo->Fill(met);
  }
  if(selectedJets.size() < njets_)
    return;


  edm::PtrVector<pat::Jet> selectedJetsOriginal = selectedJets;
  for(std::vector<MuonSelector>::iterator iSel = muonSelectors_.begin(); iSel != muonSelectors_.end(); ++iSel) {
    selectedMuons = select(selectedMuons, iSel->selector);
    if(selectedMuons.empty())
      break;
    selectedJets = cleanCollection(selectedJetsOriginal, *(selectedMuons[0]), 0.1);
    if(selectedJets.size() < njets_)
      break;

    iSel->histo->Fill(met);
  }
  if(selectedMuons.empty() || selectedJets.size() < njets_)
    return;

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMuonJetMetAnalyzer);
