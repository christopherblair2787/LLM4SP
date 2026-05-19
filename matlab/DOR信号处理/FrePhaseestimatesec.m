function [Fsec, phasesec]=FrePhaseestimatesec(Corr,F_estimate,t,range,deltaf,tintegral,noise,timestr);

f=[F_estimate-range:deltaf:F_estimate+range];
%  keyboard
for m=1:length(f)
 
    data_Ref=exp(-j*2*pi*f(m)*t);
    % keyboard
    xcorr=Corr.*data_Ref;
%     showfft2side(Corr,Fs,'in');
%    showfft2side(xcorr,Fs,'in');keyboard
    xcorrSum=sum(xcorr);
    amp(m,1)=abs(xcorrSum);
    phase(m,1)=angle(xcorrSum);
end
% keyboard
[ampmax,position]=max(amp);
Fsec=f(position);
phasesec = phase(position);
timestr_out=num2str(str2num(timestr)+tintegral/2);
%  fprintf(fid,'%15s %20.7f  %20.7f   %20.7f   %20.7f\n',timestr_out,f(position),phase(position),10*log10(ampmax),noise); 
%   keyboard;plot(amp,'.');
