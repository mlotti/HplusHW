import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register("trigger", "isHLTMu20",
                 options.multiplicity.singleton, options.varType.string,
                 "Trigger to consider")
options.register("mc", 0,
                 options.multiplicity.singleton, options.varType.int,
                 "Use MC=")
options.parseArguments

process = cms.Process("TagProbeAnalysis")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )    

trigger = options.trigger
#trigger = "isHLTMu20"
#trigger = "isHLTMu24"
#trigger = "isHLTMu30"
#trigger = "isHLTMu40"
#trigger = "isHLTMu40eta2p1"

def result(task):
    return "%s/res/histograms-%s.root" % (task, task)

(input, output) = (None, None)
if options.mc:
    input = result("DYJetsToLL_M50_TuneZ2_Summer11")
    output = "DY_Mu20"
    trigger = "isHLTMu20"
else:
    (input, output) = {
        "isHLTMu20": ([result("SingleMu_160431-163261_May10")], "Run2011A_Mu20"),
        "isHLTMu24": ([result("SingleMu_163270-163869_May10")], "Run2011A_Mu24"),
        "isHLTMu30": ([result("SingleMu_165088-165633_Prompt"), result("SingleMu_165970-166150_Prompt")], "Run2011A_Mu30"),
        "isHLTMu40": ([result("SingleMu_166161-166164_Promp"), result("SingleMu_166346-166346_Prompt"), result("SingleMu_166374-166967_Prompt"), result("SingleMu_167039-167043_Prompt"), result("SingleMu_167078-167913_Prompt"), result("SingleMu_172620-173198_Prompt")], "Run2011A_Mu40"),
        "isHLTMu40eta2p1": ([result("SingleMu_173236-173692_Prompt")], "Run2011A_Mu40eta2p1")
        }[trigger]

output = "tagprobe_output_%s.root" % output

#input = cms.vstring("histograms.root")
#output = "tagprobe_output.root"


