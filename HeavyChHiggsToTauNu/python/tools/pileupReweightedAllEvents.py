## \package pileupReweightedAllEvents
# Utilities for updating the pileup-reweighted number of all events
#
# This deserves it's own package, as with the W+Njets weighting we
# need this information also in the CMSSW configuration side. Matti
# wants to avoid all unnecessary dependencies (e.g. to ROOT) then.

## "Enumeration" of pile-up weight type
class PileupWeightType:
    class UNWEIGHTED:
        pass
    class NOMINAL:
        pass
    class UP:
        pass
    class DOWN:
        pass

    toString = {
        UNWEIGHTED: "UNWEIGHTED",
        NOMINAL: "NOMINAL",
        UP: "UP",
        DOWN: "DOWN",
        }

    fromString = {
        "UNWEIGHTED": UNWEIGHTED,
        "NOMINAL": NOMINAL,
        "UP": UP,
        "DOWN": DOWN,
        }

## Utility class for handling the weighted number of all MC events
#
# Represents values for one dataset
class WeightedAllEvents:
    ## Constructor
    #
    # \param unweighted   Number of unweighted MC events
    # \param weighted     Weighted number of all MC events (nominal)
    # \param up           Weighted number of all MC events, varied upwards (for systematics)
    # \param down         Weighted number of all MC events, varied downwards (for systematics)
    def __init__(self, unweighted, weighted, up, down):
        self.unweighted = unweighted
        self.weighted = {
            PileupWeightType.NOMINAL: weighted,
            PileupWeightType.UP: up,
            PileupWeightType.DOWN: down
            }
        self.name = "Unknown"

    def _setName(self, name):
        self.name = name

    ## Get the weighted number of all MC events
    #
    # \param unweighted  Unweighted number of all events (used for a cross check)
    # \param weightType  Type of weight (nominal, up/down varied), one of PileupWeightType members
    def getWeighted(self, unweighted, weightType=PileupWeightType.NOMINAL):
        if weightType is PileupWeightType.UNWEIGHTED:
            return unweighted
        try:
            nweighted = self.weighted[weightType]
        except KeyError:
            raise Exception("Invalid weight type %s, see pileupReweightedAllEvents.PileupWeightType" % weightType.__name__)
        if int(unweighted) != int(self.unweighted):
            nweighted = unweighted * nweighted/self.unweighted
            print "%s: Unweighted all events from analysis %d, unweighted all events from _weightedAllEvents %d, using their ratio for setting the weighted all events (weight=%f)" % (self.name, int(unweighted), int(self.unweighted), nweighted)
        #print "Using weighted event count for "+self.name+":",nweighted
        return nweighted

    ## \var unweighted
    # Number of unweighted all MC events
    ## \var weighted
    # Dictionary holding the weighted number of all MC events for nominal case, and for up/down variations (for systematics)

class WeightedAllEventsTopPt:
    # helper class
    class Weighted:
        def __init__(self, weighted, up, down):
            self.weighted = {
                PileupWeightType.NOMINAL: weighted,
                PileupWeightType.UP: up,
                PileupWeightType.DOWN: down
                }
        def getWeighted(self, topPtWeightType):
            try:
                return self.weighted[topPtWeightType]
            except KeyError:
                raise Exception("Invalid top pt weight type %s, see pileupReweightedAllEvents.PileupWeightType" % topPtWeightType.__name__)

    def __init__(self, unweighted, **kwargs):
        self.unweighted = unweighted
        self.weighted = {}
        self.weighted.update(kwargs)

    def _setName(self, name):
        self.name = name

    def getWeighted(self, unweighted, topPtWeight=None, topPtWeightType=PileupWeightType.UNWEIGHTED, **kwargs):
        if topPtWeightType is PileupWeightType.UNWEIGHTED:
            return self.unweighted.getWeighted(unweighted, **kwargs)
        if topPtWeight is None:
            raise Exception("topPtWeight must be set when topPtWeightType is not UNWEIGHTED")
        try:
            weightedAllEvents = self.weighted[topPtWeight].getWeighted(topPtWeightType)
        except KeyError:
            raise Exception("Invalid top pt weight name %s, see TopPtWeightSchemes.schemes" % topPtWeight)
        weightedAllEvents._setName(self.name)
        return weightedAllEvents.getWeighted(unweighted, **kwargs)

