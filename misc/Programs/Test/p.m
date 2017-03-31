%after adding new features in the features set add n in the features and getvocablist files 

% Load Vocabulary
vocabList = getVocabList();
[vocabList1 vocabList2]=getabbre();
%-----------------------------------------------------------------------------------------

X=[];
fid = fopen('1.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
        wordindices=procesLine(line,vocabList,vocabList1,vocabList2);
        x=Features(wordindices);
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
        y=line;
        %if(index(line,'sta')!=0)
          %y=1;
        %elseif(index(line,'que')!=0)
          %y=2;
        %elseif(index(line,'sug')!=0)
          %y=3;
        %elseif(index(line,'com')!=0)
          %y=4;
        %else
          %y=5;
        %endif
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

% Print theta to screen
%fprintf('Cost at theta found by fminunc: %f\n', cost);
%fprintf('theta: \n');
%fprintf(' %f \n', theta);
%p1=predict(theta,X)


%fprintf('Train Accuracy: %f\n', mean(double(p1 == Y)) * 100);

%fprintf('\nProgram paused. Press enter to continue.\n');
num_labels=5;
lambda = 1;
[all_theta] = oneVsAll(X, Y, num_labels, lambda);

pred = predictOneVsAll(all_theta, X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == Y)) * 100);

model=svmtrain(Y,X);
pp=svmpredict(Y,X,model)