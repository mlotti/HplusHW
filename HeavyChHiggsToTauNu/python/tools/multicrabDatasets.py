import multicrabDatasetsCollisionData10Dec22 as collisionData10Dec22
import multicrabDatasetsCollisionData10Apr21 as collisionData10Apr21
import multicrabDatasetsCollisionData11May10 as collisionData11May10
import multicrabDatasetsCollisionData11Aug05 as collisionData11Aug05
import multicrabDatasetsCollisionData11Prompt as collisionData11Prompt

import multicrabDatasetsMCSpring11 as mcSpring11
import multicrabDatasetsMCSummer11 as mcSummer11
import multicrabDatasetsMCFall11 as mcFall11

import multicrabDatasetsTauEmbedding as tauEmbedding

datasets = {}

datasets.update(collisionData10Dec22.datasets)
datasets.update(collisionData10Apr21.datasets)
datasets.update(collisionData11May10.datasets)
datasets.update(collisionData11Aug05.datasets)
datasets.update(collisionData11Prompt.datasets)

datasets.update(mcSpring11.datasets)
datasets.update(mcSummer11.datasets)
datasets.update(mcFall11.datasets)

tauEmbedding.addTo(datasets)

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
