function word_indices = processEmail(email_contents)
%PROCESSEMAIL preprocesses a the body of an email and
%returns a list of word_indices 
%   word_indices = PROCESSEMAIL(email_contents) preprocesses 
%   the body of an email and returns a list of indices of the 
%   words contained in the email. 
%

% Load Vocabulary
vocabList = getVocabList();

% Init return value
word_indices = [];

% ========================== Preprocess Email ===========================

email_contents = lower(email_contents);



% ========================== Tokenize Email ===========================

% Output the email to screen as well
fprintf('\n==== Processed Email ====\n\n');

% Process file
l = 0;

while ~isempty(email_contents)

    % Tokenize and also get rid of any punctuation 
    [str, email_contents] = ...
       strtok(email_contents, ...
              [' ']);
   
    f=str;
    

for i=1:length(vocabList)
    str2=vocabList{i};
    if(strcmp(str,str2)==1)
        word_indices=[word_indices i];
    elseif(strcmp(f,str2)==1)
        word_indices=[word_indices i];
    endif
endfor

end
% Print footer
fprintf('\n\n=========================\n');

end
