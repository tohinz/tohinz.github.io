import matplotlib.pyplot as plt

from sklearn.datasets import make_moons

plt.figure(figsize=(4, 4))

X1, Y1 = make_moons(n_samples=200, shuffle=True, noise=0.05, random_state=None)
tm = plt.scatter(X1[:, 0], X1[:, 1], marker='o', facecolors='none', s=15, edgecolor='k', linewidths=0.5)

# plt.show()
plt.savefig("fig1.png")