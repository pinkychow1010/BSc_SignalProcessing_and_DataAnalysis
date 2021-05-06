%% Assignment: Bias-variance tradeoff
% In this exercise, we will explore the bias-variance tradeoff using
% polynomials.

% From the CAOS project, you have measurements from:
% - Volumetric soil water content at cluster S_D, soil pit, in 10 cm depth (TETA_S_D_VWC_10_A) in [m³/m³]
% - Discharge at river gauge Useldange (Q_USL) in [m³/s], Ae = 245 km²
% - Timestamps which apply to all measurements (DateTime)
% Note: The data have already been preprocessed and are gap/NaN-free

%% Task 1: 
% Load the data from ue_biasvariance.mat and visualize the data.
clear all
load ue_biasvariance.mat
figure
yyaxis left
plot(DateTime, TETA_S_D_VWC_10_A_nogaps); %plot soil moisture

ylabel('Soil moisture [m³/m³]');
yyaxis right
plot(DateTime, Q_USL_nogaps); %plot discharge against datetime
ylabel('Discharge [m³/s]');
xlabel('Date');

figure
% plot TETA_S_D_VWC_10_A_nogaps x Q_USL_nogaps using scatter plot.
% Hint: use 'MarkerFaceAlpha' and 'MarkerEdgeAlpha' for plotting with transparency.

s = scatter(TETA_S_D_VWC_10_A_nogaps, Q_USL_nogaps)
s.Marker = '.';
s.MarkerFaceAlpha = 0.5;
s.MarkerEdgeAlpha = 0.5;


%% Task 2: 
% Check the documentation of "polyfit" and "polyval".  
% For getting used to the functions, fit a polynomial function of degree 
% three (y = a0 + a1*x + a2*x^2 + a3*x^3) to the full dataset and predict 
% y values given "x_pred", where TETA_S_D_VWC_10_A_nogaps is "x" and 
% Q_USL_nogaps is "y".
% After fitting, add the fitted polynomial ("x_pred" and predicted y values) 
% to the previous plot.
x_pred = (0.15:0.01:0.4)';
p = polyfit(TETA_S_D_VWC_10_A_nogaps, Q_USL_nogaps, 3);
x1 = x_pred;
y1 = polyval(p, x1);
hold on
plot(x1,y1,'LineWidth',2)
hold off

% We fitted a smooth function to the dataset. This function will be   
% assumed as the true function of the population. You already have 
% the true predictions "pred_true" for "x_pred" in your dataset.
smoo_true = smooth(TETA_S_D_VWC_10_A_nogaps, Q_USL_nogaps, 0.5, "loess"); %Curve Fitting Toolbox
[~,ii] = unique(TETA_S_D_VWC_10_A_nogaps);
pred_true = interp1(TETA_S_D_VWC_10_A_nogaps(ii), smoo_true(ii), x_pred);
plot(x_pred,pred_true,'g');
legend({'Observations','Polynomial of degree 3','True function'});



%% Task 3: 
% Now you will fit polynomials (degree 0, 1, 2 and 3) to 100 randomly
% drawn datasets containing 50 data points each. Also predict "x_pred" 
% for each one of the generated models. Save parameters and predictions,
% you will need them for calculating the bias and variance later.
bootstrap_ = 100;
samplesize = 50;

for i = 1:bootstrap_ %loop 100 times for 100 models in all 4 deg
    rng(i) %generating seeds for subsets
    r = randi([1 length(TETA_S_D_VWC_10_A_nogaps)],samplesize,1); 
    %random number between 1 and 38849, size 50 x 1
    
    %deg 0
    poly_0(i,:) = polyfit(TETA_S_D_VWC_10_A_nogaps(r), Q_USL_nogaps(r), 0); %polynomial function of degree 0
    pred_0(:,i) = polyval(poly_0(i,:), x_pred); %predictions of polynomials of degree 0
    %deg 1
    poly_1(i,:) = polyfit(TETA_S_D_VWC_10_A_nogaps(r), Q_USL_nogaps(r), 1);
    pred_1(:,i) = polyval(poly_1(i,:), x_pred);
    %deg 2
    poly_2(i,:) = polyfit(TETA_S_D_VWC_10_A_nogaps(r), Q_USL_nogaps(r), 2);
    pred_2(:,i) = polyval(poly_2(i,:), x_pred);
    %deg 3
    poly_3(i,:) = polyfit(TETA_S_D_VWC_10_A_nogaps(r), Q_USL_nogaps(r), 3);
    pred_3(:,i) = polyval(poly_3(i,:), x_pred);
  
