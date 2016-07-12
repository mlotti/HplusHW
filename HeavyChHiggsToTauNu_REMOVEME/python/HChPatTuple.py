import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, switchJetCollection
import PhysicsTools.PatAlgos.tools.tauTools as tauTools
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import restrictInputToAOD, removeSpecificPATObjects, removeCleaning, runOnData
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
import PhysicsTools.PatAlgos.tools.helpers as patHelpers
import PhysicsTools.PatAlgos.tools.pfTools as pfTools
import PhysicsTools.PatUtils.tools.metUncertaintyTools as metUncertaintyTools
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerStandAloneEventContent
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections
import CommonTools.ParticleFlow.TopProjectors.pfNoJet_cfi as pfNoJet
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggs as HChPFTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous as HChPFTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination as PFTauTestDiscrimination
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as HChDataSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMcSelection as HChMcSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex as HChPrimaryVertex
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.RemoveSoftMuonVisitor as RemoveSoftMuonVisitor
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations

tauPreSelection = "pt() > 15"
#tauPreSelection = ""

jetPreSelection = "pt() > 10"
#jetPreSelection = ""

muonPreSelection = "pt() > 5"
#muonPreSelection = ""

electronPreSelection = "pt() > 5"
#electronPreSelection = ""

outputModuleName = "out"

class PATBuilder:
    def __init__(self):
        pass

    def __call__(self, process, options, dataVersion,
                 patArgs={},
                 doTotalKinematicsFilter=False,
                 doHBHENoiseFilter=False, doPhysicsDeclared=False,
                 selectedPrimaryVertexFilter=False,
                 calculateEventCleaning=False,
                 additionalPattupleCounters=[]): # possible additional counters from pattuple job

        self.process = process
        self.counters = []

        sequence = cms.Sequence()

        if dataVersion.isData():
            # Append the data selection counters for data
            self.counters.extend(HChDataSelection.dataSelectionCounters[:])
        elif dataVersion.isMC() and options.triggerMC == 1:
            # If MC preselection is enabled, add the counters from there
            self.counters = HChMcSelection.mcSelectionCounters[:]

        if len(options.customizeConfig) > 0:
            for config in options.customizeConfig:
                module = __import__("HiggsAnalysis.HeavyChHiggsToTauNu."+config, fromlist=[config])
                if hasattr(module, "getCountersPrepend"):
                    self.counters = module.getCountersPrepend() + self.counters

                if hasattr(module, "getCounters"):
                    self.counters.extend(module.getCounters())

        if options.tauEmbeddingInput != 0:
            # Add the tau embedding counters, if that's the input
            import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff as PFEmbeddingSource
            self.counters.extend(MuonSelection.getMuonPreSelectionCountersForEmbedding())
            self.counters.extend(MuonSelection.getMuonSelectionCountersForEmbedding(dataVersion))
#            self.counters.extend(MuonSelection.getMuonSelectionCountersForEmbedding("PFlow"))
#            self.counters.extend(MuonSelection.getMuonSelectionCountersForEmbedding("PFlowChs"))
            self.counters.extend(PFEmbeddingSource.muonSelectionCounters)

        patOnTheFly = (options.doPat != 0)
        if patOnTheFly:
            print "Running PAT on the fly"

            self.process.eventPreSelection = cms.Sequence()

            if options.tauEmbeddingInput != 0:
                self.process.patSequence = self.addPatForTauEmbeddingInput(dataVersion, patArgs=patArgs, pvSelectionConfig=options.pvSelectionConfig)
            else:
                # normal AOD input
                if dataVersion.isData():
                    self.process.eventPreSelection = HChDataSelection.addDataSelection(process, dataVersion, options, calculateEventCleaning)
                elif dataVersion.isMC():
                    self.process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, options.triggerMC != 0, options.trigger)

                # Do some manipulation of PAT arguments, ensure that the
                # trigger has been given if Tau-HLT matching is required
                pargs = patArgs.copy()
                pargs["calculateEventCleaning"] = calculateEventCleaning
                if pargs.get("doTauHLTMatching", False):
                    if not "matchingTauTrigger" in pargs:
                        if options.trigger == "":
                            raise Exception("Command line argument 'trigger' is missing")
                        pargs["matchingTauTrigger"] = options.trigger
                    print "Trigger used for tau matching:", pargs["matchingTauTrigger"]

                self.process.patSequence = self.addPat(dataVersion, patArgs=pargs, pvSelectionConfig=options.pvSelectionConfig)
            sequence *= self.process.eventPreSelection

            # Selects the first primary vertex, applies the quality cuts to it
            # Applies quality cuts to all vertices too
            # Must be done before PAT sequence
            self.counters.extend(HChPrimaryVertex.addPrimaryVertexSelection(process, sequence, filter=selectedPrimaryVertexFilter))

            # Add PAT sequence
            sequence *= self.process.patSequence
        else:
            # Not running PAT, assuming that the job is taking pattuples as input
            for additionalPattupleCounter in additionalPattupleCounters:
                self.counters.append(additionalPattupleCounter)

        ## Common for PAT and analysis jobs
        # Add event filters if requested
        self.addFilters(dataVersion, sequence, doTotalKinematicsFilter, doHBHENoiseFilter, doPhysicsDeclared, patOnTheFly=(options.doPat != 0))

        if not patOnTheFly:
            # FIXME, this is hack only for v53_3 pattuples, remove for any future processing
            if dataVersion.isMC() and options.triggerMC == 0:
                # Add "missing" counters for datasets which were not
                # triggered in pattuple job
                self.process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, False, options.trigger)
                sequence += self.process.eventPreSelection

            # Add primary vertex selection
            # Selects the first primary vertex, applies the quality cuts to it
            # Applies quality cuts to all vertices too
            self.counters.extend(HChPrimaryVertex.addPrimaryVertexSelection(process, sequence, filter=selectedPrimaryVertexFilter))
            if options.tauEmbeddingInput != 0:
                # for embedding input, do vertex object selection for original event too
                self.counters.extend(HChPrimaryVertex.addPrimaryVertexSelection(process, sequence, srcProcess=dataVersion.getRecoProcess(), postfix="Original", filter=selectedPrimaryVertexFilter))

            if options.doTauHLTMatchingInAnalysis != 0:
                raise Exception("doTauLHTMatchingInAnalysis is not supported at the moment")
#                self.process.patTausHpsPFTauTauTriggerMatched = HChTriggerMatching.createTauTriggerMatchingInAnalysis(options.trigger, "selectedPatTausHpsPFTau")
#                seq *= process.patTausHpsPFTauTauTriggerMatched

        ## Common for PAT and analysis jobs (again)
        if options.bquarkNumFilter >= 0:
            if options.bquarkNumFilter > 3:
                raise Exception("bquarkNumFilter parameter is too large (%d), values 0,1,2,3 are valid (-1 for disabled)" % options.bquarkNumFilter)
            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChGenBQuarkFilter_cfi")
            sequence += getattr(process, "genBJetFilter"+{0: "ZeroBQuarks",
                                                          1: "OneBQuark",
                                                          2: "TwoBQuarks",
                                                          3: "ThreeOrMoreBQuarks"}[options.bquarkNumFilter])
            process.genBQuarkFiltered = cms.EDProducer("EventCountProducer")
            sequence += process.genBQuarkFiltered
            self.counters.append("genBQuarkFiltered")

        return (sequence, self.counters)

    def addPat(self, dataVersion, patArgs, pvSelectionConfig=""):
        # Add PF2PAT
        #sequence = addPF2PAT(self.process, dataVersion, patArgs=patArgs, pvSelectionConfig=pvSelectionConfig)
        sequence = addStandardPAT(self.process, dataVersion, patArgs=patArgs, pvSelectionConfig=pvSelectionConfig)
        return sequence
 
    def addFilters(self, dataVersion, sequence,
                   doTotalKinematicsFilter,
                   doHBHENoiseFilter, doPhysicsDeclared,
                   patOnTheFly):
        if dataVersion.isData():
            if doPhysicsDeclared:
                self.counters.extend(HChDataSelection.addPhysicsDeclaredBit(self.process, sequence))
            if doHBHENoiseFilter:
                if patOnTheFly:
                    HChDataSelection.addHBHENoiseFilterResultProducer(self.process, sequence)
                self.counters.extend(HChDataSelection.addHBHENoiseFilter(self.process, sequence))
        elif dataVersion.isMC() and doTotalKinematicsFilter:
            # TotalKinematicsFilter for managing with buggy LHE+Pythia samples
            if patOnTheFly:
                # https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1489.html
                self.process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")
                self.process.totalKinematicsFilter.src.setProcessName(dataVersion.getTriggerProcess())
            else:
                # For pattuples, this is implemented in patTuple_cfg.py, and saved in the event via TriggerResults
                import HLTrigger.HLTfilters.hltHighLevel_cfi as hltHighLevel
                self.process.totalKinematicsFilter = hltHighLevel.hltHighLevel.clone(
                    TriggerResultsTag = cms.InputTag("TriggerResults", "", "HChPatTuple"),
                    HLTPaths = cms.vstring("totalKinematicsFilterPath")
                )
            self.process.totalKinematicsFilterAllEvents = cms.EDproducer("EventCountProcucer")
            self.process.totalKinematicsFilterPassed = cms.EDProducer("EventCountProducer")
    

            sequence *(
                self.process.totalKinematicsFilterAllEvents *
                self.process.totalKinematicsFilter *
                self.process.totalKinematicsFilterPassed
            )
            self.counters.extend([
                    "totalKinematicsFilterAllEvents",
                    "totalKinematicsFilterPassed"
                    ])                    


    def addPatForTauEmbeddingInput(self, dataVersion, patArgs, pvSelectionConfig=""):
        # Hack to not to crash if something in PAT assumes process.out
        hasOut = hasattr(self.process, "out")
        if not hasOut:
            self.process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('dummy.root'),
                outputCommands = cms.untracked.vstring()
            )

        # Construct PF2PAT
        pargs = patArgs.copy()
        self._setPatArgs(pargs, {"doTauHLTMatching": False,
                                 "doMuonHLTMatching": False,
                                 "doPatElectronID": False,
                                 "doPatElectronMuon": False,
                                 })
        #sequence = addPF2PAT(self.process, dataVersion, doPatTrigger=False, doChs=False, patArgs=pargs, pvSelectionConfig=pvSelectionConfig)
        #postfix = "PFlow"
        #elePostfixes = [postfix, "PFlowAll"] # + ["PFlowChs", "PFlowChsAll"]
        #jetPostfix = postfix
        sequence = addStandardPAT(self.process, dataVersion, doPatTrigger=False, patArgs=pargs, pvSelectionConfig=pvSelectionConfig)
        postfix = ""
        elePostfixes = [""]

        # # Remove patElectrons and patPhotons altogether for the hybrid events
        # for fix in elePostfixes:
        #     seq = getattr(self.process, "patDefaultSequence"+fix)
        #     if dataVersion.isMC():
        #         seq.remove(getattr(self.process, "makePatElectrons"+fix))
        #         seq.remove(getattr(self.process, "photonMatch"+fix))
        #         delattr(self.process, "photonMatch"+fix)
        #     else:
        #         # Thanks to difference sequence structure we have to do this separately for data
        #         seq.remove(getattr(self.process, "patElectrons"+fix))

        #     seq.remove(getattr(self.process, "selectedPatElectrons"+fix))
        #     delattr(self.process, "patElectrons"+fix)
        #     delattr(self.process, "selectedPatElectrons"+fix)
        # Remove electrons, photons, muons from the hybrid events
        removeSpecificPATObjects(self.process, ["Muons", "Electrons", "Photons"], outputModules=[])

        # Remove pat caloMET
        if postfix == "":
            self.process.patDefaultSequence.remove(self.process.makePatMETs)

        # Remove soft muon/electron b tagging discriminators as they are not
        # well defined, cause technical problems and we don't use
        # them.
        def filterOutSoft(tag):
            label = tag.getModuleLabel()
            return "softMuon" not in label and "softElectron" not in label
        getattr(self.process, "patJets"+postfix).discriminatorSources = filter(filterOutSoft, self.process.patJets.discriminatorSources)
        #self.process.patJetsPFlowChs.discriminatorSources = filter(filterOutSoft, self.process.patJets.discriminatorSources)
        for seq in [self.process.btagging,
                    #self.process.btaggingJetTagsAODPFlow, self.process.btaggingTagInfosAODPFlow,
                    #self.process.btaggingJetTagsAODPFlowChs, self.process.btaggingTagInfosAODPFlowChs,
                    ]:
            softMuonRemover = RemoveSoftMuonVisitor.RemoveSoftMuonVisitor()
            seq.visit(softMuonRemover)
            softMuonRemover.removeFound(self.process, seq)

           
        # Use the merged track collection
        if postfix == "":
            self.process.jetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")
            self.process.ak5PFJetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")
        else:
            getattr(self.process, "pfJetTracksAssociatorAtVertex"+postfix).tracks.setModuleLabel("tmfTracks")
            getattr(self.process, "jetTracksAssociatorAtVertex"+postfix).tracks.setModuleLabel("tmfTracks")

        # Do jet-parton matching with the genParticles of the original event
        if dataVersion.isMC():
            getattr(self.process, "patJetPartons"+postfix).src.setProcessName(dataVersion.getTriggerProcess())
            getattr(self.process, "patJetPartonMatch"+postfix).matched.setProcessName(dataVersion.getTriggerProcess())

            # in v13_3 embeddings the GenJets are done from the tau part, hence they are meaningless
            getattr(self.process, "patJets"+postfix).addGenJetMatch = False
            getattr(self.process, "patJets"+postfix).genJetMatch = ""

        # This is now somewhat WTF, is the normal b-tagging affected by this? (FIXME)
        # I can't replace the InputTag module labels in place, because they are shared between the two PATJetProducers
        if postfix != "":
            tags = []
            for inputTag in getattr(self.process, "patJets"+postfix).discriminatorSources:
                tags.append(cms.InputTag(inputTag.getModuleLabel()+"AOD"+postfix))
            getattr(self.process, "patJets"+postfix).discriminatorSources = tags
            tags = []
            #for inputTag in self.process.patJetsPFlowChs.discriminatorSources:
            #    tags.append(cms.InputTag(inputTag.getModuleLabel()+"AODPFlowChs"))
            #self.process.patJetsPFlowChs.discriminatorSources = tags


        # Another part of the PAT process.out hack
        if not hasOut:
            del self.process.out
      
        return sequence

    def _setPatArg(self, args, name, value):
        if name in args:
            print "Overriding PAT arg '%s' from '%s' to '%s'" % (name, str(args[name]), str(value))
        args[name] = value
    def _setPatArgs(self, args, d):
        for name, value in d.iteritems():
            self._setPatArg(args, name, value)

