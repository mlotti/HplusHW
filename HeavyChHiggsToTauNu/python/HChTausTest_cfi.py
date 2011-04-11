import FWCore.ParameterSet.Config as cms

TestTauIDSources = [("byIsolationChargedPtSum", "DiscriminationByIsolationChargedPtSum"),
                    ("byIsolation05", "DiscriminationByIsolation05"),
                    ("byIsolation06", "DiscriminationByIsolation06"),
                    ("byIsolation07", "DiscriminationByIsolation07"),
                    ("byIsolation08", "DiscriminationByIsolation08"),
                    ("byIsolation09", "DiscriminationByIsolation09"),
                    ("againstElectronWithCrack", "DiscriminationAgainstElectronWithCrack")
]

def extendEventContent(content, process):
    content.append("keep *_fixedConePFTaus_*_"+process.name_())
    content.append("keep *_shrinkingConePFTaus_*_"+process.name_())
    return content
