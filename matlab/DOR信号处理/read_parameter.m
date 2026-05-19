function [sourcefiledir,jobfiledir,resultfiledir,integral_of_PLL,station,...
   windowmin_referencefre,windowmax_referencefre,sbit,samplerate,...
    sizeof_sec,fanout,bits_of_data,maincarrier_chan,scan_sec,day_begin,integral_of_Fn,subcarrier_chan,Aid_sec,subcarrier_index,carrier_aid,integral_time_of_phase,down_samplerate]= read_parameter(file_parameter)

if nargin < 1 || isempty(file_parameter)
    file_parameter = 'file_parameter.txt';
end

[RDFid,message] = fopen(file_parameter,'r');
if RDFid == -1
    error('Failed to open parameter file: %s (%s)', file_parameter, message);
end

while feof(RDFid) ~= 1
    tline = fgetl(RDFid);
    if ~ischar(tline)
        continue;
    end
    [key,value] = readline(tline);
    switch key
        case 'sourcefiledir'
            sourcefiledir = value(2:length(value)-1);
        case 'resultfiledir'
            resultfiledir = value(2:length(value)-1);
        case 'jobfiledir'
            jobfiledir = value(2:length(value)-1);
        case 'integral_of_PLL'
            integral_of_PLL = str2num(value); %#ok<ST2NM>
        case 'station'
            station = value(2:length(value)-1);
        case 'windowmin_referencefre'
            windowmin_referencefre = str2num(value); %#ok<ST2NM>
        case 'windowmax_referencefre'
            windowmax_referencefre = str2num(value); %#ok<ST2NM>
        case 'sbit'
            sbit = str2num(value); %#ok<ST2NM>
        case 'samplerate'
            samplerate = str2num(value); %#ok<ST2NM>
        case 'sizeof_sec'
            sizeof_sec = str2num(value); %#ok<ST2NM>
        case 'fanout'
            fanout = str2num(value); %#ok<ST2NM>
        case 'bits_of_data'
            bits_of_data = str2num(value); %#ok<ST2NM>
        case 'maincarrier_chan'
            maincarrier_chan = str2num(value); %#ok<ST2NM>
        case 'scan_sec'
            scan_sec = str2num(value); %#ok<ST2NM>
        case 'day_begin'
            day_begin = str2num(value); %#ok<ST2NM>
        case 'integral_of_Fn'
            integral_of_Fn = str2num(value); %#ok<ST2NM>
        case 'subcarrier_chan'
            subcarrier_chan = value(2:length(value)-1);
        case 'Aid_sec'
            Aid_sec = str2num(value); %#ok<ST2NM>
        case 'subcarrier_index'
            subcarrier_index = value(2:length(value)-1);
        case 'carrier_aid'
            carrier_aid = str2num(value); %#ok<ST2NM>
        case 'integral_time_of_phase'
            integral_time_of_phase = str2num(value); %#ok<ST2NM>
        case 'down_samplerate'
            down_samplerate = str2num(value); %#ok<ST2NM>
    end
end

fclose(RDFid);
end
