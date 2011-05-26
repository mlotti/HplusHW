#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ExpressionHisto.h"

namespace HPlus {
  ExpressionHistoVeryBase::ExpressionHistoVeryBase(const edm::ParameterSet& iConfig): 
    histo(0),
    min(iConfig.getUntrackedParameter<double>("min")),
    max(iConfig.getUntrackedParameter<double>("max")),
    nbins(iConfig.getUntrackedParameter<int>("nbins")),
    name(iConfig.getUntrackedParameter<std::string>("name")),
    description(iConfig.getUntrackedParameter<std::string>("description"))
  {}

  ExpressionHistoVeryBase::~ExpressionHistoVeryBase() {}
}
