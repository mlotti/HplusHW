import FWCore.ParameterSet.Config as cms
import os

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCor2010
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC
def customise(process, options):
    path = None

    if options.runOnCrab == 0:
        # Infer dynamically where the sqlite file is
        head = os.getcwd()
        relpath = ""
        i = 100
        while head.count("/") > 1 and i >= 0:
            p = os.path.join(head, "data/Jec10V3.db")
            if os.path.exists(p):
                path = relpath+"data/Jec10V3.db"
                break
            (head, tail) = os.path.split(head)
            relpath += "../"
            i -= 1
    
        if path == None:
            if i == 0:
                raise Exception("Maximum number of iterations reached for finding Jec10V3.db, i = %d, head = %s" % (i, head))
            else:
                raise Exception("Unable to find data/Jec10V3.db")
    else:
        # When run with crab, the position is fixed
        path = "src/HiggsAnalysis/HeavyChHiggsToTauNu/data/Jec10V3.db"

    # Load the JEC sqlite file
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
        DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
        ),
        timetype = cms.string('runnumber'),
        toGet = cms.VPSet(
            cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string('JetCorrectorParametersCollection_Jec10V3_AK5Calo'),
                label  = cms.untracked.string('AK5Calo')
            ),
            cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string('JetCorrectorParametersCollection_Jec10V3_AK5PF'),
                label  = cms.untracked.string('AK5PF')
            ),
            cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string('JetCorrectorParametersCollection_Jec10V3_AK5PFchs'),
                label  = cms.untracked.string('AK5PFchs')
            ),
        ),
        ## here you add as many jet types as you need (AK5Calo, AK5JPT, AK7PF, AK7Calo, KT4PF, KT4Calo, KT6PF, KT6Calo)
        connect = cms.string('sqlite_file:'+path)
    )

    # Add an es_prefer statement to resolve the conflict with the global tag: 
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