addPatOnTheFly = PATBuilder()


def myRemoveCleaning(process, postfix=""):
    modulesInSequence = getattr(process, "patDefaultSequence"+postfix).moduleNames()
    for module in [
        "cleanPatMuons",
        "cleanPatElectrons",
        "cleanPatPhotons",
        "cleanPatTaus",
        "cleanPatTausHpsTancPFTau",
        "cleanPatTausHpsPFTau",
        "cleanPatTausShrinkingConePFTau",
        "cleanPatTausCaloRecoTau",
        "cleanPatJets",
        "cleanPatCandidateSummary",
        ]:
        if hasattr(process, module+postfix) and module+postfix in modulesInSequence:
            getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, module+postfix))

    removeCounting(process, postfix)

def removeCounting(process, postfix=""):
    modulesInSequence = getattr(process, "patDefaultSequence"+postfix).moduleNames()
    for module in [
        "countPatElectrons",
        "countPatMuons",
        "countPatTaus",
        "countPatLeptons",
        "countPatPhotons",
        "countPatJets",
        "countPatJetsAK5PF",
        "countPatJetsAK5JPT",
        "countPatPFParticles",
        ]:
        if hasattr(process, module+postfix) and module+postfix in modulesInSequence:
            getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, module+postfix))


##################################################
#
# Base class for PAT Builders
#
# To set default PAT arguments etc
class PATBuilderBase:
    def __init__(self, process, dataVersion,
                 doHChTauDiscriminators=True, doPatTauIsoDeposits=False,
                 doTauHLTMatching=False, matchingTauTrigger=None,
                 doMuonHLTMatching=True,
                 doPatElectronMuon=True,
                 doPatElectronID=True,
                 includePFCands=False,
                 calculateEventCleaning=False):
        self.process = process
        self.dataVersion = dataVersion

        self.doHChTauDiscriminators = doHChTauDiscriminators
        self.doPatTauIsoDeposits = doPatTauIsoDeposits

        self.doTauHLTMatching = doTauHLTMatching
        self.matchingTauTrigger = matchingTauTrigger
        self.doMuonHLTMatching = doMuonHLTMatching
        self.doPatElectronMuon = doPatElectronMuon
        self.doPatElectronID = doPatElectronID
        self.includePFCands = includePFCands
        self.calculateEventCleaning = calculateEventCleaning

        self.outputCommands = []

        self.beginSequence = cms.Sequence()
        self.endSequence = cms.Sequence()

    def getOutputCommands(self):
        return self.outputCommands
       

##################################################
#
# Standard PAT
# 
# FIXME: this is still under development
class StandardPATBuilder(PATBuilderBase):
    def __init__(self, *args, **kwargs):
        PATBuilderBase.__init__(self, *args, **kwargs)

    def customize(self, jetPostfixes):
        out = None
        outdict = self.process.outputModules_()
        if outdict.has_key(outputModuleName):
            out = outdict[outputModuleName]

        # Remove MC stuff if we have real data
        # This also adds the L2L3Residual JEC to the process.patJetCorrFactors
        if self.dataVersion.isData():
            o = []
            if out != None:
                o = [outputModuleName]
            runOnData(self.process, outputModules=o)

        # Keep PFCandidates?
        if self.includePFCands:
            self.outputCommands.extend([
                    "keep *_particleFlow_*_*",
                    "keep *_generalTracks_*_*",
                    ])

        # Add PF isolation for electrons and muons
        if self.doPatElectronMuon:
            pfTools.usePFIso(self.process)
            # Apparently for data the sequences are such that the PFIso
            # sequences do not end up in patDefaultSequence
            if self.dataVersion.isData():
                self.process.patDefaultSequence.insert(0,
                                                       self.process.pfParticleSelectionSequence +
                                                       self.process.eleIsoSequence +
                                                       self.process.muIsoSequence)

        # Customize physics objects
        if self.doPatElectronMuon:
            self._customizeMuons()
            self._customizeElectrons()
        self._customizePhotons()
        self._customizeJets(jetPostfixes)
        self._customizeTaus()
        self._customizeMET(jetPostfixes)

        self._customizeEventCleaning()

        # Build the sequences
        setattr(self.process, "patHplusCustomBefore", self.beginSequence)
        setattr(self.process, "patHplusCustomAfter", self.endSequence)

        sequence = getattr(self.process, "patDefaultSequence")
        sequence.insert(0, self.beginSequence)
        sequence *= self.endSequence

    def _customizeMuons(self):
        # Default lepton options
        setPatLeptonDefaults(self.process.patMuons, self.includePFCands)
        
        self.process.selectedPatMuons.cut = muonPreSelection

        # Add isolation variables for embedding
        self.process.muonIsolationEmbeddingSequence = cms.Sequence()
        muons = tauEmbeddingCustomisations.addMuonIsolationEmbedding(self.process, self.process.muonIsolationEmbeddingSequence, "patMuons")
        self.process.patDefaultSequence.replace(self.process.selectedPatMuons,
                                                self.process.muonIsolationEmbeddingSequence*self.process.selectedPatMuons)
        self.process.selectedPatMuons.src = muons

        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Cosmic_IDs
        proto = cms.EDProducer("HPlusCosmicID",
            src=cms.InputTag("muons", "cosmicsVeto"),
            result = cms.string("cosmicCompatibility")
        )
        for name in ["cosmicCompatibility", 'timeCompatibility','backToBackCompatibility','overlapCompatibility']:
            m = proto.clone(result=name)
            self.beginSequence *= m
            setattr(self.process, name, m)
            self.process.patMuons.userData.userFloats.src.append(cms.InputTag(name))

        # HLT Matching
        if self.doMuonHLTMatching:
            (muHltSequence, muonsWithTrigger) = HChTriggerMatching.addMuonTriggerMatching(self.process, muons=self.process.selectedPatMuons.src.value())
            self.process.muonTriggerMatchingSequence = muHltSequence
            self.process.selectedPatMuons.src = muonsWithTrigger
            self.process.patDefaultSequence.replace(self.process.selectedPatMuons,
                                                    self.process.muonTriggerMatchingSequence * self.process.selectedPatMuons)
            self.outputCommands.append("drop patTriggerObjectStandAlonesedmAssociation_*_*_*")

        self.outputCommands.extend([
                "keep *_selectedPatMuons_*_*"
                ])

    def _customizeElectrons(self):
        setPatLeptonDefaults(self.process.patElectrons, self.includePFCands)

        self.process.selectedPatElectrons.cut = electronPreSelection

        # Switch isolation cone to DR<0.3 (POG recommendation) from
        # the DR<0.4 (PAT default) for the isolation values. We can
        # still compute the isolation in an almost-arbitrary cone with
        # iso deposits.
        def coneTo03(inputTag):
            inputTag.setModuleLabel(inputTag.getModuleLabel().replace("04", "03"))
        for name in self.process.patElectrons.isolationValues.parameterNames_():
            coneTo03(getattr(self.process.patElectrons.isolationValues, name))
            coneTo03(getattr(self.process.patElectrons.isolationValuesNoPFId, name))

        # Calculate the "rho" for electron isolation "effective area"
        # PU correction
        # https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection
        import RecoJets.JetProducers.kt4PFJets_cfi as kt4PFJets_cfi
        self.process.kt6PFJetsForEleIso = kt4PFJets_cfi.kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
        self.process.kt6PFJetsForEleIso.Rho_EtaMax = cms.double(2.5)
        self.beginSequence *= self.process.kt6PFJetsForEleIso

        if self.doPatElectronID:
            addPatElectronID(self.process, self.process.patElectrons)

        # Keep Conversion objects for later simple cut-based ID
        self.outputCommands.extend([
                "keep *_selectedPatElectrons_*_*",
                "keep *_allConversions_*_*",
                ])

    def _customizePhotons(self):
        self.outputCommands.extend([
                "keep *_selectedPatPhotons_*_*"
                ])

    def _customizeJets(self, jetPostfixes):
        # Switch to AK5PF jets, for standard PAT jets
        setPatJetCorrDefaults(self.process.patJetCorrFactors, self.dataVersion, True)
        switchJetCollection(self.process, cms.InputTag('ak5PFJets'),
                            doJTA        = True,
                            doBTagging   = True,
                            jetCorrLabel = ('AK5PF', self.process.patJetCorrFactors.levels),
                            doType1MET   = False,
                            genJetCollection = cms.InputTag("ak5GenJets"),
                            doJetID      = True
        )

        # Customization similar to all jets (standard PAT, CHS)
        for postfix in jetPostfixes:
            self._customizeJetCollection(postfix)

    def _customizeJetCollection(self, postfix):
        # Don't embed PFCandidates
        setPatJetDefaults(getattr(self.process, "patJets"+postfix))

        # Embed beta and betastar to pat::Jet
        setattr(self.process, "patJetsBetaEmbedded"+postfix, cms.EDProducer("HPlusPATJetViewBetaEmbedder",
            jetSrc = cms.InputTag("patJets"+postfix),
            generalTracksSrc = cms.InputTag("generalTracks"),
            vertexSrc = cms.InputTag("offlinePrimaryVertices"),
            embedPrefix = cms.string("")
        ))
        getattr(self.process, "selectedPatJets"+postfix).src = "patJetsBetaEmbedded"+postfix
        getattr(self.process, "patDefaultSequence"+postfix).replace(
            getattr(self.process, "selectedPatJets"+postfix),
            getattr(self.process, "patJetsBetaEmbedded"+postfix) * getattr(self.process, "selectedPatJets"+postfix))

        # jet pre-selection
        getattr(self.process, "selectedPatJets"+postfix).cut = jetPreSelection

        # PU jet ID
        if not hasattr(self.process, "puJetIdSqeuence"):
            self.process.load("CMGTools.External.pujetidsequence_cff")
        if postfix not in ["", "Chs"]:
            raise Exception("Only empty and 'Chs' postfix are supported")
        if postfix == "Chs":
            self.process.puJetIdChs.jets = "selectedPatJetsChs"
            self.process.puJetMvaChs.jets = "selectedPatJetsChs"

        self.endSequence *= getattr(self.process, "puJetIdSqeuence"+postfix)
            

        self.outputCommands.extend([
                "keep *_selectedPatJets%s_*_*" % postfix,
                "keep *_puJetId%s_*_*" % postfix,  # PU jet ID input variables
                "keep *_puJetMva%s_*_*" % postfix, # PU jet ID final MVAs and working point flags
                #"drop *_selectedPatJets_*_*",
                #"keep *_selectedPatJetsAK5JPT_*_*",
                #"keep *_selectedPatJetsAK5PF_*_*",
                #'drop *_selectedPatJets_pfCandidates_*', ## drop for default patJets which are CaloJets
                #'drop *_*PF_caloTowers_*',
                #'drop *_*JPT_pfCandidates_*',
                #'drop *_*Calo_pfCandidates_*',
                ])


    def _customizeTaus(self):
        # Reproduce PFTaus (as recommended by POG)
        self.process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
        self.beginSequence *= self.process.PFTau

        # PAT taus are now HPS by default
        patTaus = self.process.patTaus
        selectedPatTaus = self.process.selectedPatTaus

        # Set objects to embedded to pat::Tau
        setPatTauDefaults(patTaus, self.includePFCands)
        selectedPatTaus.cut = tauPreSelection

        # Produce HCh discriminators (could we really reduce the number of these?), and add them to pat::Tau producer
        if self.doHChTauDiscriminators:
            tauAlgos = ["hpsPFTauProducer"]

            HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(self.process, tauAlgos)
            HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(self.process, tauAlgos)
            PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(self.process, tauAlgos)

            # Tau bugfixes
            # The quality PSet is missing
            for algo in tauAlgos:
                fixFlightPath(self.process, algo)
                fixFlightPath(self.process, algo, "Cont")

            # Add to sequence
            self.beginSequence *= (
                self.process.PFTauDiscriminationSequenceForChargedHiggs *
                self.process.PFTauDiscriminationSequenceForChargedHiggsCont *
                self.process.PFTauTestDiscriminationSequence
            )

            
            for idSources in [HChPFTauDiscriminators.HChTauIDSources,
                              HChPFTauDiscriminatorsCont.HChTauIDSourcesCont,
                              PFTauTestDiscrimination.TestTauIDSources]:
                for label, tag in idSources:
                    setattr(patTaus.tauIDSources, label, cms.InputTag("hpsPFTauProducer"+tag))

        # Add the continuous isolation discriminators
        addTauRawDiscriminators(patTaus)

        # Remove iso deposits to save disk space and time
        if not self.doPatTauIsoDeposits:
            for isoDepName in patTaus.isoDeposits.parameterNames_():
                inputLabel = getattr(patTaus.isoDeposits, isoDepName).getModuleLabel()
                HChTools.removeEverywhere(self.process, inputLabel)
            patTaus.isoDeposits = cms.PSet()
            patTaus.userIsolation = cms.PSet()

        # Trigger matching
        if self.doTauHLTMatching:
            print "Tau HLT matching in PATTuple production is disabled. It should be done in the analysis jobs from now on."
