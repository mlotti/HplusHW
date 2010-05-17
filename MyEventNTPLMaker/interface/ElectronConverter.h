// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_ElectronConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_ElectronConverter_h

#include<map>
#include<string>
#include<vector>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

namespace reco { class GsfElectron; }
namespace pat { class Electron; }
namespace edm {
  class Event;
  class InputTag;
}
class EcalClusterLazyTools;
class TransientTrackBuilder;

class TrackConverter;
class ImpactParameterConverter;

class ElectronConverter {
public:
  typedef std::map<std::string, double> TagType;

  ElectronConverter(const TrackConverter&, const ImpactParameterConverter&, const TransientTrackBuilder&, EcalClusterLazyTools&,
                    const edm::Event&, const std::vector<edm::InputTag>&);
  ~ElectronConverter();

  MyJet convert(const edm::InputTag& src, edm::Handle<edm::View<reco::GsfElectron> >&, size_t);
  MyJet convert(const edm::InputTag& src, edm::Handle<edm::View<pat::Electron> >&, size_t);

private:
  template <class T>
  MyJet helper(const edm::Ref<edm::View<T> >&);

  void tag(const edm::Ref<edm::View<reco::GsfElectron> >&, TagType&);
  void tag(const edm::Ref<edm::View<pat::Electron> >&, TagType &);

  const TrackConverter& trackConverter;
  const ImpactParameterConverter& ipConverter;
  const TransientTrackBuilder& transientTrackBuilder;
  EcalClusterLazyTools& clusterTools;

  const edm::Event& iEvent;
  const std::vector<edm::InputTag>& tagLabels;
};

#endif
