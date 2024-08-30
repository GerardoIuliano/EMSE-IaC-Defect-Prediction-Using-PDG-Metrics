import json, os, csv

repository = ['PyratLabs/ansible-role-k3s', 'anthcourtney/ansible-role-cis-amazon-linux', 'ansible-ThoTeam/nexus3-oss', 'automium/service-kubernetes', 'oVirt/ovirt-ansible-hosted-engine-setup', 'riemers/ansible-gitlab-runner', 'ansistrano/deploy', 'elastic/ansible-elasticsearch', 'sensu/sensu-ansible', 'cloudalchemy/ansible-grafana', 'openstack/openstack-ansible-os_nova', 'CSCfi/ansible-role-slurm', 'openwisp/ansible-openwisp2', 'cloudalchemy/ansible-prometheus', 'ANXS/postgresql', 'openstack/openstack-ansible-rabbitmq_server', 'galaxyproject/ansible-galaxy', 'Oefenweb/ansible-percona-server', 'UnderGreen/ansible-role-mongodb', 'ansible-community/ansible-nomad', 'openstack/openstack-ansible-os_neutron', 'AlbanAndrieu/ansible-jenkins-slave', 'CoffeeITWorks/ansible_burp2_server', 'DataDog/ansible-datadog', 'oVirt/ovirt-ansible-disaster-recovery', 'stackbuilders/sb-debian-base', 'evrardjp/ansible-keepalived', 'cloudalchemy/ansible-node-exporter', 'HanXHX/ansible-nginx', 'viasite-ansible/ansible-role-zsh', 'lae/ansible-role-proxmox', 'HanXHX/ansible-debian-bootstrap', 'nusenu/ansible-relayor', 'DavidWittman/ansible-redis', 'cloudalchemy/ansible-alertmanager', 'aalaesar/install_nextcloud', 'Oefenweb/ansible-postfix', 'caktus/tequila-django', 'ansible-community/ansible-vault', 'florianutz/Ubuntu1804-CIS', 'dj-wasabi/ansible-telegraf', 'rvm/rvm1-ansible', 'cloudalchemy/ansible-blackbox-exporter', 'tulibraries/ansible-role-airflow', 'idealista/mysql_role', 'Graylog2/graylog-ansible-role', 'mrlesmithjr/ansible-netdata', 'willshersystems/ansible-sshd', 'idealista/consul_role', 'ansible-lockdown/RHEL7-STIG', 'stone-payments/ansible-rabbitmq', 'naftulikay/ansible-role-degoss', 'CSCfi/ansible-role-users', 'mrlesmithjr/ansible-manage-lvm', 'cloudalchemy/ansible-pushgateway', 'antoiner77/caddy-ansible', 'idealista/nexus-role', 'Oefenweb/ansible-supervisor', 'kibatic/ansible-traefik', 'arillso/ansible.logrotate', 'm4rcu5nl/ansible-role-zerotier', 'fgci-org/ansible-role-cuda', 'dokku/ansible-dokku', 'linux-system-roles/storage', 'florianutz/Ubuntu1604-CIS', 'idealista/java_role', 'diodonfrost/ansible-role-mariadb', 'newrelic/infrastructure-agent-ansible', 'elastic/ansible-beats', 'wcm-io-devops/ansible-conga-ansible-controlhost', 'stackhpc/ansible-role-os-images', 'infOpen/ansible-role-docker', 'stackhpc/ansible-role-libvirt-vm', 'nwoetzel/ansible-role-eclipse', 'mimacom/ansible-role-bamboo', 'AlexeySetevoi/ansible-clickhouse', 'hadret/ansible-role-containers', 'infOpen/ansible-role-fail2ban', 'cloudalchemy/ansible-smokeping_prober', 'galaxyproject/ansible-galaxy-tools']

