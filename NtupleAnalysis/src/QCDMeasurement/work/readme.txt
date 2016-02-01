Instructions for running the QCD measurement:
1) Set up options in QCDMeasurementAnalysis.py
   - set the phase space splitting with: allSelections.CommonPlots.histogramSplitting
   - decide if you wish to enable or disable systematics in AnalysisBuilder
   - decide if you wish to add optimization modules (plenty more histograms means more memory usage)

2) Run the QCD measurement analysis: (2-3 h with systematics)
   ./QCDMeasurementAnalysis.py path_to_multicrabdir <1prong> <2prong> <3prong>
   - This creates a result directory with root files containing the necessary result histograms splitted
     in phase space (usually in bins of tau pt) for doing the normalization and the final result
   - The path_to_multicrabdir is mandatory
   - The prong options are optional, please select just one. It will add a corresponding 1pr/2pr/3pr
     suffix to the end of the output directory
   - The user should check that the purities in the inverted tau isolation leg are sufficient
     (i.e. sample is dominated by QCD and EWK fake tau events)
     TODO: add instruction for running purity script

3) Calculate the normalization: (<1 min.)
   ./QCDMeasurementNormalization.py path_to_QCDresultdir
   - This takes the result directory created in step (2) and calculates the normalisation coefficients
     for both QCD bkg and EWK fake taus events
   - The coefficients are stored in a python file starting with "QCDInvertedNormalizationFactors_"
   - The script also summarizes warnings and errors encountered. These are summarized in the
     plot QCDNormalisationDQM.png . Green means deviation from normal is 0..3 %, 
     yellow means deviation of 3..10 %, and red means deviation of >10 % (i.e. something is clearly wrong).
   - The summary plot for the coefficients is QCDNormalisationCoefficients.png
   - The sources for errors and warnings can be located in the produced histograms of the fits (starting
      with fit_)
   - If necessary, do adjustments to stabilize the fits to get rid of the errors and warnings. The first
     things to work with are:
       a) make sure enough events are in the various phase space bins (i.e. go back to step (2) to adjust)
       b) adjust fit parameters in QCDMeasurementNormalization.py under the comment "Define fit functions
          and fit parameters"
   - Note that a separate normalisation coefficient file is produced for the various 1pr/2pr/3pr suffixes
   - Move on only once you are pleased with the normalisation coefficients

4) Calculate the final result (i.e. produce pseudo-multicrab): (30 mins. with systematics)
   ./makeQCDInvertedPseudoMulticrabForDatacards.py --mdir path_to_QCDresultdir <--inclusiveonly> <--qcdonly>
   - This takes the result directory created in step (2) and the corresponding normalisation 
     coefficient file produced in step (3)
   - The results are stored into a directory starting with pseudoMulticrab_ (the various 1pr/2pr/3pr 
     suffixes are included in the filename)
   - The user may calculate the final result based on the phase space binning (default option) or based
     on the inclusive bin (i.e. disable phase space binning) by using the parameter --inclusiveonly
   - The user may use the normalisation coefficients for both QCD and EWK fake taus (default) or just the
     coefficient for QCD (use parameter --qcdonly; this should be used only for testing purposes)

5) Combine result from different prongs (few seconds):
   - Run steps (2), (3), and (4) for each prong selection (specify as command line parameter in step (2)
     as indicated)
   - Then combine the resulting pseudoMulticrab directories with
       hplusMergeResultDirectories.py inputPseudoMulticrab1 inputPseudoMulticrab2 <...>
   - The results are stored into the directory pseudoMulticrab_QCDMeasurement_merged_*
   - Note that since the pseudo-multicrab is data, it is already normalised to the luminosity of the data and
     consequently no normalisation information is needed in the pseudo-multicrab directories for
     the summing of orthogonally selected results (makes life easier in the combination script)

6) From QCD measurement to control plots and limits
   - To check the closure of the QCD measurement, produce the plots with:
     TODO: add instructions
   - For limit calculation and control plots, copy the pseudoMulticrab_QCDMeasurement directory
     under a collective directory, where also the signal analysis (and embedding) result directories
     reside. Then run limit calculation on that directory (see src/LimitCalc/work/readme.txt).
