function [datarecover_ok,SIG]=datarecover(fidsource,sizeof_inputdata,chan1)

global  bits_of_data fanout sbit

%keyboard;
table=[-3.3359;-1.0;1.0;3.3359];

srt_int=['uint',num2str(bits_of_data)];

data=fread(fidsource,sizeof_inputdata,srt_int); %��ȡ��СΪM�Ķ�������ݾ���?
%

% sizeof_inputdata
% length(data)
if sbit==1
    if fanout==2
        
        if chan1==1
            DA1=bitget(data,1)-0.5;%0.5Ϊ���Ƶ�ƽ
            DA2=bitget(data,2)-0.5;
            SIG=[DA1 DA2];
            SIG=reshape(SIG',1,[]);% ��DA1��DA2�ϲ�Ϊһ��
            
        else
            if chan1==2
                DA1=bitget(data,3)-0.5;%0.5Ϊ���Ƶ�ƽ
                DA2=bitget(data,4)-0.5;
                SIG=[DA1 DA2];
                SIG=reshape(SIG',1,[]);% ��DA1��DA2�ϲ�Ϊһ��
                
            else
                if chan1==3
                    DA1=bitget(data,5)-0.5;%0.5Ϊ���Ƶ�ƽ
                    DA2=bitget(data,6)-0.5;
                    SIG=[DA1 DA2];
                    SIG=reshape(SIG',1,[]);% ��DA1��DA2�ϲ�Ϊһ��
                    %       lengthSIG=length(SIG);
                else
                    if chan1==4
                        DA1=bitget(data,7)-0.5;%0.5Ϊ���Ƶ�ƽ
                        DA2=bitget(data,8)-0.5;
                        SIG=[DA1 DA2];
                        SIG=reshape(SIG',1,[]);% ��DA1��DA2�ϲ�Ϊһ��
                        %           lengthSIG=length(SIG);
                    end
                end
            end
        end
        
    else
        if fanout==4
            if chan1==1
                DA1=bitget(data,1)-0.5;%0.5Ϊ���Ƶ�ƽ
                DA2=bitget(data,3)-0.5;
                
                DA3=bitget(data,5)-0.5;%0.5Ϊ���Ƶ�ƽ
                DA4=bitget(data,7)-0.5;
                
                
                SIG=[DA1 DA2  DA3  DA4];
                SIG=reshape(SIG',1,[]);%
                
                %                 SIG=DA1';
                %                length(SIG)
            else
                if chan1==2
                    DA1=bitget(data,9)-0.5;%0.5Ϊ���Ƶ�ƽ
                    DA2=bitget(data,11)-0.5;
                    
                    DA3=bitget(data,13)-0.5;%0.5Ϊ���Ƶ�ƽ
                    DA4=bitget(data,15)-0.5;
                    
                    
                    SIG=[DA1 DA2  DA3  DA4];
                    SIG=reshape(SIG',1,[]);%
                    
                else
                    if chan1==3
                        DA1=bitget(data,2)-0.5;%0.5Ϊ���Ƶ�ƽ
                        DA2=bitget(data,4)-0.5;
                        
                        DA3=bitget(data,6)-0.5;%0.5Ϊ���Ƶ�ƽ
                        DA4=bitget(data,8)-0.5;
                        
                        
                        SIG=[DA1 DA2  DA3  DA4];
                        SIG=reshape(SIG',1,[]);%
                        
                    else
                        if chan1==4
                            DA1=bitget(data,18)-0.5;%0.5Ϊ���Ƶ�ƽ
                            DA2=bitget(data,20)-0.5;
                            
                            DA3=bitget(data,22)-0.5;%0.5Ϊ���Ƶ�ƽ
                            DA4=bitget(data,24)-0.5;
                            
                            
                            SIG=[DA1 DA2  DA3  DA4];
                            SIG=reshape(SIG',1,[]);%
                        end
                    end
                end
                
                
                
            end
            
        else
            if fanout==1
                if chan1==1
                    DA1=bitget(data,7)-0.5;
                    SIG=DA1';
                end
                
                if chan1==2
                    DA1=bitget(data,8)-0.5;
                    SIG=DA1';
                end
                
                if chan1==3
                    DA1=bitget(data,1)-0.5;
                    SIG=DA1';
                end
                if chan1==4
                    DA1=bitget(data,2)-0.5;
                    SIG=DA1';
                end
                
                if chan1==5
                    DA1=bitget(data,3)-0.5;
                    SIG=DA1';
                end
                
                if chan1==6
                    DA1=bitget(data,4)-0.5;
                    SIG=DA1';
                end
                
                if chan1==7
                    DA1=bitget(data,5)-0.5;
                    SIG=DA1';
                end
                
                if chan1==8
                    DA1=bitget(data,6)-0.5;
                    SIG=DA1';
                end
                
                
                
            end
        end
    end
    
else if sbit==2
        if fanout==4
            if chan1==1
                
                
                %             DA1=bitget(data,1:8:9)
                %
                %             DA2=bitget(data,3:8:11)
                %
                %             DA3=bitget(data,5:8:13)%0.5Ϊ���Ƶ�ƽ
                %             DA4=bitget(data,7:8:15)
                %             DA5=bitget(data,8:8:16)
                %             DA6=bitget(data,9:8:17)
                %             DA7=bitget(data,10:8:18)
                %             DA8=bitget(data,32)
                
                %             DA6=bitget(data,11)
                %              DA7=bitget(data,13)
                %               DA8=bitget(data,15)
                %
                %
                
                DA1=bitget(data,1);
                DA2=bitget(data,3);
                
                DA3=bitget(data,5);%0.5Ϊ���Ƶ�ƽ
                DA4=bitget(data,7);
                
                DA5=bitget(data,9);
                DA6=bitget(data,11);
                DA7=bitget(data,13);
                DA8=bitget(data,15);
                sig1=DA1*2+DA5;
                sig2=DA2*2+DA6;
                sig3=DA3*2+DA7;
                sig4=DA4*2+DA8;
                
                data_result1=table(sig1+1);
                data_result2=table(sig2+1);
                data_result3=table(sig3+1);
                data_result4=table(sig4+1);
                SIG=[data_result1 data_result2 data_result3 data_result4];
                SIG=reshape(SIG',1,[]);
            end
            
            
            %             SIG=[DA1 DA2  DA3  DA4 DA5 DA6  DA7 DA8]
            %             SIG=reshape(SIG',1,[])%
            
            %                 SIG=DA1';
            %                length(SIG)
            %         else
            %             if chan==2
            %                 DA1=bitget(data,9)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                 DA2=bitget(data,11)-0.5;
            %
            %                 DA3=bitget(data,13)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                 DA4=bitget(data,15)-0.5;
            %
            %
            %                 SIG=[DA1 DA2  DA3  DA4];
            %                 SIG=reshape(SIG',1,[]);%
            %
            %             else
            %                 if chan==3
            %                 DA1=bitget(data,2)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                 DA2=bitget(data,4)-0.5;
            %
            %                 DA3=bitget(data,6)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                 DA4=bitget(data,8)-0.5;
            %
            %
            %                 SIG=[DA1 DA2  DA3  DA4];
            %                 SIG=reshape(SIG',1,[]);%
            %
            %                 else
            %                     if chan==4
            %                     DA1=bitget(data,18)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                     DA2=bitget(data,20)-0.5;
            %
            %                     DA3=bitget(data,22)-0.5;%0.5Ϊ���Ƶ�ƽ
            %                     DA4=bitget(data,24)-0.5;
            %
            %
            %                     SIG=[DA1 DA2  DA3  DA4];
            %                     SIG=reshape(SIG',1,[]);%
            %                     end
            %                 end
            %             end
            %
            %
            %     end
            
            
            
        else
            if fanout==1
                if chan1==1
                    DA1=bitget(data,1);
                    DA2=bitget(data,2);
                else if chan1==2
%                         keyboard;
                        DA1=bitget(data,3);
                        DA2=bitget(data,4);
                    else if chan1==3
                            DA1=bitget(data,5);
                            DA2=bitget(data,6);
                        else if chan1==4
                                DA1=bitget(data,7);
                                DA2=bitget(data,8);
                            else if chan1==5
                                    DA1=bitget(data,9);
                                    DA2=bitget(data,10);
                                else if chan1==6
                                        DA1=bitget(data,11);
                                        DA2=bitget(data,12);
                                    else if chan1==7
                                            DA1=bitget(data,13);
                                            DA2=bitget(data,14);
                                        else if chan1==8
                                                DA1=bitget(data,15);
                                                DA2=bitget(data,16);
                                            else if chan1==12
                                                    DA1=bitget(data,23);
                                                    DA2=bitget(data,24);
                                                else if chan1==13
                                                        DA1=bitget(data,25);
                                                        DA2=bitget(data,26);
                                                    else if chan1==14
                                                            DA1=bitget(data,27);
                                                            DA2=bitget(data,28);
                                                        end
                                                    end
                                                end
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
                sig1=DA1*2+DA2;
                SIG=table(sig1+1);
                SIG=SIG';
            end
        end
    end
end

% keyboard
datarecover_ok=1;

% fid=fopen('/home/mamaoli/result/m8b07a/chan3_10s_655364/decode.dat','wb+')
% for i=1:5000
%     fprintf(fid,'%10.5f\n',SIG(i))
% end
% keyboard