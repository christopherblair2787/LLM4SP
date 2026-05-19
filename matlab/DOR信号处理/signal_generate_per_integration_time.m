% function used for generating signal
% total time length is 1s
function S_plus_phase_noise=signal_generate_per_integration_time(i,fs,n1,centralfre,frate,fraterate,CNR,initial_phase,phase_noise,ratio,tao,lower_band)
%i represents i-th second signal
% fs is samplerate
% n1 is number of data points in one integration period in PLL.
% centralfre is central frequency
% frate is Doppler rate.fraterate is Doppler acceralation.
% CNR is carrier to noise ratio. the unit is dB-Hz
% initial_phase_carr is initial carrier phase of received signal.
% phase_noise represents phase noise.
% ratio is frequency dividing ratio
% tao is time delay.
% pp is the spline interpolation coefficient.
% station_label represents which station's data to generate.

Ts=1/fs;
t=((i-1)*n1+1:i*n1)*Ts;
fd1=frate*t+0.1*fraterate*t.^2;
% lower_band=ratio*centralfre-fs/4;%lower band of signal which has been down converted.
a1=1;
SNR=CNR-10*log10(fs/2);
fi=2*pi*ratio*centralfre*tao;

S1_cos=a1*cos(2*pi*(ratio*(centralfre+fd1)-lower_band).*t+fi+initial_phase);
S1_cos_plusnoise=awgn(S1_cos,SNR,'measured');%add noise
S1_sin=a1*sin(2*pi*(ratio*(centralfre+fd1)-lower_band).*t+fi+initial_phase);
S1_sin_plusnoise=awgn(S1_sin,SNR,'measured');

S1_plusnoise=complex(S1_cos_plusnoise,S1_sin_plusnoise);
S1=S1_plusnoise;%.*exp(ratio*1i*phase_noise);

S_plus_phase_noise=real(S1);
