function [adder,FLL_Track_Freq1,FLL_Track_Freq,pha_derivative,pha,pha1,pha3,sita_out,nco_phase]=usingPLL_closed_loop(k,SIG,samplerate,Fn,n3,pha_derivative,pha,pha1,pha3,sita_out,adder,j)
global wn

%SIG是输入信号
%j is the sequencial number of ratio
%PLL参数初始化设置

Ts=1/samplerate;
num0=n3;%1s的数据对应的积分清零点数
n1=samplerate/num0;%n1表示一个积分清零周期的积分点数。
Tcoh=n1*Ts;
factor=2^32;
trans=factor/samplerate;
%接下来进行锁频和锁相的循环

nco_phase=sita_out(j,1:n1);
nco_I=cos(nco_phase);
nco_Q=-sin(nco_phase);
%下变频
I_carr=SIG.*nco_I;
Q_carr=SIG.*nco_Q;

%积分清零器的输出
Ip=sum(I_carr);
Qp=sum(Q_carr);

pd_out=angle(Ip+1i*Qp);

%对相位差进行滤波和相位重构
pha_derivative(j,k+1)=pha_derivative(j,k)+wn(k)^3*Tcoh*pd_out;
pha1(j,k+1)=pha1(j,k)+Tcoh*pha_derivative(j,k)+2*wn(k)^2*Tcoh*pd_out;
pha2=Tcoh*pha1(j,k+1)+2*wn(k)*Tcoh*pd_out;
pha(j,k+1)=pha(j,k)+pha2;
%参考自文献《高动态环境下三阶锁相环参数设计及性能仿真》
pha3(j,k+1)=pha3(j,k)+Tcoh*pha1(j,k+1);%测量的相位输出，后向差分延迟变换

%PLL的相位更新形式
Update_Freq_Word=pha2/(2*pi*Tcoh)*trans;
facq_word=Fn(j)*trans+Update_Freq_Word;

for m=1:n1
    if m==1
        adder(j,m)=adder(j,n1)+facq_word;
    else
        adder(j,m)=adder(j,m-1)+facq_word;
    end
    
    if(adder(j,m)>=factor)
        adder(j,m)=adder(j,m)-factor;
    end
    sita_out(j,m)=adder(j,m)/factor*2*pi;
end

FLL_Track_Freq1(j)=Fn(j)+pha2/(2*pi*Tcoh);
FLL_Track_Freq(j)=Fn(j)+pha1(j,k+1)/(2*pi);%三阶降阶使用
