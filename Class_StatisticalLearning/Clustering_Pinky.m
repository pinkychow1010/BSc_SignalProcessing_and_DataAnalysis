%Assignment: Clustering 
% In this exercise we will apply the concepts learned during the lectures 
% regarding clustering methods.
 
%% K-means | part 1
% The k-means algorithm is a simple clustering approach that can still be 
% very effective under the right circumstances, i.e., when the assumptions 
% of k-means are met. For the generic dataset, you will try different K and
% initialization parameters for the k-means method.

% Load the dataset ue_kmeans.mat
clear
load ue_kmeans.mat
X1 = X(:,1); %Feature 1
X2 = X(:,2); %Feature 2

%% Task 1.1:
% Visualize a scatter plot of the data. How many clusters do you expect?
figure
scatter(X1,X2,6,'*','r')
%By visual inspection, six clusters are expected.

%% Task 1.2:
% Check the documentation of the kmeans function.
% Run the Matlab implementation of k-means on the dataset. Try different K 
% and very bad initializations ('Start'). How stable are the results?
% Hint: You can try the gscatter fuction to plot the results.
X = [X1,X2];
[idx,C0] = kmeans(X,6);
gscatter(X1,X2,idx)

[idx,C1] = kmeans(X,4);
idx = kmeans(X,4,'Start',C1*0.5);
figure
gscatter(X1,X2,idx)

idx = kmeans(X,4,'Start',C1*2);
figure
gscatter(X1,X2,idx)

%With another k value and a bad 'start' (initializaitons), the clustering performance is
%instable in different trials, assigning completely different clusters
%every time the code is run. with different initializations, the clustering
%results also seems to be different. 

%The results are sensitive to the initializations.


%% Task 1.3:
% Check the documentation of the silhouette function.
% Calculate the average silhouette coefficient of all data points for 
% clusterings obtained by using the k-means for all K = 2:10. Finally, 
% plot K vs. average silhouette score. How would you interpret these results?
% Hint: From here on, use 'Replicates',10 in kmeans to obtain more stable 
% results.
S = zeros(9,1);
for i = 2:10
    clust = kmeans(X,i,'Replicates',10);
    s = silhouette(X,clust);
    S(i-1) = mean(s);
end
S
k_ = 2:10;
bar(k_,S)
grid on
xlabel('number of clusters')
ylabel('silhouette values')
%For silhouette value close to 1, it means that the data points fit well in
%to the cluster. According to the bar chart, 5 and 6 clusters scored the
%highest point close to 0.7, with 5 clusters having a bit higher score. 
%However, since two of the clusters partially overlap from visual
%inspection, they are not well represented by the silhouette values. 
%Hence, six clusters should be kept (i.e. K = 6).
%% Task 1.4:
% Plot the results and the silhouette of the best K in your interpretation.
clust = kmeans(X,6,'Replicates',10);
figure
silhouette(X,clust)

figure
gscatter(X1,X2,clust)

title('Silhouette values for clustering performance')

%From the plotting of Silhouette values, we can see that cluster 1 and 6
%have a bit lower Silhouette values compared to other clusters. This two
%clusters belong exactly to the two clusters which overlap each other. It
%can thus conclude that the overlapping of the clusters influence the
%results of Silhouette values.


%% K-means | part 2
% For this exercise, you will try to cluster rainfall-runoff events using
% measurements from Dornbirner Ach in northwestern Austria:
% - Hourly discharge from the gauge Hoher Steg (q) in [m³/s], Ae = 113 km²
% - Precipitation from the station Ebnit located within the catchment(p)
% - Timestamps which apply to all measurements (DateTime)
% - User event identification {0,1} (true events)
%% Task 2.1:
% Load the data from ue_DoBi_dataset.mat and visualize a 
% scatter plot of the data.
clear 
clc
load ue_DoBi_dataset.mat
X1 = p; %feature 1: precipitation dataset
X2 = q; %feature 2: discharge dataset
X = [X1, X2];

figure
scatter(X1, X2,'MarkerFaceColor','b','MarkerEdgeColor','b',...
    'MarkerFaceAlpha',.02,'MarkerEdgeAlpha',.02);
xlabel('Feature 1');
ylabel('Feature 2');
title('Discharge against rainfall')
pbaspect([1 1 1]);

