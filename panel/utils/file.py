import uuid
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.core.files.uploadedfile import SimpleUploadedFile


def rename_file(file_name):
    return uuid.uuid4().hex + Path(file_name).suffix


def file_upload_path_generator(path):
    return lambda instance, file_name: Path(path) / rename_file(file_name)


def download_file(url):
    resp = requests.get(url)
    resp.raise_for_status()

    url_path = Path(urlparse(url).path)
    file_name = url_path.name

    if url_path.suffix == "":
        file_name += "." + resp.headers["content-type"].split("/")[1]

    return SimpleUploadedFile(file_name, resp.content)
