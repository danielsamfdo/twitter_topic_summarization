def fun():
 print "HI";

def fileread(s,x,y):
    f1=open(x,'w+');
    f2=open(y,'w+');
    with open(s) as fp:
        for line in fp:
            print line
            #raw_input();
            x=line.split("::");
            f1.write(x[0]+"\n");
            
            if(x[1]==' sta\n'):
                f2.write("1\n");
            elif(x[1]==' que\n'):
                f2.write("2\n");
            elif(x[1]==' sug\n'):
                f2.write("3\n");
            elif(x[1]==' com\n'):
                f2.write("4\n");
            else:
                f2.write("5\n");
    f1.close();
    f2.close();
#===================================================================#
fileread("Japan Earthquake.txt","1.txt","11.txt");

