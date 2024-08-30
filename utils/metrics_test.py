import task_metrics as mt
import file_metrics as mf
import writer_reader as wr
import networkx as nx
import get_file_path as fp
import dictionary_file_tasknode as df
import project_pdg_info as pi
import parse_pdg as pp
import extract_task_subgraph as es
import json

REPO = "RHEL7-STIG"
DIR = "tasks"
FILE = "main"
TASK_NODE = "4349"
G = wr.read_graphml("./output/repositories/"+REPO+"/"+DIR+"/"+FILE+"_"+TASK_NODE+".gml", node_type=int)
dictionary = df.getDict__file_taskPDG("RHEL7-STIG")
setPDG = dictionary["tasks/main.yml"]

""" taskSize: min max line in a playbook, (max/min)/taskNumber """
""" for key in dictionary.keys():
    setPDG = dictionary[key]
    print(key)
    print(mf.taskSize(setPDG))
print("___________________________________") """
""" taskSize2: taskNode line, + o - 1,2,3  """
""" for key in dictionary.keys():
    setPDG = dictionary[key]
    print(key)
    print(mf.taskSize2(setPDG)) """


for playbook in dictionary.keys():
    setPDG = dictionary[playbook]
    print("                          TaskCount :"+playbook, mf.taskCount(setPDG))
    print("                     TaskIdentifier :"+playbook, mf.taskIdentifier(setPDG))
    print("                     maxPdgVertices :"+playbook, mf.maxPdgVertices(setPDG))
    print("                     LackOfCohesion :"+playbook, mf.lackOfCohesion(setPDG))
    print("\n")

    """ for PDG in setPDG:
        G = PDG
        print("        verticesCount", mt.verticesCount(G))
        print("           edgesCount", mt.edgesCount(G))
        print(" edgesToVerticesRatio", mt.edgesToVerticesRatio(G))
        print("          globalInput", mt.globalInput(G))
        print("         globalOutput", mt.globalOutput(G))
        print("          directFanIn", mt.directFanIn(G,dictionary))
        print("        indirectFanIn", mt.indirectFanIn(G,dictionary))
        print("         directFanOut", mt.directFanOut(G,dictionary))
        print("       indirectFanOut", mt.indirectFanOut(G,dictionary))
        print("-------------------------------------------------------") """
        

""" print("            TaskCount", mf.taskCount(setPDG))
print("             TaskSize", mf.taskSize(setPDG))
print("       TaskIdentifier", mf.taskIdentifier(setPDG))
print("         TaskCoverage", mf.taskCoverage(setPDG))
print("        verticesCount", mt.verticesCount(G))
print("           edgesCount", mt.edgesCount(G))
print(" edgesToVerticesRatio", mt.edgesToVerticesRatio(G))
print("       maxPdgVertices", mf.maxPdgVertices(setPDG))
print("          globalInput", mt.globalInput(G))
print("         globalOutput", mt.globalOutput(G))
print("          directFanIn", mt.directFanIn(G,dictionary))
print("        indirectFanIn", mt.indirectFanIn(G,dictionary))
print("         directFanOut", mt.directFanOut(G,dictionary))
print("       indirectFanOut", mt.indirectFanOut(G,dictionary))
print("       LackOfCohesion", mf.lackOfCohesion(setPDG)) """

