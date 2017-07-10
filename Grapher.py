import networkx as nx
#for vizualization of the graph
import matplotlib.pyplot as plt
#For loading and saving the graph
import pickle as pk
#For generating combinations between each pair of nodes
import itertools

def grapher(G, nodes):
    """
    INPUT: List of nodes [a, b, c, d], Location of Grapher Pickle file
    OUTPUT: networkx Graph
    DEPENDENCY: itertools (for combinations), pickle
    """
    #Step 1: Load the Graph
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
    #Step 4: return the graph
    return G

def plotter(G):
    """
    INPUT: Graph (networkx)
    PROCESS: Gets the layout
             Gets the nodes
             Draws edges, labels nodes
    OUTPUT: matplotlib plot
    DEPENDENCY: matplotlib.pyplot
    """
    pos=nx.spring_layout(G) # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G, pos, node_color='gray', \
    node_size=[v * 50 for v in nx.get_node_attributes(G,'relevance').values()])
    # edges
    nx.draw_networkx_edges(G, pos, edgelist = G.edges(), width=1)
    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.axis('off')
    # plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

def category_grapher(fileloc, output):
    """
    INPUT : Pickle file of the form list of lists (fileloc), Output Location
    DEPENDENCY: grapher method
    OUTPUT: Graph (netwokx), PICKLE file of Graph type
    """
    try:
        G = pk.load(open(output, 'rb'))
    except:
        G = nx.Graph()
        nodes_list = pk.load(open(fileloc, 'rb'))
        for nodes in nodes_list:
            G = grapher(G, nodes)
        G = graph_filter(G)
        pk.dump(G, open(output, 'wb'))
    return G

def graph_filter(G):
    """
    INPUT: Graph (networkx)
    PROCESS: Deletes the edges with <= 1 weight,
             Gets the Largest connected component
    OUTPUT: Graph (networkx)
    """
    weight_dict = nx.get_edge_attributes(G, 'weight')
    {G.remove_edge(*k) for (k,v) in weight_dict.items() if v <= 1}
    Gc = max(nx.connected_component_subgraphs(G), key=len)
    return Gc

def graph_printer(G, databool = False):
    """
    Prints the edges and nodes of networkx Graph
    """
    print (G.edges(data=databool))
    print (G.nodes(data=databool))