%% Task 2.2:
% We will try use the dataset with K-means. The idea is that the clustering 
% will help us to automatically identify rainfall-runoff events. 
% Thus, in the end, 2 clusters are expected to be found (one for event and 
% another for non-event). 
% Run the Matlab implementation of k-means on the given features. In the
% end, 2 clusters are expected (event and non-event). Thus, K=2.

% Save the cluster indices of each observation in a variable called
% "cluster_idx" and cluster centroids in a variable called "C".
% Use the function scatterhist with 'Group' and 'Kernel' activated for
% checking your results. Analyze the results and save the index of the 
% cluster corresponding to events as the variable "event_clusterindex", so 
% you can use the and provided code in the next task.
[cluster_idx, C] = kmeans(X,2,'Replicates',10);
disp('cluster_idx')
tabulate(cluster_idx)
scatterhist(X1,X2,'Group',cluster_idx,'Kernel','on','Marker','+o','MarkerSize',[3,3]);
title('Clustering of Event occurence')
xlabel('Rainfall')
ylabel('Discharge')
legend('No Event','Event')
event_clusterindex = 2;

%% Task 2.3:
% On the next plot you can check events identified by a user and your
% cluster results. Check and comment on your results. Do you think that 
% K-means was an appropriate choice for the problem? Why?
% In the next class assignment, we will use the same dataset for training
% and evaluating classification trees.
figure
hold on
area(DateTime,max(X2)*(cluster_idx==event_clusterindex), 'LineStyle', 'none', 'FaceColor', [.9 .2 .2],'FaceAlpha',0.5); % plotting simulated events
area(DateTime,max(X2)*(event==1), 'LineStyle', 'none', 'FaceColor', [.5 .9 .5],'FaceAlpha',0.5); % plotting true events
plot(DateTime, X2, '-b'); %plotting discharge
legend({['K-means events'] ['True events'] ['Discharge'] });
title('Checking K-means performance')
ylabel('Discharge [m³/s]');
xlabel('Date');
title('Clustering Results')
ylim([0 max(q)])

%According to the results, it seems that the false negative is really high,
%with many data points being falsely simulated as non-event. In fact, the true
%event is almost not predicted in the plot. It indicates that k-means is not appropriate
%for the problem because the prediction rate of event is extremely low. It
%is possibly because the data distribution is very irregular and non-isotropic. The outliners
%in the data set are also not considered. This assumptions are not met and
%thus the clustering performance is not satisfying.

%% DBSCAN 
%% Task 3.1:
% Check the generic dataset ue_dbscan.mat and justify why 
% you should cluster the dataset with DBSCAN instead of K-means.
% How many clusters do you expect to identify? 
clear
load ue_dbscan.mat
X1 = X(:,1); %feature 1
X2 = X(:,2); %feature 2

figure
scatter(X1,X2,6,'*','r')

%By visual inspection, I expect to identify 5 clusters, with one cluster
%inside another, and some outliners that distributed in low density. The
%clusters are represented by the high density of points. 

%Instead of using K
%mean, it is in this case better to use DBSCAN for the clustering. It is
%because DBSCAN can identify the outliners which do not belong to any class
%and can better classify class with non-isotropic shape.


%% Task 3.2:
% Check the function f_dbscan available on your folder (R2018b or older) 
% or the Matlab implementation of dbscan (from R2019a on).
% Apply it to ue_dbscan.mat and plot the clustering results. Try to
% modify DBSCAN's hyperparameters ("minPts" and "eps") and comment on the results.

%From the scatter plot, we can see that the shape of the cluster is very
%irregular, which is not suitable to perform k-mean clustering.
%Alternatively, DBSCAN considers the neighbours within neighbourhood range
%so that it does not have pre-defined cluster shape. It also consider
%outliners. 

figure
[DB_idx, corepts] = dbscan(X,1,12);
gscatter(X(:,1),X(:,2),DB_idx)
grid on

figure
[DB_idx, corepts] = dbscan(X,5,4);
gscatter(X(:,1),X(:,2),DB_idx)
grid on

figure
[DB_idx, corepts] = dbscan(X,1,4);
gscatter(X(:,1),X(:,2),DB_idx)
grid on

