function g = sigmoid(z)
%SIGMOID Compute sigmoid functoon
%   J = SIGMOID(z) computes the sigmoid of z.

% You need to return the following variables correctly 
%g = zeros(size(z));
%g=1/(1+exp(z));
% ====================== YOUR CODE HERE ======================
% Instructions: Compute the sigmoid of each value of z (z can be a matrix,
%               vector or scalar).

if(rows(z)==1)
	m=size((z));
	g=zeros(1,m(2));
	
	for i=1:m(2)
		g(i)=1/(1+exp(-z(i)));
	endfor
else
	x=rows(z);
	y=columns(z);
	for i=1:x
		for j=1:y
			g(i,j)=1/(1+exp(-z(i,j)));
		endfor
	endfor
endif






% =============================================================

end
