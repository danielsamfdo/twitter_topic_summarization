function m = emoticontr()
%GETVOCABLIST reads the fixed vocabulary list in vocab.txt and returns a
%cell array of the words
%   vocabList = GETVOCABLIST() reads the fixed vocabulary list in vocab.txt 
%   and returns a cell array of the words in vocabList.
M=[];

%% Read the fixed vocabulary list
fid = fopen('emoticon1.txt');
while ~feof(fid)
    x = fscanf(fid, '%s', 1);
	M.append(x);
    y =fscanf(fid, '%s', 1);
    
    vocabList{i}=cstrcat(x," ",y);  
end

fclose(fid);
f=fopen('emot.txt','w+')
save emot.txt M

end
