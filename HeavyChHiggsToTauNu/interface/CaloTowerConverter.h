// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CaloTowerConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CaloTowerConverter_h

#include<vector>
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"

#include "TVector3.h"

namespace edm {
  class Event;
  class EventSetup;
}
namespace reco { class CaloJet; }

class MyCaloTower;
class CaloCellGeometry;
class CaloSubdetectorGeometry;

class CaloTowerConverter {
public:
  CaloTowerConverter(const edm::Event&, const edm::EventSetup&);
  ~CaloTowerConverter();

  void convert(const reco::CaloJet&, std::vector<MyCaloTower>&) const;
private:
  TVector3 getCellMomentum(const CaloCellGeometry *, double) const;

  const EBRecHitCollection& EBRecHits;
  const EERecHitCollection& EERecHits;
  const HBHERecHitCollection& HBHERecHits;

  const CaloSubdetectorGeometry *EB;
  const CaloSubdetectorGeometry *EE;
  const CaloSubdetectorGeometry *HB;
  const CaloSubdetectorGeometry *HE;
};

#endif
