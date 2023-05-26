from . import errors
import subprocess
import os


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             universal_newlines=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def from_env():
    return Client()


class Client:
    def __init__(self):
        self.api = Api(self)
        self.images = Image(self)


class Api:
    def __init__(self, client):
        self._client = client

    def build(self, path: str, dockerfile: str, tag: str, decode: bool, platform: str):
        self._client._path = path
        self._client._tag = tag
        self._client._dockerfile = dockerfile
        self._client._platform = platform
        docker_buildx_command = 'docker buildx build {} --tag {} --file {} --platform {}'.format(
            path, tag, os.path.join(path, dockerfile), platform)
        return execute(docker_buildx_command)


class Image:
    def __init__(self, client):
        self._client = client

    def push(self, target_image, stream=True, decode=True):
        docker_buildx_command = 'docker buildx build {} --tag {} --file {} --platform {} --push'.format(
            self._client._path, self._client._tag, os.path.join(self._client._path, 
            self._client._dockerfile), self._client._platform)
        return execute(docker_buildx_command)