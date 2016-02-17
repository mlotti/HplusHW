Instructions for running the limits
===================================

----------------------
The compact checklist:
----------------------
0) Setup directories containing the input multicrab directories
1) Setup input datacard
- i.e. sets all options, sources, systematics, etc.
2) Run datacard generator on the input datacard
- produces a datacard / set of datacards (text file + root file with shapes)
- produces a directory with data-driven control plots
- produces a directory with additional information
3) Optional: do tail fit
4) Optional: manipulate cards (synchronize nuisance names, etc.)
5) Move the datacard text and root files to lxplus
6) Run combine on the datacard text and root files
- produces output root files with the result
7) Run scripts to create plots and tables from the combine output
8) Done.

---------------------------------------------
The not so short details of the above points:
---------------------------------------------
0) Setting up input multicrab directories
- One needs at least the multicrab directories of the signal analysis and
  the pseudo-multicrab directory of the QCD measurement. So first generate those.
  Refer to the readme.txt files in the signal analysis and QCD measurement directories.
- Recommended prodedure:
  * create a directory below the LimitCalc/work directory
  * inside that directory, either copy or create a symbolic link to the 
    multicrab/pseudomulticrab directories (minimum: signal analysis and QCD measurement)
- There can be N such multicrab directory groupings. One can flexibly run on any number of
  them when creating the datacards (see next point).

1) Setting up input datacard
- There is a default input datacard 'dcardDefault2015Datacard.py' which should be
  used for general purpose datacard creation. Any special cases should preferably
  be written into copies of that file so that there is always one working default
  input datacard.
