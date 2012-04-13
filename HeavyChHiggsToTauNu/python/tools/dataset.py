## \package dataset
# Dataset utilities and classes
#
# This package contains classes and utilities for dataset management.
# There are also some functions and classes not directly related to
# dataset management, but are placed here due to some dependencies.

import glob, os, sys, re
import json
import math
import copy

import ROOT

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

## "Enumeration" of pile-up weight type
class PileupWeightType:
    NOMINAL = 0
    UP = 1
    DOWN = 2

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

    ## Get the weighted number of all MC events
    #
    # \param name        Name of the dataset (used only in a warning message)
    # \param unweighted  Unweighted number of all events (used for a cross check)
    # \param weightType  Type of weight (nominal, up/down varied), one of PileupWeightType members
    def getWeighted(self, name, unweighted, weightType=PileupWeightType.NOMINAL):
        try:
            nweighted = self.weighted[weightType]
        except KeyError:
            raise Exception("Invalid weight type %d, see dataset.PileupWeightType" % weightType)
        if int(unweighted) != int(self.unweighted):
            print "%s: Unweighted all events from analysis %d, unweighted all events from _weightedAllEvents %d, using their ratio for setting the weighted all events" % (name, int(unweighted), int(self.unweighted))
            nweighted = unweighted * nweighted/self.unweighted
        print nweighted
        return nweighted

    ## \var unweighted
    # Number of unweighted all MC events
    ## \var weighted
    # Dictionary holding the weighted number of all MC events for nominal case, and for up/down variations (for systematics)

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
        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=60325852.933433, up=60322253.558011, down=60231186.347115),
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
        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=59233566.400571, up=59337704.411034, down=59147168.792957),
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
    },
    "Run2011A+B": {
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
        "TTJets_TuneZ2_Fall11": WeightedAllEvents(unweighted=59444088, weighted=59732455.311131, up=59787394.224508, down=59642285.070652),
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
    },
}

## Construct DatasetManager from a list of MultiCRAB directory names.
# 
# \param multiDirs   List of strings or pairs of strings of the MultiCRAB
#                    directories (relative to the working directory). If
#                    the item of the list is pair of strings, the first
#                    element is the directory, and the second element is
#                    the postfix for the dataset names from that directory.
# \param kwargs      Keyword arguments (forwarded to getDatasetsFromMulticrabCfg())
#
# \return DatasetManager object
def getDatasetsFromMulticrabDirs(multiDirs, **kwargs):
    if "cfgfile" in kwargs:
        raise Exception("'cfgfile' keyword argument not allowed")
    if "namePostfix" in kwargs:
        raise Exception("'namePostfix' keyword argument not allowed")

    nameList = []
    for d in multiDirs:
        if isinstance(d, str):
            nameList.append( (os.path.join(d, "multicrab.cfg"), "") )
        else:
            nameList.append( (os.path.join(d[0], "multicrab.cfg"), d[1]) )

    datasets = DatasetManager()
    for cfg, postfix in nameList:
        d = getDatasetsFromMulticrabCfg(cfgfile=cfg, namePostfix=postfix, **kwargs)
        datasets.extend(d)
    return datasets

## Construct DatasetManager from a multicrab.cfg.
#
# \param kwargs   Keyword arguments (see below) 
#
# <b>Keyword arguments</b>
# \li \a opts       Optional OptionParser object. Should have options added with addOptions() and multicrab.addOptions().
# \li \a cfgfile    Path to the multicrab.cfg file (for default, see multicrab.getTaskDirectories())
# \li Rest are forwarded to getDatasetsFromCrabDirs()
#
# \return DatasetManager object
# 
# The section names in multicrab.cfg are taken as the dataset names
# in the DatasetManager object.
def getDatasetsFromMulticrabCfg(**kwargs):
    _args = copy.copy(kwargs)
    opts = kwargs.get("opts", None)
    taskDirs = []
    dirname = ""
    if "cfgfile" in kwargs:
        taskDirs = multicrab.getTaskDirectories(opts, kwargs["cfgfile"])
        dirname = os.path.dirname(kwargs["cfgfile"])
        del _args["cfgfile"]
    else:
        taskDirs = multicrab.getTaskDirectories(opts)

    datasetMgr = getDatasetsFromCrabDirs(taskDirs, **_args)
    if len(dirname) > 0:
        datasetMgr._setBaseDirectory(dirname)
    return datasetMgr

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param taskdirs     List of strings for the CRAB task directories (relative
#                     to the working directory)
# \param kwargs       Keyword arguments (see below) 
# 
# <b>Keyword arguments</b>
# \li \a opts         Optional OptionParser object. Should have options added with addOptions().
# \li \a namePostfix  Postfix for the dataset names (default: '')
# \li Rest are forwarded to getDatasetsFromRootFiles()
#
# \return DatasetManager object
# 
# The basename of the task directories are taken as the dataset
# names in the DatasetManager object (e.g. for directory '../Foo',
# 'Foo' will be the dataset name)
def getDatasetsFromCrabDirs(taskdirs, **kwargs):
    _args = copy.copy(kwargs)
    inputFile = None
    if "opts" in kwargs:
        opts = kwargs["opts"]
        del _args["opts"]
        inputFile = opts.input
    else:
        inputFile = _optionDefaults["input"]
    postfix = kwargs.get("namePostfix", "")
    try:
        del _args["namePostfix"]
    except KeyError:
        pass

    dlist = []
    noFiles = False
    for d in taskdirs:
        files = glob.glob(os.path.join(d, "res", inputFile))
        if len(files) > 1:
            raise Exception("Only one file should match the input (%d matched) for task %s" % (len(files), d))
            return 1
        elif len(files) == 0:
            print >> sys.stderr, "Ignoring dataset %s: no files matched to '%s' in task directory %s" % (d, inputFile, os.path.join(d, "res"))
            noFiles = True
            continue

        dlist.append( (os.path.basename(d)+postfix, files[0]) )

    if noFiles:
        print >> sys.stderr, ""
        print >> sys.stderr, "  There were datasets without files. Have you merged the files with hplusMergeHistograms.py?"
        print >> sys.stderr, ""
        if len(dlist) == 0:
            raise Exception("No datasets. Have you merged the files with hplusMergeHistograms.py?")

    if len(dlist) == 0:
        raise Exception("No datasets from CRAB task directories %s" % ", ".join(taskdirs))

    return getDatasetsFromRootFiles(dlist, **_args)

## Construct DatasetManager from a list of CRAB task directory names.
# 
# \param rootFileList  List of (name, filename) pairs (both should be strings).
#                     'name' is taken as the dataset name, and 'filename' as
#                      the path to the ROOT file.
# \param kwargs        Keyword arguments (see below) 
# 
# <b>Keyword arguments</b>
# \li \a counters      String for a directory name inside the ROOT files for the event counter histograms (default: 'signalAnalysisCounters').
# \li Rest are forwarded to dataset.Dataset.__init__()
#
# \return DatasetManager object
def getDatasetsFromRootFiles(rootFileList, **kwargs):
    counters = kwargs.get("counters", _optionDefaults["counterdir"])
    # Pass the rest of the keyword arguments, except 'counters', to Dataset constructor
    _args = copy.copy(kwargs)
    try:
        del _args["counters"]
    except KeyError:
        pass

    datasets = DatasetManager()
    for name, f in rootFileList:
        dset = Dataset(name, f, counters, **_args)
        datasets.append(dset)
    return datasets

## Default command line options
_optionDefaults = {
    "input": "histograms-*.root",
    "counterdir": "signalAnalysisCounters"
}

## Add common dataset options to OptionParser object.
#
# \param parser   OptionParser object
def addOptions(parser):
    parser.add_option("-i", dest="input", type="string", default=_optionDefaults["input"],
                      help="Pattern for input root files (note: remember to escape * and ? !) (default: '%s')" % _optionDefaults["input"])
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="Give input ROOT files explicitly, if these are given, multicrab.cfg is not read and -d/-i parameters are ignored")
    parser.add_option("--counterDir", "-c", dest="counterdir", type="string", default=_optionDefaults["counterdir"],
                      help="TDirectory name containing the counters (default: %s" % _optionDefaults["counterdir"])


