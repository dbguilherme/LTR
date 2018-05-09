#bin/bash
i=1
while [ $i -le 50 ]; do
   cat selectedset.txt | grep "qid:"$i" " > "/tmp/features$i"Fold"$1"
    
    #if [[ "$number1" -eq "$number2" ]] 
    #c="$(($teste + 1))"
    
    teste=`wc  /tmp/features$i"Fold"$1 | awk '{ print $1 }'`
    
    if [[ $teste -eq "0" ]]; then
             echo "$teste---- $i--- $c"
             rm "/tmp/features$i"Fold"$1"
    fi
    i=$(($i+1))
#     
done
