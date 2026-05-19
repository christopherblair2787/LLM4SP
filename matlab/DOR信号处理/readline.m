function [str,value]=readline(tline)
%READLINE returns the string before '=';
%   str(string variable) contains the key string;
%   value(string variable) contains the value of the key string.
%2004,4,24

i=findstr(tline,'=');
str=[' '];value=[' '];
if ( ~isempty(i) & (tline(1)~='%'))
    str=tline(1:i(1)-1);
    j=findstr(tline,' ');
    k=findstr(tline,';');
    value=tline(j(1)+1:k(1)-1);
end
