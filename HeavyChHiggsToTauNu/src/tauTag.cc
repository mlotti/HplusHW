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
               ptOtherTracksMin         = 1,
	       useOnlyChargedHadrforleadPFCand	= true,
	       IsolPFCands_maxEtSum	= 0;
        string metric = "DR"; // can be DR,angle,area
        unsigned int isolationAnnulus_Tracksmaxn = 0,
		     IsolPFCands_maxN = 0;

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

	double d_IsolPFCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_1"] = d_IsolPFCandsEtSum_1;

// second discrimintor d_IsolPFCandsEtSum
	double d_IsolPFCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_2"] = d_IsolPFCandsEtSum_2;

// third discrimintor d_IsolPFCandsEtSum
	double d_IsolPFCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFCandsEtSum (IsolPFCands_maxEtSum);
        tagInfo["d_IsolPFCandsEtSum_3"] = d_IsolPFCandsEtSum_3;



	double d_IsolPFCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFCandsN(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_1"] = d_IsolPFCandsN_1;

//Second discriminator d_IsolPFCandsN, can't be used simultanieosly

double d_IsolPFCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_2"] = d_IsolPFCandsN_2;


//Third d_IsolPFCandsN discriminator

double d_IsolPFCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFCandsN_3"] = d_IsolPFCandsN_3;

	double 	d_IsolPFChargedHadrCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_1"] = d_IsolPFChargedHadrCandsEtSum_1;

// Second discriminator d_IsolPFChargedHadrCandsEtSum

	double 	d_IsolPFChargedHadrCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum(
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_2"] = d_IsolPFChargedHadrCandsEtSum_2;	

// Third discriminator d_IsolPFChargedHadrCandsEtSum

double 	d_IsolPFChargedHadrCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFChargedHadrCandsEtSum_3"] = d_IsolPFChargedHadrCandsEtSum_3;


double 	d_IsolPFGammaCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_1"] = d_IsolPFGammaCandsEtSum_1;

//Second discriminator d_IsolPFGammaCandsEtSum

double 	d_IsolPFGammaCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_2"] = d_IsolPFGammaCandsEtSum_2;


//Third discriminator d_IsolPFGammaCandsEtSum

double 	d_IsolPFGammaCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsEtSum (
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFGammaCandsEtSum_3"] = d_IsolPFGammaCandsEtSum_3;


	double d_IsolPFChargedHadrCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_1"] = d_IsolPFChargedHadrCandsN_1;

//Second discriminator d_IsolPFChargedHadrCandsN

double d_IsolPFChargedHadrCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_2"] = d_IsolPFChargedHadrCandsN_2;


//Third d_IsolPFCandsN discriminator
double d_IsolPFChargedHadrCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFChargedHadrCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFChargedHadrCandsN_3"] = d_IsolPFChargedHadrCandsN_3;


double 	d_IsolPFNeutrHadrCandsEtSum_1 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum 					(thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_1"] = d_IsolPFNeutrHadrCandsEtSum_1;

//Second discriminator d_IsolPFNeutrHadrCandsEtSum
double 	d_IsolPFNeutrHadrCandsEtSum_2 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum (
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_2"] = d_IsolPFNeutrHadrCandsEtSum_2;

//Third discriminator d_IsolPFNeutrHadrCandsEtSum
double 	d_IsolPFNeutrHadrCandsEtSum_3 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsEtSum (
				IsolPFCands_maxEtSum);
	tagInfo["d_IsolPFNeutrHadrCandsEtSum_3"] = d_IsolPFNeutrHadrCandsEtSum_3;



double d_IsolPFGammaCandsN_1  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_1"] = d_IsolPFGammaCandsN_1;

//Second discriminator d_IsolPFGammaCandsN
double d_IsolPFGammaCandsN_2  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_2"] = d_IsolPFGammaCandsN_2;


//Third d_IsolPFCandsN discriminator
double d_IsolPFGammaCandsN_3  = thePFTauElementsOperators.discriminatorByIsolPFGammaCandsN  ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFGammaCandsN_3"] = d_IsolPFGammaCandsN_3;



double d_IsolPFNeutrHadrCandsN_1 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN (thePFTau.momentum(), 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCandsN_1"] = d_IsolPFNeutrHadrCandsN_1;

//Second discriminator d_IsolPFNeutrHadrCandsN
double d_IsolPFNeutrHadrCandsN_2 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN  ( 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCands_2"] = d_IsolPFNeutrHadrCandsN_2;

//Third d_IsolPFNeutrHadrCandsN discriminator
double d_IsolPFNeutrHadrCandsN_3 = thePFTauElementsOperators.discriminatorByIsolPFNeutrHadrCandsN ( 
				metric, 
				matchingConeSize, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				useOnlyChargedHadrforleadPFCand, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				IsolPFCands_maxN);
        tagInfo["d_IsolPFNeutrHadrCandsN_3"] = d_IsolPFNeutrHadrCandsN_3;



//----------------------------------------------------------------
//------------------end of discriminators-------------------------
//----------------------------------------------------------------

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

