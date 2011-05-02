import multicrabDatasetsCollisionData10 as collisionData10
import multicrabDatasetsCollisionData11 as collisionData11

import multicrabDatasetsMCWinter10 as mcWinter10
import multicrabDatasetsMCSpring11 as mcSpring11

import multicrabDatasetsTauEmbedding as tauEmbedding

datasets = {}

datasets.update(collisionData10.datasets)
datasets.update(collisionData11.datasets)

datasets.update(mcWinter10.datasets)
datasets.update(mcSpring11.datasets)

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
