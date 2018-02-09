// -*- c++ -*-
#include "EventSelection/interface/QuarkGluonLikelihoodRatio.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
#include "DataFormat/interface/HLTBJet.h"

#include "Math/VectorUtil.h"
#include <cmath>
#include <algorithm>

// --- QGLInputItem ---

// Constructor
QGLInputItem::QGLInputItem(float minQGL, float maxQGL, float minPt, float maxPt, float prob, float probErr)
: fminQGL(minQGL),
  fmaxQGL(maxQGL),
  fminPt(minPt),
  fmaxPt(maxPt),
  fProb(prob),
  fProbErr(probErr)
{}

// Destructor
QGLInputItem::~QGLInputItem() {}

// --- QGLInputStash ---

// Constructor
QGLInputStash::QGLInputStash() {}

// Destructor
QGLInputStash::~QGLInputStash() {
  
  std::vector<std::vector<QGLInputItem*>> collections = { fLight, fGluon};
  for (auto& container: collections) {
    for (size_t i = 0; i < container.size(); ++i) {
      delete container[i];
    }
    container.clear();
  }
}

// Create new input item corresponding to certain jet type 
void QGLInputStash::addInput(std::string jetType, float minQGL, float maxQGL, float minPt, float maxPt, float Prob, float ProbErr) {
  getCollection(jetType).push_back(new QGLInputItem(minQGL, maxQGL, minPt, maxPt, Prob, ProbErr));
}


// Return the Probability based on QGL value
const float QGLInputStash::getInputValue(std::string jetType, float QGL, float pt) {
  for (auto &p: getCollection(jetType)) {
    if (!p->isWithinPtRange(pt)) continue;
    if (!p->isWithinQGLRange(QGL)) continue;
    return p->getProb();
  }
  return 1.0;
}

// Get vector of input items (according to jetType)
std::vector<QGLInputItem*>& QGLInputStash::getCollection(std::string jetType) {
  if (jetType == "Light")
    return fLight;
  else if (jetType == "Gluon")
    return fGluon;
  throw hplus::Exception("Logic") << "Unknown jet type requested! " << jetType;
}



QuarkGluonLikelihoodRatio::Data::Data() 
: bPassedSelection(false)
{ }

QuarkGluonLikelihoodRatio::Data::~Data() { }

