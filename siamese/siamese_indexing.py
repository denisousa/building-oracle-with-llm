import os
import gc
import subprocess
from time import sleep
from dotenv import load_dotenv
import datetime

load_dotenv()

extract_to_path = os.getenv('PROJECTS_PATH')

def execute_siamese_index_properties():
    gc.collect()
    os.system("sync")

    port = 9200

    elasticsearch_folder = 'elasticsearch-2.2.0'
    if os.path.exists(f'{extract_to_path}/{elasticsearch_folder}'):
        os.system(f'rm -rf {extract_to_path}/{elasticsearch_folder}')

    tar_gz_file = 'elasticsearch-2.2.0.tar.gz'
    command_unzip = f'tar -xvf {extract_to_path}/{tar_gz_file} -C {extract_to_path}'
    os.system(command_unzip)

    elasticsearch_yml_path = f'{extract_to_path}/{elasticsearch_folder}/config/elasticsearch.yml'
    elasticsearch_yml_content = f'cluster.name: stackoverflow \nhttp.port: {port}'
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)

    command_execute = f'{extract_to_path}/{elasticsearch_folder}/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch')
    process = subprocess.Popen(command_execute, shell=True, stdout=subprocess.PIPE)
    process.wait()
    sleep(7)

    command = f"java -jar ./siamese/siamese-0.0.6-SNAPSHOT.jar -cf ./siamese/config-index.properties"
    process = subprocess.Popen(
        command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True
    )
    process.wait()

    command_stop = f'sudo fuser -k -n tcp {port}'
    print(f'STOP elasticsearch')
    process = subprocess.Popen(command_stop, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    process.wait()

def execute_indexing():
        start_time = datetime.datetime.now()
        execute_siamese_index_properties()
        end_time = datetime.datetime.now()

        exec_time = end_time - start_time
        print("Execution time:", exec_time)


execute_indexing()