process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer(
    "TagProbeFitTreeAnalyzer",
    # IO parameters:
    InputFileNames = cms.vstring(input),
    InputDirectoryName = cms.string("tnpTree"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string(output),
    #numbrer of CPUs to use for fitting
    NumCPU = cms.uint32(1),
    # specifies wether to save the RooWorkspace containing the data for each bin and
    # the pdf object with the initial and final state snapshots
    SaveWorkspace = cms.bool(True),

#    floatShapeParameters = cms.bool(True),

    # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
    Variables = cms.PSet(
#        mass = cms.vstring("Tag-Probe Mass", "60", "120", "GeV/c^{2}"),
        mass = cms.vstring("Tag-Probe Mass", "40", "140", "GeV/c^{2}"),
        pt = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
#        eta = cms.vstring("Probe #eta", "-2.1", "2.1", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.2", ""),
        
#        dz = cms.vstring("Probe dz(muy, vtx)", "0", "10", "cm"),
        sumIsoRel = cms.vstring("Probe sumIso/pt", "0", "2", ""),
        pfSumIsoRel = cms.vstring("Probe pfSumIso/pt", "0", "2", ""),
        tauTightIc04Iso = cms.vstring("Probe counting iso occupancy", "0", "100", "")
    ),

    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories = cms.PSet(
#        mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
        isTrackerMuon = cms.vstring("Tracker muon", "dummy[pass=1,fail=0]"),
        isGlobalMuon = cms.vstring("Global muon", "dummy[pass=1,fail=0]"),
        isHLTMu9 = cms.vstring("HLT_Mu9", "dummy[pass=1,fail=0]"),
        isHLTMu15 = cms.vstring("HLT_Mu15", "dummy[pass=1,fail=0]"), 
        isHLTMu20 = cms.vstring("HLT_Mu20", "dummy[pass=1,fail=0]"),
        isHLTMu24 = cms.vstring("HLT_Mu24", "dummy[pass=1,fail=0]"),
        isHLTMu30 = cms.vstring("HLT_Mu30", "dummy[pass=1,fail=0]"),
        isHLTMu40 = cms.vstring("HLT_Mu40", "dummy[pass=1,fail=0]"),
        hitQuality = cms.vstring("Hit quality", "dummy[pass=1,fail=0]"),
        dB = cms.vstring("IPxy,z", "dummy[pass=1,fail=0]"),
#        sumIsoRel10 = cms.vstring("Rel sum iso < 0.1", "dummy[pass=1,fail=0]"),
#        sumIsoRel15 = cms.vstring("Rel sum iso < 0.15", "dummy[pass=1,fail=0]"),
#        pfSumIsoRel10 = cms.vstring("PF rel sum iso < 0.1", "dummy[pass=1,fail=0]"),
#        pfSumIsoRel15 = cms.vstring("PF rel sum iso < 0.15", "dummy[pass=1,fail=0]"),
#        tauIsoVLoose = cms.vstring("Tau Iso VLoose", "dummy[pass=1,fail=0]"),
        fullSelection = cms.vstring("Full selection", "dummy[pass=1,fail=0]"),
    ),
    Cuts = cms.PSet(
         countIso = cms.vstring("Counting iso", "tauTightIc04Iso", "1.0"), 
#        dz1cm = cms.vstring("dz(mu, vtx) < 1", "dz", "1.0"),
        sumIsoRel10 = cms.vstring("Rel sum iso < 0.1", "sumIsoRel", "0.1"),
        pfSumIsoRel10 = cms.vstring("Rel sum iso < 0.1", "pfSumIsoRel", "0.1"),
    ),

    # defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
    # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values  
    PDFs = cms.PSet(
        gaussPlusLinear = cms.vstring(
#            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
            "Gaussian::signal(mass, mean[91.2, 89.0, 93.0], sigma[2.3, 0.5, 10.0])",
#            "Exponential::backgroundPass(mass, lp[0,-5,5])",
#            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "Chebychev::backgroundPass(mass, cPass[0,-10,10])",
            "Chebychev::backgroundFail(mass, cFail[0,-10,10])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        gaussPlusQuadratic = cms.vstring(
#            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
            "Gaussian::signal(mass, mean[91.2, 89.0, 93.0], sigma[2.3, 0.5, 10.0])",
            "Chebychev::backgroundPass(mass, {cPass1[0,-1,1], cPass2[0,-1,1]})",
            "Chebychev::backgroundFail(mass, {cFail1[0,-1,1], cFail2[0,-1,1]})",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),

    # defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
    # there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting. 
    Efficiencies = cms.PSet(
        All = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring(
                 "isTrackerMuon", "pass",
                 "isGlobalMuon", "pass",
                 trigger, "pass",
                 "hitQuality", "pass",
                 "dB", "pass",
#                "countIso", "below",
#                "sumIsoRel10", "pass",
#                "tauIsoVLoose", "pass",
#                "dz1cm", "below",
#                "fullSelection", "pass",
            ),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = cms.PSet(
                pt = cms.vdouble(40, 1000),
                abseta = cms.vdouble(0, 2.1),
#                pt = cms.vdouble(0, 20, 40, 45, 50, 60, 70, 80, 90, 100, 1000),
            ),
            #BinToPDFmap = cms.vstring("gaussPlusLinear")
#            BinToPDFmap = cms.vstring("gaussPlusQuadratic")
            #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
        ),
#         AllStdIso = cms.PSet(
#             EfficiencyCategoryAndState = cms.vstring(
#                  "isTrackerMuon", "pass",
#                  "isGlobalMuon", "pass",
#                  trigger, "pass",
#                  "hitQuality", "pass",
#                  "dB", "pass",
#                  "sumIsoRel10", "below",
#             ),
#             UnbinnedVariables = cms.vstring("mass"),
#             BinnedVariables = cms.PSet(
#                 pt = cms.vdouble(0, 1000),
#             ),
#             #BinToPDFmap = cms.vstring("gaussPlusLinear")
#             BinToPDFmap = cms.vstring("gaussPlusQuadratic")
#             #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
#         ),
#         Iso = cms.PSet(
#             EfficiencyCategoryAndState = cms.vstring(
#                 "countIso", "below",
#             ),
#             UnbinnedVariables = cms.vstring("mass"),
#             BinnedVariables = cms.PSet(
#                 isTrackerMuon = cms.vstring("pass"),
#                 isGlobalMuon = cms.vstring("pass"),
#                 hitQuality = cms.vstring("pass"),
#                 dB = cms.vstring("pass"),
#                 pt = cms.vdouble(0, 1000),
#             ),
#             #BinToPDFmap = cms.vstring("gaussPlusLinear")
#             BinToPDFmap = cms.vstring("gaussPlusQuadratic")
#             #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
#         ),
        Trigger = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring(
                trigger, "pass",
            ),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = cms.PSet(
                isTrackerMuon = cms.vstring("pass"),
                isGlobalMuon = cms.vstring("pass"),
                hitQuality = cms.vstring("pass"), 
                tauTightIc04Iso = cms.vdouble(0, 0.1),
                dB = cms.vstring("pass"),
                pt = cms.vdouble(40, 1000),
                abseta = cms.vdouble(0, 2.1),
#                pt = cms.vdouble(40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 55, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1000)
            ),
            #BinToPDFmap = cms.vstring("gaussPlusLinear")
#            BinToPDFmap = cms.vstring("gaussPlusQuadratic")
            #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
        ),
    )
)
#setattr(process.TagProbeFitTreeAnalyzer.Efficiencies.Iso.BinnedVariables, trigger, cms.vstring("pass"))
#ptbins = range(30, 410, 10)
#etabins = [x*0.21 for x in range(0, 11)] # 0.21 stepping [0, 2.1]
#ptbins = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54, 56, 58, 60, 65, 70, 80, 90, 100]
etabins = [x*0.1 for x in range(0, 23)] # 0.1 stepping [0, 2.2]
ptbins = [30, 34, 38, 39, 40, 41, 42, 44, 48, 50, 54, 58, 62, 66, 70, 80, 90, 100]
if "Mu20" in trigger:
    ptbins += [150, 200, 400, 600, 1000]
