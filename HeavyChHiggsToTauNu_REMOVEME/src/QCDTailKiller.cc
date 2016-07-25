#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDTailKiller.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <sstream>

namespace HPlus {
  QCDTailKiller::Data::Data():
    fMaxEntries(-1),
    fPassedEvent(false),
    fDeltaPhiTauMET(-1.0) { }
  QCDTailKiller::Data::~Data() {}

  void QCDTailKiller::Data::initialize(int maxEntries) {
    fMaxEntries = maxEntries;
    for (int i = 0; i < fMaxEntries; ++i) {
      fPassedBackToBackJet.push_back(false);
      fPassedCollinearJet.push_back(false);
      fCutActiveBackToBackJet.push_back(false);
      fCutActiveCollinearJet.push_back(false);
      fDeltaPhiJetMET.push_back(-1.0);
    }
  }

  const bool QCDTailKiller::Data::passedBackToBackCuts() const {
    for (std::vector<bool>::const_iterator it = fPassedBackToBackJet.begin(); it != fPassedBackToBackJet.end(); ++it) {
      if (!(*it)) return false;
    }
    return true;
  }

  const bool QCDTailKiller::Data::passedCollinearCuts() const {
    for (std::vector<bool>::const_iterator it = fPassedCollinearJet.begin(); it != fPassedCollinearJet.end(); ++it) {
      if (!(*it)) return false;
    }
    return true;
  }

  const double QCDTailKiller::Data::getDeltaPhiJetMET(int njet) const {
    if (njet > fMaxEntries)
      throw cms::Exception("LogicError") << "QCDTailKiller::Data::getDeltaPhiJetMET() Called for jet " << njet << " but only values 0-" << fMaxEntries << " are allowed!" << std::endl;
    return fDeltaPhiJetMET[njet];
  }

  const bool QCDTailKiller::Data::passBackToBackCutForJet(int njet) const {
    if (njet > fMaxEntries)
      throw cms::Exception("LogicError") << "QCDTailKiller::Data::passBackToBackCutForJet() Called for jet " << njet << " but only values 0-" << fMaxEntries << " are allowed!" << std::endl;
    return fPassedBackToBackJet[njet];
  }

  const bool QCDTailKiller::Data::passCollinearCutForJet(int njet) const {
    if (njet > fMaxEntries)
      throw cms::Exception("LogicError") << "QCDTailKiller::Data::passCollinearCutForJet() Called for jet " << njet << " but only values 0-" << fMaxEntries << " are allowed!" << std::endl;
    return fPassedCollinearJet[njet];
  }

  const bool QCDTailKiller::Data::backToBackCutActiveForJet(int njet) const {
    if (njet > fMaxEntries)
      throw cms::Exception("LogicError") << "QCDTailKiller::Data::passBackToBackCutForJet() Called for jet " << njet << " but only values 0-" << fMaxEntries << " are allowed!" << std::endl;
    return fCutActiveBackToBackJet[njet];
  }

  const bool QCDTailKiller::Data::collinearCutActiveForJet(int njet) const {
    if (njet > fMaxEntries)
      throw cms::Exception("LogicError") << "QCDTailKiller::Data::passCollinearCutForJet() Called for jet " << njet << " but only values 0-" << fMaxEntries << " are allowed!" << std::endl;
    return fCutActiveCollinearJet[njet];
  }

  QCDTailKiller::CutItem::CutItem(EventCounter& eventCounter, std::string cutName, QCDTailKiller::CutDirection cutDirection) :
  fCutShape(QCDTailKiller::kNoCut),
  fCutX(0),
  fCutY(0),
  fCutDirection(cutDirection),
  bIsInitialised(false),
  fName(cutName),
  fPassedSubCounter(eventCounter.addSubCounter("QCDTailKiller",cutName)) { }

  QCDTailKiller::CutItem::~CutItem() { }

