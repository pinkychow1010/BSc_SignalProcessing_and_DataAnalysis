function [sigma] = f_sigmoid(z)
% calculates the sigmoid of an input z
% Input
% - z: [1,n] or [n,1] double. z is typically the logit of a neuron
% Output
% - sigma: [1,n] or [n,1] double with the sigmoid of z [0,1]. sigma typically is the
%   nonlinear output of a neuron in a neural network
% Version
% - 2019/01/25 Uwe Ehret: initial version

sigma = 1./(1+exp(-z));

end

