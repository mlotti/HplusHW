#!/bin/csh   
#./doPlots.csh /uscms_data/d3/skonstan/workspace/pseudo-multicrab/TopRecoAnalysis/TopRecoAnalysis_180524_052417_Mcrab644_BDT_DR0p3_DPtOverPt0p32_PtReweighting/

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 1) then
    echo "=== You must give exactly 1 argument:"
    echo "1=PSEUDO_MCRAB_DIR"
    echo "\n=== For example:"
    echo "./doPlots.csh Hplus2tbAnalysis_PreSel_3CSVv2M_Pt40Pt40Pt30_SigSel_MVA0p85_FatjetVetoPt450Type1_180301_132908"
    echo
    exit 1
endif

#================================================================================================
# Define variables                                                                               
#================================================================================================
set DIR = ${1}

./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Genuine --type showerScales
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Genuine --type highPtRadiation
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Genuine --type colourReconnection
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Genuine --type mTop
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Genuine --type evtGen

# ./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Fake --type showerScales
# ./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Fake --type highPtRadiation
# ./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Fake --type colourReconnection
# ./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Fake --type mTop
# ./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_Fake --type evtGen

./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_ --type showerScales
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_ --type highPtRadiation
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_ --type colourReconnection
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_ --type mTop
./plot_EfficiencySystTop.py -m $DIR --folder SystTopBDT_ --type evtGen