## Represents counter count value with uncertainty.
class Count:
    ## Constructor
    def __init__(self, value, uncertainty=0.0):
        self._value = value
        self._uncertainty = uncertainty

    def copy(self):
        return Count(self._value, self._uncertainty)

    def clone(self):
        return self.copy()

    def value(self):
        return self._value

    def uncertainty(self):
        return self._uncertainty

    def uncertaintyLow(self):
        return self.uncertainty()

    def uncertaintyHigh(self):
        return self.uncertainty()

    ## self = self + count
    def add(self, count):
        self._value += count._value
        self._uncertainty = math.sqrt(self._uncertainty**2 + count._uncertainty**2)

    ## self = self - count
    def subtract(self, count):
        self.add(Count(-count._value, count._uncertainty))

    ## self = self * count
    def multiply(self, count):
        self._uncertainty = math.sqrt( (count._value * self._uncertainty)**2 +
                                       (self._value  * count._uncertainty)**2 )
        self._value = self._value * count._value

    ## self = self / count
    def divide(self, count):
        self._uncertainty = math.sqrt( (self._uncertainty / count._value)**2 +
                                       (self._value*count._uncertainty / (count._value**2) )**2 )
        self._value = self._value / count._value

    ## \var _value
    # Value of the count
    ## \var _uncertainty
    # Uncertainty of the count

## Represents counter count value with asymmetric uncertainties.
class CountAsymmetric:
    def __init__(self, value, uncertaintyLow, uncertaintyHigh):
        self._value = value
        self._uncertaintyLow = uncertaintyLow
        self._uncertaintyHigh = uncertaintyHigh

    def clone(self):
        return CountAsymmetric(self._value, self._uncertaintyLow, self._uncertaintyHigh)

    def value(self):
        return self._value

    def uncertainty(self):
        return max(self._uncertaintyLow, self._uncertaintyHigh)

    def uncertaintyLow(self):
        return self._uncertaintyLow

    def uncertaintyHigh(self):
        return self._uncertaintyHigh

    ## \var _value
    # Value of the count
    ## \var _uncertaintyLow
    # Lower uncertainty of the count (-)
    ## \var _uncertaintyHigh
    # Upper uncertainty of the count (+)

## Transform histogram (TH1) to a list of (name, Count) pairs.
#
# The name is taken from the x axis label and the count is Count
# object with value and (statistical) uncertainty.
def _histoToCounter(histo):
    ret = []

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret.append( (histo.GetXaxis().GetBinLabel(bin),
                     Count(float(histo.GetBinContent(bin)),
                           float(histo.GetBinError(bin)))) )

    return ret

## Transform a list of (name, Count) pairs to a histogram (TH1)
def _counterToHisto(name, counter):
    histo = ROOT.TH1F(name, name, len(counter), 0, len(counter))
    histo.Sumw2()

    bin = 1
    for name, count in counter:
        histo.GetXaxis().SetBinLabel(bin, name)
        histo.SetBinContent(bin, count.value())
        histo.SetBinError(bin, count.uncertainty())
        bin += 1

    return histo

## Transform histogram (TH1) to a list of values
def histoToList(histo):
    return [histo.GetBinContent(bin) for bin in xrange(1, histo.GetNbinsX()+1)]


## Transform histogram (TH1) to a dictionary.
#
# The key is taken from the x axis label, and the value is the bin
# content.
def _histoToDict(histo):
    ret = {}

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)

    return ret

## Integrate TH1 to a Count
def histoIntegrateToCount(histo):
    count = Count(0, 0)
    for bin in xrange(0, histo.GetNbinsX()+2):
        count.add(Count(histo.GetBinContent(bin), histo.GetBinError(bin)))
    return count

## Rescales info dictionary.
# 
# Assumes that d has a 'control' key for a numeric value, and then
# normalizes all items in the dictionary such that the 'control'
# becomes one.
# 
# The use case is to have a dictionary from _histoToDict() function,
# where the original histogram is merged from multiple jobs. It is
# assumed that each histogram as a one bin with 'control' label, and
# the value of this bin is 1 for each job. Then the bin value for
# the merged histogram tells the number of jobs. Naturally the
# scheme works correctly only if the histograms from jobs are
# identical, and hence is appropriate only for dataset-like
# information.
def _rescaleInfo(d):
    factor = 1/d["control"]

    ret = {}
    for k, v in d.iteritems():
        ret[k] = v*factor

    return ret


## Normalize TH1 to unit area.
# 
# \param h   TH1 histogram
# 
# \return Normalized histogram (same as the argument object, i.e. no copy is made).
def _normalizeToOne(h):
    integral = h.Integral(0, h.GetNbinsX()+1)
    if integral == 0:
        return h
    else:
        return _normalizeToFactor(h, 1.0/integral)

## Scale TH1 with a given factor.
# 
# \param h   TH1 histogram
# \param f   Scale factor
# 
# TH1.Sumw2() is called before the TH1.Scale() in order to scale the
# histogram errors correctly.
def _normalizeToFactor(h, f):
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    h.Sumw2() # errors are also scaled after this call 
    ROOT.gErrorIgnoreLevel = backup
    h.Scale(f)
    return h


## Helper function for merging/stacking a set of datasets.
# 
# \param datasetList  List of all Dataset objects to consider
# \param nameList     List of the names of Dataset objects to merge/stack
# \param task         String to identify merge/stack task (can be 'stack' or 'merge')
# 
# \return a triple of:
# - list of selected Dataset objects
# - list of non-selected Dataset objects
# - index of the first selected Dataset object in the original list
#   of all Datasets
# 
# The Datasets to merge/stack are selected from the list of all
# Datasets, and it is checked that all of them are either data or MC
# (i.e. merging/stacking of data and MC datasets is forbidden).
# """
def _mergeStackHelper(datasetList, nameList, task):
    if not task in ["stack", "merge"]:
        raise Exception("Task can be either 'stack' or 'merge', was '%s'" % task)

    selected = []
    notSelected = []
    firstIndex = None
    dataCount = 0
    mcCount = 0

    for i, d in enumerate(datasetList):
        if d.getName() in nameList:
            selected.append(d)
            if firstIndex == None:
                firstIndex = i
            if d.isData():
                dataCount += 1
            elif d.isMC():
                mcCount += 1
            else:
                raise Exception("Internal error!")
        else:
            notSelected.append(d)

    if dataCount > 0 and mcCount > 0:
        raise Exception("Can not %s data and MC datasets!" % task)

    if len(selected) != len(nameList):
        dlist = nameList[:]
        for d in selected:
            ind = dlist.index(d.getName())
            del dlist[ind]
        print >> sys.stderr, "WARNING: Tried to %s '"%task + ", ".join(dlist) +"' which don't exist"

    return (selected, notSelected, firstIndex)


