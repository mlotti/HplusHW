#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/TransverseMass.h"

#include "TH1F.h"
#include "TDirectory.h"


class L1Study: public BaseSelector {
public:
  explicit L1Study(const ParameterSet& config, const TH1* skimCounters);
  virtual ~L1Study();

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:

  float l1tauptcut,l1etmcut,mtcut;

  Count cAllEvents;
  Count cL1ETM;
  Count cL1Tau;
  Count cTransverseMass;

  WrappedTH1 *hTransverseMass;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(L1Study);

L1Study::L1Study(const ParameterSet& config, const TH1* skimCounters):
  BaseSelector(config, skimCounters),
  cAllEvents(fEventCounter.addCounter("All events")),
  cL1ETM(fEventCounter.addCounter("L1_ETM")),
  cL1Tau(fEventCounter.addCounter("L1_Tau")),
  cTransverseMass(fEventCounter.addCounter("mT"))
{
  std::cout << "L1 study" << std::endl;
  l1tauptcut = config.getParameter<float>("L1TauPt");
  l1etmcut   = config.getParameter<float>("L1ETM");
  mtcut      = config.getParameter<float>("TransverseMass");
  std::cout << "    L1TauPt        > " << l1tauptcut << std::endl;
  std::cout << "    L1ETM          > " << l1etmcut << std::endl;
  std::cout << "    TransverseMass > " << mtcut << std::endl;
}

L1Study::~L1Study(){
  std::cout << std::endl;
  std::cout << "    All events    " << cAllEvents.value() << std::endl;
  std::cout << "    L1ETM>0       " << cL1ETM.value() << std::endl;
  std::cout << "    L1Tau         " << cL1Tau.value() << std::endl;
  std::cout << "    mt            " << cTransverseMass.value() << std::endl;
}

void L1Study::book(TDirectory *dir) {
  //  selection->bookHistograms(dir);
  hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMasss", "TransverseMass", 200, 0, 800);
}

void L1Study::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void L1Study::process(Long64_t entry) {

  cAllEvents.increment();

  //  if(!selection->passedRunRange(fEvent,this->isData())) return;
  //  cRunRange.increment();

  double l1MET = fEvent.L1met().et();

  if(l1MET < l1etmcut) return;
  cL1ETM.increment();

   
  //std::cout << "L1Tau size " << fEvent.l1Taus().size() << std::endl;
  int ntaus = 0;
  for (L1Tau p: fEvent.l1Taus()) {
    if(p.pt() > l1tauptcut) ntaus++;
  }
  if(ntaus == 0) return;
  cL1Tau.increment();



  // transverse mass
  double myTransverseMass = TransverseMass::reconstruct(fEvent.l1Taus()[0].p2(), fEvent.L1met().p2());
  //  std::cout << "mT(tau.met) = " << myTransverseMass << std::endl;
  hTransverseMass->Fill(myTransverseMass);
                   
  if(myTransverseMass < 50) return;
  cTransverseMass.increment();

  //  double l1Tau = fEvent.L1tau().et();

}
