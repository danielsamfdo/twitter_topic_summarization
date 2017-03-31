%-----------precision------------%
function p = precision(Y);
fid = fopen('tweet_res.txt','r');
i = 0
tp = 0
fp = 0
if (fid < 0) 
  printf('Error:could not open file\n')
  else
	while ~feof(fid),
      integer1=str2double(fgetl(fid))
    	if(integer1==Y{i})
    		tp++;
    	else
    		fp++;
    	endif
    i++;
  	end
endif
precision_value = tp/(tp+fp);
printf("\n%d",precision_value);
fclose(fid);