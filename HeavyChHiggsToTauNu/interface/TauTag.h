// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauTag_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauTag_h

#include<map>
#include<string>

namespace reco { 
  class IsolatedTauTagInfo;
  class CaloTau;
  class PFTau;
}
namespace pat { class Tau; }

class TauTag {
public:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::IsolatedTauTagInfo&, TagType&);
  static void tag(const reco::CaloTau&, TagType&);
  static void tag(const pat::Tau&, TagType&);
  static void tag(const reco::PFTau&, TagType&);

};

#endif
