#!/bin/bash

image=ljocha/rassp
version="$(cat VERSION)"
sif=/storage/brno3-cerit/home/ljocha/singularity/rassp_${version}.sif

flags="-v ${PWD}:/work -w /work --rm -ti -e HOME=/work --ulimit nofile=32768:32768 --shm-size=8G"
user="-u $(id -u)"
amdflags="--device=/dev/kfd --device=/dev/dri --shm-size 16G --group-add video --group-add render"
nvidiaflags="--gpus=all"

if [ $(basename $0) = predict-amd.sh ]; then
	docker run -ti ${flags} ${user} ${amdflags} ${image}:amd python3 predict.py "$@"

elif [ $(basename $0) = predict-nvidia.sh ]; then
	docker run -ti ${flags} ${user} ${nvidiaflags} ${image}:nvidia-${version} python3 predict.py "$@"

elif [ $(basename $0) = predict-singularity.sh ]; then
	CUDA_VISIBLE_DEVICES=$(nvidia-smi -L | grep $CUDA_VISIBLE_DEVICES | sed 's/^GPU \([0-9]*\):/\1/')
	singularity exec --nv -B ${SCRATCHDIR}:/work --pwd /work $sif /opt/nvidia/nvidia_entrypoint.sh python3 predict.py "$@"

else
	echo $0: WTF? >&2
	exit 1
fi