QuarkGluonLikelihoodRatio::QuarkGluonLikelihoodRatio(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  bTriggerMatchingApply(config.getParameter<bool>("triggerMatchingApply")),
  fTriggerMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedQuarkGluonLikelihoodRatio(fEventCounter.addCounter("passed b-jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection ("+postfix+")", "All events")),
  fProb()
{
  initialize(config);
}

QuarkGluonLikelihoodRatio::QuarkGluonLikelihoodRatio(const ParameterSet& config)
: BaseSelection(),
  bTriggerMatchingApply(config.getParameter<bool>("triggerMatchingApply")),
  fTriggerMatchingCone(config.getParameter<float>("triggerMatchingCone")),
  fJetPtCuts(config.getParameter<std::vector<float>>("jetPtCuts")),
  fJetEtaCuts(config.getParameter<std::vector<float>>("jetEtaCuts")),
  fNumberOfJetsCut(config, "numberOfBJetsCut"),
  fDisriminatorValue(-1.0),
  // Event counter for passing selection
  cPassedQuarkGluonLikelihoodRatio(fEventCounter.addCounter("passed b-jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("bjet selection", "All events")),
  fProb()
{
  initialize(config);
  bookHistograms(new TDirectory());
}

QuarkGluonLikelihoodRatio::~QuarkGluonLikelihoodRatio() {
  delete hGluonJetQGL;
  delete hLightJetQGL;

  delete hQGLR;
  delete hQGLR_vs_HT;
  delete hQGLR_vs_NJets;
}

void QuarkGluonLikelihoodRatio::initialize(const ParameterSet& config) {
  
  handleQGLInput(config, "Light"); 
  handleQGLInput(config, "Gluon");
  
  return;
}

void QuarkGluonLikelihoodRatio::handleQGLInput(const ParameterSet& config, std::string jetType) { 
  
  boost::optional<std::vector<ParameterSet>> psets;
  
  if (jetType == "Light") psets = config.getParameterOptional<std::vector<ParameterSet>>("LightJetsQGL");
  if (jetType == "Gluon") psets = config.getParameterOptional<std::vector<ParameterSet>>("GluonJetsQGL");
  
  if (!psets) return;
  
  for (auto &p: *psets) {
    
    // Obtain variables
    float minQGL = p.getParameter<float>("QGLmin");
    float maxQGL = p.getParameter<float>("QGLmax");
    float minPt  = p.getParameter<float>("Ptmin");
    float maxPt  = p.getParameter<float>("Ptmax");
    float Prob   = p.getParameter<float>("prob");
    float ProbErr= p.getParameter<float>("probError");
    
    if (0) std::cout<<"minQGL="<<minQGL<<" maxQGL="<<maxQGL<<"  minPt="<<minPt<<"  maxPt="<<maxPt<<"   Probability="<<Prob<<"  Error="<<ProbErr<<std::endl;
    
    // Store them
    fProb.addInput(jetType, minQGL, maxQGL, minPt, maxPt, Prob, ProbErr);
  }
  return;
}


void QuarkGluonLikelihoodRatio::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "QuarkGluonLikelihoodRatio_" + sPostfix);
  
  // Histogram binning options
  int nQGLBins      = 100;
  float fQGLMin     = 0.0;
  float fQGLMax     = 1.0;
  int  nPtBins      =  50;
  float fPtMin      =   0.0;
  float fPtMax      = 500.0;
  int  nEtaBins     =  50;
  float fEtaMin     =  -5.0;
  float fEtaMax     =  +5.0;
  int  nBinsBDisc   =  10;
  float minBDisc    =   0.0;
  float maxBDisc    =  10.0;
  int nDEtaBins     = 200;   // 100;
  double fDEtaMin   =   0.0;
  double fDEtaMax   =   0.2; //  10;
  int nDPhiBins     = 200;   // 32;
  double fDPhiMin   =   0.0;
  double fDPhiMax   =   0.2; // 3.2;
  int nDRBins       =  50;
  double fDRMin     =   0;
  double fDRMax     =  10;
  // Overwrite binning from cfg file?
  if (fCommonPlots != nullptr) {  
      nPtBins    = 2*fCommonPlots->getPtBinSettings().bins();
      fPtMin     = fCommonPlots->getPtBinSettings().min();
      fPtMax     = 2*fCommonPlots->getPtBinSettings().max();
      
      nEtaBins   = fCommonPlots->getEtaBinSettings().bins();
      fEtaMin    = fCommonPlots->getEtaBinSettings().min();
      fEtaMax    = fCommonPlots->getEtaBinSettings().max();
      
      nBinsBDisc = fCommonPlots->getBJetDiscBinSettings().bins();
      minBDisc   = fCommonPlots->getBJetDiscBinSettings().min();
      maxBDisc   = fCommonPlots->getBJetDiscBinSettings().max();
      
      // nDEtaBins   = fCommonPlots->getDeltaEtaBinSettings().bins();
      // fDEtaMin    = fCommonPlots->getDeltaEtaBinSettings().min();
      // fDEtaMax    = fCommonPlots->getDeltaEtaBinSettings().max();
      
      // nDPhiBins   = fCommonPlots->getDeltaPhiBinSettings().bins();
      // fDPhiMin    = fCommonPlots->getDeltaPhiBinSettings().min();
      // fDPhiMax    = fCommonPlots->getDeltaPhiBinSettings().max();
      
      nDRBins     = fCommonPlots->getDeltaRBinSettings().bins();
      fDRMin      = fCommonPlots->getDeltaRBinSettings().min();
      fDRMax      = fCommonPlots->getDeltaRBinSettings().max();
  }

  hGluonJetQGL = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "GluonJetQGL", "Quark-Gluon discriminant for Gluon Jets", nQGLBins, fQGLMin, fQGLMax);
  hLightJetQGL = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "LightJetQGL", "Quark-Gluon discriminant for Light Jets", nQGLBins, fQGLMin, fQGLMax);
 
  hQGLR          = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "QGLR", "Quark-Gluon likelihood ratio", nQGLBins, fQGLMin, fQGLMax);
  hQGLR_vs_HT    = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "QGLR_vs_HT", "QGLR Vs H_{T} (GeVc^{-1})", 50, 0.0, 4000.0, nQGLBins, fQGLMin, fQGLMax);
  hQGLR_vs_NJets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "QGLR_vs_NJets", "QGLR Vs Jets Multiplicity", 15, -0.5, 14.5, nQGLBins, fQGLMin, fQGLMax); 
}

QuarkGluonLikelihoodRatio::Data QuarkGluonLikelihoodRatio::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData, bjetData);
  enableHistogramsAndCounters();
  return myData;
}

