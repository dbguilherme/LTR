#bin/bash

FOLDER="XXX" # diretorio a ser criado dentro de cada Fold
numfeatures=10 # numero de features no treino / teste
partitions=5 # numero de particoes a ser usado
binsfrom=10 # numero de bins (de) 
binsto=10 # numero de bins (at

treina_arff=$1".arff"
treina_txt=$1".txt"
test_arff=$2
flag=$4
numfeatures=$6
suffix=B$numfeatures

echo "the file have "$numfeatures;
# if [ ! -f $treina_arff ]; then
#         echo "treinamento nao foi definido";
# fi


# if [ ! -f $test_arff  ]; then
#         echo "teste nao foi definido";
# fi
# roda
# gera arquivos contendo os limites dos BINS determinados pelo TUBE
if [ $flag == "0" ]; then
    echo "Produce bins and remove training set"
  # ../.././gera_bins_TUBE.sh $treina_arff  $numfeatures $binsfrom $binsto

    rm -r result_temp_lac_train_TUBEfinal.txt/
    rm  /tmp/final_treina.txt
    rm alac_lac_train_TUBEfinal.txt*
    rm test_nohead.arff
    rm composite_train_un*
    rm saida_SSARP
   
fi
../.././gera_bins_TUBE.sh $treina_arff  $numfeatures $binsfrom $binsto
# rm alac_lac_train_TUBEfinal.txt*
#   echo "ONLY Produce bins"
rm -r result_temp_lac_train_TUBEfinal.txt/ 
rm -r result_temp_lac_train_TUBE*

rm train_nohead.arff


# remove os headers dos arquivos weka
if [ ! -f train_nohead.arff ]; then
    grep -v @ $treina_arff | grep -v ^$ > train_nohead.arff
#     grep -v @ $test_arff | grep -v ^$ > test_nohead.arff
fi 

if [ -f lac_train_TUBE$suffix.txt ]; then rm -f lac_train_TUBE$suffix.txt; fi
if [ -f lac_train_TUBE$suffix.txt ]; then rm -f lac_train_TUBEfinal.txt; fi



 # discretiza usando os bins definidos pelo TUBE; os arquivos jah sao gerados no formato LAC
echo "Discretizando treino e teste de acordo com os bins TUBE"
../../discretize_TUBE.pl train-$suffix train_nohead.arff $numfeatures lac_train_TUBE$suffix.txt
 ./updateRows.pl lac_train_TUBE$suffix.txt lac_train_TUBEfinal.txt $5
echo " roda o ALAC"
 i=1;
while [ $i -le 1 ]; do
  ../../run_alac_repeated.sh lac_train_TUBEfinal.txt $i

  cat alac_lac_train_TUBEfinal.txt | awk '{ print $1 }' |  while read instance; do  sed -i  "/^$instance /d" lac_train_TUBEfinal.txt  ;  done
 

 i=$(($i+1))
done
# junta as instancias selecionadas em cada particao em um arquivo unico contendo todas as features
# echo "Gerando o treino a partir das instancias selecionadas em cada particao.."

./scriptRemoveRows.pl alac_lac_train_TUBEfinal.txt composite_train_uniqB$6new composite_train_uniqB$6old $5
#./scriptRemoveRows.pl alac_lac_train_TUBEfinal.txt2 composite_train_uniqB$6new composite_train_uniqB$6old $5
#./scriptRemoveRows.pl alac_lac_train_TUBEfinal.txt3 composite_train_uniqB$6new composite_train_uniqB$6old $5


cat alac_lac_train_TUBEfinal.txt*  > composite_train$suffix.txt

# elimina instancias repetidas selecionadas em mais de uma particao
#cat composite_train$suffix.txt | uniq > composite_train_uniq$suffix.txt
#echo "`wc composite_train_uniq$suffix.txt | awk '{ print $1 }'` instancias distintas selecionadas"
#cat composite_train_uniq$suffix.txt > composite_train_uniqB10FINAL.txt
 #./reconstroi_arff_sementes.pl > sementes_arff

#grep -v [0-1]$  ../treina.arff > final_treina.arff
#cat sementes_arff >> final_treina.arff
#echo "treina ".$test_arff

#cat composite_train_uniqB10old > /tmp/final_treina.txt; 
cat composite_train_uniqB$6new | awk '{ print $1 }'  | while read instance; do  sed  -n  "$instance"p  $treina_txt; done >> /tmp/final_treina.txt;
echo "fim do script!!!";