#            self.endSequence *= HChTriggerMatching.addTauHLTMatching(self.process, self.matchingTauTrigger, collections=["patTausHpsPFTau"], outputCommands=self.outputCommands)

        self.outputCommands.extend([
                "keep *_selectedPatTaus_*_*",
#                "drop *_selectedPatTaus_*_*",
#                "keep *_selectedPatTausHpsPFTau_*_*",
                #"keep *_selectedPatTausHpsTancPFTau_*_*",
                ])

    def _customizeMET(self, jetPostfixes):
        # Produce Type I MET correction from all PF jets
        # Note that further correction is needed at the analysis level
        # to remove contribution from jet energy corrections of those
        # jets which correspond isolated e/mu/tau

        seq = self.process.patDefaultSequence

        self.outputCommands.extend([
                "keep recoCaloMETs_*_*_*", # keep all calo METs (metNoHF is needed!)
                "keep *_genMetTrue_*_*", # keep generator level MET
                ])

        self.process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
        # For Type 0 MET hack, include the producers in the sequence,
        # but not to the default corrected-MET producers
        self.process.producePatPFMETCorrections.replace(self.process.patPFJetMETtype2Corr,
                                                        (self.process.patPFJetMETtype2Corr+self.process.type0PFMEtCorrection+self.process.patPFMETtype0Corr))


        if self.dataVersion.isData():
            for postfix in jetPostfixes:
                jets = getattr(self.process, "selectedPatJets"+postfix).src.value()

                for pfix in [postfix, postfix+"Type0"]:
                    if pfix != "":
                        patHelpers.cloneProcessingSnippet(self.process, self.process.producePatPFMETCorrections, pfix)
                    getattr(self.process, "selectedPatJetsForMETtype1p2Corr"+pfix).src = jets
                    getattr(self.process, "selectedPatJetsForMETtype2Corr"+pfix).src = jets
                    getattr(self.process, "patPFMet"+pfix).addGenMET = False
                    if "Type0" in pfix:
                        getattr(self.process, "patType1CorrectedPFMet"+pfix).srcType1Corrections.append(cms.InputTag('patPFMETtype0Corr'+pfix))
                        getattr(self.process, "patType1p2CorrectedPFMet"+pfix).srcType1Corrections.append(cms.InputTag('patPFMETtype0Corr'+pfix))

                    seq *= getattr(self.process, "producePatPFMETCorrections"+pfix)

                    # Type 0 correction is included only in Type1 and
                    # Type1p2 MET objects
                    if not "Type0" in pfix:
                        self.outputCommands.append("keep *_patPFMet%s_*_*" % pfix)
                    self.outputCommands.extend([
                            "keep *_patType1CorrectedPFMet%s_*_*" % pfix,
                            "keep *_patType1p2CorrectedPFMet%s_*_*" % pfix,
                            ])
            return

        # Following is for MC only

        outputModule = ""
        outdict = self.process.outputModules_()
        if outdict.has_key(outputModuleName):
            outputModule = outputModuleName

        for postfix in jetPostfixes:
            # Reset the OutputModule outputCommands to catch the event
            # content modifications done in the runMEtUncertainties.
            # Resetting is fine since the outputCommands are saved in
            # addPF2PAT() before a call to this method, and they are
            # set to proper values after a call to this method.
            if outputModule != "":
                getattr(self.process, outputModule).outputCommands = []
                

            jets = getattr(self.process, "selectedPatJets"+postfix).src.value()

            # Smear the jet energies by JER data/MC difference for MC only
            metUncertaintyTools.runMEtUncertainties(self.process,
                                                    electronCollection="",
                                                    photonCollection="",
                                                    muonCollection="",
                                                    tauCollection="",
                                                    jetCollection=jets,
                                                    doSmearJets=self.dataVersion.isMC(),
                                                    outputModule=outputModule,
                                                    postfix=postfix,
                                                    )
            # Another version of MET+variations with Type 0 correction
            metUncertaintyTools.runMEtUncertainties(self.process,
                                                    electronCollection="",
                                                    photonCollection="",
                                                    muonCollection="",
                                                    tauCollection="",
                                                    jetCollection=jets,
                                                    doSmearJets=self.dataVersion.isMC(),
                                                    doApplyType0corr=True,
                                                    outputModule=outputModule,
                                                    postfix=postfix+"Type0",
                                                    )

            processName = self.process.name_()
            # Drop jet collections with "Type0" in their name, their
            # just duplicates of the usual jets. Also drop uncorrected
            # "Type0", since Type 0 corrections are included only in
            # Type1 and Type1p2 MET objects
            self.process.out.outputCommands.extend([
                    "drop patJets_*%sType0_*_%s" % (postfix, processName),
                    "drop *_patPFMet%sType0_*_%s" % (postfix, processName),
                    ])

            # Add "selected"-collections for all jets
            # "All" name "shiftedPatJetsBetaEmbeddedPFlowEnUpForCorrMEt"
            # "Selected" name "shiftedPatJetsPFlowEnUpForCorrMEt"
            # Create also PU jet ID for each "Selected" collection
            tmp = jets.replace("patJets", "")
            shiftedJetNames = [ # These are the ones produced by runMEtUncertainties
                "shiftedPatJets%sEnUpForCorrMEt%s" % (tmp, postfix),
                "shiftedPatJets%sEnDownForCorrMEt%s" % (tmp, postfix),
                "smearedPatJets%s%s" % (tmp, postfix),
                "smearedPatJets%sResUp%s" % (tmp, postfix),
                "smearedPatJets%sResDown%s" % (tmp, postfix),
                ]
            selectedJetNames = []

            for shiftedJet in shiftedJetNames:
                # Create selectedPatJets
                m = self.process.selectedPatJets.clone(
                    src = shiftedJet
                )
                name = shiftedJet.replace(tmp, "")
                setattr(self.process, name, m)
                seq *= m
                selectedJetNames.append(name)
    
                # Clone PU jet ID
                if not hasattr(self.process, "puJetIdSqeuence%sFor%s" % (postfix, name)):
                    puJetIdSequence = patHelpers.cloneProcessingSnippet(self.process, getattr(self.process, "puJetIdSqeuence"+postfix), "For"+name)
                    seq *= puJetIdSequence
                if postfix not in ["", "Chs"]:
                    raise Exception("Jet postfix other than empty or 'Chs' not supported, got %s" % postfix)

                getattr(self.process, "puJetId%sFor%s" % (postfix, name)).jets = name
                getattr(self.process, "puJetMva%sFor%s" % (postfix, name)).jets = name
    
            if outputModule != "":
                self.outputCommands.extend(getattr(self.process, outputModule).outputCommands)
                self.process.out.outputCommands = []

   
                # Drop "all" shifted/smeared jet collections in favor of
                # the "selected" collections. We don't need the
                # "ForRawMEt" energy variations.
                self.outputCommands.extend([
                        "drop *_shiftedPatJetsBetaEmbedded%sEnUpForRawMEt%s_*_%s" % (postfix, postfix, processName),
                        "drop *_shiftedPatJetsBetaEmbedded%sEnDownForRawMEt%s_*_%s" % (postfix, postfix, processName)
                        ])
                for n in shiftedJetNames:
                    self.outputCommands.append("drop *_%s_*_%s" % (n, processName))
                # Keep the "selected" collections
                for n in selectedJetNames:
                    self.outputCommands.extend([
                            "keep *_%s_*_%s" % (n, processName),
                            "keep *_puJetId%sFor%s_*_%s" % (postfix, n, processName),
                            "keep *_puJetMva%sFor%s_*_%s" % (postfix, n, processName),
                            ])
    
    def _customizeEventCleaning(self):
        self.outputCommands.extend([
                "keep recoBeamHaloSummary_*_*_*", # keep beam halo summaries
                "keep recoGlobalHaloData_*_*_*",
                ])

        # HBHE noise filter
        if self.dataVersion.isData():
            HChDataSelection.addHBHENoiseFilterResultProducer(self.process, self.endSequence)
            self.outputCommands.append("keep *_HBHENoiseFilterResultProducer*_*_*")

        # TotalKinematicsFilter for managing with buggy LHE+Pythia samples
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1489.html
        if self.dataVersion.isMC():
            self.process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")
            self.process.totalKinematicsFilter.src.setProcessName(self.dataVersion.getSimProcess())
            self.process.totalKinematicsFilterPath = cms.Path(
                self.process.totalKinematicsFilter
            )

        if not self.calculateEventCleaning:
            return

        # These require the tags in test/pattuple/checkoutTags.sh

        if self.dataVersion.isData():
            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter_updated
            self.process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
            self.process.trackingFailureFilter.VertexSource = "goodPrimaryVertices"
            self.process.trackingFailureFilter.taggingMode = True
            self.endSequence *= self.process.trackingFailureFilter
            self.outputCommands.append("keep *_trackingFailureFilter*_*_*")

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
            # https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
            self.process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
            self.process.EcalDeadCellTriggerPrimitiveFilter.taggingMode = True

            self.process.load('RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi')
            self.process.EcalDeadCellBoundaryEnergyFilter.taggingMode = cms.bool(False)
            self.process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEB=cms.untracked.double(10)
            self.process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEE=cms.untracked.double(10)
            self.process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEB=cms.untracked.double(100)
            self.process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEE=cms.untracked.double(100)
            self.process.EcalDeadCellBoundaryEnergyFilter.enableGap=cms.untracked.bool(False)
            self.process.EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEB = cms.vint32(12,14)
            self.process.EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEE = cms.vint32(12,14)
            self.process.EcalDeadCellBoundaryEnergyFilter.taggingMode = True

            self.endSequence *= (
                self.process.EcalDeadCellTriggerPrimitiveFilter *
                self.process.EcalDeadCellBoundaryEnergyFilter
            )
            self.outputCommands.extend([
                    "keep *_EcalDeadCellTriggerPrimitiveFilter_*_*",
                    "keep *_EcalDeadCellBoundaryEnergyFilter_*_*",
                    ])

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#CSC_Beam_Halo_Filter
            self.process.load("RecoMET.METAnalyzers.CSCHaloFilter_cfi")
            self.process.CSCTightHaloFilterPath = cms.Path(self.process.CSCTightHaloFilter)

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#HCAL_laser_events_updated
            # Keep still the old
            self.process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
            self.process.hcalLaserEventFilter.taggingMode = True
            self.endSequence *= self.process.hcalLaserEventFilter
            self.outputCommands.append("keep *_hcalLaserEventFilter_*_*")
            # New (November 2012)
            self.process.load("EventFilter.HcalRawToDigi.hcallasereventfilter2012_cfi")
            self.process.hcallasereventfilter2012Path = cms.Path(self.process.hcallasereventfilter2012)

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Bad_EE_Supercrystal_filter_added
            self.process.load("RecoMET.METFilters.eeBadScFilter_cfi")
            self.process.eeBadScFilter.taggingMode = True
            self.endSequence *= self.process.eeBadScFilter
            self.outputCommands.append("keep *_eeBadScFilter_*_*")

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#EB_or_EE_Xtals_with_large_laser
            self.process.load("RecoMET.METFilters.ecalLaserCorrFilter_cfi")
            self.process.ecalLaserCorrFilter.taggingMode = True
            self.endSequence *= self.process.ecalLaserCorrFilter
            self.outputCommands.append("keep *_ecalLaserCorrFilter_*_*")

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_odd_events_filters
            # https://twiki.cern.ch/twiki/bin/view/CMS/TrackingPOGFilters#Filters
            # http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/RecoMET/METFilters/test/exampleICHEPrecommendation_cfg.py?revision=1.3&view=markup&pathrev=V00-00-13
            self.process.load("RecoMET.METFilters.trackingPOGFilters_cff")
            for name in ["manystripclus53X", "toomanystripclus53X", "logErrorTooManyClusters", # in process.trkPOGFilters sequence
                         # others available in trackingPOGFilters_cfi
                         "logErrorTooManyTripletsPairs", "logErrorTooManySeeds", "logErrorTooManySeedsDefault",
                         "logErrorTooManyTripletsPairsMainIterations", "logErrorTooManySeedsMainIterations",
                         ]:
                mod = getattr(self.process, name)
                mod.taggedMode = cms.untracked.bool(True)
                self.endSequence += mod
                self.outputCommands.append("keep *_%s_*_*" % name)

            # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Muons_with_wrong_momenta_PF_only
            self.process.load('RecoMET.METFilters.inconsistentMuonPFCandidateFilter_cfi')
            self.process.load('RecoMET.METFilters.greedyMuonPFCandidateFilter_cfi')
            self.process.inconsistentMuonPFCandidateFilter.taggingMode = True
            self.process.greedyMuonPFCandidateFilter.taggingMode = True
            self.endSequence *= (
                self.process.inconsistentMuonPFCandidateFilter *
                self.process.greedyMuonPFCandidateFilter
            )
            self.outputCommands.extend([
                    "keep *_inconsistentMuonPFCandidateFilter_*_*",
                    "keep *_greedyMuonPFCandidateFilter_*_*",
            ])

