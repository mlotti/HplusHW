import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbeAnalysis")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )    

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    # IO parameters:
    InputFileNames = cms.vstring("histograms.root"),
#    InputFileNames = cms.vstring("Mu_147196-149294_Dec22/res/histograms-Mu_147196-149294_Dec22.root"),
#    InputFileNames = cms.vstring("Mu_146428-147116_Dec22/res/histograms-Mu_146428-147116_Dec22.root"),
    InputDirectoryName = cms.string("tnpTree"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string("tagprobe_output.root"),
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
        abseta = cms.vstring("Probe |#eta|", "0", "2.1", ""),
        
        dz = cms.vstring("Probe dz(muy, vtx)", "0", "10", "cm"),
        sumIsoRel = cms.vstring("Probe sumIso/pt", "0", "2", ""),
        pfSumIsoRel = cms.vstring("Probe pfSumIso/pt", "0", "2", ""),
    ),

    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories = cms.PSet(
#        mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
        isTrackerMuon = cms.vstring("Tracker muon", "dummy[pass=1,fail=0]"),
        isGlobalMuon = cms.vstring("Global muon", "dummy[pass=1,fail=0]"),
        isHLTMu9 = cms.vstring("HLT_Mu9", "dummy[pass=1,fail=0]"),
        isHLTMu15 = cms.vstring("HLT_Mu15", "dummy[pass=1,fail=0]"), 
        isHLTMu20 = cms.vstring("HLT_Mu20", "dummy[pass=1,fail=0]"),
        hitQuality = cms.vstring("Hit quality", "dummy[pass=1,fail=0]"),
        dB = cms.vstring("IPxy,z", "dummy[pass=1,fail=0]"),
        sumIsoRel10 = cms.vstring("Rel sum iso < 0.1", "dummy[pass=1,fail=0]"),
        sumIsoRel15 = cms.vstring("Rel sum iso < 0.15", "dummy[pass=1,fail=0]"),
        pfSumIsoRel10 = cms.vstring("PF rel sum iso < 0.1", "dummy[pass=1,fail=0]"),
        pfSumIsoRel15 = cms.vstring("PF rel sum iso < 0.15", "dummy[pass=1,fail=0]"),
        tauIsoVLoose = cms.vstring("Tau Iso VLoose", "dummy[pass=1,fail=0]"),
        fullSelection = cms.vstring("Full selection", "dummy[pass=1,fail=0]"),
    ),
    Cuts = cms.PSet(
        dz1cm = cms.vstring("dz(mu, vtx) < 1", "dz", "1.0"),
        sumIsoRel50 = cms.vstring("Rel sum iso < 0.5", "sumIsoRel", "0.5"),
        pfSumIsoRel50 = cms.vstring("Rel sum iso < 0.5", "pfSumIsoRel", "0.5"),
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
                "isHLTMu9", "pass",
                "hitQuality", "pass",
                "dB", "pass",
#                "sumIsoRel10", "pass",
                "tauIsoVLoose", "pass",
                "dz1cm", "below",
#                "fullSelection", "pass",
            ),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = cms.PSet(
                pt = cms.vdouble(0, 1000),
            ),
            #BinToPDFmap = cms.vstring("gaussPlusLinear")
            BinToPDFmap = cms.vstring("gaussPlusQuadratic")
            #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
        ),
        # All_pt = cms.PSet(
        #     EfficiencyCategoryAndState = cms.vstring(
        #         "fullSelection", "pass"
        #     ),
        #     UnbinnedVariables = cms.vstring("mass"),
        #     BinnedVariables = cms.PSet(
        #         pt = cms.vdouble(range(30, 410, 10)),
        #     ),
        #     #BinToPDFmap = cms.vstring("gaussPlusLinear")
        #     BinToPDFmap = cms.vstring("gaussPlusQuadratic")
        #     #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
        # ),
        # All_abseta = cms.PSet(
        #     EfficiencyCategoryAndState = cms.vstring(
        #         "fullSelection", "pass"
        #     ),
        #     UnbinnedVariables = cms.vstring("mass"),
        #     BinnedVariables = cms.PSet(
        #         abseta = cms.vdouble([x*0.21 for x in range(0, 11)]), # 0.21 stepping [0, 2.1]
        #     ),
        #     #BinToPDFmap = cms.vstring("gaussPlusLinear")
        #     BinToPDFmap = cms.vstring("gaussPlusQuadratic")
        #     #BinToPDFmap = cms.vstring("gaussPlusLinear", "*pt_bin0*", "gaussPlusQuadratic")
        # ),
    )
)
# process.TagProbeFitTreeAnalyzer.Efficiencies.All_pt = process.TagProbeFitTreeAnalyzer.Efficiencies.All.clone(
#     BinnedVariables = cms.PSet(
#         pt = cms.vdouble(range(30, 410, 10)),
#     ),
# )
# process.TagProbeFitTreeAnalyzer.Efficiencies.All_abseta = process.TagProbeFitTreeAnalyzer.Efficiencies.All.clone(
#     BinnedVariables = cms.PSet(
#         abseta = cms.vdouble([x*0.21 for x in range(0, 11)]), # 0.21 stepping [0, 2.1]
#     ),
# )


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
