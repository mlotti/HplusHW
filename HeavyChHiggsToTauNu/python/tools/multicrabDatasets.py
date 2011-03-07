import multicrabDatasetsCollisionData as collisionData
import multicrabDatasetsMCSummer10 as mcSummer10
import multicrabDatasetsMCFall10 as mcFall10
import multicrabDatasetsMCFall10PU as mcFall10PU
import multicrabDatasetsMCWinter10 as mcWinter10
import multicrabDatasetsTauEmbedding as tauEmbedding

datasets = {}

datasets.update(collisionData.datasets)
datasets.update(mcSummer10.datasets)
datasets.update(mcFall10.datasets)
datasets.update(mcWinter10.datasets)

mcFall10PU.addTo(datasets)
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
