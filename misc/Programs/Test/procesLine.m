function word_indices = procesLine(email_contents,vocabList,vocabList1,vocabList2)
%PROCESSEMAIL preprocesses a the body of an email and
%returns a list of word_indices 
%   word_indices = PROCESSEMAIL(email_contents) preprocesses 
%   the body of an email and returns a list of indices of the 
%   words contained in the email. 
%


email_contents = lower(email_contents);
email_con=email_contents;
word_indices = [];
cntdot=findcntdot(email_contents);
cntque=findcntque(email_contents);
cntexp=findcntex(email_contents);



end
b="";

email_con=email_contents;
while(~isempty(email_con))
  found=0;
  [l email_con]=strtok(email_con,[' ']);
  for i=1:3269
    if(strcmp(l,vocabList1(i))==1)
      b=cstrcat(b," ",vocabList2{i});
      found=1;
    endif
  endfor
  if(found==0)
    
    b=cstrcat(b," ",l);
    endif
  end
email_contents=b;

% ========================== Preprocess Email ===========================

email_contents = regexprep(email_contents, ...
                           '(http|https)://[^\s]*', '<httpaddr>');

email_contents = regexprep(email_contents, '@[^\s]+', '<dir at>');



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
%word_indices=[word_indices cntexp cntque cntdot];
word_indices
% Print footer
fprintf('\n\n=========================\n');

end
