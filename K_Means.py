import os
import sys
import math
import random
import logging
import openpyxl
import traceback
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import _t_sne

# Global Variable
gRow: int = 0
gCol: int = 0
gDim: int = 0
gK: int = 0
gMaxValue: float = 0.0
gMinValue: float = 0.0
gResourcePath: str = ""
gResultPath: str = ""
gResultName: str = ""

# Read xlsx
def _readXlsx() -> np.ndarray:
    global gRow
    global gCol
    global gResourcePath
    resFile: openpyxl.workbook.workbook.Workbook = openpyxl.load_workbook(gResourcePath)
    resSheet: openpyxl.worksheet.worksheet.Worksheet = resFile.active
    originalData: np.ndarray = np.zeros((gRow, gCol), dtype=float, order='C')
    for row in range(0, gRow, 1):
        for col in range(0, gCol, 1):
            # Start from 1
            originalData[row, col] = resSheet.cell(row + 1, col + 1).value
    return originalData

# Initialization centroid
def _initializationCentroid(originalData: np.ndarray) -> np.ndarray:
    global gRow
    global gK
    global gDim
    centroid: np.ndarray = np.zeros((gK, gDim), dtype=float, order='C')
    alreadyChoices: np.ndarray = np.zeros((gRow, ), dtype=bool, order='C')
    firstChoice: int = random.randint(0, gRow)
    centroid[0] = originalData[firstChoice]
    alreadyChoices[firstChoice] = True
    for k in range(1, gK, 1):
        weightSum: float = 0.0
        weight: np.ndarray = np.zeros((gRow, ), dtype=float, order='C')
        weight.fill(float('inf'))
        for point in range(0, gRow, 1):
            if alreadyChoices[point]:
                weight[point] = 0
                continue
            for existCentroid in range(0, k, 1):
                centroidDistance: float = _euclideanDistance(originalData[point], centroid[existCentroid])
                if centroidDistance < weight[point]:
                    weight[point] = centroidDistance
            weightSum += weight[point]
        weight /= weightSum
        choiceWhich = random.choices(list(range(0, gRow, 1)), weight)[0]
        centroid[k] = originalData[choiceWhich]
        alreadyChoices[choiceWhich] = True
    return centroid

