function vocabList = getBi()
%GETVOCABLIST reads the fixed vocabulary list in vocab.txt and returns a
%cell array of the words
%   vocabList = GETVOCABLIST() reads the fixed vocabulary list in vocab.txt 
%   and returns a cell array of the words in vocabList.


%% Read the fixed vocabulary list
fid = fopen('bigrams.txt');

% Store all dictionary words in cell array vocab{}
n = 50;  % Total number of words in the dictionary

% For ease of implementation, we use a struct to map the strings => integers
% In practice, you'll want to use some form of hashmap
vocabList = cell(n, 1);
for i = 1:n
    % Word Index (can ignore since it will be = i)
    fscanf(fid, '%d', 1);
    % Actual Word
    x = fscanf(fid, '%s', 1);
    y =fscanf(fid, '%s', 1);
    
    vocabList{i}=cstrcat(x," ",y);  
end

fclose(fid);

end
