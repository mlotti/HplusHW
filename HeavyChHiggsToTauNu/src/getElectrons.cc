#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronTag.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/Common/interface/ValueMap.h"


vector<MyJet> MyEventConverter::getElectrons(const edm::Event& iEvent,const edm::EventSetup& iSetup, const edm::InputTag& label){
	vector<MyJet> electrons;

        Handle<GsfElectronCollection> electronHandle;
        iEvent.getByLabel(label, electronHandle);
        if(!electronHandle.isValid())
                return electrons;

        const GsfElectronCollection & recoElectrons = *(electronHandle.product());
        cout << "Offline electron collection size " << recoElectrons.size() << endl;

        EcalClusterLazyTools lazyTools(iEvent,iSetup,reducedBarrelRecHitCollection,reducedEndcapRecHitCollection);
        for(unsigned int i = 0; i < recoElectrons.size(); ++i){
		MyJet electron = myJetConverter(recoElectrons[i]);

		edm::Ref<reco::GsfElectronCollection> iElectron(electronHandle,i);
		for(unsigned int ietag = 0; ietag < electronIdLabels.size(); ++ietag){
			edm::Handle<edm::ValueMap<float> > electronIdHandle;
			iEvent.getByLabel(electronIdLabels[ietag], electronIdHandle );
			const edm::ValueMap<float> & electronId = *(electronIdHandle.product());

			electron.tagInfo[electronIdLabels[ietag].label()] = electronId[iElectron];
		}

		ElectronTag::tag(*iElectron,lazyTools,electron.tagInfo);

		electrons.push_back(electron);
        }

        return electrons;
}
