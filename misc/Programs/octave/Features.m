function x = Features(word_indices,vocablist,bi,tri)

n =length(vocablist)+3;
max=length(vocablist)+length(bi)+length(tri);
x = zeros(n, 1);
[j k]=size(word_indices);
for i=1:k
	if(i<=n)
		x(word_indices(i))=1;
	endif
endfor
%%x(n+1)=m1;
%%x(n+2)=m2;
%%x(n+3)=m3;
end
