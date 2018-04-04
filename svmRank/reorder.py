
import csv
from operator import itemgetter
import subprocess

#reader = csv.reader(open("/tm"), delimiter=" ")



for i in range(1,6):
    reader = (open("/home/guilherme/Downloads/Gov/QueryLevelNorm/2004_td_dataset/Fold"+str(i)+"/train.txt"))
    F = open("/home/guilherme/Downloads/Gov/QueryLevelNorm/2004_td_dataset/Fold"+str(i)+"/train_reorder.txt","w")
    for line in reader:

        split=line.split("WT04-")
        #print(split[0]+str(split[1]))
        F.write(split[0]+str(split[1]))
        #break;
    F.close()

    str1="sort -n -t: -k2 /home/guilherme/Downloads/Gov/QueryLevelNorm/2004_td_dataset/Fold"+str(i)+"/train_reorder.txt > /home/guilherme/Downloads/Gov/QueryLevelNorm/2004_td_dataset/Fold"+str(i)+"/train_sort.txt"

    subprocess.call(["sh", "-c", str1])
