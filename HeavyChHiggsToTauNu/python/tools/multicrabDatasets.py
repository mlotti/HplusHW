import multicrabDatasetsCollisionData as collisionData
import multicrabDatasetsMCSummer10 as mcSummer10
import multicrabDatasetsMCFall10 as mcFall10
import multicrabDatasetsTauEmbedding as tauEmbedding

datasets = {}

datasets.update(collisionData.datasets)
datasets.update(mcSummer10.datasets)
datasets.update(mcFall10.datasets)

tauEmbedding.addTo(datasets)
