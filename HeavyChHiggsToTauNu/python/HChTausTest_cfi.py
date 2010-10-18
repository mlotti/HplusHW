import FWCore.ParameterSet.Config as cms

TestTauIDSources = [("byIsolationChargedPtSum", "DiscriminationByIsolationChargedPtSum")
]

def extendEventContent(content, process):
    content.append("keep *_fixedConePFTaus_*_"+process.name_())
    content.append("keep *_shrinkingConePFTaus_*_"+process.name_())
    return content
