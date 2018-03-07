#!/bin/csh   

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
set PSEUDO_MCRAB_DIR = ${1}

./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder PUDependency --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder counters/weighted --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder eSelection_Veto --url 
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder muSelection_Veto --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder tauSelection_Veto --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder jetSelection_ --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder bjetSelection_ --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder topbdtSelection_ --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder fatjetSelection_Veto --url
./plotDataMC_ControlPlots.py -m $PSEUDO_MCRAB_DIR --folder ForDataDrivenCtrlPlots --url

./plotTH2.py -m $PSEUDO_MCRAB_DIR --folder ForDataDrivenCtrlPlots --dataset ChargedHiggs_HplusTB_HplusToTB_M_650 --normalizeToLumi --logZ --gridX --gridY  --url
./plotTH2.py -m $PSEUDO_MCRAB_DIR --folder ForDataDrivenCtrlPlots --dataset ChargedHiggs_HplusTB_HplusToTB_M_800 --normalizeToLumi --logZ --gridX --gridY  --url
./plotTH2.py -m $PSEUDO_MCRAB_DIR --folder ForDataDrivenCtrlPlots --dataset ChargedHiggs_HplusTB_HplusToTB_M_1000 --normalizeToLumi --logZ --gridX --gridY  --url
