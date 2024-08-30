import networkx as nx
import matplotlib.pyplot as plt
import writer_reader as wr

def myPrintPDG(G):
    # Define nodes label. Now =  node_type
    node_labels = {}    
    for id in G.nodes():
        node_labels[id] = G.nodes[id]["node_type"]

    # Define edges label. Now =  type
    edge_labels = {}
    u = G.edges(data="source")
    source, target, _ = zip(*u)
    for i in range(0,len(source)):
        edge_labels[(source[i], target[i])] = G.edges.get([source[i],target[i]])["type"]

    pos = nx.spring_layout(G, seed=96531234)
    options = {"edgecolors": "tab:gray", "node_size": 100, "alpha": 0.8}
    # custom node (color, size)
    nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), node_color="tab:gray", **options)
    # custom node (node type)
    nx.draw_networkx_labels(G,pos,node_labels,font_size=7,font_color='g')
    # custom egde (alpha, color)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    # custom edge (edge type)
    nx.draw_networkx_edge_labels(G, pos,edge_labels,font_size=7)
    mng = plt.get_current_fig_manager()
    #mng.full_screen_toggle()
    mng.resize(*mng.window.maxsize())
    #plt.subplots_adjust(left=0, bottom=0, right=0, top=0, wspace=0.2, hspace=0.2)
    plt.show()



REPO = "RHEL7-STIG"
DIR = "tasks"
FILE = "main"
TASK_NODE = "4349"
G = wr.read_graphml("./output/repositories/"+REPO+"/"+DIR+"/"+FILE+"_"+TASK_NODE+".gml")

myPrintPDG(G)