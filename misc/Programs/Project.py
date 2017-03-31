def fun():
 print "HI";

def fileread(s):
    f1=open("2.txt",'w+');
    f2=open("21.txt",'w+');
    with open(s) as fp:
        for line in fp:
            print line
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
fileread("1.txt");