QuarkGluonLikelihoodRatio::Data QuarkGluonLikelihoodRatio::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  QuarkGluonLikelihoodRatio::Data data = privateAnalyze(event, jetData, bjetData);
  // Send data to CommonPlots
  //if (fCommonPlots != nullptr)
  //  fCommonPlots->fillControlPlotsAtBtagging(event, data);
  // Return data
  return data;
}

QuarkGluonLikelihoodRatio::Data QuarkGluonLikelihoodRatio::privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  Data output;
  cSubAll.increment();
  
  int nBJets = 0;
  int nNoBJets  = 0;
  // Loop over selected jets
  for(const Jet& jet: jetData.getSelectedJets()) {
    
    if (isBJet(jet, bjetData.getSelectedBJets())){
      nBJets++;
      continue;
    }
    nNoBJets++;
    
    
    const short jetHadronFlavour = std::abs(jet.hadronFlavour());
    const short jetPartonFlavour = std::abs(jet.partonFlavour());
    
    // === Reject jets consistent with b or c  (jet flavors:  https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Hadron_parton_based_jet_flavour )
    if (jetHadronFlavour != 0) continue;
    if (jetPartonFlavour != 1 && jetPartonFlavour != 2 && jetPartonFlavour != 3 && jetPartonFlavour != 21) continue;
    
    
    output.fGluonLightJets.push_back(jet);
    
    // Gluon Jets
    if (jetPartonFlavour == 21)
      {
        output.fGluonJets.push_back(jet);
        hGluonJetQGL->Fill(jet.QGTaggerAK4PFCHSqgLikelihood());
      }
    // Light Jets
    if (jetPartonFlavour == 1 || jetPartonFlavour == 2 || jetPartonFlavour == 3)
      {
        output.fLightJets.push_back(jet);
        hLightJetQGL->Fill(jet.QGTaggerAK4PFCHSqgLikelihood());
      }
  }
  
  int N  = output.fGluonLightJets.size();
  int Nq = output.fLightJets.size();
  int Ng = output.fGluonJets.size();
  
  int Permutations = factorial(N)/(factorial(N-Ng)*factorial(Ng));
  
  //std::cout<<"Number of B-Jets= "<<nBJets<<"  Number of non b-jets= "<<nNoBJets<<"  Number of all light Jets= "<<N<<"    Quark Jets="<<Nq<<"     Gluon Jets="<<Ng<<"    Permutations="<<Permutations<<std::endl;
  
  double QGLR = calculateQGLR(iEvent, output.fGluonLightJets, output.fLightJets, output.fGluonJets);
  
  output.fQGLR = QGLR;
  
  // Fill Histograms
  hQGLR          -> Fill(QGLR);
  hQGLR_vs_HT    -> Fill(jetData.HT(), QGLR);
  hQGLR_vs_NJets -> Fill(jetData.getNumberOfSelectedJets(), QGLR);
  
  // Return data object
  return output;
}

double QuarkGluonLikelihoodRatio::calculateQGLR(const Event& iEvent, const std::vector<Jet> Jets, const std::vector<Jet> LightJets, const std::vector<Jet> GluonJets)
{
  // Quark term
  double LNq0g = calculateL(iEvent, Jets, Jets.size(), 0);
  //std::cout<<"Quark term L(Nq=N, Ng=0) = L("<<Jets.size()<<",0) ="<<LNq0g<<std::endl;
  
  // Gluon term
  double L0qNg = calculateL(iEvent, Jets, 0, Jets.size());
  //std::cout<<"Gluon term L(Nq=0, Ng=N) = L(0,"<<Jets.size()<<") ="<<L0qNg<<std::endl;
  
  double QGLR = LNq0g / ( LNq0g+L0qNg);
  
  /*
  double sum = 0;
  std::cout<<"Sum = "<<sum<<std::endl;
  for (unsigned int iNg=1; iNg<Jets.size()+1; iNg++)
    {
      int iNq = Jets.size() - iNg;
      double L = calculateL(iEvent, Jets, iNq, iNg);
      std::cout<<"    L("<<iNq<<","<<iNg<<") = "<<L<<std::endl;
      sum +=  L;
    }
  std::cout<<"Sum="<<sum<<std::endl;
  
  double QGLR = LNq0g / (LNq0g+sum);
  */
  
  return QGLR;
}



double QuarkGluonLikelihoodRatio::factorial(const int N)
{
  if (N > 1)
    return N * factorial(N-1);
  else
    return 1;
}


