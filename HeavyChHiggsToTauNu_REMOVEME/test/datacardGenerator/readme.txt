To run datacard generator:
./datacardGenerator.py -h

example: produce datacards for all variations
./datacardGenerator.py -x defaultDatacard --combine


To run tail fit:
first create datacards
then go to a datacard directory and
../tailFitter.py -x ../tailFitSettings.py

it stores original datacards into originalDatacards directory
and creates new datacards with the settings in the settings directory
One should check the created figures to see how good the fit is
