#!/bin/csh
#================================
# LAST USED:
#================================
# Default Training:   DR < 0.3 && DPt/Pt < 0.32
# Other Training:     DR < 0.3
#
# BDT -0.90: ./doPlots.csh TopTaggerEfficiency_180717_033003_BDT_m0p90_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_034243_BDT_m0p90_TopMassCut400_TrainingBJet40_OtherTraining -0.90
# BDT -0.80: ./doPlots.csh TopTaggerEfficiency_180717_033905_BDT_m0p80_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_034729_BDT_m0p80_TopMassCut400_TrainingBJet40_OtherTraining -0.80
# BDT -0.70: ./doPlots.csh TopTaggerEfficiency_180717_040055_BDT_m0p70_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_040045_BDT_m0p70_TopMassCut400_TrainingBJet40_OtherTraining -0.70
# BDT -0.60: ./doPlots.csh TopTaggerEfficiency_180717_043046_BDT_m0p60_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_041859_BDT_m0p60_TopMassCut400_TrainingBJet40_OtherTraining -0.60
# BDT -0.50: ./doPlots.csh TopTaggerEfficiency_180717_043850_BDT_m0p50_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_042316_BDT_m0p50_TopMassCut400_TrainingBJet40_OtherTraining -0.50
# BDT -0.40: ./doPlots.csh TopTaggerEfficiency_180717_045258_BDT_m0p40_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_042959_BDT_m0p40_TopMassCut400_TrainingBJet40_OtherTraining -0.40
# BDT -0.30: ./doPlots.csh TopTaggerEfficiency_180717_050121_BDT_m0p30_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_043421_BDT_m0p30_TopMassCut400_TrainingBJet40_OtherTraining -0.30
# BDT -0.20: ./doPlots.csh TopTaggerEfficiency_180717_051813_BDT_m0p20_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_044543_BDT_m0p20_TopMassCut400_TrainingBJet40_OtherTraining -0.20
# BDT -0.10: ./doPlots.csh TopTaggerEfficiency_180717_052713_BDT_m0p10_TopMassCut400_TrainingBJet40_DefaultTraining TopTaggerEfficiency_180718_044957_BDT_m0p10_TopMassCut400_TrainingBJet40_OtherTraining -0.10
# BDT  0.00: ./doPlots.csh TopTaggerEfficiency_180717_065545_BDT_0p00_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_045359_BDT_0p00_TopMassCut400_TrainingBJet40_OtherTraining   0.00
# BDT  0.10: ./doPlots.csh TopTaggerEfficiency_180717_070547_BDT_0p10_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_050251_BDT_0p10_TopMassCut400_TrainingBJet40_OtherTraining   0.10
# BDT  0.20: ./doPlots.csh TopTaggerEfficiency_180717_074103_BDT_0p20_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_050733_BDT_0p20_TopMassCut400_TrainingBJet40_OtherTraining   0.20
# BDT  0.30: ./doPlots.csh TopTaggerEfficiency_180717_074911_BDT_0p30_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_051149_BDT_0p30_TopMassCut400_TrainingBJet40_OtherTraining   0.30
# BDT  0.40: ./doPlots.csh TopTaggerEfficiency_180717_081727_BDT_0p40_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_051601_BDT_0p40_TopMassCut400_TrainingBJet40_OtherTraining   0.40
# BDT  0.50: ./doPlots.csh TopTaggerEfficiency_180717_083328_BDT_0p50_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_061343_BDT_0p50_TopMassCut400_TrainingBJet40_OtherTraining   0.50
# BDT  0.60: ./doPlots.csh TopTaggerEfficiency_180717_084203_BDT_0p60_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_061835_BDT_0p60_TopMassCut400_TrainingBJet40_OtherTraining   0.60
# BDT  0.70: ./doPlots.csh TopTaggerEfficiency_180717_084936_BDT_0p70_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_062208_BDT_0p70_TopMassCut400_TrainingBJet40_OtherTraining   0.70
# BDT  0.80: ./doPlots.csh TopTaggerEfficiency_180717_085614_BDT_0p80_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_062549_BDT_0p80_TopMassCut400_TrainingBJet40_OtherTraining   0.80
# BDT  0.90: ./doPlots.csh TopTaggerEfficiency_180717_090250_BDT_0p90_TopMassCut400_TrainingBJet40_DefaultTraining  TopTaggerEfficiency_180718_062921_BDT_0p90_TopMassCut400_TrainingBJet40_OtherTraining   0.90

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
