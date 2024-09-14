#!/usr/bin/bash

PORT=1234
SIF_FILE='library://csimkin/dash/dash_server'

singularity instance stop dash_server
singularity instance start $SIF_FILE dash_server $PORT

echo "running on port $PORT, if local can access at http://localhost:$PORT"
