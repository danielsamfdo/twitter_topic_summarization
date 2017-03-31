%after adding new features in the features set add n in the features and getvocablist files 
% Load Vocabulary
vocabList = getVocabList();
[vocabList1 vocabList2]=getabbre();
bi=getBi();
tri=getTri();
%-----------------------------------------------------------------------------------------
X=[];
fid = fopen('tweets_text.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
        wordindices=procesLine(line,vocabList,vocabList1,vocabList2,bi,tri);
        x=Features(wordindices,vocabList,bi,tri);
        X=[X;x];
  end
    fclose(fid);
  end
%Output Preprocess -For Annotated Examples
Y=[];
fid = fopen('tweet_res.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
    while ~feof(fid),
        %y=zeros(1,3);
        line = fgetl(fid);
        y=str2double(line);
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

%  Run fminunc to obtain the optimal theta
%  This function will return theta and the cost 
%[theta, cost] = ...
%  fminunc(@(t)(costFunction(t, X, y)), initial_theta, options);

%fprintf('Train Accuracy: %f\n', mean(double(p1 == Y)) * 100);

%fprintf('\nProgram paused. Press enter to continue.\n');
num_labels=5;
lambda = 1;
[all_theta] = oneVsAll(X, Y, num_labels, lambda);

pred = predictOneVsAll(all_theta, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == Y)) * 100);

model=svmtrain(Y,X);
pp=svmpredict(Y,X,model)