_th1_re = re.compile(">>\s*(?P<name>\S+)\s*\((?P<nbins>\S+)\s*,\s*(?P<min>\S+)\s*,\s*(?P<max>\S+)\s*\)")
_th1name_re = re.compile(">>\s*(?P<name>\S+)")
## Helper class for obtaining histograms from TTree
#
# This class provides an easy way to get a histogram from a TTree. It
# is inteded to be used with dataset.Dataset.getDatasetRootHisto()
# such that instead of giving the name of the histogram, an object of
# this class is given instead. dataset.Dataset.getDatasetRootHisto()
# will then call the draw() method of this class for actually
# producing the histogram.
#
# TreeDraw objects can easily be cloned from existing TreeDraw object
# with the clone() method. This method allows overriding the
# parameters given in constructor.
#
# Note that TreeDraw does not hold any results or TTree objects, only
# the recipe to produce a histogram from a TTree.
class TreeDraw:
    ## Constructor
    #
    # \param tree       Path to the TTree object in a file
    # \param varexp     Expression for the variable, if given it should also include the histogram name and binning explicitly.
    # \param selection  Draw only those entries passing this selection
    # \param weight     Weight the entries with this weight
    #
    # If varexp is not given, the number of entries passing selection
    # is counted (ignoring weight). In this case the returned TH1 has
    # 1 bin, which contains the event count and the uncertainty of the
    # event count (calculated as sqrt(N)).
    def __init__(self, tree, varexp="", selection="", weight=""):
        self.tree = tree
        self.varexp = varexp
        self.selection = selection
        self.weight = weight

    ## Clone a TreeDraw
    #
    # <b>Keyword arguments</b> are the same as for the constructor (__init__())
    #
    # If any of the values of the keyword arguments is a function (has
    # attribute __call__), the function is called with the current
    # value as an argument, and the return value is assigned to the
    # corresponding name.
    def clone(self, **kwargs):
        args = {"tree": self.tree,
                "varexp": self.varexp,
                "selection": self.selection,
                "weight": self.weight}
        args.update(kwargs)

        # Allow modification functions
        for name, value in args.items():
            if hasattr(value, "__call__"):
                args[name] = value(getattr(self, name))

        return TreeDraw(**args)

    ## Prodouce TH1 from a file
    #
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset, the output TH1 contains
    #                     this in the name. Mainly needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, rootFile, datasetName):
        if self.varexp != "" and not ">>" in self.varexp:
            raise Exception("varexp should include explicitly the histogram binning (%s)"%self.varexp)

        selection = self.selection
        if len(self.weight) > 0:
            if len(selection) > 0:
                selection = "%s * (%s)" % (self.weight, selection)
            else:
                selection = self.weight

        tree = rootFile.Get(self.tree)
        if tree == None:
            raise Exception("No TTree '%s' in file %s" % (self.tree, rootFile.GetName()))

        if self.varexp == "":
            nentries = tree.GetEntries(selection)
            h = ROOT.TH1F("nentries", "Number of entries by selection %s"%selection, 1, 0, 1)
            h.SetDirectory(0)
            if len(self.weight) > 0:
                h.Sumw2()
            h.SetBinContent(1, nentries)
            h.SetBinError(1, math.sqrt(nentries))
            return h

        varexp = self.varexp
        m = _th1_re.search(varexp)
        h = None
        #if m:
        #    varexp = _th1_re.sub(">>"+m.group("name"), varexp)
        #    h = ROOT.TH1D(m.group("name"), varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
        
        # e to have TH1.Sumw2() to be called before filling the histogram
        # goff to not to draw anything on the screen
        opt = ""
        if len(self.weight) > 0:
            opt = "e "
        option = opt+"goff"
        nentries = tree.Draw(varexp, selection, option)
        if nentries < 0:
            raise Exception("Error when calling TTree.Draw with\ntree:       %s\nvarexp:     %s\nselection:  %s\noption:     %s" % (self.tree, varexp, selection, option))
        h = tree.GetHistogram()
        if h != None:
            h = h.Clone(h.GetName()+"_cloned")
        else:
            m = _th1_re.search(varexp)
            if m:
                h = ROOT.TH1F("tmp", varexp, int(m.group("nbins")), float(m.group("min")), float(m.group("max")))
            else:
                m = _th1name_re.search(varexp)
                if m:
                    h = ROOT.gDirectory.Get(m.group("name"))
                    h = h.Clone(h.GetName()+"_cloned")
                    if nentries == 0:
                        h.Scale(0)

                    if h == None:
                        raise Exception("Got null histogram for TTree::Draw() from file %s with selection '%s', unable to infer the histogram limits,  and did not find objectr from gDirectory, from the varexp %s" % (rootFile.GetName(), selection, varexp))
                else:
                    raise Exception("Got null histogram for TTree::Draw() from file %s with selection '%s', and unable to infer the histogram limits or name from the varexp %s" % (rootFile.GetName(), selection, varexp))

        h.SetName(datasetName+"_"+h.GetName())
        h.SetDirectory(0)
        return h


    ## \var tree
    # Path to the TTree object in a file
    ## \var varexp
    # Expression for the variable
    ## \var selection
    # Draw only those entries passing this selection
    ## \var weight
    # Weight the entries with this weight

## Helper class for running code for selected TTree entries
#
# A function is given to the constructor, the function is called for
# each TTree entry passing the selection. The TTree object is given as
# a parameter, leaf/branch data can then be read from it.
#
# Main use case: producing pickEvents list from a TTree
class TreeScan:
    ## Constructor
    #
    # \param tree       Path to the TTree object in a file
    # \param function   Function to call for each TTree entry
    # \param selection  Select only these TTree entries
    def __init__(self, tree, function, selection=""):
        self.tree = tree
        self.function = function
        self.selection = selection

    def clone(self, **kwargs):
        args = {"tree": self.tree,
                "function": self.function,
                "selection": self.selection}
        args.update(kwargs)
        return TreeScan(**args)

    ## Process TTree
    #
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset. Only needed for compatible interface with
    #                     dataset.TreeDrawCompound
    def draw(self, rootFile, datasetName):
        tree = rootFile.Get(self.tree)
        if tree == None:
            raise Exception("No TTree '%s' in file %s" % (self.tree, rootFile.GetName()))

        tree.Draw(">>elist", self.selection)
        elist = ROOT.gDirectory.Get("elist")
        for ientry in xrange(elist.GetN()):
            tree.GetEntry(elist.GetEntry(ientry))
            self.function(tree)

    ## \var tree
    # Path to the TTree object in a file
    ## \var function
    # Function to call for each TTree entry
    ## \var selection
    # Select only these TTree entries

## Provides ability to have separate dataset.TreeDraws for different datasets
#
# One specifies a default dataset.TreeDraw, and the exceptions for that with a
# map from string to dataset.TreeDraw.
class TreeDrawCompound:
    ## Constructor
    #
    # \param default     Default dataset.TreeDraw
    # \param datasetMap  Dictionary for the overriding dataset.TreeDraw objects
    #                    containing dataset names as keys, and TreeDraws as values.
    def __init__(self, default, datasetMap={}):
        self.default = default
        self.datasetMap = datasetMap

    ## Add a new dataset specific dataset.TreeDraw
    #
    # \param datasetName  Name of the dataset
    # \param treeDraw     dataset.TreeDraw object to add
    def add(self, datasetName, treeDraw):
        self.datasetMap[datasetName] = treeDraw

    ## Produce TH1
    #
    # \param rootFile     TFile object containing the TTree
    # \param datasetName  Name of the dataset.
    #
    # The dataset.TreeDraw for which the call is forwarded is searched from
    # the datasetMap with the datasetName. If found, that object is
    # used. If not found, the default TreeDraw is used.
    def draw(self, rootFile, datasetName):
        h = None
        if datasetName in self.datasetMap:
            #print "Dataset %s in datasetMap" % datasetName, self.datasetMap[datasetName].selection
            h = self.datasetMap[datasetName].draw(rootFile, datasetName)
        else:
            #print "Dataset %s with default" % datasetName, self.default.selection
            h = self.default.draw(rootFile, datasetName)
        return h

    ## Clone
    #
    # <b>Keyword arguments</b> are the same as for the clone() method
    # of the contained TreeDraw objects. The new TreeDrawCompoung is
    # constructed such that the default and dataset-specific TreeDraws
    # are cloned with the given keyword arguments.
    def clone(self, **kwargs):
        ret = TreeDrawCompound(self.default.clone(**kwargs))
        for name, td in self.datasetMap.iteritems():
            ret.datasetMap[name] = td.clone(**kwargs)
        return ret

    ## \var default
    # Default dataset.TreeDraw
    ## \var datasetMap
    # Dictionary for the overriding dataset.TreeDraw objects
    # containing dataset names as keys, and TreeDraws as values.

