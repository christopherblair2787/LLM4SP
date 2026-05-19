%%%fit=2

function [X,Y,p,sigma_y_err]=selectdata_sigma(x,y,sigma) 

index_y_max_err=0;
y=y(:);
x=x(:);
length_x=length(x);

if length_x> 5
    p=polyfit(x,y,2);
    y_remainder_err=y-polyval(p,x);
    sigma_y_err=std(y_remainder_err);
    [sigma_y_max_err index_y_max_err]=max(abs(y_remainder_err));
    
    while (length_x >2) & (sigma_y_max_err> sigma*sigma_y_err)
        x(index_y_max_err)=[];
        y(index_y_max_err)=[];
        p=polyfit(x,y,2);
        y_remainder_err=y-polyval(p,x);
        sigma_y_err=std(y_remainder_err);
        [sigma_y_max_err index_y_max_err]=max(abs(y_remainder_err));
        length_x=length(x);
    end
end

X=x(:);
Y=y(:);
        