  void QCDTailKiller::CutItem::initialise(HistoWrapper& histoWrapper, TFileDirectory& histoDir, std::string cutShape, double cutX, double cutY, int jetN) {
    if (bIsInitialised)
      throw cms::Exception("LogicError") << "QCDTailKiller::CutItem Called more than once initialise() !" << std::endl;
    // Initialise values
    bIsInitialised = true;
    if (cutShape == "noCut") {
      fCutShape = QCDTailKiller::kNoCut;
    } else if (cutShape == "rectangular") {
      fCutShape = QCDTailKiller::kRectangle;
    } else if (cutShape == "triangular") {
      fCutShape = QCDTailKiller::kTriangle;
    } else if (cutShape == "circular") {
      fCutShape = QCDTailKiller::kCircle;
    } else if (cutShape == "minDeltaPhiJetMET") {
      fCutShape = QCDTailKiller::kMinDeltaPhiJetMET;
    } else {
      throw cms::Exception("LogicError") << "QCDTailKiller::CutItem by name '"+fName+"' unknown cutShape="+cutShape+"! (options: noCut, rectangular, triangular, circular)!" << std::endl;
    }
    fCutX = cutX;
    fCutY = cutY;
    // Create histograms
    std::string myNameString;
    std::stringstream myStream;
    myNameString = "CircleCut_"+fName;
    if (fCutDirection == kCutUpperLeftCorner)
      myStream << "CircleCut_" << fName << ";#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{" << jetN << "},MET))^{2}}, ^{o};N_{events}";
    else
      myStream << "CircleCut_" << fName << ";#sqrt{(#Delta#phi(#tau,MET))^{2}+(180^{o}-#Delta#phi(jet_{" << jetN << "},MET))^{2}}, ^{o};N_{events}";
    hOptimisationPlot = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, histoDir, myNameString.c_str(), myStream.str().c_str(),52,0.,260.);
    myStream.str("");
    myNameString = "2DplaneBeforeCut_"+fName;
    myStream << "2DplaneBeforeCut_" << fName << ";#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{" << jetN << "},MET), ^{o}";
    hBeforeCut = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, histoDir, myNameString.c_str(), myStream.str().c_str(),18,0.,180.,18,0.,180.);
    myStream.str("");
    myNameString = "2DplaneAfterAllCuts_"+fName;
    myStream << "2DplaneAfterAllCuts_" << fName << ";#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{" << jetN << "},MET), ^{o}";
    hAfterAllCuts = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, histoDir, myNameString.c_str(), myStream.str().c_str(),18,0.,180.,18,0.,180.);
  }

  bool QCDTailKiller::CutItem::passedCut(double x, double y) {
    // Check initialisation
    if (!bIsInitialised)
      throw cms::Exception("LogicError") << "QCDTailKiller::CutItem You forgot to call initialise() before calling passedCut()!" << std::endl;
    // Fill before plots
    hBeforeCut->Fill(x,y);
    if (fCutDirection == kCutUpperLeftCorner)
      hOptimisationPlot->Fill(std::sqrt(std::pow(x,2)+std::pow(180.-y,2)));
    else
      hOptimisationPlot->Fill(std::sqrt(std::pow(180.-x,2)+std::pow(y,2)));
    bool myPassedStatus = false;
    // No cut requested
    if (fCutShape == QCDTailKiller::kNoCut) {
      myPassedStatus = true;
    } else if (fCutShape == QCDTailKiller::kRectangle) {
    // Rectangular cut
      if (fCutDirection == QCDTailKiller::kCutUpperLeftCorner) {
        myPassedStatus = !(x < fCutX && y > fCutY);
      } else {
        myPassedStatus = !(x > fCutX && y < fCutY);
      }
    } else if (fCutShape == QCDTailKiller::kTriangle) {
    // Triangular cut
      if (fCutDirection == QCDTailKiller::kCutUpperLeftCorner) {
        if (fCutX == 0)
          throw cms::Exception("LogicError") << "QCDTailKiller::CutItem by name '"+fName+"' cutX is zero in triangular cut!" << std::endl;
        // y(x) = y0/x0 * x + 180 - y0
	myPassedStatus = y < fCutY/fCutX * x + 180.0 - fCutY;
      } else {
        if (fCutX == 0)
          throw cms::Exception("LogicError") << "QCDTailKiller::CutItem by name '"+fName+"' cutX is zero in triangular cut!" << std::endl;
        // y(x) = y0/x0 * x + y0/x0*(180 - x0) = y0/x0 * (x+180-x0)
        myPassedStatus = y > fCutY/fCutX * (x + 180.0 - fCutX);
      }
    } else if (fCutShape == QCDTailKiller::kCircle) {
    // Circular cut
      if (fCutDirection == QCDTailKiller::kCutUpperLeftCorner) {
        myPassedStatus = std::sqrt(std::pow(180.0-y,2)+std::pow(x,2)) > fCutX;
      } else {
        myPassedStatus = std::sqrt(std::pow(180.0-x,2)+std::pow(y,2)) > fCutX;
      }
    } else if (fCutShape == QCDTailKiller::kMinDeltaPhiJetMET) {
      // Make the cut only in place of the back-to-back cut
      if (fCutDirection == QCDTailKiller::kCutLowerRightCorner) {
        myPassedStatus = y > fCutX;
      }
    }
    // Increment counter and return
    if (myPassedStatus)
      increment(fPassedSubCounter);
    return myPassedStatus;
  }

  void QCDTailKiller::CutItem::fillAfterAllCuts(double x, double y) {
    hAfterAllCuts->Fill(x,y);
  }

  QCDTailKiller::QCDTailKiller(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string postfix):
    BaseSelection(eventCounter, histoWrapper),
    fMaxEntries(iConfig.getUntrackedParameter<uint32_t>("maxJetsToConsider")),
    bDisableCollinearCuts(iConfig.getUntrackedParameter<bool>("disableCollinearCuts")),
    fSubCountAllEvents(eventCounter.addSubCounter("QCDTailKiller"+postfix, "All events")),
    fSubCountPassedEvents(eventCounter.addSubCounter("QCDTailKiller"+postfix, "Passed events"))
  {
    edm::Service<TFileService> fs;
    std::string myDirName = "QCDTailKiller"+postfix;
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kVital, *fs, myDirName);
    TFileDirectory myBackToBackDir = histoWrapper.mkdir(HistoWrapper::kVital, myDir, "BackToBackSystem");
    TFileDirectory myCollinearDir = histoWrapper.mkdir(HistoWrapper::kVital, myDir, "CollinearSystem");

    // Create and initialise cut items for back to back system
    std::vector<edm::ParameterSet> myBackToBackPSets = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("backToBack");
    for (size_t i = 0; i < fMaxEntries; ++i) {
      std::stringstream myStream;
      myStream << "BackToBackJet" << i+1;
      fBackToBackJetCut.push_back(CutItem(eventCounter, myStream.str(), QCDTailKiller::kCutLowerRightCorner));
      if (i < myBackToBackPSets.size()) {
        fBackToBackJetCut[i].initialise(histoWrapper, myBackToBackDir,
                                        myBackToBackPSets[i].getUntrackedParameter<std::string>("CutShape"),
                                        myBackToBackPSets[i].getUntrackedParameter<double>("CutX"),
                                        myBackToBackPSets[i].getUntrackedParameter<double>("CutY"),
                                        i+1);
      } else {
        fBackToBackJetCut[i].initialise(histoWrapper, myBackToBackDir, "noCut", 0.0, 0.0, i+1);
      }
    }
    // Create and initialise cut items for collinear system
    std::vector<edm::ParameterSet> myCollinearPSets = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("collinear");
    for (size_t i = 0; i < fMaxEntries; ++i) {
      std::stringstream myStream;
      myStream << "CollinearJet" << i+1;
      fCollinearJetCut.push_back(CutItem(eventCounter, myStream.str(), QCDTailKiller::kCutUpperLeftCorner));
      if (i < myCollinearPSets.size()) {
        if (!bDisableCollinearCuts) {
          fCollinearJetCut[i].initialise(histoWrapper, myCollinearDir,
                                         myCollinearPSets[i].getUntrackedParameter<std::string>("CutShape"),
                                         myCollinearPSets[i].getUntrackedParameter<double>("CutX"),
                                         myCollinearPSets[i].getUntrackedParameter<double>("CutY"),
                                         i+1);
        } else {
          fCollinearJetCut[i].initialise(histoWrapper, myCollinearDir, "noCut", 0., 0., i+1);
        }
      } else {
        fCollinearJetCut[i].initialise(histoWrapper, myCollinearDir, "noCut", 0.0, 0.0, i+1);
      }
    }
  }

  QCDTailKiller::~QCDTailKiller() {}

  QCDTailKiller::Data QCDTailKiller::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, tau, jets, met);
  }

  QCDTailKiller::Data QCDTailKiller::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tau, jets, met);
  }

  QCDTailKiller::Data QCDTailKiller::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    Data output;
    output.initialize(fMaxEntries);
    increment(fSubCountAllEvents);
    // Obtain delta phi between tau and MET
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*tau, *met) * 57.3;
    output.fDeltaPhiTauMET = myDeltaPhiTauMET;

    // Back to back topology
    // Loop over the jet list (it might contain also the jet corresponding to tau depending on which list is supplied to the analyse method)
    output.fPassedEvent = true;
    size_t i = 0;
    while (i < jets.size() && i < fMaxEntries) {
      // Obtain delta phi between jet and MET
      double myDeltaPhiJetMET = DeltaPhi::reconstruct(*(jets[i]), *met) * 57.3;
      if (fBackToBackJetCut[i].passedCut(myDeltaPhiTauMET, myDeltaPhiJetMET)) {
        // passed
        output.fDeltaPhiJetMET[i] = myDeltaPhiJetMET;
        output.fPassedBackToBackJet[i] = true;
      } else {
        // failed
        output.fPassedEvent = false;
      }
      output.fCutActiveBackToBackJet[i] = fBackToBackJetCut[i].isActive();
      ++i;
    }
    i = 0;
    while (i < jets.size() && i < fMaxEntries) {
      // Obtain delta phi between jet and MET
      double myDeltaPhiJetMET = DeltaPhi::reconstruct(*(jets[i]), *met) * 57.3;
      if (fCollinearJetCut[i].passedCut(myDeltaPhiTauMET, myDeltaPhiJetMET)) {
        // passed
        output.fPassedCollinearJet[i] = true;
      } else {
        // failed
        output.fPassedEvent = false;
      }
      output.fCutActiveCollinearJet[i] = fCollinearJetCut[i].isActive();
      ++i;
    }
    // Return if cut failed
    if (!output.fPassedEvent) return output;
    // Event passed cuts, now fill histograms after all cuts
    increment(fSubCountPassedEvents);
    i = 0;
    while (i < jets.size() && i < fMaxEntries) {
      double myDeltaPhiJetMET = DeltaPhi::reconstruct(*(jets[i]), *met) * 57.3;
      fCollinearJetCut[i].fillAfterAllCuts(myDeltaPhiTauMET, myDeltaPhiJetMET);
      fBackToBackJetCut[i].fillAfterAllCuts(myDeltaPhiTauMET, myDeltaPhiJetMET);
      ++i;
    }
    return output;
  }
}
