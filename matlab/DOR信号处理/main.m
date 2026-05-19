close all;
clc;
clear;
fclose all;
format long;
tic;

global wn
global pd_out pha FLL_Track_Freq FLL_Track_Freq1 pha_derivative pha1 pha2 sita_out pha3 adder sigma_y_err
global Nfft window_minpoint window_maxpoint integral_time_of_phase
global bits_of_data fanout sbit
global samplerate subcarrier_chan_num subcarrier_index_num chan_freq timesamplerate down_samplerate chan

param_file = fullfile('..', '老版', 'file_parameter.txt');
[sourcefiledir,~,resultfiledir,integral_of_PLL,station_str,...
    windowmin_referencefre,windowmax_referencefre,sbit,samplerate,...
    sizeof_sec,fanout,bits_of_data,maincarrier_chan,~,~,integral_of_Fn,~,Aid_sec,~,~,integral_time_of_phase,down_samplerate] = read_parameter(param_file);

sourcefiledir = ensureTrailingSlash(sourcefiledir);
resultfiledir = ensureTrailingSlash(resultfiledir);

timesamplerate = 1 / samplerate;
Nfft = samplerate;
window_minpoint = floor(windowmin_referencefre / (samplerate / Nfft));
window_maxpoint = floor(windowmax_referencefre / (samplerate / Nfft));

chan = maincarrier_chan;
if isempty(chan)
    error('maincarrier_chan is empty in parameter file.');
end
chan = chan(1);

% Keep the same constants as old main.m.
subcarrier_chan_num = [1 2 2 2 3];
subcarrier_index_num = [439/440 2199/2200 1 2201/2200 441/440];
chan_freq = [8396.000 8412.000 8428.000] * 1e6;

stations = parseStations(station_str);
if isempty(stations)
    error('No station configured in parameter file.');
end

n3 = round(1 / integral_of_PLL);
if n3 <= 0
    error('integral_of_PLL must be positive.');
end
n1 = samplerate / n3;
if mod(n1, 1) ~= 0
    error('samplerate / n3 must be an integer.');
end

sizeof_Fn = integral_of_Fn * samplerate / fanout;

for i_station = 1:length(stations)
    station = stations{i_station};
    station_input = [sourcefiledir lower(station) '/'];

    if ~exist(station_input, 'dir')
        warning('Input directory not found, skip station %s: %s', station, station_input);
        continue;
    end

    files = dir(fullfile(station_input, '*.dat'));
    if isempty(files)
        warning('No .dat files found for station %s under %s', station, station_input);
        continue;
    end
    [~, order] = sort({files.name});
    files = files(order);

    first_file = fullfile(station_input, files(1).name);
    fid_first = fopen(first_file, 'rb');
    if fid_first < 0
        warning('Cannot open first file for station %s: %s', station, first_file);
        continue;
    end
    [~, sig_first] = datarecover(fid_first, sizeof_Fn, chan);
    fclose(fid_first);

    [Fn, ~] = getFn(sig_first, samplerate, integral_of_Fn);

    dot_length = 0:n1-1;
    sita_out = 2 * pi * dot_length * timesamplerate * Fn;
    pha = zeros(1, n3 + 1);
    pd_out = zeros(1, n3 + 1);
    pha_derivative = zeros(1, n3 + 1);
    pha1 = zeros(1, n3 + 1);
    pha2 = zeros(1, n3 + 1);
    pha3 = zeros(1, n3 + 1);
    adder = zeros(1, n1);

    wn0 = buildWn(n3, numel(files));

    main_out_dir = [resultfiledir station '/main_carrier/'];
    ensureDir(main_out_dir);
    for iaidchan = 1:length(subcarrier_index_num)
        ensureDir([resultfiledir station '/aid' num2str(iaidchan) '/']);
    end

    n_present = 1;
    for i_file = 1:numel(files)
        file_path = fullfile(station_input, files(i_file).name);
        d = dir(file_path);
        if isempty(d) || d.bytes < sizeof_sec
            warning('Skip short file: %s', file_path);
            continue;
        end

        fid = fopen(file_path, 'rb');
        if fid < 0
            warning('Cannot open file: %s', file_path);
            continue;
        end
        [~, SIG] = datarecover(fid, sizeof_Fn, chan);
        fclose(fid);

        wn = wn0((n_present-1)*n3+1:n_present*n3);
        [phase_carrier, ~] = usingPLL_new_original_for_processed1s_pertime(SIG, samplerate, Fn, n3);

        t_seq = (n_present - 1) + (0.5/n3:1/n3:1-0.5/n3);
        tp2 = pha3(1:end-1) - 2*pi*(Fn + (FLL_Track_Freq - Fn)/2) * (1/n3);
        data_to_save = [t_seq(:), FLL_Track_Freq(:), tp2(:), repmat(Fn, n3, 1)];

        main_file = [main_out_dir station num2str(n_present) '.dat'];
        writematrix(data_to_save, main_file, 'Delimiter', ' ');

        for iaidchan = 1:length(subcarrier_index_num)
            aid_dir = [resultfiledir station '/aid' num2str(iaidchan) '/'];
            aid_file = [aid_dir station num2str(n_present) '.dat'];
            fid_vco = fopen(aid_file, 'wb');
            if fid_vco > 0
                subcarrier(SIG(:), phase_carrier, iaidchan, Aid_sec, Fn, n_present, fid_vco);
                fclose(fid_vco);
            end
        end

        pha = [pha(end), zeros(1, n3)];
        pd_out = [pd_out(end), zeros(1, n3)];
        pha_derivative = [pha_derivative(end), zeros(1, n3)];
        pha1 = [pha1(end), zeros(1, n3)];
        pha2 = [pha2(end), zeros(1, n3)];
        pha3 = [pha3(end), zeros(1, n3)];

        n_present = n_present + 1;
    end
end

toc;

function p = ensureTrailingSlash(p)
if p(end) ~= '/'
    p = [p '/'];
end
end

function ensureDir(p)
if ~exist(p, 'dir')
    mkdir(p);
end
end

function stations = parseStations(station_str)
if iscell(station_str)
    stations = station_str;
    return;
end
parts = strsplit(strtrim(station_str));
parts = parts(~cellfun(@isempty, parts));
stations = parts;
end

function wn0 = buildWn(n3, nsec)
wn0 = zeros(1, n3 * max(1, nsec));
m0 = 2;
m1 = 5;
w00 = 10;
wend = 5;
wn0(1:n3*m0) = w00;
tt = m0*n3 + 1:min(m1*n3, numel(wn0));
if ~isempty(tt)
    v = (1/wend - 1/w00) / (n3 * (m1 - m0));
    wn0(tt) = 1 ./ (1/w00 + v * (tt - m0*n3));
end
if numel(wn0) > n3*m1
    wn0(n3*m1+1:end) = wn0(n3*m1);
end
end
