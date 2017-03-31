function x = findcntdot(y)
x=0;
for i=1:length(y)
	if(y(i)=='.')
		x++;
	endif
endfor
if(x>1)
	x=2;
endif

end
