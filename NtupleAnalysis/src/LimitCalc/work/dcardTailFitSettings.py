# Settings file for tail fitter

# Final binning for fitted shapes
max_bin=2000
bin_width=20
list_length=max_bin/bin_width

finalBinning = {
    # Transverse mass, 20 GeV bins (old)
    #"shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700]
    # Transverse mass, 20 GeV bins for range of 0-1600 GeV:
    #"shape": [x*bin_width for x in range(list_length+1)]
    "shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800],
    #"shape": [0,20,40,60,80,100,120,140,160,200,250,300,350,400,450,500,550,600,650,700],
    #"shapeTransverseMass": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400],
    #"shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,400],
}

applyFitUncertaintyAsBinByBinUncertainty = False

# Minimum stat. uncertainty to set to bins with zero events
MinimumStatUncertaintySignal = 0.03
MinimumStatUncertaintyBkg = 0.5


fitstart = 180
<<<<<<< HEAD
fitstop = 4000 # extended, used to be 700
=======
fitstop = 2000 # extended, used to be 700
>>>>>>> public/master
applyfrom = fitstart
function = "FitFuncExpTailExoAlternate"
#function = "FitFuncExpTailTauTauAlternate"

fitSettings = [
    # Fit settings for QCD
    {
        "id": "QCD",
        #"fitfunc": "FitFuncExpTailFourParamAlternate",
        "fitfunc": function,
        "fitmin": fitstart, #140
        "fitmax": fitstop,
        "applyFrom": applyfrom, # 160
    },
    # Fit settings for EWK+tt with taus from data
    {
        "id": "CMS_Hptntj_EWK_t_genuine",
        #"fitfunc": "FitFuncSimpleExp",
        #"fitfunc": "FitFuncExpTailExo",
        "fitfunc": function,
        "fitmin": fitstart, #120
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    },
    # Fit settings for EWK+tt with taus from MC
    {
        "id": "CMS_Hptntj_ttbar_and_singleTop_t_genuine",
        "fitfunc": function,
        "fitmin": fitstart, # 140
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    },
    # Fit settings for EWK+tt with fake taus
    {
        "id": "MC_faketau",
        #"fitfunc": "FitFuncSimpleExp",
        #"fitfunc": "FitFuncExpTailExo",
        "fitfunc": function,
        "fitmin": fitstart, # 140
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    }
]

# List of backgrounds, for which no fit is done
Blacklist = [
#    "CMS_Hptntj_DY_genuinetau","DY_genuinetau", #blacklisted because contribution from DY is ~zero above mT=180 GeV (=fitstart=applyfrom)
#    "CMS_Hptntj_W_genuinetau","W_genuinetau", #FIXME: temporarily blacklisted to get rid of errors
]