def _treeDrawToNumEntriesSingle(treeDraw):
    var = treeDraw.weight
    if var == "":
        var = treeDraw.selection
    if var != "":
        var += ">>dist(1,0,2)" # the binning is arbitrary, as the under/overflow bins are counted too
    # if selection and weight are "", TreeDraw.draw() returns a histogram with the number of entries
    return treeDraw.clone(varexp=var)

## Maybe unnecessary function?
#
# Seems to be used only from DatasetQCDData class, which was never
# finished.
def treeDrawToNumEntries(treeDraw):
    if isinstance(treeDraw, TreeDrawCompound):
        td = TreeDrawCompound(_treeDrawToNumEntriesSingle(treeDraw.default))
        for name, td2 in treeDraw.datasetMap.iteritems():
            td.add(name, _treeDrawToNumEntriesSingle(td2))
        return td
    else:
        return _treeDrawToNumEntriesSingle(treeDraw)

## Base class for DatasetRootHisto classes (wrapper for TH1 histogram and the originating Dataset)
# 
# The derived class must implement
# _normalizedHistogram()
# which should return the cloned and normalized TH1
#
# The wrapper holds the normalization of the histogram. User should
# set the current normalization scheme with the normalize* methods,
# and then get a clone of the original histogram, which is then
# normalized according to the current scheme.
#
# This makes the class very flexible with respect to the many
# possible normalizations user could want to apply within a plot
# script. The first use case was MC counters, which could be printed
# first normalized to the luminosity of the data, and also
# normalized to the cross section.
#
# The histogram wrapper classes also abstract the signel histogram, and
# merged data and MC histograms behind a common interface.
class DatasetRootHistoBase:
    def __init__(self, dataset):
        self.dataset = dataset
        self.name = dataset.getName()
        self.multiplication = None

    def getDataset(self):
        return self.dataset

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def isData(self):
        return self.dataset.isData()

    def isMC(self):
        return self.dataset.isMC()

    ## Get a clone of the wrapped histogram normalized as requested.
    def getHistogram(self):
        h = self._normalizedHistogram()

        if self.multiplication != None:
            h = _normalizeToFactor(h, self.multiplication)
        return h

    ## Scale the histogram bin values with a value.
    # 
    # \param value    Value to multiply with
    # 
    # h = h*value
    def scale(self, value):
        if self.multiplication == None:
            self.multiplication = value
        else:
            self.multiplication *= value

    ## \var dataset
    # dataset.Dataset object where the histogram originates
    ## \var name
    # Name of the histogram (default is dataset name)
    ## \var multiplication
    # Multiplication factor to be applied after normalization (if None, not applied)

## Wrapper for a single TH1 histogram and the corresponding Dataset.
class DatasetRootHisto(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histo    TH1 histogram
    # \param dataset  Corresponding Dataset object
    # 
    # Sets the initial normalization to 'none'
    def __init__(self, histo, dataset):
        DatasetRootHistoBase.__init__(self, dataset)
        self.histo = histo
        self.normalization = "none"

    ## Get list of the bin labels of the histogram.
    def getBinLabels(self):
        return [x[0] for x in _histoToCounter(self.histo)]

    ## Modify the TH1 with a function
    #
    # \param function              Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto   The other DatasetRootHisto object
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHisto):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHisto")

        self.histo = function(self.histo, newDatasetRootHisto.histo)

    ## Return normalized clone of the original TH1
    def _normalizedHistogram(self):
        # Always return a clone of the original
        h = self.histo.Clone()
        h.SetDirectory(0)
        h.SetName(h.GetName()+"_cloned")
        if self.normalization == "none":
            return h
        elif self.normalization == "toOne":
            return _normalizeToOne(h)

        # We have to normalize to cross section in any case
        h = _normalizeToFactor(h, self.dataset.getNormFactor())
        if self.normalization == "byCrossSection":
            return h
        elif self.normalization == "toLuminosity":
            return _normalizeToFactor(h, self.luminosity)
        else:
            raise Exception("Internal error")

    ## Set the normalization scheme to 'to one'.
    #
    # The histogram is normalized to unit area.
    def normalizeToOne(self):
        self.normalization = "toOne"

    ## Set the current normalization scheme to 'by cross section'.
    #
    # The histogram is normalized to the cross section of the
    # corresponding dataset. The normalization can be applied only
    # to MC histograms.
    def normalizeByCrossSection(self):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram by cross section")
        self.normalization = "byCrossSection"

    ## Set the current normalization scheme to 'to luminosity'.
    #
    # \param lumi   Integrated luminosity in pb^-1 to normalize to
    #
    # The histogram is normalized first normalized to the cross
    # section of the corresponding dataset, and then to a given
    # luminosity. The normalization can be applied only to MC
    # histograms.
    def normalizeToLuminosity(self, lumi):
        if self.dataset.isData():
            raise Exception("Can't normalize data histogram to luminosity")

        self.normalization = "toLuminosity"
        self.luminosity = lumi
    
    ## \var histo
    # Holds the unnormalized ROOT histogram (TH1)
    ## \var normalization
    # String representing the current normalization scheme


## Wrapper for a merged TH1 histograms from data and the corresponding Datasets.
#
# The merged data histograms can only be normalized 'to one'.
#
# \see dataset.DatasetRootHisto class.
class DatasetRootHistoMergedData(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are data, and
    # are not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoBase.__init__(self, mergedDataset)

        self.histoWrappers = histoWrappers
        self.normalization = "none"
        for h in self.histoWrappers:
            if not h.isData():
                raise Exception("Histograms to be merged must come from data (%s is not data)" % h.getDataset().getName())
            if h.normalization != "none":
                raise Exception("Histograms to be merged must not be normalized at this stage")
            if h.multiplication != None:
                raise Exception("Histograms to be merged must not be multiplied at this stage")

    def isData(self):
        return True

    def isMC(self):
        return False

    ## Modify the TH1 with a function
    #
    # \param function             Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto  The other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedData):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedData")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    ## Get list of the bin labels of the first of the merged histogram.
    def getBinLabels(self):
        return self.histoWrappers[0].getBinLabels()

    ## Set the current normalization scheme to 'to one'.
    #
    # The histogram is normalized to unit area.
    def normalizeToOne(self):
        self.normalization = "toOne"

   ## Calculate the sum of the histograms (i.e. merge).
   # 
   # Intended for internal use only.
    def _getSumHistogram(self):
        hsum = self.histoWrappers[0].getHistogram() # we get a clone
        for h in self.histoWrappers[1:]:
            if h.getHistogram().GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.GetName(), self.histoWrappers[0].getDataset().getName(), h.getDataset().getName(), hsum.GetNbinsX(), h.getHistogram().GetNbinsX()))

            hsum.Add(h.getHistogram())
        return hsum

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    def _normalizedHistogram(self):
        hsum = self._getSumHistogram()
        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


