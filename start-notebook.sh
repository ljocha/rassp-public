#!/bin/bash

set -x

. /opt/jovyan/bin/activate
exec jupyterhub-singleuser --ip 0.0.0.0 --port 8888 "$@"
