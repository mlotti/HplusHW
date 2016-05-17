// -*- c++ -*-                                
#ifndef Framework_MCTools_h
#define Framework_MCTools_h

#include "DataFormat/interface/Event.h"

#include <cmath>
#include <iomanip>
#include <string>
#include <vector>

#include "TLorentzVector.h"
#include "Math/VectorUtil.h"

using namespace std;
// typedef GenParticleCollection genParticle;

class MCTools {
  
public:
  MCTools(Event &fEvt);
  ~MCTools();
  GenParticle GetGenP(const size_t genP_Index);

  bool RecursivelyLookForMotherId(const unsigned int genP_Index, 
				  int momId, 
				  const bool posn);

  TLorentzVector GetP4(const int genP_Index);

  bool LookForMotherId(const unsigned int genP_Index, 
		       int momId, 
		       const bool bAbsoluteMomId);

  TLorentzVector GetVisibleP4(const unsigned int genP_Index);

  bool IsNeutrino(const int pdgId);

  int GetPosOfMotherId(const unsigned int genP_Index,
		       int momId, 
		       const bool bAbsoluteMomId);

  bool IsItsMother(const int genP_Index,
		   const int mom_Index);

  int GetLdgDaughter(const int genP_Index, 
		     bool bOnlyChargedDaughters);

  double GetHadronicTauMaxSignalCone(const int genP_Index, 
				     bool bOnlyChargedDaughters, 
				     double minPt);

  void GetHadronicTauFinalDaughters(const int genP_Index,
				    std::vector<short int>& finalDaughters);

  void GetHadronicTauChargedPions(const int genP_Index, 
				  std::vector<short int> &chargedPions);

  void GetHadronicTauNeutralPions(const int genP_Index,
				  std::vector<short int> &neutralPions);

  bool IsFinalStateTau(const int genP_Index);

  int GetTauDecayMode(const int genP_Index);

  void PrintMothersRecursively(const int genP_Index, 
			       bool bPrintHeaders=true);

  void PrintDaughtersRecursively(const int genP_Index,
				 bool bPrintHeaders=true);

  void PrintGenParticle(const int genP_Index, 
			bool bPrintHeaders=true);

  double GetVertexX(void){return fEvent->vertexInfo().pvX();}

  double GetVertexY(void){return fEvent->vertexInfo().pvY();}

  double GetVertexZ(void){return fEvent->vertexInfo().pvZ();}

  double GetLxy(const int genP_Index,
		bool wrtPV=true);

  double GetD0Mag(const int genP_Index,
		  const int mom_Index,
		  bool wrtPV=true);

private:
  Event *fEvent;

  void _GetHadronicTauChargedOrNeutralPions(int tauIndex, 
					    bool charged,
					    std::vector<short int> &pions);


  
};

#endif

