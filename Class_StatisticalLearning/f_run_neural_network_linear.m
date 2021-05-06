function [z_hidden, y_hidden, z_output, y_output] = f_run_neural_network_linear(num_neurons_hidden, num_neurons_output, w_to_hidden, w_to_output, x_input)
% performs a single forward pass of a neural network

% define variables
z_hidden = NaN(num_neurons_hidden,1); % sum of all w*z connected to the neuron from the preceding layer
y_hidden = NaN(num_neurons_hidden,1); % the nonlinear transform of y
z_output = NaN(num_neurons_output,1);
y_output = NaN(num_neurons_output,1);


% calculate z and y of the hidden layer
for j = 1 : num_neurons_hidden
    z_hidden(j) = sum(x_input .* w_to_hidden(j,:)');
    y_hidden(j) = z_hidden(j);
end

% calculate z and y of the output layer
for j = 1 : num_neurons_output
    z_output(j) = sum(y_hidden .* w_to_output(j,:)');
    y_output(j) = z_output(j);
end

end

