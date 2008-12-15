#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::getTrajectories(const edm::Event& iEvent){
        iEvent.getByLabel(trajectoryInput, myTrajectoryCollectionHandle);
        cout << "Trajectory collection size=" << myTrajectoryCollectionHandle->size() << endl;
}

