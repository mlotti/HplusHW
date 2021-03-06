import sys
def QCDInvertedNormalizationSafetyCheck(era, searchMode, optimizationMode):
    validForEra = 'Run2016'
    validForSearchMode = '350to3000'
    validForOptMode = ''
    if not era == validForEra:
        raise Exception('Error: inconsistent era, normalisation factors valid for',validForEra,'but trying to use with',era)
    if not searchMode == validForSearchMode:
        raise Exception('Error: inconsistent search mode, normalisation factors valid for',validForSearchMode,'but trying to use with',searchMode)
    if not optimizationMode == validForOptMode:
        raise Exception('Error: inconsistent optimization mode, normalisation factors valid for',validForOptMode,'but trying to use with',optimizationMode)
QCDNormalization = {
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.151234567901 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.174718196457 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.21875 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.12962962963 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.109686609687 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0912208504801 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0581098339719 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0740740740741 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0204678362573 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.174718196457 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.201848351187 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.252717391304 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.149758454106 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.126718691936 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.105385578816 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0671331001166 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0855762594893 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.023646071701 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.21875 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.252717391304 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.31640625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.1875 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.158653846154 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.131944444444 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0840517241379 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.107142857143 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0296052631579 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.12962962963 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.149758454106 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.1875 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.111111111111 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0940170940171 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0781893004115 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0498084291188 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0634920634921 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0175438596491 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.109686609687 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.126718691936 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.158653846154 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0940170940171 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0795529257068 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0661601772713 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0421455938697 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0537240537241 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0148448043185 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.0912208504801 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.105385578816 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.131944444444 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0781893004115 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0661601772713 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0550221002896 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0350503760465 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0446796002352 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0123456790123 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.388888888889 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.449275362319 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.5625 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.282051282051 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.234567901235 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.149425287356 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.190476190476 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.0526315789474 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0581098339719 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0671331001166 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0840517241379 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0498084291188 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0421455938697 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0350503760465 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0223279165015 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0284619594964 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.00786448880823 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.0740740740741 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.0855762594893 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.107142857143 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0634920634921 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0537240537241 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0446796002352 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0284619594964 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0362811791383 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0100250626566 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0204678362573 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.023646071701 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0296052631579 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0175438596491 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0148448043185 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0123456790123 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.00786448880823 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0100250626566 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.00277008310249 ,
    'Inclusive': 1,
}
EWKFakeTausNormalization = {
    'Inclusive': 1,
}
QCDPlusEWKFakeTausNormalization = {
    'Inclusive': 1,
}
QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarDown = {
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.201848351187 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.275362318841 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.325337331334 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.166170339488 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.166170339488 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.166170339488 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0731378496798 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.11231884058 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0499194847021 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.275362318841 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.375650364204 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.44382647386 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.226690234202 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.226690234202 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.226690234202 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0997749437359 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.153225806452 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0681003584229 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.325337331334 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.44382647386 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.524375743163 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.267831837506 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.267831837506 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.267831837506 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.117882919006 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.181034482759 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0804597701149 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.166170339488 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.226690234202 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.267831837506 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.060210258044 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0924657534247 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.041095890411 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.166170339488 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.226690234202 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.267831837506 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.060210258044 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0924657534247 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.041095890411 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.166170339488 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.226690234202 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.267831837506 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.136798648902 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.060210258044 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0924657534247 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.041095890411 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.333333333333 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.315789473684 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.428571428571 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.298701298701 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.204819277108 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.123595505618 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.136363636364 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.136363636364 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0731378496798 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0997749437359 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.117882919006 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.060210258044 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.060210258044 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.060210258044 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0265008112493 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0406976744186 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0180878552972 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.11231884058 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.153225806452 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.181034482759 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0924657534247 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0924657534247 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0924657534247 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0406976744186 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0625 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0277777777778 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0499194847021 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0681003584229 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0804597701149 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.041095890411 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.041095890411 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.041095890411 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0180878552972 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0277777777778 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0123456790123 ,
    'Inclusive': 1,
}
QCDPlusEWKFakeTausNormalizationSystFakeWeightingVarUp = {
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2lt1'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2lt1'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2lt1'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2lt1'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2lt1'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2lt1'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2lt1'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2lt1'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2lt1'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq1to2'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq1to2'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq1to2'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.111111111111 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.105263157895 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.142857142857 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0995670995671 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0682730923695 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0411985018727 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0454545454545 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0454545454545 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq1to2'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.105263157895 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0997229916898 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.135338345865 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0943267259057 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0646797717185 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0390301596688 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0430622009569 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0430622009569 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq1to2'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.142857142857 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.135338345865 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq1to2'   : -0.183673469388 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.128014842301 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0877796901893 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0529695024077 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0584415584416 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0584415584416 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq1to2'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2eq2to3'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2eq2to3'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2eq2to3'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0995670995671 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0943267259057 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.128014842301 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0892224658458 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0611797840714 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0369181380417 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0407319952774 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0407319952774 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2eq2to3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0682730923695 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0646797717185 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0877796901893 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0611797840714 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0419509362752 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0253147421145 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0279299014239 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0279299014239 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2eq2to3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.0411985018727 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.0390301596688 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2eq2to3'   : -0.0529695024077 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0369181380417 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0253147421145 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2eq2to3'   : -0.015275849009 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0168539325843 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0168539325843 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2eq2to3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.449275362319 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.612903225806 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2lt20:decayMode_2gt3'   : 0.724137931034 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.369863013699 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.369863013699 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2lt20:decayMode_2gt3'   : 0.369863013699 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.162790697674 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.25 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2lt20:decayMode_2gt3'   : 0.111111111111 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0454545454545 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0430622009569 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq20to40:decayMode_2gt3'   : -0.0584415584416 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0407319952774 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0279299014239 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0168539325843 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0185950413223 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0185950413223 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq20to40:decayMode_2gt3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.0454545454545 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.0430622009569 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2eq40to60:decayMode_2gt3'   : -0.0584415584416 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0407319952774 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0279299014239 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0168539325843 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0185950413223 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0185950413223 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2eq40to60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1eq40to60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1gt60:decayMode_1lt2:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1eq40to60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1gt60:decayMode_1eq2to3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1lt40:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1eq40to60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'tauPt_1gt60:decayMode_1gt3:tauPt_2gt60:decayMode_2gt3'   : -0.0 ,
    'Inclusive': 1,
}
