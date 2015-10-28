// -*- c++ -*-
#ifndef DataFormat_Tau_h
#define DataFormat_Tau_h

#include "DataFormat/interface/TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"
#include "MiniAOD2TTree/interface/NtupleAnalysis_fwd.h"

#include <vector>

class Tau;

class TauCollection: public TauGeneratedCollection, public ParticleIteratorAdaptor<TauCollection> {
public:
  using value_type = Tau;

  TauCollection() { initialize(); }
  explicit TauCollection(const std::string& prefix): TauGeneratedCollection(prefix) { initialize(); }
  ~TauCollection() {}
  
  // Discriminators
  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }
  void setAgainstElectronDiscriminator(const std::string& name);
  void setAgainstMuonDiscriminator(const std::string& name);
  void setIsolationDiscriminator(const std::string& name);
  bool againstElectronDiscriminatorIsValid() const;
  bool againstMuonDiscriminatorIsValid() const;
  bool isolationDiscriminatorIsValid() const;

  void setupBranches(BranchManager& mgr);

  Tau operator[](size_t i) const;
  std::vector<Tau> toVector() const;

  friend class Tau;
  friend class TauGenerated<TauCollection>;
  friend class Particle<TauCollection>;

protected:
  std::vector<const Branch<std::vector<bool>> *> fConfigurableDiscriminators;
  const Branch<std::vector<bool>>* fAgainstElectronDiscriminator;
  const Branch<std::vector<bool>>* fAgainstMuonDiscriminator;
  const Branch<std::vector<bool>>* fIsolationDiscriminator;

private:
  /// Initialize data members
  void initialize();
  
  std::vector<std::string> fConfigurableDiscriminatorNames;
  std::string fAgainstElectronDiscriminatorName;
  std::string fAgainstMuonDiscriminatorName;
  std::string fIsolationDiscriminatorName;
  bool bValidityOfAgainstElectronDiscr;
  bool bValidityOfAgainstMuonDiscr;
  bool bValidityOfIsolationDiscr;
};

class Tau: public TauGenerated<TauCollection> {
public:
  Tau() {}
  Tau(const TauCollection* coll, size_t index): TauGenerated(coll, index) {}
  ~Tau() {}

  // Getters for MC tau identifier
  bool isGenuineTau() const { return this->pdgId() == TauDecayMatchType::kTauDecaysToHadrons; }
  bool isFakeTau() const { return !isGenuineTau(); }
  bool isElectronToTau() const { return this->pdgId() == TauDecayMatchType::kElectronToTau || this->pdgId() == TauDecayMatchType::kTauDecaysToElectron; }
  bool isMuonToTau() const { return this->pdgId() == TauDecayMatchType::kMuonToTau || this->pdgId() == TauDecayMatchType::kTauDecaysToMuon; }
  bool isJetToTau() const { return (this->pdgId() >= TauDecayMatchType::kUToTau && this->pdgId() <= TauDecayMatchType::kBToTau) || this->pdgId() == TauDecayMatchType::kGluonToTau; }
  bool isQuarkToTau(int quarkPid) const { return this->pdgId() == std::abs(quarkPid); }
  bool isGluonToTau() const { return this->pdgId() >= TauDecayMatchType::kGluonToTau; }
  bool isUnknownTauDecay() const { return this->pdgId() == TauDecayMatchType::kTauDecayUnknown; /* NOTE: return this is assumed to be jet->tau */ }
  
  // Getters for MC tau origin
  bool isFromZDecay() const { return this->pdgOrigin() == TauOriginType::kFromZ; }
  bool isFromWDecay() const { return this->pdgOrigin() == TauOriginType::kFromW; }
  bool isFromHplusDecay() const { return this->pdgOrigin() == TauOriginType::kFromHplus; }
  bool isFromOtherSource() const { return this->pdgOrigin() == TauOriginType::kFromOtherSource; }
  bool isFromUnknownSource() const { return this->pdgOrigin() == TauOriginType::kTauOriginUnknown; }

  // Getter for rtau
  double rtau() const {
    // Calculate p_z of leading track
    double pz = std::sinh(static_cast<double>(this->lChTrkEta()))*static_cast<double>(this->lChTrkPt());
    // Calcualte p of leading track
    double p = std::sqrt(pz*pz + static_cast<double>(this->lChTrkPt()*this->lChTrkPt()));
    // Calculate Rtau
    double rtau = -1.0;
    double taup = this->p4().P();
    if (taup > 0.0)
      rtau = p / taup;
    return rtau; 
  }
  
  // Methods for discriminators
  bool configurableDiscriminators() const {
    for(auto& disc: fCollection->fConfigurableDiscriminators) {
      if(!disc->value()[index()])
        return false;
    }
    return true;
  }
  bool againstElectronDiscriminator() const {
    if (!fCollection->againstElectronDiscriminatorIsValid())
      return true;
    return fCollection->fAgainstElectronDiscriminator->value()[index()];
  }
  bool againstMuonDiscriminator() const {
    if (!fCollection->againstMuonDiscriminatorIsValid())
      return true;
    return fCollection->fAgainstMuonDiscriminator->value()[index()];
  }
  bool isolationDiscriminator() const {
    if (!fCollection->isolationDiscriminatorIsValid())
      return true;
    return fCollection->fIsolationDiscriminator->value()[index()];
  }
  /// Operator defined for using std::sort on vector<Tau>
  bool operator<(const Tau& tau) const {
    // Descending order by tau pT
    return (this->pt() > tau.pt());
  }
};

inline
Tau TauCollection::operator[](size_t i) const {
  return Tau(this, i);
}

inline
std::vector<Tau> TauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