def addStandardPAT(process, dataVersion, doPatTrigger=True, doChsJets=True, patArgs={}, pvSelectionConfig=""):
    print "########################################"
    print "#"
    print "# Using standard PAT"
    print "#"
    print "########################################"

    out = None
    outdict = process.outputModules_()
    outputCommands = []
    hasOut = False
    if outdict.has_key(outputModuleName):
        out = outdict[outputModuleName]
        outputCommands = out.outputCommands[:]
        hasOut = True
    else:
        # Hack to not to crash if something in PAT assumes process.out
        process.out = cms.OutputModule("PoolOutputModule",
            fileName = cms.untracked.string("dummy.root"),
            outputCommands = cms.untracked.vstring()
        )
        out = process.out
        

    # Out usual event content
    outputCommands.extend([
            "keep *_genParticles_*_*",
            "keep edmTriggerResults_*_*_*",
#            "keep triggerTriggerEvent_*_*_*", # the information is alread in full PAT trigger
            "keep L1GlobalTriggerReadoutRecord_*_*_*",   # needed for prescale provider
#            "keep L1GlobalTriggerObjectMapRecord_*_*_*", # needed for prescale provider
            "keep *_conditionsInEdm_*_*",
            "keep edmMergeableCounter_*_*_*", # in lumi block
            "keep PileupSummaryInfos_*_*_*", # only in MC
            "keep *_offlinePrimaryVertices_*_*",
            "keep *_l1GtTriggerMenuLite_*_*", # in run block, needed for prescale provider
            "keep *_kt6PFJets*_rho_*", # keep the rho of the event
            ])
    if dataVersion.isData():
        # Why do we need this?
        outputCommands.append("drop recoGenJets_*_*_*")
    else:
        outputCommands.extend([
                "keep LHEEventProduct_*_*_*",
                "keep GenEventInfoProduct_*_*_*",
                "keep GenRunInfoProduct_*_*_*",
                ])

    sequence = cms.Sequence()

    # Visible taus
    if dataVersion.isMC():
        process.VisibleTaus = cms.EDProducer("HLTTauMCProducer",
            GenParticles  = cms.untracked.InputTag("genParticles"),
            ptMinTau      = cms.untracked.double(3),
            ptMinMuon     = cms.untracked.double(3),
            ptMinElectron = cms.untracked.double(3),
            BosonID       = cms.untracked.vint32(23),
            EtaMax         = cms.untracked.double(2.5)
        )
        sequence *= process.VisibleTaus
        outputCommands.append("keep *_VisibleTaus_*_*")

    # Vertex and Beamspot
    outputCommands.extend([
            "keep *_offlinePrimaryVerticesSumPt_*_*",
            "keep *_offlineBeamSpot_*_*",
            ])

    # ValueMap of sumPt of vertices
    process.offlinePrimaryVerticesSumPt = cms.EDProducer("HPlusVertexViewSumPtComputer",
        src = cms.InputTag("offlinePrimaryVertices")
    )
    sequence *= process.offlinePrimaryVerticesSumPt


    # PAT
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    jetPostfixes = [""]

    # PF2PAT for CHS jets
    # Probably the easiest way to get CHS jets is to use PF2PAT and disable muon/electron top projections
    if doChsJets:
        jetCorrFactors = patJetCorrLevels(dataVersion, L1FastJet=True)
        pfTools.usePF2PAT(process, runPF2PAT=True, jetAlgo="AK5", jetCorrections=("AK5PFchs", jetCorrFactors),
                          runOnMC=dataVersion.isMC(), postfix="Chs")
        # Apparently have to set this explicitly in order to have pro
        process.pfPileUpChs.checkClosestZVertex = False
        # Disable isolated muon/electron top projections before jet clustering
        process.pfNoMuonChs.enable = False
        process.pfNoElectronChs.enable = False

        # Disable jet-tau disambiguation (we do it ourselves in the analysis)
        process.pfNoTauChs.enable = False
        # Remove all tau-related from the CHS sequence, we don't use
        # CHS-tau and they just waste some precious time
        process.PFBRECOChs.remove(process.pfTauSequenceChs)
        remove = ["patHPSPFTauDiscriminationUpdateChs", "patPFTauIsolationChs", "patTausChs", "selectedPatTausChs", "countPatTausChs"]
        if dataVersion.isMC():
            remove.extend(["tauMatchChs", "tauGenJetsChs", "tauGenJetsSelectorAllHadronsChs", "tauGenJetMatchChs"])
        for name in remove:
            process.patDefaultSequenceChs.remove(getattr(process, name))

        # Remove MET from CHS sequence, we don't use it and it just
        # wastes some precious time
        process.PFBRECOChs.remove(process.pfMETChs)
        process.patDefaultSequenceChs.remove(process.patMETsChs)


        jetPostfixes.append("Chs")
        process.patDefaultSequence *= process.patPF2PATSequenceChs


    # Run simple electron ID sequence for once (default is to run it)
    if not "doPatElectronID" in patArgs or patArgs["doPatElectronID"]:
        addPatElectronIDProducers(process, sequence)

    # Customize PAT
    patBuilder = StandardPATBuilder(process, dataVersion, **patArgs)
    patBuilder.customize(jetPostfixes)
    outputCommands.extend(patBuilder.getOutputCommands())

    ### Trigger (as the last)
    if doPatTrigger:
        outputCommands.extend(addPatTrigger(process, dataVersion, sequence))


    ### Other customisation
    # Tracks (mainly needed for muon efficiency tag&probe studies
    process.generalTracks20eta2p5 = cms.EDFilter("TrackSelector",
        src = cms.InputTag("generalTracks"),
        cut = cms.string("pt > 20 && abs(eta) < 2.5"),
        filter = cms.bool(False)
    )
    sequence *= process.generalTracks20eta2p5
    outputCommands.append("keep *_generalTracks20eta2p5_*_*")
    

    ### Primary vertex selection
    # Although defined here, it is run before any PF2PAT modules
    # It just has to be run after PAT trigger, in order make use of that in the PV selection code
    if len(pvSelectionConfig) > 0:
        # Reorder offlinePrimaryVertices
        module = __import__("HiggsAnalysis.HeavyChHiggsToTauNu."+pvSelectionConfig, fromlist=[pvSelectionConfig])
        process.primaryVertexSelectionSequence = module.buildSequence(process, patArgs)

        process.offlinePrimaryVertices = cms.EDProducer("HPlusVertexReorderProducer",
            vertexSrc = cms.InputTag("offlinePrimaryVertices"),
            indexSrc = cms.InputTag("selectedPrimaryVertexIndex")
        )
        process.primaryVertexSelectionSequence *= process.offlinePrimaryVertices
        outputCommands.extend([
                "drop *_offlinePrimaryVertices_*_*",
                "keep *_offlinePrimaryVertices_*_%s" % process.name_(),
                "keep *_selectedPrimaryVertexIndex_*_*",
                ])

        sequence *= process.primaryVertexSelectionSequence

    # Adjust output commands
    if hasOut:
        print "Finishing addStandardPAT(), outputCommands are:"
        print "  "+"\n  ".join(outputCommands)
        out.outputCommands = outputCommands
    else:
        del process.out

    ### Construct the sequences
    sequence *= process.patDefaultSequence
    return sequence

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPlainPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
                doPatCalo=True, doBTagging=True, doPatTauIsoDeposits=False,
                doTauHLTMatching=True, matchingTauTrigger=None, matchingJetTrigger=None,
                doMuonHLTMatching=True,
                includePFCands=False,
                calculateEventCleaning=False):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key(outputModuleName):
        out = outdict[outputModuleName]

    outputCommands = []

    # Tau Discriminators
    process.hplusPatTauSequence = cms.Sequence()
    if doPatTaus:
        process.hplusPatTauSequence = addPFTausAndDiscriminators(process, dataVersion, doPatCalo, doHChTauDiscriminators)

    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    sequence = cms.Sequence(
        process.hplusPatTauSequence
    )

    process.plainPatEndSequence = cms.Sequence()

    # Restrict input to AOD
    restrictInputToAOD(process, ["All"])

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    # This also adds the L2L3Residual JEC correction to the process.patJetCorrFactors
    if dataVersion.isData():
        o = []
        if out != None:
            o = [outputModuleName]
        runOnData(process, outputModules=o)

    # Tracks (mainly needed for muon efficiency tag&probe studies
    process.generalTracks20eta2p5 = cms.EDFilter(
        "TrackSelector",
        src = cms.InputTag("generalTracks"),
        cut = cms.string("pt > 20 && abs(eta) < 2.5"),
        filter = cms.bool(False)
    )
    sequence *= process.generalTracks20eta2p5
    outputCommands.append("keep *_generalTracks20eta2p5_*_*")

    # PF particle selectors
    addSelectedPFlowParticle(process, sequence)
    addPFCandidatePtSums(process, process.plainPatEndSequence)
    outputCommands.append("keep double_pf*SumPt_*_*")

    # Jets
    # Produce kt6 rho for L1Fastjet
    process.load('RecoJets.Configuration.RecoPFJets_cff')
    process.kt6PFJets.doRhoFastjet = True
    process.ak5PFJets.doAreaFastjet = True
    process.ak5PFJetSequence = cms.Sequence(process.kt6PFJets * process.ak5PFJets)

    # Calculate kt6 rho, maybe only neutrals and PU particles make sense?
    for particle in ["AllNeutralHadrons", "AllPhotons", "AllNeutralHadronsAndPhotons",
#                     "AllChargedHadrons", "AllChargedParticles",
                     "PileUpAllChargedParticles",
#                     "AllChargedHadronsNoChs", "AllChargedParticlesNoChs"
                     ]:
        m = process.kt6PFJets.clone(
            src = "pf"+particle
        )
        setattr(process, "kt6PFJets"+particle, m)
        process.plainPatEndSequence *= m
        outputCommands.append("keep *_kt6PFJets%s_rho_*" % particle)

    # Produce Type 2 MET correction from unclustered PFCandidates
    process.pfCandsNotInJet = pfNoJet.pfNoJet.clone(
        topCollection = cms.InputTag("ak5PFJets"),
        bottomCollection = cms.InputTag("particleFlow")
    )
    process.pfCandMETcorr = cms.EDProducer("PFCandMETcorrInputProducer",
        src = cms.InputTag('pfCandsNotInJet')
    )
    process.plainPatEndSequence *= (process.pfCandsNotInJet*process.pfCandMETcorr)
    outputCommands.append("keep *_pfCandMETcorr_*_*")

    # Set defaults
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    setPatJetDefaults(process.patJets)
    setPatJetCorrDefaults(process.patJetCorrFactors, dataVersion)
    process.patDefaultSequence.replace(process.patJetCorrFactors,
                                       process.ak5PFJetSequence*process.patJetCorrFactors)
    process.selectedPatJets.cut = jetPreSelection

    # The default JEC to be embedded to pat::Jets are L2Relative,
    # L3Absolute, L5Flavor and L7Parton. The default JEC to be applied
    # is L2L3Residual, or L3Absolute, or Uncorrected (in this order).

    betaPrototype = cms.EDProducer("HPlusPATJetViewBetaEmbedder",
        jetSrc = cms.InputTag("patJetsAK5PF"),
        vertexSrc = cms.InputTag("offlinePrimaryVertices"),
        generalTracksSrc = cms.InputTag("generalTracks"),
        embedPrefix = cms.string("")
    )

    if doPatCalo:
        # Add JPT jets
        # FIXME: Disabled for now until the JEC for JPT works again (with the latest JEC)
