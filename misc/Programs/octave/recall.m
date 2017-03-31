%------recall------------%
function p = recall(pred,Y);
i = 0
tp = cell(4,1);
fn = cell(4,1);
tp = {0,0,0,0};
fn = {0,0,0,0};
n=length(Y)
i=1;
while (i<=n)
	x=pred{i}
	if(x == 1)
		if(x == Y{i})
			tp{1}++;
		else
			fn{1}++;
	else if(x == 2)
		if(x == Y{i})
			tp{2}++;
		else
			fn{2}++;
	else if(x == 3)
		if(x == Y{i})
			tp{3}++;
		elsef
			fn{3}++;
	else if(x == 4)
		if(x == Y{i})
			tp{4}++;
		else
			fn{4}++;
	i++;
	endif
end

recall_1 = tp{1}/(tp{1}+fn{1});
recall_2 = tp{2}/(tp{2}+fn{2});
recall_3 = tp{3}/(tp{3}+fn{3});
recall_4 = tp{4}/(tp{4}+fn{4});
printf("\n");
printf("recall vaues");
printf("%d\n%d\n%d\n%d\n",recall_1,recall_2,recall_3,recall_4);
fclose(fid);