#!/usr/bin/bash

PORT=1234

singularity instance stop dash_server
singularity instance start dash.sif dash_server $PORT

echo "running on port $PORT, if local can access at http://localhost:$PORT"