#        addJetCollection(process, cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
#                         'AK5', 'JPT',
#                         doJTA        = True,
#                         doBTagging   = doBTagging,
#                         jetCorrLabel = ('AK5JPT', process.patJetCorrFactors.levels),
#                         doType1MET   = False,
#                         doL1Cleaning = False,
#                         doL1Counters = True,
#                         genJetCollection = cms.InputTag("ak5GenJets"),
#                         doJetID      = True
#        )
    
        # Add PF jets
        addJetCollection(process, cms.InputTag('ak5PFJets'),
                         'AK5', 'PF',
                         doJTA        = True,
                         doBTagging   = doBTagging,
                         jetCorrLabel = ('AK5PF', process.patJetCorrFactors.levels),
                         doType1MET   = False,
                         doL1Cleaning = False,
                         doL1Counters = True,
                         genJetCollection = cms.InputTag("ak5GenJets"),
                         doJetID      = True
        )
        setPatJetCorrDefaults(process.patJetCorrFactorsAK5PF, dataVersion, True)
        process.patJetsAK5PFBetaEmbedded = betaPrototype.clone()
        process.selectedPatJetsAK5PF.src = "patJetsAK5PFBetaEmbedded"
        process.patDefaultSequence.replace(process.selectedPatJetsAK5PF,
                                           process.patJetsAK5PFBetaEmbedded*process.selectedPatJetsAK5PF)

    else:
        setPatJetCorrDefaults(process.patJetCorrFactors, dataVersion, True)
        switchJetCollection(process, cms.InputTag('ak5PFJets'),
                            doJTA        = True,
                            doBTagging   = doBTagging,
                            jetCorrLabel = ('AK5PF', process.patJetCorrFactors.levels),
                            doType1MET   = False,
                            genJetCollection = cms.InputTag("ak5GenJets"),
                            doJetID      = True
        )
    
    outputCommands.extend([
            "keep *_selectedPatJets_*_*",
            "keep *_selectedPatJetsAK5JPT_*_*",
            "keep *_selectedPatJetsAK5PF_*_*",
            'drop *_selectedPatJets_pfCandidates_*', ## drop for default patJets which are CaloJets
            'drop *_*PF_caloTowers_*',
            'drop *_*JPT_pfCandidates_*',
            'drop *_*Calo_pfCandidates_*',
            ])

    # Taus

    # Set default PATTauProducer options here, they should be
    # replicated to all added tau collections (and the first call to
    # addTauCollection should replace the default producer modified
    # here)
    setPatTauDefaults(process.patTaus, includePFCands)
    process.selectedPatTaus.cut = tauPreSelection

    if doPatTaus:
        if doHChTauDiscriminators:
            addHChTauDiscriminators()

        # Don't enable TCTau nor shrinking cone tau
        # if doPatCalo:
        #     tauTools.addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
        #                      algoLabel = "caloReco",
        #                      typeLabel = "Tau")
        #     setPatTauDefaults(process.patTausCaloRecoTau, True)
        #     process.patTausCaloRecoTau.embedLeadTrack = not includePFCands
        #     process.patTausCaloRecoTau.embedLeadPFChargedHadrCand = False
    
        # tauTools.addTauCollection(process,cms.InputTag('shrinkingConePFTauProducer'),
        #                  algoLabel = "shrinkingCone",
        #                  typeLabel = "PFTau")
        # # Disable isoDeposits like this until the problem with doPFIsoDeposits is fixed 
        # if not doPatTauIsoDeposits:
        #     process.patTausShrinkingConePFTau.isoDeposits = cms.PSet()

        tauTools.addTauCollection(process,cms.InputTag('hpsPFTauProducer'),
                         algoLabel = "hps",
                         typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsPFTau.isoDeposits = cms.PSet()
        # Continous isolation
        addTauRawDiscriminators(process.patTausHpsPFTau)
        addPatTauIsolationEmbedding(process, process.patDefaultSequence, "HpsPFTau")

        tauTools.addTauCollection(process,cms.InputTag('hpsTancTaus'),
                                  algoLabel = "hpsTanc",
                                  typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsTancPFTau.isoDeposits = cms.PSet()
        # Disable discriminators which are not in AOD
#        del process.patTausHpsTancPFTau.tauIDSources.againstCaloMuon
#        del process.patTausHpsTancPFTau.tauIDSources.byHPSvloose
        addPatTauIsolationEmbedding(process, process.patDefaultSequence, "HpsTancPFTau")

        # Add visible taus    
        if dataVersion.isMC():
            process.VisibleTaus = cms.EDProducer("HLTTauMCProducer",
                GenParticles  = cms.untracked.InputTag("genParticles"),
                ptMinTau      = cms.untracked.double(3),
                ptMinMuon     = cms.untracked.double(3),
                ptMinElectron = cms.untracked.double(3),
                BosonID       = cms.untracked.vint32(23),
                EtaMax         = cms.untracked.double(2.5)
            )
            sequence *= process.VisibleTaus
            outputCommands.append("keep *_VisibleTaus_*_*")

    else:
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Taus"], outputInProcess= out != None)
        process.patDefaultSequence.remove(process.patTaus)
        process.patDefaultSequence.remove(process.selectedPatTaus)

    outputCommands.extend(["drop *_selectedPatTaus_*_*",
#                           "keep *_selectedPatTausCaloRecoTau_*_*",
#                           "keep *_selectedPatTausShrinkingConePFTau_*_*",
                           "keep *_selectedPatTausHpsPFTau_*_*",
                           "keep *_selectedPatTausHpsTancPFTau_*_*",
                           #"keep *_cleanPatTaus_*_*",
                           #"drop *_cleanPatTaus_*_*",
                           #"keep *_patTaus*_*_*",
                           #"keep *_patPFTauProducerFixedCone_*_*",
                           # keep these until the embedding problem with pat::Tau is fixed
                           #"keep recoPFCandidates_particleFlow_*_*",
                           #"keep recoTracks_generalTracks_*_*"
                           ])

    # MET
    addPfMET(process, 'PF')
    if doPatCalo:
        addTcMET(process, 'TC')
    else:
        # FIXME: This is broken at the moment...
        #removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)
        #process.patDefaultSequen
        process.patDefaultSequence.remove(process.patMETCorrections)
        process.patDefaultSequence.remove(process.patMETs)
        del process.patMETCorrections
        del process.patMETs

    outputCommands.extend([
            "keep *_patMETs_*_*",
            "keep *_patMETsTC_*_*",
            "keep *_patMETsPF_*_*",
            "keep *_genMetTrue_*_*",
            ])

    # Muons
    setPatLeptonDefaults(process.patMuons, includePFCands)
    addPFMuonIsolation(process, process.patMuons)
    process.muonIsolationEmbeddingSequence = cms.Sequence()
    muons = tauEmbeddingCustomisations.addMuonIsolationEmbedding(process, process.muonIsolationEmbeddingSequence, "patMuons")
    process.patDefaultSequence.replace(process.selectedPatMuons,
                                       process.muonIsolationEmbeddingSequence*process.selectedPatMuons)
    process.selectedPatMuons.src = muons

    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Cosmic_ID
    process.cosmicCompatibility = cms.EDProducer("HPlusCosmicID",
        src=cms.InputTag("muons", "cosmicsVeto"),
        result = cms.string("cosmicCompatibility")
    )
    process.timeCompatibility = process.cosmicCompatibility.clone(result = 'timeCompatibility')
    process.backToBackCompatibility = process.cosmicCompatibility.clone(result = 'backToBackCompatibility')
    process.overlapCompatibility = process.cosmicCompatibility.clone(result = 'overlapCompatibility')
    sequence *= (
        process.cosmicCompatibility *
        process.timeCompatibility *
        process.backToBackCompatibility *
        process.overlapCompatibility
    )
    for name in ["cosmicCompatibility", 'timeCompatibility','backToBackCompatibility','overlapCompatibility']:
        setattr(process.patMuons.userData.userFloats, name, cms.InputTag(name))

    outputCommands.extend([
            "keep *_selectedPatMuons_*_*"
            ])

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    setPatLeptonDefaults(process.patElectrons, includePFCands)
    addPFElectronIsolation(process, process.patElectrons)

    # Electron ID, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    if doPatElectronID:
        addPatElectronID(process, process.patElectrons, process.patDefaultSequence)

    outputCommands.extend([
            "keep *_selectedPatElectrons_*_*"
            ])

    # Photons
#    process.patPhotons.embedGenMatch = False
    outputCommands.extend([
            "keep *_selectedPatPhotons_*_*"
            ])

    # Trigger
    if doPatTrigger:
        outMod= ''
        if out != None:
            outMod  = 'out'
        switchOnTrigger(process, hltProcess=dataVersion.getTriggerProcess(), outputModule=outMod)
        process.patTrigger.addL1Algos = cms.bool(False)
        process.patTrigger.l1ExtraMu = cms.InputTag("l1extraParticles")
        process.patTrigger.l1ExtraCenJet = cms.InputTag("l1extraParticles", "Central")
        process.patTrigger.l1ExtraTauJet = cms.InputTag("l1extraParticles", "Tau")
        process.patTrigger.l1ExtraForJet = cms.InputTag("l1extraParticles", "Forward")
        process.patTrigger.l1ExtraETM = cms.InputTag("l1extraParticles", "MET")
        process.patTrigger.l1ExtraHTM = cms.InputTag("l1extraParticles", "MHT")
        # This is the only way for now to reduce the size of PAT trigger objects
        # And yes, there is a typo in the parameter name
        process.patTrigger.exludeCollections = cms.vstring(
            "hltAntiKT5*",
            "hltBLifetime*",
            "hltBSoft*",
            "hltCleanEle*",
            "hltHITIPT*",
            "hltIsolPixelTrack*",
            "hltJet*",
            "hltL1HLTDouble*",
            "hltL1IsoRecoEcal*",
            "hltL1NonIsoRecoEcal*",
            #"hltL2Muon*",
            #"hltL3Muon*",
            #"hltMuTrack*",
            "hltPixel*",
            "hltRecoEcal*",
        )


        # Keep StandAlone trigger objects for enabling trigger
        # matching in the analysis phase with PAT tools
        outputCommands.extend(patTriggerStandAloneEventContent)
        outputCommands.extend([
                "keep patTriggerAlgorithms_patTrigger_*_*", # for L1
                "keep patTriggerConditions_patTrigger_*_*",
                ])

    # Remove cleaning step and set the event content
    if out == None:
        myRemoveCleaning(process)
    else:
        backup = out.outputCommands[:]
        myRemoveCleaning(process)
#        backup_pat = out.outputCommands[:]

        # Remove PFParticles here, they are explicitly included when needed
#        backup_pat = filter(lambda n: "selectedPatPFParticles" not in n, backup_pat)

        out.outputCommands = backup
#        out.outputCommands.extend(backup_pat)
        out.outputCommands.extend(outputCommands)

    # Build sequence
    sequence *= process.patDefaultSequence

    if calculateEventCleaning:
        # Event cleaning steps which require pat objects
        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
        process.load('SandBox.Skims.trackingFailureFilter_cfi')
        process.trackingFailureFilter.taggingMode = True
        process.trackingFailureFilter.JetSource = "selectedPatJetsAK5PF"
        process.trackingFailureFilter.VertexSource = "goodPrimaryVertices"
        sequence *= process.trackingFailureFilter

    # Tau+HLT matching
    if doTauHLTMatching:
        sequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger, outputCommands=outputCommands)
    # Muon+HLT matching
    if doMuonHLTMatching:
        (process.muonTriggerMatchingSequence, muonsWithTrigger) = HChTriggerMatching.addMuonTriggerMatching(process, muons=process.selectedPatMuons.src.value())
        process.selectedPatMuons.src = muonsWithTrigger
        process.patDefaultSequence.remove(process.selectedPatMuons)
        process.patDefaultSequence *= (
            process.muonTriggerMatchingSequence *
            process.selectedPatMuons
        )
        out.outputCommands.append("drop patTriggerObjectStandAlonesedmAssociation_*_*_*")

    # Add the end sequence (to be able to add possible skim sequence between other pat sequences and it
    sequence *= process.plainPatEndSequence

    return sequence

# Helper functions
def fixFlightPath(process, prefix, postfix=""):
    from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import PFTauQualityCuts
    getattr(process, prefix+"DiscriminationByFlightPathSignificance"+postfix).qualityCuts = PFTauQualityCuts

def addPatTauIsolationEmbedding(process, sequence, name):
    import RecoTauTag.Configuration.RecoPFTauTag_cff as RecoPFTauTag

    prevName = "patTaus"+name
    for iso in ["Tight", "Medium", "Loose", "VLoose"]:
        module = cms.EDProducer("HPlusPATTauViewIsolationEmbedder",
            candSrc = cms.InputTag(prevName),
            primaryVertexSrc = cms.InputTag("offlinePrimaryVertices"),
            embedPrefix = cms.string("by"+iso)
        )
        module.qualityCuts = getattr(RecoPFTauTag, "hpsPFTauDiscriminationBy%sIsolation"%iso).qualityCuts.clone()

        newName = "patTaus%sWith%sEmbedded" % (name, iso)
        setattr(process, newName, module)

        prevModule = getattr(process, prevName)
        sequence.replace(prevModule, prevModule*module)
        prevName = newName

    getattr(process, "selectedPatTaus"+name).src = prevName

def addPFTausAndDiscriminators(process, dataVersion, doCalo, doDiscriminators):
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")

    if doDiscriminators:
        # Do these imports here in order to be able to run PAT with
        # doPatTaus=False with 3_9_7 without extra tags
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["hpsPFTau", "hpsTancTaus"]
        # to synchronize with addPF2PAT
        #if not hasattr(process, "hpsPFTauDiscriminationForChargedHiggsByLeadingTrackPtCut"):
        #    tauAlgos.append("hpsPFTau")

        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos)
        PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos)

        HChCaloTauDiscriminators.addCaloTauDiscriminationSequenceForChargedHiggs(process)
        HChCaloTauDiscriminatorsCont.addCaloTauDiscriminationSequenceForChargedHiggsCont(process)

        # Tau bugfixes
        # The quality PSet is missing
        for tauAlgo in ["caloRecoTau"]+tauAlgos:
            fixFlightPath(process, tauAlgo)
            fixFlightPath(process, tauAlgo, "Cont")


    # These are already in 36X AOD, se remove them from the tautagging
    # sequence
    process.tautagging.remove(process.jptRecoTauProducer)
    process.tautagging.remove(process.caloRecoTauProducer)
    process.tautagging.remove(process.caloRecoTauDiscriminationAgainstElectron)
    process.tautagging.remove(process.caloRecoTauDiscriminationByIsolation)
    process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackFinding)
    process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackPtCut)


    process.hplusHpsTancTauSequence = cms.Sequence()
    sequence = cms.Sequence()

    if doCalo:
        sequence *= process.tautagging

    sequence *= process.PFTau

    if doDiscriminators:
        if doCalo:
            sequence *= (
                process.CaloTauDiscriminationSequenceForChargedHiggs *
                process.CaloTauDiscriminationSequenceForChargedHiggsCont
            )
        sequence *= (
            process.PFTauDiscriminationSequenceForChargedHiggs *
            process.PFTauDiscriminationSequenceForChargedHiggsCont *
            process.PFTauTestDiscriminationSequence
        )

    return sequence

