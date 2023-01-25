import docker

build_name = 'pythonapi'
version = 'v0.2.0'

client = docker.from_env()

image_list = client.images.list()
container_list = client.containers.list(all=True)

images = list()
for image in image_list:
    for tag in image.tags:
        if build_name in tag:
            images.append(image)

containers = []
for image in images:
    for container in container_list:
        if container.image == image:
            containers.append(container)

for container in containers:
    container.stop()
    container.remove()

for image in images:
    image.remove()

client.images.build(
    path = ".",
    dockerfile = "PythonAPI.Dockerfile",
    tag = f"{build_name}:{version}"
)