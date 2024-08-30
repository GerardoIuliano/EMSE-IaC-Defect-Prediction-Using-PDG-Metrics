import numpy as np
import pandas as pd

from sklearn import ensemble, linear_model, naive_bayes, svm, tree
from sklearn.feature_selection import VarianceThreshold, SelectFromModel
from sklearn import metrics
from sklearn import model_selection
from sklearn import preprocessing
from sklearn import feature_selection 

from sklearn.utils import indexable
from sklearn.utils.validation import _num_samples

from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import KFold

import traceback

#====================================================== Hyper-parameters ======================================================#
#                                                                                                                              #
# This section contains the possible values for models' hyper-parameters                                                       #
#                                                                                                                              #
#==============================================================================================================================#

decision_tree_params = dict(
    clf__criterion = ['gini', 'entropy'],
    clf__splitter = ['best', 'random'],
    clf__max_features = ['auto', 'sqrt', 'log2', None],
    clf__class_weight = ['balanced', None]
)


naive_params = dict(clf__var_smoothing = np.logspace(start = -10, stop = -8, num = 10))

logistic_params = dict(
    clf__penalty = ['l2', 'none'],
    clf__tol = np.logspace(-5,-3,10),
    clf__C = np.linspace(0,2,10),
    clf__class_weight = [None, 'balanced'],
    clf__solver = ['lbfgs', 'sag', 'saga'],
    clf__fit_intercept = [False, True] 
)

max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)

random_forest_params = dict(
    clf__n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 10)],
    clf__max_features = ['auto', 'sqrt'],
    clf__max_depth = max_depth,
    clf__bootstrap = [True, False]
)

svc_params = dict(
    clf__C = [int(x) for x in np.linspace(start = 1, stop = 1000, num = 100)],
    clf__gamma = ['scale', 'auto'], 
    clf__kernel = ['rbf', 'sigmoid', 'poly'],
    clf__degree = [1, 2, 3, 4, 5],
    clf__shrinking = [False, True],
    clf__tol = [x for x in np.logspace(start = -5, stop = -1, num = 10)],
    clf__class_weight = [None, 'balanced']
)

search_params = dict(
    decision_tree = decision_tree_params,
    naive_bayes = naive_params,
    logistic = logistic_params,
    random_forest = random_forest_params,
    svc = svc_params 
)

estimators = dict(
    decision_tree = tree.DecisionTreeClassifier(),
    naive_bayes = naive_bayes.GaussianNB(),
    logistic = linear_model.LogisticRegression(),
    random_forest = ensemble.RandomForestClassifier(),
    svc = svm.SVC(probability=True)
)

estimators_rfe = dict(
    decision_tree = tree.DecisionTreeClassifier(),
    naive_bayes = ensemble.RandomForestClassifier(), #l'algoritmo naive_bayes non contiene la feature importance, quindi non è applicabile RFE 
    logistic = linear_model.LogisticRegression(),
    random_forest = ensemble.RandomForestClassifier(),
    svc = svm.SVC(kernel='linear')
)


features_to_select = dict(
    delta = 10, # calcolate tramite RFECV
    process = 6,# calcolate tramite RFECV
    iac = 16,   # calcolate tramite RFECV
    pdg = 4,    # calcolate tramite RFECV
    pdg_delta = 14,
    pdg_iac = 20,
    pdg_process = 10,
    delta_iac = 26,
    delta_process = 16,
    iac_process = 22,
    pdg_delta_iac = 30,
    pdg_delta_process = 20,
    pdg_iac_process = 26,
    delta_iac_process = 32,
    pdg_iac_delta_process = 36
)



#====================================================== Hyper-parameters ======================================================#
#                                                                                                                              #
# This section contains the releasae-based walk-forward validation procedure                                                   #
#                                                                                                                              #
#==============================================================================================================================#
def walk_forward(X, y, groups):
    """
    Generate train and test splits fro TimeSeriesSplit on releases.
    Train consists of a release or a list of successive releases, and
    the test set consist of the next release in time

    groups : array-like of shape (n_samples,)
        Group labels for the samples used while splitting the dataset into
        train/test set.
        Must be an ordered list of integer, i.e., [1, 1, 1, 2, 2, 3, 4, 4, etc.].
        Each integer denote a given release. Files within the same release have the same 
        group id.
    """

    X, y, groups = indexable(X, y, groups)
    n_samples = _num_samples(X)
    n_folds = len(set(groups)) # Number of distinct groups (releases)
    if n_folds > n_samples:
        raise ValueError(
            ("Cannot have number of folds ={0} greater"
                " than the number of samples: {1}.").format(n_folds, n_samples))
    
    indices = np.arange(n_samples)
    offset = 0

    for _ in range(0, n_folds - 1):
        train_indices = [i for i, x in enumerate(groups) if x == groups[offset]]
        offset += len(train_indices)
        test_indices = [i for i, x in enumerate(groups) if x == groups[offset]]

        yield (indices[:offset], indices[offset: offset+len(test_indices)])
 