std::vector<int> QuarkGluonLikelihoodRatio::getJetIndices(const std::vector<Jet> Jets)
{
  std::vector<int> v;
  for (unsigned int i=0; i<Jets.size(); i++)
    {
      v.push_back(Jets.at(i).index());
    }
  return v;
}



double QuarkGluonLikelihoodRatio::calculateL(const Event& iEvent, const std::vector<Jet> Jets, const int Nq, const int Ng)
{
  std::vector<int> v = getJetIndices(Jets);
  std::vector<std::vector<int> > permutations = getPermutations(v, Nq, Ng);
  
  // First Nq places are for Quarks and the last Ng are for Gluons
  double sum = 0;
  for (unsigned int i=0; i<permutations.size(); i++)
    {
      double productQuark = 1;
      double productGluon = 1;
      
      std::vector<int> v = permutations.at(i);

      for (unsigned int q=0; q<Nq; q++)
	{
	  int index    = v.at(q);
	  Jet QuarkJet = iEvent.jets()[index];
	  double QGL   = QuarkJet.QGTaggerAK4PFCHSqgLikelihood();
	  double pt    = QuarkJet.pt();
	  
	  productQuark *= fProb.getInputValue("Light", QGL, pt);
	  
	  //std::cout<<"Light Jet |  q="<<q<<"  with index="<<index<<"   pt ="<<pt<<"  QGL="<<QGL<<"  Probability="<<fProb.getInputValue("Light", QGL, pt)<<std::endl;

	  //std::cout<<" Quark "<<q<<"  QGL="<<QGL<<"   Probability ="<<fProb.getInputValueByQGL("Light", QGL)<<std::endl;
	}

      for (unsigned int g=Nq; g<v.size(); g++)
	{
	  int index    = v.at(g);
	  Jet GluonJet = iEvent.jets()[index];
	  double QGL   = GluonJet.QGTaggerAK4PFCHSqgLikelihood();
	  double pt    = GluonJet.pt();
	  
	  productGluon *= fProb.getInputValue("Gluon", QGL, pt);
	  
	  //std::cout<<" GLuon "<<g<<"  QGL="<<QGL<<"   Probability = "<<fProb.getInputValueByQGL("Gluon", QGL)<<std::endl;
	  
	  //std::cout<<"Gluon Jet |  g="<<g<<"  with index="<<index<<"   pt ="<<pt<<"  QGL="<<QGL<<"  Probability="<<fProb.getInputValue("Gluon", QGL, pt)<<std::endl;
	}
      
      sum+= productQuark * productGluon;
    }
  return sum;
}


std::vector<std::vector<int> > QuarkGluonLikelihoodRatio::getPermutations(std::vector<int> v, const int Nq, const int Ng)
{
  std::vector<std::vector<int> > permutations;
  int nPermutations = 0;
  
  do {    
    bool Found = PermutationFound(permutations, v, Nq, Ng);
    if (!Found)
      {
	nPermutations++;
	permutations.push_back(v);
	//for (unsigned int i=0; i<v.size(); i++)
	// {
	//    std::cout << v.at(i) << " ";
	//  }
	//std::cout<<" "<<std::endl;
      }
    
  } while (std::next_permutation(v.begin(), v.end()));
  return permutations;
}


					 
bool QuarkGluonLikelihoodRatio::PermutationFound(std::vector<std::vector<int> > p, std::vector<int> v, const int Nq, const int Ng)
{
  
  int nStart = 0;
  int nEnd   = 0;
  int nJets  = 0;

  if (Nq < Ng){
    nStart = 0;
    nEnd   = Nq;
    nJets  = Nq;
  }
  else{
    nStart = Nq;
    nEnd   = Nq+Ng;
    nJets  = Ng;
  }
  
  for (unsigned int row=0; row<p.size(); row++)
    {
      std::vector<int> perm = p.at(row);
      int FoundAll = 0;
      
      // Loop over
      for (unsigned int j=nStart; j<nEnd; j++){
	
	int FindIndex =  v.at(j);
	
	bool FoundIndex = false;
	for (unsigned int k=nStart; k<nEnd;k++){
	  if (perm.at(k) == FindIndex) FoundIndex = true;
	}
	if (FoundIndex) FoundAll++;
	else break;	
      }
      if (FoundAll == nJets) return 1;
    }
  return 0;
}


bool QuarkGluonLikelihoodRatio::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool QuarkGluonLikelihoodRatio::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}
