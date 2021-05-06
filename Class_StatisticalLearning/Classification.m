% Tree-based methods
% In this exercise we will apply the concepts learned during the lectures 
% regarding supervised learning, decision tree.
 
% For this exercise, you will classify rainfall-runoff events using
% measurements from Dornbirner Ach in northwestern Austria (same dataset  
% used in one exercise of clustering):
% - Hourly discharge from the gauge Hoher Steg (q) in [m³/s], Ae = 113 km²
% - Precipitation from the station Ebnit located within the catchment(p)
% - Timestamps which apply to all measurements (DateTime)
% - User event identification {0 for non-event, 1 for event}

%% Task 1:
% Load the data from ue_DoBi_dataset.mat and split it evenly 
% into a training set(X_train, y_train) and a test set (X_test, y_test). 
% Each sample consists of a point in 2D feature space (X) and a 
% binary class label (y) {0 for non-event, 1 for event}. 
clear all
% clc
load ue_DoBi_dataset.mat
X = [p, q]; %features
y = event;  %labels (or classes)


%% Task 2:
% Check the documentation of the Matlab implementation of Decision tree
% (fitctree and predict).
% For each point in the test set, predict its label by fitting a 
% classification tree using the training set. 


%% Task 3:
% Check the classification error using the true labels of the 
% test set. For that, compute accuracy and the Matthews correlation 
% coefficient (MCC). Comment on your results.
% Hint: as an intermeadiate step compute True Positives (TP), True
% Negatives (TN), False Positives (FP), and False Negatives (FN).


%% Task 4: (just comment)
% 4.1: How could you try to improve your results?

% 4.2: Is it possible that the performance of another model ( let's call 
% it B) results in a higher accuracy and lower MCC than yours? How? 
% In this case, which model would you choose for event identification? Why?


%% Task 5:
% Now play with the parameter 'MinLeafSize' or 'MaxNumSplits'. For that, 
% use MCC as performance metric for selecting the best value of this parameter.
% Plot the parameter vs. metric values and justify your selection.


%% Task 6:
% Plot your final tree using the view function and comment on your results.


%% Task 7
% Plot the predictions for your model in a discharge time series and
% visually compare them with the true events.
% Hint: call your final model "Mdl_final" and run the provided code below.

y_predict = predict(Mdl_final,X);

figure
hold on
area(DateTime,max(q)*(y_predict==1), 'LineStyle', 'none', 'FaceColor', [.9 .2 .2],'FaceAlpha',0.5); % plotting simulated events
area(DateTime,max(q)*(y==1), 'LineStyle', 'none', 'FaceColor', [.5 .9 .5],'FaceAlpha',0.5); % plotting true events
plot(DateTime, q, '-b'); %plotting discharge
legend({['Decision tree events'] ['True events'] ['Discharge'] });
ylabel('Discharge [m³/s]');
xlabel('Date');
ylim([0 max(q)]);

%% Challenge task 8(optional task):
% Create a single-split tree (called stump) by hand, using only feature q:
% Vary a threshold and classify all datapoints above threshold as event=1.
% Plot the ROC curve of the resulting models and the point indicating your
% selected tree in the previous task.

