import FWCore.ParameterSet.Config as cms

# Message logger
from FWCore.MessageService.MessageLogger_cfi import *
MessageLogger.categories.append("HPlusRootFileDumper")
MessageLogger.categories.append("hltPrescaleTable")
MessageLogger.categories.append("EventCounts")  # HPlusEventCountAnalyzer
MessageLogger.categories.append("HLTTableInfo") # HPlusHLTTableAnalyzer
MessageLogger.categories.append("EcalLaserDbService") # To suppress messages (53X)

# Do NOT lower this number (or the logs will eat all your quota)
MessageLogger.cerr.FwkReport.reportEvery = 5000

MessageLogger.cerr.hltPrescaleTable = cms.untracked.PSet(reportEvery = MessageLogger.cerr.FwkReport.reportEvery)
# Suppress messages "The interpolated laser correction is <= zero! (0). Using 1. as correction factor." in 53X
MessageLogger.cerr.EcalLaserDbService = cms.untracked.PSet(limit = cms.untracked.int32(2))

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
from Configuration.Geometry.GeometryIdeal_cff import *

# Calo geometry service model
from Geometry.CaloEventSetup.CaloGeometry_cfi import *
# Calo topology service model
from Geometry.CaloEventSetup.CaloTopology_cfi import *

from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *

from RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi import *
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *

TFileService = cms.Service("TFileService",
  fileName = cms.string('histograms.root')
)
