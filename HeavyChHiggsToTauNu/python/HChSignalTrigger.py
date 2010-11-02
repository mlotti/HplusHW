def getSignalTrigger(dataVersion):
    if dataVersion.isData():
        if dataVersion.isRun2010A():
            #return "HLT_SingleLooseIsoTau20" # prescaled
            return "HLT_SingleIsoTau20_Trk5" # not prescaled
        elif dataVersion.isRun2010B():
            return "HLT_SingleIsoTau20_Trk15_MET20"
        else:
            raise Exception("Unsupported data version!")
    else:
        if dataVersion.is38X():
            return "HLT_SingleIsoTau20_Trk15_MET20"
        else:
            return "HLT_SingleLooseIsoTau20" # only tau trigger available in 36X MC
