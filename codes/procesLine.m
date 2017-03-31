function [word_indices cntdot cntque cntexp]= procesLine(email_contents,vocabList,vocabList1,vocabList2,bi,tri)
cntdot=0;
cntque=0;
cntexp=0;
email_contents = lower(email_contents);

urlwrite ("http://text-processing.com/api/tag/", "daa.txt","post", {"text",email_contents});
urlwrite ("http://text-processing.com/api/phrases/", "daa1.txt","post", {"text",email_contents});

email_con=email_contents;
word_indices = [];
cntdot=findcntdot(email_contents);
cntque=findcntque(email_contents);
cntexp=findcntex(email_contents);
b="";
verbs=[];
fid=fopen('daa.txt','r');
pos=fgetl(fid);
while ~isempty(pos)

    % Tokenize and also get rid of any punctuation 
    [string, pos] = ...
       strtok(pos, ...
              [' ']);
       if(findstr(string,'/VB')!=0)
        verbs=[verbs substr(string,1,length(string)-4)];
        endif
endwhile
verbs
email_con=email_contents;
while(~isempty(email_con))
  found=0;
  [l email_con]=strtok(email_con,[' ']);
  for i=1:3269
    if(strcmp(l,vocabList1{i})==1)
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
email_contents = regexprep(email_contents, '&amp;', '&');
email_contents = regexprep(email_contents, '#[^\s]+', '<Hashtaginfo>');
dupcont=email_contents;

% ========================== Tokenize Email ===========================


% Output the email to screen as well
fprintf('\n==== Processed Tweet ====\n\n');
Tweet_processed=email_contents


for j=1:length(bi)
    str2=bi{j};
    if(length(findstr(email_contents,str2))!=0)
        word_indices=[word_indices length(vocabList)+j];
        printf("Bi %d\n",j );
    endif
endfor

for k=1:length(tri)
    str2=tri{k};
    if(length(findstr(email_contents,str2))!=0)
        word_indices=[word_indices length(vocabList)+j+k];
        printf("Tri %d\n",k );
    endif
endfor

l = 0;

while ~isempty(email_contents)

    % Tokenize and also get rid of any punctuation 
    [str, email_contents] = ...
       strtok(email_contents, ...
              [' ']);
    
    f=porterStemmer(str);
    
for i=1:length(vocabList)
    str2=vocabList{i};
    if(strcmp(str,str2)==1)
        word_indices=[word_indices i];
        printf("Uni %d    --\n",i );
    elseif(strcmp(f,str2)==1)
        word_indices=[word_indices i];
        printf("Uni %d\n",i );
    endif
endfor

end
word_indices
% Print footer
fprintf('\n\n=========================\n');
end