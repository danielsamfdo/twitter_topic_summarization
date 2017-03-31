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
save pred.txt pred
fprintf('\nLogistic Regression Training Set Accuracy: %f\n', mean(double(pred == Y)) * 100);
save C:/Python27/Proj/Final/Y.txt Y;
model=svmtrain(Y,X);
pp=svmpredict(Y,X,model);
save pp.txt pp
fprintf('\n SVM Training Set Accuracy: %f\n', mean(double(pp == Y)) * 100);

X1=[];
fid = fopen('tweetsTEXT1.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
        [wordindices cntdot cntque cntexp]=procesLine(line,vocabList,vocabList1,vocabList2,bi,tri);
        x=Features(wordindices,vocabList,bi,tri,cntdot,cntque,cntexp);
        x
        X1=[X1;x'];

  end
    fclose(fid);
  end
[m, n] = size(X1);
X1 = [ones(m, 1) X1];
Y1=[];
fid = fopen('tweet_res.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
        
    while ~feof(fid),
        %y=zeros(1,3);
        line = fgetl(fid);
        y=str2double(line(length(line)));
        Y1=[Y1;y];


    endwhile
    fclose(fid);
  endif

  pred1 = predictOneVsAll(all_theta, X1);
  fprintf('\nLogistic Regression Test Set Accuracy: %f\n', mean(double(pred1 == Y1)) * 100);

  save pred1.txt pred1

pp1=svmpredict(Y1,X1,model);
save pp1.txt pp1
fprintf('\n SVM Training Set Accuracy: %f\n', mean(double(pp1 == Y1)) * 100);