- The input datacard is structured in the following way:
  * Define input directory and mass point(s) to run.
    The input directory can be overridden from command line. The light and heavy mass points
    are generated into different result directories because the combine physics model is
    different for them (ttbar production of (1-mu)*(1-mu)*N_SMttbar + 2*mu*(1-mu)*N_HW vs.
    standard mu=sigma*br production). At least one mass point needs to be specified.
  * Define options.
    Most options are designated with the 'Option' prefix. Comments contain pieces of
    documentation for them. The most important options are:
    . OptionGenuineTauBackgroundSource: currently just the 'MC_FakeAndGenuineTauNotSeparated'
      selection is supported. I.e. QCD+fake bkg is data-driven and genuine tau bkg comes from MC.
      Eventually, the 'DataDriven' selection should be configured to contain the data-driven
      QCD fake bkg and the data-driven genuine tau bkg.
    . OptionIncludeSystematics: to use shape systematics (recommended), set to True (note that
      to generate the variation modules one needs to produce the multicrabs with 
      doSystematicVariations=True). Setting to False replaces the shape systematics with
      guesstimates of what those uncertainties could be, i.e. usable for fast testing.
    . OptionDoControlPlots: enable/disable generating control plots. Recommend to enable
      when running on a single mass point and to disable when producing cards for all mass points.
    . OptionCtrlPlotsAtMt: enable/disable generating control plots after all selections.
      Recommend to enable when running on a single mass point and to disable when producing
      cards for all mass points.
    . OptionCombineSingleColumnUncertainties: if in doubt, set to False. Limit calculation
      is a bit faster, if scalar uncertainties affecting just one bkg are merged as one. Yet
      it may lead to missing correlations in combinations.
    . OptionConvertFromShapeToConstantList: This is a list of nuisance ID's which are
      shape variations, but the user wishes to contract them as a scalar nuisance (i.e. remove
      shape dependence). A shape uncertainty can be converted into a scalar uncertainty
      (faster limit calculation) if the uncertainty does not significantly change as function
      of the shape. In practice, run limits with the uncertainty as shape and as a scalar. If
      there is no difference in the limit, convert it to scalar to obtain simpler and faster datacards.
    . ToleranceForMinimumRate: removes from datacards any columns (datasets) whose event rate
      for the luminosity is smaller than this number. I.e. removes columns, which have negligible
      impact on limit yet needlessly slow down the limit calculation.
    . MinimumStatUncertainty: in limit calculation it is very important to give some statistical
      uncertainty to shape bins which have zero counts or in which the stat.uncert. is below this value.
      If this is neglected, one has seen even 1.5 sigma deviation from correct results. The value is
      essentially a number describing how many pb one generated MC event corresponds to. The same number
      is used for all MC samples.
  * Define histogram (histoPath*) and counter sources (SignalRateCounter, FakeRateCounter).
  * Define observation (i.e. source for data).
  * Define the list of shape systematics common to all columns in datacard. This is changed usually
    only at the stage where new shape systematics are added or superfluous ones are removed.
  * Define datacard columns (via DataGroup objects). Here one sets the name, column number,
    and source of for the column as well as specifies which uncertainties affect it. The uncertainties
    are nuisance ID's. The combine understands, that columns with negative or zero number (landsProcess)
    are signal columns and that columns with positive number are backgrounds. The datacards
    should contain consecutive numbers, although it should be tested if combine complains about it or not.
    For historical reasons (i.e. using LandS, the prequel of combine), one needed to create an
    empty column for the number of 2 in order for the light H+ physics model to work properly; this is
    no longer necessary for combine.
  * Define nuisances, i.e. systematic uncertainties. The ID appears as the first column in the datacard.
    The recommendation is to use CMS naming conventions from page:
      https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/HiggsCombinationConventions
    If the ID of a nuisance is identical in datacards of different final states, combine treats them as
    fully correlated, hence the naming is important. The distribution is a combine keyword specifying
    the pdf of the nuisance. Usual options are log-normal (lnN), gamma (gmN), log-uniform (lnU), or
    shape-dependent log-normal (shape; the datacard generator uses still the LandS notation of shapeQ).
    For details, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit
    The function and the following parameters specify what method of obtaining the uncertainty is used.
    For each function, there is an Extractor class so it is adviced to look at python/Extractor.py for
    more details. Note that the values of most scalar uncertainties are set in
      NtupleAnalysis/python/tools/systematics.py
  * Define merging of nuisances. This option does not physically merge any values, it just tells that
    the user wishes to have these nuisance on the same row in the datacards. The need for this option
    arises from the fact that in data-driven backgrounds one sometimes needs to use a different way
    of obtaining the systematic uncertainty than for simulated backgrounds. For example, scalar
    uncertainties affecting simulated samples need to be scaled down by the purity of the sample in
    QCD measurement and anticorrelated (the uncertainty affects just the simulated samples subtracted
    from the data).
  * Define control plots. They need a title (-> output filename), a name of the histogram (source), and
    a list of details, which is a dictionary containing options supported in plots.py. Additionally,
    one can specify a range for which data values are not shown for blinding reasons (blindedRange).
    The flowPlotCaption keyword is used to signify that the integral of this histogram enters the
    SelectionFlow plot; the specified string is set as the bin label. Note that the final binning
    of the histograms is specified in NtupleAnalysis/python/tools/systematics.py 
  
2) Running datacard generator on the input datacard
- Running the datacard generator is done with
    ./dcardGenerator.py -x dcardDefault2015Datacard.py
- There are several command line parameters:
  * -l    Prints a list of available era/searchMode/optimizationMode options (datacards are created
          separately for each one of them).
  * -e    Chooses the era(s), see -l. Multiple values can be given (for example -e 0 -e 2)
  * -m    Chooses the search mode(s), see -l. Multiple values can be given (for example -m 0 -m 2)
  * -o    Chooses the optimization mode(s), see -l. Multiple values can be given (for example -o 0 -o 2)
  * -d    Chooses the input directory/ies. Multiple values can be given (for example -d test_1pr -d test_3pr)
  * --systAnalysis   Runs plotShapes.py to create plots of the syst. uncertainties as function of the shape.
  * --tailfit        Runs dcardTailFitter.py with the default tail fitter input card.
  * Various debugging options (use -h to see the options)
- Producing the datacards and control plots for one set of cards takes about 20-30 s.
- One should always check that the control plots look reasonable before proceeding to limit calculation.

