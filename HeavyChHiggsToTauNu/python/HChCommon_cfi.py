import FWCore.ParameterSet.Config as cms

# Message logger
from FWCore.MessageService.MessageLogger_cfi import *
MessageLogger.categories.append("HPlusRootFileDumper")
MessageLogger.categories.append("hltPrescaleTable")
MessageLogger.categories.append("EventCounts")  # HPlusEventCountAnalyzer
MessageLogger.categories.append("HLTTableInfo") # HPlusHLTTableAnalyzer

MessageLogger.cerr.FwkReport.reportEvery = 100

MessageLogger.cerr.hltPrescaleTable = cms.untracked.PSet(reportEvery = MessageLogger.cerr.FwkReport.reportEvery)

#MessageLogger.cerr = cms.untracked.PSet(
#  placeholder = cms.untracked.bool(True)
#)
#MessageLogger.cout = cms.untracked.PSet(
#  INFO = cms.untracked.PSet(
   #reportEvery = cms.untracked.int32(100), # every 100th only
   #limit = cms.untracked.int32(100)       # or limit to 100 printouts...
#  )
#)
#MessageLogger.statistics.append('cout')

# Job will exit if any product is not found in the event
options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

# Magnetic Field
#process.load("Configuration/StandardSequences/MagneticField_cff")
from Configuration.StandardSequences.MagneticField_38T_cff import *
from Configuration.StandardSequences.Services_cff import *
from Configuration.StandardSequences.Geometry_cff import *

# Calo geometry service model
from Geometry.CaloEventSetup.CaloGeometry_cfi import *
# Calo topology service model
from Geometry.CaloEventSetup.CaloTopology_cfi import *

from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *

from RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi import *
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *

TFileService = cms.Service("TFileService",
  fileName = cms.string('HPlusOutInfo.root')
)
