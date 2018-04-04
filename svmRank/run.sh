#bin/bash

c=2.5

binsto=5
k=1
#fold="/home/guilherme/Downloads/OHSUMED/QueryLevelNorm/Fold"
#fold="/home/guilherme/Downloads/MSLR-WEB10K_1/Fold"
fold="/home/guilherme/Downloads/Gov/QueryLevelNorm/2004_td_dataset/Fold"
memoria=0
c_stored=0
while [ "$(bc <<< "$c < 3")" == "1"  ]; do
    SUM=0;
    SUMMAP=0
    while [ $k -le $binsto ]; do
        ./svm_rank_learn  -c $c $fold$k/train_sort.txt model
        ./svm_rank_classify $fold$k/test_sort.txt model predictions
        perl Eval-Score-3.0.pl $fold$k/test_sort.txt predictions out 0
        echo "MAP obtido para o Fold$k $c $suffix: `cat out | grep MAP | awk '{ print $2 }'`"
        echo "NDCG obtido para o Fold$k $c $suffix: `cat out | grep NDCG `"
        k=$(($k+1))
        MAP=`cat out | grep MAP | awk '{ print $2 }'`;
        NDCG=`cat out | grep NDCG | awk '{ print $11 }'`;
        SUMMAP=`echo "scale=8; $SUMMAP+$NDCG" | bc`;
    done
    if (( $(echo "$SUMMAP > $memoria" | bc -l) )); then


        memoria=`echo "$SUMMAP" | bc`;
        c_stored=$c
        echo "memoria $memoria e c $c_stored"
    fi
echo "total $c é $SUMMAP"
c=`echo "$c*2" | bc -l`
echo "novo valor $c"
k=1
done

finalx=`echo "$memoria/5" | bc -l`
echo "fimmm memoria $finalx  c $c_stored"