def setPatJetDefaults(module):
    module.addJetID = True
    module.embedCaloTowers = False
    module.embedPFCandidates = False
    module.addTagInfos = False

def patJetCorrLevels(dataVersion, L1FastJet=False):
    levels = []
    if L1FastJet:
        levels.append("L1FastJet")
    else:
        levels.append("L1Offset")
    levels.extend(["L2Relative", "L3Absolute"])
    if dataVersion.isData():
        levels.append("L2L3Residual")
# FIXME: these are not availabel at the moment in 53X
#    levels.extend(["L5Flavor", "L7Parton"])
    return levels

def setPatJetCorrDefaults(module, dataVersion, L1FastJet=False):
    module.levels = cms.vstring(patJetCorrLevels(dataVersion, L1FastJet))
    module.useRho = L1FastJet

def setPatTauDefaults(module, includePFCands):
    attrs = [
        "embedLeadTrack",
        "embedLeadPFCand",
        "embedLeadPFChargedHadrCand",
        "embedLeadPFNeutralCand",
#        "embedSignalPFCands",
#        "embedSignalPFChargedHadrCands",
#        "embedSignalPFNeutralHadrCands",
#        "embedSignalPFGammaCands",
#        "embedIsolationPFCands",
#        "embedIsolationPFChargedHadrCands",
#        "embedIsolationPFNeutralHadrCands",
#        "embedIsolationPFGammaCands",
        ]

    value = not includePFCands
    for a in attrs:
        setattr(module, a, value)
#    module.embedGenMatch = False


def addHChTauDiscriminators():
    if HChPFTauDiscriminators.HChTauIDSources[0] in tauTools.classicTauIDSources:
        print "addHChTauDiscriminators called already once, not adding them again"
        return

    for idSources in [tauTools.classicTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChPFTauDiscriminators.HChTauIDSources)
        idSources.extend(HChPFTauDiscriminatorsCont.HChTauIDSourcesCont)
    for idSources in [tauTools.classicPFTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(PFTauTestDiscrimination.TestTauIDSources)

def addHChTauDiscriminatorsPF2PAT(process, module, postfix):
    sequence = cms.Sequence()
    
    tauAlgos = ["pfTaus"+postfix]
    sequence *= HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos, postfix)
    sequence *= HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos, postfix)
    sequence *= PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos, postfix)

    for idSources in [HChPFTauDiscriminators.HChTauIDSources,
                      HChPFTauDiscriminatorsCont.HChTauIDSourcesCont,
                      PFTauTestDiscrimination.TestTauIDSources]:
        for label, tag in idSources:
            setattr(module.tauIDSources, label, cms.InputTag("pfTaus"+postfix+tag+postfix))

    return sequence

def addTauRawDiscriminators(module, postfix=""):
    module.tauIDSources.byRawCombinedIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr"+postfix)
    module.tauIDSources.byRawChargedIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorr"+postfix)
    module.tauIDSources.byRawGammaIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorr"+postfix)


def setPatLeptonDefaults(module, includePFCands):
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    module.usePV = False
    module.embedTrack = not includePFCands
#    module.embedGenMatch = False

def addPatElectronIDProducers(process, sequence):
    # Simple cut-based ElectronID seems to work as simply as this
    # Note that this is OLD
    # https://twiki.cern.ch/twiki/bin/view/CMS/VbtfEleID2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    process.load("ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff")
    sequence *= process.simpleEleIdSequence

    # MVA ID, should be up-to-date
    # https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification
    # Note that this requires that the CVS tags in
    # test/pattuple/checkoutTags.sh are checked out
    process.load("EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi")
    sequence *= (process.mvaTrigV0 + process.mvaNonTrigV0)
    

def addPatElectronID(process, module):
    # Simple cut-based electron ID (old)
    module.electronIDSources.simpleEleId95relIso = cms.InputTag("simpleEleId95relIso")
    module.electronIDSources.simpleEleId90relIso = cms.InputTag("simpleEleId90relIso")
    module.electronIDSources.simpleEleId85relIso = cms.InputTag("simpleEleId85relIso")
    module.electronIDSources.simpleEleId80relIso = cms.InputTag("simpleEleId80relIso")
    module.electronIDSources.simpleEleId70relIso = cms.InputTag("simpleEleId70relIso")
    module.electronIDSources.simpleEleId60relIso = cms.InputTag("simpleEleId60relIso")
    module.electronIDSources.simpleEleId95cIso = cms.InputTag("simpleEleId95cIso")
    module.electronIDSources.simpleEleId90cIso = cms.InputTag("simpleEleId90cIso")
    module.electronIDSources.simpleEleId85cIso = cms.InputTag("simpleEleId85cIso")
    module.electronIDSources.simpleEleId80cIso = cms.InputTag("simpleEleId80cIso")
    module.electronIDSources.simpleEleId70cIso = cms.InputTag("simpleEleId70cIso")
    module.electronIDSources.simpleEleId60cIso = cms.InputTag("simpleEleId60cIso")

    # MVA ID
    module.electronIDSources.mvaTrigV0 = cms.InputTag("mvaTrigV0")
    module.electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")


def addPatTrigger(process, dataVersion, sequence):
    switchOnTrigger(process, hltProcess=dataVersion.getTriggerProcess(), outputModule="")
    process.patTrigger.addL1Algos = cms.bool(False)
    process.patTrigger.l1ExtraMu = cms.InputTag("l1extraParticles")
    process.patTrigger.l1ExtraCenJet = cms.InputTag("l1extraParticles", "Central")
    process.patTrigger.l1ExtraTauJet = cms.InputTag("l1extraParticles", "Tau")
    process.patTrigger.l1ExtraForJet = cms.InputTag("l1extraParticles", "Forward")
    process.patTrigger.l1ExtraETM = cms.InputTag("l1extraParticles", "MET")
    process.patTrigger.l1ExtraHTM = cms.InputTag("l1extraParticles", "MHT")
    # This is the only way for now to reduce the size of PAT trigger objects
    # And yes, there is a typo in the parameter name
    process.patTrigger.exludeCollections = cms.vstring(
#        "hltAntiKT5*",
 #       "hltBLifetime*",
 #       "hltBSoft*",
        "hltCleanEle*",
        "hltHITIPT*",
        "hltIsolPixelTrack*",
#        "hltJet*",
        "hltL1HLTDouble*",
        "hltL1IsoRecoEcal*",
        "hltL1NonIsoRecoEcal*",
        #"hltL2Muon*",
        #"hltL3Muon*",
        #"hltMuTrack*",
        "hltPixel*",
        "hltRecoEcal*",
        "hltEle*",
        "hltGetJetsfrom*",
        "hltMuTrackJpsi*",
        # After 53X
        "hltDeDxFilter*",
        "hltPFHT*",
        "hltMu17B*",
        "hltPFDisplacedJets*",
    )
    # Disable exludeCollections for now
    # https://hypernews.cern.ch/HyperNews/CMS/get/physTools/2955.html
    process.patTrigger.exludeCollections = cms.vstring()


    # Keep StandAlone trigger objects for enabling trigger
    # matching in the analysis phase with PAT tools
    outputCommands = [
        "keep patTriggerAlgorithms_patTrigger_*_*", # for L1
        "keep patTriggerConditions_patTrigger_*_*",
        "keep patTriggerPaths_patTrigger_*_*",
        "keep patTriggerObjects_patTrigger_*_*",
        "keep patTriggerFilters_patTrigger_*_*",
        "keep patTriggerEvent_patTriggerEvent_*_*",
        "drop patTriggerObjectStandAlones_patTrigger_*_*",
    ]

    sequence *= process.patDefaultSequenceTrigger
    sequence *= process.patDefaultSequenceTriggerEvent

    return outputCommands    


##################################################
#
# PF2PAT
#
class PF2PATBuilder(PATBuilderBase):
    def __init__(self, *args, **kwargs):
        raise Exception("At least the outputCommand changes must be migrated from StandardPATBuilder")
        PATBuilderBase.__init__(self, *args, **kwargs)
        # Add PF2PAT with PAT tools
        self._buildPF2PAT(self.postfix, chs)

    def customize(self):
        # Customize physics objects
        self._customizeMuons(self.postfix)
        self._customizeElectrons(self.postfix)
        self._customizeJets(self.postfix)
        self._customizeTaus(self.postfix)
        self._customizeMET(self.postfix)

        self._customizeEventCleaning(self.postfix)

        # Remove unclustered PFParticles
        self.outputCommands.append("drop *_selectedPatPFParticles%s_*_*"%self.postfix)

        # Remove counting filters (what on earth are they for?)
        removeCounting(self.process, self.postfix)

        # Build the sequences
        setattr(self.process, "patHplusCustomBefore"+self.postfix, self.beginSequence)
        setattr(self.process, "patHplusCustomAfter"+self.postfix, self.endSequence)

        sequence = getattr(self.process, "patPF2PATSequence"+self.postfix)
        sequence.insert(0, self.beginSequence)
        sequence *= self.endSequence
        

    def _buildPF2PAT(self, postfix, chs):
        jetCorrFactors = patJetCorrLevels(self.dataVersion, L1FastJet=True)
        jetCorrPayload = "AK5PF"
        if chs:
            jetCorrPayload += "chs"
        pfTools.usePF2PAT(self.process, runPF2PAT=True, jetAlgo="AK5", jetCorrections=(jetCorrPayload, jetCorrFactors),
                          runOnMC=self.dataVersion.isMC(), postfix=postfix)
        self.outputCommands.extend([
#        "keep *_selectedPatPhotons%s_*_*" % postfix, # isolated photons are not (yet?) produced as part of PF2PAT
        'keep *_selectedPatElectrons%s_*_*' % postfix, 
        'keep *_selectedPatMuons%s_*_*' % postfix,
        'keep *_selectedPatJets%s*_*_*' % postfix,
        'keep *_selectedPatTaus%s_*_*' % postfix,
        'keep *_selectedPatPFParticles%s_*_*' % postfix,
        'keep *_selectedPatJets%s_pfCandidates_*' % postfix,
        'drop *_selectedPatJets%s_caloTowers_*' % postfix,
        'drop *_*JPT_pfCandidates_*',
        'drop *_*Calo_pfCandidates_*',
        'keep *_patMETs%s_*_*' % postfix,
        ])

        # Enable/disable CHS
        getattr(self.process, "pfPileUp"+postfix).Enable = chs
        # According to JEC recipe (redundant for this non-CHS case, but
        # hopefully this confuses less)
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCorPFnoPU
        # There is a separate pfPileUpIso+postfix whith has this True for lepton isolation
        getattr(self.process, "pfPileUp"+postfix).checkClosestZVertex = False


    def _customizeMuons(self, postfix):
        # isolation step in PF2PAT, default is 0.15 (deltabeta corrected)
        #getattr(process, "pfIsolatedMuons"+postfix).isolationCut = 0.15
    
        # First for isolated muons (PF2PAT default)
        self._customizeMuons2(postfix)

        # Then, for all muons (needed for muon isolation studies for embedding)
        allPostfix = "All"
        if self.dataVersion.isMC():
            # For MC, clone the makePatMuons sequence
            makePatMuonsAll = patHelpers.cloneProcessingSnippet(self.process, getattr(self.process, "makePatMuons"+postfix), allPostfix)
            makePatMuons = getattr(self.process, "makePatMuons"+postfix)
            getattr(self.process, "patDefaultSequence"+postfix).replace(makePatMuons,
                                                                        makePatMuons * makePatMuonsAll)
            # Set the InputTags to point to pfMuons (all PF muons) instead of pfIsolatedMuons (after isolation)
            getattr(self.process, "muonMatch"+postfix+allPostfix).src = "pfMuons"+postfix
            getattr(self.process, "patMuons"+postfix+allPostfix).pfMuonSource = "pfMuons"+postfix
        else:
            # For data, clone just patMuons, as muonMatch and hence makePatMuons don't exist
            patMuons = getattr(self.process, "patMuons"+postfix)
            patMuonsAll = patMuons.clone(
                pfMuonSource = "pfMuons"+postfix
            )
            setattr(self.process, "patMuons"+postfix+allPostfix, patMuonsAll)
            getattr(self.process, "patDefaultSequence"+postfix).replace(patMuons, patMuons*patMuonsAll)

        # Clone selectedPatMuons
        selectedPatMuons = getattr(self.process, "selectedPatMuons"+postfix)
        selectedPatMuonsAll = selectedPatMuons.clone(
            src = "patMuons"+postfix+allPostfix
        )
        setattr(self.process, "selectedPatMuons"+postfix+allPostfix, selectedPatMuonsAll)
        getattr(self.process, "patDefaultSequence"+postfix).replace(selectedPatMuons,
                                                                    selectedPatMuons*selectedPatMuonsAll)
        self._customizeMuons2(postfix, allPostfix)

    def _customizeMuons2(self, postfix, postfixMuon=""):
        # Set default lepton options
        setPatLeptonDefaults(getattr(self.process, "patMuons"+postfix+postfixMuon), self.includePFCands)
        # Embed tau-embedding-like isolation variables to pat::Muons
        isoSeq = cms.Sequence()
        setattr(self.process, "muonIsolationEmbeddingSequence"+postfix+postfixMuon, isoSeq)
        muons = tauEmbeddingCustomisations.addMuonIsolationEmbedding(self.process, isoSeq, "patMuons"+postfix+postfixMuon, postfix=postfix+postfixMuon)
        getattr(self.process, "patDefaultSequence"+postfix).replace(
            getattr(self.process, "selectedPatMuons"+postfix+postfixMuon),
            isoSeq * getattr(self.process, "selectedPatMuons"+postfix+postfixMuon))
        getattr(self.process, "selectedPatMuons"+postfix+postfixMuon).src = muons

        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Cosmic_ID
        proto = cms.EDProducer("HPlusCosmicID",
            src=cms.InputTag("muons", "cosmicsVeto"),
            result = cms.string("cosmicCompatibility")
        )
        for name in ["cosmicCompatibility", 'timeCompatibility','backToBackCompatibility','overlapCompatibility']:
            m = proto.clone(result=name)
            self.beginSequence *= m
            setattr(self.process, name+postfix+postfixMuon, m)
            getattr(self.process, "patMuons"+postfix+postfixMuon).userData.userFloats.src.append(cms.InputTag(name+postfix+postfixMuon))
    
        # HLT Matching
        if self.doMuonHLTMatching:
            (muHltSequence, muonsWithTrigger) = HChTriggerMatching.addMuonTriggerMatching(self.process, muons=getattr(self.process, "selectedPatMuons"+postfix+postfixMuon).src.value(), postfix=postfix+postfixMuon)
            setattr(self.process, "muonTriggerMatchingSequence"+postfix+postfixMuon, muHltSequence)
            getattr(self.process, "selectedPatMuons"+postfix+postfixMuon).src = muonsWithTrigger
            getattr(self.process, "patDefaultSequence"+postfix).remove(getattr(self.process, "selectedPatMuons"+postfix+postfixMuon))
            seqTmp = getattr(self.process, "patDefaultSequence"+postfix) 
            seqTmp *= (
                muHltSequence *
                getattr(self.process, "selectedPatMuons"+postfix+postfixMuon)
            )
            self.outputCommands.append("drop patTriggerObjectStandAlonesedmAssociation_*_*_*")

        self.outputCommands.append("keep *_selectedPatMuons%s%s_*_*" % (postfix, postfixMuon))

    def _customizeElectrons(self, postfix):
        # isolation step in PF2PAT, default is 0.2 (deltabeta corrected)
        #getattr(process, "pfIsolatedElectrons"+postfix).isolationCut = 0.2

        # First, for isolated electrons (PF2PAT default) 
        # Simple cut-based ElectronID  seems to work as simply as this
        if self.doPatElectronID:
            addPatElectronID(self.process, getattr(self.process, "patElectrons"+postfix)) # FIXME replace this with a producer that produces user ints of latest recommended PF isolations
        # FIXME Add also GSF electrons!

        # Then, for all electrons (not necessarily needed, but let's keep them when we're still studying the PU effects)
        allPostfix = "All"
        if self.dataVersion.isMC():
            # For MC, clone the makePatElectrons sequence
            makePatElectronsAll = patHelpers.cloneProcessingSnippet(self.process, getattr(self.process, "makePatElectrons"+postfix), allPostfix)
            makePatElectrons = getattr(self.process, "makePatElectrons"+postfix)
            getattr(self.process, "patDefaultSequence"+postfix).replace(makePatElectrons,
                                                                        makePatElectrons * makePatElectronsAll)
            # Set the InputTags to point to pfElectrons (all PF electrons) instead of pfIsolatedElectrons (after isolation)
            getattr(self.process, "patElectrons"+postfix+allPostfix).pfElectronSource = "pfElectrons"+postfix
        else:
            # For data, clone just patElectrons, as electronMatch and makePatElectrons don't exist
            patElectrons = getattr(self.process, "patElectrons"+postfix)
            patElectronsAll = patElectrons.clone(
                pfElectronSource = "pfElectrons"+postfix
            )
            setattr(self.process, "patElectrons"+postfix+allPostfix, patElectronsAll)
            getattr(self.process, "patDefaultSequence"+postfix).replace(patElectrons, patElectrons*patElectronsAll)

        # Clone selectedPatElectrons
        selectedPatElectrons = getattr(self.process, "selectedPatElectrons"+postfix)
        selectedPatElectronsAll = selectedPatElectrons.clone(
            src = "patElectrons"+postfix+allPostfix
        )
        setattr(self.process, "selectedPatElectrons"+postfix+allPostfix, selectedPatElectronsAll)
        getattr(self.process, "patDefaultSequence"+postfix).replace(selectedPatElectrons,
                                                                    selectedPatElectrons*selectedPatElectronsAll)
        # Add the elecron Id
