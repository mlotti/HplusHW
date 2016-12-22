#!/usr/bin/env python

import HiggsAnalysis.LimitCalc.LandSTools as lands
import HiggsAnalysis.LimitCalc.CombineTools as combine
import HiggsAnalysis.LimitCalc.CommonLimitTools as commonLimitTools

lepType = False
lhcType = False
lhcTypeAsymptotic = False

massPoints = [] # auto detect
#massPoints = ["180", "190", "200","220","250","300"]
#massPoints = ["180", "190", "200","220","250","300","400","500","600"]
#massPoints = ["120"]

ntoys = {
    # njobs, ntoysCLsb, ntoysCLb
    #"default": (160, 150, 75),
    #"default": (40, 150, 75),
#    "default": (10, 150, 75),
    "default": (10, 300, 150),
    #"100":     (200, 120, 60),
    # for nominal
    #"150":     (40,  600, 300),
    #"160":     (40,  600, 300),
}
def _ntoys(index):
    ret = {}
    for key, value in ntoys.iteritems():
        ret[key] = value[index]
    return ret
def _njobs():
    return _ntoys(0)
def _ntoysCLsb():
    return _ntoys(1)
def _ntoysCLb():
    return _ntoys(2)

def main(opts, settings, myDir):
    postfix = "taujets"

#    lepType = True
#    lhcType = True
    lhcTypeAsymptotic = True

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }
    if settings.isLands():
        if opts.lepType:
            lands.generateMultiCrab(
                opts,
                myDir,
                massPoints = settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS),
                datacardPatterns = [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS)],
                rootfilePatterns = [settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)],
                clsType = lands.LEPType(opts.brlimit,opts.sigmabrlimit,toysPerJob=100,firstSeed=settings.getFirstSeed()),
                numberOfJobs = 10,
                postfix = postfix+"_lep_toys1k",
                crabScheduler=crabScheduler, crabOptions=crabOptions)
        elif opts.lhcType:
            myVR = None
            if opts.brlimit:
                if commonLimitTools.isHeavyHiggs(settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS)):
                    raise Exception("Error: --brlimit is not available for heavy H+! Please use --sigmabrlimit !")
                myVR = {"default": None,
                    # Initially obtained from asymp. limit as min/max of +-2 sigma and observed
                    # After that, with trial and error of hybrid limit (e.g. by looking plot*.gif plots)
                    # Light H+, values calibrated with 2011A, met>50, loose delta phi
                    "80":  ("0.001",  "0.08", "x1.05"), 
                    "90":  ("0.001",  "0.07", "x1.05"), 
                    "100": ("0.001", "0.06", "x1.05"), 
                    "120": ("0.0005", "0.04", "x1.05"), 
                    "140": ("0.0001", "0.03", "x1.05"), 
                    "150": ("0.0001", "0.025", "x1.03"),
                    "155": ("0.0001", "0.02", "x1.03"),
                    "160": ("0.0001", "0.02", "x1.03"), 
                }
            if opts.sigmabrlimit:
                myVR = {"default": None,
                    # Initially obtained from asymp. limit as min/max of +-2 sigma and observed
                    # After that, with trial and error of hybrid limit (e.g. by looking plot*.gif plots)
                    # Light H+, values calibrated with 2011A, met>50, loose delta phi
                    "80":  ("1",  "20", "x1.05"),
                    "90":  ("1",  "20", "x1.05"),
                    "100": ("0.5", "20", "x1.05"),
                    "120": ("0.5", "20", "x1.05"),
                    "140": ("0.5", "10", "x1.05"),
                    "150": ("0.1", "10", "x1.03"),
                    "155": ("0.1", "10", "x1.03"),
                    "160": ("0.1", "10", "x1.03"),
                    "180": ("0.01", "5", "x1.05"),
                    "190": ("0.01", "5", "x1.05"),
                    "200": ("0.01", "5", "x1.05"),
                    "220": ("0.01", "5", "x1.03"),
                    "250": ("0.01", "5", "x1.03"),
                    "300": ("0.01", "5", "x1.03"),
                    "350": ("0.01", "5", "x1.03"),
                    "400": ("0.005", "1", "x1.03"),
                    "500": ("0.005", "1", "x1.03"),
                    "600": ("0.005", "1", "x1.03"),
                }
            lands.generateMultiCrab(
                opts,
                myDir,
                massPoints = settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS),
                datacardPatterns = [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS)],
                rootfilePatterns = [settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)],
                clsType = lands.LHCType(opts.brlimit,opts.sigmabrlimit,toysCLsb=_ntoysCLsb(),toysCLb=_ntoysCLb(),firstSeed=settings.getFirstSeed(),vR=myVR),
                numberOfJobs = _njobs(),
                postfix = postfix+"_lhc_jobs160_sb150_b75",
                crabScheduler=crabScheduler, crabOptions=crabOptions)
        elif opts.lhcTypeAsymptotic:
            lands.produceLHCAsymptotic(
                opts,
                myDir,
                massPoints = settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS),
                datacardPatterns = [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS)],
                rootfilePatterns = [settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)],
                clsType = lands.LHCTypeAsymptotic(opts.brlimit,opts.sigmabrlimit),
                postfix = postfix+"_lhcasy"
                )
        else:
            return False
    elif settings.isCombine():
        if opts.lepType:
            raise Exception("LEP type Hybrid CLs not implemented yet for combine")
        elif opts.lhcType:
            raise Exception("LHC type Hybrid CLs not implemented yet for combine")
        elif opts.lhcTypeAsymptotic:
            pfix = postfix #+"_lhcasy"
            if opts.postfix != "":
                pfix += "_"+opts.postfix
            combine.produceLHCAsymptotic(
                opts,
                myDir,
                massPoints = settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS),
                datacardPatterns = [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS)],
                rootfilePatterns = [settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)],
                clsType = combine.LHCTypeAsymptotic(opts),
                postfix = pfix
                )
        else:
            return False
    return True

if __name__ == "__main__":
    parser = commonLimitTools.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    parser.add_option("--postfix", dest="postfix", default="",
                      help="Postfix to add to output directory name")
    opts = commonLimitTools.parseOptionParser(parser)
    # General settings

    myDirs = opts.dirs[:]
    if len(myDirs) == 0:
        myDirs.append(".")

    for myDir in myDirs:
        settings = commonLimitTools.GeneralSettings(myDir, opts.masspoints)
        print "The following masses are considered:",settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS)
        if not main(opts, settings, myDir):
            print ""
            parser.print_help()
            print ""
            raise Exception("You forgot to specify limit calculation method as a command line parameter!")