def best_predictors_pdg():
    metrics = ["maxPdgVertices","lackOfCohesion","verticesCount","edgesCount","edgesToVerticesRatio","globalInput",
               "globalOutput","directFanIn","indirectFanIn","directFanOut","indirectFanOut"]

    selected_metric = {}
    ranked_metric = {}
    optimal_num = 0
    repo_analyzed = 0

    for m in metrics:
        selected_metric.setdefault(m,0)
    for m in metrics:
        ranked_metric.setdefault(m,0)

    for repo in repository:
        path = 'rq1/best_PDG_metrics/result/pdg/'+repo.replace("/","_")+'.json'
        if(os.path.exists(path)):
            repo_analyzed +=1
            # Apri il file JSON in modalità lettura
            with open(path, 'r') as file:
                # Carica il contenuto JSON dal file
                data = json.load(file)
                selected = data["selected"]
                for metric in selected:
                    selected_metric[metric] += 1
                ranked = data["ranked"]
                for rank in ranked:
                    ranked_metric[rank[1]] += int(rank[0])
                optimal_num += int(data["optimal_n"])
        else:
            print("NO ", path)

    optimal_num = round(optimal_num/repo_analyzed,2)

    selected_metric = dict(sorted(selected_metric.items(), key=lambda item: item[1], reverse=True))

    rows = []
    for m in selected_metric.keys():
        if(selected_metric[m]==0):
            selected_metric[m]=1
        ranked_metric[m] = round(ranked_metric[m]/selected_metric[m],2)  
        row = []
        row.append(m) 
        row.append(selected_metric[m]) 
        row.append(ranked_metric[m]) 
        row.append(optimal_num)
        rows.append(row)             

    # CSV file name
    csv_file = 'rq1/best_PDG_metrics/csv/best_predictors_pdg.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers row
        writer.writerow(["Metric", "Occurrences", "mean_Ranked", "mean_Optimal_n"])
        # Write the data row
        writer.writerows(rows)

def best_predictors_iac():
    metrics = ['avg_play_size','avg_task_size','lines_blank','lines_code','lines_comment','num_authorized_key',
               'num_block_error_handling','num_blocks','num_commands', 'num_conditions','num_decisions','num_deprecated_keywords',
               'num_deprecated_modules','num_distinct_modules','num_external_modules','num_fact_modules', 'num_file_exists',
               'num_file_mode','num_file_modules','num_filters','num_ignore_errors','num_import_playbook','num_import_role',
               'num_import_tasks', 'num_include','num_include_role','num_include_tasks','num_include_vars','num_keys','num_lookups',
               'num_loops','num_math_operations','num_names_with_vars', 'num_parameters','num_paths','num_plays','num_regex',
               'num_roles','num_suspicious_comments','num_tasks','num_tokens','num_unique_names','num_prompts', 'num_vars','text_entropy']

    selected_metric = {}
    ranked_metric = {}
    optimal_num = 0
    repo_analyzed = 0

    for m in metrics:
        selected_metric.setdefault(m,0)
    for m in metrics:
        ranked_metric.setdefault(m,0)

    for repo in repository:
        path = 'rq1/best_PDG_metrics/result/iac/'+repo.replace("/","_")+'.json'
        if(os.path.exists(path=path)):
            repo_analyzed +=1
            # Apri il file JSON in modalità lettura
            with open(path, 'r') as file:
                # Carica il contenuto JSON dal file
                data = json.load(file)
                selected = data["selected"]
                for metric in selected:
                    selected_metric[metric] += 1
                ranked = data["ranked"]
                for rank in ranked:
                    ranked_metric[rank[1]] += int(rank[0])
                optimal_num += int(data["optimal_n"])

    optimal_num = round(optimal_num/repo_analyzed,2)

    selected_metric = dict(sorted(selected_metric.items(), key=lambda item: item[1], reverse=True))

    rows = []
    for m in selected_metric.keys():#controllo divisione per zero
        if(selected_metric[m]==0):
            selected_metric[m]=1
        ranked_metric[m] = round(ranked_metric[m]/selected_metric[m],2)  
        row = []
        row.append(m) 
        row.append(selected_metric[m]) 
        row.append(ranked_metric[m]) 
        row.append(optimal_num)
        rows.append(row)             

    # CSV file name
    csv_file = 'rq1/best_PDG_metrics/csv/best_predictors_iac.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers row
        writer.writerow(["Metric", "Occurrences", "mean_Ranked", "mean_Optimal_n"])
        # Write the data row
        writer.writerows(rows)

