import writer_reader as wr
import networkx as nx
import matplotlib.pyplot as p
import get_file_path as fp
import dictionary_file_tasknode as df
import project_pdg_info as pi
import parse_pdg as pp
import extract_task_subgraph as es
import os

def extract_pdg_task_level_from_repo(repository : str):

    OUTPUT_DIR = os.path.normpath(os.path.join(os.getcwd(), "output", "repositories"))
    FILES_PATH = fp.getAllFilesPaths()
    REPO_DICTIONARY = pp.getRepoDictionary()

    repoPath=REPO_DICTIONARY[repository]

    ## Ottengo il PDG di una repository
    PDG = pi.getPDG(repository)

    ## Ottengo un dizionario che associa ad ogni file della repository la lista di task appartenenti a quel file
    dict_file_tasknode = df.getDict__file_tasknode(repoPath)
  
    ## Per ogni file del dizionario verifico se il file è uno dei file utilizzati nello studio di defect prediction
    if(len(dict_file_tasknode)>0):
        for file in dict_file_tasknode.keys():
            ##  file path example RHEL7-STIG/handlers/main.yml
            filePath=repository+"/"+file
            if(filePath in FILES_PATH):
            
                ## se il file è valido per lo studio recupero i nodi task del file
                taskNodeIdList = dict_file_tasknode[file]
            
                ## per ogni nodo task estraggo il sottografo a livello di task
                i=1
                for taskNodeId in taskNodeIdList:
                    SUB_PDG = es.getPDG_tasklevel(PDG,taskNodeId)
                    ## salvo il sub-pdg

                    dir_path = filePath[0:filePath.rfind("/")]

                    file_name = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
                    
                    # creo la cartella di destinazione del sub-pdg del task 
                    # la cartella di destinazione segue lo stesso path del file .yml che contiene il task
                    # la directory tree viene mantenuta uguale a quella della repository di input
                    try:
                        path = os.path.normpath(os.path.join(OUTPUT_DIR,dir_path))
                        os.makedirs(path)
                        #os.makedirs(OUTPUT_DIR+"/"+dir_path)
                    except Exception as e:
                        1==1

                    destination = os.path.normpath(os.path.join(OUTPUT_DIR,dir_path,file_name+"_"+str(taskNodeId)+".gml"))
                    #print("SAVING ---",dir_path+"\\"+file_name+"_"+str(taskNodeId)+".gml")
                    i=i+1
                    roleName = dir_path+"/"+file_name+".yml"
                    roleName = roleName.replace("\\", "/")
                    roleName = '{"path": "'+roleName+'", "id" : "'+str(taskNodeId)+'"}'
                    SUB_PDG.graph["role_name"] = roleName
                    wr.write_graphml(SUB_PDG, destination)
    else:
        print(repoPath," has't the same file of original study")
