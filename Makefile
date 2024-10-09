image=cerit.io/ljocha/rassp
port=8070

flags=-v ${PWD}:/work -w /work --rm -ti -e HOME=/work --ulimit nofile=32768:32768
user=-u ${shell id -u} 
version=${shell cat VERSION}
amdflags=--device=/dev/kfd --device=/dev/dri --shm-size 16G --group-add video --group-add render
nvidiaflags=--gpus=all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --shm-size 16G
# --entrypoint=/usr/bin/python

build-amd:
	docker build -f Dockerfile.amd -t ${image}:amd .

build-nvidia:
	docker build -f Dockerfile.nvidia -t ${image}:nvidia-${version} .
	docker push ${image}:nvidia-${version}

run:
	docker run -ti ${flags} ${user} -p ${port}:${port} ${image}:amd jupyter lab --ip 0.0.0.0 --port ${port}

run-amd:
	docker run -ti ${flags} ${user} ${amdflags} -p ${port}:${port} ${image}:amd jupyter lab --ip 0.0.0.0 --port ${port}

bash-amd:
	docker run -ti ${flags} ${user} ${amdflags} ${image}:amd bash

root-amd:
	docker run -ti ${flags} ${amdflags} ${image}:amd bash

run-nvidia:
	docker run -ti ${flags} ${user} ${nvidiaflags} -p ${port}:${port} ${image}:nvidia-${version} jupyter lab --ip 0.0.0.0 --port ${port}

bash-nvidia:
	docker run -ti ${flags} ${user} ${nvidiaflags} ${image}:nvidia-${version} bash


