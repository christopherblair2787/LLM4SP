function [ output_args ] = subcarrier(SIG, phase2_carrier,iaidchan,Aid_sec,Fn,num_fd,fid_vco)
global subcarrier_chan_num subcarrier_index_num chan_freq samplerate chan timesamplerate down_samplerate
output_args=[];
down=samplerate/down_samplerate;
chan_AID=subcarrier_chan_num(iaidchan);
time_sample=[timesamplerate/2:timesamplerate:Aid_sec-timesamplerate/2];
phase_AID=((chan_freq(chan(1))+Fn)*subcarrier_index_num(iaidchan)-chan_freq(chan_AID))*(time_sample+num_fd-1)*2*pi+phase2_carrier*subcarrier_index_num(iaidchan);
signal_AID=exp(-1j*phase_AID);
signal_rotation=SIG.*(signal_AID.');
signal_reshape=reshape(signal_rotation,down,down_samplerate);
signal_mean=mean(signal_reshape);
% 改为交替存储 [Real1, Imag1, Real2, Imag2, ...]
signal_write = zeros(1, 2*length(signal_mean));
signal_write(1:2:end) = real(signal_mean);
signal_write(2:2:end) = imag(signal_mean);

if ~isempty(fid_vco) && fid_vco>0
    fwrite(fid_vco,signal_write,'single');
end
end
