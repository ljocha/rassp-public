#!/bin/bash

image=ljocha/rassp

flags="-v ${PWD}:/work -w /work --rm -ti -e HOME=/work --ulimit nofile=32768:32768"
user="-u $(id -u)"
version="$(cat VERSION)"
amdflags="--device=/dev/kfd --device=/dev/dri --shm-size 16G --group-add video --group-add render"
nvidiaflags="--gpus=all"

if [ $(basename $0) = predict-amd.sh ]; then
	docker run -ti ${flags} ${user} ${amdflags} ${image}:amd python3 predict.py "$@"

elif [ $(basename $0) = predict-nvidia.sh ]; then
	docker run -ti ${flags} ${user} ${nvidiaflags} -p ${port}:${port} ${image}:nvidia-${version} python3 predict.py "$@"

else
	echo $0: WTF? >&2
	exit 1
fi

