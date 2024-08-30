import warnings
warnings.filterwarnings('ignore')

import os
import json
import pandas as pd
from rq2_base import *

def rq2_combo(repository : str, metric_type : str, best_model : str):
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
          data = pdg(data)
     elif(metric_type == "delta"):
          data = delta(data)
     elif(metric_type == "process"):
          data = process(data)
     elif(metric_type == "iac"):
          data = iac(data)
     elif(metric_type == "pdg_delta"):
          data = pdg_delta(data)
     elif(metric_type == "pdg_iac"):
          data = pdg_iac(data)
     elif(metric_type == "pdg_process"):
          data = pdg_process(data)
     elif(metric_type == "delta_iac"):
          data = delta_iac(data)
     elif(metric_type == "delta_process"):
          data = delta_process(data)
     elif(metric_type == "iac_process"):
          data = iac_process(data)
     elif(metric_type == "pdg_delta_iac"):
          data = pdg_delta_iac(data)
     elif(metric_type == "pdg_delta_process"):
          data = pdg_delta_process(data)
     elif(metric_type == "pdg_iac_process"):
          data = pdg_iac_process(data)
     elif(metric_type == "delta_iac_process"):
          data = delta_iac_process(data)
     elif(metric_type == "pdg_iac_delta_process"):
          data = pdg_iac_delta_process(data)
     else:
          raise("Error metric type not found")
     
     X, y = data.drop(['failure_prone'], axis=1), data.failure_prone

     if not(os.path.exists('rq2/metric_combination/result/'+metric_type+'/'+repository.replace("/","_"))):
          os.makedirs('rq2/metric_combination/result/'+metric_type+'/'+repository.replace("/","_"))
     classifiers = ['naive_bayes','logistic', 'svc', 'decision_tree', 'random_forest']
     
     for method in classifiers:
          print(f'Training a {method} classifier...')
          predict = train(X, y, method, metric_type=metric_type)
          
          with open('rq2/metric_combination/result/'+metric_type+'/'+repository.replace("/","_")+'/'+method+'.json', "w") as json_file:
               json.dump(predict, json_file)

     print('Done')

