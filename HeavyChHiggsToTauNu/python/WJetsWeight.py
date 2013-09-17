import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.pileupReweightedAllEvents as pileupReweightedAllEvents
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

class NEvents:
    def __init__(self, inclusive_v1, inclusive_v2, jet1, jet2, jet3, jet4):
        self.inclusive_v1 = inclusive_v1
        self.inclusive_v2 = inclusive_v2
        self.jet1 = jet1
        self.jet2 = jet2
        self.jet3 = jet3
        self.jet4 = jet4

    def construct7TeV(self, era, weightType):
        # The cross sections should the ones given by madgraph (LO, from PREP)
        pset = cms.EDProducer("HPlusWJetsWeightProducer",
            lheSrc = cms.InputTag("source", "", "LHE"),
            alias = cms.string("wjetsWeight"),
            enabled = cms.bool(True),
            sampleJetBin = cms.int32(-1),
            inclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_WJets", "7")),
            jetBin1 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W1Jets", "7")),
            ),
            jetBin2 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W2Jets", "7")),
            ),
            jetBin3 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W3Jets", "7")),
            ),
            jetBin4 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W4Jets", "7")),
            ),
        )

        # Assume that if no era is given, on PU reweighting is done
        if era == None or len(era) == 0:
            pset.inclusiveNevents = cms.double(self.inclusive_v1)
            for jetBin in [1, 2, 3, 4]:
                getattr(pset, "jetBin%d"%jetBin).exclusiveNevents = cms.double(getattr(self, "jet%d"%jetBin))

            return pset


        def weightedAllEvents(datasetName, unweighted):
            return pileupReweightedAllEvents.getWeightedAllEvents(datasetName, era).getWeighted(unweighted, weightType)

        pset.inclusiveNevents = cms.double(
            weightedAllEvents("WJets_TuneZ2_Fall11", self.inclusive_v1)
        )
        for jetBin in [1, 2, 3, 4]:
            getattr(pset, "jetBin%d"%jetBin).exclusiveNevents = cms.double(weightedAllEvents("W%dJets_TuneZ2_Fall11"%jetBin, getattr(self, "jet%d"%jetBin)))

        return pset

    def construct8TeV(self, era, weightType):
        # The cross sections should the ones given by madgraph (LO, from PREP)
        pset = cms.EDProducer("HPlusWJetsWeightProducer",
            lheSrc = cms.InputTag("source", "", "LHE"),
            alias = cms.string("wjetsWeight"),
            enabled = cms.bool(True),
            sampleJetBin = cms.int32(-1),
            inclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_WJets", "8")),
            jetBin1 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W1Jets", "8")),
            ),
            jetBin2 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W2Jets", "8")),
            ),
            jetBin3 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W3Jets", "8")),
            ),
            jetBin4 = cms.PSet(
                exclusiveCrossSection = cms.double(xsect.backgroundCrossSections.crossSection("PREP_W4Jets", "8")),
            ),
        )

        # Assume that if no era is given, on PU reweighting is done
        if era == None or len(era) == 0:
            pset.inclusiveNevents = cms.double(self.inclusive_v1 + self.inclusive_v2)
            for jetBin in [1, 2, 3, 4]:
                getattr(pset, "jetBin%d"%jetBin).exclusiveNevents = cms.double(getattr(self, "jet%d"%jetBin))

            return pset


        def weightedAllEvents(datasetName, unweighted):
            return pileupReweightedAllEvents.getWeightedAllEvents(datasetName, era).getWeighted(unweighted, weightType)

        pset.inclusiveNevents = cms.double(
            weightedAllEvents("WJets_TuneZ2star_v1_Summer12", self.inclusive_v1) +
            weightedAllEvents("WJets_TuneZ2star_v2_Summer12", self.inclusive_v2)
        )
        for jetBin in [1, 2, 3, 4]:
            getattr(pset, "jetBin%d"%jetBin).exclusiveNevents = cms.double(weightedAllEvents("W%dJets_TuneZ2star_Summer12"%jetBin, getattr(self, "jet%d"%jetBin)))

        return pset

# Non-pu-reweighted events
# These are obtained by running the signal analysis once (e.g. without
# W+jets weights) and recording the numbers of all unweighted events
# here.
_wjetsNumberOfEvents = {
    "pattuple_v44_4": NEvents(inclusive_v1=81345384,
                              inclusive_v2=None,
                              jet1=None,
                              jet2=25400546,
                              jet3=6533053,
                              jet4=12608390),
    "pattuple_v44_5": NEvents(inclusive_v1=81345384,
                              inclusive_v2=None,
                              jet1=76051616,
                              jet2=25400546,
                              jet3=7541595,
                              jet4=13133738),
    "embedding_skim_v44_5_1": NEvents(inclusive_v1=80996768,
                                      inclusive_v2=None,
                                      jet1=75834320,
                                      jet2=25400548,
                                      jet3=7541595,
                                      jet4=13133738),
    "pattuple_v53_1_test1": NEvents(inclusive_v1=2504608,
                                    inclusive_v2=3458492,
                                    jet1=2314140,
                                    jet2=851120,
                                    jet3=317130,
                                    jet4=218488),
    "pattuple_v53_1": NEvents(inclusive_v1=18393090,
                              inclusive_v2=56094032,
                              jet1=23141596,
                              jet2=34044920,
                              jet3=15539503,
                              jet4=13382803),
    "pattuple_v53_2": NEvents(inclusive_v1=18393090,
                              inclusive_v2=57709900,
                              jet1=23141596,
                              jet2=34044920,
                              jet3=15539503,
                              jet4=13382803),
    "pattuple_v53_3": NEvents(inclusive_v1=18393090,
                              inclusive_v2=57709900,
                              jet1=23141598,
                              jet2=34044920,
                              jet3=15457717,
                              jet4=13382803),
    "embedding_skim_v53_3": NEvents(inclusive_v1=18393090,
                                    inclusive_v2=57709908,
                                    jet1=23141596,
                                    jet2=34044948,
                                    jet3=15539503,
                                    jet4=13382803),
}


def getWJetsWeight(dataVersion, options, inputWorkflow, era, suffix="", useInclusiveIfNotFound=False):
    weightType = {"": pileupReweightedAllEvents.PileupWeightType.NOMINAL,
                  "up": pileupReweightedAllEvents.PileupWeightType.UP,
                  "down": pileupReweightedAllEvents.PileupWeightType.DOWN
                  }[suffix]

    if dataVersion.is44X():
        pset = _wjetsNumberOfEvents[inputWorkflow].construct7TeV(era, weightType)
    elif dataVersion.is53X():
        pset = _wjetsNumberOfEvents[inputWorkflow].construct8TeV(era, weightType)
    else:
        raise Exception("WJets weights are available only for 44X and 53X")
    try:
        pset.sampleJetBin = {"WJets": -1,
                             "W1Jets": 1,
                             "W2Jets": 2,
                             "W3Jets": 3,
                             "W4Jets": 4}[options.sample]
    except KeyError, e:
        if useInclusiveIfNotFound:
            pset.sampleJetBin = -1
        else:
            raise e

    return pset

