// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ElectronConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ElectronConverter_h

#include<map>
#include<string>
#include<vector>

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

namespace reco { class GsfElectron; }
namespace pat { class Electron; }
namespace edm {
  class Event;
  class InputTag;
}
class EcalClusterLazyTools;
class TransientTrackBuilder;

class ImpactParameterConverter;

class ElectronConverter {
public:
  typedef std::map<std::string, double> TagType;

  ElectronConverter(const TransientTrackBuilder&, const ImpactParameterConverter&, EcalClusterLazyTools&,
                    const edm::Event&, const std::vector<edm::InputTag>&);
  ~ElectronConverter();

  MyJet convert(edm::Handle<edm::View<reco::GsfElectron> >&, size_t);
  MyJet convert(edm::Handle<edm::View<pat::Electron> >&, size_t);

private:
  template <class T>
  MyJet helper(const edm::Ref<edm::View<T> >&);

  void tag(const edm::Ref<edm::View<reco::GsfElectron> >&, TagType&);
  void tag(const edm::Ref<edm::View<pat::Electron> >&, TagType &);

  const TransientTrackBuilder& transientTrackBuilder;
  const ImpactParameterConverter& ipConverter;
  EcalClusterLazyTools& clusterTools;

  const edm::Event& iEvent;
  const std::vector<edm::InputTag>& tagLabels;
};

#endif
