import pandas as pd
import os, csv
import scipy.stats as ss
from critdd import Diagram

def rank_project_classifiers(project : str):
    data = pd.read_csv(os.path.normpath(os.path.join("rq1", "best_model", "analysis", "analysis_0_1", "repoAndClassifiers.csv")))

    project_row = data[data["repository"]==project]
    mcc_dict ={
        "naive_bayes" : project_row["naive_bayes"].values[0],
        "logistic" : project_row["logistic"].values[0],
        "svc" : project_row["svc"].values[0],
        "decision_tree" : project_row["decision_tree"].values[0],
        "random_forest" : project_row["random_forest"].values[0]
    }   
    sorted_dict = {k: v for k, v in sorted(mcc_dict.items(), key=lambda item: item[1], reverse=True)}
    ranked_list = ss.rankdata(list(sorted_dict.values()), method="average")
    ranked_list = list(ranked_list)
    metrics = list(sorted_dict.keys())
    rows=[]

    my_dict = {metrics[i]: 6-ranked_list[i] for i in range(len(ranked_list))}
    return my_dict

def ranked_table():
    data = pd.read_csv(os.path.normpath(os.path.join("rq1", "best_model", "analysis", "analysis_0_1", "analysis.csv")))
    data = data[data['metric']=="pdg"]
    projects = data["repository"]
    projects = list(dict.fromkeys(projects))
    rows = []
    avg_nb = 0
    avg_lr = 0
    avg_svc = 0
    avg_dt = 0
    avg_rf = 0
    for project in projects:
        rank = rank_project_classifiers(project=project)
        rows.append([project,"naive_bayes",rank["naive_bayes"]])
        rows.append([project,"logistic", rank["logistic"]])
        rows.append([project,"svc", rank["svc"],])
        rows.append([project, "decision_tree", rank["decision_tree"]])
        rows.append([project,"random_forest",rank["random_forest"]])
        avg_nb+=rank["naive_bayes"]
        avg_lr+=rank["logistic"]
        avg_svc+=rank["svc"]
        avg_dt+=rank["decision_tree"]
        avg_rf+=rank["random_forest"]
    print(avg_nb/80)    
    print(avg_lr/80)
    print(avg_svc/80)
    print(avg_dt/80)
    print(avg_rf/80)
    with open("rq1/best_model/statistic/statistic_0_1/"+"nemenyi_rank2.csv", mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(["repository", "classifier", "rank"])
        writer.writerows(rows)


ranked_table()




