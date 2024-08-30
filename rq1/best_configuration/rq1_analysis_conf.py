import warnings
warnings.filterwarnings('ignore')

import os
import json
import pandas as pd
from rq1_base_conf import train, pdg_metrics_only, delta_metrics_only, process_metrics_only, iac_metrics_only

def rq1_conf(repository : str, metric_type : str, bal : int, pre : int):
    data = pd.read_csv('kaggle/input/iac-defect-prediction-using-pdg-metrics/ansible.csv')
    data = data[data.repository == repository].fillna(0)

    # Remove releases with only failure_prone equal 0 or 1
    for commit in data.commit.unique():
        tmp = data[data.commit == commit]
        if tmp.failure_prone.to_list().count(0) == 0 or tmp.failure_prone.to_list().count(1) == 0:
            indices = data[data.commit == commit].index
            data.drop(indices, inplace=True)

    # Create column to group files belonging to the same release (identified by the commit hash)
    data['group'] = data.commit.astype('category').cat.rename_categories(range(1, data.commit.nunique()+1))

    # Sort data from the oldest to the newest release
    data.sort_values(by=['committed_at'], ascending=True)
    data = data.reset_index(drop=True)

    # Remove metadata columns but not 'group'
    data = data.drop(['commit', 'committed_at', 'filepath', 'repository'], axis=1)

    # metrics selection
    if(metric_type == "pdg"):
         data = pdg_metrics_only(data)
    elif(metric_type == "delta"):
         data = delta_metrics_only(data)
    elif(metric_type == "process"):
        data = process_metrics_only(data)
    elif(metric_type == "iac"):
         data = iac_metrics_only(data)
    else:
         raise("Error metric type not found")
    
    X, y = data.drop(['failure_prone'], axis=1), data.failure_prone

    if not(os.path.exists('rq1/best_configuration/result/result_'+str(bal)+'_'+str(pre)+'/'+metric_type+'/'+repository.replace("/","_"))):
            os.makedirs('rq1/best_configuration/result/result_'+str(bal)+'_'+str(pre)+'/'+metric_type+'/'+repository.replace("/","_"))

    for method in ['naive_bayes','logistic', 'svc', 'decision_tree', 'random_forest']:
        print(f'Training a {method} classifier...')
        predict = train(X, y, method, metric_type=metric_type, bal=bal, pre=pre)
        
        with open('rq1/best_configuration/result/result_'+str(bal)+'_'+str(pre)+'/'+metric_type+'/'+repository.replace("/","_")+'/'+method+'.json', "w") as json_file:
            json.dump(predict, json_file)

    print('Done')

