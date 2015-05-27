# Description: Collection of routines to calculate error propagation
# The methods return the absolute uncertainty
#
# Authors: LAW

from math import sqrt

## f = a + b (with scalars)
def errorPropagationForSum(a, sigmaA, b, sigmaB):
    return sqrt(sigmaA**2 + sigmaB**2)

## f = a + b (with histograms)
def errorPropagationForSumWithHistograms(hA, hB, index):
    return errorPropagationForSum(0, hA.GetBinError(index), 0, hB.GetBinError(index))

## f = a * b (with scalars)
def errorPropagationForProduct(a, sigmaA, b, sigmaB):
    if abs(a) < 0.000001 or abs(b) < 0.000001:
        return 0.0 # Because the product will be zero (it is extremely difficult to obtain the resolution of the sample)
    return sqrt((b*sigmaA)**2 + (a*sigmaB)**2)

## f = a * b (with histograms)
def errorPropagationForProductWithHistograms(hA, hB, index):
    return errorPropagationForProduct(hA.GetBinContent(index), hA.GetBinError(index), hB.GetBinContent(index), hB.GetBinError(index))

## f = a / b (with scalars)
def errorPropagationForDivision(a, sigmaA, b, sigmaB):
    if abs(a) < 0.000001 or abs(b) < 0.000001:
        return 0.0 # Safety (it is extremely difficult to obtain the resolution of the sample)
    return sqrt((sigmaA/b)**2 + (a/(b**2)*sigmaB)**2)

## f = a / b (with histograms)
def errorPropagationForDivisionWithHistograms(hA, hB, index):
    return errorPropagationForDivision(hA.GetBinContent(index), hA.GetBinError(index), hB.GetBinContent(index), hB.GetBinError(index))

## Returns the total absolute error of a histogram
def integratedUncertaintyForHistogram(minBinIndex, maxBinIndex, h):
    mySum = 0.0
    for j in range(minBinIndex, maxBinIndex):
        mySum += h.GetBinError(j)**2
    return sqrt(mySum)

## Validation routine
def validateErrorPropagation(codeValidator):
    codeValidator.setPackage("ErrorPropagation")
    # Test sum
    codeValidator.test("errorPropagationForSum() test1", errorPropagationForSum(12., 3., 31., 4.), 5.)
    codeValidator.test("errorPropagationForSum() test2", errorPropagationForSum(12., 3., -31., 4.), 5.)
    # Test product
    codeValidator.test("errorPropagationForProduct() test1", errorPropagationForProduct(0., 3., -31., 4.), 0.)
    codeValidator.test("errorPropagationForProduct() test2", errorPropagationForProduct(5., 3., -31., 4.), 95.12623192)
    # Test division
    codeValidator.test("errorPropagationForDivision() test1", errorPropagationForDivision(0., 3., -31., 4.), 0.)
    codeValidator.test("errorPropagationForDivision() test2", errorPropagationForDivision(5., 3., -31., 4.), 0.09898671)
