'''
DESCRIPTION:
Settings file for tail fitter, as implemented in dcardTailFitter.py and ../python/TailFitter.py

USAGE:
dcardTailFitter.py -x dcardTailFitSettings.py -d <path-to-datacard-directory>
'''

#================================================================================================  
# Define final binning of the fitted shape histograms
#================================================================================================  

#max_bin=2000
#bin_width=20
#list_length=max_bin/bin_width

finalBinning = {
    # Rebinning defined in systematics.py, used without tail fit
    # "shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,800,10000], #aggressive rebinning to get rid of empty bins
    # Transverse mass, 20 GeV bins, 50 GeV bins up to 1000, after that standard binning
    "shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,10000]
    # Another convenient way to define binning, using max_bin and bin_width variebles defined above:
    #"shape": [x*bin_width for x in range(list_length+1)]
}

#================================================================================================  
# Choose the strategy for handling uncertainties
#================================================================================================  

# Set to True if you want to yse stat. uncertainties as fitted rates instead of fit uncertainties
applyFitUncertaintyAsBinByBinUncertainty = False

# Minimum stat. uncertainty to set to bins with zero events
# NB! Empty bins should be avoided in the first place!
MinimumStatUncertaintySignal = 0.03
MinimumStatUncertaintyBkg = 0.5
# FIXME: Implement automatic determination of stat. uncertainties also in the tail fitter!

#================================================================================================  
# Define fit settings for each dataset
#================================================================================================  

# Settings common to all datasets (can be overwritten below for each dataset)
fitstart = 180
fitstop = 800
applyfrom = fitstart
function = "FitFuncExpTailExoAlternate" # SF*Aexp(-Bx) starting from fitmin

# Dataset-specific settings
fitSettings = [
    # Fit settings for ttbar
    {
        "id": "ttbar_CMS_Hptntj",
        "fitfunc": function,
        "fitmin": 200,
        "fitmax": fitstop,
        "applyFrom": 200,
    },
    # Fit settings for single top
    {
        "id": "CMS_Hptntj_singleTop",
        "fitfunc": function,
        "fitmin": 180, 
        "fitmax": fitstop,
        "applyFrom": 180,
    },
    # Fit settings for WJets 
    # NB! Should be taken from WJetsHT for sufficient statistics
    {
        "id": "CMS_Hptntj_W",
        "fitfunc": function,
        "fitmin": 160, 
        "fitmax": fitstop,
        "applyFrom": 160,
    },
    # Fit settings for DY
    {
        "id": "CMS_Hptntj_DY",
        "fitfunc": function,
        "fitmin": 60, 
        "fitmax": fitstop,
        "applyFrom": 60,
    },
    # Fit settings for VV
    {
        "id": "CMS_Hptntj_VV",
        "fitfunc": function,
        "fitmin": 160, 
        "fitmax": fitstop,
        "applyFrom": 160,
    },
    # Fit settings for fake taus
    {
        "id": "CMS_Hptntj_QCDandFakeTau",
        "fitfunc": function,
        "fitmin": 160, 
        "fitmax": fitstop,
        "applyFrom": 160,
    }
]

# List of backgrounds, for which no fit is done
Blacklist = []
