#ifndef GEN_JET
#define GEN_JET

using namespace std;

#include "TROOT.h"
#include "TLorentzVector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyVertex.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyCaloTower.h"

#include <vector>
#include <map>
#include <iostream>
#include <string>

double myDeltaR(double,double,double,double);

class MyJet : public TLorentzVector {
  public:
    	MyJet();
        MyJet(double,double,double,double);
    	virtual ~MyJet();

    	double   Et() const;
    	double   E() const; // calculating E from Ex,Ey,Ez

    	double   Ex() const;
    	double   Ey() const;
    	double   Ez() const;

        double   pt()  const;
        double   eta() const;
        double   phi() const;

        double   px()  const;
        double   py()  const;
        double   pz()  const;
        double   p()   const;
        double   energy() const;


        TLorentzVector 	    p4() const;
        void 		    setP4(TLorentzVector&);
        TLorentzVector      combinedTracksMomentum(double,double matchingCone = 0.1) const;
	TLorentzVector	    ecalClusterMomentum(double,double matchingCone = 0.1) const;
        TLorentzVector      hcalClusterMomentum(double,double matchingCone = 0.1) const;

	void 		    setJetEnergyCorrection(string,double);
    	double              getCorrectionFactor(string) const;
	MyJet		    recalculateEnergy(string) const;
	vector<string> 	    getCorrectionNames() const;

    	vector<MyTrack>     getTracks(double cone = 0.7) const;
	inline vector<MyTrack>::const_iterator tracks_begin() const { return tracks.begin();}
        inline vector<MyTrack>::const_iterator tracks_end() const { return tracks.end();}

        vector<MyTrack>     getTracksAroundLeadingTrack(double signalCone,double matchingCone = 0.1) const;

    	vector<MyVertex>    getSecVertices() const;
        inline vector<MyVertex>::const_iterator secVertices_begin() const { return secVertices.begin();}
        inline vector<MyVertex>::const_iterator secVertices_end() const { return secVertices.end();}

    	vector<MyCaloTower> getCaloInfo() const;
        inline vector<MyCaloTower>::const_iterator caloInfo_begin() const { return caloInfo.begin();}
        inline vector<MyCaloTower>::const_iterator caloInfo_end() const { return caloInfo.end();}

	double 		    tag(string) const;
	bool 		    btag(double) const;
	MyTrack		    leadingTrack(double matchingCone = 0.1) const;


    	int      type;

    	vector<MyTrack>         tracks;
	vector<MyHit>           hits; // hits associated to tracks
    	vector<MyVertex>        secVertices;
    	vector<MyCaloTower>     caloInfo;
    	map<string,double>      tagInfo;
	map<string,double>	jetEnergyCorrection;

	void printTracks() const;
	void printVertices() const;
	void printCaloInfo() const;
	void printTagInfo() const;
	void printEnergyCorrections() const;
	void printCorrections() const;
	void print() const;

  private:
    	ClassDef(MyJet,1)
};
#endif
