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
X = [p, q]; %features p = rainfall; q = discharge value
y = event;  %labels (or classes) 1/0

%Separating training data and test set
n = ceil(length(X)*0.7);
trainX = X(1:n,:);
testX = X(n+1:end,:);
trainy = y(1:n,:);
testy = y(n+1:end,:);

%% Task 2:
% Check the documentation of the Matlab implementation of Decision tree
% (fitctree and predict).
% For each point in the test set, predict its label by fitting a 
% classification tree using the training set. 

%Mdl = fitctree(X,y,'OptimizeHyperparameters','auto');
Mdl = fitctree(trainX,trainy);
label = predict(Mdl,testX);

%% Task 3:
% Check the classification error using the true labels of the 
% test set. For that, compute accuracy and the Matthews correlation 
% coefficient (MCC). Comment on your results.
% Hint: as an intermeadiate step compute True Positives (TP), True
% Negatives (TN), False Positives (FP), and False Negatives (FN).

%Calculate general accuracy
tbl = label - testy;
unique(tbl);
FP = sum(tbl == 1)/length(tbl);
FN = sum(tbl == -1)/length(tbl);
TP = sum(label == 1 & testy == 1)/length(tbl);
TN = sum(label == 0 & testy == 0)/length(tbl);
accuracy = (sum(tbl == 0)/length(tbl)); %in percentage
MCC = ((TP*TN) - (FP*FN))/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN));

%MCC value = 0.5302
%MCC value range between -1 and 1 with 1 represents perfect perfect
%prediction. The result 0.5302 indicates average prediction but not
%satisfactory. It might be due to the fact that there are much more
%factors influences the occurance of events other than precipitation and
%discharge, for instance the factor of temporal relationship. Only two
%predictors then will be not enough for the prediction. It may due
%to insufficient training data.

%% Task 4: (just comment)
% 4.1: How could you try to improve your results?

%We can use bagging and ensemble model to increase the sampling size for training, 
%in order to improve the performance in predicting event. The more data we
%can use for training, the more possible we can filter out the noise and
%concentrate on the general patterns. 

% 4.2: Is it possible that the performance of another model ( let's call 
% it B) results in a higher accuracy and lower MCC than yours? How? 
% In this case, which model would you choose for event identification? Why?

%Yes. We can try the random forest to increase the accuracy and
%decrease MCC since random forest are good at prediction by
%training on bootstrap-samples of the data. It combines classifiers that 
%output a final classification and thus give better generalization and
%avoid overfitting.

%% Task 5:
% Now play with the parameter 'MinLeafSize' or 'MaxNumSplits'. For that, 
% use MCC as performance metric for selecting the best value of this parameter.
% Plot the parameter vs. metric values and justify your selection.

for s = 1:50
    Mdl = fitctree(trainX,trainy,'MaxNumSplits',s);
    pred = predict(Mdl,testX);
    tbl = pred - testy;
    FP = sum(tbl == 1)/length(tbl);
    FN = sum(tbl == -1)/length(tbl);
    TP = sum(label == 1 & testy == 1)/length(tbl);
    TN = sum(label == 0 & testy == 0)/length(tbl);
    accuracy(s) = (sum(tbl == 0)/length(tbl)); 
    MCC(s) = ((TP*TN) - (FP*FN))/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN));
end
figure
plot(1:50,MCC,'o-')
hold on
plot(accuracy,'*-')
title('MCC and Accuracy against parameter MaxNumSplits')
xlabel('MaxNumSplits')
ylabel('MCC/Accuracy')
legend('MCC','Accuracy','Location','southeast')
grid on
grid minor
hold off

%According to MCC calculated, MaxNumSplits 2 leads to the best
%performace of prediciton, with MCC = 0.599 and accuracy = 93.6% which is
%rather satisfactory. More splits do not really further improve performance.
%It might be because there are only two
%predictors and high values of MaxNumSplits will lead to overfitting. So
%a classification tree with the layer of two should be enough.

%% Task 6:
% Plot your final tree using the view function and comment on your results.
Mdl_final = fitctree(trainX,trainy,'MaxNumSplits',2);
label = predict(Mdl_final,testX);
view(Mdl_final,'mode','graph') 

%% Task 7
% Plot the predictions for your model in a discharge time series and
% visually compare them with the true events.
% Hint: call your final model "Mdl_final" and run the provided code below.

y_predict = predict(Mdl_final,testX);

figure
hold on
area(DateTime(n+1:end,:),max(q)*(y_predict==1), 'LineStyle', 'none', 'FaceColor', [.9 .1 .1],'FaceAlpha',1); % plotting simulated events
area(DateTime(n+1:end,:),max(q)*(testy==1), 'LineStyle', 'none', 'FaceColor', [.5 .9 .5],'FaceAlpha',0.5); % plotting true events
plot(DateTime(n+1:end,:), q(n+1:end,:), '-b'); %plotting discharge
legend({['Decision tree events'] ['True events'] ['Discharge'] });
ylabel('Discharge [m³/s]');
xlabel('Date');
ylim([0 max(q)]);

%% Challenge task 8(optional task):
% Create a single-split tree (called stump) by hand, using only feature q:
% Vary a threshold and classify all datapoints above threshold as event=1.
% Plot the ROC curve of the resulting models and the point indicating your
% selected tree in the previous task.

