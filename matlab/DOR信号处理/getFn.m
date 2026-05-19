
function [Fn,Fn_error]=getFn(xulie,samplerate,integral_of_Fn)
global Nfft window_minpoint window_maxpoint integral_time_of_phase

 df=samplerate/Nfft;
 Ts=1/samplerate;
 numphase=integral_of_Fn/integral_time_of_phase;
 time_phase=[0:integral_time_of_phase:integral_of_Fn-integral_time_of_phase]+integral_time_of_phase/2;
 sigma=3;
%  df=caiyanglv/65536/2;
% keyboard
%  hold on
%    figure(1);
% subplot(2,1,1);
% hold on
y_fft=fft(xulie,Nfft);
n=length(y_fft);
F=(0:df:(0.5*samplerate-df));
amp=abs(y_fft(1:n/2));

ampwindow=amp(window_minpoint:window_maxpoint);

[maxamp,position0]=max(ampwindow);
SNR=maxamp/(sum(amp)-maxamp)*(n/2-1);
SNR_dB=20*log10(SNR);

F0=F(1,window_minpoint+position0-1);
Sig_ref=exp(-j*2*pi*F0*(0:Ts:integral_of_Fn-Ts));
Sig_xcorr=xulie.*Sig_ref;
Sig_xcorr=reshape(Sig_xcorr,integral_of_Fn*samplerate/numphase,numphase);
Sig_xcorr_sum=sum(Sig_xcorr);
phase_xcorr=unwrap(angle(Sig_xcorr_sum));
phase_xcorr_unwrap=unwrap(phase_xcorr);
[t_unwarpangle_selected,unwarpangle_selected,sigma_y_err]= selectdata_sigma(time_phase,phase_xcorr_unwrap,sigma); 
unwarpangle_selected=unwarpangle_selected/2./pi;   %in unit of circle
 [a,s]=polyfit(t_unwarpangle_selected,unwarpangle_selected,2); 
 Fn_error=s.normr;
 discrepancy=a(2);
 Fn=F0+discrepancy;
%  figure;plot(t_unwarpangle_selected,unwarpangle_selected,'.');
 
%  figure;
% plot(F, 10*log10(amp/maxamp), 'r');
% xlabel('Frequency (Hz)');
% ylabel('Amplitude (dB)');
% title('信号频谱');
% grid on;
% figure;hold on;
% plot(F,10*log10(amp/maxamp),'r');
% hold on;
% xlabel('Frequency/Hz');
%  ylabel('Amp/dB');keyboard
% xlim([0.8e6,1.5e6]);
% subplot(2,1,2);
% plot((0:df:(0.5*samplerate-df)),10*log10(abs(y_fft(1:n/2))),'b');
% grid on;
% hold on;
% xlabel('Frequency/Hz');
% ylabel('phase/rad');