3) Optional: do tail fit
- The tail fit does a parametrized fit onto the transverse mass tail for the backgrounds. Above a 
  specified mT value the original counts are replaced by the fitted spectrum and the stat. uncertainty
  of it is replaced by the uncertainty on the fit parameters. The fit parameter uncertainty is calculated
  in an orthogonal base of them (through error matrix orthogonalization), i.e. in such base one can treat
  the fit parameter uncertainties as uncorrelated.
- First edit the settings file dcardTailFitSettings.py (or make a copy of it prior to editing). The
  items, which need to be specified for each background are:
  * Name of the background, i.e. the name of that background's column in the datacards
  * Fit function (they are implemented in python/TailFitter.py)
  * Minimum and maximum values for the range over which the fit is done
  * The value above which the fitted counts (and their uncertainties) replace the original counts (and 
    their stat. uncert.) 
- In addition, general settings need to be set for:
  * The final binning (the fit is done on the finely binned histograms, i.e. the binning specified when
    running the analysis; see python/parameters/signalAnalysisParameters.py) is specified here. The last
    bin will contain also the overflow events.
  * Settings of minimum stat. uncertainty for bins with zero entries or for bins with stat.uncert. below
    this value. Separate levels can be set for signal samples and background samples. The value is
    essentially a number describing how many pb one generated MC event corresponds to.
- To perform the fits, go inside the datacard directory and run there:
    ./dcardTailFitter.py -x dcardTailFitSettings.py
- There are some further command line parameters:
  * -r   Does tail fit recursively to all subdirectories
  * --noFitUncert      No fit uncertainty
  * --doubleFitUncert  Double the fit uncertainty
  * --noSystUncert     Remove all syst. uncertainties
  * --lumiprojection --bkgxsecprojection  For projections, need to be validated before serious use
- The tail fitter generates also a number of plots:
  * Updated final shape plots on linear and log scale
  * Plots for the fit parameter uncertainties, i.e. usable for checking that the fit is reasonable.
- Note: please look carefully through the ROOT fit options and take into account the following:
  * The fit is done on histograms with values ranging over many magnitudes -> likelihood fit is
    strongly adviced (without the likelihood fit, the low value tail is usually not properly modelled
    and that's where the potential signal usually is).
  * The fit is done on histograms with weighted events counts, i.e. make sure that the fit does not
    assume sqrt(N) type errors for the uncertainties, but instead supports weighted event counts.
  
    
4) Optional: manipulate cards (synchronize nuisance names, etc.)
- Sometimes there arises the need to do some manipulation of the datacards such as changing nuisance names,
  adding/changing the minimal stat. uncertainty for zero counts, combining columns, etc. In an optimal
  situation such operations would be done at the stage where the datacards are generated, yet sometimes
  it is not feasible (especially when doing combinations with cards from another group). For such purposes,
  there is a collection of macros in python/DatacardReader.py .
- For an example of datacard manipulations, see dcardCombinationSynchronizeNuisanceNamesOnOtherDatacards.py
  which was used for synchronizing datacards from different groups for the Run I combination.

5) Move the datacard text and root files to lxplus
- First, one needs to setup CMSSW and combine. The instructions for doing that are at:
  https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicLimits
  Check the recommended CMSSW version from 
  https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit#GIT_recipe_the_only_supported_re
- You may wish to increase the number decimals in the combine output for the light H+ result; to do this, search 
  the combine code for the output part, edit, and then recompile.
- Once CMSSW has been setup and combine has been compiled, follow the instructions for continuing on an
  existing release at https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicLimits

6) Run combine on the datacard text and root files
- The logic for model-independent limits is the following:
  * needed input: datacards and their root files
  * combine runs separately on each datacard
    . First a workspace root file is created (for light H+ the special ttbar physics model is invoked).
    . Then combine is run on the workspace.
  * output: root file(s) contains the limit information (it is also printed to the screen)
  * invoke script(s) to create plots and tables of the output results
