import matplotlib.pyplot as plt
import numpy as np
import pprint

from sklearn.datasets import make_moons
from sklearn.metrics.pairwise import euclidean_distances
import math

plt.figure(figsize=(4, 4))

# sample points
X1, Y1 = make_moons(n_samples=400, shuffle=True, noise=0.05, random_state=None)

# exit()

# X1 = np.asarray([[0.2, 0.4], [0.3, 0.5], [0.4, 0.6], [0.5, 0.5], [0.6, 0.4],
#                  [0.4, 0.6], [0.5, 0.5], [0.6, 0.4], [0.7, 0.5], [0.8, 0.6]])
# Y1 = [0, 0, 0, 1, 1, 1]

# normalize points
# X1[:, 0] = (X1[:, 0]-min(X1[:, 0])) / (max(X1[:, 0])-min(X1[:, 0]))
# X1[:, 1] = (X1[:, 1]-min(X1[:, 1])) / (max(X1[:, 1])-min(X1[:, 1]))
# print(Y1)
# print(X1[0])
# print(X1[1])

# generate basic plot with the samples

################################################################
# color dots
################################################################
col = []
for _label in Y1:
    if _label == 0:
        col.append("b")
    else:
        col.append(("r"))
tm = plt.scatter(X1[:, 0], X1[:, 1], marker='o', facecolors=col, s=15, edgecolor='k', linewidths=0.5)
################################################################


################################################################
# connect samples
################################################################
# number of connections from each point
# neighbors = 1
#
# # calculate distance matrix
# distance_matrix = euclidean_distances(X1, X1)
# max_distance = 0
# min_distance = 100
#
# # get min and max distance for normalization
# for idx1 in range(len(X1)):
#     for idx2 in range(len(X1)):
#         if idx1 == idx2:
#             continue
#         if distance_matrix[idx1, idx2] > max_distance:
#             max_distance = distance_matrix[idx1, idx2]
#         elif distance_matrix[idx1, idx2] < min_distance:
#             min_distance = distance_matrix[idx1, idx2]
#
# for idx1 in range(len(X1)):
#     distances = []
#     closest_points = []
#     labels = []
#     for idx2 in range(len(X1)):
#         if idx1 == idx2:
#             continue
#         if len(distances) < neighbors:
#             distances.append(distance_matrix[idx1, idx2])
#             closest_points.append([X1[idx2, 0], X1[idx2, 1]])
#             labels.append(Y1[idx2])
#         elif distance_matrix[idx1, idx2] < max(distances):
#             idx = np.argmax(distances)
#             distances[idx] = distance_matrix[idx1, idx2]
#             closest_points[idx] = [X1[idx2, 0], X1[idx2, 1]]
#             labels[idx] = Y1[idx2]
#     for _idx in range(neighbors):
#         if Y1[idx1] == labels[_idx]:
#             linecolor = "k"
#         else:
#             linecolor = "r"
#         linewidth = 0.5-((distances[_idx] - min_distance) / (max_distance - min_distance))
#         plt.plot([X1[idx1, 0], closest_points[_idx][0]], [X1[idx1, 1], closest_points[_idx][1]],
#                  linewidth=linewidth, color=linecolor)
################################################################