#        addPatElectronID(self.process, getattr(self.process, "patElectrons"+postfix+allPostfix))
        self.outputCommands.append("keep *_selectedPatElectrons%s%s_*_*" % (postfix, allPostfix))

#        getattr(self.process, "patElectrons"+postfix+allPostfix).isoDeposits = cms.PSet()
#        getattr(self.process, "patElectrons"+postfix+allPostfix).isolationValues = cms.PSet()
#        getattr(self.process, "patElectrons"+postfix+allPostfix).electronIDSources = cms.PSet()
#        getattr(self.process, "patElectrons"+postfix+allPostfix).addElectronID = False
#        getattr(self.process, "patElectrons"+postfix+allPostfix).addGenMatch = False


    def _customizeJets(self, postfix):
        # Take all jets (we clean jets from tau later in the analysis)
        getattr(self.process, "pfNoTau"+postfix).enable = False
    
        # Don't embed PFCandidates
        setPatJetDefaults(getattr(self.process, "patJets"+postfix))
    
        # Calculate rho-neutral
        for particle in ["AllNeutralHadrons"]:
            m = getattr(self.process, "kt6PFJets"+postfix).clone(
                src = "pf"+particle+postfix
            )
            name = "kt6PFJets"+particle+postfix
            setattr(self.process, name, m)
            self.endSequence *= m
            self.outputCommands.append("keep *_%s_rho_*" % name)
    
        # Embed beta and betastar to pat::Jet
        betaPrototype = cms.EDProducer("HPlusPATJetViewBetaEmbedder",
            jetSrc = cms.InputTag("patJets"+postfix),
            generalTracksSrc = cms.InputTag("generalTracks"),
            vertexSrc = cms.InputTag("offlinePrimaryVertices"),
            embedPrefix = cms.string("")
        )
        m = betaPrototype.clone()
        name = "patJetsBetaEmbedded"+postfix
        setattr(self.process, name, m)
        getattr(self.process, "selectedPatJets"+postfix).src = name
        getattr(self.process, "patDefaultSequence"+postfix).replace(
            getattr(self.process, "selectedPatJets"+postfix),
            m * getattr(self.process, "selectedPatJets"+postfix)
        )
    
        # jet pre-selection
        getattr(self.process, "selectedPatJets"+postfix).cut = jetPreSelection

    def _customizeTaus(self, postfix):
        # Switch to HPS taus
        pfTools.adaptPFTaus(self.process, "hpsPFTau", postfix=postfix)
        # Disable the default PFTau selection in PF2PAT (byDecayMode + loose isolation)
        getattr(self.process, "pfTaus"+postfix).discriminators = []
    
        # Remove shrinking cone discrimination sequence as unnecessary
        getattr(self.process, "patDefaultSequence"+postfix).remove(getattr(self.process, "patShrinkingConePFTauDiscrimination"+postfix))
    
        # Set objects to embedded to pat::Tau
        setPatTauDefaults(getattr(self.process, "patTaus"+postfix), self.includePFCands)
        getattr(self.process, "selectedPatTaus"+postfix).cut = tauPreSelection
    
        # Produce HCh discriminators (could we really reduce the number of these?), and add them to pat::Tau producer
        if self.doHChTauDiscriminators:
            seq = addHChTauDiscriminatorsPF2PAT(self.process, getattr(self.process, "patTaus"+postfix), postfix)
            setattr(self.process, "hplusPatTauSequence"+postfix, seq)
            getattr(self.process, "patDefaultSequence"+postfix).replace(
                getattr(self.process, "patTaus"+postfix),
                seq * getattr(self.process, "patTaus"+postfix)
            )
            # Fix the flight path discriminator
            fixFlightPath(self.process, "pfTaus"+postfix, postfix)
            fixFlightPath(self.process, "pfTaus"+postfix, "Cont"+postfix)
    
        # Add the continuous isolation discriminators
        addTauRawDiscriminators(getattr(self.process, "patTaus"+postfix), postfix)
    
        # Remove iso deposits to save disk space
        if not self.doPatTauIsoDeposits:
            getattr(self.process, "patTaus"+postfix).isoDeposits = cms.PSet()
    
        # Trigger matching
        if self.doTauHLTMatching:
            self.endSequence *= HChTriggerMatching.addTauHLTMatching(self.process, self.matchingTauTrigger, collections=["patTaus"+postfix], postfix=postfix, outputCommands=self.outputCommands)


    def _customizeMET(self, postfix):
        # Produce Type I MET correction from all PF jets
        # Note that further correction is needed at the analysis level
        # to remove contribution from jet energy corrections of those
        # jets which correspond isolated e/mu/tau

        if postfix != "PFlow":
            print "########################################"
            print "#"
            print "# NOT producing ES variations nor type 1/2 MET for postfix %s (but only for PFlow)" % postfix
            print "#"
            print "########################################"

            # Apparently the cloning of patDefaultSequencePFlow to any
            # other postfix clones also the metUncertaintySequence.
            # Although this might work in practice, we should test it
            # first (if we even want it), and the event content should
            # be adjusted (which is not done automatically for the
            # other postfix). For now, just disable the ES variation
            # for other postfixes.
            #getattr(self.process, "patDefaultSequence"+postfix).remove(getattr(self.process, "metUncertaintySequence"+postfix))
            #delattr(self.process, "metUncertaintySequence"+postfix)

            return

        selectedPatJets = getattr(self.process, "selectedPatJets"+postfix)
        jets = selectedPatJets.src.value()
        seq = getattr(self.process, "patDefaultSequence"+postfix)

        if self.dataVersion.isData():
            self.process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
            self.process.selectedPatJetsForMETtype1p2Corr.src = jets
            self.process.selectedPatJetsForMETtype2Corr.src = jets
            self.process.patPFMet.addGenMET = False

            seq *= self.process.producePatPFMETCorrections
            self.outputCommands.extend([
                    "keep *_patPFMet_*_*",
                    "keep *_patType1CorrectedPFMet_*_*",
                    "keep *_patType1p2CorrectedPFMet_*_*",
                    ])
            return

        # Following is for MC only

        outputModule = ""
        outdict = self.process.outputModules_()
        if outdict.has_key(outputModuleName):
            outputModule = outputModuleName
            # Reset the OutputModule outputCommands to catch the event
            # content modifications done in the runMEtUncertainties.
            # Resetting is fine since the outputCommands are saved in
            # addPF2PAT() before a call to this method, and they are
            # set to proper values after a call to this method.
            self.process.out.outputCommands = []

        # Smear the jet energies by JER data/MC difference for MC only
        metUncertaintyTools.runMEtUncertainties(self.process,
                                                electronCollection="",
                                                photonCollection="",
                                                muonCollection="",
                                                tauCollection="",
                                                jetCollection=jets,
                                                doSmearJets=self.dataVersion.isMC(),
                                                outputModule=outputModule
                                                )

        # The function call above adds metUncertaintySequence to
        # patDefaultSequence. We have to add it to patDefaultSequence PFlow manually
        seq *= self.process.metUncertaintySequence

        # Add "selected"-collections for all jets
        # "All" name "shiftedPatJetsBetaEmbeddedPFlowEnUpForCorrMEt"
        # "Selected" name "shiftedPatJetsPFlowEnUpForCorrMEt"
        tmp = jets.replace("patJets", "")
        shiftedJetNames = [ # These are the ones produced by runMEtUncertainties
            "shiftedPatJets%sEnUpForCorrMEt" % tmp,
            "shiftedPatJets%sEnDownForCorrMEt" % tmp,
            "smearedPatJets%s" % tmp,
            "smearedPatJets%sResUp" % tmp,
            "smearedPatJets%sResDown" % tmp,
            ]
        selectedJetNames = []
        for shiftedJet in shiftedJetNames:
            m = selectedPatJets.clone(
                src = shiftedJet
            )
            name = shiftedJet.replace(tmp, postfix)
            setattr(self.process, name, m)
            seq *= m
            selectedJetNames.append(name)

        if outputModule != "":
            self.outputCommands.extend(self.process.out.outputCommands)
            self.process.out.outputCommands = []


            processName = self.process.name_()
            # Drop "all" shifted/smeared jet collections in favor of
            # the "selected" collections. We don't need the
            # "ForRawMEt" energy variations.
            self.outputCommands.extend([
                    "drop *_shiftedPatJetsBetaEmbedded%sEnUpForRawMEt_*_%s" % (postfix, processName),
                    "drop *_shiftedPatJetsBetaEmbedded%sEnDownForRawMEt_*_%s" % (postfix, processName)
                    ])
            for n in shiftedJetNames:
                self.outputCommands.append("drop *_%s_*_%s" % (n, processName))
            # Keep the "selected" collections
            for n in selectedJetNames:
                self.outputCommands.append("keep *_%s_*_%s" % (n, processName))

   
    def _customizeEventCleaning(self, postfix):
        if not self.calculateEventCleaning:
            return

        # Event cleaning steps which require pat objects
        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
        from SandBox.Skims.trackingFailureFilter_cfi import trackingFailureFilter
        m = trackingFailureFilter.clone(
            taggingMode = True,
            JetSource = "selectedPatJets"+postfix,
            VertexSource = "goodPrimaryVertices",
        )
        setattr(self.process, "trackingFailureFilter"+postfix, m)
        self.endSequence *= m