## Get WeightedAllEvents for dataset and era
#
# \param datasetName   Name of the dataset
# \param era           Data era
def getWeightedAllEvents(datasetName, era):
    try:
        data = _weightedAllEvents[era]
    except KeyError:
        raise Exception("No weighted numbers of all events specified for data era '%s', see pileupReweightedAllEvents._weightedAllEvents dictionary" % era)

    weightedAllEvents = data[datasetName]
    weightedAllEvents._setName(datasetName)
    return weightedAllEvents


## Number of PU-reweighted all events for skimmed datasets
#
# These are obtained with following tools:
# 1) pileupNtuple_cfg.py (produces tree of true number of vertices in MC)
# 2) pileupCalc.py (produces histogram of true interactions for data in given run range)
# 3) test/PUtools/generatePUweights.py (produces histogram of MC interactions)
# 4) test/PUtools/calculateWeightedTotalEventCount.py (uses output of 1-3 as input and produces the following code fragment
_weightedAllEvents = {
    "Run2011A": {
        "TTToHplusBWB_M80_Fall11": WeightedAllEvents(unweighted=218200, weighted=222212.037137, up=221902.723480, down=222062.117878),
        "TTToHplusBWB_M90_Fall11": WeightedAllEvents(unweighted=218050, weighted=222329.037037, up=222279.317313, down=221972.416812),
        "TTToHplusBWB_M100_Fall11": WeightedAllEvents(unweighted=218200, weighted=222212.037137, up=221902.723480, down=222062.117878),
        "TTToHplusBWB_M120_Fall11": WeightedAllEvents(unweighted=218400, weighted=222440.768255, up=222128.289383, down=222293.443724),
        "TTToHplusBWB_M140_Fall11": WeightedAllEvents(unweighted=218400, weighted=222440.768255, up=222128.289383, down=222293.443724),
        "TTToHplusBWB_M150_Fall11": WeightedAllEvents(unweighted=219000, weighted=223111.838288, up=222797.371623, down=222965.554287),
        "TTToHplusBWB_M155_Fall11": WeightedAllEvents(unweighted=219000, weighted=223111.838288, up=222797.371623, down=222965.554287),
        "TTToHplusBWB_M160_Fall11": WeightedAllEvents(unweighted=218400, weighted=222712.375684, up=222661.426845, down=222356.837539),
        "TTToHplusBHminusB_M80_Fall11": WeightedAllEvents(unweighted=218400, weighted=222712.375684, up=222661.426845, down=222356.837539),
        "TTToHplusBHminusB_M90_Fall11": WeightedAllEvents(unweighted=219000, weighted=223381.100608, up=223151.800306, down=223188.617539),
        "TTToHplusBHminusB_M100_Fall11": WeightedAllEvents(unweighted=217600, weighted=225984.226087, up=225590.815111, down=225943.497197),
        "TTToHplusBHminusB_M120_Fall11": WeightedAllEvents(unweighted=218800, weighted=227181.902417, up=226791.315198, down=227135.151346),
        "TTToHplusBHminusB_M140_Fall11": WeightedAllEvents(unweighted=218800, weighted=227184.956817, up=226793.804900, down=227138.794531),
        "TTToHplusBHminusB_M150_Fall11": WeightedAllEvents(unweighted=218800, weighted=227181.902417, up=226791.315198, down=227135.151346),
        "TTToHplusBHminusB_M155_Fall11": WeightedAllEvents(unweighted=217400, weighted=224622.885922, up=224178.880421, down=224636.065563),
        "TTToHplusBHminusB_M160_Fall11": WeightedAllEvents(unweighted=220000, weighted=228152.034711, up=227725.646117, down=228213.572648),
        "HplusTB_M180_Fall11": WeightedAllEvents(unweighted=210823, weighted=215080.692951, up=214985.140001, down=214797.010366),
        "HplusTB_M190_Fall11": WeightedAllEvents(unweighted=209075, weighted=212878.780873, up=212824.595123, down=212547.329155),
        "HplusTB_M200_Fall11": WeightedAllEvents(unweighted=214140, weighted=218729.296340, up=218489.020677, down=218535.610169),
        "HplusTB_M220_Fall11": WeightedAllEvents(unweighted=204040, weighted=207525.122919, up=207385.995097, down=207274.662719),
        "HplusTB_M250_Fall11": WeightedAllEvents(unweighted=202450, weighted=204070.910060, up=204125.717761, down=203593.971870),
        "HplusTB_M300_Fall11": WeightedAllEvents(unweighted=201457, weighted=202116.437670, up=202356.380887, down=201437.047268),
#        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=60325852.933433, up=60322253.558011, down=60231186.347115),
        "WJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=81345381, weighted=82377568.126906, up=82349060.998291, down=82313862.591121),
        "W2Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=25400546, weighted=25071227.079162, up=25154522.001505, down=24950382.486547),
        "W3Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=7685944, weighted=7317449.306018, up=7341688.317943, down=7278364.468218),
        "W4Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=13133738, weighted=13062301.621954, up=13055893.988491, down=13048100.263525),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=31480628, weighted=30998553.038641, up=31063192.638656, down=30901298.958760),
        "DYJetsToLL_M50_TuneZ2_Fall11": WeightedAllEvents(unweighted=36264432, weighted=36784308.329060, up=36782129.609356, down=36718648.659880),
        "T_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=3900171, weighted=4050330.241432, up=4041225.448775, down=4051357.109157),
        "Tbar_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=1944826, weighted=2020509.925110, up=2015928.430863, down=2021038.792512),
        "T_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=814390, weighted=829409.258989, up=828376.221702, down=828732.889419),
        "Tbar_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=809984, weighted=824128.618323, up=823807.971595, down=822971.688741),
        "T_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=259971, weighted=266159.892291, up=266020.508502, down=265848.527590),
        "Tbar_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=137980, weighted=143304.004260, up=143054.135023, down=143277.899169),
        "WW_TuneZ2_Fall11": WeightedAllEvents(unweighted=4225916, weighted=4257746.373670, up=4256437.413790, down=4252953.634985),
        "WZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4265243, weighted=4406721.928127, up=4401780.867118, down=4403806.738003),
        "ZZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4191045, weighted=4344331.840620, up=4335210.895426, down=4344886.886857),
        "QCD_Pt20_MuEnriched_TuneZ2_Fall11": WeightedAllEvents(unweighted=25080241, weighted=25063106.092206, up=25105540.088830, down=24980532.692696),
        "QCD_Pt30to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=6583068, weighted=6828964.415819, up=6818908.354848, down=6827256.290380),
        "QCD_Pt50to80_TuneZ2_Fall11": WeightedAllEvents(unweighted=6600000, weighted=6832512.936987, up=6819965.347566, down=6831831.879193),
        "QCD_Pt80to120_TuneZ2_Fall11": WeightedAllEvents(unweighted=6581772, weighted=6715674.668516, up=6715172.795926, down=6703671.535201),
        "QCD_Pt120to170_TuneZ2_Fall11": WeightedAllEvents(unweighted=6127528, weighted=6221598.645593, up=6218900.049906, down=6212658.706050),
        "QCD_Pt170to300_TuneZ2_Fall11": WeightedAllEvents(unweighted=6220160, weighted=6267144.446872, up=6268077.975866, down=6252959.749113),
        "QCD_Pt300to470_TuneZ2_Fall11": WeightedAllEvents(unweighted=6432669, weighted=6508237.455281, up=6506327.251603, down=6497639.996005),
        "W1Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=76051609, weighted=77644362.113436, up=77583557.117218, down=77586056.500796),
        "W3Jets_TuneZ2_v2_Fall11": WeightedAllEvents(unweighted=7541595, weighted=7537540.054457, up=7537738.468034, down=7537552.142497),
        # multicrab_pileupNtuple_130909_162629
        "TTJets_TuneZ2_Fall11": WeightedAllEventsTopPt(unweighted = WeightedAllEvents(unweighted=59444088, weighted=60325852.741440, up=60322253.227963, down=60231186.256806),
                                                       TopPtCombined = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=62844239.913834, up=62840342.797988, down=62745699.176327),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=67888121.440667, up=67883615.781412, down=67781921.010222),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=60325852.741440, up=60322253.227963, down=60231186.256806)),
                                                       TopPtSeparate = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=61633358.519904, up=61629412.690126, down=61536897.856909),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=63894925.717996, up=63890526.992493, down=63795219.409307),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=60325852.741440, up=60322253.227963, down=60231186.256806)),
                                                       TTH = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=60293195.146847, up=60289444.973253, down=60198684.099778),
                                                                                             up=WeightedAllEvents(unweighted=59444088, weighted=62015383.416890, up=62011283.979865, down=61918377.302050),
                                                                                             down=WeightedAllEvents(unweighted=59444088, weighted=60325852.741440, up=60322253.227963, down=60231186.256806)),
                                                       ),
    },
    "Run2011B": {
        "TTToHplusBWB_M80_Fall11": WeightedAllEvents(unweighted=218200, weighted=216325.066231, up=217254.616614, down=215493.146064),
        "TTToHplusBWB_M90_Fall11": WeightedAllEvents(unweighted=218050, weighted=216859.944595, up=217180.292362, down=216556.317936),
        "TTToHplusBWB_M100_Fall11": WeightedAllEvents(unweighted=218200, weighted=216325.066231, up=217254.616614, down=215493.146064),
        "TTToHplusBWB_M120_Fall11": WeightedAllEvents(unweighted=218400, weighted=216524.347428, up=217455.340840, down=215690.106370),
        "TTToHplusBWB_M140_Fall11": WeightedAllEvents(unweighted=218400, weighted=216524.347428, up=217455.340840, down=215690.106370),
        "TTToHplusBWB_M150_Fall11": WeightedAllEvents(unweighted=219000, weighted=217109.397096, up=218029.521207, down=216287.997096),
        "TTToHplusBWB_M155_Fall11": WeightedAllEvents(unweighted=219000, weighted=217109.397096, up=218029.521207, down=216287.997096),
        "TTToHplusBWB_M160_Fall11": WeightedAllEvents(unweighted=218400, weighted=217199.576237, up=217514.164630, down=216901.320571),
        "TTToHplusBHminusB_M80_Fall11": WeightedAllEvents(unweighted=218400, weighted=217199.576237, up=217514.164630, down=216901.320571),
        "TTToHplusBHminusB_M90_Fall11": WeightedAllEvents(unweighted=219000, weighted=217073.026776, up=217778.431885, down=216434.807809),
        "TTToHplusBHminusB_M100_Fall11": WeightedAllEvents(unweighted=217600, weighted=215031.262959, up=214978.393602, down=215302.959444),
        "TTToHplusBHminusB_M120_Fall11": WeightedAllEvents(unweighted=218800, weighted=216219.097087, up=216173.510679, down=216484.635746),
        "TTToHplusBHminusB_M140_Fall11": WeightedAllEvents(unweighted=218800, weighted=216219.090151, up=216173.481971, down=216484.635946),
        "TTToHplusBHminusB_M150_Fall11": WeightedAllEvents(unweighted=218800, weighted=216219.097087, up=216173.510679, down=216484.635746),
        "TTToHplusBHminusB_M155_Fall11": WeightedAllEvents(unweighted=217400, weighted=214084.219074, up=214266.075952, down=214126.078536),
        "TTToHplusBHminusB_M160_Fall11": WeightedAllEvents(unweighted=220000, weighted=218747.551196, up=218669.481239, down=218888.810312),
        "HplusTB_M180_Fall11": WeightedAllEvents(unweighted=210823, weighted=209675.165216, up=209964.628187, down=209409.359243),
        "HplusTB_M190_Fall11": WeightedAllEvents(unweighted=209075, weighted=207916.798292, up=208265.237141, down=207609.804017),
        "HplusTB_M200_Fall11": WeightedAllEvents(unweighted=214140, weighted=212259.966393, up=212959.494690, down=211648.087179),
        "HplusTB_M220_Fall11": WeightedAllEvents(unweighted=204040, weighted=202835.223906, up=203486.164125, down=202216.528988),
        "HplusTB_M250_Fall11": WeightedAllEvents(unweighted=202450, weighted=202079.322576, up=202933.498424, down=201279.034487),
        "HplusTB_M300_Fall11": WeightedAllEvents(unweighted=201457, weighted=200195.422594, up=200967.096588, down=199592.613978),
#        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=59233566.400571, up=59337704.411034, down=59147168.792957),
        "WJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=81345381, weighted=81541165.831106, up=81615917.662211, down=81430140.570515),
        "W2Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=25400546, weighted=25596891.612887, up=25715435.973731, down=25461089.267917),
        "W3Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=7685944, weighted=7543101.017547, up=7667914.058201, down=7428410.947998),
        "W4Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=13133738, weighted=12919750.711232, up=13004194.638553, down=12844014.406319),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=31480628, weighted=31788206.010619, up=31946855.170268, down=31614247.507630),
        "DYJetsToLL_M50_TuneZ2_Fall11": WeightedAllEvents(unweighted=36264432, weighted=36063683.838480, up=36150961.119609, down=35988475.218389),
        "T_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=3900171, weighted=3828410.447194, up=3831367.711587, down=3830175.824693),
        "Tbar_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=1944826, weighted=1908779.793916, up=1910193.238839, down=1909741.525521),
        "T_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=814390, weighted=808735.788971, up=811899.643085, down=805867.527582),
        "Tbar_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=809984, weighted=806305.718518, up=807730.689485, down=804934.759558),
        "T_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=259971, weighted=258318.871836, up=258441.583483, down=258343.357276),
        "Tbar_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=137980, weighted=136359.429157, up=136330.371583, down=136527.779738),
        "WW_TuneZ2_Fall11": WeightedAllEvents(unweighted=4225916, weighted=4189325.647057, up=4201960.423124, down=4178839.405548),
        "WZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4265243, weighted=4236720.798188, up=4236658.208119, down=4238992.390341),
        "ZZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4191045, weighted=4115225.896538, up=4118948.772735, down=4116500.010809),
        "QCD_Pt20_MuEnriched_TuneZ2_Fall11": WeightedAllEvents(unweighted=25080241, weighted=25141194.478285, up=25217057.175022, down=25058921.790455),
        "QCD_Pt30to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=6583068, weighted=6540519.679274, up=6536435.713132, down=6547124.981665),
        "QCD_Pt50to80_TuneZ2_Fall11": WeightedAllEvents(unweighted=6600000, weighted=6485525.157505, up=6490583.270396, down=6488112.330529),
        "QCD_Pt80to120_TuneZ2_Fall11": WeightedAllEvents(unweighted=6581772, weighted=6543851.805321, up=6552109.358305, down=6536295.560018),
        "QCD_Pt120to170_TuneZ2_Fall11": WeightedAllEvents(unweighted=6127528, weighted=6096655.446293, up=6114847.606844, down=6078872.005553),
        "QCD_Pt170to300_TuneZ2_Fall11": WeightedAllEvents(unweighted=6220160, weighted=6194092.620957, up=6222731.577817, down=6167568.648234),
        "QCD_Pt300to470_TuneZ2_Fall11": WeightedAllEvents(unweighted=6432669, weighted=6360307.883080, up=6380161.481108, down=6344053.485342),
        "W1Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=76051609, weighted=75728733.328432, up=75798599.404381, down=75648203.837487),
        "W3Jets_TuneZ2_v2_Fall11": WeightedAllEvents(unweighted=7541595, weighted=7546266.215300, up=7546438.546617, down=7545655.045459),
        "TTJets_TuneZ2_Fall11": WeightedAllEventsTopPt(unweighted = WeightedAllEvents(unweighted=59444088, weighted=59233566.566973, up=59337704.690950, down=59147168.805523),
                                                       TopPtCombined = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=61708257.760790, up=61817297.445449, down=61617575.301592),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=66662764.612929, up=66781256.877939, down=66563947.479685),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=59233566.566973, up=59337704.690950, down=59147168.805523)),
                                                       TopPtSeparate = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=60517440.575763, up=60624127.398478, down=60428860.149392),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=62737845.364941, up=62848796.728375, down=62645641.312006),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=59233566.566973, up=59337704.690950, down=59147168.805523)),
                                                       TTH = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=59203328.156319, up=59307949.139600, down=59116323.979157),
                                                                                             up=WeightedAllEvents(unweighted=59444088, weighted=60896014.579425, up=61004234.334096, down=60805784.037903),
                                                                                             down=WeightedAllEvents(unweighted=59444088, weighted=59233566.566973, up=59337704.690950, down=59147168.805523)),
                                                       ),
    },
    "Run2011AB": {
        "TTToHplusBWB_M80_Fall11": WeightedAllEvents(unweighted=218200, weighted=219013.870316, up=219377.625194, down=218493.470983),
        "TTToHplusBWB_M90_Fall11": WeightedAllEvents(unweighted=218050, weighted=219357.887652, up=219509.256396, down=219030.077434),
        "TTToHplusBWB_M100_Fall11": WeightedAllEvents(unweighted=218200, weighted=219013.870316, up=219377.625194, down=218493.470983),
        "TTToHplusBWB_M120_Fall11": WeightedAllEvents(unweighted=218400, weighted=219226.602415, up=219589.695779, down=218706.127472),
        "TTToHplusBWB_M140_Fall11": WeightedAllEvents(unweighted=218400, weighted=219226.602415, up=219589.695779, down=218706.127472),
        "TTToHplusBWB_M150_Fall11": WeightedAllEvents(unweighted=219000, weighted=219850.940864, up=220207.222286, down=219337.917510),
        "TTToHplusBWB_M155_Fall11": WeightedAllEvents(unweighted=219000, weighted=219850.940864, up=220207.222286, down=219337.917510),
        "TTToHplusBWB_M160_Fall11": WeightedAllEvents(unweighted=218400, weighted=219717.481950, up=219865.160887, down=219393.083965),
        "TTToHplusBHminusB_M80_Fall11": WeightedAllEvents(unweighted=218400, weighted=219717.481950, up=219865.160887, down=219393.083965),
        "TTToHplusBHminusB_M90_Fall11": WeightedAllEvents(unweighted=219000, weighted=219954.164625, up=220232.701459, down=219519.555956),
        "TTToHplusBHminusB_M100_Fall11": WeightedAllEvents(unweighted=217600, weighted=220033.898861, up=219825.584633, down=220162.939281),
        "TTToHplusBHminusB_M120_Fall11": WeightedAllEvents(unweighted=218800, weighted=221226.228298, up=221023.160383, down=221349.172885),
        "TTToHplusBHminusB_M140_Fall11": WeightedAllEvents(unweighted=218800, weighted=221227.619591, up=221024.281952, down=221350.836988),
        "TTToHplusBHminusB_M150_Fall11": WeightedAllEvents(unweighted=218800, weighted=221226.228298, up=221023.160383, down=221349.172885),
        "TTToHplusBHminusB_M155_Fall11": WeightedAllEvents(unweighted=217400, weighted=218897.630068, up=218793.719042, down=218926.430381),
        "TTToHplusBHminusB_M160_Fall11": WeightedAllEvents(unweighted=220000, weighted=223042.937415, up=222805.856818, down=223147.820335),
        "HplusTB_M180_Fall11": WeightedAllEvents(unweighted=210823, weighted=212144.075847, up=212257.731586, down=211870.125460),
        "HplusTB_M190_Fall11": WeightedAllEvents(unweighted=209075, weighted=210183.124939, up=210347.709939, down=209864.978819),
        "HplusTB_M200_Fall11": WeightedAllEvents(unweighted=214140, weighted=215214.756058, up=215485.088754, down=214793.907779),
        "HplusTB_M220_Fall11": WeightedAllEvents(unweighted=204040, weighted=204977.279613, up=205267.399981, down=204526.790792),
        "HplusTB_M250_Fall11": WeightedAllEvents(unweighted=202450, weighted=202988.956520, up=203478.040956, down=202336.363474),
        "HplusTB_M300_Fall11": WeightedAllEvents(unweighted=201457, weighted=201072.823428, up=201601.647938, down=200435.044014),
#        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=59732455.311131, up=59787394.224508, down=59642285.070652),
        "WJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=81345381, weighted=81923182.650655, up=81950778.642015, down=81833773.478359),
        "W2Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=25400546, weighted=25356800.576871, up=25459240.234189, down=25227828.062063),
        "W3Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=7685944, weighted=7440037.276690, up=7518911.450093, down=7359878.427958),
        "W4Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=13133738, weighted=12984859.147391, up=13027808.158229, down=12937228.976309),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=31480628, weighted=31427541.389412, up=31543245.014197, down=31288614.004514),
        "DYJetsToLL_M50_TuneZ2_Fall11": WeightedAllEvents(unweighted=36264432, weighted=36392820.522162, up=36439245.395375, down=36321976.051131),
        "T_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=3900171, weighted=3929769.679131, up=3927219.590481, down=3931198.593261),
        "Tbar_t-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=1944826, weighted=1959811.205155, up=1958487.464056, down=1960575.654961),
        "T_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=814390, weighted=818178.151018, up=819425.269922, down=816311.097266),
        "Tbar_tW-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=809984, weighted=814446.116456, up=815073.938865, down=813172.981553),
        "T_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=259971, weighted=261900.164859, up=261903.234280, down=261771.283312),
        "Tbar_s-channel_TuneZ2_Fall11": WeightedAllEvents(unweighted=137980, weighted=139531.281406, up=139401.429947, down=139610.842371),
        "WW_TuneZ2_Fall11": WeightedAllEvents(unweighted=4225916, weighted=4220576.001822, up=4226842.621789, down=4212690.482360),
        "WZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4265243, weighted=4314366.796459, up=4312077.477019, down=4314270.014944),
        "ZZ_TuneZ2_Fall11": WeightedAllEvents(unweighted=4191045, weighted=4219867.317119, up=4217725.835095, down=4220813.875245),
        "QCD_Pt20_MuEnriched_TuneZ2_Fall11": WeightedAllEvents(unweighted=25080241, weighted=25105528.535085, up=25166122.087209, down=25023118.201654),
        "TTToHplusBWB_M90_Fall11_HighPU": WeightedAllEvents(unweighted=218050, weighted=1.477673, up=0.861639, down=2.872045), #ave32
        "TTToHplusBWB_M160_Fall11_HighPU": WeightedAllEvents(unweighted=218400, weighted=1.480045, up=0.863022, down=2.876655), #ave32
        "TTJets_TuneZ2_Fall11_HighPU": WeightedAllEvents(unweighted=1033841, weighted=7.006093, up=4.085293, down=13.617234), #ave32
        "QCD_Pt30to50_TuneZ2_Fall11": WeightedAllEvents(unweighted=6583068, weighted=6672263.388985, up=6665454.227340, down=6675072.698602),
        "QCD_Pt50to80_TuneZ2_Fall11": WeightedAllEvents(unweighted=6600000, weighted=6644007.707199, up=6641027.525614, down=6645103.463428),
        "QCD_Pt80to120_TuneZ2_Fall11": WeightedAllEvents(unweighted=6581772, weighted=6622329.858643, up=6626588.084143, down=6612743.187378),
        "QCD_Pt120to170_TuneZ2_Fall11": WeightedAllEvents(unweighted=6127528, weighted=6153721.769562, up=6162373.241593, down=6139978.002476),
        "QCD_Pt170to300_TuneZ2_Fall11": WeightedAllEvents(unweighted=6220160, weighted=6227458.175356, up=6243443.406265, down=6206570.345192),
        "QCD_Pt300to470_TuneZ2_Fall11": WeightedAllEvents(unweighted=6432669, weighted=6427872.959324, up=6437787.310456, down=6414202.885941),
        "W1Jets_TuneZ2_Fall11": WeightedAllEvents(unweighted=76051609, weighted=76603674.038794, up=76613873.380221, down=76533302.418103),
        "W3Jets_TuneZ2_v2_Fall11": WeightedAllEvents(unweighted=7541595, weighted=7542280.644894, up=7542464.812360, down=7541954.109907),
        "TTJets_TuneZ2_Fall11": WeightedAllEventsTopPt(unweighted = WeightedAllEvents(unweighted=59444088, weighted=59732455.313507, up=59787394.226023, down=59642285.036207),
                                                       TopPtCombined = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=62227104.125905, up=62284570.278088, down=62132836.787114),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=67222431.799873, up=67284755.932160, down=67120247.071204),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=59732455.313507, up=59787394.226023, down=59642285.036207)),
                                                       TopPtSeparate = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=61027122.852141, up=61083288.380528, down=60934947.439112),
                                                                                                       up=WeightedAllEvents(unweighted=59444088, weighted=63266328.082984, up=63324603.840149, down=63170701.839852),
                                                                                                       down=WeightedAllEvents(unweighted=59444088, weighted=59732455.313507, up=59787394.226023, down=59642285.036207)),
                                                       TTH = WeightedAllEventsTopPt.Weighted(weighted=WeightedAllEvents(unweighted=59444088, weighted=59701111.968319, up=59756244.356672, down=59610683.238908),
                                                                                             up=WeightedAllEvents(unweighted=59444088, weighted=61407273.009811, up=61464201.176636, down=61313952.042213),
                                                                                             down=WeightedAllEvents(unweighted=59444088, weighted=59732455.313507, up=59787394.226023, down=59642285.036207)),
                                                       ),
    },
}
