// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_TauConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_TauConverter_h

#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"
#include "DataFormats/TauReco/interface/CaloTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"

#include<vector>
#include<map>
#include<string>

namespace reco { 
  class IsolatedTauTagInfo;
  class CaloTau;
  class PFTau;
  class CaloJet;
}
namespace pat { class Tau; }
namespace edm { 
  class Event;
  class InputTag;
}
class TransientTrackBuilder;
class TauJetCorrector;

class MyCaloTower;
class TrackConverter;
class ImpactParameterConverter;
class TrackEcalHitPoint;
class CaloTowerConverter;
class EcalClusterConverter;
class CaloTauConf;
class PFTauConf;

class TauConverter {
public:
  TauConverter(const TrackConverter&, const edm::Event&,
               const ImpactParameterConverter&, TrackEcalHitPoint&, const CaloTowerConverter&,
               const EcalClusterConverter&,
               const TransientTrackBuilder&, const TauJetCorrector&);
  ~TauConverter();


  template <class T> MyJet convert(const edm::InputTag& src, edm::Handle<T>& handle, size_t i) {
    return convert((*handle)[i]);
  }

  MyJet convert(const reco::CaloTau& recTau);
  MyJet convert(const reco::IsolatedTauTagInfo& recTau);
  MyJet convert(const pat::Tau& recTau);
  MyJet convert(const reco::PFTau& recTau);

  MyJet convert(const CaloTauConf& conf, edm::Handle<reco::CaloTauCollection>& handle, size_t i);
  MyJet convert(const PFTauConf& conf, edm::Handle<reco::PFTauCollection>& handle, size_t i);

private:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::IsolatedTauTagInfo&, TagType&);
  static void tag(const reco::CaloTau&, TagType&);
  static void tag(const pat::Tau&, TagType&);
  static void tag(const reco::PFTau&, TagType&);

  template <typename T>
  double correction(const std::string& name, const T&);

  const TrackConverter& trackConverter;
  const edm::Event& iEvent;
  const ImpactParameterConverter& ipConverter;
  TrackEcalHitPoint& trackEcalHitPoint;
  const CaloTowerConverter& caloTowerConverter;
  const EcalClusterConverter& ecalClusterConverter;
  const TransientTrackBuilder& transientTrackBuilder;
  const TauJetCorrector& tauJetCorrection;
};

#endif
