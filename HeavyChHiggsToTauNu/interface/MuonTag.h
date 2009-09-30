// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MuonTag_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MuonTag_h

#include<map>
#include<string>

namespace reco { class Muon; }
namespace pat { class Muon; }

class MuonTag {
public:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::Muon&, TagType&);
  static void tag(const pat::Muon&, TagType&);
};

#endif
