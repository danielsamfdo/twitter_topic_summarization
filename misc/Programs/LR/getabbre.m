function [vocablist1 vocabList2] = getabbre()
 n=3269;  
 i=1;
 vocablist1= cell(n, 1);
 vocabList2= cell(n, 1);
 fid = fopen('abbreviations.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
    vocablist1{i}=lower(fscanf(fid, '%s', 1));
    % Actual Word
    vocabList2{i} =lower( fscanf(fid, '%s', 1));
    i++;
  end
  fclose(fid);
  end
