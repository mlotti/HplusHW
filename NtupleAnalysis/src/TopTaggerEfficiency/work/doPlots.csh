#!/bin/csh
#================================
# LAST USED:
#================================
# BDT cut -0.80: ./doPlots.csh TopTaggerEfficiency_180710_045319_BDT_m0p80_DefaultTraining TopTaggerEfficiency_180712_024546_BDT_m0p80_OtherTraining -0.80
# BDT cut -0.60: ./doPlots.csh TopTaggerEfficiency_180710_044534_BDT_m0p60_DefaultTraining TopTaggerEfficiency_180712_025319_BDT_m0p60_OtherTraining -0.60
# BDT cut -0.40: ./doPlots.csh TopTaggerEfficiency_180710_043542_BDT_m0p40_DefaultTraining TopTaggerEfficiency_180712_031225_BDT_m0p40_OtherTraining -0.40
# BDT cut -0.20: ./doPlots.csh TopTaggerEfficiency_180710_042228_BDT_m0p20_DefaultTraining TopTaggerEfficiency_180712_032136_BDT_m0p20_OtherTraining -0.20
# BDT cut  0.00: ./doPlots.csh TopTaggerEfficiency_180704_034821_BDT_0p00_DefaultTraining  TopTaggerEfficiency_180704_062045_BDT_0p00_OtherTraining   0.00
# BDT cut  0.10: ./doPlots.csh TopTaggerEfficiency_180704_035600_BDT_0p10_DefaultTraining  TopTaggerEfficiency_180704_062956_BDT_0p10_OtherTraining   0.10
# BDT cut  0.20: ./doPlots.csh TopTaggerEfficiency_180704_041515_BDT_0p20_DefaultTraining  TopTaggerEfficiency_180704_063844_BDT_0p20_OtherTraining   0.20
# BDT cut  0.30: ./doPlots.csh TopTaggerEfficiency_180704_042126_BDT_0p30_DefaultTraining  TopTaggerEfficiency_180704_072414_BDT_0p30_OtherTraining   0.30
# BDT cut  0.40: ./doPlots.csh TopTaggerEfficiency_180704_042603_BDT_0p40_DefaultTraining  TopTaggerEfficiency_180704_072108_BDT_0p40_OtherTraining   0.40
# BDT cut  0.50: ./doPlots.csh TopTaggerEfficiency_180704_042603_BDT_0p40_DefaultTraining  TopTaggerEfficiency_180704_072108_BDT_0p40_OtherTraining   0.50
# BDT cut  0.60: ./doPlots.csh TopTaggerEfficiency_180704_043957_BDT_0p60_DefaultTraining  TopTaggerEfficiency_180704_073136_BDT_0p60_OtherTraining   0.60
# BDT cut  0.70: ./doPlots.csh TopTaggerEfficiency_180704_044510_BDT_0p70_DefaultTraining  TopTaggerEfficiency_180704_073451_BDT_0p70_OtherTraining   0.70
# BDT cut  0.80: ./doPlots.csh TopTaggerEfficiency_180704_051420_BDT_0p80_DefaultTraining  TopTaggerEfficiency_180704_073738_BDT_0p80_OtherTraining   0.80
# BDT cut  0.90: ./doPlots.csh TopTaggerEfficiency_180704_055838_BDT_0p90_DefaultTraining  TopTaggerEfficiency_180704_074041_BDT_0p90_OtherTraining   0.90

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments:"
    echo "1 = The pseudo-multicrab with the default training"
    echo "2 = The pseudo-multicrab with the other training"
    echo "3 = The BDT cut studied"
    echo "\n=== For example:"
    echo "./doPlots.csh TopTaggerEfficiency_180704_042603_BDT_0p40_DefaultTraining TopTaggerEfficiency_180704_072108_BDT_0p40_OtherTraining 0.40"
    exit 1
endif

#================================================================================================ 
# Define variables                                                                                                                   
#================================================================================================
set INITIAL = `echo $USER | cut -c1-1`
set PSEUDO_MCRAB_DIR_DEFAULT = ${1}
set PSEUDO_MCRAB_DIR_OTHER   = ${2}
set BDT_CUT = ${3}

echo "\n==== Running ttbar variations (shower scales, high pT radiation, mTop, parton shower, evtGen)"
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR_DEFAULT --type showerScales --bdt $BDT_CUT
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR_DEFAULT --type highPtRadiation --bdt $BDT_CUT
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR_DEFAULT --type mTop --bdt $BDT_CUT
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR_DEFAULT --type partonShower --bdt $BDT_CUT
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR_DEFAULT --type evtGen --bdt $BDT_CUT

echo "\n==== Running default ttbar with different training (mathing definition)"
./plot_MatchingDefinition.py -m $PSEUDO_MCRAB_DIR_DEFAULT -s $PSEUDO_MCRAB_DIR_OTHER --bdt $BDT_CUT

echo "\n==== Merging JSON files"
./mergeJSONs.py --bdt $BDT_CUT

echo "\n==== Done"