## Wrapper for a merged TH1 histograms from MC and the corresponding Datasets.
# 
# See also the documentation of DatasetRootHisto class.
class DatasetRootHistoMergedMC(DatasetRootHistoBase):
    ## Constructor.
    # 
    # \param histoWrappers   List of dataset.DatasetRootHisto objects to merge
    # \param mergedDataset   The corresponding dataset.DatasetMerged object
    # 
    # The constructor checks that all histoWrappers are MC, and are
    # not yet normalized.
    def __init__(self, histoWrappers, mergedDataset):
        DatasetRootHistoBase.__init__(self, mergedDataset)
        self.histoWrappers = histoWrappers
        self.normalization = "none"
        for h in self.histoWrappers:
            if not h.isMC():
                raise Exception("Histograms to be merged must come from MC")
            if h.normalization != "none":
                raise Exception("Histograms to be merged must not be normalized at this stage")
            if h.multiplication != None:
                raise Exception("Histograms to be merged must not be multiplied at this stage")

    def isData(self):
        return False

    def isMC(self):
        return True

    ## Modify the TH1 with a function
    #
    # \param function   Function taking the original TH1 and some other DatasetRootHisto object as input, returning a new TH1
    # \param newDatasetRootHisto  The other DatasetRootHisto object, must be the same type and contain same number of DatasetRootHisto objects
    #
    # Needed for appending rows to counters from TTree
    def modifyRootHisto(self, function, newDatasetRootHisto):
        if not isinstance(newDatasetRootHisto, DatasetRootHistoMergedMC):
            raise Exception("newDatasetRootHisto must be of the type DatasetRootHistoMergedMC")
        if not len(self.histoWrappers) == len(newDatasetRootHisto.histoWrappers):
            raise Exception("len(self.histoWrappers) != len(newDatasetrootHisto.histoWrappers), %d != %d" % len(self.histoWrappers), len(newDatasetRootHisto.histoWrappers))
            
        for i, drh in enumerate(self.histoWrappers):
            drh.modifyRootHisto(function, newDatasetRootHisto.histoWrappers[i])

    ## Get list of the bin labels of the first of the merged histogram.
    def getBinLabels(self):
        return self.histoWrappers[0].getBinLabels()

    ## Set the current normalization scheme to 'to one'.
    # 
    # The histogram is normalized to unit area.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section' in order
    # to be able to sum them. The normalization 'to one' is then done
    # for the summed histogram.
    def normalizeToOne(self):
        self.normalization = "toOne"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    ## Set the current normalization scheme to 'by cross section'.
    # 
    # The histogram is normalized to the cross section of the
    # corresponding dataset.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'by cross section'. Then
    # they can be summed directly, and the summed histogram is
    # automatically correctly normalized to the total cross section of
    # the merged dataset.Dataset objects.
    def normalizeByCrossSection(self):
        self.normalization = "byCrossSection"
        for h in self.histoWrappers:
            h.normalizeByCrossSection()

    ## Set the current normalization scheme to 'to luminosity'.
    # 
    # \param lumi   Integrated luminosity in pb^-1 to normalize to
    # 
    # The histogram is normalized first normalized to the cross
    # section of the corresponding dataset, and then to a given
    # luminosity.
    # 
    # Sets the normalization of the underlying
    # dataset.DatasetRootHisto objects to 'to luminosity'. Then they
    # can be summed directly, and the summed histogram is
    # automatically correctly normalized to the given integrated
    # luminosity. """
    def normalizeToLuminosity(self, lumi):
        self.normalization = "toLuminosity"
        for h in self.histoWrappers:
            h.normalizeToLuminosity(lumi)

    ## Merge the histograms and apply the current normalization.
    # 
    # The returned histogram is a clone, so client code can do
    # anything it wishes with it.
    # 
    # The merged MC histograms must be normalized in some way,
    # otherwise they can not be summed (or they can be, but the
    # contents of the summed histogram doesn't make any sense as it
    # is just the sum of the MC events of the separate datasets
    # which in general have different cross sections).
    def _normalizedHistogram(self):
        if self.normalization == "none":
            raise Exception("Merged MC histograms must be normalized to something!")

        hsum = self.histoWrappers[0].getHistogram() # we get a clone
        for h in self.histoWrappers[1:]:
            if h.getHistogram().GetNbinsX() != hsum.GetNbinsX():
                raise Exception("Histogram '%s' from datasets '%s' and '%s' have different binnings: %d vs. %d" % (hsum.getHistogram().GetName(), self.histoWrappers[0].getHistogram().getName(), h.getDataset().getName(), hsum.GetNbinsX(), h.getHistogram().GetNbinsX()))

            hsum.Add(h.getHistogram())

        if self.normalization == "toOne":
            return _normalizeToOne(hsum)
        else:
            return hsum

    ## \var histoWrappers
    # List of underlying dataset.DatasetRootHisto objects
    ## \var normalization
    # String representing the current normalization scheme


## Dataset class for histogram access from one ROOT file.
# 
# The default values for cross section/luminosity are read from
# 'configInfo/configInfo' histogram (if it exists). The data/MC
# datasets are differentiated by the existence of 'crossSection'
# (for MC) and 'luminosity' (for data) keys in the histogram. Reads
# the dataVersion from 'configInfo/dataVersion' and deduces whether
# the dataset is data/MC from it.
#
# \see dataset.DatasetMerged for merging multiple Dataset objects
# (either data or MC) to one logical dataset (e.g. all data datasets
# to one dataset, all QCD pThat bins to one dataset)
class Dataset:
    ## Constructor.
    # 
    # \param name              Name of the dataset (can be anything)
    # \param fname             Path to the ROOT file of the dataset
    # \param counterDir        Name of the directory in the ROOT file for
    #                          event counter histograms. If None is given, it
    #                          is assumed that the dataset has no counters.
    #                          This also means that the histograms from this
    #                          dataset can not be normalized unless the
    #                          number of all events is explictly set with
    #                          setNAllEvents() method. Note that this
    #                          directory should *not* point to the 'weighted'
    #                          subdirectory, but to the top-level counter
    #                          directory. The weighted counters are taken
    #                          into account with \a useWeightedCounters
    #                          argument
    # \param weightedCounters  If True, pick the counters from the 'weighted' subdirectory
    # 
    # Opens the ROOT file, reads 'configInfo/configInfo' histogram
    # (if it exists), and reads the main event counter
    # ('counterDir/counters') if counterDir is not None. Reads also
    # 'configInfo/dataVersion' TNamed.
    # """
    def __init__(self, name, fname, counterDir, weightedCounters=True):
        self.name = name
        self._setBaseDirectory(os.path.dirname(os.path.dirname(os.path.dirname(fname))))
        self.file = ROOT.TFile.Open(fname)
        if self.file == None:
            raise Exception("Unable to open ROOT file '%s'"%fname)

        configInfo = self.file.Get("configInfo")
        if configInfo == None:
            raise Exception("configInfo directory is missing from file %s" % fname)

        self.info = _rescaleInfo(_histoToDict(self.file.Get("configInfo").Get("configinfo")))

        dataVersion = configInfo.Get("dataVersion")
        if dataVersion == None:
            raise Exception("Unable to determine dataVersion for dataset %s from file %s" % (name, fname))
        self.dataVersion = dataVersion.GetTitle()

        era = configInfo.Get("era")
        if era == None:
            self.era = None
        else:
            self.era = era.GetTitle()

        self._isData = "data" in self.dataVersion

        if counterDir != None:
            self.counterDir = counterDir
            self._origCounterDir = counterDir
            d = self.file.Get(counterDir)
            if d == None:
                raise Exception("Could not find counter directory %s from file %s" % (counterDir, fname))
            ctr = _histoToCounter(d.Get("counter"))
            self.nAllEventsUnweighted = ctr[0][1].value() # first counter, second element of the tuple
            self.nAllEventsWeighted = None

            self.nAllEvents = self.nAllEventsUnweighted

            if weightedCounters:
                self.counterDir += "/weighted"
                d = self.file.Get(self.counterDir)
                if d == None:
                    raise Exception("Could not find counter directory %s from file %s" % (self.counterDir, fname))
                ctr = _histoToCounter(d.Get("counter"))
                self.nAllEventsWeighted = ctr[0][1].value() # first counter, second element of the tuple

                self.nAllEvents = self.nAllEventsWeighted

    ## Close the file
    #
    # Can be useful when opening very many files in order to reduce
    # the memory footprint and not hit the limit of number of open
    # files
    def close(self):
