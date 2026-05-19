function phase_correct_out=solveambiguity_qua_correct(phase_correct,ratio,label)
%接下来进行相位模糊度的消除
para=2;
pa=1;

i0=find(ratio==1);

for i=1:length(phase_correct)
    if i~=i0
        errorphase1=phase_correct(i)-phase_correct(i0);
        while abs(errorphase1)>pa*pi
            if errorphase1<0
                errorphase1=errorphase1+para*pi;
                phase_correct(i)=phase_correct(i)+para*pi;
            else
                errorphase1=errorphase1-para*pi;
                phase_correct(i)=phase_correct(i)-para*pi;
            end
        end
    end
end
phase_correct_out=phase_correct;

%% 继续微调
if label>0
    n=length(ratio);
    if i0+2<=n
        p1=phase_correct_out(i0+1)-phase_correct_out(i0-1);
        p2=phase_correct_out(i0+2)-phase_correct_out(i0+1);
        delta_fi1=p2-p1;
        n1=round(delta_fi1/(2*pi));
        phase_correct_out(i0+2)=phase_correct_out(i0+2)-n1*2*pi;%校准
    end
    
    if i0-2>0
        p3=phase_correct_out(i0+2)-phase_correct_out(i0-1);
        p4=phase_correct_out(i0-1)-phase_correct_out(i0-2);
        delta_fi2=p4-p3;
        n2=round(delta_fi2/(2*pi));
        phase_correct_out(i0-2)=phase_correct_out(i0-2)+n2*2*pi;%校准
    end
    
    if i0+3<=n
        p5=phase_correct_out(i0+2)-phase_correct_out(i0-2);
        p6=phase_correct_out(i0+3)-phase_correct_out(i0+2);
        delta_fi3=p6-p5;
        n3=round(delta_fi3/(2*pi));
        phase_correct_out(i0+3)=phase_correct_out(i0+3)-n3*2*pi;%校准
    end
    
    if i0-3>0
        p7=phase_correct_out(i0+3)-phase_correct_out(i0-2);
        p8=phase_correct_out(i0-2)-phase_correct_out(i0-3);
        delta_fi4=p8-p7;
        n4=round(delta_fi4/(2*pi));
        phase_correct_out(i0-3)=phase_correct_out(i0-3)+n4*2*pi;%校准
    end
    
    if i0+4<=n
        p9=phase_correct_out(i0+3)-phase_correct_out(i0-3);
        p10=phase_correct_out(i0+4)-phase_correct_out(i0+3);
        delta_fi5=p10-p9;
        n5=round(delta_fi5/(2*pi));
        phase_correct_out(i0+4)=phase_correct_out(i0+4)-n5*2*pi;%校准
    end
end
