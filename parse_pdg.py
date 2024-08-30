import pandas as pd
import re
import os

def getRepoDictionary():
    data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "input", "ansible.csv")))
    repositories = data.repository
    repositories = set(repositories)
    githubName_repoName = repositories
    # remove github username from file path
    pattern = re.compile(r'^.*?/')
    repoDic = {}
    for string in githubName_repoName:
        repoDic[pattern.sub('', string)] = string
    return repoDic

