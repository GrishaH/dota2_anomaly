import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn import preprocessing
import matplotlib.pyplot as plt


team_fights = pd.read_csv("7_27_data.csv")

X_val = team_fights[['fightDuration']]
Y_val = team_fights[['participants']]
total = np.column_stack((X_val, Y_val))
scaler = StandardScaler()
data_std = scaler.fit_transform(total)


# total = preprocessing.scale(total)
# total = StandardScaler().fit_transform(total)

db = DBSCAN(eps=0.6, min_samples=10).fit(data_std)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
print("A")
print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)


# Plot result

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = scaler.inverse_transform(data_std[class_member_mask & core_samples_mask])
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = scaler.inverse_transform(data_std[class_member_mask & ~core_samples_mask])
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.xlabel('Teamfight Duration (Seconds)')
plt.ylabel('Hero participants')
plt.show()
