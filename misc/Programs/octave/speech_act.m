%after adding new features in the features set add n in the features and getvocablist files 

% Load Vocabulary
vocabList = getVocabList();
[vocabList1 vocabList2]=getabbre();
bi=getBi();
tri=getTri();
cntdot=0;
cntque=0;
cntexp=0;
%-----------------------------------------------------------------------------------------

X=[];
fid = fopen('1.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
        [wordindices cntdot cntque cntexp]=procesLine(line,vocabList,vocabList1,vocabList2,bi,tri);
        x=Features(wordindices,vocabList,bi,tri,cntdot,cntque,cntexp);
        x
        X=[X;x'];

  end
    fclose(fid);
  end
  
%Output Preprocess -For Annotated Examples


Y=[];
fid = fopen('11.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
        
    while ~feof(fid),
        %y=zeros(1,3);
        line = fgetl(fid);
        y=str2double(line(length(line)));
        Y=[Y;y];


    endwhile
    fclose(fid);
  endif
m=size(X,1);
size(Y,1);

[m, n] = size(X);
X = [ones(m, 1) X];

initial_theta = zeros(n + 1, 1);

[cost, grad] = costFunction(initial_theta, X, Y);

%  Set options for fminunc
options = optimset('GradObj', 'on', 'MaxIter', 400);
num_labels=5;
lambda = 1;
[all_theta] = oneVsAll(X, Y, num_labels, lambda);

pred = predictOneVsAll(all_theta, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == Y)) * 100);

model=svmtrain(Y,X);
pp=svmpredict(Y,X,model);