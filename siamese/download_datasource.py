import gdown
import zipfile
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

def delete_folder_or_file(filename_path):
    os.system(f'rm -rf {filename_path}')

def unzip_file(zip_file_path, extract_to_path):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to_path)

def unzip_targz_file(tar_gz_file_path, extract_to_path):
    command_unzip = f'tar -xvf {tar_gz_file_path} -C {extract_to_path}'
    os.system(command_unzip)

def download_stackoverflow(datasource):
    download_file_from_google_drive(datasource["file_id"], datasource["filename"])
    unzip_targz_file(datasource["filename"], extract_to_path)
    delete_folder_or_file(datasource["filename"])


def download_file_from_google_drive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

def download_elasticsearch_tar_gz():
    tar_gz_file = 'elasticsearch-2.2.0.tar.gz'
    
    if not os.path.isfile(tar_gz_file):
        os.system('wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.2.0/elasticsearch-2.2.0.tar.gz')
        shutil.move(tar_gz_file, extract_to_path)

extract_to_path = os.getenv('PROJECTS_PATH')
if not os.path.exists(extract_to_path):
    os.makedirs(extract_to_path)

datasource_list = [
    # {
    #     "filename": "projects_130901r_pt1+2+3",
    #     "file_id": "1D2tst0k18Z8L--nDLMOM2NSsj-T8Wn8M" 
    # },
    {
        "filename": "stackoverflow.tar.gz",
        "file_id": "1sfU6SBwFvVRp0QKecQeK_INaP7qrlAH3" 
    }
    # {
    #     "filename": "cut_stackoverflow_filtered.zip",
    #     "file_id": "19_9nkEytXVWt_GkLxAGdjwnJaGDGUT5n",
    # },
    # {
    #     "filename": "qualitas_corpus_clean.zip",
    #     "file_id": "1Cvm9pYddjB6_PzzqKUd0Ri6BV-fX6MuV",
    # },
    # {
    #     "filename": "mini_qualitas_corpus_clean.zip",
    #     "file_id": "1rph8OcDVUpBNycS_3x1bdouEX1zykdEL",
    # },
]

def download_projects():
    for datasource in datasource_list:

        if datasource["filename"] == "stackoverflow.tar.gz":
            download_stackoverflow(datasource)
            break
    
        download_file_from_google_drive(datasource["file_id"], datasource["filename"])
        unzip_file(datasource["filename"], extract_to_path)
        delete_folder_or_file(datasource["filename"])

    download_elasticsearch_tar_gz()

download_projects()