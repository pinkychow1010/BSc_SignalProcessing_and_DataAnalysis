% Uwe Ehret 2019/01/28
% Trains and applies a simple feed-forward neural network

clear all
close all
clc

% load data
load neural_networks_data

% create data
num_ts = length(Q_USL_nogaps);
area_a = 7;
area_b = 3;   
Qc = zeros(num_ts,1) + 3.67;
Qd = 10 * Q_USL_nogaps - Qc;
Qa = Qd * 0.7;
Qb = Qd * 0.3;
qa = Qa / 7;
qb = Qb / 3;

clear Q_USL_nogaps Qa Qb

% set dimensions and parameters
num_neurons_input = 3;
num_neurons_hidden = 3;
num_neurons_output = 1;

% define input data
input = NaN(num_neurons_input,num_ts);
input(1,:) = qa';
input(2,:) = qb';
input(3,:) = Qc';

% define observed output data
obs = NaN(num_neurons_output,num_ts);
obs(1,:) = Qd';

% define matrices for neuron values
x_input = NaN(num_neurons_input,1); % the input values (simply the input values)
z_hidden = NaN(num_neurons_hidden,6); % sum of all w*z connected to the neuron from the preceding layer
y_hidden = NaN(num_neurons_hidden,12); % the nonlinear transform of y
z_output = NaN(num_neurons_output,24);
y_output = NaN(num_neurons_output,36);
output = NaN(num_neurons_output,num_ts); % container for the neural network results

% define matrices for connections among neurons
% Note: For each neuron in the 'to'-layer, 
%       the weights of all neurons connected to it from the preceding layer
w_to_hidden = NaN(num_neurons_hidden,num_neurons_input); 
w_to_output = NaN(num_neurons_output,num_neurons_hidden);

%% training the model via backpropagation

% set the inital weights
w_to_hidden(:) = 1;
w_to_output(:) = 1;

% set the hyperparameters
learning_rate = (num_ts:-1:1)/num_ts;   % dynamic (decrasing) learning rate
delta = 0.2;  % the weight change

% create a container for the error
err = NaN(1,num_ts);

% loop over all timesteps (data tuples available for learning)
for t = 1 : num_ts
    t
       
    % read input of the current time step to the model
    x_input = input(:,t); 
            
    % run the model once to get the current error
    [~, ~, ~, sim] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
    err(t) = mean((sim - obs(:,t)).^2);
            
    % adjust weigths and evaluate its effect on model perforance    
    
        % randomly pick an element in either w_to_hidden or w_to_output
        ii = randi(numel(w_to_hidden)+numel(w_to_output));
        
        if ii <= numel(w_to_hidden)
        
        % adjust weight in w_to_hidden
        
            % randomly pick an element
            i = randi(numel(w_to_hidden));
            
            % keep the original weight
            w = w_to_hidden(i);
            
            % adjust the weight by adding delta
            w_to_hidden(i) = w + learning_rate(t) * delta;
            
            % run the model
            [~, ~, ~, sim] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
            
            % compute the error
            err_plus = mean((sim - obs(:,t)).^2);       
            
            % adjust the weight by subtracting delta
            w_to_hidden(i) = w - learning_rate(t) * delta;
            
            % run the model
            [~, ~, ~, sim] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
            
            % compute the error
            err_minus = mean((sim - obs(:,t)).^2);      
            
            % adjust the weight
            dummy = [err_plus err_minus err(t)];
            indx = find( dummy == min(dummy));
            if indx == 1
                w_to_hidden(i) = w + learning_rate(t) * delta;
            elseif indx == 2
                w_to_hidden(i) = w - learning_rate(t) * delta;
            else
                w_to_hidden(i) = w;
            end
                       
        else    
        % adjust weight in w_to_output
        
            % randomly pick an element
            i = randi(numel(w_to_output));    
            
            % keep the original weight
            w = w_to_output(i);
            
            % adjust the weight by adding delta
            w_to_output(i) = w + learning_rate(t) * delta;
            
            % run the model
            [~, ~, ~, sim] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
            
            % compute the error
            err_plus = mean((sim - obs(:,t)).^2);       
            
            % adjust the weight by subtracting delta
            w_to_output(i) = w - learning_rate(t) * delta;
            
            % run the model
            [~, ~, ~, sim] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
            
            % compute the error
            err_minus = mean((sim - obs(:,t)).^2);      
            
            % adjust the weight
            % w_to_output(i) = w - learning_rate(t) * ((err_plus - err_minus)/(2*delta));
            dummy = [err_plus err_minus err(t)];
            indx = find( dummy == min(dummy));
            if indx == 1
                w_to_output(i) = w + learning_rate(t) * delta;
            elseif indx == 2
                w_to_output(i) = w - learning_rate(t) * delta;
            else
                w_to_output(i) = w;
            end
            
        end
        
end

%% plot the error function
figure('Renderer', 'painters', 'Position', [10 10 900 600])
hold on
plot(err,'color',rgb('steelblue'),'LineWidth',1);
xlabel('learning steps');
ylabel('error');
set(gca,'FontSize',12,'FontWeight','bold');
hold off

%% forward pass (model application)

sim = NaN(1,num_ts);

% loop over all timesteps
for t = 1 : num_ts
    
    % read input
    x_input = input(:,t);
    
    % perform a single forward pass
    [~,~,~,sim(t)] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input);
        
end

%% plot the simulation
figure('Renderer', 'painters', 'Position', [10 10 900 600])
hold on
plot(DateTime,obs,'color',rgb('steelblue'),'LineWidth',1);
plot(DateTime,sim,'color',rgb('peru'),'LineWidth',1);
legend('observation','simulation','Location','northeast');
xlabel('time steps');
ylabel('discharge at D [m³/s]');
set(gca,'FontSize',12,'FontWeight','bold');
ylim([0 400]);
hold off