def addPF2PAT(process, dataVersion, doPatTrigger=True, doChs=False, patArgs={}, pvSelectionConfig=""):
    print "########################################"
    print "#"
    print "# Using PF2PAT"
    print "#"
    print "########################################"

    # Hack to not to crash if something in PAT assumes process.out
    # hasOut = hasattr(process, outputModuleName)
    # outputCommands = []
    # outputCommandsBackup = []
    # if hasOut:
    #     outputCommandsBackup = process.out.outputCommands[:]
    # else:
    #     process.out = cms.OutputModule("PoolOutputModule",
    #         fileName = cms.untracked.string('dummy.root'),
    #         outputCommands = cms.untracked.vstring()
    #     )
    out = None
    outdict = process.outputModules_()
    outputCommands = []
    if outdict.has_key(outputModuleName):
        out = outdict[outputModuleName]
        outputCommands = out.outputCommands[:]

    sequence = cms.Sequence()

    # Visible taus
    if dataVersion.isMC():
        process.VisibleTaus = cms.EDProducer("HLTTauMCProducer",
            GenParticles  = cms.untracked.InputTag("genParticles"),
            ptMinTau      = cms.untracked.double(3),
            ptMinMuon     = cms.untracked.double(3),
            ptMinElectron = cms.untracked.double(3),
            BosonID       = cms.untracked.vint32(23),
            EtaMax         = cms.untracked.double(2.5)
        )
        sequence *= process.VisibleTaus
        outputCommands.append("keep *_VisibleTaus_*_*")

    # PAT
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    # Run simple electron ID sequence for once (default is to run it)
    if not "doPatElectronID" in patArgs or patArgs["doPatElectronID"]:
        addPatElectronIDProducers(process, sequence)

    # Note that although PF2PAT configurations are built here, they're
    # really executed after the "sequence" Sequence.
    postfixes = []
    # First build PF2PAT without CHS
    pflowBuilder = PF2PATBuilder(process, dataVersion, postfix="PFlow", **patArgs)
    postfixes.append("PFlow")

    # Then build with CHS
    if doChs:
        pflowChsBuilder = PF2PATBuilder(process, dataVersion, postfix="PFlowChs", chs=True, **patArgs)
        postfixes.append("PFlowChs")

    # Then run our customizations. Its easier to understand if the
    # customizations are run after building both PFlow and PFlowChs,
    # since the cloning of patDefaultSequence by usePF2PAT()
    # interferes with the runMEtUncertainties()
    pflowBuilder.customize()
    if doChs:
        pflowChsBuilder.customize()

    outputCommands.extend(pflowBuilder.getOutputCommands())
    if doChs:
        outputCommands.extend(pflowChsBuilder.getOutputCommands())


    # Add GSF electrons (as that is the POG recommendation)
    process.gsfPatElectronSequence = cms.Sequence()
    if dataVersion.isMC():
        process.gsfPatElectronSequence *= process.electronMatch
    process.gsfPatElectronSequence *= (
        process.patElectrons *
        process.selectedPatElectrons
    )
    addPatElectronID(process, process.patElectrons)
    outputCommands.append("keep *_selectedPatElectrons_*_*")


    ### Trigger (as the last)
    if doPatTrigger:
        outputCommands.extend(addPatTrigger(process, dataVersion, sequence))

    ### Other customisation
    # Tracks (mainly needed for muon efficiency tag&probe studies
    process.generalTracks20eta2p5 = cms.EDFilter("TrackSelector",
        src = cms.InputTag("generalTracks"),
        cut = cms.string("pt > 20 && abs(eta) < 2.5"),
        filter = cms.bool(False)
    )
    sequence *= process.generalTracks20eta2p5
    outputCommands.append("keep *_generalTracks20eta2p5_*_*")


    ### Primary vertex selection
    # Although defined here, it is run before any PF2PAT modules
    # It just has to be run after PAT trigger, in order make use of that in the PV selection code
    if len(pvSelectionConfig) > 0:
        # Reorder offlinePrimaryVertices
        module = __import__("HiggsAnalysis.HeavyChHiggsToTauNu."+pvSelectionConfig, fromlist=[pvSelectionConfig])
        process.primaryVertexSelectionSequence = module.buildSequence(process, patArgs)

        process.offlinePrimaryVertices = cms.EDProducer("HPlusVertexReorderProducer",
            vertexSrc = cms.InputTag("offlinePrimaryVertices"),
            indexSrc = cms.InputTag("selectedPrimaryVertexIndex")
        )
        process.primaryVertexSelectionSequence *= process.offlinePrimaryVertices
        outputCommands.extend([
                "drop *_offlinePrimaryVertices_*_*",
                "keep *_offlinePrimaryVertices_*_%s" % process.name_(),
                "keep *_selectedPrimaryVertexIndex_*_*",
                ])

        sequence *= process.primaryVertexSelectionSequence

    # Adjust output commands
    if out != None:
        out.outputCommands = outputCommands

    ### Construct the sequences
    for pf in postfixes:
        sequence *= getattr(process, "patPF2PATSequence"+pf)
    sequence *= process.gsfPatElectronSequence
    return sequence


### The functions below are taken from
### UserCode/PFAnalyses/VBFHTauTau/python/vbfDiTauPATTools.py
### revision 1.7

###################a#################################################
from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace

def addSelectedPFlowParticle(process, sequence, verbose=False):
    if verbose:
        print "[Info] Adding pf-particles (for pf-isolation and pf-seed pat-leptons)"

    process.load("CommonTools.ParticleFlow.pfParticleSelection_cff")
    process.pfAllElectrons.src = "pfNoPileUp" # take electrons from all no-PU candidates instead of pfNoMuon (which apparently doesn't exist without PF2PAT)
    sequence *= process.pfParticleSelectionSequence


    # Create NoChs versions of particle selections, which take the
    # input from particleFlow instead of pfNoPileUp
    process.pfSortByTypeSequenceNoChs = cms.Sequence()
    for particle in ["NeutralHadrons", "ChargedHadrons", "Photons", "ChargedParticles", "NeutralHadronsAndPhotons"]:
        m = getattr(process, "pfAll"+particle).clone()
        m.src = "particleFlow"
        setattr(process, "pfAll"+particle+"NoChs", m)
        process.pfSortByTypeSequenceNoChs *= m
    process.pfParticleSelectionSequence *= process.pfSortByTypeSequenceNoChs

def addPFCandidatePtSums(process, sequence):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")

    prototype = cms.EDProducer("HPlusCandViewSumPtComputer",
        src = cms.InputTag("")
    )
    colls = ["pfAll" + p for p in ["NeutralHadrons", "ChargedHadrons", "Photons", "ChargedParticles", "NeutralHadronsAndPhotons",
                                   "ChargedHadronsNoChs", "ChargedParticlesNoChs"
                                   ]]
    colls.append("pfPileUpAllChargedParticles")
    for collection in colls:
        m = prototype.clone(src = collection)
        setattr(process, collection+"SumPt", m)
        sequence *= m

# From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
def addPFMuonIsolation(process, module):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")

    process.load("RecoMuon.MuonIsolation.muonPFIsolation_cff")
    process.patDefaultSequence.replace(module, process.muonPFIsolationSequence*module)

    ## Iso deposits
    # Set the muon source to 'muons' from 'muons1st'
    process.muPFIsoDepositCharged.src = "muons"
    process.muPFIsoDepositChargedAll.src = "muons"
    process.muPFIsoDepositNeutral.src = "muons"
    process.muPFIsoDepositGamma.src = "muons"
    process.muPFIsoDepositPU.src = "muons"

    # Without CHS (neutral hadrons and photons are not modified by CHS)
    process.muPFIsoDepositChargedNoChs = isoDepositReplace("muons", "pfAllChargedHadronsNoChs")
    process.muPFIsoDepositChargedAllNoChs = isoDepositReplace("muons", "pfAllChargedParticlesNoChs")
    process.muonPFIsolationDepositsSequence *= (
        process.muPFIsoDepositChargedNoChs *
        process.muPFIsoDepositChargedAllNoChs
    )

    ## Iso values
    # Without CHS (neutral hadrons and photons are not modified by CHS)
    for name in ["Charged", "ChargedAll"]:
        for cone in ["03", "04"]:
            m = getattr(process, "muPFIsoValue%s%s" % (name, cone)).clone()
            m.deposits[0].src = "muPFIsoDeposit%sNoChs" % name
            setattr(process, "muPFIsoValue%sNoChs%s" % (name, cone), m)
            process.muonPFIsolationSequence *= m

    ## Add iso deposits and values to the PATMuonProducer module

    # Example from PhysicsTools/PatAlgos/python/tools/pfTools.py
    # We can't use pfTools directly, because it's only for PF2PAT, but
    # we can get the PF isolation by adding these by ourselves
    module.isoDeposits = cms.PSet(
        pfChargedHadrons   = cms.InputTag("muPFIsoDepositCharged"),
        pfChargedAll       = cms.InputTag("muPFIsoDepositChargedAll"),
        pfPUChargedHadrons = cms.InputTag("muPFIsoDepositPU"),
        pfNeutralHadrons   = cms.InputTag("muPFIsoDepositNeutral"),
        pfPhotons          = cms.InputTag("muPFIsoDepositGamma"),
        user               = cms.VInputTag(
            cms.InputTag("muPFIsoDepositChargedNoChs"),
            cms.InputTag("muPFIsoDepositChargedAllNoChs")
        )
    )

    cone = "04"
    module.isolationValues = cms.PSet(
        pfChargedHadrons   = cms.InputTag("muPFIsoValueCharged"+cone),
        pfChargedAll       = cms.InputTag("muPFIsoValueChargedAll"+cone),
        pfPUChargedHadrons = cms.InputTag("muPFIsoValuePU"+cone),
        pfNeutralHadrons   = cms.InputTag("muPFIsoValueNeutral"+cone),
        pfPhotons          = cms.InputTag("muPFIsoValueGamma"+cone),
        user               = cms.VInputTag(
            cms.InputTag("muPFIsoValueChargedNoChs"+cone),
            cms.InputTag("muPFIsoValueChargedAllNoChs"+cone)
        )
    )

def addPFElectronIsolation(process, module):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")
    
    process.load("CommonTools.ParticleFlow.Isolation.pfElectronIsolation_cff")
    process.patDefaultSequence.replace(module, process.pfElectronIsolationSequence*module)

    ## Iso deposits
    # Set the electron source to 'gsfElectrons'
    #print "process.elPFIsoDepositCharged.src =",process.elPFIsoDepositCharged.src
    electronSrc = "gsfElectrons"
    process.elPFIsoDepositCharged.src = electronSrc
    process.elPFIsoDepositChargedAll.src = electronSrc
    process.elPFIsoDepositNeutral.src = electronSrc
    process.elPFIsoDepositGamma.src = electronSrc
    process.elPFIsoDepositPU.src = electronSrc

    # Without CHS (neutral hadrons and photons are not modified by CHS)
    #print "process.elPFIsoDepositChargedNoChs =",process.elPFIsoDepositChargedNoChs.src
    process.elPFIsoDepositChargedNoChs = isoDepositReplace("gsfElectrons", "pfAllChargedHadronsNoChs")
    process.elPFIsoDepositChargedAllNoChs = isoDepositReplace("gsfElectrons", "pfAllChargedParticlesNoChs")
    process.electronPFIsolationDepositsSequence *= (
        process.elPFIsoDepositChargedNoChs *
        process.elPFIsoDepositChargedAllNoChs
    )

    ## Iso values
    # Without CHS (neutral hadrons and photons are not modified by CHS)
    for name in ["Charged", "ChargedAll"]:
        for cone in ["03", "04"]:
            m = getattr(process, "elPFIsoValue%s%s" % (name, cone)).clone()
            m.deposits[0].src = "elPFIsoDeposit%sNoChs" % name
            setattr(process, "elPFIsoValue%sNoChs%s" % (name, cone), m)
            process.pfElectronIsolationSequence *= m

    ## Add iso deposits and values to the PATElectronProducer module

    # Example from PhysicsTools/PatAlgos/python/tools/pfTools.py
    # We can't use pfTools directly, because it's only for PF2PAT, but
    # we can get the PF isolation by adding these by ourselves
    module.isoDeposits = cms.PSet(
        pfChargedHadrons   = cms.InputTag("elPFIsoDepositCharged"),
        pfChargedAll       = cms.InputTag("elPFIsoDepositChargedAll"),
        pfPUChargedHadrons = cms.InputTag("elPFIsoDepositPU"),
        pfNeutralHadrons   = cms.InputTag("elPFIsoDepositNeutral"),
        pfPhotons          = cms.InputTag("elPFIsoDepositGamma"),
        user               = cms.VInputTag(
            cms.InputTag("elPFIsoDepositChargedNoChs"),
            cms.InputTag("elPFIsoDepositChargedAllNoChs")
        )
    )

    cone = "04"
    module.isolationValues = cms.PSet(
        pfChargedHadrons   = cms.InputTag("elPFIsoValueCharged"+cone),
        pfChargedAll       = cms.InputTag("elPFIsoValueChargedAll"+cone),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU"+cone),
        pfNeutralHadrons   = cms.InputTag("elPFIsoValueNeutral"+cone),
        pfPhotons          = cms.InputTag("elPFIsoValueGamma"+cone),
        user               = cms.VInputTag(
            cms.InputTag("elPFIsoValueChargedNoChs"+cone),
            cms.InputTag("elPFIsoValueChargedAllNoChs"+cone)
        )
    )
