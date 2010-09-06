import ROOT

def histoToCounter(histo):
    ret = []

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret.append( (histo.GetXaxis().GetBinLabel(bin),
                     long(histo.GetBinContent(bin))) )

    return ret

def histoToDict(histo):
    ret = {}

    for bin in xrange(1, histo.GetNbinsX()+1):
        ret[histo.GetXaxis().GetBinLabel(bin)] = histo.GetBinContent(bin)

    return ret

def rescaleInfo(d):
    factor = 1/d["control"]

    ret = {}
    for k, v in d.iteritems():
        ret[k] = v*factor

    return ret
