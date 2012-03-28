## \package multicrabDatasets
# Root of dataset definitions for multicrab operations
#
# For dataset definitions, data datasets are split according to the
# Prompt/ReReco era, and MC datasets according to the production era.
#
# Note that you can obtain a list of all defined datasets by running
# this file through the python interpreter.
#
# \see multicrab

import multicrabDatasetsCollisionData11May10 as collisionData11May10
import multicrabDatasetsCollisionData11Aug05 as collisionData11Aug05
import multicrabDatasetsCollisionData11Prompt as collisionData11Prompt
import multicrabDatasetsCollisionData11Nov08Nov19 as collisionData11Nov08Nov19

import multicrabDatasetsMCSummer11 as mcSummer11
import multicrabDatasetsMCFall11 as mcFall11

import multicrabDatasetsTauEmbedding as tauEmbedding

## Dictionary for dataset definitions, updated from the other
## multicrabDatasets* files
datasets = {}

datasets.update(collisionData11May10.datasets)
datasets.update(collisionData11Aug05.datasets)
datasets.update(collisionData11Prompt.datasets)
datasets.update(collisionData11Nov08Nov19.datasets)

datasets.update(mcSummer11.datasets)
datasets.update(mcFall11.datasets)

tauEmbedding.addTo(datasets)

## Print all defined datasets
#
# \param details   Detailed printout?
def printAllDatasets(details=False):
    names = datasets.keys()
    names.sort()

    for name in names:
        line = name
        if details:
            content = datasets[name]
            if "crossSection" in content:
                line += " (%g pb)" % content["crossSection"]

            inputs = content["data"].keys()
            inputs.sort()
            line += " : " + ", ".join(inputs)
        print line

if __name__ == "__main__":
    printAllDatasets(True)
