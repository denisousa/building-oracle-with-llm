import re
import os
import subprocess
from time import sleep
from dotenv import load_dotenv
load_dotenv()

extract_to_path = os.getenv('PROJECTS_PATH')

def create_one_cluster_elasticserach(folder_name):
    port = 9200
    elasticsearch_path = os.getenv('ELASTICSEARCH_CLUSTERS')


    command_delete = f'rm -rf {elasticsearch_path}/elasticsearch-ngram-{ngram}'
    command_unzip = f'tar -xvf {folder_name}.tar.gz -C {elasticsearch_path}'
    command_rename = f'mv {elasticsearch_path}/{folder_name} {elasticsearch_path}/elasticsearch-ngram-{ngram}'
    os.system(command_rename)
    elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/config/elasticsearch.yml'

    elasticsearch_in_sh_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/bin/elasticsearch.in.sh'


    os.system(command_delete)
    sleep(1)

    os.system(command_unzip)
    sleep(1)

    elasticsearch_yml_content = f'cluster.name: stackoverflow \nhttp.port: {port}'
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)

    elasticsearch_content = open(elasticsearch_in_sh_path, 'r').read()
    elasticsearch_new_content = elasticsearch_content.replace('256m', '4g').replace('1g', '6g')
    open(elasticsearch_in_sh_path, 'w').write(elasticsearch_new_content)

    print(f'\nCREATE ELASTICSEARCH elasticsearch-ngram-{ngram}\n')

def execute_cluster_elasticserach(ngram):
    elasticsearch_path = os.getenv('ELASTICSEARCH_CLUSTERS')
    command_execute = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch-ngram-{ngram}')
    process = subprocess.Popen(command_execute, shell=True, stdout=subprocess.PIPE)
    process.wait()
    sleep(7)

def stop_cluster_elasticserach():
    port = 9200
    command_stop = f'sudo fuser -k -n tcp {port}'
    print(f'STOP elasticsearch')
    process = subprocess.Popen(command_stop, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    process.wait()
