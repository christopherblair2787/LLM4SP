function y=showfft2side(xulie,caiyanglv,s)
%y=showfft(xuliu,caiyanglv,s)
%�ú�����������е�fft��,���ڱ��⴦��ʾs�ַ�
N_fft=2^15;
df=caiyanglv/N_fft;

hold on
 figure(4);hold on;
% subplot(2,1,1);
y_fft=fft(xulie,N_fft);
plot((-0.5*caiyanglv:df:(0.5*caiyanglv-df)),fftshift(10*log10(abs(y_fft)/max(abs(y_fft)))),'r');
grid on;
% title(s);
xlabel('frequency(Hz)');
ylabel('amp(dB)');
% figure;
%  plot((-0.5*caiyanglv:df:(0.5*caiyanglv-df)),fftshift(10*log10(angle(y_fft))));
% grid on;
%  xlabel('frequency(Hz)');
%  ylabel('amp(dB)');
