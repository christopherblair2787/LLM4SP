function [phase_carrier, phase_fit] = usingPLL_new_original_for_processed1s_pertime(SIG,samplerate,Fn,n3)
global wn pd_out pha FLL_Track_Freq FLL_Track_Freq1 pha_derivative pha1 pha2 sita_out pha3 adder phase_carrier phase_fit sigma_y_err

n0=samplerate;
Ts=1/n0;
num0=n3;
num=num0;
n1=n0/num0;

Tcoh=n1*Ts;
Ip=zeros(1,num);
Qp=zeros(1,num);

factor=2^32;
trans=factor/samplerate;
Update_Freq_Word=zeros(1,num);
facq_word=zeros(1,num+1);

for k=1:num
   
   n_sample=(k-1)*n1+1:k*n1;
   s_I=SIG(n_sample);
   nco_I=cos(sita_out(1:n1));
   nco_Q=-sin(sita_out(1:n1));
   
   I_carr=s_I.*nco_I;
   Q_carr=s_I.*nco_Q;
   
   Ip(k)=sum(I_carr);
   Qp(k)=sum(Q_carr);
   
   pd_out(k+1)=angle(Ip(k)+1i*Qp(k));
   
   pha_derivative(k+1)=pha_derivative(k)+wn(k)^3*Tcoh*pd_out(k+1);
   pha1(k+1)=pha1(k)+Tcoh*pha_derivative(k)+2*wn(k)^2*Tcoh*pd_out(k+1);
   
   pha2(k+1)=Tcoh*pha1(k+1)+2*wn(k)*Tcoh*pd_out(k+1);
   
   pha(k+1)=pha(k)+pha2(k+1);
   pha3(k+1)=pha3(k)+Tcoh*pha1(k+1);
   
   Update_Freq_Word(k)=pha2(k+1)/(2*pi*Tcoh)*trans;
   facq_word(k)=Fn*trans+Update_Freq_Word(k);
   
   for m=1:n1
      if m==1
         adder(m)=adder(n1)+facq_word(k);
      else
         adder(m)=adder(m-1)+facq_word(k);
      end
      
      if(adder(m)>=factor)
         adder(m)=adder(m)-factor;
      end
      
      sita_out(m)=adder(m)/factor*2*pi;
   end
   
   FLL_Track_Freq1(k) = Fn+pha2(k)/(2*pi*Tcoh);
   FLL_Track_Freq(k)  = Fn+pha1(k)/(2*pi);
   
end

integral_of_PLL = 1/num;
time_fit_phase=[0:integral_of_PLL:1-integral_of_PLL]+integral_of_PLL/2;
Track_fre = (FLL_Track_Freq - Fn)';
Track_pha = pha3(1:end-1) - 2*pi*(Fn + (FLL_Track_Freq - Fn)/2)*(1/n3);
[time_fit_phase_deleteoutliers,fd_msec_deleteoutliers,phase_msec_deleteoutliers,sigma_y_err,p_phase]=selectdata_sigma_delete(time_fit_phase,Track_fre,3,Track_pha);
phase_carrier=polyval(p_phase,[0:1/samplerate:1-1/samplerate]);
phase_fit=polyval(p_phase,time_fit_phase');
