// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MuonConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MuonConverter_h

#include<map>
#include<string>

#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

namespace reco { class Muon; }
namespace pat { class Muon; }
class TransientTrackBuilder;

class ImpactParameterConverter;

class MuonConverter {
public:
  MuonConverter(const TransientTrackBuilder&, const ImpactParameterConverter&);
  ~MuonConverter();

  template <class T> MyJet convert(edm::Handle<T>& handle, size_t i) const {
    return convert((*handle)[i]);
  }

  MyJet convert(const reco::Muon&) const;
  MyJet convert(const pat::Muon&) const;

private:
  template <class T> MyJet helper(const T&) const;

  typedef std::map<std::string, double> TagType;

  void tag(const reco::Muon&, TagType&) const;
  void tag(const pat::Muon&, TagType&) const;
  template <class T> void tagHelper(const T&, TagType&) const;

  const TransientTrackBuilder& transientTrackBuilder;
  const ImpactParameterConverter& ipConverter;
};

#endif
