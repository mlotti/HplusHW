#ifndef __MyEvent__
#define __MyEvent__

namespace std{}
using namespace std;

#include "TROOT.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MySimTrack.h" // LAW 11.02.08

#include <vector>
#include <iostream>
#include <iomanip>

class MyEvent : public TObject {
    public:
	MyEvent();
    	virtual ~MyEvent();

    	inline short int event(){return eventNumber;}
    	inline short int run(){return runNumber;}

    	short int     eventNumber;
    	short int     runNumber;

    // Rec event
	bool trigger(string);

    	MyGlobalPoint getPrimaryVertex();

    	vector<MyJet> getL1objects();
        inline vector<MyJet>::const_iterator L1objects_begin(){return L1objects.begin();}
        inline vector<MyJet>::const_iterator L1objects_end(){return L1objects.end();}

    	vector<MyJet> getHLTobjects();
        inline vector<MyJet>::const_iterator HLTobjects_begin(){return HLTobjects.begin();}
        inline vector<MyJet>::const_iterator HLTobjects_end(){return HLTobjects.end();}

    	vector<MyJet> getElectrons();
        inline vector<MyJet>::const_iterator electrons_begin(){return electrons.begin();}
        inline vector<MyJet>::const_iterator electrons_end(){return electrons.end();}

    	vector<MyJet> getPhotons();
        inline vector<MyJet>::const_iterator photons_begin(){return photons.begin();}
        inline vector<MyJet>::const_iterator photons_end(){return photons.end();}

    	vector<MyJet> getMuons();
        inline vector<MyJet>::const_iterator muons_begin(){return muons.begin();}
        inline vector<MyJet>::const_iterator muons_end(){return muons.end();}

    	vector<MyJet> getTaujets();
        inline vector<MyJet>::const_iterator taujets_begin(){return taujets.begin();}
        inline vector<MyJet>::const_iterator taujets_end(){return taujets.end();}

    	vector<MyJet> getPFTaus();
        inline vector<MyJet>::const_iterator pftaus_begin(){return pftaus.begin();}
        inline vector<MyJet>::const_iterator pftaus_end(){return pftaus.end();}

    	vector<MyJet> getJets();
        //inline vector<MyJet>::const_iterator jets_begin(){return jets.begin();}
        //inline vector<MyJet>::const_iterator jets_end(){return jets.end();}

    	vector<MyJet> getJets(string);
        vector<MyJet> getTaujets(string);

    	MyMET         getMET();

    	void 	      listJetCorrections();
    	void          print();
    	void          printAll();
	void	      printCorrections();

    // rec data
	map<string,bool> triggerResults;

    	MyGlobalPoint primaryVertex;

    	vector<MyJet> L1objects;
    	vector<MyJet> HLTobjects;
    	vector<MyJet> electrons;
    	vector<MyJet> photons;
    	vector<MyJet> muons;
    	vector<MyJet> taujets;
    	vector<MyJet> pftaus;
    	vector<MyJet> jets;

    	MyMET         MET;

  // MC event
    	MyMET            getMCMET();
    	MyGlobalPoint 	 getMCPrimaryVertex();

    	vector<MyMCParticle> getMCParticles();
        inline vector<MyMCParticle>::const_iterator mcParticles_begin(){return mcParticles.begin();}
        inline vector<MyMCParticle>::const_iterator mcParticles_end(){return mcParticles.end();}

    	vector<MySimTrack>   getSimTracks();
        inline vector<MySimTrack>::const_iterator simTracks_begin(){return simTracks.begin();}
        inline vector<MySimTrack>::const_iterator simTracks_end(){return simTracks.end();}

    // MC data
    	MyMET         	 mcMET;
    	MyGlobalPoint        mcPrimaryVertex;
    	vector<MyMCParticle> mcParticles;
    	vector<MySimTrack>   simTracks; // LAW 12.02.08

    private:

    	ClassDef(MyEvent,1) // The macro
};

#endif
