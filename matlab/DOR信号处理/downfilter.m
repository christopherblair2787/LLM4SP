function [Signal_out] = downfilter(Signal_in,Fs,down,tintegral)
%DOWNFILTER Summary of this function goes here
%   Detailed explanation goes here
Signal_reshape=reshape(Signal_in,down,Fs*tintegral/down);
Signal_out=mean(Signal_reshape,1);
% keyboard;

end

