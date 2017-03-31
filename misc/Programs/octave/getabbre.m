function [vocabList1 vocabList2] = getabbre();
 n=3269; 
 i=1;
 vocabList1= cell(n);
 vocabList2= cell(n);
 fid = fopen('accr.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    vocabList1{i} =fgetl(fid);
    i++;
  end
  endif
fclose(fid);
i=1;
fid = fopen('abbr.txt','r');
if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    vocabList2{i} =fgetl(fid);
    i++;
  end
  endif
fclose(fid);
