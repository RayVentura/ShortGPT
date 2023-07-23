import os
import platform
import sys
import subprocess
def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

magick_path = get_program_path("magick")
if magick_path:
    os.environ['IMAGEMAGICK_BINARY'] = magick_path

import os

def is_running_in_colab():
    return 'COLAB_GPU' in os.environ

def handle_path(path):
    if 'https' in path:
        if is_running_in_colab():
            import requests
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(requests.get(path).content)
            temp_file.close()
            return temp_file.name
    return path
