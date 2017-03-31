function recall_1 = recall(pred,Y)

n=length(Y);
tp=fn=0
printf("%d",1);
i=1;
r=1;
while(r<=4),
while(i<=n),
	x=pred(i)
	if(Y(i)==x)
		tp+=1;
	else if(Y(i)==r && x!=r)
		fn+=1;
	endif
	i+=1;
end
printf("recall")
if(tp+fn>0)
	tp/(tp+fn)
else
	printf("0\n")
endif
r++
end

i=1;
r=1;
tp=fp=0
while(r<=4),
while(i<=n),
	x=pred(i);
	if(Y(i)==x)
		tp++;
	else if(Y(i)!=r && x==r)
		fp++;
	endif
	i++
end
printf("PRECISION")
tp/(tp+fp)
r++
end
end
recall_1=0