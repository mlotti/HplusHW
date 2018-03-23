# Settings file for tail fitter

# Final binning for fitted shapes
#max_bin=2000
#bin_width=20
#list_length=max_bin/bin_width

finalBinning = {
    # Transverse mass, 20 GeV bins (old)
    #"shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700]
    # Transverse mass, 20 GeV bins for range of 0-1600 GeV:
    #"shape": [x*bin_width for x in range(list_length+1)]
    #"shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000,1500,2000,5000],
    "shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000,1500,2000,3000,4000,5000]
}

applyFitUncertaintyAsBinByBinUncertainty = False

# Minimum stat. uncertainty to set to bins with zero events
MinimumStatUncertaintySignal = 0.03
MinimumStatUncertaintyBkg = 0.5


fitstart = 180
fitstop = 5000
applyfrom = fitstart
function = "FitFuncExpTailExoAlternate"
#function = "FitFuncExpTailTauTauAlternate"

fitSettings = [
    # Fit settings for ttbar
    {
#        "id": "CMS_Hptntj_ttbar_t_genuine",
        "id": "ttbar_t_genuine",
        "fitfunc": function,
        "fitmin": fitstart,
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    },
    # Fit settings for single top
    {
#        "id": "CMS_Hptntj_singleTop_t_genuine",
        "id": "singleTop_t_genuine",
        "fitfunc": function,
        "fitmin": fitstart, 
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    },
    # Fit settings for fake taus
    {
#        "id": "CMS_Hptntj_QCDandFakeTau",
        "id": "QCDandFakeTau",
        #"fitfunc": "FitFuncSimpleExp",
        #"fitfunc": "FitFuncExpTailExo",
        "fitfunc": function,
        "fitmin": fitstart, 
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    }
]

# List of backgrounds, for which no fit is done
Blacklist = [
#    "CMS_Hptntj_W_t_genuine","CMS_Hptntj_DY_t_genuine","CMS_Hptntj_VV_t_genuine", #FIXME: temporarily blacklisted to get rid of errors
    "W_t_genuine","DY_t_genuine","VV_t_genuine", #FIXME: temporarily blacklisted to get rid of errors

]
