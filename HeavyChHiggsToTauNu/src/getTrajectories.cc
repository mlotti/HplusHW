#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"

#include<iostream>
using std::cout;
using std::endl;

void MyEventConverter::getTrajectories(const edm::Event& iEvent){
        iEvent.getByLabel(trajectoryInput, myTrajectoryCollectionHandle);
        cout << "Trajectory collection size=" << myTrajectoryCollectionHandle->size() << endl;
}