#        print "Closing", self.file.GetName()
        self.file.Close("R")
        self.file.Delete()
        del self.file

    ## Clone the Dataset object
    # 
    # Nothing is shared between the returned copy and this object.
    #
    # Use case is creative dataset manipulations, e.g. copying ttbar
    # to another name and scaling the cross section by the BR(t->H+)
    # while also keeping the original ttbar with the original SM cross
    # section.
    def deepCopy(self):
        d = Dataset(self.name, self.file.GetName(), self._origCounterDir, self.nAllEventsWeighted != None)
        d.info.update(self.info)
        return d

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    ## Set cross section of MC dataset (in pb).
    def setCrossSection(self, value):
        if not self.isMC():
            raise Exception("Should not set cross section for data dataset %s" % self.name)
        self.info["crossSection"] = value

    ## Get cross section of MC dataset (in pb).
    def getCrossSection(self):
        if not self.isMC():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        try:
            return self.info["crossSection"]
        except KeyError:
            raise Exception("Dataset %s is MC, but 'crossSection' is missing from configInfo/configInfo histogram. You have to explicitly set the cross section with setCrossSection() method." % self.name)

    ## Set the integrated luminosity of data dataset (in pb^-1).
    def setLuminosity(self, value):
        if not self.isData():
            raise Exception("Should not set luminosity for MC dataset %s" % self.name)
        self.info["luminosity"] = value

    ## Get the integrated luminosity of data dataset (in pb^-1).
    def getLuminosity(self):
        if not self.isData():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        try:
            return self.info["luminosity"]
        except KeyError:
            raise Exception("Dataset %s is data, but luminosity has not been set yet. You have to explicitly set the luminosity with setLuminosity() method." % self.name)

    def isData(self):
        return self._isData

    def isMC(self):
        return not self._isData

    def getCounterDirectory(self):
        return self.counterDir

    ## Set the number of all events (for normalization).
    #
    # This allows both overriding the value read from the event
    # counter, or creating a dataset without event counter at all.
    def setNAllEvents(self, nAllEvents):
        self.nAllEvents = nAllEvents

    ## Update number of all events (for normalization) to a pileup-reweighted value.
    #
    # \param era     Data era to use to pick the pile-up-reweighted all
    #                event number (optional, if not given a default
    #                value read from the configinfo is used)
    # \param kwargs  Keyword arguments (forwarded to WeightedAllEvents.getWeighted())
    def updateNAllEventsToPUWeighted(self, era=None, **kwargs):
        # Ignore if data
        if self.isData():
            return

        if era == None:
            era = self.era
        if era == None:
            raise Exception("%s: tried to update number of all events to pile-up reweighted value, but the data era was not set in 'configInfo' nor was given as an argument" % self.getName())

        try:
            data = _weightedAllEvents[era]
        except KeyError:
            raise Exception("No weighted numbers of all events specified for data era '%s', see dataset._weightedAllEvents dictionary" % era)

        try:
            self.nAllEvents = data[self.getName()].getWeighted(self.getName(), self.nAllEventsUnweighted, **kwargs)
        except KeyError:
            # Just ignore if no weights found for this dataset
            pass

    def getNAllEvents(self):
        return self.nAllEvents

    ## Get the cross section normalization factor.
    #
    # The normalization factor is defined as crossSection/N(all
    # events), so by multiplying the number of MC events with the
    # factor one gets the corresponding cross section.
    def getNormFactor(self):
        if not hasattr(self, "nAllEvents"):
            raise Exception("Number of all events is not set for dataset %s! The counter directory was not given, and setNallEvents() was not called." % self.name)
        if self.nAllEvents == 0:
            raise Exception("%s: Number of all events is 0.\nProbable cause is that the counters are weighted, the analysis job input was a skim, and the updateAllEventsToPUWeighted() has not been called." % self.name)

        return self.getCrossSection() / self.nAllEvents

    ## Check if a ROOT histogram exists in this dataset
    #
    # \param name  Name (path) of the ROOT histogram
    #
    # If dataset.TreeDraw object is given, it is considered to always
    # exist.
    def hasRootHisto(self, name):
        if hasattr(name, "draw"):
            return True
        pname = name
        return self.file.Get(pname) != None

    ## Get the dataset.DatasetRootHisto object for a named histogram.
    # 
    # \param name   Path of the histogram in the ROOT file
    #
    # \return dataset.DatasetRootHisto object containing the (unnormalized) TH1 and this Dataset
    # 
    # If dataset.TreeDraw object is given (or actually anything with
    # draw() method), the draw() method is called by giving the TFile
    # and the dataset name as parameters. The draw() method is
    # expected to return a TH1 which is then returned.
    def getDatasetRootHisto(self, name):
        h = None
        if hasattr(name, "draw"):
            h = name.draw(self.file, self.getName())
        else:
            pname = name
            h = self.file.Get(pname)
            if h == None:
                raise Exception("Unable to find histogram '%s' from file '%s'" % (pname, self.file.GetName()))

            name = h.GetName()+"_"+self.name
            h.SetName(name.translate(None, "-+.:;"))
        return DatasetRootHisto(h, self)

    ## Get the directory content of a given directory in the ROOT file.
    # 
    # \param directory   Path of the directory in the ROOT file
    # \param predicate   Append the directory name to the return list only if
    #                    predicate returns true for the name. Predicate
    #                    should be a function taking a string as an
    #                    argument and returning a boolean.
    # 
    # \return List of names in the directory.
    def getDirectoryContent(self, directory, predicate=lambda x: True):
        d = self.file.Get(directory)
        if d == None:
            raise Exception("No object %s in file %s" % (directory, self.file.GetName()))
        dirlist = d.GetListOfKeys()

        # Suppress the warning message of missing dictionary for some iterator
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        diriter = dirlist.MakeIterator()
        ROOT.gErrorIgnoreLevel = backup

        key = diriter.Next()

        ret = []
        while key:
            if predicate(key.ReadObj()):
                ret.append(key.GetName())
            key = diriter.Next()
        return ret

    def _setBaseDirectory(self,base):
        self.basedir = base
        
    ## \var name
    # Name of the dataset
    ## \var file
    # TFile object of the dataset
    ## \var info
    # Dictionary containing the configInfo histogram
    ## \var dataVersion
    # dataVersion string of the dataset (from TFile)
    ## \var era
    # Era of the data (used in the analysis for pile-up reweighting,
    # trigger efficiencies etc). Is None if corresponding TNamed
    # doesn't exist in configinfo directory
    ## \var nAllEvents
    # Number of all MC events, used in MC normalization
    ## \var nAllEventsUnweighted
    # Number of all MC events as read from the unweighted counter.
    # This should always be a non-zero number
    ## \var nAllEventsWeighted
    # Number of all MC events as read from the weighted counter. This
    # can be None (if weightedCounters was False in __init__()), zero
    # (if the input for the analysis job was a skim), or a non-zero
    # number (if the input for the anlysis job was not a skim)
    ## \var counterDir
    # Name of TDirectory containing the main event counter
    ## \var _origCounterDir
    # Name of the counter directory as given for __init__(), needed for deepCopy()
    ## \var _isData
    # If true, dataset is from data, if false, from MC


