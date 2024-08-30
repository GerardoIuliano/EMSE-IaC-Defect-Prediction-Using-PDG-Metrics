import pandas as pd
import os, math

data = pd.read_csv(os.path.normpath(os.path.join(os.getcwd(), "output", "ansible.csv")))

repositories = set(data.repository)
file = list(data.filepath)

print("File totali",len(file))
somma = 0
for f in file:
    if(str(f).startswith("tasks") or str(f).startswith("handlers")):
        somma+=1
print("File che sono in cartella tasks o handlers",somma)

calcolata = 0
calcolata_startwith = 0

for index, row in data.iterrows():
    if not(
        math.isnan(row["lackOfCohesion"]) and 
        math.isnan(row["maxPdgVertices"]) and 
        math.isnan(row["verticesCount"]) and 
        math.isnan(row["edgesCount"]) and 
        math.isnan(row["globalInput"]) and 
        math.isnan(row["globalOutput"]) and 
        math.isnan(row["directFanIn"]) and 
        math.isnan(row["indirectFanIn"]) and 
        math.isnan(row["directFanOut"]) and 
        math.isnan(row["indirectFanOut"]) and 
        math.isnan(row["edgesToVerticesRatio"])
    ):
        calcolata+=1
        if(str(row["filepath"]).startswith("tasks") or str(row["filepath"]).startswith("handlers")):
            calcolata_startwith += 1
print("File per cui sono state estratte le metriche",calcolata)
print("File per cui sono state estratte le metriche e che stanno in tasks o handlers",calcolata_startwith)
        

print("Repo totali", len(repositories))
repo_numberFile_notAnalized = {}
repo_numberFile_analized = {}

for repo in repositories:
    rows = data[data.repository==repo]
    metric1 = rows.lackOfCohesion
    metric2 = rows.maxPdgVertices
    metric3 = rows.verticesCount
    metric4 = rows.edgesCount
    metric5 = rows.globalInput
    metric6 = rows.globalOutput
    metric7 = rows.directFanIn
    metric8 = rows.indirectFanIn
    metric9 = rows.directFanOut
    metric10 = rows.indirectFanOut
    metric11 = rows.edgesToVerticesRatio
    if(
        all(math.isnan(elemento) for elemento in metric1) and
        all(math.isnan(elemento) for elemento in metric2) and
        all(math.isnan(elemento) for elemento in metric3) and
        all(math.isnan(elemento) for elemento in metric4) and
        all(math.isnan(elemento) for elemento in metric5) and
        all(math.isnan(elemento) for elemento in metric6) and
        all(math.isnan(elemento) for elemento in metric7) and
        all(math.isnan(elemento) for elemento in metric8) and
        all(math.isnan(elemento) for elemento in metric9) and
        all(math.isnan(elemento) for elemento in metric10) and
        all(math.isnan(elemento) for elemento in metric11) 
    ):
        repo_numberFile_notAnalized[repo] = len(rows)
    else:
        repo_numberFile_analized[repo] = len(rows)
    
dizionario_ordinato_notAnalized = dict(sorted(repo_numberFile_notAnalized.items(), key=lambda item: item[1], reverse=True))
dizionario_ordinato_analized = dict(sorted(repo_numberFile_analized.items(), key=lambda item: item[1], reverse=True))

print("Repository non analizzate:",len(dizionario_ordinato_notAnalized))
print("File non analizzati:",sum(value for value in dizionario_ordinato_notAnalized.values()))


print("Repository analizzate:",len(dizionario_ordinato_analized))
print("Repository analizzate:",dizionario_ordinato_analized.keys())
#['PyratLabs/ansible-role-k3s', 'anthcourtney/ansible-role-cis-amazon-linux', 'ansible-ThoTeam/nexus3-oss', 'automium/service-kubernetes', 'oVirt/ovirt-ansible-hosted-engine-setup', 'riemers/ansible-gitlab-runner', 'ansistrano/deploy', 'elastic/ansible-elasticsearch', 'sensu/sensu-ansible', 'cloudalchemy/ansible-grafana', 'openstack/openstack-ansible-os_nova', 'CSCfi/ansible-role-slurm', 'openwisp/ansible-openwisp2', 'cloudalchemy/ansible-prometheus', 'ANXS/postgresql', 'openstack/openstack-ansible-rabbitmq_server', 'galaxyproject/ansible-galaxy', 'Oefenweb/ansible-percona-server', 'UnderGreen/ansible-role-mongodb', 'ansible-community/ansible-nomad', 'openstack/openstack-ansible-os_neutron', 'AlbanAndrieu/ansible-jenkins-slave', 'CoffeeITWorks/ansible_burp2_server', 'DataDog/ansible-datadog', 'oVirt/ovirt-ansible-disaster-recovery', 'stackbuilders/sb-debian-base', 'evrardjp/ansible-keepalived', 'cloudalchemy/ansible-node-exporter', 'HanXHX/ansible-nginx', 'viasite-ansible/ansible-role-zsh', 'lae/ansible-role-proxmox', 'HanXHX/ansible-debian-bootstrap', 'nusenu/ansible-relayor', 'DavidWittman/ansible-redis', 'cloudalchemy/ansible-alertmanager', 'aalaesar/install_nextcloud', 'Oefenweb/ansible-postfix', 'caktus/tequila-django', 'ansible-community/ansible-vault', 'florianutz/Ubuntu1804-CIS', 'dj-wasabi/ansible-telegraf', 'rvm/rvm1-ansible', 'cloudalchemy/ansible-blackbox-exporter', 'tulibraries/ansible-role-airflow', 'idealista/mysql_role', 'Graylog2/graylog-ansible-role', 'mrlesmithjr/ansible-netdata', 'willshersystems/ansible-sshd', 'idealista/consul_role', 'ansible-lockdown/RHEL7-STIG', 'stone-payments/ansible-rabbitmq', 'naftulikay/ansible-role-degoss', 'CSCfi/ansible-role-users', 'mrlesmithjr/ansible-manage-lvm', 'cloudalchemy/ansible-pushgateway', 'antoiner77/caddy-ansible', 'idealista/nexus-role', 'Oefenweb/ansible-supervisor', 'kibatic/ansible-traefik', 'arillso/ansible.logrotate', 'm4rcu5nl/ansible-role-zerotier', 'fgci-org/ansible-role-cuda', 'dokku/ansible-dokku', 'linux-system-roles/storage', 'florianutz/Ubuntu1604-CIS', 'idealista/java_role', 'diodonfrost/ansible-role-mariadb', 'newrelic/infrastructure-agent-ansible', 'elastic/ansible-beats', 'wcm-io-devops/ansible-conga-ansible-controlhost', 'stackhpc/ansible-role-os-images', 'infOpen/ansible-role-docker', 'stackhpc/ansible-role-libvirt-vm', 'nwoetzel/ansible-role-eclipse', 'mimacom/ansible-role-bamboo', 'AlexeySetevoi/ansible-clickhouse', 'hadret/ansible-role-containers', 'infOpen/ansible-role-fail2ban', 'cloudalchemy/ansible-smokeping_prober', 'galaxyproject/ansible-galaxy-tools']
print("File analizzati:",sum(value for value in dizionario_ordinato_analized.values()))



