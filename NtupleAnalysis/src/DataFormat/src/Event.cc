#include "DataFormat/interface/Event.h"

#include "boost/optional.hpp"

#include <stdexcept>

namespace {
  template <typename T, typename Child>
  std::vector<T> to_vector(const Child& child) {
    std::vector<T> res;
    for(const auto& item: child) {
      res.push_back(item.second.data());
    }
    return res;
  }

  template <typename T>
  std::vector<T> to_vector(const boost::property_tree::ptree& config, const std::string& name) {
    return to_vector<T>(config.get_child(name));
  }

  template <typename T>
  boost::optional<std::vector<T>> to_vector_optional(const boost::property_tree::ptree& config, const std::string& name) {
    boost::optional<std::vector<T>> res;

    boost::optional<const boost::property_tree::ptree&> child = config.get_child_optional(name);
    if(child) {
      res = to_vector<T>(*child);
    }

    return res;
  }
}

Event::Event():
  fGenMET("GenMET"),
  fMET_Type1("MET_Type1")
{}
Event::Event(const boost::property_tree::ptree& config): Event() {
  bool variationAssigned = false;

  boost::optional<std::string> jetSyst = config.get_optional<std::string>("JetSelection.systematicVariation");
  if(jetSyst) {
    fJetCollection.setEnergySystematicsVariation(*jetSyst);
    fMET_Type1.setEnergySystematicsVariation(*jetSyst);
    variationAssigned = true;
  }

  boost::optional<std::string> tauSyst = config.get_optional<std::string>("TauSelection.systematicVariation");
  if(tauSyst) {
    if(variationAssigned) {
      throw std::runtime_error("Trying to set systematicVariation for taus, but a variation has already been set for jets! Only one variation per analyzer is allowed");
    }
    fTauCollection.setEnergySystematicsVariation(*tauSyst);
    fMET_Type1.setEnergySystematicsVariation(*tauSyst);
    variationAssigned = true;
  }

  boost::optional<std::vector<std::string> > tauDiscr = to_vector_optional<std::string>(config, "TauSelection.discriminators");
  if(tauDiscr) {
    fTauCollection.setConfigurableDiscriminators(*tauDiscr);
  }
}
Event::~Event() {}

void Event::setupBranches(BranchManager& mgr) {
  fEventID.setupBranches(mgr);
  fTauCollection.setupBranches(mgr);
  fJetCollection.setupBranches(mgr);
  fMuonCollection.setupBranches(mgr);
  fElectronCollection.setupBranches(mgr);
  fGenMET.setupBranches(mgr);
  fMET_Type1.setupBranches(mgr);
}
