#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyConvertCollection.h"
#include "Math/VectorUtil.h"

using std::string;
using std::map;
using std::pair;
using std::vector;
using std::cout;
using std::ostream;
using std::endl;

ClassImp(MyJet)

MyJet::MyJet():
  TLorentzVector(0, 0, 0, 0),
  originalP4(0, 0, 0, 0),
  type(0)
{}

MyJet::MyJet(double px, double py, double pz, double E):
  TLorentzVector(px, py, pz, E),
  originalP4(px, py, pz, E),
  type(0)
{}


MyJet::~MyJet() {}

///////////////////////////

double MyJet::Ex() const { return Px(); }
double MyJet::Ey() const { return Py(); }
double MyJet::Ez() const { return Pz(); }

double MyJet::pt()  const { return Pt(); }
double MyJet::eta() const { return Eta(); }
double MyJet::phi() const { return Phi(); }

double MyJet::px()  const { return Px(); }
double MyJet::py()  const { return Py(); }
double MyJet::pz()  const { return Pz(); }
double MyJet::p()  const { return P(); }
double MyJet::energy()  const { return E(); }

TLorentzVector MyJet::p4() const {
  return TLorentzVector(Px(), Py(), Pz(), E());
}

void MyJet::setP4(const TLorentzVector& vector){
  SetXYZT(vector.Px(), vector.Py(), vector.Pz(), vector.E());
}

////////////////////////////

void MyJet::addEnergyCorrection(const std::string& name, double value) {
  pair<map<string, double>::iterator, bool> ret = jecs.insert(make_pair(name, value));
  if(!ret.second) {
    cout << "Unable to add energy correction " << name << ".";
    if(jecs.find(name) != jecs.end())
      cout << " A correction with the same name already exists.";
    cout << endl;
    exit(0);
  }
}

void MyJet::setEnergyCorrection(const std::string& name) {
  double correction = getEnergyCorrectionFactor(name);

  currentCorrection = name;
  SetXYZT(originalP4.X() * correction,
          originalP4.Y() * correction,
          originalP4.Z() * correction,
          originalP4.T() * correction);
}

double MyJet::getEnergyCorrectionFactor(const std::string& name) const {
  if(name == "raw" || name == "" || name == "none")
    return 1;

  map<string, double>::const_iterator found = jecs.find(name);
  if(found == jecs.end()) {
    cout << "Requested energy correction " << name << " doesn't exist." << endl;
    exit(0);
  }

  return found->second;
}

bool MyJet::hasEnergyCorrection(const std::string& name) const {
  map<string, double>::const_iterator found = jecs.find(name);
  return found != jecs.end();
}

const std::string& MyJet::getActiveEnergyCorrectionName() const {
  return currentCorrection;
}

double MyJet::getActiveEnergyCorrectionFactor() const {
  return getEnergyCorrectionFactor(currentCorrection);
}

// helper
std::vector<MyTrack *> MyJet::getTracksAroundP4(const TLorentzVector& p4, double signalCone) {
  vector<MyTrack *> selectedTracks;
  vector<MyTrack>::const_iterator i;
  for(vector<MyTrack>::iterator i = tracks.begin(); i != tracks.end(); ++i){
    double DR = ROOT::Math::VectorUtil::DeltaR(p4, i->p4());
    if(DR < signalCone)
      selectedTracks.push_back(&(*i));
  }
  return selectedTracks;
}

vector<MyTrack*> MyJet::getTracks(double signalCone) {
  return getTracksAroundP4(p4(), signalCone);
}

vector<MyTrack *> MyJet::getTracksAroundLeadingTrack(double signalCone,double matchingCone) {
  return getTracksAroundP4(leadingTrack(matchingCone)->p4(), signalCone);
}

const MyTrack *MyJet::leadingTrack(double matchingCone) const {
  const MyTrack *theLeadingTrack = 0;
  double ptmax = 0;
  for(vector<MyTrack>::const_iterator i = tracks.begin(); i != tracks.end(); ++i) {
    if(i->pt() == 0) continue;
    if(i->charge() == 0) continue;
    // Require track to be within Delta IPz < 1 mm
    if(TMath::Abs(i->impactParameter().impactParameterZ().value()) > 0.1) continue;
    // Require track to be within IPT < 0.3 mm
    if(TMath::Abs(i->impactParameter().impactParameter2D().value()) > 0.03) continue;

    double DR = ROOT::Math::VectorUtil::DeltaR(p4(),i->p4());
    if(DR > matchingCone) continue;

    if(i->Pt() > ptmax){
      ptmax = i->Pt();
      theLeadingTrack = &(*i);
    }
  }
  return theLeadingTrack;
}

vector<MyVertex *> MyJet::getSecVertices() {
  return convertCollection(secVertices);
}

vector<MyHit *> MyJet::getHits() {
  return convertCollection(hits);
}

vector<MyCaloTower *> MyJet::getCaloInfo() {
  return convertCollection(caloInfo);
}