elif "Mu24" in trigger:
    ptbins += [125, 150, 200, 300, 400, 600, 1000]
elif "Mu30" in trigger or "Mu40" in trigger:
    ptbins += [125, 150, 200, 250, 300, 400, 500, 600, 800, 1000]
print "pT bins", ptbins
print "eta bins", etabins

process.TagProbeFitTreeAnalyzer.Efficiencies.All_pt = process.TagProbeFitTreeAnalyzer.Efficiencies.All.clone(
    BinnedVariables = cms.PSet(
        pt = cms.vdouble(ptbins),
        abseta = cms.vdouble(0, 2.1),
    ),
)
process.TagProbeFitTreeAnalyzer.Efficiencies.Trigger.BinnedVariables.pt = ptbins
process.TagProbeFitTreeAnalyzer.Efficiencies.All_abseta = process.TagProbeFitTreeAnalyzer.Efficiencies.All.clone(
    BinnedVariables = cms.PSet(
        pt = cms.vdouble(40, 1000),
        abseta = cms.vdouble(etabins),
    ),
)
process.TagProbeFitTreeAnalyzer.Efficiencies.All_pt_abseta = process.TagProbeFitTreeAnalyzer.Efficiencies.All.clone(
    BinnedVariables = cms.PSet(
        pt = cms.vdouble(ptbins),
        abseta = cms.vdouble(etabins),
    ),
)



#         All_eta = cms.PSet(
#             EfficiencyCategoryAndState = cms.vstring(
#                 "fullSelection", "pass"
#             ),
#             UnbinnedVariables = cms.vstring("mass"),
#             BinnedVariables = cms.PSet(
#                 eta = cms.vdouble([x*0.21-2.1 for x in range(0, 21)]), # 0.21 stepping [-2.1, 2.1]
#             ),
#             #BinToPDFmap = cms.vstring("gaussPlusLinear")
#             BinToPDFmap = cms.vstring("gaussPlusQuadratic")
#             #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
#         ),
#         All_pt_abseta = cms.PSet(
#             EfficiencyCategoryAndState = cms.vstring(
# #                "Trigger15", "true"
# #                "Global", "true",
# #                "HitQuality", "true",
# #                "IP", "true",
# #                "Isolation", "true",
#                 "FullSelection", "true"
#             ),
#             UnbinnedVariables = cms.vstring("mass"),
#             BinnedVariables = cms.PSet(
# #                pt = cms.vdouble(25.0, 50.0, 75.0, 100.0, 125.0),
#                 pt = cms.vdouble(range(30, 130, 10)),
#                 abseta = cms.vdouble(0.0, 0.525, 1.05, 1.575, 2.1),
#             ),
#             BinToPDFmap = cms.vstring("gaussPlusQuadratic")
#             #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
#          ),

#        #the name of the parameter set becomes the name of the directory
#        Glb_pt_abseta = cms.PSet(
#            #specifies the efficiency of which category and state to measure 
#            EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#            #specifies what unbinned variables to include in the dataset, the mass is needed for the fit
#            UnbinnedVariables = cms.vstring("mass"),
#            #specifies the binning of parameters
#            BinnedVariables = cms.PSet(
#                pt = cms.vdouble(25.0, 50.0, 100.0),
#                abseta = cms.vdouble(0.0, 1.2, 2.4),
#            ),
#            #first string is the default followed by binRegExp - PDFname pairs
#            BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
#        ),
#        Glb_pt_abseta_mcTrue = cms.PSet(
#            EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#            UnbinnedVariables = cms.vstring("mass"),
#            BinnedVariables = cms.PSet(
#                mcTrue = cms.vstring("true"),
#                pt = cms.vdouble(3.0, 6.0, 20.0),
#                abseta = cms.vdouble(0.0, 1.2, 2.4),
#            )
#            #unspecified binToPDFmap means no fitting
#        ),
#        Glb_pt = cms.PSet(
#            EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#            UnbinnedVariables = cms.vstring("mass"),
#            BinnedVariables = cms.PSet(
#                pt = cms.vdouble(25.0, 50.0, 100.0),
#            ),
#            BinToPDFmap = cms.vstring("gaussPlusLinear")
#        ),
#        Glb_pt_mcTrue = cms.PSet(
#            EfficiencyCategoryAndState = cms.vstring("Glb","true"),
#            UnbinnedVariables = cms.vstring("mass"),
#            BinnedVariables = cms.PSet(
#                mcTrue = cms.vstring("true"),
#                pt = cms.vdouble(3.0, 6.0, 20.0),
#            )
#        ),
#    )
#)

process.fitness = cms.Path(
    process.TagProbeFitTreeAnalyzer
)
