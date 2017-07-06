#### GRAPH MODULE
## TAKES IN THE ENTITIES, each node can have infinite number of edges.
# The edge will represent how many times two ENTITIES have occured together.

#for forming the graph network
import networkx as nx
#for vizualization of the graph
import matplotlib.pyplot as plt
#For loading and saving the graph
import pickle as pk
#For generating combinations between each pair of nodes
import itertools

def grapher(nodes):
    #Step 1: Load the Graph
    try:
        G = pk.load(open('data/categories/entertainmentG.p', 'rb'))
    except:
        G = nx.Graph()

    if len(nodes)>1:
        #Step 2: Add weight to each of the nodes.
        for node in nodes:
            if node in G:
                G.node[node]['relevance'] += 1
            else:
                G.add_node(node, relevance = 1)

        #Step 3: Connect the entities appearing together.
        edges = itertools.combinations(nodes,2)
        for n1, n2 in edges:
            if G.has_edge(n1, n2):
                G[n1][n2]['weight'] += 1
            else:
                G.add_edge(n1, n2, weight = 1)

    #Step 4: Save and return the graph
    pk.dump(G, open('data/categories/entertainmentG.p', 'wb'))
    return G

#nodes_list = pk.load(open('data/categories/entertainment2.p', 'rb'))
# for nodes in nodes_list:
#     G = grapher(nodes)
G = grapher([])
Gc = max(nx.connected_component_subgraphs(G), key=len)
pos=nx.shell_layout(Gc) # positions for all nodes
# nodes
nx.draw_networkx_nodes(Gc, pos, node_color='gray', node_size=[v * 50 for v in nx.get_node_attributes(Gc,'relevance').values()])
# edges
nx.draw_networkx_edges(Gc, pos, edgelist = Gc.edges(), width=1)
# nx.draw_networkx_edges(G,pos,edgelist=esmall,
#                     width=6,alpha=0.5,edge_color='b',style='dashed')
# labels
nx.draw_networkx_labels(Gc, pos, font_size=10, font_family='sans-serif')

plt.axis('off')
# plt.savefig("weighted_graph.png") # save as png
plt.show() # display

print (G.edges(data=True))
print (G.nodes(data=True))
