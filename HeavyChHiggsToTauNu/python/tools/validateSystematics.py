# Description: Collection of routines to validate systematics calculation
#
# Authors: LAW

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics

from math import sqrt
import ROOT

## Common validation routine
def validateAll(codeValidator):
    validateSystematics(codeValidator)
    validateRootHistoWithUncertainties(codeValidator)

## Validation routine
def validateSystematics(codeValidator):
    codeValidator.setPackage("tools.systematics.ScalarUncertaintyItem")
    a = systematics.ScalarUncertaintyItem("a",0.123)
    codeValidator.test("name()", a.getName(), "a")
    codeValidator.test("isAsymmetric()", a.isAsymmetric(), False)
    codeValidator.test("getUncertaintyDown()", a.getUncertaintyDown(), 0.123)
    codeValidator.test("getUncertaintyUp()", a.getUncertaintyUp(), 0.123)
    codeValidator.test("getUncertaintySquaredDown()", a.getUncertaintySquaredDown(), 0.123**2)
    codeValidator.test("getUncertaintySquaredUp()", a.getUncertaintySquaredUp(), 0.123**2)
    # Scale
    a.scale(3.0)
    codeValidator.test("getUncertaintyDown() after scale()", a.getUncertaintyDown(), 0.369)
    codeValidator.test("getUncertainty() after scale()", a.getUncertaintyUp(), 0.369)
    # Clone
    aprime = a.Clone()
    codeValidator.test("name() after Clone()", aprime.getName(), "a")
    codeValidator.test("getUncertaintyDown() after Clone()", aprime.getUncertaintyDown(), 0.369)
    codeValidator.test("getUncertaintyUp() after Clone()", aprime.getUncertaintyUp(), 0.369)
    # copy constructor
    b = systematics.ScalarUncertaintyItem("b",a)
    codeValidator.test("getUncertaintyDown() for asymmetric", b.getUncertaintyDown(), 0.369)
    codeValidator.test("getUncertaintyUp() for asymmetric", b.getUncertaintyUp(), 0.369)
    codeValidator.test("isAsymmetric()", b.isAsymmetric(), False)
    # Scale
    b.scale(0.5)
    codeValidator.test("getUncertaintyDown() after Clone()", b.getUncertaintyDown(), 0.1845)
    codeValidator.test("getUncertaintyUp() after Clone()", b.getUncertaintyUp(), 0.1845)
    # two keyword arguments
    c = systematics.ScalarUncertaintyItem("c",plus=0.123,minus=-0.246)
    codeValidator.test("getUncertaintyDown() for kw asymmetric", c.getUncertaintyDown(), -0.246)
    codeValidator.test("getUncertaintyUp() for kw asymmetric", c.getUncertaintyUp(), 0.123)
    codeValidator.test("isAsymmetric()", c.isAsymmetric(), True)
    # Add
    a.add(c)
    codeValidator.test("name()", a.getName(), "a+c")
    codeValidator.test("isAsymmetric()", a.isAsymmetric(), True)
    codeValidator.test("getUncertaintyDown()", a.getUncertaintyDown(), 0.44348281)
    codeValidator.test("getUncertaintyUp()", a.getUncertaintyUp(), 0.388960)

