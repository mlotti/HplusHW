// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_PhotonConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_PhotonConverter_h

#include<map>
#include<string>

#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

namespace reco { 
  class Photon;
  class Conversion;
}
class TransientTrackBuilder;

class TrackConverter;
class ImpactParameterConverter;

class PhotonConverter {
public:
  PhotonConverter(const TrackConverter&, const ImpactParameterConverter&, const TransientTrackBuilder&);
  ~PhotonConverter();

  template <class T> MyJet convert(edm::Handle<T>& handle, size_t i) const {
    return convert((*handle)[i]);
  }

  MyJet convert(const reco::Photon&) const;
  MyJet convert(const reco::Conversion&) const;

private:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::Photon&, TagType&);
  static void tag(const reco::Conversion&, TagType &);

  const TrackConverter& trackConverter;
  const ImpactParameterConverter& ipConverter;
  const TransientTrackBuilder& transientTrackBuilder;
};

#endif
