// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ElectronTag_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ElectranTag_h

#include<map>
#include<string>

namespace reco { class GsfElectron; }
namespace pat { class Electron; }
class EcalClusterLazyTools;

class ElectronTag {
public:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::GsfElectron *, EcalClusterLazyTools&, TagType&);
  static void tag(const pat::Electron&, TagType &);
};

#endif
