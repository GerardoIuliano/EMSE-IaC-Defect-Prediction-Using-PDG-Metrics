# EMSE-Infrastructure-as-Code-Defect-Prediction-Using-Program-Dependence-Graph-Metrics

## Overview

- **Context**: Infrastructure-as-code (IaC) is a DevOps practice that facilitates the management and provisioning of infrastructure by utilizing machine-readable files known as IaC scripts. Similarly to other types of source code artifacts, these scripts are susceptible to defects that may hinder their functionality.
- **Objective**: We conjecture that Program Dependency Graph (PDG) metrics may provide insights into the defectiveness of IaC scripts. Based on this conjecture, we propose to develop and empirically evaluate a new defect prediction model based on PDG metrics.
- **Method**: We extracted 11 PDG metrics from 139 open-source Ansible projects and trained five machine learners to assess their capabilities in a within-project scenario, other than comparing them with a state-of-the-art defect predictor relying on structural and process IaC-oriented metrics. Finally, we assessed the performance of a combined model that mixes PDG and existing IaC-oriented metrics.
- **Results**: The most occurring predictors are MAXPDGVERTICES, EDGESTOVERTICESRATIO, EDGESCOUNT, and VERTICESCOUNT. Program Dependence Graph metrics-based models trained using RANDOM FOREST and DECISION TREE perform statistically better than those relying on the remaining classifiers. PDG metrics-based models correctly predicted the number of bugs over 20% more than Delta and Process metrics-based models. Finally, PDG metrics can improve Delta and Process metrics' performance. However, such metrics have negligible effects on models employing ICO metrics.

## Repository Structure

- **Dockerfile**: This file contains the necessary instructions to build a Docker image to run the pipeline. This ensures a consistent and reproducible environment for executing the analysis.
- **input**: This folder contains the input file. It comprises all projects and commits with process, delta, and ICO metrics.
- **output**: This folder contains the output file. It comprises all projects and commits with process, delta, ICO, and PDG metrics. 
- **RQ1**: This folder contains all the files and scripts used to answer the first research question, including data and results related to RQ1.
- **RQ2**: This folder contains all the files and scripts used to answer the second research question, including data and results related to RQ2.

## Pipeline Steps

1. **Checkout at Commit**: The pipeline starts by checking out the project repository at a specific commit.
2. **Extraction of PDG at Project Level**: For the checked-out commit, a Program Dependency Graph (PDG) is extracted at the project level.
3. **Slicing the Project-Level PDG**: The project-level PDG is sliced to obtain file-level PDGs.
4. **Extraction of Metrics from File-Level PDGs**: Various metrics are extracted from the file-level PDGs.
5. **Next Commit or Project**: If another commit is available, the pipeline repeats from step 1. If no commits are left, it moves to the next project and restarts from step 1. If no projects are left, it ends.

## How to Use

### Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine.
- **Python**: Ensure Python is installed on your machine.

### Running the Pipeline

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
  
2. **Build Docker Image**:
   ```bash
   docker build -t <image-name> .

2. **Run Docker Image**:
   ```bash
   docker run -v output_volume:/output -v input_volume:/input <image-name>

## Results

**RQ1 Results**
  - **Best PDG Metrics**: The most effective PDG metrics identified during the analysis.

      | Metric                | Occurrences |
      |-----------------------|-------------|
      | MaxPDGVertices        | 57          |
      | VerticesCount         | 50          |
      | EdgesToVerticesRatio  | 42          |
      | EdgesCount            | 41          |
      | GlobalInput           | 38          |
      | LackOfCohesion        | 24          |
      | IndirectFanOut        | 19          |
      | IndirectFanIn         | 9           |
      | DirectFanOut          | 7           |
      | DirectFanIn           | 3           |
      | GlobalOutput          | 2           |

  - **Best Model Configuration**: The optimal configuration for the models used in the analysis.
    
      | Parameter             | Value          |
      |-----------------------|----------------|
      | Data Balancing        | None           |
      | Data Normalization    | Minmax Scaling |
    
  - **Best Model**: The best-performing model based on the analysis results.

      | Model                  | Occurrence     |
      |------------------------|----------------|
      | Random Forest          |    44          |
      | Decision Tree          |    44          |
      | Linear Regression      |    19          |
      | Support Vector Machine |    18          |
      | Naive Bayes            |    16          |

**RQ2 Results**
  - **Best Metric Combinations**: Predictive power of each metric set and their combinations.
    
      | Metric                  | Average Rank | Precision | Recall | MCC   |
      |-------------------------|--------------|-----------|--------|-------|
      | pdg+iac                 | 1.912        | 0.81      | 0.86   | 0.79  |
      | iac                     | 2.306        | 0.81      | 0.86   | 0.78  |
      | delta+iac               | 3.850        | 0.76      | 0.82   | 0.73  |
      | pdg+iac+process         | 3.887        | 0.76      | 0.81   | 0.73  |
      | pdg+delta+iac           | 3.237        | 0.75      | 0.81   | 0.72  |
      | iac+process             | 4.675        | 0.75      | 0.81   | 0.72  |
      | delta+iac+process       | 5.681        | 0.74      | 0.80   | 0.71  |
      | pdg+iac+delta+process   | 5.325        | 0.74      | 0.79   | 0.71  |
      | pdg                     | 6.475        | 0.73      | 0.76   | 0.66  |
      | pdg+delta               | 7.956        | 0.64      | 0.68   | 0.55  |
      | pdg+process             | 8.475        | 0.61      | 0.65   | 0.54  |
      | pdg+delta+process       | 9.150        | 0.59      | 0.63   | 0.50  |
      | delta+process           | 12.000       | 0.22      | 0.25   | 0.10  |
      | process                 | 12.006       | 0.21      | 0.25   | 0.10  |
      | delta                   | 12.531       | 0.17      | 0.24   | 0.06  |

