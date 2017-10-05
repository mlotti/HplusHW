#!/usr/bin/env python

import HiggsAnalysis.LimitCalc.LandSTools as lands
import HiggsAnalysis.LimitCalc.CombineTools as combine
import HiggsAnalysis.LimitCalc.CommonLimitTools as commonLimitTools
import HiggsAnalysis.LimitCalc.DatacardReader as DatacardReader

import os

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
#lhcType = True
#lhcTypeAsymptotic = True


def main(opts, myDir, datacardPatterns, rootFilePatterns, myMassPoints):
    postfix = "combination"

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }
    
    # run
    if opts.lepType:
        raise Exception("LEP type Hybrid CLs not implemented yet for combine")
    elif opts.lhcType:
        raise Exception("LHC type Hybrid CLs not implemented yet for combine")
    elif opts.lhcTypeAsymptotic:
        combine.produceLHCAsymptotic(
            opts,
            myDir,
            massPoints = myMassPoints,
            datacardPatterns = datacardPatterns,
            rootfilePatterns = rootFilePatterns,
            clsType = combine.LHCTypeAsymptotic(opts),
            postfix = postfix+"_lhcasy"
            )
    else:
        return False
    return True

if __name__ == "__main__":
    def addToDatacards(myDir, massPoints, dataCardList, rootFileList, dataCardPattern, rootFilePattern):
        if rootFilePattern != None and "%s" in dataCardPattern:
            m = DatacardReader.getMassPointsForDatacardPattern(myDir, dataCardPattern)
            if len(m) > 0:
                m = DatacardReader.getMassPointsForDatacardPattern(myDir, dataCardPattern, massPoints)
                del massPoints[:]
                massPoints.extend(m)
                dataCardList.append(dataCardPattern)
                rootFileList.append(rootFilePattern)
        else:
            if os.path.exists(dataCardPattern):
                dataCardList.append(dataCardPattern)
                rootFileList.append(rootFilePattern)

    parser = commonLimitTools.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    opts = commonLimitTools.parseOptionParser(parser)
    # General settings

    myDirs = opts.dirs[:]
    if len(myDirs) == 0:
        myDirs.append(".")

    for myDir in myDirs:
        print "Considering directory:",myDir
        datacardPatterns = []
        rootFilePatterns = []
        myMassPoints = []
        if len(opts.masspoints) > 0:
            myMassPoints = opts.masspoints[:]
        # taunu, tau+jets final state
        settings = commonLimitTools.GeneralSettings(myDir, opts.masspoints)
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS), settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS))
        # taunu, tau mu final state
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "datacard_mutau_taunu_m%s_mutau.txt", "shapes_taunu_m%s_btagmultiplicity_j.root")
        # taunu, dilepton final states
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_ee_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_ee.root")
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_emu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_emu.root")
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_mumu_taunu_m%s.txt", "CrossSectionShapes_taunu_m%s_mumu.root")
        # tb, tau mu final state
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "datacard_mutau_tb_m%s_mutau.txt", "shapes_tb_m%s_btagmultiplicity_j.root")
        # tb, dilepton final states
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_ee_tb_m%s.txt", "CrossSectionShapes_tb_m%s_ee.root")
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_emu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_emu.root")
        addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "DataCard_mumu_tb_m%s.txt", "CrossSectionShapes_tb_m%s_mumu.root")
        # tb, single lepton final states
        myLabels = ["nB1_mu", "nB2p_mu", "nB1_el", "nB2p_el"]
        for l in myLabels:
            addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "HpToSingleLepton_datacard_"+l+"_%s.txt", "HpToSingleLepton_HT_M%s_"+l+".root")
        myLabels = ["Control_nB0_mu", "Control_nB1_mu", "Control_nB2p_mu", "Control_nB0_el", "Control_nB1_el", "Control_nB2p_el"]
        for l in myLabels:
            addToDatacards(myDir, myMassPoints, datacardPatterns, rootFilePatterns, "HpToSingleLepton_datacard_"+l+".txt", "HpToSingleLepton_HT_CR_"+l+".root")

        if 0:
            print "The following masses are considered:",", ".join(map(str, myMassPoints))
        if len(myMassPoints) > 0:
            if not main(opts, myDir, datacardPatterns, rootFilePatterns, myMassPoints):
                #print ""
                parser.print_help()
                #print ""
                raise Exception("You forgot to specify limit calculation method as a command line parameter!")
    
