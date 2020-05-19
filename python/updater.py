"""
Python script with helper functions to pull docker images, re-tag with the mapping found
in a yaml file and push the new tags. For to use with the mappings found in this repository
simply call python updater.py
"""

import docker
import logging
import os
import yaml

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class DockerClient:

    def __init__(self):
        self.client = docker.from_env()
        self.docker_registry = os.getenv("DOCKER_REGISTRY")
        try:
            self.client.login(dockercfg_path="/.docker/config.json", username="applications", registry=self.docker_registry)
        except docker.errors.APIError as api_error:
            logging.info(f"Docker API error:\n{str(api_error)}")
            exit(1)

    def pull_tag_push(self, source="", target="", version=""):
        """ Pull the requested source image, re-tag it as the target and then push it """
        full_source = f"{source}:{version}"
        full_target = f"{target}:{version}"
        try:
            image = self.client.images.pull(full_source)
            if image.tag(target, tag=version):
                self.client.images.push(full_target)
                return True
            else:
                logging.info(f"Failed to tag image {source} as {target}")
                return False
        except docker.errors.APIError as api_error:
            logging.info(f"Docker API error:\n{str(api_error)}")
            exit(1)


def process_images(image_file_name):
    """ Load an images yaml file and pull_tag_push each entry """
    with open(image_file_name, "r") as file:
        doc = yaml.load(file)
        for image in doc["images"]:
            source = image["source"]
            target = f'{self.docker_registry}/{image["source"]}'
            version = image["version"]

            logging.info(f"Mirroring {source}:{version} as {target}:{version}")
            if docker_client.pull_tag_push(source=source, target=target, version=version):
                logging.info(f"Successfully mirrored {source}:{version} as {target}:{version}")
            else:
                logging.info(f"Failed to mirror {source}:{version} as {target}:{version}")
                exit(1)


if __name__ == "__main__":
    docker_client = DockerClient()
    process_images("images.yml")
