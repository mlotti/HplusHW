# Settings file for tail fitter

# Final binning for fitted shapes
finalBinning = {
    # Transverse mass, 20 GeV bins
    "shape": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700],
    #"shape": [0,20,40,60,80,100,120,140,160,200,250,300,350,400,450,500,550,600,650,700],
    #"shapeTransverseMass": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400],
    #"shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,400],
}

applyFitUncertaintyAsBinByBinUncertainty = False

# Minimum stat. uncertainty to set to bins with zero events
MinimumStatUncertaintySignal = 0.03
MinimumStatUncertaintyBkg = 0.5


fitstart = 180
fitstop = 700
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
        "id": "EWK_Tau",
        #"fitfunc": "FitFuncSimpleExp",
        #"fitfunc": "FitFuncExpTailExo",
        "fitfunc": function,
        "fitmin": fitstart, #120
        "fitmax": fitstop,
        "applyFrom": applyfrom,
    },
    # Fit settings for EWK+tt with taus from MC
    {
        "id": "genuinetau",
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
