#include "Math/VectorUtil.h"

//soti                                                                                                                                      
struct TrijetSelection{
  std::vector<int> bjet_index;
  std::vector<int> jet1_index;
  std::vector<int> jet2_index;
  std::vector<math::XYZTLorentzVector> TrijetP4;
  std::vector<math::XYZTLorentzVector> DijetP4;
  std::vector<Jet> Jet1;
  std::vector<Jet> Jet2;
  std::vector<Jet> BJet;
};



/*
struct TopRec{
  double PtDR;
  double DijetPtDR;
  double BjetMass;
  double LdgJetPt;
  double LdgJetEta;
  double LdgJetBDisc;
  double SubldgJetPt;
  double SubldgJetEta;
  double SubldgJetBDisc;
  double BjetLdgJetMass;
  double BjetSubldgJetMass;

};
*/