# Clustering
def _clustering(originalData: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    global gRow
    global gK
    cluster: np.ndarray = np.zeros((gRow, ), dtype=int, order='C')
    for point in range(0, gRow, 1):
        whichCentroid: int = 0
        minDistance: float = float('inf')
        for k in range(0, gK, 1):
            centroidDistance: float = _euclideanDistance(originalData[point], centroid[k])
            if centroidDistance < minDistance:
                minDistance = centroidDistance
                whichCentroid = k
        cluster[point] = whichCentroid
    return cluster

# Calculate centroid
def _calcCentroid(originalData: np.ndarray, cluster: np.ndarray) -> np.ndarray:
    global gK
    global gDim
    centroid: np.ndarray = np.zeros((gK, gDim), dtype=float, order='C')
    for k in range(0, gK, 1):
        inGroup: int = 0
        sum: np.ndarray = np.zeros((gDim, ), dtype=float, order='C')
        for point in range(0, gRow, 1):
            if k == cluster[point]:
                inGroup += 1
                sum += originalData[point]
        centroid[k] = (sum / inGroup)
    return centroid

# Euclidean distance
def _euclideanDistance(point1: np.ndarray, point2: np.ndarray) -> float:
    global gDim
    result: float = 0.0
    for dim in range(0, gDim, 1):
        result += math.pow(point1[dim] - point2[dim], 2)
    return math.sqrt(result)

# Dimension reduction
def _dimReduction(allPoint: np.ndarray) -> tuple:
    global gK
    tSNE: _t_sne.TSNE = _t_sne.TSNE(n_components=2, perplexity=50.0, learning_rate=200.0, n_iter=1000)
    dimReduceAllData: np.ndarray = tSNE.fit_transform(allPoint)
    # Left: Data, Right: Centroid
    return dimReduceAllData[gK:], dimReduceAllData[:gK]

# Output to text
def _text(centroid: np.ndarray, cluster: np.ndarray) -> None:
    global gRow
    global gK
    global gDim
    global gResourcePath
    global gResultPath
    global gResultName
    with open(os.path.join(gResultPath, f"{gResultName}.txt"), "w", encoding="utf_8") as resultFile:
        text: str = ""
        for k in range(0, gK, 1):
            text += f"Centroid {k} ("
            for dim in range(0, gDim, 1):
                text += f"{centroid[k, dim]:.10f},"
            text = text[:-1]
            text += ")\n"
        text += "\n"
        clusterDataCount: np.ndarray = np.zeros((gK, ), dtype=int, order='C')
        for point in range(0, gRow, 1):
            clusterDataCount[cluster[point]] += 1
            text += f"Point {point} in cluster {cluster[point]}\n"
        text += "\n"
        for k in range(0, gK, 1):
            text += f"Cluster {k}: {clusterDataCount[k]} point\n"
        resultFile.write(text)
        resultFile.close()

# Output to picture
def _picture(data: np.ndarray, centroid: np.ndarray) -> None:
    global gDim
    global gResourcePath
    global gResultPath
    global gResultName
    fig = plt.figure(figsize=[12.8, 7.2])
    if gDim == 3:
        axes = fig.add_subplot(111, projection='3d')
        axes.scatter(data[:, 0], data[:, 1], data[:, 2])
        axes.scatter(centroid[:, 0], centroid[:, 1], centroid[:, 2], c="red")
        axes.set_zlabel("Z")
    else:
        axes = plt.axes()
        axes.scatter(data[:, 0], data[:, 1])
        axes.scatter(centroid[:, 0], centroid[:, 1], c="red")
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.set_title("K-Means")
    plt.savefig(os.path.join(gResultPath, f"{gResultName}.jpg"))

# Main Function
def K_Means(resRow: int, resCol: int, k: int, resPath: str, resultPath: str, resultName: str) -> None:
    global gRow
    global gCol
    global gDim
    global gK
    global gMaxValue
    global gMinValue
    global gResourcePath
    global gResultPath
    global gResultName

    # Initialization global variable
    gRow = resRow
    gCol = gDim = resCol
    gK = k
    gResourcePath = resPath
    gResultPath = resultPath
    gResultName = resultName

    # Judge
    if (resRow < 1) or (resCol < 1) or (k < 2) or (k > resRow) or (k > 3 and resRow < 50):
        raise ValueError("Invalid Argument.")

    # Read file
    originalData = _readXlsx()

    # Data normalization
    gMaxValue = originalData.max()
    gMinValue = originalData.min()
    originalData -= gMinValue
    originalData /= (gMaxValue - gMinValue)

    # Initialization centroid
    centroid: np.ndarray = np.zeros((2, gK, gDim), dtype=float, order='C')
    centroid[0] = _initializationCentroid(originalData)

    # Clustering
    cluster: np.ndarray = np.zeros((gRow, ), dtype=int, order='C')
    while True:
        cluster = _clustering(originalData, centroid[0])
        # Note: centroid[0] = past, centroid[1] = current
        centroid[1] = _calcCentroid(originalData, cluster)
        if np.all(np.equal(centroid[0], centroid[1])):
            break
        centroid[0] = centroid[1]

    # Output to picture
    if gDim == 2 or gDim == 3:
        # Draw picture (2d/3d)
        _picture(originalData, centroid[0])
    else:
        # Dimensionality reduction
        allData: np.ndarray = np.vstack((originalData, centroid[0]))
        dimReduceData, dimReduceCentroid = _dimReduction(allData)
        # Draw picture (2d)
        _picture(dimReduceData, dimReduceCentroid)

    # Data recovery
    originalData *= (gMaxValue - gMinValue)
    originalData += gMinValue
    centroid *= (gMaxValue - gMinValue)
    centroid += gMinValue

    # Output to text
    _text(centroid[0], cluster)

if __name__ == "__main__":
    # Help
    if "-h" in sys.argv or "--help" in sys.argv:
        print("                                                              ")
        print(f"Usage {sys.argv[0]} [Options] [Resource path] [Result path]  ")
        print("                                                              ")
        print("Options:                                                      ")
        print("                                                              ")
        print("  Required options                                            ")
        print("  -r, --row                           Set rows                ")
        print("  -c, --cow                           Set cols                ")
        print("  -k                                  Set target clusters     ")
        print("  -n  --name                          Set output name         ")
        print("                                                              ")
        print("  Unnecessary options                                         ")
        print("  -h, --help                          Show this list          ")
        sys.exit()

    # If missing argument
    if len(sys.argv) < 11:
        print("                                                              ")
        print("Invalid argument                                              ")
        print(f"Use {sys.argv[0]} -h to get more information                 ")
        sys.exit()

    # Handle arguments
    inputRow: int = 0
    inputCol: int = 0
    inputK: int = 0
    inputResourcePath: str = ""
    inputResultPath: str = ""
    inputResultName: str = ""
    for arg in sys.argv:
        if arg in ["-r", "--row"]:
            inputRow: int = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg in ["-c", "--col"]:
            inputCol: int = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg == "-k":
            inputK: int = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg in ["-n", "--name"]:
            inputResultName = sys.argv[sys.argv.index(arg) + 1]
    inputResourcePath: str = sys.argv[-2]
    inputResultPath: str = sys.argv[-1]

    # Execute main function
    try:
        K_Means(inputRow, inputCol, inputK, inputResourcePath, inputResultPath, inputResultName)
    except Exception as e:
        with open(os.path.join(gResultPath, f"{inputResultName}.log"), 'w') as logFile:
            logFile.write(traceback.format_exc())
            logFile.close()
