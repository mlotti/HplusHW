#!/bin/csh   

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 1) then
    echo "=== You must give exactly 1 argument:"
    echo "1=PSEUDO_MCRAB_DIR"
    echo "\n=== For example:"
    echo "./doPlots.csh FakeBMeasurement_PreSel_3CSVv2M_Pt40Pt40Pt30_InvSel_3CSVv2L_2CSVv2M_LdgBjetIsCSVv2M_MVA0p60to0p85_4BinsEta0p4Eta1p2Eta1p8_FatjetVetoPt450Type1_180301_144503"
    echo
    exit 1
endif

#================================================================================================
# Define variables                                                                               
#================================================================================================                                                                                                                                 
set PSEUDO_MCRAB_DIR = ${1}

./plot_Closure.py -m $PSEUDO_MCRAB_DIR -n --url
./plot_ClosureBinned.py -m $PSEUDO_MCRAB_DIR -n --url
./plot_FailedBJet.py -m  $PSEUDO_MCRAB_DIR --url
./plot_Purity.py -m $PSEUDO_MCRAB_DIR --url
./plot_DataMC.py -m $PSEUDO_MCRAB_DIR --folder counters/weighted --url
./getABCD_TF.py -m $PSEUDO_MCRAB_DIR --url 
./makePseudoMulticrab.py -m  $PSEUDO_MCRAB_DIR --url
./plot_MediumVsLoose.py -m $PSEUDO_MCRAB_DIR --dataset EWK --refBdisc Medium --url
./plot_MediumAndLoose.py -m $PSEUDO_MCRAB_DIR --dataset EWK --normalizeToOne --url
