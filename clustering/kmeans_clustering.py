import pandas as pd
import pylab as pl
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import time

# Load the data
team_fights = pd.read_csv("7_27_data.csv")
X = team_fights[['fightDuration']]
Y = team_fights[['deaths']]
data = team_fights[['fightDuration', 'deaths']]

# Standardize the data
scaler = StandardScaler()
data_std = scaler.fit_transform(data)
data_std1 = data.to_numpy()

# Run local implementation of kmeans
km = KMeans(n_clusters=3, max_iter=1000, n_init=10, random_state=4231)

# kmeansoutput = km.fit(data_std)
kmeansoutput = km.fit_predict(data_std)

# Get centres of clusters
start = time.process_time()
time_taken = time.time()
time_again = time.perf_counter()
centers = km.cluster_centers_
points = np.empty((0,len(data_std[0])), float)
distances = np.empty((0,len(data_std[0])), float)

# getting points and distances
for i, center_elem in enumerate(centers):
    # cdist is used to calculate the distance between center and other points
    distances = np.append(distances, cdist([center_elem],data_std[kmeansoutput == i], 'euclidean')) 
    points = np.append(points, data_std[kmeansoutput == i], axis=0)


percentile = 97
# getting outliers whose distances are greater than some percentile
outliers = points[np.where(distances > np.percentile(distances, percentile))]


fig = plt.figure()  # plotting initial data


#### Do the same for test data
##Measuring time to process test data
##start = time.process_time()
##time_taken = time.time()
##time_again = time.perf_counter()
##
##test_data = pd.read_csv("7_27_test_data.csv")
##A = test_data[['fightDuration']]
##B = test_data[['deaths']]
##data2 = test_data[['fightDuration', 'deaths']]
##scaler = StandardScaler()
##data_std2 = scaler.fit_transform(data2)
##test_result = km.predict(data_std2)
##
#########Gets data for the test data's anomalies
##### Center of clusters Attempt
##centers = km.cluster_centers_
##points = np.empty((0,len(data_std[0])), float)
##distances = np.empty((0,len(data_std[0])), float)
##
### getting points and distances
##for i, center_elem in enumerate(centers):
##    # cdist is used to calculate the distance between center and other points
##    distances = np.append(distances, cdist([center_elem],data_std2[test_result == i], 'euclidean')) 
##    points = np.append(points, data_std2[test_result == i], axis=0)
##    
##percentile = 97
##outliers = points[np.where(distances > np.percentile(distances, percentile))]

# Print time taken through the various means
print(time.process_time() - start)
print(time.time() - time_taken)
print(time.perf_counter() - time_again)

# Gets data for the test data's anomalies
# full_data = np.append(data_std, data_std2, axis=0)


print("Outliers would be: ")
print(scaler.inverse_transform(outliers))

plt.scatter(X, Y, c=kmeansoutput, marker="o")  # plotting red ovals around outlier points
plt.scatter(*zip(*scaler.inverse_transform(outliers)), marker="o", facecolor="None", edgecolor="r", s=70)
# plotting centers as blue dots
plt.scatter(*zip(*scaler.inverse_transform(centers)), marker="o", facecolor="b", edgecolor="b", s=10)
plt.xlabel('Teamfight Duration (Seconds)')
plt.ylabel('Hero Deaths')
# plt.scatter(data_std[:,0], data_std[:,1],c=kmeansoutput,marker = "x") # plotting red ovals around outlier points
# plt.scatter(*zip(*outliers),marker="o",facecolor="None",edgecolor="r",s=70);# plotting centers as blue dots
# plt.scatter(*zip(*centers),marker="o",facecolor="b",edgecolor="b",s=10);
# plt.scatter(data_std2[:,0], data_std2[:,1],c=test_result,marker = "^") # plotting red ovals around outlier points
# plt.scatter(*zip(*outliers),marker="o",facecolor="None",edgecolor="r",s=70);# plotting centers as blue dots
# plt.scatter(*zip(*centers),marker="o",facecolor="b",edgecolor="b",s=10);
plt.show()


