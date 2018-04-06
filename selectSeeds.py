import os



for x in range(1,6):
    print ("fold ", x , "\n")
    fold="/home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold"+str(x)+"/train_sort.txt"
    l2_out="/tmp/leknng_saida"+str(x)
    reader = (open(l2_out))
    temp=0
    #str="rm /tmp/saida_processada"
    #
    out_file="/tmp/saida_processada"+str(x)
    os.system("rm "+ out_file)


    with open(l2_out, 'r') as f:
        contents=f.read()
        lines=contents.split("\n")

        #splitted=lines[0].split(" ")
        tempStr="sed '%sq;d' %s >> %s"% ("1",fold,out_file)
        os.system(tempStr)
        setId = set()
        for i in range(1,len(lines)-1):

            l2neigbor=lines[i].split(" ")
            if (l2neigbor[58] in setId):
                continue
            temp=0
            while(temp< 10):
                if (l2neigbor[58] in setId):
                    #print("ja adicionado o ",l2neigbor[58])
                    l2neigbor=lines[int(l2neigbor[58])].split(" ")
                    temp+=1
                    continue;
                setId.add(l2neigbor[58])
                tempStr="sed '%sq;d' %s >> %s"% (l2neigbor[58],fold,out_file)
                os.system(tempStr)
                #print(l2neigbor[58]) #dobro -2
                l2neigbor=lines[int(l2neigbor[58])].split(" ")

    #    splitted=lines[0].split(" ")
    #    if (splitted[0] in setId):
        #             continue;

    # for line in reader:
    #     temp+=1
    #     if temp==1:
    #         continue;
    #     if temp ==2:
    #         splitted=line.split(" ")
    #         if (splitted[0] in setId):
    #             continue;
    #
    #         setId.add(splitted[0])
    #         tempStr="sed '%sq;d' %s >> %s"% (splitted[0],fold,out_file)
    #         #tempStr="awk 'NR == %i' %s > %s"% (int(splitted[0]),fold,out_file)
    #         #cmd = 'svm_rank/svm_rank_learn %s %s %s > /tmp/saida_processada' % (args, tr_filename, model_filename)
    #         os.system(tempStr)
    #         # if( temp>5000):
    #         #      break;
    #     else:
    #
    strSort="sort -n -t: -k2  %s > %s" % (out_file, "/tmp/training_file_sort"+str(x)+".txt")
    os.system(strSort)
