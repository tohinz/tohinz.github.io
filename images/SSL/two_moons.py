import matplotlib.pyplot as plt
import numpy as np
import pprint

from sklearn.datasets import make_moons
from sklearn.metrics.pairwise import euclidean_distances
import math

plt.figure(figsize=(4, 4))

X1, Y1 = make_moons(n_samples=50, shuffle=True, noise=0.01, random_state=None)

# normalize points
X1[:, 0] = (X1[:, 0]-min(X1[:, 0])) / (max(X1[:, 0])-min(X1[:, 0]))
X1[:, 1] = (X1[:, 1]-min(X1[:, 1])) / (max(X1[:, 1])-min(X1[:, 1]))

tm = plt.scatter(X1[:, 0], X1[:, 1], marker='o', facecolors='none', s=15, edgecolor='k', linewidths=0.5)

# number of connections from each point
neighbors = 1
# print(X1)

# calculate distance matrix
distance_matrix = euclidean_distances(X1, X1)
max_distance = 0
min_distance = 100


for idx1 in range(len(X1)):
    for idx2 in range(len(X1)):
        if idx1 == idx2:
            continue
        if distance_matrix[idx1, idx2] > max_distance:
            max_distance = distance_matrix[idx1, idx2]
        elif distance_matrix[idx1, idx2] < min_distance:
            min_distance = distance_matrix[idx1, idx2]

# max_distance = max(distance_matrix)
# print(max_distance)
# print(min_distance)
# exit()
# pprint.pprint(np.asarray(distance_matrix))
# i = 0

for idx1 in range(len(X1)):
    distances = []
    closest_points = []
    labels = []
    for idx2 in range(len(X1)):
        if idx1 == idx2:
            continue
        if len(distances) < neighbors:
            distances.append(distance_matrix[idx1, idx2])
            closest_points.append([X1[idx2, 0], X1[idx2, 1]])
            labels.append(Y1[idx2])
        elif distance_matrix[idx1, idx2] < max(distances):
            idx = np.argmax(distances)
            distances[idx] = distance_matrix[idx1, idx2]
            closest_points[idx] = [X1[idx2, 0], X1[idx2, 1]]
            labels[idx] = Y1[idx2]
    for _idx in range(neighbors):
        if Y1[idx1] == labels[_idx]:
            linecolor = "k"
        else:
            linecolor = "r"
        linewidth = 0.5-((distances[_idx] - min_distance) / (max_distance - min_distance))
        plt.plot([X1[idx1, 0], closest_points[_idx][0]], [X1[idx1, 1], closest_points[_idx][1]],
                 linewidth=linewidth, color=linecolor)



# plt.show()
plt.savefig("fig1_2.png")
