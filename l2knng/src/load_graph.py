import csv
import random
import math
import operator
import networkx as nx

import matplotlib.pyplot as plt


def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(1,len(dataset)):
	        trainingSet.append(dataset[x])

	#print(trainingSet[0][0].split(" ")[1])
	#return trainingSet

# def euclideanDistance(instance1, instance2, length):
# 	distance = 0
# 	for x in range(length):
# 		distance += pow((instance1[x] - instance2[x]), 2)
# 	return math.sqrt(distance)
#
# def getNeighbors(trainingSet, testInstance, k):
# 	distances = []
# 	length = len(testInstance)-1
# 	for x in range(len(trainingSet)):
# 		dist = euclideanDistance(testInstance, trainingSet[x], length)
# 		distances.append((trainingSet[x], dist))
# 	distances.sort(key=operator.itemgetter(1))
# 	neighbors = []
# 	for x in range(k):
# 		neighbors.append(distances[x][0])
# 	return neighbors
#
# def getResponse(neighbors):
# 	classVotes = {}
# 	for x in range(len(neighbors)):
# 		response = neighbors[x][-1]
# 		if response in classVotes:
# 			classVotes[response] += 1
# 		else:
# 			classVotes[response] = 1
# 	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
# 	return sortedVotes[0][0]
#
# def getAccuracy(testSet, predictions):
# 	correct = 0
# 	for x in range(len(testSet)):
# 		if testSet[x][-1] == predictions[x]:
# 			correct += 1
# 	return (correct/float(len(testSet))) * 100.0

def plot_graph(G):
	elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
	#esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
	pos=nx.spring_layout(G)
	nx.draw_networkx_nodes(G,pos,node_size=700)
	nx.draw_networkx_edges(G,pos,edgelist=elarge,                width=6)
	#nx.draw_networkx_edges(G,pos,edgelist=esmall, width=6,alpha=0.5,edge_color='b',style='dashed')
	nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

	plt.axis('off')
	plt.savefig("weighted_graph.png") # save as png
	#plt.show() # display



def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('/home/guilherme/Downloads/l2knng/build/neighbors.csr', split, trainingSet, testSet)

	G = nx.Graph()

	print ('Train set: ' + repr(len(trainingSet)))
	for i in range(len(trainingSet)):
		G.add_node(i)


	for i in range(len(trainingSet)):
		features=trainingSet[i][0].split(" ")
		for j in range(0,len(features),2):
			if(features[j] != ""):
				#print ((i+1) , " ", int(features[j]))
				G.add_edge(i, int(features[j]), weight=float(features[j+1]))

#	for (u, v, wt) in G.edges.data('weight'):
#		if wt > 0.5: print('(%d, %d, %.3f)' % (u, v, wt))
	#plot_graph(G)
	# pos=nx.get_node_attributes(G,'pos')
	# nx.draw_networkx_edge_labels(G, pos, font_weight='bold')
	# plt.show()
	for i in range(1000):
		print(len(sorted(G[i].items(), key=lambda edge: edge[1]['weight'])))

	#print("teste " , int(str(trainingSet[0]).split(" ")[0]))
	# print ('Test set: ' + repr(len(testSet)))
	# generate predictions
	# predictions=[]
	# k = 3
	# for x in range(len(testSet)):
	# 	neighbors = getNeighbors(trainingSet, testSet[x], k)
	# 	result = getResponse(neighbors)
	# 	predictions.append(result)
	# 	print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	# accuracy = getAccuracy(testSet, predictions)
	# print('Accuracy: ' + repr(accuracy) + '%')

main()
