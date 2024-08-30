import os
import subprocess
import traceback
import project_pdg_info as info

def extract_pdg_repository_level(repository : str):
    repositories_path = os.path.normpath(os.path.join("input","repositories", repository))
    output_path = os.path.normpath(os.path.join(repositories_path, "PDG"))
    os.makedirs(output_path)
    try:
        command = f'poetry run python -m scansible build-pdg -f graphml {repositories_path}'
        output_file = f'{repositories_path}/PDG/graphml.txt'

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout

        # Salva l'output su file
        with open(output_file, 'w') as file:
            file.write(output)
            
        return info.is_repo_with_graph(repository)
    except:
        traceback.print_exc()
        return False