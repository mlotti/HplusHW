#!/usr/bin/env python

# https://twiki.cern.ch/twiki/bin/view/CMS/PileupReweighting
# https://twiki.cern.ch/twiki/bin/view/CMS/LumiCalc#How_to_use_script_estimatePileup

# estimatePileup.py --saveRuns --nowarning -i foo.txt --maxPileupBin 50 pileup.root

import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)

# Spring11
# SimGeneral/MixingModule/python/mix_E7TeV_FlatDist10_2011EarlyData_inTimeOnly_cfi.py rev 1.1
mix_E7TeV_FlatDist10_2011EarlyData_inTimeOnly = [0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0630151648,0.0526654164,0.0402754482,0.0292988928,0.0194384503,0.0122016783,0.007207042,0.004003637,0.0020278322,0.0010739954,0.0004595759,0.0002229748,0.0001028162,4.58337152809607E-05]

# Summer11
# SimGeneral/MixingModule/python/mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT.py rev 1.2
mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT = [0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0698146584,0.0630151648,0.0526654164,0.0402754482,0.0292988928,0.0194384503,0.0122016783,0.007207042,0.004003637,0.0020278322,0.0010739954,0.0004595759,0.0002229748,0.0001028162,4.58337152809607E-05]


def main(opts):
    f = ROOT.TFile.Open(opts.file)
    histo = f.Get("pileup")

    # Spring11
    #npu_probs = mix_E7TeV_FlatDist10_2011EarlyData_inTimeOnly
    # Summer11 (the weights seem to be the same as for Spring11
    npu_probs = mix_E7TeV_FlatDist10_2011EarlyData_50ns_PoissonOOT

    weights = generate_weights(npu_probs, histo)

    print "Sum of weights ", sum(weights)
    print "Sum of probs ", sum(npu_probs)
    print "Sum of [weight*prob]", sum([w*p for w, p in zip(weights, npu_probs)])
    weights.append(0)

    print
    print "weights = cms.vdouble(%s)" % ", ".join(["%.8f" % x for x in weights])

def generate_weights(npu_probs, data_npu_estimated):
    result = []
    s = 0.0
    for npu, pu_prob in enumerate(npu_probs):
        npu_estimated = data_npu_estimated.GetBinContent(data_npu_estimated.GetXaxis().FindBin(npu))
        result.append(npu_estimated / pu_prob)
        s += npu_estimated

    # Normalize the weights
    result = [x/s for x in result]
    
    return result

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-f", dest="file", type="string",
                      help="Input ROOT file produced with estimatePileup.py")

    (opts, args) = parser.parse_args()
    sys.exit(main(opts))
