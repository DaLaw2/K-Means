# K-Means Algorithm
## Introduction
This is an implementation of the K-Means clustering algorithm, written in Python. Given a set of data points, the algorithm aims to partition them into K clusters, where each point belongs to the cluster whose mean has the closest distance to it. This algorithm can be used in many fields, such as image processing, market segmentation, and document clustering.

## Prerequisites
- Python 3
- openpyxl
- numpy
- matplotlib
- scikit-learn

## Usage
**python K_Means.py [Options] [Resource path] [Result path]**

## Required options
- **-r, --row** Set rows
- **-c, --col** Set cols
- **-k** Set target clusters
- **-n, --name** Set output name

### Note
- If the dimension of the data set is greater than 3, at least 50 data points are required.

## Unnecessary options
- **-h, --help** Show help information

## Implementation
The algorithm consists of the following steps:

1. Initialization: randomly choose K data points as the initial centroids.
2. Clustering: assign each data point to the nearest centroid.
3. Recalculation: recalculate the centroid of each cluster.
4. Repeat steps 2-3 until the centroids no longer change or a maximum number of iterations is reached.
## Functions
- **_readXlsx()**: read data from xlsx file.
- **_initializationCentroid(originalData: np.ndarray)**: randomly choose K data - points as the initial centroids.
- **_clustering(originalData: np.ndarray, centroid: np.ndarray)**: assign each data point to the nearest centroid.
- **_calcCentroid(originalData: np.ndarray, cluster: np.ndarray)**: recalculate the centroid of each cluster.
- **_euclideanDistance(point1: np.ndarray, point2: np.ndarray)**: calculate the euclidean distance between two data points.
- **_dimReduction(allPoint: np.ndarray)**: reduce the dimension of the data to 2D using t-SNE.
- **_text(centroid: np.ndarray, cluster: np.ndarray)**: output the result to a text file.
- **_picture(data: np.ndarray, centroid: np.ndarray)**: output the result to a picture file.

## Example
```
from K_Means import K_Means

if __name__ == "__main__":
    K_Means(150, 4, 3, "data.xlsx", "result", "output")
```
This will run the K-Means algorithm with 150 data points, 4 dimensions, 3 target clusters, "data.xlsx" as the resource file, "result" as the result directory, and "output" as the output file name.
