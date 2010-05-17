// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_JetConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_JetConverter_h

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
//#include "DataFormats/JetReco/interface/CaloJet.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

#include<vector>
#include<string>

namespace edm { 
  class Event;
  class EventSetup;
  class InputTag;
}
namespace reco { class CaloJet; }
namespace pat { class Jet; }
class JetCorrector;

class TrackConverter;

class JetConverter {
public:
  JetConverter(const TrackConverter&, const edm::Event&, const edm::EventSetup&,
               const std::vector<std::string>& types, const std::vector<std::string>& btags);
  ~JetConverter();

  template <class T> MyJet convert(const edm::InputTag& src, edm::Handle<T>& handle, size_t i) const {
    return convert((*handle)[i]);
  }
  /*
  template <> MyJet convert<edm::View<reco::CaloJet> >(edm::Handle<edm::View<reco::CaloJet> >& handle, size_t i) const {
    return convert(edm::Ref<edm::View<reco::CaloJet> >(handle, i));
  }
  */

  //MyJet convert(const edm::Ref<edm::View<reco::CaloJet> >& jet) const;
  MyJet convert(const reco::CaloJet& jet) const;
  MyJet convert(const pat::Jet& jet) const;
  MyJet convert(const reco::JetTag& jet) const;

private:
  typedef std::map<std::string, double> TagType;

  //void tag(const edm::Ref<edm::View<reco::CaloJet> >&, TagType&) const;
  void tag(const reco::CaloJet&, TagType&) const;
  void tag(const pat::Jet&, TagType&) const;

  const TrackConverter& trackConverter;
  const std::vector<std::string>& jetEnergyCorrectionTypes;
  std::vector<const JetCorrector *> jetEnergyCorrections;
  const std::vector<std::string>& btagAlgos;
  const edm::Event& iEvent;
};

#endif
