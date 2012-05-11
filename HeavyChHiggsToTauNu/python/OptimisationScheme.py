import FWCore.ParameterSet.Config as cms
import sys
import ctypes

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis

## Class for generating variations to the analysis for optimisation
class HPlusOptimisationScheme():
    ## Constructor
    def __init__(self):
        # initialise internal variables
        self._tauPtVariation = []
        self._tauIsolationVariation = []
        self._tauIsolationContinuousVariation = []
        self._rtauVariation = []
        self._jetNumberVariation = []
        self._jetEtVariation = []
        self._jetBetaVariation = []
        self._METSelectionVariation = []
        self._bjetDiscriminatorVariation = []
        self._bjetEtVariation = []
        self._bjetNumberVariation = []
        self._deltaPhiVariation = []
        self._topRecoVatiation = []
        self._maxVariations = 200

    def disableMaxVariations(self):
        self._maxVariations = -1

    def addTauPtVariation(self, value):
        if isinstance(value, list):
            self._tauPtVariation.extend(value)
        else:
            self._tauPtVariation.append(value)

    def addTauIsolationVariation(self, value):
        if isinstance(value, list):
            self._tauIsolationVariation.extend(value)
        else:
            self._tauIsolationVariation.append(value)

    def addTauIsolationContinuousVariation(self, value):
        if isinstance(value, list):
            self._tauIsolationContinuousVariation.extend(value)
        else:
            self._tauIsolationContinuousVariation.append(value)

    def addRtauVariation(self, value):
        if isinstance(value, list):
            self._rtauVariation.extend(value)
        else:
            self._rtauVariation.append(value)

    def addJetNumberSelectionVariation(self, value):
        if isinstance(value, list):
            self._jetNumberVariation.extend(value)
        else:
            self._jetNumberVariation.append(value)

    def addJetEtVariation(self, value):
        if isinstance(value, list):
            self._jetEtVariation.extend(value)
        else:
            self._jetEtVariation.append(value)

    def addJetBetaVariation(self, value):
        if isinstance(value, list):
            self._jetBetaVariation.extend(value)
        else:
            self._jetBetaVariation.append(value)

    def addMETSelectionVariation(self, value):
        if isinstance(value, list):
            self._METSelectionVariation.extend(value)
        else:
            self._METSelectionVariation.append(value)

    def addBJetDiscriminatorVariation(self, value):
        if isinstance(value, list):
            self._bjetDiscriminatorVariation.extend(value)
        else:
            self._bjetDiscriminatorVariation.append(value)

    def addBJetEtVariation(self, value):
        if isinstance(value, list):
            self._bjetEtVariation.extend(value)
        else:
            self._bjetEtVariation.append(value)

    def addBJetNumberVariation(self, value):
        if isinstance(value, list):
            self._bjetNumberVariation.extend(value)
        else:
            self._bjetNumberVariation.append(value)

    def addDeltaPhiVariation(self, value):
        if isinstance(value, list):
            self._deltaPhiVariation.extend(value)
        else:
            self._deltaPhiVariation.append(value)

    def addTopRecoVariation(self, value):
        if isinstance(value, list):
            self._topRecoVatiation.extend(value)
        else:
            self._topRecoVatiation.append(value)

    def _dealWithEmptyVariations(self, nominalAnalysis):
        if len(self._tauPtVariation) == 0:
            self._tauPtVariation.append(nominalAnalysis.tauSelection.ptCut.value())
        if len(self._tauIsolationVariation) == 0:
            self._tauIsolationVariation.append(nominalAnalysis.tauSelection.isolationDiscriminator.value())
        if len(self._tauIsolationContinuousVariation) == 0:
            self._tauIsolationContinuousVariation.append(nominalAnalysis.tauSelection.isolationDiscriminatorContinuousCutPoint.value())
        if len(self._rtauVariation) == 0:
            self._rtauVariation.append(nominalAnalysis.tauSelection.rtauCut.value())
        if len(self._jetEtVariation) == 0:
            self._jetEtVariation.append(nominalAnalysis.jetSelection.ptCut.value())
        if len(self._jetNumberVariation) == 0:
            self._jetNumberVariation.append("%s%d"%(nominalAnalysis.jetSelection.jetNumberCutDirection.value(),nominalAnalysis.jetSelection.jetNumber.value()))
        if len(self._jetBetaVariation) == 0:
            self._jetBetaVariation.append("%s%.1f"%(nominalAnalysis.jetSelection.betaCutDirection.value(),nominalAnalysis.jetSelection.betaCut.value()))
        if len(self._METSelectionVariation) == 0:
            self._METSelectionVariation.append(nominalAnalysis.MET.METCut.value())
        if len(self._bjetDiscriminatorVariation) == 0:
            self._bjetDiscriminatorVariation.append(nominalAnalysis.bTagging.discriminatorCut.value())
        if len(self._bjetEtVariation) == 0:
            self._bjetEtVariation.append(nominalAnalysis.bTagging.ptCut.value())
        if len(self._bjetNumberVariation) == 0:
            self._bjetNumberVariation.append("%s%d"%(nominalAnalysis.bTagging.jetNumberCutDirection.value(),nominalAnalysis.bTagging.jetNumber.value()))
        if len(self._deltaPhiVariation) == 0:
            self._deltaPhiVariation.append(nominalAnalysis.deltaPhiTauMET.value())
        if len(self._topRecoVatiation) == 0:
            self._topRecoVatiation.append("None") # FIXME

    def printOptimisationConfig(self):
        print "Optimisation configuration:"
        print "  tau pT",self._tauPtVariation
        print "  tau isolation",self._tauIsolationVariation
        print "  tau cont. isolation discr. values",self._tauIsolationContinuousVariation
        print "  rtau",self._rtauVariation
        print "  jet ET",self._jetEtVariation
        print "  jet number",self._jetNumberVariation
        print "  jet beta cut",self._jetBetaVariation
        print "  MET",self._METSelectionVariation
        print "  btag disriminator values",self._bjetDiscriminatorVariation
        print "  btag ET",self._bjetEtVariation
        print "  btag number",self._bjetNumberVariation
        print "  delta phi (tau,MET) cut",self._deltaPhiVariation
        print "  top mass reco",self._topRecoVatiation

    def getOperatorFromCutWithDirection(self, variation):
        myValidOperators = ["GT","GEQ","NEQ","EQ","LT","LEQ"]
        myRange = 2
        if variation[2] == 'Q':
            myRange = 3
        myOperator = variation[:myRange]
        if myOperator not in myValidOperators:
            raise Exception("Error: valid operators for cut direction are ",myValidOperators)
        return myOperator

    def getNumberFromCutWithDirection(self, variation):
        myRange = 2
        if variation[2] == 'Q':
            myRange = 3
        myNumber = float(variation[myRange:])
        return myNumber

    def generateVariations(self, process, additionalCounters, commonSequence, nominalAnalysis):
        # if no variations were supplied, take the default value
        self._dealWithEmptyVariations(nominalAnalysis)
        # Print info
        self.printOptimisationConfig()
        # loop over variations
        nVariations = 0
        for taupt in self._tauPtVariation:
            for tauIsol in self._tauIsolationVariation:
                for tauIsolCont in self._tauIsolationContinuousVariation:
                    for rtau in self._rtauVariation:
                        for jetEt in self._jetEtVariation:
                            for jetNumber in self._jetNumberVariation:
                                for jetBeta in self._jetBetaVariation:
                                    for met in self._METSelectionVariation:
                                        for bjetDiscr in self._bjetDiscriminatorVariation:
                                            for bjetEt in self._bjetEtVariation:
                                                for bjetNumber in self._bjetNumberVariation:
                                                    for dphi in self._deltaPhiVariation:
                                                        for topreco in self._topRecoVatiation:
                                                            # make sanity checks
                                                            if bjetEt >= jetEt:
                                                                  nVariations += 1
                                                                  # Construct name for variation
                                                                  myVariationName = "var"
                                                                  myVariationName += "_taupt%.0f"%taupt
                                                                  myVariationName += "_%s"%tauIsol
                                                                  if tauIsolCont > 0:
                                                                      myVariationName += "%.1f"%tauIsolCont
                                                                  myVariationName += "_rtau%.1f"%rtau
                                                                  myVariationName += "_jet%s"%jetNumber
                                                                  myVariationName += "_Et%.0f"%jetEt
                                                                  myVariationName += "_Beta%s"%jetBeta
                                                                  myVariationName += "_met%.0f"%met
                                                                  myVariationName += "_bjet%s"%bjetNumber
                                                                  myVariationName += "_Et%.0f_discr%.1f"%(bjetEt,bjetDiscr)
                                                                  myVariationName += "_dphi%.0f"%dphi
                                                                  myVariationName += "_topreco"+topreco
                                                                  myVariationName = myVariationName.replace(".","") # remove dots from name since they are forbidden
                                                                  #print "Generating variation",myVariationName
                                                                  # Clone module and make changes
                                                                  myModule = nominalAnalysis.clone()
                                                                  myModule.tauSelection.ptCut = taupt
                                                                  myModule.tauSelection.isolationDiscriminator = tauIsol
                                                                  myModule.tauSelection.isolationDiscriminatorContinuousCutPoint = tauIsolCont
                                                                  myModule.tauSelection.rtauCut = rtau
                                                                  myModule.jetSelection.ptCut = jetEt
                                                                  myModule.jetSelection.betaCut = self.getNumberFromCutWithDirection(jetBeta)
                                                                  myModule.jetSelection.betaCutDirection = self.getOperatorFromCutWithDirection(jetBeta)
                                                                  myModule.jetSelection.jetNumberCutDirection = self.getOperatorFromCutWithDirection(jetNumber)
                                                                  myModule.jetSelection.jetNumber = (int)(self.getNumberFromCutWithDirection(jetNumber))
                                                                  myModule.MET.METCut = met
                                                                  myModule.bTagging.discriminatorCut = bjetDiscr
                                                                  myModule.bTagging.ptCut = bjetEt
                                                                  myModule.bTagging.jetNumberCutDirection = self.getOperatorFromCutWithDirection(bjetNumber)
                                                                  myModule.bTagging.jetNumber = (int)(self.getNumberFromCutWithDirection(bjetNumber))
                                                                  myModule.deltaPhiTauMET = dphi
                                                                  # FIXME add top variation here
                                                                  # Add analysis
                                                                  addAnalysis(process, myVariationName, myModule,
                                                                              preSequence=commonSequence,
                                                                              additionalCounters=additionalCounters,
                                                                              signalAnalysisCounters=True)
        if self._maxVariations > 0:
            if nVariations > self._maxVariations:
                print "You generated %d variations, which is more than the safety limit (%d)!"%(nVariations,self._maxVariations)
                print "To remove the safety switch (if you REALLY know what you are doing), call disableMaxVariations()"
                sys.exit()
        print "Added %d variations to the analysis"%nVariations