################################################################
# calculate label propagation
################################################################
# num_samples = 200
# num_labels = 150
#
# # sort X1 by label and increasing x coordinate
# x_0 = np.asarray(X1[Y1 == 0])
# x_1 = np.asarray(X1[Y1 == 1])
# y_0 = np.asarray(Y1[Y1 == 0])
# y_1 = np.asarray(Y1[Y1 == 1])
#
# x_0 = np.asarray(sorted(x_0, key=lambda k: [k[0], k[1]]))
# x_1 = np.asarray(sorted(x_1, key=lambda k: [k[0], k[1]]))
# # Y1 = np.asarray([0] * len(x_0) + [1] * len(x_1))
#
# # print(type(x_0))
# _idx_0 = np.random.choice(x_0.shape[0], num_labels//2, replace=False)
# _idx_1 = np.random.choice(x_1.shape[0], num_labels//2, replace=False)
# # _idx_0 = np.asarray([3,5,7])
# # _idx_1 = np.asarray([4,5,6])
# print(_idx_0)
#
# _not_idx_0 = [x for x in range(len(x_0)) if x not in _idx_0]
# _not_idx_1 = [x for x in range(len(x_1)) if x not in _idx_1]
# # print(_idx_0)
# # print(y_0)
# # exit()
#
# # x1_l = x_1[_idx_1]
# # x1_u = x_1[_not_idx_1]
# # print(x1_l.shape, x1_u.shape)
# # exit(9)
# X1 = np.concatenate((x_0[_idx_0], x_1[_idx_1], x_0[_not_idx_0], x_1[_not_idx_1]), 0)
# Y1 = np.concatenate((y_0[_idx_0], y_1[_idx_1], y_0[_not_idx_0], y_1[_not_idx_1]))
#
# # print(Y1)
# # exit()
# print(X1)
# print(Y1)
#
#
# # calculate distance matrix
# distance_matrix = euclidean_distances(X1, X1)
# print(distance_matrix)
#
#
# distance_matrix_prob = np.copy(distance_matrix)
# for idx1 in range(len(distance_matrix)):
#     for idx2 in range(len(distance_matrix)):
#         distance_matrix_prob[idx1, idx2] = distance_matrix[idx1, idx2] / sum(distance_matrix[idx1, :])
# print("")
# print(distance_matrix_prob)
# # print(distance_matrix_prob[0])
# # print(sum(distance_matrix_prob[0]))
# # exit()
#
# def one_hot(a, num_classes):
#     return np.squeeze(np.eye(num_classes)[a.reshape(-1)])
# label_matrix = one_hot(Y1, 2)
#
# # labelled labels
# Y_l = label_matrix[:num_labels]
# col = []
# for _label in np.argmax(Y_l, 1):
#     if _label == 0:
#         col.append("b")
#     else:
#         col.append(("r"))
# while len(col) < len(X1):
#     col.append("none")
# tm = plt.scatter(X1[:, 0], X1[:, 1], marker='o', facecolors=col, s=15, edgecolor='k', linewidths=0.5)
# plt.savefig("fig0.png")
# # print(Y_l)
# # exit()
#
# Y_u = label_matrix[num_labels:]
# T_ll = distance_matrix_prob[:num_labels, :num_labels]
# T_lu = distance_matrix_prob[:num_labels, num_labels:]
# T_ul = distance_matrix_prob[num_labels:, :num_labels]
# T_uu = distance_matrix_prob[num_labels:, num_labels:]
#
# diag = np.diag([1]*(num_samples-num_labels))
# # calculate unlabelled labels
# Y_u = np.matmul(np.matmul(np.linalg.inv(np.subtract(T_uu, diag)), T_ul), Y_l)
# print(Y_u)
#
# for idx1 in range(len(Y_u)):
#     max_idx = np.argmax(Y_u[idx1])
#     Y_u[idx1, :] = 0
#     Y_u[idx1, max_idx] = 1
#
# print("predicted Y:", np.argmax(Y_u, 1))
# print("correct Y:", Y1[num_labels:])
# print("accuracy:", (Y1[num_labels:] == np.argmax(Y_u, 1)).mean())
#
# col = []
# for _label in np.argmax(Y_l, 1):
#     if _label == 0:
#         col.append("b")
#     else:
#         col.append(("r"))
# for _label in np.argmax(Y_u, 1):
#     if _label == 0:
#         col.append("b")
#     else:
#         col.append(("r"))
# tm = plt.scatter(X1[:, 0], X1[:, 1], marker='o', facecolors=col, s=15, edgecolor='k', linewidths=0.5)
# # tm = plt.scatter(X1[:5, 0], X1[:5, 1], marker='o', facecolors='r', s=15, edgecolor='k', linewidths=0.5)
################################################################

plt.savefig("fig1.png")
