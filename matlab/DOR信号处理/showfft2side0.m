function [F_estimate,noise]=showfft2side(xulie,caiyanglv,s,ichan,chanall_new,samestr)
% 计算信号序列的双边谱主峰频率和噪声均值

global bl; % 声明全局变量 bl

N_fft=1024*16; % FFT点数
df=caiyanglv/N_fft; % 频率分辨率

% 对输入序列做FFT
y_fft=fft(xulie,N_fft);

% 构造频率轴
F=(-0.5*caiyanglv:df:(0.5*caiyanglv-df));

% 计算幅度谱（dB），并移到中心
amp=fftshift(10*log10(abs(y_fft)));

% 找到最大幅度及其位置
[ampmax,position]=max(amp);

% 估算主峰频率
F_estimate=F(position);

% 估算主峰右侧的噪声均值
noise=mean(amp(position+8:N_fft));

% 以下为注释掉的绘图和保存代码
% figure();
% % subplot(1,3,ichan)
% plot((-0.5*caiyanglv:df:(0.5*caiyanglv-df)),fftshift(20*log10(abs(y_fft))),'r');
% % title(char(chanall_new{ichan}));
% xlabel('Frequency (Hz)');ylabel('PSD (dB)')
% saveas(gcf,['/vlbi/hx1/doppler/s3c28g_errcrt/',samestr,num2str(bl)],'fig');
% saveas(gcf,['/vlbi/hx1/doppler/s3c28g_errcrt/',samestr,num2str(bl)],'jpg');

% 其他注释掉的绘图代码
% grid on;
% title(s);
% xlabel('frequency(Hz)');
% ylabel('amp(dB)');
% subplot(2,1,2);
% plot((-0.5*caiyanglv:df:(0.5*caiyanglv-df)),fftshift(10*log10(angle(y_fft))));
% grid on;
% xlabel('frequency(Hz)');
% ylabel('phase(rad)');
