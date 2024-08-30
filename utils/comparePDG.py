import writer_reader as wr

task_node_id = 4371
G = wr.read_graphml("C:\\Users\\gerar\\Desktop\\scansible-result\\"+str(task_node_id)+"alg_2.gml")
G1 = wr.read_graphml("C:\\Users\\gerar\\Desktop\\scansible-result\\"+str(task_node_id)+"alg_3.gml")

print("G")
print(G.nodes)
print(G.edges)
print("G1")
print(G1.nodes)
print(G1.edges)
print(G.nodes==G1.nodes)
print(G.edges==G1.edges)