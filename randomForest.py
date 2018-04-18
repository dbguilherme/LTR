from __future__ import print_function
import pyltr
import os
import sys

from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import subprocess
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import make_scorer
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import sklearn.externals.six



def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    #print (proc_stdout)

# input_array=np.array([1,2,3])
# new_row= np.array([4,5,6])
#
# new_array=np.vstack([input_array, new_row])
for cluster_size in range(200, 201,20):
    sets= set()
    valor=0
    store_precision=0
    store_ndcg=0
    for i in range(1,6):
        train=np.empty((0,64), float)
        label=[]
        text_file = open('/home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold'+str(i)+'/train.txt', "r")
        fileout = open("/tmp/firstRoundSelection.txt","w")
        lines = text_file.readlines()

        with open('/home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold'+str(i)+'/train.txt') as trainfile, \
                open('/home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold'+str(i)+'/vali.txt') as valifile, \
                open('/home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold'+str(i)+'/test.txt') as evalfile:
            TX, Ty, Tqids, _ = pyltr.data.letor.read_dataset(trainfile)
            VX, Vy, Vqids, _ = pyltr.data.letor.read_dataset(valifile)
            EX, Ey, Eqids, _= pyltr.data.letor.read_dataset(evalfile)
        generator=(pyltr.util.group.get_groups(Tqids))
        vez=0
        for g in generator:

            TA=TX[g[1]:g[2]]
            TB=Ty[g[1]:g[2]]

            clustering = AgglomerativeClustering(linkage='average', affinity="euclidean", n_clusters=cluster_size)
            clustering.fit(TA)

            codebook = []

            for rangevetor in range(clustering.labels_.min(), clustering.labels_.max()+1):
                 codebook.append(TA[clustering.labels_ == rangevetor].mean(0))
            #print(codebook)
            closest, _=(pairwise_distances_argmin_min(codebook, TA,metric="euclidean"))
            train = np.append(train, np.array(TA[closest]), axis=0)
            stringout=""
            #print(closest)
            for clost in (closest):
                temp=clost+g[1]
                fileout.write(lines[temp])
                #print("line ",temp, "  ",g[1], " " ,g[2])

            #print(str)
            #break;
            for c1 in closest:
                label.append (TB.item(int(c1)))
            vez+=1

        fileout.close()
        #call(["rm", " -r ./SSARP/Fold"+str(i)+"/temp1000"])
        print("rodando alac com ", len(label), " instancias no fold " + str(i) )
        try:
            subprocess_cmd("cd SSARP ;pwd; rm -r Fold"+str(i)+"/temp; ./SSARP.sh"+ " temp 64 "+str(i)+" > /tmp/sadiaSSARP")
        except :
            e = sys.exc_info()[0]
            write_to_page( "<p>Error: %s</p>" % e )

        with open('/tmp/SecondRoundSelection.txt') as trainfileFinal: TX, Ty, Tqids, _ = pyltr.data.letor.read_dataset(trainfileFinal)

        print("label len ", len(TX))
        print("rotulo len ", len(Ty), " size ", (100*len(Ty))/30000 ,"%")
#RandomForestRegressor(n_estimators=200, min_samples_split=5, random_state=1, n_jobs=-1)
        regr = RandomForestRegressor(n_estimators=300, max_features=0.3)
        #regr =RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=2, max_features='auto', max_leaf_nodes=None,    min_impurity_decrease=0.0, min_impurity_split=None,  min_samples_leaf=1, min_samples_split=2,          min_weight_fraction_leaf=0.0, n_estimators=300, n_jobs=1,    oob_score=False, random_state=0, verbose=0, warm_start=False)
        regr.fit(TX, Ty)


        print("treinando a arvore ")

        out=(regr.predict(EX))

        file_out = open("/tmp/out3","w")
        for x in out:
            file_out.write(str(x)+"\n")
        file_out.close()
        str1="perl Eval-Score-3.0.pl /home/guilherme/Downloads/Gov/QueryLevelNorm/2003_td_dataset/Fold"+str(i)+"/test.txt /tmp/out3 out 0"
        print(str1)
        subprocess.call(["sh", "-c", str1])

        inputfile = open('out')
        for line in inputfile:
            if "MAP" in line:
                precision=line.split("	")
            if "NDCG" in line:
                ndcg=line.split("	")

        print("map " , precision[1])
        print("ndcg " , ndcg[10])
        store_precision+=float(precision[1])
        store_ndcg+=float(ndcg[10])

    print (sets)
    print("final ndcg" , store_ndcg/5)
    print("final map" , store_precision/5)
   # ndcg_scorer = make_scorer(ndcg_score, needs_proba=True, k=5)
    #print(svc_param_selection(VX,Vy,5))

    #tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     #'C': [1, 10, 100, 1000]},
                    #{'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    #scores = ['precision']

    #for score in scores:
        #print("# Tuning hyper-parameters for %s" % score)
        #print()

        #clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,  scoring='precision')
        #clf.fit(X_train, y_train)

        #print("Best parameters set found on development set:")
        #print()
        #print(clf.best_params_)
        #print()
        #print("Grid scores on development set:")
        #print()
        #for params, mean_score, scores in clf.grid_scores_:
            #print("%0.3f (+/-%0.03f) for %r"  % (mean_score, scores.std() * 2, params))
        #print()

        #print("Detailed classification report:")
        #print()
        #print("The model is trained on the full development set.")
        #print("The scores are computed on the full evaluation set.")
        #print()
        #y_true, y_pred = y_test, clf.predict(X_test)
        #print(classification_report(y_true, y_pred))
        #print()
    #metric = pyltr.metrics.NDCG(k=10)

    ## Only needed if you want to perform validation (early stopping & trimming)
    #monitor = pyltr.models.monitors.ValidationMonitor(
        #VX, Vy, Vqids, metric=metric, stop_after=500)

    #model = pyltr.models.LambdaMART(
        #metric=metric,
        #n_estimators=1000,
        #learning_rate=0.02,
        #max_features=0.5,
        #query_subsample=0.5,
        #max_leaf_nodes=10,
        #min_samples_leaf=64,
        #verbose=1,
    #)

    #model.fit(TX, Ty, Tqids, monitor=monitor)


    #Epred = model.predict(EX)
    #print ('Random ranking:', metric.calc_mean_random(Eqids, Ey))
    #print ('Our model:', metric.calc_mean(Eqids, Ey, Epred))
    #valor+=metric.calc_mean(Eqids, Ey, Epred)

#print("media final ", valor/5)
