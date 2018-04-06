#!/usr/bin/python3

from graph_tool.all import *
import random
import graph_tool.all as gt

g = Graph()

vlist =g.add_vertex(100)

e2 = g.add_edge(g.vertex_index[0], g.vertex_index[2])
e1 = g.add_edge(g.vertex_index[1], g.vertex_index[3])

for i in range(1000):
    g.add_edge(g.vertex_index[random.randint(1, 20)], g.vertex_index[random.randint(1, 30)])

for i in range(1000):
    g.add_edge(g.vertex_index[random.randint(50,90)], g.vertex_index[random.randint(50,90)])


# v_prop = g.new_vertex_property("string")
# v_prop[g.vertex_index[0]] = 'fooxxx'
# v_prop[g.vertex_index[1]] = 'bar'
# v_prop[g.vertex_index[2]] = 'bazxxx'

# e_prop = g.new_edge_property("double")
# e_prop[g.vertex_index[0]] = 200
# e_prop[g.vertex_index[2]] = 0.04

# e_len = g.new_edge_property("double")
# e_len[e1] = 10
# e_len[e2] = 20


pr = gt.pagerank(g)
# for i in pr:
#     print (i)
graph_draw(g,  vertex_fill_color=pr, vertex_font_size=2,vorder=pr, output_size=(800, 800), output="two-nodes.png")
