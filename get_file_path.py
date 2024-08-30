import pandas as pd
import re
import os

def getAllFilesPaths():
    data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "input", "ansible.csv")))

    repositories = data.repository
    files = data.filepath

    file_path = set(repositories+"/"+files)
    file_path = list(file_path)

    # remove github username from file path
    pattern = re.compile(r'^.*?/')
    file_path = [pattern.sub('', string) for string in file_path]

    return file_path

def getFilesFromRepo(repository_value):
    data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "input", "ansible.csv")))
    rows = data[data['repository'] == repository_value]
    return list(set(rows.filepath))    

def get_repo_names():
    data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "input", "ansible.csv")))
    repositories = data.repository
    repositories = set(repositories)
    list(repositories).sort
    repositories_names = repositories
    # remove github username from file path
    pattern = re.compile(r'^.*?/')
    repositories_names = [pattern.sub('', string) for string in repositories_names]
    return repositories_names

def get_repo_path():
    data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "input", "ansible.csv")))
    repositories = data.repository
    repositories = set(repositories)
    list(repositories).sort
    repositories_names = repositories
    return repositories_names