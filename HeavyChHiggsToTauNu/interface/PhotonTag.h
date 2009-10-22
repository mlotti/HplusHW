// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_PhotonTag_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_PhotonTag_h

#include<map>
#include<string>

namespace reco { 
  class Photon;
  class Conversion;
}

class PhotonTag {
public:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::Photon&, TagType&);
  static void tag(const reco::Conversion&, TagType &);
};

#endif
