import writer_reader as wr
import networkx as nx
import matplotlib.pyplot as p

G = wr.read_graphml("C:\\Users\\gerar\\Desktop\\scansible-result\\graphml.txt", node_type=int)

######## GET EDGE TYPE ##########
source = 5
target = 4
u = G.edges(data=True)
s, t, k = zip(*u)
print(s[9])
print(t[9])
print(k[9]["type"])


######## GET NODE TYPE ##########
print(G.nodes[1]["node_type"])

file = "handlers/main.yml"
file_name_save = file.replace("/","_")
print(file[0:file.rfind(".")])