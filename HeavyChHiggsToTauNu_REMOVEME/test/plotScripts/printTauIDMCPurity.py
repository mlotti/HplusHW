#!/usr/bin/env python
import ROOT, sys, array
from types import *
from math import sqrt


def getEntry(file, histoName, output, k):
  f = ROOT.TFile(file);
  histo = f.Get(histoName)
  if type(histo) is NoneType:
    print file, histoName
    print "Histogram not found!"
    sys.exit()
  sum = 0
  for i in range(histo.GetNbinsX()):
    sum = sum + histo.GetBinContent(i+1)
  if sum > 0:
    return output+","+str(histo.GetBinContent(k)/sum)+",+-,"+str(sqrt(histo.GetBinContent(k))/sum)
  else:
    return output+",-,+-,-"


def getHisto(file, histoName):
  f = ROOT.TFile(file);
  histo = f.Get(histoName)
  if type(histo) is NoneType:
    print file, histoName
    print "Histogram not found!"
    sys.exit()
  return histo


def tauIDStage(prefix1, name, bin, label):
  histoName = prefix1 + name
  myOutput = histoName+","+label
  for file in sys.argv[1:]:
    myOutput = getEntry(file, histoName, myOutput, bin)
  print myOutput


def tauAlgorithm(prefix1, taualgo, bin, label):
  print taualgo
  prefix = prefix1 + taualgo + "/"
  # table header
  myOutput = ","
  for file in sys.argv[1:]:
    myOutput = myOutput+","+file+",,"
  print myOutput

  # table rows
  tauIDStage(prefix, "TauSelection_all_tau_candidates_MC_purity", bin, label)
  tauIDStage(prefix, "TauSelection_cleaned_tau_candidates_MC_purity", bin, label)
  tauIDStage(prefix, "TauSelection_selected_taus_MC_purity", bin, label)


def tauMatcher(bin, label):
  print ""
  print label
  myprefix = "signalAnalysis"
  tauAlgorithm(myprefix, "TauSelectionCaloTauCutBased", bin, label)
  tauAlgorithm(myprefix, "TauSelectionShrinkingConeCutBased", bin, label)
  tauAlgorithm(myprefix, "TauSelectionShrinkingConeTaNCBased", bin, label)
  tauAlgorithm(myprefix, "TauSelectionHPSMediumTauBased", bin, label)
  tauAlgorithm(myprefix, "TauSelectionHPSTightTauBased", bin, label)


if __name__ == "__main__" :
  tauMatcher(1, "H+")
  tauMatcher(2, "W")
  #tauMatcher(3, "other")
  #tauMatcher(4, "nomatch")

