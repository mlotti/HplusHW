#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "RecoTauTag/TauTagTools/interface/CaloTauElementsOperators.h"
#include "RecoTauTag/TauTagTools/interface/PFTauElementsOperators.h"

map<string,double> MyEventConverter::tauTag(const IsolatedTauTagInfo& jet){
	map<string,double> tagInfo;

        double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1;

        tagInfo["discriminator"] = 
		jet.discriminator(matchingConeSize,
				  signalConeSize,
                                  isolationConeSize,
                                  ptLeadingTrackMin,
                                  ptOtherTracksMin);

	return tagInfo;
}

map<string,double> MyEventConverter::tauTag(const CaloTau& tau){
        map<string,double> tagInfo;

	CaloTau theCaloTau = tau;
	CaloTauElementsOperators theCaloTauElementsOperators(theCaloTau);

        double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0;

//	double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(0);
	double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(
                                metric,
                                matchingConeSize,
                                ptLeadingTrackMin,
                                ptOtherTracksMin,
                                metric,
                                signalConeSize,
                                metric,
                                isolationConeSize,
                                isolationAnnulus_Tracksmaxn);

        tagInfo["d_trackIsolation"]   = d_trackIsolation;
/*
	double d_leadingTrack = 1;
	if(!theCaloTau.leadTrack()) d_leadingTrack = 0;
        tagInfo["d_leadingTrack"]     = d_leadingTrack;
*/
        return tagInfo;
}

map<string,double> MyEventConverter::tauTag(const PFTau& tau){
        map<string,double> tagInfo;

	PFTau thePFTau = tau;
	PFTauElementsOperators thePFTauElementsOperators(thePFTau);

        double matchingConeSize         = 0.1,
               signalConeSize           = 0.07,
               isolationConeSize        = 0.4,
               ptLeadingTrackMin        = 20,
               ptOtherTracksMin         = 1;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0;

//	double d_trackIsolation   = thePFTauElementsOperators.discriminatorByIsolTracksN(0);
	double d_trackIsolation = thePFTauElementsOperators.discriminatorByIsolTracksN(
                                metric,
                                matchingConeSize,
                                ptLeadingTrackMin,
                                ptOtherTracksMin,
                                metric,
                                signalConeSize,
                                metric,
                                isolationConeSize,
                                isolationAnnulus_Tracksmaxn);
        tagInfo["d_trackIsolation"]   = d_trackIsolation;

	double d_pftrackIsolation = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN(0);
        tagInfo["d_pftrackIsolation"] = d_pftrackIsolation;

	double d_ecalIsolation = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN(0);
        tagInfo["d_ecalIsolation"]    = d_ecalIsolation;
/*
	double d_leadingTrack = 1;
	if(!thePFTau.leadTrack()) d_leadingTrack = 0;
        tagInfo["d_leadingTrack"]     = d_leadingTrack;

        double d_leadingPFTrack = 1;
        if(!thePFTau.leadPFChargedHadrCand()) d_leadingPFTrack = 0;
        tagInfo["d_leadingPFTrack"]   = d_leadingPFTrack;
*/
/*
	cout << "check MyEventConverter::tauTag " << d_trackIsolation << " " 
		<< d_pftrackIsolation << " "
		<< d_ecalIsolation << " "
		<< d_leadingTrack << " "
		<< d_leadingPFTrack << endl;
*/
/*
        double Rmatch  = 0.1,
               Rsignal = 0.07,
               Riso    = 0.4,
               pT_LT   = 6,
               pT_min  = 1;

        tagInfo["discriminator"] =
                jet.discriminatorByIsolPFChargedHadrCandsN(Rmatch,
                                                           Rsignal,
                                                           Riso,
                                                           true,
                                                           pT_LT,
                                                           pT_min);
*/
        return tagInfo;
}