double MyJet::tag(const std::string& name) const {
  map<string, double>::const_iterator found = tagInfo.find(name);
  if(found == tagInfo.end()) {
    if(tracks.size() == 0) cout << "No tracks!" << endl;
    cout << "Requested tag " << name << " doesn't exist." << endl;
    exit(0);
  }
  return found->second;
}

bool MyJet::hasTag(const std::string& name) const {
  map<string, double>::const_iterator found = tagInfo.find(name);
  return found != tagInfo.end();
}


TLorentzVector MyJet::combinedTracksMomentum(double signalCone,double matchingCone) const {
  TLorentzVector p(0,0,0,0);

  const MyTrack *leadingtrack = leadingTrack(matchingCone);
  if(!leadingtrack)
    return p;

  for(vector<MyTrack>::const_iterator i = tracks.begin(); i != tracks.end(); ++i) {
    if(i->charge() == 0) continue;
    double DR = ROOT::Math::VectorUtil::DeltaR(leadingtrack->p4(), i->p4());
    if(DR > signalCone) continue;
    p += i->p4();
  }
  return p;
}

TLorentzVector MyJet::ecalClusterMomentum(double signalCone, double matchingCone) const {
  TVector3 ecalHitPoint(0,0,0);

  const MyTrack *leadingtrack = leadingTrack(matchingCone);
  if(!leadingtrack) {
    ecalHitPoint = p4().BoostVector();
  }
  else {
    ecalHitPoint = leadingtrack->ecalHitPoint().tvector3();
  }

  TVector3 cluster(0,0,0);

  for(vector<MyCaloTower>::const_iterator i = caloInfo.begin(); i != caloInfo.end(); ++i) {
    vector<TVector3> cells = i->ECALCells;
    for(vector<TVector3>::const_iterator j; j != cells.end(); ++j) {
      double DR = ROOT::Math::VectorUtil::DeltaR(ecalHitPoint, *j);
      if(DR < signalCone)
        cluster += *j;
    }
  }

  return TLorentzVector(cluster, cluster.Mag());
}

TLorentzVector MyJet::hcalClusterMomentum(double signalCone, double matchingCone) const {
  TVector3 hcalHitPoint(0,0,0);

  const MyTrack *leadingtrack = leadingTrack(matchingCone);
  if(!leadingtrack) {
    hcalHitPoint = p4().BoostVector();
  }
  else {
    hcalHitPoint = leadingtrack->ecalHitPoint().tvector3();
  }

  TVector3 cluster(0,0,0);

  for(vector<MyCaloTower>::const_iterator i = caloInfo.begin(); i != caloInfo.end(); ++i) {
    vector<TVector3> cells = i->HCALCells;
    for(vector<TVector3>::const_iterator j; j != cells.end(); ++j) {
      double DR = ROOT::Math::VectorUtil::DeltaR(hcalHitPoint, *j);
      if(DR < signalCone)
        cluster += *j;
    }
  }

  return TLorentzVector(cluster, cluster.Mag());
}

vector<TLorentzVector *> MyJet::getClusters() {
  return convertCollection(clusters);
}

template <class C>
void printCollection(std::ostream& out, const C& coll, const char *name) {
  if(coll.size() == 0)
    return;

  out << "      " << name << " " << coll.size() << endl;
  for(typename C::const_iterator i = coll.begin(); i != coll.end(); ++i) {
    i->print();
  }
  
}
template <class C>
void printMap(std::ostream& out, const C& coll, const char *name) {
  if(coll.size() == 0)
    return;

  out << "      " << name << " " << coll.size() << endl;
  for(typename C::const_iterator i = coll.begin(); i != coll.end(); ++i) {
    cout << "        " << i->first << " "  << i->second << endl;
  }
  
}

void MyJet::printTracks(std::ostream& out) const {
  printCollection(out, tracks, "tracks");
}
void MyJet::printVertices(std::ostream& out) const {
  printCollection(out, secVertices, "vertices");
}
void MyJet::printCaloInfo(std::ostream& out) const {
  printCollection(out, caloInfo, "caloTowers");
}
void MyJet::printTagInfo(std::ostream& out) const {
  printMap(out, tagInfo, "tagInfo");
}
void MyJet::printEnergyCorrections(std::ostream& out) const {
  printMap(out, jecs, "jetEnergyCorrections");
}

void MyJet::printCorrections(std::ostream& out) const {
  if(jecs.size() == 0)
    return;
  for(map<string,double>::const_iterator i = jecs.begin(); i!= jecs.end(); ++i) {
    out << "          " << i->first << endl;
  }
}

void MyJet::print(std::ostream& out) const {
  printTracks(out);
  printVertices(out);
  printCaloInfo(out);
  printTagInfo(out);
  printEnergyCorrections(out);
  out << endl;
}

void useCorrection(std::vector<MyJet *>& jets, const std::string& name) {
  for(vector<MyJet *>::iterator p = jets.begin(); p != jets.end(); ++p) {
    (*p)->setEnergyCorrection(name);
  }
}
