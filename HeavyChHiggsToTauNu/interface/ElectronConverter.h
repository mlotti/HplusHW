// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ElectronConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ElectronConverter_h

#include<map>
#include<string>

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

namespace reco { class GsfElectron; }
namespace pat { class Electron; }
class EcalClusterLazyTools;
class TransientTrackBuilder;

class ImpactParameterConverter;

class ElectronConverter {
public:
  typedef std::map<std::string, double> TagType;

  ElectronConverter(const TransientTrackBuilder&, const ImpactParameterConverter&, EcalClusterLazyTools&);
  ~ElectronConverter();

  MyJet convert(const reco::GsfElectron&) const;
  MyJet convert(const pat::Electron&) const;

  void tag(const reco::GsfElectron&, TagType&);
  void tag(const pat::Electron&, TagType &) const;

private:
  const TransientTrackBuilder& transientTrackBuilder;
  const ImpactParameterConverter& ipConverter;
  EcalClusterLazyTools& clusterTools;
};

#endif
