// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauConverter_h

#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

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
namespace edm { class InputTag; }
class TransientTrackBuilder;
class TauJetCorrector;

class MyCaloTower;
class TrackConverter;
class ImpactParameterConverter;
class TrackEcalHitPoint;
class CaloTowerConverter;
class EcalClusterConverter;

class TauConverter {
public:
  typedef std::vector<std::pair<edm::InputTag, std::vector<std::string> > > InputTagCorrectorVector;
  TauConverter(const TrackConverter&, const ImpactParameterConverter&, TrackEcalHitPoint&, const CaloTowerConverter&,
               const EcalClusterConverter&,
               const TransientTrackBuilder&, const TauJetCorrector&,
               const InputTagCorrectorVector&);
  ~TauConverter();

  template <class T> MyJet convert(const edm::InputTag& src, edm::Handle<T>& handle, size_t i) {
    return convert(src, (*handle)[i]);
  }

  MyJet convert(const edm::InputTag& src, const reco::CaloTau& recTau);
  MyJet convert(const edm::InputTag& src, const reco::IsolatedTauTagInfo& recTau);
  MyJet convert(const edm::InputTag& src, const pat::Tau& recTau);
  MyJet convert(const edm::InputTag& src, const reco::PFTau& recTau);

private:
  typedef std::map<std::string, double> TagType;

  static void tag(const reco::IsolatedTauTagInfo&, TagType&);
  static void tag(const reco::CaloTau&, TagType&);
  static void tag(const pat::Tau&, TagType&);
  static void tag(const reco::PFTau&, TagType&);

  template <typename T>
  double correction(const std::string& name, const T&);

  const TrackConverter& trackConverter;
  const ImpactParameterConverter& ipConverter;
  TrackEcalHitPoint& trackEcalHitPoint;
  const CaloTowerConverter& caloTowerConverter;
  const EcalClusterConverter& ecalClusterConverter;
  const TransientTrackBuilder& transientTrackBuilder;
  const TauJetCorrector& tauJetCorrection;
  const InputTagCorrectorVector& inputTagCorrector;
};

#endif