## Dataset class for histogram access for a dataset merged from Dataset objects.
# 
# The merged datasets are required to be either MC or data.
class DatasetMerged:
    ## Constructor.
    # 
    # \param name      Name of the merged dataset
    # \param datasets  List of dataset.Dataset objects to merge
    # 
    # Calculates the total cross section (luminosity) for MC (data)
    # datasets.
    def __init__(self, name, datasets):
        self.name = name
        #self.stacked = stacked
        self.datasets = datasets
        if len(datasets) == 0:
            raise Exception("Can't create a DatasetMerged from 0 datasets")

        self.info = {}

        if self.datasets[0].isMC():
            crossSum = 0.0
            for d in self.datasets:
                crossSum += d.getCrossSection()
            self.info["crossSection"] = crossSum
        else:
            lumiSum = 0.0
            for d in self.datasets:
                lumiSum += d.getLuminosity()
            self.info["luminosity"] = lumiSum

    ## Close TFiles in the contained dataset.Dataset objects
    def close(self):
        for d in self.datasets:
            d.close()

    ## Make a deep copy of a DatasetMerged object.
    #
    # Nothing is shared between the returned copy and this object.
    #
    # \see dataset.Dataset.deepCopy()
    def deepCopy(self):
        dm = DatasetMerged(self.name, [d.deepCopy() for d in self.datasets])
        dm.info.update(self.info)
        return dm

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setCrossSection(self, value):
        if self.isData():
            raise Exception("Should not set cross section for data dataset %s (has luminosity)" % self.name)
        raise Exception("Setting cross section for merged dataset is meaningless (it has no real effect, and hence is misleading")

    ## Get cross section of MC dataset (in pb).
    def getCrossSection(self):
        if self.isData():
            raise Exception("Dataset %s is data, no cross section available" % self.name)
        return self.info["crossSection"]

    def setLuminosity(self, value):
        if self.isMC():
            raise Exception("Should not set luminosity for MC dataset %s (has crossSection)" % self.name)
        raise Exception("Setting luminosity for merged dataset is meaningless (it has no real effect, and hence is misleading")

    ## Get the integrated luminosity of data dataset (in pb^-1).
    def getLuminosity(self):
        if self.isMC():
            raise Exception("Dataset %s is MC, no luminosity available" % self.name)
        return self.info["luminosity"]

    def isData(self):
        return self.datasets[0].isData()

    def isMC(self):
        return self.datasets[0].isMC()

    def getCounterDirectory(self):
        countDir = self.datasets[0].getCounterDirectory()
        for d in self.datasets[1:]:
            if countDir != d.getCounterDirectory():
                raise Exception("Error: merged datasets have different counter directories")
        return countDir

    def getNormFactor(self):
        return None

    ## Check if a ROOT histogram exists in this dataset
    #
    # \param name  Name (path) of the ROOT histogram
    #
    # The ROOT histogram is expected to exist in all underlying
    # dataset.Dataset objects.
    def hasRootHisto(self, name):
        has = True
        for d in self.datasets:
            has = has and d.hasRootHisto(name)
        return has

    ## Get the DatasetRootHistoMergedMC/DatasetRootHistoMergedData object for a named histogram.
    #
    # \param name   Path of the histogram in the ROOT file
    def getDatasetRootHisto(self, name):
        wrappers = [d.getDatasetRootHisto(name) for d in self.datasets]
        if self.isMC():
            return DatasetRootHistoMergedMC(wrappers, self)
        else:
            return DatasetRootHistoMergedData(wrappers, self)

        
    ## Get the directory content of a given directory in the ROOT file.
    # 
    # \param directory   Path of the directory in the ROOT file
    # \param predicate   Append the directory name to the return list only if
    #                    predicate returns true for the name. Predicate
    #                    should be a function taking a string as an
    #                    argument and returning a boolean.
    # 
    # Returns a list of names in the directory. The contents of the
    # directories of the merged datasets are required to be identical.
    def getDirectoryContent(self, directory, predicate=lambda x: True):
        content = self.datasets[0].getDirectoryContent(directory, predicate)
        for d in self.datasets[1:]:
            if content != d.getDirectoryContent(directory, predicate):
                raise Exception("Error: merged datasets have different contents in directory '%s'" % directory)
        return content

    ## \var name
    # Name of the merged dataset
    ## \var datasets
    # List of merged dataset.Dataset objects
    ## \var info
    # Dictionary containing total cross section (MC) or integrated luminosity (data)

