%after adding new features in the features set add n in the features and getvocablist files 


X=[];
fid = fopen('sample3.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
  while ~feof(fid),
    line = fgetl(fid);
        wordindices=procesLine(line);
        x=Features(wordindices);
        X=[X;x'];

  end
    fclose(fid);
  end
  
%Output Preprocess -For Annotated Examples


Y=[];
fid = fopen('sample3a.txt','r');
  if (fid < 0) 
  printf('Error:could not open file\n')
  else
    while ~feof(fid),
        %y=zeros(1,3);
        line = fgetl(fid)
        if(index(line,'sta')!=0)
          y=1;
        else
          y=0;
        %elseif(index(line,'que')!=0)
          %y(2)=1;
        %else
          %y(3)=1;
        endif
        
        Y=[Y;y];
    endwhile
    fclose(fid);
  endif
m=size(X,1);
size(Y,1);

[m, n] = size(X);
X = [ones(m, 1) X];

initial_theta = zeros(n + 1, 1);

[cost, grad] = costFunction(initial_theta, X, y);

%  Set options for fminunc
options = optimset('GradObj', 'on', 'MaxIter', 400);

%  Run fminunc to obtain the optimal theta
%  This function will return theta and the cost 
[theta, cost] = ...
  fminunc(@(t)(costFunction(t, X, y)), initial_theta, options);

% Print theta to screen
fprintf('Cost at theta found by fminunc: %f\n', cost);
fprintf('theta: \n');
fprintf(' %f \n', theta);

p1 = predict(theta, X)
%fprintf('Train Accuracy: %f\n', mean(double(p1 == Y)) * 100);

fprintf('\nProgram paused. Press enter to continue.\n');
