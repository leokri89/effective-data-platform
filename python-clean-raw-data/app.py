import logging

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)

import gzip
import json
import math
import os
import shutil
from datetime import datetime, timedelta

import click
import yaml
from google.cloud import storage


@click.command()
@click.argument("config")
def main(config):

    config = get_config(f"{config}")

    processed_folder = config.get("tmp_folder")
    projeto = config.get("projeto")
    transient_bucket_name = config.get("transient_bucket")
    raw_bucket_name = config.get("raw_bucket")

    extract_day = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    prefix = config.get("prefix").replace("{extract_day}", extract_day)

    download_client, download_bucket_obj = get_bucket(transient_bucket_name, projeto)
    bloblist = get_files_list(download_client, download_bucket_obj, prefix)
    check_path(processed_folder)

    process_uniques(bloblist, processed_folder)
    upload_client, upload_bucket_obj = get_bucket(raw_bucket_name, projeto)
    upload_processed_files(processed_folder, prefix, upload_bucket_obj)

    shutil.rmtree(processed_folder)
    logging.info(f"Process finished.")


def get_config(cpath):
    with open(cpath, "r") as cfile:
        config = yaml.safe_load(cfile)
    return config


def check_path(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)
        logging.info(f"Folder {folder} created.")
    else:
        logging.info(f"Folder {folder} already exists.")


def get_bucket(bucket, project):
    client = storage.Client()
    bucket = storage.Bucket(client, bucket, user_project=project)
    return client, bucket


def get_files_list(gcs_client, gcs_bucket, prefix):
    all_blobs = list(gcs_client.list_blobs(gcs_bucket, prefix=prefix))
    return all_blobs


def process_groups(flist):
    i = 0
    groups = []
    list_size = len(flist)
    k = math.ceil(1 + 3.3 * math.log(list_size))
    while k * i < list_size:
        lbound = k * i
        ubound = k * (i + 1)
        groups.append(flist[lbound:ubound])
        i = i + 1
    return groups


def download_data(blob_data):
    return blob_data.download_as_string()


def decompress_data(binary_data):
    return gzip.decompress(binary_data)


def load_string_list(data):
    return [
        json.dumps(x)
        for x in json.loads("[" + data.decode("utf-8").replace("}\n{", "},{") + "]")
    ]


def write_uniques(tmpfile, data, unique_hash):
    with gzip.open(tmpfile + ".gz", "wb") as file:
        for line in data:
            if hash(line) not in unique_hash:
                file.write((line + "\n").encode("utf-8"))
                unique_hash.add(hash(line))
    return unique_hash


def get_blobname(file):
    filename = file.name
    filename = filename.split("/")[len(filename.split("/")) - 1]
    return filename.split(".")[0]


def process_uniques(bloblist, processed_folder):
    uniques = set()

    for blob in bloblist:
        logging.info(f"Processing {blob.name}.")
        fname = get_blobname(blob)
        binary_data = download_data(blob)
        uncompressed_data = decompress_data(binary_data)
        data_as_list = load_string_list(uncompressed_data)
        uniques = write_uniques(
            f"{processed_folder}/{fname}.json", data_as_list, uniques
        )


def upload_processed_files(folder, prefix, upload_bucket_obj):
    for file in os.listdir(folder):
        if os.path.isfile(f"{folder}/{file}"):
            logging.info(f"Uploading file {file}.")
            blob = storage.Blob(f"{prefix}/{file}", upload_bucket_obj)
            blob.upload_from_filename(f"{folder}/{file}")


def clean_process_folder(folder):
    shutil.rmtree(folder)


if __name__ == "__main__":
    main()
