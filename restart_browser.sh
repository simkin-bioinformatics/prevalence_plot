#!/usr/bin/bash

PORT=1234
SIF_FILE='dash_server.sif'

singularity instance stop dash_server
singularity instance start -B $(pwd -P):$(pwd -P) $SIF_FILE dash_server $PORT

echo "running on port $PORT, if local can access at http://localhost:$PORT"
