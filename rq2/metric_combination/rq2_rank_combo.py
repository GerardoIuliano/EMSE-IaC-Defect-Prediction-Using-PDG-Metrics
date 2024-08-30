import os, csv
import pandas as pd
import scipy.stats as ss

def rank_project_metrics(project: str):
    # Read the data from CSV
    data = pd.read_csv(os.path.normpath(os.path.join("rq2", "metric_combination", "analysis", "models_analysis.csv")))
    
    # Filter data for random_forest classifier and the specific project
    data = data[data["classifier"] == "random_forest"]
    project_row = data[data["repository"] == project]
    
    # Extract MCC values for each metric
    mcc_dict = {
        "pdg": project_row[project_row["metric"] == "pdg"]["mcc"].values[0],
        "iac": project_row[project_row["metric"] == "iac"]["mcc"].values[0],
        "delta": project_row[project_row["metric"] == "delta"]["mcc"].values[0],
        "process": project_row[project_row["metric"] == "process"]["mcc"].values[0],
        "pdg_delta": project_row[project_row["metric"] == "pdg_delta"]["mcc"].values[0],
        "pdg_iac": project_row[project_row["metric"] == "pdg_iac"]["mcc"].values[0],
        "pdg_process": project_row[project_row["metric"] == "pdg_process"]["mcc"].values[0],
        "delta_iac": project_row[project_row["metric"] == "delta_iac"]["mcc"].values[0],
        "delta_process": project_row[project_row["metric"] == "delta_process"]["mcc"].values[0],
        "iac_process": project_row[project_row["metric"] == "iac_process"]["mcc"].values[0],
        "pdg_delta_iac": project_row[project_row["metric"] == "pdg_delta_iac"]["mcc"].values[0],
        "pdg_delta_process": project_row[project_row["metric"] == "pdg_delta_process"]["mcc"].values[0],
        "pdg_iac_process": project_row[project_row["metric"] == "pdg_iac_process"]["mcc"].values[0],
        "delta_iac_process": project_row[project_row["metric"] == "delta_iac_process"]["mcc"].values[0],
        "pdg_iac_delta_process": project_row[project_row["metric"] == "pdg_iac_delta_process"]["mcc"].values[0]
    }

    # Compute ranks in descending order (higher MCC gets a lower rank number)
    ranked_list = ss.rankdata([-v for v in mcc_dict.values()], method="average")
    
    # Convert ranked list to dictionary with metric names
    metrics = list(mcc_dict.keys())
    my_dict = {metrics[i]: ranked_list[i] for i in range(len(ranked_list))}
    
    return my_dict

        

def ranked_table():
    data = pd.read_csv(os.path.normpath(os.path.join("rq2", "metric_combination", "analysis", "models_analysis.csv")))
    data = data[data["classifier"]=="random_forest"]

    projects = data["repository"]
    projects = list(dict.fromkeys(projects))
    rows = []
    for project in projects:
        rank = rank_project_metrics(project=project)
        rows.append([project,"pdg",rank["pdg"]])
        rows.append([project,"delta", rank["delta"]])
        rows.append([project,"iac", rank["iac"],])
        rows.append([project, "process", rank["process"]])
        rows.append([project,"pdg_delta",rank["pdg_delta"]])
        rows.append([project,"pdg_iac",rank["pdg_iac"]])
        rows.append([project,"pdg_process",rank["pdg_process"]])
        rows.append([project,"delta_iac",rank["delta_iac"],])
        rows.append([project,"delta_process",rank["delta_process"]])
        rows.append([project,"iac_process",rank["iac_process"]])
        rows.append([project,"pdg_delta_iac",rank["pdg_delta_iac"]])
        rows.append([project,"pdg_delta_process",rank["pdg_delta_process"]])
        rows.append([project,"pdg_iac_process",rank["pdg_iac_process"]])
        rows.append([project,"delta_iac_process",rank["delta_iac_process"]])
        rows.append([project,"pdg_iac_delta_process",rank["pdg_iac_delta_process"]])
        
    with open("rq2/metric_combination/statistic/"+"nemenyi_rank.csv", mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(["repository", "metric", "rank"])
        writer.writerows(rows)

ranked_table()

