import math

def leastSquareFitPoly0(values, uncertainties):
    if len(values) != len(uncertainties):
        raise Exception("len(values) != len(uncertainties) (%d != %d)" % len(values), len(uncertainties))

    val = []
    unc2inv = []
    for v, u in zip(values, uncertainties):
        if u == 0:
            continue
        val.append(v)
        unc2inv.append(1/(float(u)**2))

    if len(val) == 0:
        return (None, None, 0, 0)
    if len(val) == 1:
        return (val[0], 1/sqrt(unc2inv), 0, 0)


    a = sum([x*s2i for x, s2i in zip(val, unc2inv)])/sum(unc2inv)
    da = math.sqrt( 1/sum(unc2inv) )

    chi2 = sum([(x-a)**2 *s2i for x, s2i in zip(val, unc2inv)])
    ndof = len(values)-1

    return (a, da, chi2, ndof)

def leastSquareFitPoly0Weights(values, uncertainties):
    if len(values) != len(uncertainties):
        raise Exception("len(values) != len(uncertainties) (%d != %d)" % len(values), len(uncertainties))

    val = []
    unc2inv = []
    for v, u in zip(values, uncertainties):
        if u == 0:
            continue
        val.append(v)
        unc2inv.append(1/(float(u)**2))

    if len(val) == 0:
        return []
    if len(val) == 1:
        return [1]
    return [ s2i/sum(unc2inv) for s2i in unc2inv]
