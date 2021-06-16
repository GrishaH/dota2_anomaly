# Anomaly Detection in Dota 2 Teamfights

This repository contains the source code written for my final year dissertation, consisting of a `fightdetection` parser for Dota 2 replay data, as well as several `clustering` models, all written in Python 3. This is primarily for code storage, but as well as explaining what my project was in some depth.

Do note that the required data for the `fightdetection` parser that was provided by the University of York is not included in this repository.

### How it works
This manages the parsing of Dota 2 replay data files and writing it into an `.csv` file as to use later on. Specifically, this parser attempts to classify and detect **teamfights**. For this purpose, teamfights are defined as scenarios where the majority of both teams (three players from the Radiant team and three players from the Dire team) have participated, by either damaging or taking damage in a given, relatively-small range. Further exchanges are measured in a larger area once a teamfight has been detected, and once 15 seconds of inactivity passes, the teamfight is concluded.

 As it is now, the parser stores the match ID, the starting and ending time for a detected teamfight, the teamfight's duration, the number of Hero deaths, and the number of Hero participants. This data is then applied to various clustering methods through `scikit-learn`, namely 2D and 3D K-means, with some tests into DBSCAN. The number of clusters used for K-means was detected via the `Elbow Method`, as well as tinkering with the values for the optimal possible result. This left us with roughly three clusters that defined and described general teamfight trends within the game. Using these, outliers can be detected, which may lead to the discovery potential anomalous gameplay events.

Outliers were detected in K-means by measuring the distances of points from their assigned cluster, and filtering the top percentile (usually ranging from 95-99% percentiles) as to find the furthest possible data points. By examining how these points translated to in-game actions and what values they consisted of, they were safely viewed as anomalous game events. What caused them and what exactly made them anomalous was discussed further in my dissertation, but namely included long-term stand-offs for valuable vantage points (middle lane towers, Roshan), as well as fights that lead into escape attempts by various Heroes, with dead Heroes respawning and rejoining the fight.

The process of detecting anomalies was timed with a large amount of data as to argue for its usability in real-time scenarios, keeping up with live games for the purpose of assisting commentators and audience members.


### TL;DR
Dota 2 replay data files are parsed into a human-readable file that can then be passed onto various clustering machine learning models, where outlying data is detected and flagged. The idea is that these data points can be potential, fruitful discussion topics for commentators.


### Results
Interesting game events were detected, and a large amount of data was able to be clustered and detected quickly, and so there's a strong argument that this is feasible in real-time. However, the strongest indicator one way or another would be to provide this informations to commentators/casters and audience members, to gauge how interesting or useful the data actually is. Unfortunately, for one reason or another, this was not possible to do in the time-frame of this project.

### Issues
- Code should be tidied up and restructured, as it unfortunately fell victim to blind and unplanned feature additions
- Needs to be tested in practice (Dealing with real-time data, and seeing if casters and the audience actually care)
- Values used aren't perfect and may need to be altered (15 second inactivity timer, ranges for teamfight detection and upkeep, anomaly percentiles, etc, all vary)
- Clustering model used (K-means is weak to outliers - they affect the overall clustering positions. Other models (DBSCAN) were tested, but ultimately it seemed like K-means was good enough. Other models may give better performance)
- Uncertainty if to use 2D or 3D clustering (received conflicting responses and feedback regarding this)

### Code referenced and used
Whilst the parser was made from scratch, various sources were used to help me find my footing with clustering.
Elbow Method - 
`https://bl.ocks.org/rpgove/0060ff3b656618e9136b`
`https://towardsdatascience.com/k-means-clustering-algorithm-applications-evaluation-methods-and-drawbacks-aa03e644b48a`
K-Means Clustering -
`https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html`
`https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html`
`https://medium.datadriveninvestor.com/outlier-detection-with-k-means-clustering-in-python-ee3ac1826fb0`
DBSCAN - 
`https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html`