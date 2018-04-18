#bin/bash

FOLDER="XXX" # diretorio a ser criado dentro de cada Fold
numfeatures=10 # numero de features no treino / teste
partitions=5 # numero de particoes a ser usado
binsfrom=10 # numero de bins (de) 
binsto=10 # numero de bins (at

treina_arff=$1".arff"
treina_txt=$1".txt"
test_arff=$2
suffix=B$4
numfeatures=$4
#sleep 100000000

echo "the file have "$numfeatures;

# gera arquivos contendo os limites dos BINS determinados pelo TUBE
if [[ $flag -le "7" ]]; then
   echo "******************************************remove training set"
   #../.././gera_bins_TUBE.sh $treina_arff  $numfeatures $binsfrom $binsto

  
    rm  /tmp/final_treina.txt
    rm  /tmp/final_treina_arff.txt
    rm alac_lac_train_TUBEfinal.txt*
    rm test_nohead.arff
    rm composite_train_un*
    rm saida_SSARP
    rm /tmp/final_treina_arff.txt
  #  echo "ONLY Produce bins"
    rm -r result_temp_lac_train_TUBEfinal.txt/ 
    rm -r result_temp_lac_train_TUBE*
    rm composite_train_uniq*
   
   #  ../.././gera_bins_TUBE.sh $treina_arff  $numfeatures $binsfrom $binsto   
fi
 rm train_nohead.arff
# rm alac_lac_train_TUBEfinal.txt*


# 
# remove os headers dos arquivos weka
if [ ! -f train_nohead.arff ]; then
     grep  @ $treina_arff  > /tmp/final_treina.arff
    grep -v @ $treina_arff | grep -v ^$ > train_nohead.arff

#     grep -v @ $test_arff | grep -v ^$ > test_nohead.arff
fi 



if [ ! -s train_nohead.arff ]; then
    echo "empty file"
    exit;
fi


x=$(cat train_nohead.arff | wc -l)

if [ $x -le 5 ]; then
    echo "file almost empty"
    exit;
fi

if [ -f lac_train_TUBE.txt ]; then rm -f lac_train_TUBE.txt; fi
if [ -f lac_train_TUBE.txt ]; then rm -f lac_train_TUBEfinal.txt; fi



 # discretiza usando os bins definidos pelo TUBE; os arquivos jah sao gerados no formato LAC
echo "Discretizando treino e teste de acordo com os bins TUBE"
 echo ../../discretize_TUBE.pl train-$suffix train_nohead.arff $numfeatures  lac_train_TUBE.txt
../../discretize_TUBE.pl train-$suffix train_nohead.arff $numfeatures  lac_train_TUBE.txt

echo  ./updateRows.pl lac_train_TUBE.txt lac_train_TUBEfinal.txt $numfeatures
 ./updateRows.pl lac_train_TUBE.txt lac_train_TUBEfinal.txt $numfeatures
echo " roda o ALAC $numfeatures"
i=1
while [[ $i -le 1 ]]; do
    echo " roda o ALAC ...."
  ../../run_alac_repeated.sh lac_train_TUBEfinal.txt $i

  cat alac_lac_train_TUBEfinal.txt* | awk '{ print $1 }' |  while read instance; do  sed -i  "/^$instance /d" lac_train_TUBEfinal.txt  ;  done
 

 i=$(($i+1))
done
# junta as instancias selecionadas em cada particao em um arquivo unico contendo todas as features
# echo "Gerando o treino a partir das instancias selecionadas em cada particao.."

./scriptRemoveRows.pl alac_lac_train_TUBEfinal.txt* composite_train_uniqB$numfeatures composite_train_uniqBold$numfeatures $numfeatures


cat alac_lac_train_TUBEfinal.txt*  > composite_train$suffix.txt

# cat alac_lac_train_TUBEfinal.txt* | while read instance; do echo "$instance"; done

#cat composite_train_uniqB$numfeatures | awk '{ print $1 }'  | while read instance; do  sed  -n  "$instance"p  $treina_txt; done >> /tmp/final_treina.txt;

cat composite_train_uniqB$numfeatures | awk '{ print $1 }'  | while read instance; do  sed  -n  "$instance"p  train_nohead.arff; done >> /tmp/final_treina.arff;