## Validation routine
def validateRootHistoWithUncertainties(codeValidator):
    def createHisto(name, data, dataerr):
        h = ROOT.TH1F(name,name,len(data)-2,0,len(data)-2)
        for i in range(0,len(data)):
            h.SetBinContent(i, data[i])
        for i in range(0,len(dataerr)):
            h.SetBinError(i, dataerr[i])
        return h
    def printHistoContents(h):
        for i in range(0,h.GetNbinsX()+2):
            print i,h.GetBinContent(i),h.GetBinError(i)
    def testHistoContents(name,h,data,dataerr):
        for i in range(0,len(data)):
            codeValidator.test("histoContents(%s) content in bin %d"%(name,i), h.GetBinContent(i), data[i])
        for i in range(0,len(dataerr)):
            codeValidator.test("histoContents(%s) error in bin %d"%(name,i), h.GetBinError(i), dataerr[i])
    def testGraphContents(name,h,data,dataerrup,dataerrdown):
        for i in range(0,len(data)):
            codeValidator.test("graphContents(%s) content in bin %d"%(name,i), g.GetY()[i], data[i])
        for i in range(0,len(dataerrup)):
            codeValidator.test("graphContents(%s) error+ in bin %d"%(name,i), h.GetErrorYhigh(i), dataerrup[i])
            codeValidator.test("graphContents(%s) error- in bin %d"%(name,i), h.GetErrorYlow(i), dataerrdown[i])

    codeValidator.setPackage("tools.dataset.RootHistoWithUncertainties")
    # histogram
    h = createHisto("h",[3.2,6.4,7.6,10.4,5.3],[1.2,2.1,2.3,1.6,2.0])

    rhwu = dataset.RootHistoWithUncertainties(h)
    rhwu.makeFlowBinsVisible()
    testHistoContents("afterFlowBins", rhwu.getRootHisto(), [0.0,9.6,7.6,15.7,0.0], [0.0,2.4186773245,2.3,2.561249695,0.0])
    codeValidator.test("getRate()", rhwu.getRate(), 32.9)
    codeValidator.test("getRateStatUncertainty()", rhwu.getRateStatUncertainty(), 4.2071367936)
    (systUp,systDown) = rhwu.getRateSystUncertainty()
    codeValidator.test("getRateSystUncertainty() up", systUp, 0.0)
    codeValidator.test("getRateSystUncertainty() down", systDown, 0.0)
    # Add a norm. uncertainty
    rhwu.addNormalizationUncertaintyRelative("normA", uncertaintyPlus=0.1, uncertaintyMinus=-0.2)
    testHistoContents("after normA", rhwu.getRootHisto(), [0.0,9.6,7.6,15.7,0.0], [0.0,2.4186773245,2.3,2.561249695,0.0])
    codeValidator.test("getRate()", rhwu.getRate(), 32.9)
    codeValidator.test("getRateStatUncertainty()", rhwu.getRateStatUncertainty(), 4.2071367936)
    (systUp,systDown) = rhwu.getRateSystUncertainty() # this tests also Merge
    codeValidator.test("getRateSystUncertainty() up", systUp, 3.29)
    codeValidator.test("getRateSystUncertainty() down", systDown, 6.58)
    g = rhwu.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6,7.6,15.7], [0.96,0.76,1.57], [1.92,1.52,3.14])
    g = rhwu.getSystematicUncertaintyGraph(addStatistical=True)
    testGraphContents("syst.graph,addStat=True", g, [9.6,7.6,15.7], [2.6022298131,2.4223129443,3.0041471335], [3.0881062158,2.7568822971,4.0521105612])
    # Add shape uncertainty
    htestUp = createHisto("shapeUp", [0,10.5,12.1,13.3,0],[0,0,0,0,0])
    htestDown = createHisto("shapeDown", [0,8.8,8.1,15.5,0],[0,0,0,0,0])
    rhwu.addShapeUncertaintyFromVariation("shape",htestUp,htestDown)
    testHistoContents("after shape", rhwu.getRootHisto(), [0.0,9.6,7.6,15.7,0.0], [0.0,2.4186773245,2.3,2.561249695,0.0])
    codeValidator.test("getRate()", rhwu.getRate(), 32.9)
    codeValidator.test("getRateStatUncertainty()", rhwu.getRateStatUncertainty(), 4.2071367936)
    g = rhwu.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6,7.6,15.7], [1.315902732,4.5637265475,1.57], [2.08,1.52,3.9521639642])
    (systUp,systDown) = rhwu.getRateSystUncertainty() # this tests also Merge
    codeValidator.test("getRateSystUncertainty() up", systUp, 4.4524263048)
    codeValidator.test("getRateSystUncertainty() down", systDown, 6.5989696165)
    # Clone
    rhwuCloned = rhwu.Clone()
    testHistoContents("after Clone", rhwuCloned.getRootHisto(), [0.0,9.6,7.6,15.7,0.0], [0.0,2.4186773245,2.3,2.561249695,0.0])
    g = rhwuCloned.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6,7.6,15.7], [1.315902732,4.5637265475,1.57], [2.08,1.52,3.9521639642])
    # Scale
    rhwuCloned.Scale(2.0)
    testHistoContents("after Scale", rhwuCloned.getRootHisto(), [0.0,9.6*2,7.6*2,15.7*2,0.0], [0.0,2.4186773245*2,2.3*2,2.561249695*2,0.0])
    g = rhwuCloned.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6*2,7.6*2,15.7*2], [1.315902732*2,4.5637265475*2,1.57*2], [2.08*2,1.52*2,3.9521639642*2])
    # ScaleVariationUncertainty
    rhwuCloned.ScaleVariationUncertainty("shape",2.0)
    testHistoContents("after ScaleVariationUncertainty", rhwuCloned.getRootHisto(), [0.0,9.6*2,7.6*2,15.7*2,0.0], [0.0,2.4186773245*2,2.3*2,2.561249695*2,0.0])
    g = rhwuCloned.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6*2,7.6*2,15.7*2], [4.08,18.064063773,1.57*2], [4.9985597926,1.52*2,11.4716345827])
    # Add second shape uncertainty
    htest2Up = createHisto("shape2Up", [0,11.2,13.5,16.3,0],[0,0,0,0,0])
    htest2Down = createHisto("shape2Down", [0,8.2,6.1,13.5,0],[0,0,0,0,0])
    rhwu.addShapeUncertaintyFromVariation("shape2",htest2Up,htest2Down)
    testHistoContents("after shape2", rhwu.getRootHisto(), [0.0,9.6,7.6,15.7,0.0], [0.0,2.4186773245,2.3,2.561249695,0.0])
    g = rhwu.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [9.6,7.6,15.7], [2.0716177254,7.4590616032,1.6807438829], [2.5072694311,2.1355093069,4.5232289352])
    # Add the two rhwu's
    rhwuSum = rhwu.Clone()
    rhwuSum.Add(rhwuCloned)
    testHistoContents("rate after Add", rhwuSum.getRootHisto(), [0,28.8,22.8,47.1,0], [0,5.4083269132,5.1429563482,5.7271284253,0])
    #testHistoContents("shape+ after Add", rhwuSum._shapeUncertaintyAbsolutePlus, [0,2.88,2.28,4.71,0], [])
    #testHistoContents("shape- after Add", rhwuSum._shapeUncertaintyAbsoluteMinus, [0,5.76,4.56,9.42,0], [])
    g = rhwuSum.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [28.8,22.8,47.1], [5.5771318794,23.3721714866,4.7480627629], [7.1510558661,4.8003749854,15.4135135514])
    (systUp,systDown) = rhwuSum.getRateSystUncertainty() # this tests also Merge
    codeValidator.test("getRateSystUncertainty() up", systUp, 19.6983984121)
    codeValidator.test("getRateSystUncertainty() down", systDown, 20.5408763202)
    # Test add in the other direction
    rhwuSum2 = rhwuCloned.Clone()
    rhwuSum2.Add(rhwu)
    testHistoContents("rate after Add2", rhwuSum2.getRootHisto(), [0,28.8,22.8,47.1,0], [0,5.4083269132,5.1429563482,5.7271284253,0])
    #testHistoContents("shape+ after Add2", rhwuSum2._shapeUncertaintyAbsolutePlus, [0,2.88,2.28,4.71,0], [])
    #testHistoContents("shape- after Add2", rhwuSum2._shapeUncertaintyAbsoluteMinus, [0,5.76,4.56,9.42,0], [])
    g = rhwuSum2.getSystematicUncertaintyGraph(addStatistical=False)
    testGraphContents("syst.graph,addStat=False", g, [28.8,22.8,47.1], [5.5771318794,23.3721714866,4.7480627629], [7.1510558661,4.8003749854,15.4135135514])
    (systUp,systDown) = rhwuSum2.getRateSystUncertainty() # this tests also Merge
    codeValidator.test("getRateSystUncertainty() up", systUp, 19.6983984121)
    codeValidator.test("getRateSystUncertainty() down", systDown, 20.5408763202)

    #rhwuSum.Debug()


# Bugs found
# rate stat uncert.: last bin was ignored
# rate syst uncert.: normalization uncertainties in bin content, i.e. linear sum used when combining bins (was squared sum)
# syst. uncert: combining of norm