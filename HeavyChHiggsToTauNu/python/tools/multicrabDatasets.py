import multicrabDatasetsCollisionData as collisionData
import multicrabDatasetsMCSummer10 as mcSummer10
import multicrabDatasetsMCFall10 as mcFall10
import multicrabDatasetsMCFall10PU as mcFall10PU

datasets = {}

datasets.update(collisionData.datasets)
datasets.update(mcSummer10.datasets)
datasets.update(mcFall10.datasets)

mcFall10PU.addTo(datasets)