end


%% Task 4:
% In a subplot (4 by 2), plot together all 100 models obtained for each
% polynomial order in the first row. In the second row, plot the mean of
% all models and the true polynomial. 
% Hint: For a better comparison, specify the axis limits.
% What can you observe in these plots?

%From the plot, we can observe that all models have very similar trends
%even though the amplitudes are different. This pattern applies to models
%of all degrees. The mean of all model shows a more general trend of the
%model, which fits the true data least with degree of 1 and the best with
%degree of 3. 

figure
subplot(2,4,1)
plot(x_pred, pred_0)
subplot(2,4,2)
plot(x_pred, pred_1)
subplot(2,4,3)
plot(x_pred, pred_2)
subplot(2,4,4)
plot(x_pred, pred_3)

mean_0 = mean(pred_0,2);
mean_1 = mean(pred_1,2);
mean_2 = mean(pred_2,2);
mean_3 = mean(pred_3,2);

subplot(2,4,5)
plot(x_pred, mean_0)
hold on
plot(x_pred,pred_true,'g');
hold off
subplot(2,4,6)
plot(x_pred, mean_1)
hold on
plot(x_pred,pred_true,'g');
hold off
subplot(2,4,7)

plot(x_pred, mean_2)
hold on
plot(x_pred,pred_true,'g');
hold off
subplot(2,4,8)
plot(x_pred, mean_3)
hold on
plot(x_pred,pred_true,'g');
hold off

%% Task 5:
% Calculate the bias: for each polynomial model, take the average of the
% mean absolute error between the true model predictions "pred_true" and 
% the average of all predictions at each value of "x_pred".
% Hint: One bias for each polynomial is expected.  
err_0 = abs(pred_true - pred_0);
bias_0 = mean(err_0,'all');
err_1 = abs(pred_true - pred_1);
bias_1 = mean(err_1,'all');
err_2 = abs(pred_true - pred_2);
bias_2 = mean(err_2,'all');
err_3 = abs(pred_true - pred_3);
bias_3 = mean(err_3,'all');
bias_ = [bias_0 bias_1 bias_2 bias_3]; %savind them together

% Calculate the variance: for each polynomial model, take the average of
% the variance of all predictions at each value of "x_pred".
% Hint: One variance for each polynomial is expected.
variance_0 = mean(var(transpose(pred_0)));
variance_1 = mean(var(transpose(pred_1)));
variance_2 = mean(var(transpose(pred_2)));
variance_3 = mean(var(transpose(pred_3)));
variance_ = [variance_0 variance_1 variance_2 variance_3];%savind them together

%% Task 6: 
% Finally, plot bias^2, variance, and (variance + bias^2) obtainded for 
% each polynomial order.
% Hint: you can try the function "area" to stack the bias^2 and variance
% curves. 
% How do you interpret the results? Does the data confirm your previous 
% interpretation of the bias-variance tradeoff?

%In the results, the model with 0 degree has the highest bias square
%and the lowest variance. The bias square decreases with degree and the 
%variance increases with degree. The sum of bias square and variance first
%decrease from 0 degree to 2 degree and then increase with the degree of 3.
%At the degree of 2, the sum of bias square and variance is the lowest,
%which means degree 3 is overfit and degree 1 is underfit. Fitting a model
%of degree 2 is optimal. The data confirm my previous 
% interpretation of the bias-variance tradeoff leanrt from the lecture. 

% Play with "samplesize" and comment on the results. 
%When the sample size increases, the differences between the 100 random
%models decreases and largely overlap. The variance decreases regardless of
%the degree and the sum of bias square and variance is dominated by the
%variance. Variance is as small as 0.04 at the degree of 1. The sum
%decreases with the increases of degree. The optimal degree for the model
%increases from 2 to 3. It means, a model of higher degree fit the true data better
%when the sample size of our 100 model increases. 

biassq_ = bias_ .^2;
vb_ = biassq_ + variance_;

figure
deg = [0 1 2 3];
plot(deg, biassq_)
hold on
plot(deg, variance_)
plot(deg, vb_)
hold off
xlabel('Degree of the polynomal');
ylabel('Error rate');
legend({'bias square','variance','bias^2 + var'})