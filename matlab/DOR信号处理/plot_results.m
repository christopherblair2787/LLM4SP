
close all
clc
clear all

% 参数配置（需与 main.m 保持一致）
stations={'LX','KM','TM','UR'};
fs = 4e6;
num_per_second = 200;
centralfre=8469.23e6;
f0 = centralfre;
ratio = [439/440 2199/2200 1 2201/2200 441/440];
subcarrier_index_num = ratio;

% 绘图处理参数
Fs = 100; % 下采样后的采样率
down = 1;
sec_everytime = 1;
dop_steplength= 0.001;
tintegral_doppler= 1;
dop_range = 0.2;
t_doppler=[0:1/(Fs/down):tintegral_doppler-1/(Fs/down)]';

% 定义需要差分的双站组合
pair_stations = {'UR', 'KM'}; 
% 对应原 stations 中的索引
pair_indices = [find(strcmp(stations, pair_stations{1})), find(strcmp(stations, pair_stations{2}))];

% 存储两个站的侧音相位差结果
% 结构：station_results{1} 存站1的 [vco_sec1, vco_sec2]
% vco_sec1 是侧音1的相位差，vco_sec2 是侧音5的相位差
station_results = cell(1, 2);
F0_all = [];
F0_all_2 = [];
phase0_all = [];
phase0_all_2 = [];
% 遍历双站
for k = 1:2
    s_idx = pair_indices(k);
    station = stations{s_idx};
    
    % 读取主载波数据
    main_dir = fullfile(pwd, station, 'main_carrier');
    files_main = dir(fullfile(main_dir, '*.dat'));
    
    % 按文件名中的数字排序 (1.dat, 2.dat, ...)
    [~, sort_idx] = sort(str2double(regexp({files_main.name}, '\d+', 'match', 'once')));
    files_main = files_main(sort_idx);
    
    % 读取光行时模型 (用于 tau 计算)
    lighttime_dir = ['D:\shao_code\光行时\', station, 'lighttime_chan3.dat'];
    lighttime_model = readmatrix(lighttime_dir);
    
    % 初始化存储变量
    vco_sec1 = zeros(length(files_main), 1);
    vco_sec2 = zeros(length(files_main), 1);
    
    % aid1 和 aid5 对应的子载波索引
    idx_aid1 = 1;
    idx_aid5 = 5;
    
    % 获取 aid1 和 aid5 的文件列表
    aid1_dir = fullfile(pwd, station, ['aid' num2str(idx_aid1)]);
    files_aid1 = dir(fullfile(aid1_dir, '*.dat'));
    [~, sort_idx1] = sort(str2double(regexp({files_aid1.name}, '\d+', 'match', 'once')));
    sort_vco1 = files_aid1(sort_idx1);
    
    aid5_dir = fullfile(pwd, station, ['aid' num2str(idx_aid5)]);
    files_aid5 = dir(fullfile(aid5_dir, '*.dat'));
    [~, sort_idx2] = sort(str2double(regexp({files_aid5.name}, '\d+', 'match', 'once')));
    sort_vco2 = files_aid5(sort_idx2);
    
    last_phase1 = [];
    last_phase2 = [];
    
    for j = 1:length(files_main)
        % 读取主载波数据
        filepath = fullfile(main_dir, files_main(j).name);
        data1 = readmatrix(filepath); % [t_seq, FLL, tp2, Fn]
        
        row_idx = min(j, size(lighttime_model, 1));
        a0 = lighttime_model(row_idx, 7);
        a1 = lighttime_model(row_idx, 6);
        a2 = lighttime_model(row_idx, 5);
        a3 = lighttime_model(row_idx, 4);
        a4 = lighttime_model(row_idx, 3);
        a5 = lighttime_model(row_idx, 2);
        % 修正时标参考点，使其与 fs=4e6 匹配
        t_center_ref = 0.5 + 0.5/fs; 
        time_len_sec = t_center_ref;
        tau = a0 + a1*time_len_sec + a2*time_len_sec.^2 + a3*time_len_sec.^3 + a4*time_len_sec.^4 + a5*time_len_sec.^5;
        n1 = fs / num_per_second;
        mTau = tau;%mean(reshape(tau, n1, []), 1)'; % 按积分周期平均
        
        % 处理 aid1 侧音
        fid_1 = fopen(fullfile(aid1_dir, sort_vco1(j).name), 'r');
        datayuan = fread(fid_1, inf, 'single'); % main.m 中写入的是 single
        fclose(fid_1);
        
        % 重塑为复数信号 (交替存储 [Real1, Imag1, ...])
        data_complex = complex(datayuan(1:2:end), datayuan(2:2:end));
        
        % 降采样
        Signal_down = downfilter(data_complex, Fs, 1, tintegral_doppler); % down=fs/Fs=2000
        
        % FFT 和精细频率/相位估计
        vco_timestr = num2str(j);
        [F_estimate, noise] = showfft2side0(Signal_down, Fs, 'in');
        [F0, phase0] = FrePhaseestimatesec(Signal_down, F_estimate, t_doppler', dop_range, dop_steplength, tintegral_doppler, noise, vco_timestr);
        F0_all(k, j) = F0;
        phase0_all(k, j) = phase0;
        % 相位解卷绕
        if isempty(last_phase1)
            phase0_adj1 = phase0;
        else
            k_wrap = round((last_phase1 - phase0) / (2*pi));
            phase0_adj1 = phase0 + 2*pi*k_wrap;
        end
        last_phase1 = phase0_adj1;
        
        % 处理 aid5 侧音
        fid_5 = fopen(fullfile(aid5_dir, sort_vco2(j).name), 'r');
        datayuan = fread(fid_5, inf, 'single');
        fclose(fid_5);
        
        data_complex = complex(datayuan(1:2:end), datayuan(2:2:end));
        
        % 降采样
        Signal_down = downfilter(data_complex, Fs, 1, tintegral_doppler); 
        
        [F_estimate, noise] = showfft2side0(Signal_down, Fs, 'in');
        [F02, phase0] = FrePhaseestimatesec(Signal_down, F_estimate, t_doppler', dop_range, dop_steplength, tintegral_doppler, noise, vco_timestr);
        F0_all_2(k, j) = F02;
        phase0_all_2(k, j) = phase0;
        if isempty(last_phase2)
            phase0_adj2 = phase0;
        else
            k_wrap = round((last_phase2 - phase0) / (2*pi));
            phase0_adj2 = phase0 + 2*pi*k_wrap;
        end
        last_phase2 = phase0_adj2;
        
        %主载波射频相位
        tp2_sec = mean(data1(:, 3));
       
        carrier_phase = tp2_sec;
        
        
        t_seq = mean(data1(:, 1));
        t_1s = t_seq + mean(mTau);
       
        term_geo = 2*pi*subcarrier_index_num(idx_aid1)*f0*t_1s;
        term_carrier = carrier_phase * subcarrier_index_num(idx_aid1);
        
        vco_sec1(j) = term_carrier + phase0_adj1 + 2*pi*F0*t_center_ref - term_geo;
        % vco_sec1(j) = term_carrier - term_geo;
        
        % 侧音 5 解算
        term_geo = 2*pi*subcarrier_index_num(idx_aid5)*f0*t_1s;
        term_carrier = carrier_phase * subcarrier_index_num(idx_aid5);
        
        vco_sec2(j) = term_carrier + phase0_adj2 + 2*pi*F02*t_center_ref - term_geo;
        % vco_sec2(j) = term_carrier - term_geo;
    end
    
    % 存储该站的结果
    station_results{k} = [vco_sec1, vco_sec2];
end

% 计算双差分时延
% station_results{1} 是站1的 [侧音1, 侧音5]
% station_results{2} 是站2的 [侧音1, 侧音5]

vco_sec1_st1 = station_results{1}(:, 1); % LX 侧音1
vco_sec2_st1 = station_results{1}(:, 2); % LX 侧音5

vco_sec1_st2 = station_results{2}(:, 1); % KM 侧音1
vco_sec2_st2 = station_results{2}(:, 2); % KM 侧音5

% 去模糊
vco_sec1_st1 = vco_sec1_st1 - 2*pi*round(vco_sec1_st1/(2*pi));
vco_sec2_st1 = vco_sec2_st1 - 2*pi*round(vco_sec2_st1/(2*pi));
vco_sec1_st2 = vco_sec1_st2 - 2*pi*round(vco_sec1_st2/(2*pi));
vco_sec2_st2 = vco_sec2_st2 - 2*pi*round(vco_sec2_st2/(2*pi));

% 双差分公式：
% (站2侧音2 - 站1侧音2) - (站2侧音1 - 站1侧音1)
% 即 (KM侧音5 - LX侧音5) - (KM侧音1 - LX侧音1)
% 注意：这里侧音2对应 aid5

diff_aid5 = vco_sec2_st2 - vco_sec2_st1;
diff_aid1 = vco_sec1_st2 - vco_sec1_st1;

% 再次去模糊
diff_aid5 = diff_aid5 - 2*pi*round(diff_aid5/(2*pi));
diff_aid1 = diff_aid1 - 2*pi*round(diff_aid1/(2*pi));

% 最终双差分相位
double_diff_phase = diff_aid5 - diff_aid1;
double_diff_phase = double_diff_phase - 2*pi*round(double_diff_phase/(2*pi));

% 转换为时延
% delay = phase / (2*pi * (f_aid5 - f_aid1))
% f_aid5 = ratio5 * f0, f_aid1 = ratio1 * f0
temp1 = f0 * (subcarrier_index_num(idx_aid5) - subcarrier_index_num(idx_aid1));
delay_ns = (double_diff_phase / temp1 / (2*pi)) * 1e9;

% 绘图
figure;
plot(1:length(delay_ns), delay_ns, '.');
title(['Double Differential Delay (', pair_stations{2}, ' - ', pair_stations{1}, ')']);
xlabel('Time (s)');
ylabel('Delay (ns)');
grid on;

figure();plot(vco_sec1_st1, '.');title("station1 aid1");ylabel("rad");xlabel("s");
figure();plot(vco_sec2_st1, '.');title("station1 aid7");ylabel("rad");xlabel("s");
figure();plot(vco_sec1_st2, '.');title("station2 aid1");ylabel("rad");xlabel("s");
figure();plot(vco_sec2_st2, '.');title("station2 aid1");ylabel("rad");xlabel("s");
figure();plot(F0_all(1,:), '.');title("station1 aid1 F0");ylabel("Hz");xlabel("s");
figure();plot(F0_all(2,:), '.');title("station2 aid1 F0");ylabel("Hz");xlabel("s");
figure();plot(F0_all_2(1,:), '.');title("station1 aid7 F0");ylabel("Hz");xlabel("s");
figure();plot(F0_all_2(2,:), '.');title("station2 aid7 F0");ylabel("Hz");xlabel("s");
figure();plot(phase0_all(1,:), '.');title("station1 aid1 phase0");ylabel("rad");xlabel("s");
figure();plot(phase0_all_2(2,:), '.');title("station2 aid1 phase0");ylabel("rad");xlabel("s");
figure();plot(phase0_all_2(1,:), '.');title("station1 aid7 phase0");ylabel("rad");xlabel("s");
figure();plot(phase0_all(2,:), '.');title("station2 aid1 phase0");ylabel("rad");xlabel("s");

keyboard