#====================================================== Hyper-parameters ======================================================#
#                                                                                                                              #
# This section contains the training procedure                                                                                 #
#                                                                                                                              #
#==============================================================================================================================#
scoring = dict(
    roc_auc = 'roc_auc',
    pr_auc = 'average_precision',
    accuracy = 'accuracy',
    balanced_accuracy = 'balanced_accuracy',
    precision = 'precision',
    recall = 'recall',
    f1 = 'f1',
    mcc = metrics.make_scorer(metrics.matthews_corrcoef)
)

def train(X, y, method: str, metric_type : int):
    
    if method not in ('decision_tree', 'naive_bayes', 'logistic', 'random_forest', 'svc'):
        raise ValueError('Method not supported')
    
    _search_params = search_params[method]
    _search_params['bal'] = [None, RandomUnderSampler(sampling_strategy='majority', random_state=42), RandomOverSampler(sampling_strategy='minority', random_state=42)]
    _search_params['pre'] = [None, preprocessing.MinMaxScaler(), preprocessing.StandardScaler()]
    
    groups = X['group']
    X = X.drop(['group'], axis=1)

    # Remove constant features
    try:
        selected_features_indices = VarianceThreshold(threshold=0).fit(X).get_support(indices=True)
        X = X.iloc[:, selected_features_indices]
    except Exception as e:
        traceback.print_exc()

    pipe = Pipeline([
        ('bal', _search_params["bal"][0]), # To balance the training data See search_params['bal']
        ('pre', _search_params["pre"][1]), # To scale (and center) data. See search_params['pre']
        ('rfe', feature_selection.RFE(estimator=estimators_rfe[method], n_features_to_select=features_to_select[metric_type])), 
        ('clf', estimators[method])
    ])

    json = {}
    split = 0
    for train_indices, test_indices in walk_forward(X, y, groups):
        
        X_train, y_train = X.iloc[train_indices], y.iloc[train_indices]
        pipe.fit(X_train, y_train)

        X_test, y_test = X.iloc[test_indices], y.iloc[test_indices]
        y_pred = pipe.predict(X_test)
        predicted_probabilities = pipe.predict_proba(X_test)[:, 1]
        notXOR = (y_pred == y_test).astype(int)

        json["split"+str(split)+"_index"]=test_indices.tolist()
        json["split"+str(split)+"_pred"]=y_pred.tolist()
        json["split"+str(split)+"_test"]=y_test.values.tolist()
        json["split"+str(split)+"_notXOR"]=notXOR.values.tolist()
        json["split"+str(split)+"_prob"]=predicted_probabilities.tolist()

        split+=1

    return json

                                                                                                               
def pdg(df):
    return df[['failure_prone', 'group','maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut']]

def iac(df):
    return df[['failure_prone', 'group','avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy']]

def delta(df):
    return df[['failure_prone', 'group','delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy']]

def process(df):
    return df[['failure_prone', 'group','change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]
                                                                                                  
def pdg_delta(df):
    return df[['failure_prone', 'group', 
               
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy']]

def pdg_iac(df):
    return df[['failure_prone', 'group', 
               
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy']]

def pdg_process(df):
    return df[['failure_prone', 'group', 
               
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def delta_iac(df):
    return df[['failure_prone', 'group', 
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy']]

def delta_process(df):
    return df[['failure_prone', 'group', 
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def iac_process(df):
    return df[['failure_prone', 'group', 
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def pdg_delta_iac(df):
    return df[['failure_prone', 'group', 
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy']]

def pdg_delta_process(df):
    return df[['failure_prone', 'group', 
               
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def pdg_iac_process(df):
    return df[['failure_prone', 'group', 
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def delta_iac_process(df):
    return df[['failure_prone', 'group', 
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

def pdg_iac_delta_process(df):
    return df[['failure_prone', 'group', 
               
               'maxPdgVertices', 'verticesCount','edgesCount','edgesToVerticesRatio','globalInput','globalOutput','directFanIn','indirectFanIn','directFanOut','indirectFanOut',
               
               'avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy',
               
               'delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy',
               
               'change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']]