- Understanding if the datacards work properly:
  * This is tedious work and it is required to be done before the pre-approval. Instructions are provided at:
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks . In practice, if some
    nuisance has large pulls, there is most likely a bug on it. In such case some of the following might work:
    . If combine crashes, it usually tells the reason. Most likely some histogram is missing or its name or path
      has a typo (i.e. name logic in datacard is not in sync with root file naming scheme).
    . For light H+, make sure that the naming of the columns matches to what is specified in the physics model.
      The physics model is located at HiggsAnalysis/CombinedLimit/python/ChargedHiggs.py . In practice, edit
      the physics model in such a way that Combine knows which column is signal and which datacard column is 
      SM ttbar (note: if ttbar is evaluated from data, then obviously there should be no column in datacard for
      SM ttbar; in such case argumentation goes: data-driven picks the (1-BR(t->bH+))**2 value, which is
      present in nature for ttbar).
    . Check that the value of the uncertainty makes sense across the columns. Check code in doing the variation
      (i.e. python input to running of analysis and the input datacard to datacard generator).
    . If it is a shape nuisance and it is physically meaningful to convert it to a scalar nuisance, try it.
    . If nothing else works, try removing all other syst. uncertainties from the datacard (fastest to do by editing
      manually the datacard text file; not needed to edit the root file). Then run combine again. Then add back
      uncertainties one by one to the datacard and run combine after each addition to pin down what causes the
      problem.
    . Ask the experts from Higgs combination group for help. Especially check with them that the command for running
      combine is ok.
    . Check the combine options (combine --help) and try using smaller values for tolerances (may increase run times).
    . In principle, all large pulls and constraints need to be understood. Note, that having large number (>10000)
      of expected events for a background will cause constraining of any systematic uncertainty assigned to it.
      For clarity, pull means that the central value of the nuisance is moved to smaller or larger values; constraint
      means that the width of the nuisance around the central value becomes smaller. For example, if there is an
      uncertainty of +-3% on tau ES and combine constrains it by 50% with no pull on it, then the fitted uncertainty
      used in the result is +-1.5%.
  * The process is repeated separately for datacards of a single final state. For combinations, one adds one by one
    further datacards and checks incrementally for any anomalies.
- The logic for limits in a given model is the following:
  * Needed input: datacards and their root files; root files for the model-dependent parameters (xsection and BR's
    and their uncertainties). Copy the model-dependent parameter files to the directory where you launch the
    combine running script.
  * For each mass point and model, a number of tan beta points are scanned (for each of them, combine calculates
    the limit). For each point, the signal is scaled by the model's xsection and BR (original ones are kept 
    unmodified as a backup); with such approach, one can compare the obtained result always to 1.0 pb and combine
    stays numerically stable. I.e. if the calculated limit for a given point is smaller than 1.0 pb (pb is the
    unit used in combine), then the point is excluded.
  * Note that lines for the model's xsection and BR uncertainties are added to the datacards. Note that the Higgs
    Combination group insists that the xsection and BR uncertainties are treated as uncorrelated (despite
    LHCHXSWG or theorists might indicate otherwise).
  * Note that the number of calls to combine is usually very large. CRAB2 allowed to submit custom non-CMSSW tasks
    to grid, which was great for this kind of jobs. In principle one could replace CRAB2 here with submission to
    lxbatch. At the time of writing, CRAB3 does not support non-CMSSW jobs. In 2012, running combination for
    heavy H+ for 8 mass points and 6 models took about 2-3 days of CPU time.
  * The processing of the output is automatized as much as possible
    (see https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicLimits), but because combine sometimes fails,
    manual checking (and editing of non-physical values) of the output is necessary.
  * invoke script(s) to create plots and tables of the output results

7) Run scripts to create plots and tables from the combine output
- This is documented at: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicLimits
- If you are in luck (or in bug) and there is a distinct separatation between the observed and expected curves, the
  excess/deficit should be quantified, i.e. it's p-value should be calculated. Note that the usual limit plot does NOT
  give a number how many sigmas the deviation represents. Follow the instructions for "Significance and p-value" on
  the page https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronicLimits .
  