## Collection of Dataset objects which are managed together.
# 
# Holds both an ordered list of Dataset objects, and a name->object
# map for convenient access by dataset name.
#
# \todo The code structure could be simplified by getting rid of
# dataset.DatasetRootHisto. This would mean that the MC normalisation
# should be handled in dataset.DatasetManagager and dataset.Dataset,
# with an interface similar to what dataset.DatasetRootHisto and
# histograms.HistoManager provide now (i.e. user first sets the
# normalisation scheme, and then asks histograms which are then
# normalised as requested). dataset.Dataset and dataset.DatasetManager
# should then return ROOT TH1s, with which user is free to do what
# (s)he wants. histograms.HistoManager and histograms.HistoManagerImpl
# could be merged, as it would take already-normalized histograms as
# input (the input should still be histograms.Histo classes in order
# to give user freedom to provide fully customized version of such
# wrapper class if necessary). The interface of plots.PlotBase would
# still accept TH1/TGraph, so no additional burden would appear for
# the usual use cases with plots. The information of a histogram being
# data/MC in histograms.Histo could also be removed (as it is
# sometimes too restrictive), and the use in plots.PlotBase (and
# deriving classes) could be transformed to identify the data/MC
# datasets (for default formatting purposes) by the name of the
# histograms (in the usual workflow the histograms have the dataset
# name), with the possibility that user can easily modify the names of
# data/MC histograms. This would bring more flexibility on that front,
# and easier customization when necessary.
class DatasetManager:
    ## Constructor
    #
    # \param base    Directory (absolute/relative to current working
    #                directory) where the luminosity JSON file is located (see
    #                loadLuminosities())
    #
    # DatasetManager is constructed as empty
    def __init__(self, base=""):
        self.datasets = []
        self.datasetMap = {}
        self._setBaseDirectory(base)

    ## Populate the datasetMap member from the datasets list.
    # 
    # Intended only for internal use.
    def _populateMap(self):
        self.datasetMap = {}
        for d in self.datasets:
            self.datasetMap[d.getName()] = d

    def _setBaseDirectory(self, base):
        for d in self.datasets:
            d._setBaseDirectory(base)

    ## Close all TFiles of the contained dataset.Dataset objects
    #
    # \see dataset.Dataset.close()
    def close(self):
        for d in self.datasets:
            d.close()

    ## Append a Dataset object to the set.
    # 
    # \param dataset    Dataset object
    # 
    # The new Dataset must have a different name than the already existing ones.
    def append(self, dataset):
        if dataset.getName() in self.datasetMap:
            raise Exception("Dataset '%s' already exists in this DatasetManager" % dataset.getName())

        self.datasets.append(dataset)
        self.datasetMap[dataset.getName()] = dataset

    ## Extend the set of Datasets from another DatasetManager object.
    # 
    # \param datasetmgr   DatasetManager object
    # 
    # Note that the dataset.Dataset objects of datasetmgr are appended to
    # self by reference, i.e. the Dataset objects will be shared
    # between them.
    # """
    def extend(self, datasetmgr):
        for d in datasetmgr.datasets:
            self.append(d)

    ## Make a shallow copy of the DatasetManager object.
    # 
    # The dataset.Dataset objects are shared between the DatasetManagers.
    #
    # Useful e.g. if you want to have a subset of the dataset.Dataset objects
    def shallowCopy(self):

        copy = DatasetManager()
        copy.extend(self)
        return copy

    ## Make a deep copy of the DatasetManager object.
    # 
    # Nothing is shared between the DatasetManagers.
    #
    # Useful e.g. if you want to have two sets of same datasets, but
    # others are somehow modified (e.g. cross section)
    def deepCopy(self):
        copy = DatasetManager()
        for d in self.datasets:
            copy.append(d.deepCopy())
        return copy

    def hasDataset(self, name):
        return name in self.datasetMap

    def getDataset(self, name):
        return self.datasetMap[name]

    ## Get a list of dataset.DatasetRootHisto objects for a given name.
    # 
    # \param histoName   Path to the histogram in each ROOT file.
    #
    # \see dataset.Dataset.getDatasetRootHisto()
    def getDatasetRootHistos(self, histoName):
        return [d.getDatasetRootHisto(histoName) for d in self.datasets]

    ## Get a list of all dataset.Dataset objects.
    def getAllDatasets(self):
        return self.datasets

    ## Get a list of MC dataset.Dataset objects.
    #
    # \todo Implementation would be simpler with filter() method
    def getMCDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isMC():
                ret.append(d)
        return ret

    ## Get a list of data dataset.Dataset objects.
    #
    # \todo Implementation would be simpler with filter() method
    def getDataDatasets(self):
        ret = []
        for d in self.datasets:
            if d.isData():
                ret.append(d)
        return ret

    ## Get a list of names of all dataset.Dataset objects.
    def getAllDatasetNames(self):
        return [x.getName() for x in self.getAllDatasets()]

    ## Get a list of names of MC dataset.Dataset objects."""
    def getMCDatasetNames(self):
        return [x.getName() for x in self.getMCDatasets()]

    ## Get a list of names of data dataset.Dataset objects.
    def getDataDatasetNames(self):
        return [x.getName() for x in self.getDataDatasets()]

    ## Select and reorder Datasets.
    # 
    # \param nameList   Ordered list of Dataset names to select
    # 
    # This method can be used to either select a set of
    # dataset.Dataset objects. reorder them, or both.
    def selectAndReorder(self, nameList):
        selected = []
        for name in nameList:
            try:
                selected.append(self.datasetMap[name])
            except KeyError:
                print >> sys.stderr, "WARNING: Dataset selectAndReorder: dataset %s doesn't exist" % name

        self.datasets = selected
        self._populateMap()

    ## Remove dataset.Dataset objects
    # 
    # \param nameList    List of dataset.Dataset names to remove
    # \param close       If true, close the removed dataset.Dataset objects
    def remove(self, nameList, close=True):
        if isinstance(nameList, basestring):
            nameList = [nameList]

        selected = []
        for d in self.datasets:
            if not d.getName() in nameList:
                selected.append(d)
            else:
                d.close()
        self.datasets = selected
        self._populateMap()

    ## Rename a Dataset.
    # 
    # \param oldName   The current name of a dataset.Dataset
    # \param newName   The new name of a dataset.Dataset
    def rename(self, oldName, newName):
        if oldName == newName:
            return

        if newName in self.datasetMap:
            raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))
        self.datasetMap[oldName].setName(newName)
        self._populateMap()

    ## Rename many dataset.Dataset objects
    # 
    # \param nameMap   Dictionary containing oldName->newName mapping
    # \param silent    If true, don't raise Exception if source dataset doesn't exist
    #
    # \see rename()
    def renameMany(self, nameMap, silent=False):
        for oldName, newName in nameMap.iteritems():
            if oldName == newName:
                continue

            if newName in self.datasetMap:
                raise Exception("Trying to rename datasets '%s' to '%s', but a dataset with the new name already exists!" % (oldName, newName))

            try:
                self.datasetMap[oldName].setName(newName)
            except KeyError, e:
                if not silent:
                    raise Exception("Trying to rename dataset '%s' to '%s', but '%s' doesn't exist!" % (oldName, newName, oldName))
        self._populateMap()

    ## Merge all data dataset.Dataset objects to one with a name 'Data'.
    #
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeData(self, *args, **kwargs):
        self.merge("Data", self.getDataDatasetNames(), *args, **kwargs)

    ## Merge all MC dataset.Datasetobjects to one with a name 'MC'.
    #
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeMC(self, *args, **kwargs):
        self.merge("MC", self.getMCDatasetNames(), *args, **kwargs)

    ## Merge datasets according to the mapping.
    #
    # \param mapping Dictionary of oldName->mergedName mapping. The
    #                dataset.Dataset objects having the same mergedName are merged
    # \param args    Positional arguments (forwarded to merge())
    # \param kwargs  Keyword arguments (forwarded to merge())
    def mergeMany(self, mapping, *args, **kwargs):
        toMerge = {}
        for d in self.datasets:
            if d.getName() in mapping:
                newName = mapping[d.getName()]
                if newName in toMerge:
                    toMerge[newName].append(d.getName())
                else:
                    toMerge[newName] = [d.getName()]

        for newName, nameList in toMerge.iteritems():
            self.merge(newName, nameList, *args, **kwargs)

    ## Merge dataset.Dataset objects.
    # 
    # \param newName      Name of the merged dataset.DatasetMerged
    # \param nameList     List of dataset.Dataset names to merge
    # \param keepSources  If true, keep the original dataset.Dataset
    #                     objects in the list of datasets. Otherwise
    #                     they are removed, as they are now contained
    #                     in the dataset.DatasetMerged object
    #
    # If nameList translates to only one dataset.Dataset, the
    # dataset.Daataset object is renamed (i.e. dataset.DatasetMerged
    # object is not created)
    def merge(self, newName, nameList, keepSources=False):
        (selected, notSelected, firstIndex) = _mergeStackHelper(self.datasets, nameList, "merge")
        if len(selected) == 0:
            print >> sys.stderr, "Dataset merge: no datasets '" +", ".join(nameList) + "' found, not doing anything"
            return
        elif len(selected) == 1:
            print >> sys.stderr, "Dataset merge: one dataset '" + selected[0].getName() + "' found from list '" + ", ".join(nameList)+"', renaming it to '%s'" % newName
            self.rename(selected[0].getName(), newName)
            return

        if not keepSources:
            self.datasets = notSelected
        self.datasets.insert(firstIndex, DatasetMerged(newName, selected))
        self._populateMap()

    ## Load integrated luminosities from a JSON file.
    # 
    # \param fname   Path to the file (default: 'lumi.json'). If the
    #                directory part of the path is empty, the file is
    #                looked from the base directory (which defaults to
    #                current directory)
    # 
    # The JSON file should be formatted like this:
    # \verbatim
    # '{
    #    "dataset_name": value_in_pb,
    #    "Mu_135821-144114": 2.863224758
    #  }'
    # \endverbatim
    # Note: as setting the integrated luminosity for a merged dataset
    # will fail (see dataset.DatasetMerged.setLuminosity()), loading
    # luminosities must be done before merging the data datasets to
    # one.
    def loadLuminosities(self, fname="lumi.json"):
        for d in self.datasets:
            jsonname = os.path.join(d.basedir, fname)
            if not os.path.exists(jsonname):
                print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist!" % jsonname
            data = json.load(open(jsonname))
            for name, value in data.iteritems():
                if self.hasDataset(name):
                    self.getDataset(name).setLuminosity(value)

####        if len(os.path.dirname(fname)) == 0:
####            fname = os.path.join(self.basedir, fname)
####
####        if not os.path.exists(fname):
####            print >> sys.stderr, "WARNING: luminosity json file '%s' doesn't exist!" % fname
####
####        data = json.load(open(fname))
####        for name, value in data.iteritems():
####            if self.hasDataset(name):
####                self.getDataset(name).setLuminosity(value)

    ## Update all event counts to the ones taking into account the pile-up reweighting
    #
    # \param kwargs     Keyword arguments (forwarded to dataset.Dataset.updateAllEventsToWeighted)
    #
    # Uses the table dataset._weightedAllEvents
    def updateNAllEventsToPUWeighted(self, **kwargs):
        for dataset in self.datasets:
            dataset.updateNAllEventsToPUWeighted(**kwargs)

    ## Print dataset information.
    def printInfo(self):
        col1hdr = "Dataset"
        col2hdr = "Cross section (pb)"
        col3hdr = "Norm. factor"
        col4hdr = "Int. lumi (pb^-1)" 

        maxlen = max([len(x.getName()) for x in self.datasets]+[len(col1hdr)])
        c1fmt = "%%-%ds" % (maxlen+2)
        c2fmt = "%%%d.4g" % (len(col2hdr)+2)
        c3fmt = "%%%d.4g" % (len(col3hdr)+2)
        c4fmt = "%%%d.10g" % (len(col4hdr)+2)

        c2skip = " "*(len(col2hdr)+2)
        c3skip = " "*(len(col3hdr)+2)
        c4skip = " "*(len(col4hdr)+2)

        print (c1fmt%col1hdr)+"  "+col2hdr+"  "+col3hdr+"  "+col4hdr
        for dataset in self.datasets:
            line = (c1fmt % dataset.getName())
            if dataset.isMC():
                line += c2fmt % dataset.getCrossSection()
                normFactor = dataset.getNormFactor()
                if normFactor != None:
                    line += c3fmt % normFactor
                else:
                    line += c3skip
            else:
                line += c2skip+c3skip + c4fmt%dataset.getLuminosity()
            print line


    ## \var datasets
    # List of dataset.Dataset (or dataset.DatasetMerged) objects to manage
    ## \var datasetMap
    # Dictionary from dataset names to dataset.Dataset objects, for
    # more straightforward accessing of dataset.Dataset objects by
    # their name.
    ## \var basedir
    # Directory (absolute/relative to current working directory) where
    # the luminosity JSON file is located (see loadLuminosities())