def best_predictors_delta():
    metrics = ['delta_avg_play_size','delta_avg_task_size','delta_lines_blank','delta_lines_code',
               'delta_lines_comment','delta_num_authorized_key','delta_num_block_error_handling','delta_num_blocks','delta_num_commands',
               'delta_num_conditions','delta_num_decisions','delta_num_deprecated_keywords','delta_num_deprecated_modules',
               'delta_num_distinct_modules','delta_num_external_modules','delta_num_fact_modules','delta_num_file_exists',
               'delta_num_file_mode','delta_num_file_modules','delta_num_filters','delta_num_ignore_errors','delta_num_import_playbook',
               'delta_num_import_role','delta_num_import_tasks','delta_num_include','delta_num_include_role', 'delta_num_include_tasks',
               'delta_num_include_vars','delta_num_keys','delta_num_lookups','delta_num_loops','delta_num_math_operations',
               'delta_num_names_with_vars', 'delta_num_parameters','delta_num_paths','delta_num_plays','delta_num_regex',
               'delta_num_roles','delta_num_suspicious_comments','delta_num_tasks','delta_num_tokens','delta_num_unique_names',
               'delta_num_prompts', 'delta_num_vars','delta_text_entropy']

    selected_metric = {}
    ranked_metric = {}
    optimal_num = 0
    repo_analyzed = 0

    for m in metrics:
        selected_metric.setdefault(m,0)
    for m in metrics:
        ranked_metric.setdefault(m,0)

    for repo in repository:
        path = 'rq1/best_PDG_metrics/result/delta/'+repo.replace("/","_")+'.json'
        if(os.path.exists(path=path)):
            repo_analyzed +=1
            # Apri il file JSON in modalità lettura
            with open(path, 'r') as file:
                # Carica il contenuto JSON dal file
                data = json.load(file)
                selected = data["selected"]
                for metric in selected:
                    selected_metric[metric] += 1
                ranked = data["ranked"]
                for rank in ranked:
                    ranked_metric[rank[1]] += int(rank[0])
                optimal_num += int(data["optimal_n"])

    optimal_num = round(optimal_num/repo_analyzed,2)

    selected_metric = dict(sorted(selected_metric.items(), key=lambda item: item[1], reverse=True))

    rows = []
    for m in selected_metric.keys():
        if(selected_metric[m]==0):
            selected_metric[m]=1
        ranked_metric[m] = round(ranked_metric[m]/selected_metric[m],2)  
        row = []
        row.append(m) 
        row.append(selected_metric[m]) 
        row.append(ranked_metric[m]) 
        row.append(optimal_num)
        rows.append(row)             

    # CSV file name
    csv_file = 'rq1/best_PDG_metrics/csv/best_predictors_delta.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers row
        writer.writerow(["Metric", "Occurrences", "mean_Ranked", "mean_Optimal_n"])
        # Write the data row
        writer.writerows(rows)

def best_predictors_process():
    metrics = ['change_set_avg', 'change_set_max', 'code_churn_count', 'code_churn_avg', 
               'code_churn_max', 'commits_count', 'contributors_count', 'highest_contributor_experience', 'additions', 
               'additions_avg', 'additions_max', 'deletions', 'deletions_avg', 'deletions_max', 'hunks_median', 'minor_contributors_count']

    selected_metric = {}
    ranked_metric = {}
    optimal_num = 0
    repo_analyzed = 0

    for m in metrics:
        selected_metric.setdefault(m,0)
    for m in metrics:
        ranked_metric.setdefault(m,0)

    for repo in repository:
        path = 'rq1/best_PDG_metrics/result/process/'+repo.replace("/","_")+'.json'
        if(os.path.exists(path=path)):
            repo_analyzed +=1
            # Apri il file JSON in modalità lettura
            with open(path, 'r') as file:
                # Carica il contenuto JSON dal file
                data = json.load(file)
                selected = data["selected"]
                for metric in selected:
                    selected_metric[metric] += 1
                ranked = data["ranked"]
                for rank in ranked:
                    ranked_metric[rank[1]] += int(rank[0])
                optimal_num += int(data["optimal_n"])

    optimal_num = round(optimal_num/repo_analyzed,2)

    selected_metric = dict(sorted(selected_metric.items(), key=lambda item: item[1], reverse=True))

    rows = []
    for m in selected_metric.keys():
        if(selected_metric[m]==0):
            selected_metric[m]=1
        ranked_metric[m] = round(ranked_metric[m]/selected_metric[m],2)  
        row = []
        row.append(m) 
        row.append(selected_metric[m]) 
        row.append(ranked_metric[m]) 
        row.append(optimal_num)
        rows.append(row)             

    # CSV file name
    csv_file = 'rq1/best_PDG_metrics/csv/best_predictors_process.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers row
        writer.writerow(["Metric", "Occurrences", "mean_Ranked", "mean_Optimal_n"])
        # Write the data row
        writer.writerows(rows)

best_predictors_pdg()