#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyEventConverter::MyEventConverter(){
        init();
}

MyEventConverter::~MyEventConverter(){

        cout << endl << endl;
        cout << "    SUMMARY " << endl << endl;
        cout << "    All events   : " << allEvents << endl;
//        cout << "    HLT          : " << triggeredEvents << endl;
//        cout << "    PV reconstr. : " << eventsWithPrimaryVertex << endl;
        cout << "    saved events : " << savedEvents << endl;
        cout << endl << endl;


        delete tauMETTriggerAnalysis;

	userRootTree->setAcceptance("allEvents",allEvents);
//	userRootTree->setAcceptance("HLTselection",triggeredEvents);
//        userRootTree->setAcceptance("eventsWithPrimaryVertex",eventsWithPrimaryVertex);
        userRootTree->setAcceptance("savedEvents",savedEvents);
        delete userRootTree;

	delete tauResolutionAnalysis;
}


void MyEventConverter::init(){

	electronIdAlgo = new CutBasedElectronID();
	userRootTree = new MyRootTree();

	// counters
	allEvents 		= 0;
	triggeredEvents 	= 0;
	eventsWithPrimaryVertex = 0;
	savedEvents 		= 0;

	tauResolutionAnalysis = new TauResolutionAnalysis();
	tauMETTriggerAnalysis = new TauMETTriggerAnalysis(userRootTree);
}