%After trying out different values of parameters neighbourhood range and
%minimun points, different values heavily influence the performance of
%clustering. A larger range will leads to only one cluster which will not
%be helpful, and a large minPts will leads to non-intuituve clustering that
%are highly deviated form visual inspection. It is because this method mostly
%consider the approximity and density of the data points, but not the
%general continuity of pattern. 

%range = 1 and minPts = 4 seem to work the best.


%% Task 3.3:
% Calculate the average silhouette coefficient of all non-outlier data points for 
% clusterings obtained by using the DBSCAN with epsilon = 0:0.1:5. Finally, 
% plot EPS vs. average silhouette score and EPS vs. number of clusters found.
% Is the silhouette score appropriate for this dataset? Why?
% Plot also the set of epsilon you tested against the number of observations 
% clustered as noise (-1). Can you identify the best epsilon?

out = sum(DB_idx == -1) %97 outliners
in = sum(DB_idx ~= -1) %302 non-outliners
no_idx = find(DB_idx ~= -1);
figure
silhouette(X,DB_idx)
title('Silhouette values for DBSCAN clustering performance')

%No. From the plot, it can be seen that the silhouette score is not appropriate 
%for this dataset because for cluster 4, the silhouette value is as low
%as -0.8 which indicates poor clustering. However, it is possibly caused by
%one of the cluster which completely surround another cluster. Since silhouette
%value only consider distance of members in different clusters, the member
%in these two clusters will be considered poor fit into the clusters. 

n = 0;
silhouetteS = zeros(length(0:0.1:5),1);

for e = 0:0.1:5
    n = n+1;
    [DB_idx, corepts] = dbscan(X,e,4);
    number_clusterS(n) = length(unique(DB_idx));
    outS(n) = sum(DB_idx == -1);
    inS(n) = sum(DB_idx ~= -1);
    no_idx = find(DB_idx ~= -1);
    silhouetteS(n) = nanmean(silhouette(X(no_idx,:),DB_idx(no_idx)));
end
n
e
outS
inS
silhouetteS
number_clusterS

%Plotting EPS v.s. number of cluster

x = 0:0.1:5; %EPS
y = silhouetteS;
z = number_clusterS;
o = outS;

figure
plot(x,z,'-o')
title('DBSCAN Clustering: number of cluster/EPS')
xlabel('EPS')
ylabel('number of clusters')

%From the plot, we can see tha 6 clusters (include group of outliner) 
%has EPS value from 0.8 to 1.5.
%The silhouette value increases with EPS from 1 on until there is a sudden
%jump at EPS = 1.5.

figure
plot(x,o,'-o')
title('DBSCAN Clustering: number of outlinears/EPS')
xlabel('EPS')
ylabel('number of outliners')

%Generally, the number of outlinears decreases from all points to zero
%point. With EPS = 1.5, there are 59 outlinears. 

figure
plot(x,y,'-x')
title('DBSCAN Clustering: silhouette/EPS')
xlabel('EPS')
ylabel('average silhouette value')

%The silhouette indicates if the clustering is well performed concerning the
%similarity of members in a cluster compared to the others. It is not
%approperiate because according to the values, 2 cluster (includes one class of outliner)
% fits the best. The problem occurs also with K means, with the same reason
% that the class within another class does not work well wit silhouette
% values. It is hence difficult to identify the best EPS solely from the values, 
% but EPS = 1.5 has a good silhouette value by having 5 clusters + 1 outliner
% class as visually investigated. Hence EPS = 1.5 is considered the
% optimal EPS value. 

%% Task 3.4: 
% Plot the results and the default plot of the silhouette function, for the
% best clustering in your interpretation.

%The original clustering
[DB_idx_1, corepts] = dbscan(X,1,4);
gscatter(X(:,1),X(:,2),DB_idx_1)
grid on
silhouette(X,DB_idx_1)

%the optimal clustering
[DB_idx_2, corepts] = dbscan(X,1.5,4);
gscatter(X(:,1),X(:,2),DB_idx_2)
grid on
silhouette(X,DB_idx_2)

%In the optimal clustering with EPS value 1.5, all the data
%points in all clusters have high silhouette values of over 0.8, 
%indicating that the clusters are well separated. In contrast, with EPS
%values 1, one of the cluster has values less than zero, which means the
%assignment of member data points is not clearly separated. It is
%considered bad clustering.













