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

  MyJet convert(edm::Handle<edm::View<reco::GsfElectron> >&, size_t i);
  MyJet convert(edm::Handle<edm::View<pat::Electron> >& handle, size_t i);

private:
  template <class T>
  MyJet helper(const T&) const;

  void tag(const reco::GsfElectron&, TagType&);
  void tag(const pat::Electron&, TagType &) const;

  const TransientTrackBuilder& transientTrackBuilder;
  const ImpactParameterConverter& ipConverter;
  EcalClusterLazyTools& clusterTools;

  const edm::Event& iEvent;
  const std::vector<edm::InputTag>& tagLabels;
};

#endif
