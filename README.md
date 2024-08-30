# Infrastructure-as-Code Defect Prediction Using Program Dependence Graph Metrics
- **Context**: Infrastructure-as-code (IaC) is a DevOps practice that facilitates the management and provisioning of infrastructure by utilizing machine-readable files known as IaC scripts. Similarly to other types of source code artifacts, these scripts are susceptible to defects that may hinder their functionality.
- **Objective**: We conjecture that Program Dependence Graph (PDG) metrics may provide insights into the defectiveness of IaC scripts and, based on such a conjecture, we propose to develop and empirically evaluate a new defect prediction model based on PDG metrics.
- **Method**: We extracted 11 PDG metrics from 139 open-source Ansible projects and train five machine learners to assess their capabilities in a within-project scenario, other than comparing them with a state-of-the-art defect predictor relying on structural and process IaC-oriented metrics. Finally, we assessed the performance of a combined model that mixes together PDG and existing IaC-oriented metrics.
- **Results**: The most occurring predictors are MAXPDGVERTICES, EDGESTOVERTICESRATIO, EDGESCOUNT, and VERTICESCOUNT. Program Dependence Graph metrics-based models trained using RANDOM FOREST and DECISION TREE perform statistically better than those relying on the remaining classifiers. PDG metrics-based models correctly predicted the number of bugs over 20% more than Delta and Process metrics-based models. Finally, PDG metrics can improve the performance of Delta and Process metrics. However, such metrics have negligible effects on models employing ICO metrics.


Instruction

Il file Dockerfile consente l'esecuzione della pipeline. 
La pipeline analizza commit per commit i progetti ed esegue i seguenti step:
1- Checkout al commit
2- Estrazione del PDG a livello di progetto
3- Slicing del PDG a livello di progetto per ottenere PDGs a livello dei file
4- Estrazione delle metriche dal PDG
5- Commit successivo se presente, altrimenti progetto successivo

RQ1

La cartella RQ1 contiene i file utilizzati per rispondere alla prima domanda di ricerca. 

Results

Best PDG metrics
Best model configuration
Best model


