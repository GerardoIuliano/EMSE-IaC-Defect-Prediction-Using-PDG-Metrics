For each repository, 20 models were constructed. 
Five models (Naive Bayes, Logistic Regression, SVC, Decision Tree, and Random Forest) were built for each of the 4 metrics (PDG, ICO, Process, Delta).

The configuration used is as follows:

'balance' = _search_params[“bal”][0]), # None
'balance' = _search_params[“bal”][1]), # RandomUnderSampler
'balance' = _search_params[“bal”][2]), # RandomOverSampler

'preprocessing' = _search_params[“pre”][0]), # None
'preprocessing' = _search_params[“pre”][1]), # MinMaxScaler
'preprocessing' = _search_params[“pre”][2]), # StandardScaler

Example
The folder “result_1_2” contains the results of models that use RandomUnderSampler as a balancing technique and StandardScaler for data standardization.
